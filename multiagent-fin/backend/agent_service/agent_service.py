from fastapi import FastAPI, HTTPException, status, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import asyncio
from agents import Runner, trace
from agents.exceptions import InputGuardrailTripwireTriggered
from agents_.agent_definitions import create_agents

# Initialize agents once (singleton pattern)
_AGENT_INSTANCE = None

def get_agent():
    global _AGENT_INSTANCE
    if _AGENT_INSTANCE is None:
        print("Initializing agents...")
        _AGENT_INSTANCE = create_agents()
    return _AGENT_INSTANCE

class QueryRequest(BaseModel):
    query: str
    session_id: str = "default"
    previous_response_id: str = None

class QueryResponse(BaseModel):
    text: str
    response_id: str

app = FastAPI(title="Finance Agent Service")

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/query", response_model=QueryResponse)
async def handle_query(request: QueryRequest):
    print(f"\n🔹 Received query request:")
    print(f"   • Query: {request.query}")
    print(f"   • Session ID: {request.session_id}")
    print(f"   • Previous Response ID: {request.previous_response_id}")

    agents = get_agent()
    print("✅ Agents loaded successfully.")

    try:
        print("🚀 Running agent with input query...")
        with trace(workflow_name="Financial_Analysis", group_id=request.session_id):
            result = await Runner.run(
                agents["start_language_agent"],
                request.query,
                previous_response_id=request.previous_response_id
            )
        print("✅ Agent completed processing.")
        print(f"🔹 Final output:\n{result.final_output}\n")

        return QueryResponse(
            text=result.final_output,
            response_id=result.id if hasattr(result, "id") else "no_id"
        )

    except InputGuardrailTripwireTriggered as e:
        print("⛔ Input blocked by guardrail:", str(e))
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Guardrail triggered: {str(e)}"
        )
    except Exception as e:
        print("🔥 Agent processing error:")
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Agent processing error: {str(e)}"
        )

@app.post("/reset")
async def reset_agents():
    global _AGENT_INSTANCE
    _AGENT_INSTANCE = None
    return {"status": "Agents reset successfully"}