# AI Software Engineering Team

An AI-powered multi-agent software engineering assistant built using **LangGraph**, **LangChain**, **Ollama**, and **ChromaDB**.

Instead of relying on a single LLM, this project uses a team of specialized AI agents that collaborate to understand an existing codebase, plan implementation tasks, retrieve relevant project context, generate code changes, and (eventually) review and apply those changes.

---

## Features

- Project Loader
  - Scans an existing project
  - Indexes source files
  - Stores embeddings in ChromaDB

- Understanding Agent
  - Understands the architecture of the loaded project
  - Generates a structured project summary
  - Identifies technologies, modules and execution flow

- Router Agent
  - Understands user intent
  - Routes requests to the appropriate agent
  - Handles general conversation

- Planner Agent
  - Creates a step-by-step implementation plan
  - Identifies files to modify
  - Determines retrieval targets
  - Estimates possible risks

- Human Approval
  - Allows the user to approve or reject the generated plan before coding begins

- Retriever Agent
  - Searches ChromaDB
  - Retrieves only the relevant project context required for implementation

- Coder Agent
  - Generates structured code changes
  - Produces file-level modifications for the Apply agent

---

## Workflow

```
                +----------------+
                |     START      |
                +-------+--------+
                        |
                        v
                +----------------+
                |     Router     |
                +---+--------+---+
                    |        |
     Load Project   |        |  Coding Request
                    |        |
                    v        v
              +---------+  +---------+
              | Loader  |  | Planner |
              +----+----+  +----+----+
                   |            |
                   v            v
           +---------------+  Human Approval
           | Understanding |        |
           +-------+-------+        |
                   |                v
                   +----------> Retriever
                                |
                                v
                             Coder
                                |
                                v
                         (Reflection)
                                |
                                v
                            (Apply)
                                |
                                v
                             Router
```

---

## Tech Stack

### Frameworks

- LangGraph
- LangChain

### LLM

- Ollama
- Qwen 3 8B

### Vector Database

- ChromaDB

### Embeddings

- BAAI/bge-small-en-v1.5

### Language

- Python

---

## Project Structure

```
ai-sw-team/
│
├── agents/
│   ├── router.py
│   ├── understanding.py
│   ├── planner.py
│   ├── retriever.py
│   └── coder.py
│
├── loader/
│   ├── loader.py
│   └── vector_store.py
│
├── prompts/
│
├── models/
│
├── schemas/
│
├── graph.py
├── state.py
├── human.py
├── main.py
│
└── chroma_db/
```

---

## Current Agent Flow

```
User
   │
   ▼
Router
   │
   ├────────► Loader
   │             │
   │             ▼
   │      Understanding
   │             │
   │             ▼
   │          Router
   │
   └────────► Planner
                  │
                  ▼
          Human Approval
                  │
                  ▼
             Retriever
                  │
                  ▼
               Coder
```

---

## Future Work

- Reflection Agent
- Apply Agent
- Automatic code patching
- Git integration
- Tool calling
- Memory across conversations
- Multi-file code editing
- IDE integration

---

## Installation

Clone the repository

```bash
git clone <repository-url>
cd ai-sw-team
```

Create a virtual environment

```bash
python -m venv venv
```

Activate it

### macOS/Linux

```bash
source venv/bin/activate
```

### Windows

```bash
venv\Scripts\activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

Run Ollama

```bash
ollama serve
```

Download the model

```bash
ollama pull qwen3:8b
```

Run the project

```bash
python main.py
```

---

## Example Usage

```
User:
Add JWT authentication.

↓

Router

↓

Planner

↓

Human Approval

↓

Retriever

↓

Coder

↓

Generated code changes
```

---

## Status

Current Progress

- [x] Loader
- [x] Understanding Agent
- [x] Router
- [x] Planner
- [x] Human Approval
- [x] Retriever
- [x] Coder
- [ ] Reflection Agent
- [ ] Apply Agent
- [ ] Git Integration
- [ ] Memory

---

## Author

**Ishaan Suryavanshi**

Computer Engineering Student | AI & Full Stack Developer