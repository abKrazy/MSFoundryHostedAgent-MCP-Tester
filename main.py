import os
from dotenv import load_dotenv
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient

# Load environment variables from .env file
load_dotenv()

# Configuration from environment
AZURE_AI_ENDPOINT = os.getenv("AZURE_AI_ENDPOINT")
AGENT_NAME = os.getenv("AGENT_NAME")
DEBUG = os.getenv("DEBUG", "false").lower() == "true"

if not AZURE_AI_ENDPOINT:
    raise ValueError("AZURE_AI_ENDPOINT is required. Set it in .env file.")
if not AGENT_NAME:
    raise ValueError("AGENT_NAME is required. Set it in .env file.")

project_client = AIProjectClient(
    endpoint=AZURE_AI_ENDPOINT,
    credential=DefaultAzureCredential(),
)

# Get an existing agent
agent = project_client.agents.get(agent_name=AGENT_NAME)
print(f"Retrieved agent: {agent.name}")

openai_client = project_client.get_openai_client()

def run_agent_with_mcp_approval(user_input, previous_response_id=None):
    """Run agent and handle MCP approval requests"""
    
    # Build the request
    request_params = {
        "input": [{"role": "user", "content": user_input}],
        "extra_body": {"agent": {"name": agent.name, "type": "agent_reference"}},
    }
    
    # If continuing a conversation, include the previous response ID
    if previous_response_id:
        request_params["previous_response_id"] = previous_response_id
    
    response = openai_client.responses.create(**request_params)
    
    if DEBUG:
        print(f"Response ID: {response.id}")
    
    # Check if there are MCP approval requests that need handling
    while True:
        mcp_approvals = []
        for item in response.output:
            if hasattr(item, 'type') and item.type == 'mcp_approval_request':
                if DEBUG:
                    print(f"Found MCP approval request: {item.id} for {item.name} on server {item.server_label}")
                mcp_approvals.append({
                    "type": "mcp_approval_response",
                    "approve": True,
                    "approval_request_id": item.id
                })
        
        if not mcp_approvals:
            # No more approvals needed, we're done
            break
        
        if DEBUG:
            print(f"Approving {len(mcp_approvals)} MCP tool call(s)...")
        
        # Continue the conversation with approvals
        response = openai_client.responses.create(
            input=mcp_approvals,
            extra_body={"agent": {"name": agent.name, "type": "agent_reference"}},
            previous_response_id=response.id,
        )
        
        if DEBUG:
            print(f"Continued response ID: {response.id}")
    
    return response

# Interactive conversation loop
print(f"\n{AGENT_NAME}")
print("Type 'quit' or 'exit' to end the conversation\n")

previous_response_id = None

while True:
    try:
        user_input = input("You: ").strip()
    except (EOFError, KeyboardInterrupt):
        print("\nGoodbye!")
        break
    
    if not user_input:
        continue
    
    if user_input.lower() in ['quit', 'exit', 'q']:
        print("Goodbye!")
        break
    
    response = run_agent_with_mcp_approval(user_input, previous_response_id=previous_response_id)
    print(f"\nAgent: {response.output_text}\n")
    
    # Save response ID to continue conversation
    previous_response_id = response.id