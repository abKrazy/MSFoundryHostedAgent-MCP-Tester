# FHA-MCP-Tester: Test Microsoft Foundry Hosted Agents in the terminal with auto-approval for MCP tool use.

This utility allows you to interact with a Microsoft Foundry hosted agent that uses MCP (Model Context Protocol) tools from the terminal. It provides an interactive conversation experience with automatic tool call approvals.

## Features

- **Interactive conversations** - Multi-turn chat with any Microsoft Foundry hosted agent
- **MCP tool support** - Automatically approves MCP tool calls, enabling seamless agent workflows
- **Configurable** - Easy setup via `.env` file for different agents and projects

## Prerequisites

- Python 3.10+
- Azure subscription with AI Foundry access
- An existing Foundry agent configured with MCP tools
- Azure CLI logged in (`az login`)

## Setup

1. Clone this repository

2. Install dependencies:
   ```bash
   pip install azure-ai-projects azure-identity python-dotenv
   ```

3. Create your environment file:
   ```bash
   cp .env.example .env
   ```

4. Edit `.env` with your values:
   ```
   AZURE_AI_ENDPOINT=https://your-resource.services.ai.azure.com/api/projects/your-project
   AGENT_NAME=Your-Agent-Name
   DEBUG=false
   ```

## Usage

Run the CLI:
```bash
python main.py
```

Then interact with your agent:
```
You: Get details for incident INC0010000
Agent: Here are the details for Incident INC0010000...

You: Show me the work notes
Agent: Here's the work note history...

You: quit
```

Type `quit`, `exit`, or `q` to end the session.

## Configuration

| Variable | Required | Description |
|----------|----------|-------------|
| `AZURE_AI_ENDPOINT` | Yes | Your Azure AI Foundry project endpoint |
| `AGENT_NAME` | Yes | Name of the Foundry agent to use |
| `DEBUG` | No | Set to `true` to show response IDs and MCP approval details |

## How It Works

When a Foundry agent uses MCP tools, the API returns approval requests before executing tool calls. This CLI automatically approves these requests and continues the conversation, providing a seamless interactive experience in the terminal similar to the Foundry UI.

## License

MIT
