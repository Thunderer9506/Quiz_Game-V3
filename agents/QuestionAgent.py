from langchain.agents import create_agent
from langchain_groq import ChatGroq
from langchain.messages import SystemMessage,HumanMessage
from langgraph.checkpoint.memory import InMemorySaver
import os
from dotenv import load_dotenv
from pydantic import BaseModel,Field
load_dotenv()

class Question(BaseModel):
    """Info About Question"""
    Question: str = Field(description="Actual Question in text or markdown")
    QuestionNumber: int = Field(description="Question Number")
    Difficulty: str = Field(description="Difficulty of the Question")

class UserContext(BaseModel):
    Role: str
    Year: int

sysMsg = '''

'''
class Agent:
    def __init__(self):
        os.environ['GROQ_API_KEY'] = os.getenv("GROQ_API_KEY") #type:ignore
        self.model = ChatGroq(
            model="openai/gpt-oss-120b",
            temperature=0.5,
            timeout=30,
            max_tokens=1000,
        )
        
    def initAgent(self, sessionId, role, year):
        self.sessionId = sessionId
        self.role = role
        self.year = year
        self.agent = create_agent(
            self.model,
            system_prompt=SystemMessage(sysMsg.format(self.role, self.year)),
            response_format=Question,
            context_schema=UserContext,
            checkpointer=InMemorySaver()
            )

    def getQuestion(self,input: str):
        if input == "exit":
            return "Interview End"
        
        response = self.agent.invoke( 
                        {"messages":HumanMessage(input)}, #type:ignore
                        config={"context":UserContext(Role=self.role,Year=self.year),#type:ignore
                                "configurable":{"thread_id": self.sessionId}},
                    ) 
        output = response['structured_response']
        return output