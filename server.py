import asyncio
import os
import glob
from pydantic import BaseModel, Field
from fastmcp import FastMCP
import chromadb

# Initialize the MCP Server for Claude Code/Cowork
mcp = FastMCP("Enterprise_DevOps_Agent")

# Connect to local Vector DB
try:
    chroma_client = chromadb.PersistentClient(path="./.internal_kb")
    wiki_collection = chroma_client.get_collection(name="engineering_wikis")
except Exception as e:
    print(f"Warning: ChromaDB not initialized. Run init_kb.py first. Error: {e}")

# --- Pydantic Schemas for Strict Input Validation ---
class CIWorkflowParams(BaseModel):
    repository_name: str = Field(..., description="The name of the internal repo")
    branch: str = Field(..., description="The branch to deploy (e.g., main, staging)")
    force_build: bool = Field(default=False, description="Whether to bypass the cache")

# --- Complex Agent Tools ---

@mcp.tool()
async def semantic_search_internal_wiki(query: str, n_results: int = 2) -> str:
    """Perform a semantic vector search over the internal engineering wiki."""
    try:
        results = wiki_collection.query(
            query_texts=[query],
            n_results=n_results
        )

        docs = results.get('documents')
        if not docs or not docs[0]:
            return "No relevant internal documents found."
        
        formatted_context = "\n---\n".join(docs[0])
        return f"Retrieved Internal Context:\n{formatted_context}"
    except Exception as e:
        return f"Error querying vector database: {str(e)}"

@mcp.tool()
async def scan_local_error_logs(directory: str = "/var/log", file_extension: str = "*.log") -> str:
    """Simulates async traversal of local file systems to fetch recent error logs."""
    safe_dir = "./mock_logs" if directory == "/var/log" else directory
    os.makedirs(safe_dir, exist_ok=True)
    
    search_pattern = os.path.join(safe_dir, file_extension)
    files = glob.glob(search_pattern)
    
    if not files:
        return f"No log files found matching {search_pattern}."
        
    summary = []
    for file in files[:3]: 
        with open(file, 'r') as f:
            content = f.read()[-500:] 
            summary.append(f"File: {file}\nTail: ...{content}")
            
    return "\n\n".join(summary)

@mcp.tool()
async def trigger_ci_pipeline(params: str) -> str:
    """Triggers an internal CI/CD pipeline using strict JSON validation."""
    try:
        # Pydantic validation step
        validated_data = CIWorkflowParams.model_validate_json(params)
        
        # Mocking the async network request
        await asyncio.sleep(1) 
        
        return f"✅ SUCCESS: Triggered build for {validated_data.repository_name} on branch '{validated_data.branch}'. Force: {validated_data.force_build}. Build ID: #8492"
    except Exception as e:
        return f"❌ FAILED: Invalid parameters. Ensure JSON matches schema. Error: {str(e)}"

if __name__ == "__main__":
    mcp.run()