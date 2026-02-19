# Validating Political Position Predictions of Arguments

This repository contains the code, data, and experiments for a research paper on validating LLM-based political position predictions in argumentative discourse. The project builds a knowledge base of political arguments from 30 BBC Question Time debates, uses multiple LLMs to predict the political leaning of each argument, validates those predictions through human annotation studies, and provides a retrieval-augmented generation (RAG) system for politically-grounded argumentation.

## Overview

The project has three main components:

1. **Knowledge Base Instantiation** — Processes argumentation data from 30 BBC Question Time episodes, tasks 22 LLMs with predicting the political position (on a 0-100 left-right scale) of locution-proposition pairs, aggregates predictions into ensembles, and stores everything in a Neo4j graph database.

2. **Human Annotation and Validation** — Conducts two crowdsourced annotation studies via [Prolific](https://www.prolific.com/) to validate the LLM predictions: (i) a pointwise study assessing whether models correctly identify both political and apolitical content, and (ii) a pairwise comparison study evaluating whether model-predicted orderings of political positions align with human judgements.

3. **Political Argumentation RAG** — A Python package ([`political_argumentation_rag`](political_argumentation_rag/)) that provides graph-based, vector-based, and hybrid retrieval strategies over the knowledge base, enabling retrieval-augmented generation of politically-grounded responses.

## Repository Structure

```
├── README.md
├── LICENSE
├── docker/
│   └── Dockerfile.neo4j                 # Neo4j Docker image for the knowledge base
├── knowledge_base_instantiation/        # Knowledge base construction pipeline
│   ├── data/                            # Raw, interim, and processed data
│   ├── notebooks/                       # Jupyter notebooks for the full pipeline
│   │   ├── GDBMS/                       # Graph database management
│   │   └── PoliticalPositionResults/    # Political position prediction & analysis
│   └── pyproject.toml
├── human_annotation_and_validation/     # Human annotation studies
│   ├── data/                            # Samples, study results, and outputs
│   ├── 1 - sampling.ipynb               # Sampling from the knowledge base
│   ├── 2 - prolific.ipynb               # Prolific study management
│   ├── 3 - prob_na_analysis.ipynb       # Pointwise NA analysis
│   ├── 4 - pairwise_polpos_analysis.ipynb # Pairwise political position analysis
│   ├── annotation_guidelines.md         # Guidelines provided to annotators
│   ├── prolific.py                      # Prolific API helper
│   ├── prolific.yaml                    # Prolific study configuration
│   └── pyproject.toml
├── political_argumentation_rag/         # RAG Python package
│   ├── src/political_argumentation_rag/
│   │   ├── graph_rag.py                 # Core GraphBasedRetrieval class
│   │   └── datatypes/
│   │       ├── dataclasses.py           # Configuration and data classes
│   │       └── enums.py                 # Enumerations (utterance types, directions, etc.)
│   ├── README.md
│   └── pyproject.toml
└── examples/                            # Example notebooks showing how to use the political_argumentation_rag package
    ├── connection-to-knowledgebase.ipynb
    ├── graph-based-retrieval.ipynb
    ├── retrieval-augmented-generation.ipynb
    └── pyproject.toml
```

## Neo4j Database Setup

The knowledge base is stored in a Neo4j graph database. A pre-configured Docker image is provided with APOC and Graph Data Science plugins.

### Prerequisites

- [Docker](https://www.docker.com/) installed on your system
- You will need Git Large File Storage (LFS) to download the knowledge base. Full details of how to install Git LFS can be found [here](https://docs.github.com/en/repositories/working-with-files/managing-large-files/installing-git-large-file-storage).
- The `neo4j.dump` file located at `knowledge_base_instantiation/data/processed/GDBMS/neo4j.dump`

### Building and Running

Once you have installed Docker and Git LFS, you can run the knowledge base inside of a Docker container using the following commands:

```bash
# download the neo4j dump
git lfs pull

# Build the Docker image
docker build -f docker/Dockerfile.neo4j -t neo4j-political-af .

# Run the container
docker run -d \
  --name neo4j-political-container \
  -p 7474:7474 \
  -p 7687:7687 \
  -e NEO4J_AUTH=neo4j/your_password \
  neo4j-political-af
```

Replace `your_password` with a secure password of your choice.

### Accessing Neo4j

| Interface | URL |
|-----------|-----|
| Browser | http://localhost:7474 |
| Bolt | bolt://localhost:7687 |

### Memory Configuration

| Setting | Value |
|---------|-------|
| Initial Heap Size | 1GB |
| Max Heap Size | 4GB |
| Page Cache Size | 8GB |

Adjust these values in [`docker/Dockerfile.neo4j`](docker/Dockerfile.neo4j) based on your system resources.

### Managing the Container

```bash
# Stop
docker stop neo4j-political-container

# Remove
docker rm neo4j-political-container
```

## Knowledge Base Instantiation

The [`knowledge_base_instantiation/`](knowledge_base_instantiation/) directory handles constructing the political argumentation knowledge base. See its [README](knowledge_base_instantiation/README.md) for full details.

### Pipeline

1. **Graph Construction** — Structured argumentation frameworks (i.e. an ASPIC+ argumentation theory) from 30 BBC Question Time episodes (in AIF format) are parsed and loaded into Neo4j. Nodes represent locutions and propositions; edges represent argumentative relations (`SUPPORTS`, `ATTACKS`, `IS_A_REPHRASE_OF`, `TRANSITIONS_TO`).

2. **Political Position Prediction** — 22 LLMs are prompted to score each locution-proposition pair on a 0-100 left-right political scale, or `NA` if non-political. Per-model results are aggregated into ensemble predictions via an ablation study.

3. **Graph Enrichment** — Model and ensemble predictions (mean, variance, standard deviation, probability of NA) are written back to the graph as node properties.

## Human Annotation and Validation

The [`human_annotation_and_validation/`](human_annotation_and_validation/) directory contains two crowdsourced studies conducted on [Prolific](https://www.prolific.com/). See its [README](human_annotation_and_validation/README.md) for full details.

| Study | Description |
|-------|-------------|
| **Pointwise NA Analysis** | Evaluates whether LLMs correctly distinguish political and apolitical arguments |
| **Pairwise Political Position Comparison** | Assesses whether LLM-predicted orderings of political positions agree with human judgements |

Key metrics reported include Spearman's footrule distance ($d_\text{footrule}$), Kendall's tau distance ($d_\tau$), Krippendorff's alpha ($\alpha_o$), and Macro-F1.

## Political Argumentation RAG

The [`political_argumentation_rag/`](political_argumentation_rag/) package provides retrieval over the knowledge base. See its [README](political_argumentation_rag/README.md) for full details.

### Installation

```bash
uv pip install -e political_argumentation_rag/
```

### Quick Start

```python
from political_argumentation_rag.graph_rag import GraphBasedRetrieval
from political_argumentation_rag.datatypes.dataclasses import (
    KnowledgeBaseConfig, GraphRAGConfig, PoliticalFilter,
    Utterance, TypicalResponsesConfig,
)
from political_argumentation_rag.datatypes.enums import (
    IllocutionaryForce, PoliticalPositionEnsembleOrModelName,
    QueryDirection, UtteranceType,
)

# Configure knowledge base connection
kb_config = KnowledgeBaseConfig(uri="bolt://localhost:7687", user="neo4j", password="your_password")

# Define a political filter (e.g., left-wing: 10-30)
political_filter = PoliticalFilter(
    PoliticalPositionEnsembleOrModelName.ENSEMBLE_1_ALL_MODELS,
    position_min=10, position_max=30,
    position_std=10, probability_of_na=0.05,
)
config = GraphRAGConfig(political_filter)

# Initialise retriever
retriever = GraphBasedRetrieval(kb_config, config)

# Create an utterance and retrieve examples
utt = Utterance(
    "The covid vaccine is safe",
    locution_or_proposition=UtteranceType.LOCUTION,
    illocutinary_force=IllocutionaryForce.ASSERTING,
)

results = retriever.get_typical_responses(
    utt, TypicalResponsesConfig(num_examples=3, query_direction=QueryDirection.BOTH)
)
```

### Retrieval Strategies

| Strategy | Description | Configuration |
|----------|-------------|---------------|
| **Hybrid vector-and-graph-based** | Cosine similarity to find similar nodes, then graph traversal along argumentative relations | [`TypicalResponsesConfig`](political_argumentation_rag/src/political_argumentation_rag/datatypes/dataclasses.py) |
| **User-defined explicit examples** | Retrieve examples matching specific relation types and illocutionary forces | [`UserDefinedExamplesConfig`](political_argumentation_rag/src/political_argumentation_rag/datatypes/dataclasses.py) |
| **Vector-based similarity** | Pure embedding-based nearest-neighbour search | [`VectorBasedConfig`](political_argumentation_rag/src/political_argumentation_rag/datatypes/dataclasses.py) |

## Examples

The [`examples/`](examples/) directory contains Jupyter notebooks demonstrating the full workflow:

| Notebook | Description |
|----------|-------------|
| [`connection-to-knowledgebase.ipynb`](examples/connection-to-knowledgebase.ipynb) | Connecting to the Neo4j knowledge base |
| [`graph-based-retrieval.ipynb`](examples/graph-based-retrieval.ipynb) | Hybrid, explicit, and vector-based retrieval |
| [`retrieval-augmented-generation.ipynb`](examples/retrieval-augmented-generation.ipynb) | End-to-end RAG for political persona generation |

### Running the Examples

```bash
cd examples
uv sync
```

Ensure that a Neo4j instance is running with the knowledge base loaded (see above) and that you have an OpenAI/OpenRouter API key configured for the RAG notebook.

## Dependencies

Each sub-project manages its own dependencies via [`pyproject.toml`](examples/pyproject.toml). Key dependencies across the project include:

| Package | Purpose |
|---------|---------|
| `neo4j` | Neo4j Python driver |
| `langchain-community` | Neo4j graph integration |
| `sentence-transformers` | Embedding models for vector similarity |
| `openai` | LLM API client (for generation) |

[uv](https://docs.astral.sh/uv/) is used for dependency management across all sub-projects.

## Citation

*Citation information will be added upon publication.*

## License

This project is released under the [MIT License](LICENSE).