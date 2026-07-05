import chromadb
from chromadb.config import Settings

class VectorStore:

    def __init__(self, project_name):


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
    
    def count(self):
        return self.collection.count()

    def peek(self):

        return self.collection.peek()

    #def search(...)

    #def clear(...)

    #def count(...)