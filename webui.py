import gradio as gr
from apis import MultiAgentPlanner
import json
import os
import time
from prompts import plan_agent_prompt, act_agent_prompt, summary_agent_prompt
import tempfile
from observation import load_gdf 
import shutil 
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

#添加上传文件组件
# def process_query(query, uploaded_files):
#     """处理查询并加载用户上传的文件"""
#     try:
#         # 临时保存上传的文件
#         temp_dir = tempfile.mkdtemp()
#         for file in uploaded_files:
#             file_path = os.path.join(temp_dir, os.path.basename(file.name))
#             # 读取临时文件内容并保存
#         with open(file.name, "rb") as temp_file:  #  使用 .name 获取临时文件路径
#             content = temp_file.read()
#         with open(file_path, "wb") as f:
#             f.write(content)  #  写入字节流
        
#         # 加载Shapefile（自动识别主文件）
#         shp_files = [f for f in os.listdir(temp_dir) if f.endswith(".shp")]
#         if not shp_files:
#             raise ValueError("未找到有效的.shp文件")
        
#         shp_path = os.path.join(temp_dir, shp_files[0])

def process_query(query, uploaded_files):
    """处理查询并加载用户上传的文件"""
    try:
        # 临时保存上传的文件
        temp_dir = tempfile.mkdtemp()
        
        # 修改文件保存逻辑
        for file in uploaded_files:
            file_path = os.path.join(temp_dir, os.path.basename(file.name))
            # 直接复制上传的文件到临时目录
            shutil.copy2(file.name, file_path)
        
        # 检查必要的文件是否都存在
        base_files = set([os.path.splitext(f)[0] for f in os.listdir(temp_dir)])
        for base in base_files:
            required_exts = ['.shp', '.shx', '.dbf']
            if all(os.path.exists(os.path.join(temp_dir, base + ext)) for ext in required_exts):
                shp_path = os.path.join(temp_dir, base + '.shp')
                break
        else:
            raise ValueError("未找到完整的Shapefile文件集（需要.shp、.shx、.dbf文件）")

        load_gdf(shp_path)  # 调用动态加载函数
        
        # 执行原有逻辑
        agent = MultiAgentPlanner(plan_agent_prompt, act_agent_prompt, summary_agent_prompt)
        response = agent.process_query(query)
        formatted_response = json.dumps(response, ensure_ascii=False, indent=2)
        
        # 清理临时文件
        for f in os.listdir(temp_dir):
            os.remove(os.path.join(temp_dir, f))
        os.rmdir(temp_dir)
        
        # 获取图片
        latest_image = get_latest_image()
        return formatted_response, latest_image if latest_image else None
    
    except Exception as e:
        return json.dumps({"error": str(e)}, ensure_ascii=False), None

# with demo:
    
#     with gr.Row():
#         with gr.Column(scale=1):
#             gr.Image("/share/home/wuqingyao_zhangboyang/GIS_Agent2/img/logistic.svg", width=200, height=100)
#             gr.Markdown("# GIS 审核助手")
#             gr.Markdown("这是一个基于大模型的建筑审核系统")
            
#             # 添加文件上传组件
#             file_upload = gr.File(
#                 label="上传GIS数据（请上传完整的Shapefile文件包）",
#                 file_types=[".shp", ".dbf", ".shx", ".prj", ".zip"],
#                 file_count="multiple"
#             )

with demo:
    # 居中显示logo
    with gr.Row(justify="center"):
        gr.Image("/share/home/wuqingyao_zhangboyang/GIS_Agent2/img/logistic.svg", 
                 width=200,  # 增加宽度
                 height=200  # 增加高度
        )
    
    # 标题和说明文字居中
    with gr.Row(justify="center"):
        with gr.Column(scale=1):
            gr.Markdown("# GIS 审核助手")
            gr.Markdown("这是一个基于大模型的建筑审核系统")
    
    # 文件上传部分
    with gr.Row():
        with gr.Column(scale=1):
            file_upload = gr.File(
                label="上传GIS数据（请上传完整的Shapefile文件包）",
                file_types=[".shp", ".dbf", ".shx", ".prj", ".zip"],
                file_count="multiple"
            )
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
        inputs=[input_text, file_upload],
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
        server_port=6789,
        share=False
    )