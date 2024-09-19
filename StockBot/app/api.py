from fastapi import APIRouter, HTTPException
from .models import ChatMessage, ChatResponse, AIResponse, CombinedAnalysis
from .utils import get_claude_response
import logging

router = APIRouter()

conversation_history = []

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@router.post("/chat", response_model=ChatResponse)
async def chat(message: ChatMessage):
    global conversation_history
    try:
        # First AI process: Analyze the stock
        ai_response = await get_claude_response(f"Analyze the stock: {message.content}", conversation_history)
        
        # Second AI process: Combine AI analysis with user comments
        combined_prompt = f"Given the following AI analysis of {message.content} stock:\n\n{ai_response['summary']}\n\n{ai_response['detailed_analysis']}\n\nAnd considering this user comment: '{message.user_comments}'\n\nProvide a combined analysis that takes into account both the AI analysis and the user's perspective."
        combined_analysis = await get_claude_response(combined_prompt, conversation_history)
        
        # Update conversation history
        conversation_history.append({"role": "user", "content": message.content})
        conversation_history.append({"role": "assistant", "content": f"{ai_response['summary']}\n\n{ai_response['detailed_analysis']}"})
        conversation_history.append({"role": "user", "content": f"User comment: {message.user_comments}"})
        conversation_history.append({"role": "assistant", "content": f"{combined_analysis['summary']}\n\n{combined_analysis['detailed_analysis']}"})
        
        # Keep only the last 20 messages in the history
        if len(conversation_history) > 20:
            conversation_history = conversation_history[-20:]
        
        return ChatResponse(
            ai_response=AIResponse(**ai_response),
            combined_analysis=CombinedAnalysis(**combined_analysis)
        )
    except Exception as e:
        logger.error(f"Error in chat endpoint: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="An internal server error occurred. Please try again later.")