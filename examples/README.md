# Examples

This sub-directory contains Jupyter notebooks demonstrating how to use the [`political_argumentation_rag`](../political_argumentation_rag) package to connect to the Neo4j knowledge base, retrieve argumentation data, and perform retrieval-augmented generation (RAG) for political position analysis.

## Notebooks

| Notebook | Description |
|----------|-------------|
| [`connection-to-knowledgebase.ipynb`](connection-to-knowledgebase.ipynb) | Demonstrates how to establish a connection to the Neo4j knowledge base and run basic queries |
| [`graph-based-retrieval.ipynb`](graph-based-retrieval.ipynb) | Shows how to retrieve examples from the knowledge base using hybrid vector-and-graph-based retrieval, user-defined explicit examples, and vector-based similarity search |
| [`retrieval-augmented-generation.ipynb`](retrieval-augmented-generation.ipynb) | End-to-end example of using retrieved argumentation examples as context for LLM-based political position analysis |

## Prerequisites

- [uv](https://docs.astral.sh/uv/) for dependency management
- A running Neo4j instance with the knowledge base loaded (see [`docker/Dockerfile.neo4j`](../docker/Dockerfile.neo4j) and the [main README](../README.md) for setup instructions)
- An OpenAI/OpenRouter API key (for the RAG notebook)

## Getting Started

### 1. Install dependencies

```bash copy
cd examples
uv sync
```

### 2. Install the `political_argumentation_rag` package

The [`political_argumentation_rag`](../political_argumentation_rag) package is included as a local path dependency in [`pyproject.toml`](pyproject.toml). If you need to install it manually:

```bash copy
uv pip install -e ../political_argumentation_rag
uv add ../political_argumentation_rag
```

### 3. Set up the Jupyter kernel

```bash copy
uv add --dev ipykernel
uv run ipython kernel install --user --env .venv --name=examples
```

### 4. Run the notebooks

Open the notebooks in VS Code or Jupyter and select the `examples` kernel.

## Key Concepts

### Knowledge Base Connection

Use [`KnowledgeBaseConfig`](../political_argumentation_rag/src/political_argumentation_rag/datatypes/dataclasses.py) to configure the connection to Neo4j. The defaults match the credentials in the provided Docker setup:

```python
from political_argumentation_rag.datatypes.dataclasses import KnowledgeBaseConfig

kb_config = KnowledgeBaseConfig()  # defaults: bolt://localhost:7687, neo4j/password
```

### Retrieval Methods

The [`GraphBasedRetrieval`](../political_argumentation_rag/src/political_argumentation_rag/graph_rag.py) class supports three retrieval strategies:

1. **Hybrid vector-and-graph-based** — Finds nodes similar to the input via cosine similarity, then traverses graph relations (e.g., `SUPPORTS`, `ATTACKS`, `IS_A_REPHRASE_OF`, `TRANSITIONS_TO`) to retrieve structurally related examples. Configured via [`UserDefinedExamplesConfig`](../political_argumentation_rag/src/political_argumentation_rag/datatypes/dataclasses.py) and [`TypicalResponsesConfig`](../political_argumentation_rag/src/political_argumentation_rag/datatypes/dataclasses.py).

2. **User-defined explicit examples** — Retrieves examples matching specific relation types and illocutionary forces. Configured via [`UserDefinedExamplesConfig`](../political_argumentation_rag/src/political_argumentation_rag/datatypes/dataclasses.py).

3. **Vector-based** — Pure cosine similarity search over node embeddings. Configured via [`VectorBasedConfig`](../political_argumentation_rag/src/political_argumentation_rag/datatypes/dataclasses.py).

### Political Filtering

All retrieval methods support filtering by political position using [`PoliticalFilter`](../political_argumentation_rag/src/political_argumentation_rag/datatypes/dataclasses.py), which allows constraining results by position range, standard deviation, and probability of NA.

## Dependencies

See [`pyproject.toml`](pyproject.toml) for the full dependency list. Key dependencies include:

- [`political-argumentation-rag`](../political_argumentation_rag) — Core retrieval library
- [`openai`](https://pypi.org/project/openai/) — For LLM-based generation in the RAG notebook