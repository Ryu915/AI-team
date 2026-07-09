import chromadb
from chromadb.config import Settings
from langchain_huggingface import HuggingFaceEmbeddings

class VectorStore:

    def __init__(self, project_name):

        self.embedding_model = HuggingFaceEmbeddings(
            model_name="BAAI/bge-small-en-v1.5"
        )


        self.client = chromadb.PersistentClient(
            path="./chroma_db"
        )

        self.collection = self.client.get_or_create_collection(
            name = project_name
        )

    def add(self, embedded_chunks):
        ids = []

        documents = []

        embeddings = []

        metadatas = []

        for embedded in embedded_chunks:

            ids.append(embedded.chunk.id)
            documents.append(embedded.chunk.text)
            embeddings.append(embedded.embedding)

            metadatas.append({

                "file_path": str(
                    embedded.chunk.file_path
                ),

                "file_name": embedded.chunk.file_name,

                "language": embedded.chunk.language,

                "chunk_index": embedded.chunk.chunk_index

            })

            self.collection.add(

                ids=ids,

                documents=documents,

                embeddings=embeddings,

                metadatas=metadatas

            )

    def search(self, query: str, k: int = 5) -> str:
        """
        Search the vector database for the most relevant chunks.

        Args:
            query: Natural language query.
            k: Number of chunks to retrieve.

        Returns:
            A single string containing the retrieved context.
        """

        # Convert the query into an embedding
        query_embedding = self.embedding_model.embed_query(query)

        # Search ChromaDB
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=k
        )

        # Extract the documents
        documents = results["documents"][0]

        # Combine them into one context string
        context = "\n\n".join(documents)

        return context
    
    def count(self):
        return self.collection.count()

    def peek(self):

        return self.collection.peek()

