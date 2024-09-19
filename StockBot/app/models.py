from pydantic import BaseModel

class ChatMessage(BaseModel):
    content: str
    user_comments: str

class AIResponse(BaseModel):
    summary: str
    detailed_analysis: str
    ai_opinion: str

class CombinedAnalysis(BaseModel):
    summary: str
    detailed_analysis: str

class ChatResponse(BaseModel):
    ai_response: AIResponse
    combined_analysis: CombinedAnalysis