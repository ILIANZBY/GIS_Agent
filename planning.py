from prompts import plan_agent_prompt, act_agent_prompt, summary_agent_prompt
from apis import MultiAgentPlanner


if __name__ == "__main__":


    planner=MultiAgentPlanner(plan_agent_prompt=plan_agent_prompt,act_prompt=act_agent_prompt,summary_agent_prompt=summary_agent_prompt)
    
    planner.run(text='建筑5的面积应该小于300平方，高度应该小于6',query='审核建筑5是否符合建筑要求，并画出建筑5的图片。')

