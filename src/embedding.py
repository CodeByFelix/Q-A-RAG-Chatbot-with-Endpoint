import os
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from src.utils import vectorStore


async def embedPDF (path: str) -> bool:
    
    if path.endswith (".pdf"):
        loader = PyPDFLoader (path)
        pages:list

        async for page in loader.alazy_load ():
            doc = spliter.split_documents ([page])
            success = False
            while not success:
                try:
                    vectorStore.add_documents(doc)
                    success = True
                except:
                    print ("Retrying page")
            #print (f"Done embedding {pdf}")
        return True
    else:
        return False

spliter = RecursiveCharacterTextSplitter (chunk_size=512, chunk_overlap=64)