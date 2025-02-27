import gradio as gr

def redirect_to_main_ui():
    # 直接返回JavaScript重定向代码
    return """
        <script>
            // 立即执行重定向
            window.top.location.href = `http://${window.location.hostname}:7860`;
        </script>
    """

# 创建重定向界面
demo = gr.Blocks(title="重定向到GIS审核助手", css="button { height: 60px; }")

with demo:
    gr.Markdown("# 欢迎使用GIS审核助手")
    gr.Markdown("点击下方按钮进入主系统")
    
    # 使用HTML组件直接添加带onclick事件的按钮
    gr.HTML("""
        <button 
            onclick="window.top.location.href='http://' + window.location.hostname + ':7860'" 
            style="padding: 15px 30px; font-size: 18px; background-color: #2196F3; color: white; border: none; border-radius: 5px; cursor: pointer; margin: 20px 0;">
            进入GIS审核助手
        </button>
    """)

if __name__ == "__main__":
    # 使用不同的端口启动
    demo.launch(
        server_name="0.0.0.0",
        server_port=7861,
        share=False
    )