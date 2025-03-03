import gradio as gr
from apis import MultiAgentPlanner
import json
import os
import time
from prompts import plan_agent_prompt, act_agent_prompt, summary_agent_prompt
import tempfile
from observation import load_gdf 
import shutil 
from document_processor import DocumentProcessor
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
    return "", "", None, None, None  # 返回值包含input_text, output_text, image_output, gis_files, rag_file

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

def process_query(query, gis_files, doc_files):
    """处理查询并加载用户上传的GIS文件和文档文件"""
    try:
        temp_dir = tempfile.mkdtemp()
        doc_content = ""
        processor = None
        
        # 处理文档文件（PDF和TXT）
        if doc_files:
            for doc_file in doc_files:
                file_ext = os.path.splitext(doc_file.name)[1].lower()
                
                # 创建临时文件路径
                temp_file_path = os.path.join(temp_dir, os.path.basename(doc_file.name))
                shutil.copy2(doc_file.name, temp_file_path)
                
                # 根据文件类型处理文档
                processor = DocumentProcessor(temp_file_path)
                if file_ext == '.pdf':
                    processor.process_pdf()
                elif file_ext == '.txt':
                    processor.process_text()
        
        # 处理GIS文件
        gdf = None
        if gis_files:
            # 处理Shapefile文件
            for file in gis_files:
                file_path = os.path.join(temp_dir, os.path.basename(file.name))
                shutil.copy2(file.name, file_path)
            
            # 检查并加载Shapefile
            base_files = set([os.path.splitext(f)[0] for f in os.listdir(temp_dir)])
            for base in base_files:
                required_exts = ['.shp', '.shx', '.dbf']
                if all(os.path.exists(os.path.join(temp_dir, base + ext)) for ext in required_exts):
                    shp_path = os.path.join(temp_dir, base + '.shp')
                    gdf = load_gdf(shp_path)
                    break

        # 创建agent并处理查询
        agent = MultiAgentPlanner(
            plan_agent_prompt,
            act_agent_prompt,
            summary_agent_prompt
        )
        
        # 如果有文档处理器，使用它来查询相关内容
        if processor:
            relevant_docs = processor.query_database(query)
            doc_content = "\n".join([doc.page_content for doc in relevant_docs])
        
        # 组合GIS内容和文档内容
        combined_content = f"{doc_content}\n{gdf.to_string() if gdf is not None else ''}"
        
        response = agent.process_query(query, combined_content)
        formatted_response = json.dumps(response, ensure_ascii=False, indent=2)
        
        # 清理临时文件
        try:
            shutil.rmtree(temp_dir)
        except Exception:
            pass
        
        latest_image = get_latest_image()
        return formatted_response, latest_image if latest_image else None
    
    except Exception as e:
        return json.dumps({"error": str(e)}, ensure_ascii=False), None
with demo:
    # 设置整体主题和样式
    demo.theme = gr.themes.Soft(
        primary_hue="blue",
        secondary_hue="indigo",
    )
    
    # 添加页面级CSS样式
    # 修改CSS样式部分
    demo.load(None, None, None, _js="""
    function() {
        const style = document.createElement('style');
        style.textContent = `
            .container { 
                max-width: 1200px; 
                margin: 0 auto; 
                padding: 2rem; 
            }
            .header { 
                text-align: center; 
                margin-bottom: 2rem;
                display: flex;
                flex-direction: column;
                align-items: center;
            }
            .title-container h1 {
                font-size: 2.5rem !important;
                margin-bottom: 1rem !important;
            }
            .title-container h3 {
                font-size: 1.5rem !important;
                color: #666 !important;
            }
            .large-text textarea {
                font-size: 18px !important;
                line-height: 1.8 !important;
                padding: 1.2rem !important;
                border-radius: 8px !important;
            }
            .result-box textarea {
                font-size: 18px !important;
                line-height: 1.8 !important;
            }
            .upload-section h3 {
                font-size: 1.5rem !important;
                margin-bottom: 1rem !important;
            }
            .label-text {
                font-size: 1.2rem !important;
                margin-bottom: 0.5rem !important;
                }
                /* ...existing styles... */
            `;
            document.head.appendChild(style);
        }
    """)

    with gr.Box(class_name="container"):
        # 修改页面头部布局
        with gr.Box(class_name="header"):
            with gr.Row(class_name="logo-container"):
                gr.Image("/share/home/wuqingyao_zhangboyang/GIS_Agent2/img/image.png",
                        width=200,
                        height=200,
                        elem_classes="logo")
            
            with gr.Box(class_name="title-container"):
                gr.Markdown("""
                    # 🏗️ GIS 审核助手
                    ### 智能建筑审核系统 - powered by AI
                """)

        # ...其余代码保持不变...
        
        # 文件上传区域
    with gr.Box(elem_classes="upload-section"):
        with gr.Row():
            # GIS数据文件上传
            gis_file_upload = gr.File(
                label="上传GIS数据文件（支持Shapefile格式）",
                file_types=[".shp", ".dbf", ".shx", ".prj", ".zip"],
                file_count="multiple",
                elem_classes="file-upload"
            )
            # 文档文件上传（支持PDF和TXT）
            doc_file_upload = gr.File(
                label="上传文档文件（支持PDF和TXT格式）",
                file_types=[".pdf", ".txt"],
                file_count="multiple",
                elem_classes="file-upload"
            )
        # 主要内容区域
        with gr.Row(equal_height=True):
            # 左侧区域：输入和文本输出
            with gr.Column(scale=1):
                input_text = gr.Textbox(
                    label="✍️ 输入审核查询",
                    placeholder="例如：请审核建筑A是否符合建筑要求，并生成建筑示意图...",
                    lines=4,
                    elem_classes="large-text"
                )
                
                output_text = gr.Textbox(
                    label="📊 分析结果",
                    lines=12,
                    elem_classes="large-text result-box",
                    show_copy_button=True
                )
                
                with gr.Row():
                    submit_btn = gr.Button("🚀 开始分析", elem_classes="button-primary")
                    clear_btn = gr.Button("🗑️ 清除", variant="secondary")

            # 右侧区域：图片显示
            with gr.Column(scale=1):
                image_output = gr.Image(
                    label="🖼️ 生成图片",
                    type="filepath",
                    height=800,  # 增加图片显示高度
                    elem_classes="result-image"
                )
    # 绑定事件处理
    submit_btn.click(
        fn=process_query,
        inputs=[input_text, gis_file_upload, doc_file_upload],
        outputs=[output_text, image_output],
        api_name="analyze"
    )
    
    clear_btn.click(
        fn=clear_inputs,
        inputs=[],
        outputs=[input_text, output_text, image_output, gis_file_upload, doc_file_upload],
        api_name="clear"
    )

# ...existing code...

if __name__ == "__main__":
    demo.launch(
        server_name="0.0.0.0", 
        server_port=7860,
        share=False
    )