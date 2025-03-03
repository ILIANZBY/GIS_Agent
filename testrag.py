from document_processor import DocumentProcessor
from prompts import rag_agent_prompt
import openai

doc_processor = DocumentProcessor("/share/home/wuqingyao_zhangboyang/GIS_Agent2/rag_data/13-云安区镇安镇全域土地综合整治试点实施方案.pdf")
doc_processor.process_pdf()
relevant_docs = doc_processor.query_database('镇安镇全镇耕地总规模是多少')
context = "\n".join([doc.page_content for doc in relevant_docs])
print(context)
client = openai.Client(api_key='none', base_url="http://localhost:9876/v1")

def rag(text):  # 移除 self 参数
    try:
        response = client.chat.completions.create(  # 注意：需要确保 client 已正确初始化
            model="qwen2-vl-instruct",
            messages=[{"role": "user", "content": text}],
            max_tokens=8000,
            temperature=0.05,
        )
        return response.choices[0].message
    except Exception as e:
        print(e)
        return None  # 添加适当的错误处理返回值


query = '镇安镇全镇耕地总规模是多少'
# 使用 format() 方法格式化提示模板
formatted_prompt = rag_agent_prompt.format(text=context, query=query)
result = rag(formatted_prompt).content
if result:
    print(result)