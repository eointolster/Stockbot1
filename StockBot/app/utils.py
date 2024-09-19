import os
import anthropic
import aiohttp
from dotenv import load_dotenv
import logging
import asyncio
import json

load_dotenv()

claude_api_key = os.getenv("ANTHROPIC_API_KEY")
brave_api_key = os.getenv("BRAVE_API_KEY")

if not claude_api_key:
    raise ValueError("ANTHROPIC_API_KEY is not set in the environment variables")
if not brave_api_key:
    raise ValueError("BRAVE_API_KEY is not set in the environment variables")

claude_client = anthropic.Anthropic(api_key=claude_api_key)

logger = logging.getLogger(__name__)

async def brave_search(query):
    headers = {"Accept": "application/json", "X-Subscription-Token": brave_api_key}
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(
                "https://api.search.brave.com/res/v1/web/search",
                params={"q": query},
                headers=headers
            ) as response:
                response.raise_for_status()
                return await response.json()
    except aiohttp.ClientError as e:
        logger.error(f"Error in Brave Search: {str(e)}")
        raise

async def get_claude_response(message, conversation_history):
    system_message = "You are an AI assistant specializing in stock market analysis. Provide factual, data-driven responses without caveats or disclaimers. Focus on current stock performance, recent news, and key financial metrics. Structure your response with a brief summary followed by a detailed analysis. At the end, provide your opinion as either THUMBS_UP or THUMBS_DOWN based on the overall outlook. If you need to search for information, you can use the format: [SEARCH: your search query]."

    messages = conversation_history + [
        {
            "role": "user",
            "content": message
        }
    ]

    try:
        response = await asyncio.to_thread(
            claude_client.messages.create,
            model="claude-3-5-sonnet-20240620",
            max_tokens=1000,
            messages=messages,
            system=system_message
        )

        if response.content and "[SEARCH:" in response.content[0].text:
            search_query = response.content[0].text.split("[SEARCH:", 1)[1].split("]", 1)[0].strip()
            try:
                search_results = await brave_search(search_query)
                
                messages.append({
                    "role": "assistant",
                    "content": f"I need to search for: {search_query}"
                })
                messages.append({
                    "role": "user",
                    "content": f"Here are the search results: {json.dumps(search_results)}"
                })
                
                final_response = await asyncio.to_thread(
                    claude_client.messages.create,
                    model="claude-3-5-sonnet-20240620",
                    max_tokens=1000,
                    messages=messages,
                    system=system_message
                )
                return parse_response(final_response.content[0].text)
            except Exception as e:
                logger.error(f"Error in brave_search: {str(e)}")
                return {
                    "summary": "An error occurred while searching.",
                    "detailed_analysis": f"Error details: {str(e)}",
                    "ai_opinion": "THUMBS_DOWN"
                }
        elif response.content:
            return parse_response(response.content[0].text)
        else:
            return {
                "summary": "I'm sorry, but I couldn't generate a response.",
                "detailed_analysis": "Please try again.",
                "ai_opinion": "THUMBS_DOWN"
            }
    except Exception as e:
        logger.error(f"Error in get_claude_response: {str(e)}", exc_info=True)
        return {
            "summary": "An error occurred while processing your request.",
            "detailed_analysis": f"Error details: {str(e)}",
            "ai_opinion": "THUMBS_DOWN"
        }

def parse_response(content):
    parts = content.split("\n\n", 1)
    opinion = "THUMBS_UP" if "THUMBS_UP" in content else "THUMBS_DOWN"
    content = content.replace("THUMBS_UP", "").replace("THUMBS_DOWN", "").strip()
    
    if len(parts) > 1:
        return {"summary": parts[0], "detailed_analysis": parts[1], "ai_opinion": opinion}
    else:
        return {"summary": content, "detailed_analysis": "", "ai_opinion": opinion}