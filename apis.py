import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.getcwd(), "..")))
from langchain.prompts import PromptTemplate
from prompts import plan_agent_prompt, act_agent_prompt, summary_agent_prompt
import openai
from observation import observate
from document_processor import DocumentProcessor  




class MultiAgentPlanner:
    def __init__(self,
                 plan_agent_prompt: PromptTemplate = plan_agent_prompt,
                 act_prompt: PromptTemplate = act_agent_prompt,
                 summary_agent_prompt: PromptTemplate = summary_agent_prompt,
                 ) -> None:
        
        self.plan_prompt = plan_agent_prompt
        self.act_prompt = act_prompt
        self.summary_prompt = summary_agent_prompt
        self.scratchpad = ''
        self.query = None
        self.max_steps = 3
        self.reset()
        self.finished = False
        self.answer = ''
        self.client = openai.Client(api_key='none', base_url="http://localhost:9876/v1")
        
    # def llm(self, text):
    #     try:
    #         response=self.client.chat.completions.create(
    #             model="qwen2.5-instruct",
    #             messages=[{"role": "user", "content": text}],
    #             max_tokens=8000,
    #             temperature=0,
    #             )
    #         return response.choices[0].message
    
    def llm(self, text):
        try:
            response=self.client.chat.completions.create(
                model="qwen2-vl-instruct",
                messages=[{"role": "user", "content": text}],
                max_tokens=8000,
                temperature=0.05,
                )
            return response.choices[0].message        
            
    
        except Exception as e:
            print(e)
            
        return response.choices[0].message




    def run(self, text, query, reset = True) -> None:

        self.query = query
        self.text = text


        self.step()
        return self.answer, self.scratchpad

    
    def step(self) -> None:
        # Plan
        self.scratchpad += f'\nPlan :'
        plan=self.llm(self._build_plan_prompt()).content
        self.scratchpad += ' ' + plan
        print('PLAN:',plan)

        # Act
        self.scratchpad += f'\nAction :'
        action = self.llm(self._build_action_prompt()).content
        self.scratchpad += ' ' + action
        print('ACTION:',action)

        # Observe
        self.scratchpad += f'\nObservation : '
        observation=observate(action)
        observation_str = str(observation) if isinstance(observation, list) else observation
        self.scratchpad += ' ' + observation_str
        print("OBS",observation)

 
        # Sum
        self.scratchpad += f'\nSummary :'
        sum = self.llm(self._build_summary_prompt()).content
        self.scratchpad += ' ' + sum
        print("SUM",sum)


    
                
    def _build_plan_prompt(self) -> str:
        return self.plan_prompt.format(
                            query = self.query,
                            text = "",
                            scratchpad = self.scratchpad)
        
    def _build_action_prompt(self) -> str:
              return self.act_prompt.format(
                            query = self.query,
                            text = "",
                            scratchpad = self.scratchpad)  
    
    def _build_summary_prompt(self) -> str:
        return self.summary_prompt.format(
                            query = self.query,
                            text = self.text,
                            scratchpad = self.scratchpad)
    
    def is_finished(self) -> bool:
        return self.finished

    def is_halted(self) -> bool:
        return ((self.curr_step > self.max_steps) or (
                    len(self.enc.encode(self._build_agent_prompt())) > 14000)) and not self.finished

    def reset(self) -> None:
        self.scratchpad = ''
        self.answer = ''
        self.curr_step = 1
        self.finished = False
        
    def process_query(self, query, doc_content=None):
        """
        处理用户查询的主要函数
        """
        try:
            self.reset()
            

            text = doc_content
            
            answer, scratchpad = self.run(text=text, query=query)
            return scratchpad

        except Exception as e:
            return {
                "status": "error",
                "error": str(e),
                "query": query
            }

def format_step(step: str) -> str:
    return step.strip('\n').strip().replace('\n', '')






    