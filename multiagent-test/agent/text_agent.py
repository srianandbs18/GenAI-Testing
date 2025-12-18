"""
Text Responder Agent - Simple local agent for general text queries.

This is a basic LLM agent that handles general text responses.
Used as a local tool by the root agent.
"""

from google.adk.agents import Agent

# Simple text responder agent
text_agent = Agent(
    name="TextResponder",
    model="gemini-2.5-flash",
    instruction="""
    You are a helpful assistant. Provide clear, concise text responses to user questions.
    
    Your role:
    - Answer general questions
    - Provide explanations
    - Help with information requests
    - Be friendly and professional
    
    Keep responses concise and helpful.
    """
)
