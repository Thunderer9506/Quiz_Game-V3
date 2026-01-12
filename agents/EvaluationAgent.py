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
        try:
            groq_api_key = os.getenv("GROQ_API_KEY")
            if groq_api_key:
                os.environ['GROQ_API_KEY'] = groq_api_key
            self.model = ChatGroq(
                model=os.getenv("GROQ_MODEL"),
                temperature=0.8,
            )
            self.agent = create_agent(
                self.model,
                system_prompt=SystemMessage(sysMsg),
                checkpointer=InMemorySaver()
            )
        except Exception as e:
            raise RuntimeError(f"Failed to initialize EvaluationAgent: {e}")

        
    def evaluate(self,input:str,session:str):
        try:
            result = self.agent.invoke(
                {"messages": HumanMessage(input)},
                config={"configurable": {"thread_id": session}}
            )
            return result['messages'][-1].content
        except Exception as e:
            raise RuntimeError(f"Failed to evaluate answers: {e}")