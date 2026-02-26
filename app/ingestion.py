##############################################
# This executes the process of locating the docs, split, 
# generates embeddings and store in Vector DB.
##############################################
from langchain_core.documents import Document
import os
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from embeddings import get_embeding_model
from vectorstore import VectorStoreManager

def loadDocuments(data_dir:str) -> list[Document]:    
    if not os.path.exists(data_dir):
        raise FileNotFoundError(f"The file path {data_dir} not exists!")
    
    loader = DirectoryLoader(path=data_dir, glob="**/*.txt", loader_cls=TextLoader, loader_kwargs={"encoding": "utf-8"}, show_progress=True, use_multithreading=True)
    docs = loader.load()

    if not docs:
        raise ValueError(f" No .txt file found in {data_dir}.")
    
    return docs


def splitDocuments(docs: list[Document],
                   chunk_size: int = 500,
                   chunk_overlap: int = 50
                   ) -> list[Document]:
    
    splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size,
                 chunk_overlap=chunk_overlap,
                 length_function=len)
    
    chunks = splitter.split_documents(documents=docs)

    if not chunks:
        raise ValueError("No chunks created.")
    
    return chunks


def buildIndex(chunks: list[Document], dbtype: str = "faiss"):
    embeddings = get_embeding_model(provider="ollama")
    store = VectorStoreManager.buildFromDocuments(docs=chunks, dbtype="faiss", embeddings=embeddings)
    return store

def persistIndex(store, persist_path: str) -> None:
    VectorStoreManager.save(store=store, persist_path=persist_path)

def runIngestion(dataDir: str = "./data",
                 persist_path: str = "./vector_db",
                 dbtype: str = "faiss",
                 chunk_size: int = 500,
                 chunk_overlap: int = 50):
    embeddings = get_embeding_model("ollama")

    if VectorStoreManager.exists(persist_path=persist_path):
        store = VectorStoreManager.load(embeddings=embeddings, persist_path=persist_path, dbtype="faiss")
        print(f"The store exists {persist_path}")
        return store
    
    docs = loadDocuments(data_dir=dataDir)
    chunks = splitDocuments(docs=docs, chunk_overlap=50, chunk_size=500)

    store = VectorStoreManager.buildFromDocuments(docs=chunks, embeddings=embeddings, dbtype="faiss")
    persistIndex(store=store, persist_path=persist_path)
    
    return store
    

# if __name__ == "__main__":
#     store = runIngestion(dataDir="/home/srujan/Documents/repo/rag-mini/data/", persist_path="./vector_db", dbtype="faiss", chunk_size=500, chunk_overlap=50)
#     res = store.similarity_search(query="What is this document about?", k=2)
#     for n in res:
#         print(n.page_content)
