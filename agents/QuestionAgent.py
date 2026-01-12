from langchain.agents import create_agent
from langchain_groq import ChatGroq
from langchain.messages import SystemMessage,HumanMessage
from langgraph.checkpoint.memory import InMemorySaver
import os
from dotenv import load_dotenv
from pydantic import BaseModel,Field
from typing import List
load_dotenv()

class Question(BaseModel):
    """Info About Question"""
    QuestionNumber: int = Field(description="Question number, Auto Incremented")
    Type: str = Field(description="Type of the Question")
    Category: str = Field(description="Category of the Question")
    Question: str = Field(description="Actual Question in text or markdown")
    Options: List[str] = Field(description="Options for the Question, Empty if Type is text")
    Correct: str = Field(description="Correct Answer for the Question, May vary if type is text")
    Difficulty: str = Field(description="Difficulty of the Question")

class QuestionList(BaseModel):
    """List of Questions"""
    questions: List[Question] = Field(description="List of quiz questions")

# Custom Error
class QuestionAgentError(Exception):
    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(self.message)


sysMsg = '''
You are an expert quiz question generator that creates high-quality, educational questions.

Generate exactly the number of questions requested by the user with these strict requirements:
- Question type: mcq, true/false, or text based answer
- Question must be factual, educational, and interesting
- Avoid meta-questions about quiz formats
- Include appropriate difficulty: easy, medium, or hard
- Use specific categories: science, history, geography, literature, math, technology, sports, or general
- For mcq: provide exactly 4 distinct, plausible options
- For true/false: provide exactly 2 options (True, False)
- For text based: provide empty options list
- Correct answer must be exact and unambiguous
- A single category must not repeat more then 3 times

Quality standards:
- Questions should test real knowledge
- Options should be similar in length and style
- Avoid "all of the above" or "none of the above"
- Make questions clear and specific

Follow the output schema strictly.
'''


class Agent:
    def __init__(self):
        try: 
            if os.getenv("GROQ_API_KEY"):
                os.environ['GROQ_API_KEY'] = os.getenv("GROQ_API_KEY")
            self.model = ChatGroq(
                model=os.getenv("GROQ_MODEL"),
                temperature=0.8,
            )
            self.agent = create_agent(
                self.model,
                system_prompt=SystemMessage(sysMsg),
                response_format=QuestionList,
                checkpointer=InMemorySaver()
            )
        except Exception as e:
            raise QuestionAgentError(f"Failed to initialize agent: {e}")
        
    def getQuestion(self, input: str,session:str):
        try:
            result = self.agent.invoke(
                {"messages": HumanMessage(input)},
                config={"configurable": {"thread_id": session}}
            )
            return result['structured_response']
        except Exception as e:
            raise QuestionAgentError(f"Failed to generate questions: {e}")
            