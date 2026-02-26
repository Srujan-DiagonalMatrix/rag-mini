##### This is a sample RAG Project for the beginners.#####

##### These are the steps to follow in setting up the project: #####
1. Setup Project folder, .venv, install libraries/packages, git, .env
2. create project structure
3. pull ollama embeddings, update OpenAI library.

##### Ollama API for embeddings:#####
curl -s http://localhost:11434/api/tags | head
Instance: http://localhost:11434

#### Target folder structure (minimal additions) #####
app/
├── embeddings.py ✅ already
├── ingestion.py ✅ already (minor fix: splitDocuments returns chunks)
├── llm.py ⚠ expand for OpenAI chat
├── main.py ❌ CLI entry
├── rag_pipeline.py ❌ orchestrator “brain”
├── retrieval.py ❌ NEW: query-time retrieval only
├── prompts.py ❌ NEW: prompt templates/builders
├── generation.py ❌ NEW: LLM answer generation only
├── api.py ❌ NEW: FastAPI app
├── schemas.py ❌ NEW: Pydantic request/response models
├── config.py ❌ NEW: env/config handling
├── logging_utils.py ❌ NEW: logging + request id + timing helpers
└── vectorstore.py ✅ already

(You can keep fewer files, but this split makes each module single-purpose.)