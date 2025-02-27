from document_processor import DocumentProcessor
doc_processor=DocumentProcessor("/share/home/wuqingyao_zhangboyang/GIS_Agent2/rag_data/13-云安区镇安镇全域土地综合整治试点实施方案.pdf")
doc_processor.process_pdf()
relevant_docs = doc_processor.query_database('建筑面积和高度')
context = "\n".join([doc.page_content for doc in relevant_docs])
print(context)