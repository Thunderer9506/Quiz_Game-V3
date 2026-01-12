from langchain.agents import create_agent
from langchain_groq import ChatGroq
from langchain.messages import SystemMessage,HumanMessage
from langgraph.checkpoint.memory import InMemorySaver
import os
from dotenv import load_dotenv
load_dotenv()
    
sysMsg = '''
You are an expert at evaluating a candidate's performance in a mock test.
you are given a list of questions and the answers provided by the candidate.
'''

class Agent:
    def __init__(self):
        os.environ['GROQ_API_KEY'] = os.getenv("GROQ_API_KEY") #type:ignore
        self.model = ChatGroq(
            model=os.getenv("GROQ_MODEL"),
            temperature=0.8,
        )
        self.agent = create_agent(
            self.model,
            system_prompt=SystemMessage(sysMsg),
            checkpointer=InMemorySaver()
        )
        
        
    def evaluate(self,input:str,session:str):
        result = self.agent.invoke({"messages": HumanMessage(input)},
                            config={"configurable": {"thread_id": session}}
                        )
        return result['messages'][-1].content
    