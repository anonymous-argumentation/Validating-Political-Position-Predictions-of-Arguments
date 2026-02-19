# Political Argumentation RAG

A Python package for retrieval-augmented generation (RAG) over a political argumentation knowledge base stored in Neo4j. It provides graph-based, vector-based, and hybrid retrieval strategies for extracting argumentation examples from UK political debates, with support for filtering by predicted political position.

## Features

- **Hybrid vector-and-graph-based retrieval** — Finds nodes similar to an input utterance via cosine similarity, then traverses graph relations (`SUPPORTS`, `ATTACKS`, `IS_A_REPHRASE_OF`, `TRANSITIONS_TO`) to retrieve structurally related examples.
- **User-defined explicit examples** — Retrieves examples matching specific relation types and illocutionary forces.
- **Vector-based similarity search** — Pure cosine similarity search over node embeddings.
- **Political position filtering** — Constrain retrieved results by political position range, standard deviation, and probability of NA using ensemble or individual model predictions.

## Installation

### Prerequisites

- Python 3.13+ (see [`.python-version`](../examples/.python-version))
- [uv](https://docs.astral.sh/uv/) for dependency management
- A running Neo4j instance with the knowledge base loaded (see [`docker/Dockerfile.neo4j`](../docker/Dockerfile.neo4j) and the [main README](../README.md) for setup instructions)

### Install from source

```bash copy
cd argumentation_rag
uv pip install -e .
```

### Install as a dependency in another project

Add it as a local path dependency in your `pyproject.toml`:

```toml
[tool.uv.sources]
argumentation-rag = { path = "../argumentation_rag" }
```

Then run:

```bash copy
uv sync
```

### Build the package

```bash copy
uv build
```

This produces a distributable wheel in the `dist/` directory.

## Quick Start

### Connect to the knowledge base

```python
from argumentation_rag.datatypes.dataclasses import KnowledgeBaseConfig

kb_config = KnowledgeBaseConfig()  # defaults: bolt://localhost:7687, neo4j/password
```

### Configure a political filter and retrieve examples

```python
from argumentation_rag.graph_rag import GraphBasedRetrieval
from argumentation_rag.datatypes.dataclasses import (
    GraphRAGConfig,
    PoliticalFilter,
    TypicalResponsesConfig,
    UserDefinedExamplesConfig,
    VectorBasedConfig,
)
from argumentation_rag.datatypes.enums import (
    IllocutionaryForce,
    PoliticalPositionEnsembleOrModelName,
    QueryDirection,
    ReturnType,
    UtteranceType,
)

# Set up a political filter (e.g. left-wing positions)
political_filter = PoliticalFilter(
    PoliticalPositionEnsembleOrModelName.ENSEMBLE_1_ALL_MODELS,
    position_min=10,
    position_max=30,
    position_std=10,
    probability_of_na=0.05,
)

config = GraphRAGConfig(political_filter)

# Initialise the retrieval engine
retriever = GraphBasedRetrieval(kb_config, config)
```

### Hybrid vector-and-graph-based retrieval

```python
from argumentation_rag.datatypes.dataclasses import Utterance

utt = Utterance(
    "The covid vaccine is safe",
    locution_or_proposition=UtteranceType.LOCUTION,
    illocutinary_force=IllocutionaryForce.ASSERTING,
)

typical_responses_config = TypicalResponsesConfig(3, QueryDirection.BOTH)
results = retriever.retrieve_typical_responses(utt, typical_responses_config)
```

### Vector-based similarity search

```python
vector_config = VectorBasedConfig(top_k=5)
results = retriever.retrieve_vector_based(utt, vector_config)
```

## Package Structure

```
argumentation_rag/
├── pyproject.toml                # Project dependencies and build configuration
├── README.md                     # This file
└── src/
    └── argumentation_rag/
        ├── __init__.py
        ├── graph_rag.py          # Core GraphBasedRetrieval class
        ├── py.typed              # PEP 561 marker for type checking
        └── datatypes/
            ├── __init__.py
            ├── dataclasses.py    # Configuration and data classes
            └── enums.py          # Enumerations (utterance types, political positions, etc.)
```

### Key Components

| Module | Description |
|--------|-------------|
| [`graph_rag.py`](src/argumentation_rag/graph_rag.py) | `GraphBasedRetrieval` class implementing all retrieval strategies |
| [`datatypes/dataclasses.py`](src/argumentation_rag/datatypes/dataclasses.py) | Data classes including `KnowledgeBaseConfig`, `GraphRAGConfig`, `PoliticalFilter`, `Utterance`, `TypicalResponsesConfig`, `UserDefinedExamplesConfig`, `VectorBasedConfig`, and `RetrievedExample` |
| [`datatypes/enums.py`](src/argumentation_rag/datatypes/enums.py) | Enumerations including `UtteranceType`, `IllocutionaryForce`, `PoliticalPositionEnsembleOrModelName`, `QueryDirection`, and `ReturnType` |

## Dependencies

| Package | Purpose |
|---------|---------|
| `langchain-community` | Neo4j graph integration |
| `neo4j` | Neo4j Python driver |
| `sentence-transformers` | Embedding models for vector similarity |

## Examples

See the [`examples/`](../examples) directory for Jupyter notebooks demonstrating:

- [Connecting to the knowledge base](../examples/connection-to-knowledgebase.ipynb)
- [Graph-based retrieval](../examples/graph-based-retrieval.ipynb)
- [Retrieval-augmented generation](../examples/retrieval-augmented-generation.ipynb)

## License

This project is released under the [MIT License](../LICENSE).