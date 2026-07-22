import uuid

from pathlib import Path
from dataclasses import dataclass
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from loader.vector_store import VectorStore


IGNORE_DIRS = {
    ".git",
    "__pycache__",
    "node_modules",
    ".venv",
    "venv",
    "dist",
    "build"
}

SUPPORTED_EXTENSIONS = {
    ".py",
    ".js",
    ".ts",
    ".tsx",
    ".jsx",
    ".java",
    ".cpp",
    ".c",
    ".go",
    ".rs",
    ".json",
    ".md",
    ".html",
    ".css"
}

LANGUAGE_MAP = {
    ".py": "Python",
    ".js": "JavaScript",
    ".ts": "TypeScript",
    ".jsx": "React JavaScript",
    ".tsx": "React TypeScript",
    ".java": "Java",
    ".cpp": "C++",
    ".c": "C",
    ".cs": "C#",
    ".go": "Go",
    ".rs": "Rust",
    ".php": "PHP",
    ".rb": "Ruby",
    ".swift": "Swift",
    ".kt": "Kotlin",
    ".html": "HTML",
    ".css": "CSS",
    ".scss": "SCSS",
    ".json": "JSON",
    ".xml": "XML",
    ".yaml": "YAML",
    ".yml": "YAML",
    ".md": "Markdown",
    ".sql": "SQL",
    ".sh": "Shell",
}

@dataclass
class Document:

    path: Path
    file_name: str
    extension: str
    language: str
    content: str

    """
    This class saves files as documents

    Document(
        path = Path("app/auth.py"),
        content = "def login(): ...",
        extension = ".py"
    )
    """

    

@dataclass
class Chunk:
    id: str
    text: str
    file_path: Path
    file_name: str
    language: str
    chunk_index: int

@dataclass
class EmbeddedChunk:
    chunk: Chunk
    embedding: list[float]

class ProjectLoader:

    def __init__(self):

        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size = 1000,
            chunk_overlap = 200
        )

        self.embedding_model = HuggingFaceEmbeddings(
            model_name="BAAI/bge-small-en-v1.5"
        )

        self.vector_store = None

    def load(self, project_path: str):
        
        path = self._validate_path(project_path)
        print(path)

        self.vector_store = VectorStore(path.name)
        print("\nScanning project...")
        files = self._scan_project(path)
        
        print("\nReading files...")
        documents = self._read_files(files)
        print(f"\nFound {len(documents)} documents")
        
        print("\nChunking documents...")
        chunks = self._chunk_documents(documents)

        print("\nEmbedding chunks...")
        embedded_chunks = self._embed_chunks(chunks)

        print("\nStoring embeddings...")
        self._store_embeddings(embedded_chunks)
        #print(self.vector_store.count())
        print("\nProject loaded successfully.")
        return self.vector_store
        
    
    def _validate_path(self, project_path: str):

        path = Path(project_path)

        if not path.exists():
            raise FileNotFoundError(f"Project path '{project_path}' does not exist.")
        
        if not path.is_dir():
            raise NotADirectoryError(f"'{project_path}' is not a directory.")
        
        return path
    
    def  _scan_project(self, project_path: str):
        files = []

        for item in project_path.rglob("*"): # .rglob("*") gives every file and folder
            # skip the folders
            if not item.is_file():
                continue
            
            # for unwanted files
            if any(parent.name in IGNORE_DIRS for parent in item.parents):
                continue
            
            # to skip images, audio and video files
            if item.suffix not in SUPPORTED_EXTENSIONS:
                continue

            files.append(item)

        files.sort()
        
        return files
    
    def _read_files(self, files: list[Path]) ->  list[Document]:
        documents = []

        for file in files:
            try:
                content = file.read_text(encoding="utf-8")

            except Exception:
                continue

            document = Document(
                path = file,
                content = content,
                extension = file.suffix,
                file_name = file.name,
                language = self._detect_language(file.suffix)
            )
            documents.append(document)

        return documents
    
    def _detect_language(self, extension: str) -> str:
        return LANGUAGE_MAP.get(extension.lower(), "Unknown")
    
    def _chunk_documents(self, documents: list[Document]) -> list[Chunk]:
        chunks = []

        for document in documents:
            texts = self.text_splitter.split_text(document.content)
        
            for index, text in enumerate(texts):


                chunk = Chunk(
                    id=str(uuid.uuid4()),
                    text=text,
                    file_path=document.path,
                    file_name=document.file_name,
                    language=document.language,
                    chunk_index=index
                )

                chunks.append(chunk)

        return chunks
    
    def _embed_chunks(self, chunks: list[Chunk]):

        texts = [chunk.text for chunk in chunks]

        vectors = self.embedding_model.embed_documents(texts)

        embedded_chunks = []

        for chunk, vector in zip(chunks, vectors):

            embedded_chunks.append(
                EmbeddedChunk(
                    chunk = chunk,
                    embedding = vector
                )
            )

        return embedded_chunks
    
    def _store_embeddings(self, embedded_chunks: list[EmbeddedChunk]):

        self.vector_store.add(embedded_chunks)

    