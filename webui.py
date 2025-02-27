import gradio as gr
from apis import MultiAgentPlanner
import json
import os
import time
from prompts import plan_agent_prompt, act_agent_prompt, summary_agent_prompt

# 定义图片输出目录
OUTPUT_DIR = "/share/home/wuqingyao_zhangboyang/GIS_Agent2"

# 确保输出目录存在
os.makedirs(OUTPUT_DIR, exist_ok=True)

def get_latest_image():
    """获取输出目录中最新的图片"""
    files = [os.path.join(OUTPUT_DIR, f) for f in os.listdir(OUTPUT_DIR) if f.endswith(('.png', '.jpg', '.jpeg'))]
    if not files:
        return None
    return max(files, key=os.path.getctime)

def process_query(query):
    agent = MultiAgentPlanner(plan_agent_prompt, act_agent_prompt, summary_agent_prompt)
    response = agent.process_query(query)
    formatted_response = json.dumps(response, ensure_ascii=False, indent=2)
    
    # 检查是否有新图片生成
    latest_image = get_latest_image()
    
    return formatted_response, latest_image if latest_image else None

def clear_inputs():
    return "", "", None

# 创建 Gradio 界面
demo = gr.Blocks(title="GIS 审核助手")

with demo:
    
    with gr.Row():
        with gr.Column(scale=1):
            gr.Image("/share/home/wuqingyao_zhangboyang/GIS_Agent2/img/1.jpg", width=200, height=100)
    
    gr.Markdown("# GIS 审核助手")
    gr.Markdown("这是一个基于大模型的建筑审核系统")
    
    with gr.Row():
        
        with gr.Column(scale=1):
            input_text = gr.Textbox(
                label="请输入您的查询",
                placeholder="例如：审核建筑xx是否符合建筑要求，并画出该建筑的图片。",
                lines=2
            )
            
            with gr.Row():
                submit_btn = gr.Button("提交查询")
                clear_btn = gr.Button("清除")
                
            output_text = gr.Textbox(
                label="查询结果",
                lines=10
            )
            
        with gr.Column(scale=1):
            image_output = gr.Image(
                label="生成的图片",
                type="filepath"
            )

    # 绑定事件
    submit_btn.click(
        fn=process_query,
        inputs=[input_text],
        outputs=[output_text, image_output]
    )
    
    clear_btn.click(
        fn=clear_inputs,
        inputs=[],
        outputs=[input_text, output_text, image_output]
    )

if __name__ == "__main__":
    demo.launch(
        server_name="0.0.0.0", 
        server_port=7860,
        share=False
    )