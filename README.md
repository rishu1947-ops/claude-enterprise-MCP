# Enterprise DevOps & Knowledge MCP Server for Claude

## Overview
This repository implements an advanced **Model Context Protocol (MCP)** server specifically designed to integrate **Claude Code** and **Claude Cowork** into secure, internal enterprise workflows. 

While standard LLM interfaces rely on static context, this server grants Claude secure, bounded execution capabilities to act as a fully autonomous **Internal DevOps & Knowledge Agent**.

## Core Architecture
This agent bridges scalable AI infrastructure with internal tools:
1. **Persistent Vector Memory (ChromaDB):** Replaces static prompt-stuffing by allowing Claude to semantically query an internal `.internal_kb` database of engineering wikis and architecture decisions on the fly.
2. **Asynchronous System Access:** Uses `asyncio` to allow Claude to perform non-blocking reads of local file systems and error logs without freezing the agent loop.
3. **Guardrailed Action Execution:** Uses `Pydantic` to enforce strict type-checking and schema validation before Claude is allowed to trigger internal CI/CD pipelines.

## Technologies Used
* **Framework:** `fastmcp` (Anthropic's MCP Standard)
* **Memory & RAG:** `chromadb`
* **Validation:** `pydantic`
* **Concurrency:** `asyncio`

## Setup & Running
1. Install dependencies: `pip install -r requirements.txt`
2. Initialize the internal vector database: `python init_kb.py`
3. Configure Claude Desktop / Claude Code to bind to this MCP server:

### Connecting to Claude Code (`claude.json` config)
To expose these tools to your local Claude Code CLI environment:
```json
{
  "mcpServers": {
    "enterprise-devops-agent": {
      "command": "python",
      "args":["/absolute/path/to/server.py"]
    }
  }
}
