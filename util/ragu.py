import chromadb
import ollama
from typing import List, Dict
from langchain.text_splitter import RecursiveCharacterTextSplitter


class ChromaDBClient:
    def __init__(self, collection_name: str, embedding_function: callable):
        """
        Initialize ChromaDB client and create a collection
        """
        self.client = chromadb.Client()
        self.collection_name = collection_name
        self.embedding_function = embedding_function

        self.collection = self.client.get_or_create_collection(
            name=collection_name,
            embedding_function=embedding_function
        )

    def add_documents(self, documents: list, batch_size: int = 10, chunk: bool = True):
        """
        Add documents to the collection
        """
        print(f"[DEBUG] Adding {len(documents)} documents to ChromaDB collection '{self.collection_name}'")
        


        if chunk:

            documents = self.chunk_documents(documents=documents)


        
        self.collection.add(
            ids=[doc["id"] for doc in documents],
            documents=[doc["text"] for doc in documents],
            metadatas=[doc["metadata"] for doc in documents]
        )
        
        print(f"[DEBUG] Added {len(documents)} documents to ChromaDB collection '{self.collection_name}'")

    def chunk_documents(self, documents, chunk_size: int = 500, chunk_overlap: int = 50):
        """
        Split documents into smaller chunks for embedding,
        using LangChain's RecursiveCharacterTextSplitter
        """
        chunked_documents = []

        # Create the chunker with specified parameters
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            length_function=len
        )


        # Apply the chunker to the document text

        
        for document in documents:
            chunks = text_splitter.split_text(document["text"])
            for i, chunk in enumerate(chunks):
                chunked_documents.append({
                    "id": f"{document["id"]}_chunk_{i}",
                    "text": chunk,
                    "metadata": {"source": document["id"], "chunk": i}.append(document["metadata"])
                })

        print(f"Created {len(chunked_documents)} chunks from {len(documents)} documents")
        return chunked_documents

    def query(self, query_text: str, n_results: int = 5):
        """
        Query the collection for similar documents
        """
        results = self.collection.query(
            query_texts=[query_text],
            n_results=n_results
        )
        return results["documents"]
    
    def peek(self):
        """
        Peek at the collection to see its contents
        """
        return self.collection.peek()

class OllamaEmbeddingFunction:
    """Custom embedding function that uses Ollama for embeddings"""
    
    def __init__(self, model_name="nomic-embed-text"):
        self.model_name = model_name
    
    def __call__(self, input: List[str]) -> List[List[float]]:
        """Generate embeddings for a list of texts using Ollama"""
        return ollama.embed(model=self.model_name, input=input)["embeddings"]
        pass
