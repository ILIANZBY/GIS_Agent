from document_processor import DocumentProcessor
doc_processor=DocumentProcessor("/share/home/wuqingyao_zhangboyang/GIS_Agent2/rag_data/建筑要求.txt")
doc_processor.process_text()
relevant_docs = doc_processor.query_database('建筑10属于小型住宅，审核它是否符合建筑要求，并画出它的图像')
context = "\n".join([doc.page_content for doc in relevant_docs])
print(context)