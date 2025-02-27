from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
import os
import requests


class DocumentProcessor:
    def __init__(self, pdf_path):
        self.pdf_path = pdf_path
        self.embeddings = HuggingFaceEmbeddings(
            model_name="/share/home/wuqingyao_zhangboyang/.xinference/cache/bge-m3",
            
        )
        
    def process_pdf(self):
        # 加载 PDF
        loader = PyPDFLoader(self.pdf_path)
        documents = loader.load()
        
        # 分割文本
        text_splitter = CharacterTextSplitter(
            chunk_size=200,
            chunk_overlap=50,
            separator="\n"
        )
        texts = text_splitter.split_documents(documents)
        
        # 创建向量存储
        vectorstore = FAISS.from_documents(texts, self.embeddings)
        
        # 保存向量存储
        vectorstore.save_local("faiss_index")
        
    def query_database(self, query, k=3):
        # 加载向量存储
        vectorstore = FAISS.load_local("faiss_index", self.embeddings, allow_dangerous_deserialization=True)
        
        # 检索相似文档
        docs = vectorstore.similarity_search(query, k=k)
        return docs