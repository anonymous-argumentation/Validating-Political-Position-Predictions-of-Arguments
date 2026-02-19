# Knowledge Base Instantiation

This sub-directory handles the construction and population of the political argumentation knowledge base. It processes argumentation data from 30 BBC Question Time episodes, tasks 22 LLMs with the prediction of political positions of locution-proposition pairs, and stores the results in a Neo4j graph database.

## Directory Structure

```
knowledge_base_instantiation/
├── pyproject.toml                  # Project dependencies and configuration
├── data/
│   ├── external/                   # Raw source data
│   │   ├── ClaudeBatchAPIRequests/ # Batch API request/response files for Claude models
│   │   │   ├── claude-3-5-haiku-20241022/
│   │   │   └── claude-3-7-sonnet-20250219/
│   │   └── QuestionTime/          # BBC Question Time argumentation data (AIF format)
│   │       ├── cutiestestrun*/    # Multiple episode datasets
│   │       └── qt30/
│   ├── interim/                   # Intermediate results
│   │   └── PoliticalPositions/    # Raw LLM predictions per provider
│   │       ├── alibaba_cloud/
│   │       ├── anthropic/
│   │       ├── deepseek/
│   │       ├── meta/
│   │       ├── microsoft/
│   │       ├── mistral/
│   │       ├── openai/
│   │       ├── vertex/
│   │       ├── xai/
│   │       ├── incomplete_tests/
│   │       └── prompts/           # Prompt templates used for predictions
│   └── processed/                 # Final outputs
│       ├── GDBMS/
│       │   ├── neo4j.dump         # Neo4j database dump (ready to import)
│       │   └── graphs/            # Intermediate dump files
│       └── PoliticalPositions/
│           ├── ensembles/         # Aggregated ensemble predictions
│           └── models/            # Per-model processed results
├── notebooks/
│   ├── GDBMS/                     # Graph database management notebooks
│   │   ├── 1.0  - Creating the graph database from QT data
│   │   ├── 1.01 - Removing locutor names from locutions
│   │   ├── 1.2  - Reinstantiating graph without political positions (metadata cleanup)
│   │   ├── 1.3  - Adding model & ensemble results to the graph
│   │   └── 1.4  - Visualising political positions over time
│   ├── PoliticalPositionResults/  # Political position prediction notebooks
│   │   ├── 1.0  - Testing political position prediction
│   │   ├── 1.1  - Creating prompt JSON files for testing using Golem
│   │   ├── 1.2  - Batch prompts for Claude (Anthropic Batch API)
│   │   ├── 1.3  - Plotting each model's distribution of predictions
│   │   ├── 1.4  - Processing results per model for GDBMS upload
│   │   ├── 1.5  - Model-to-model scatter plots
│   │   ├── 1.6  - Checking whether predictions make intuitive sense
│   │   ├── 1.7  - Ablation study for ensemble containing all results
│   │   ├── 1.8  - Saving ensemble results to TSV
│   │   ├── 1.9  - Creating locution & proposition embeddings for GraphRAG retrieval
│   │   └── examples_of_interesting_completions.ipynb
│   └── Utils/                     # Shared utilities
│       └── translation_from_AIF_to_ASPIC_to_DAF.py
```

## Pipeline Overview

The knowledge base was built in two main stages:

### 1. Political Position Prediction

Multiple LLMs were prompted to predict the political leaning (left-right spectrum) of argumentative locution-proposition pairs extracted from 30 BBC Question Time debates. The following model providers are used:

- **Anthropic** 
    - Claude 3.5 Haiku
    - Claude 3.7 Sonnet
- **OpenAI**
    - GPT 4.5
    - GPT 4o 
    - GPT 4 Turbo
    - GPT 4o Mini
    - GPT 3.5 Turbo
    - o3 Mini
- **Meta** 
    - Llama 4 Maverick
    - Llama 3.3 70B
    - Llame 3.2 3B
    - Llama 3.1 405B
    - Llama 3.1 8B
- **DeepSeek**
    - DeepSeek R1
    - DeepSeek V3
- **Mistral**
    - Mistral 7B
- **Microsoft**
    - Phi 4
- **Alibaba Cloud** 
    - Qwen 3 235B
    - Qwen QwQ 32B
- **xAI** 
    - Grok 2
- **Google Vertex AI**
    - Gemini 1.5 Pro
    - Gemini 2.5 Flash

Predictions from individual models are aggregated into **ensemble** results via an ablation study (see notebook 1.7).

### 2. Graph Database Construction

Argumentation data from BBC Question Time (in [AIF format](http://www.arg-tech.org/index.php/projects/aif/)) is ingested into a **Neo4j** graph database. The pipeline:

1. Creates an ASPIC+ argumentation framework from raw Question Time data
2. Cleans locution nodes (removes speaker names from the start of a locution)
3. Prompts all 22 models to make 5 predictions per argument (node) in the argumentation graph
4. Adds per-model and ensemble political position predictions as node properties
5. Generates embeddings for locutions and propositions to support GraphRAG-based retrieval

A ready-to-import Neo4j dump is available at `data/processed/GDBMS/neo4j.dump`.

## LLM Client: Golem

[Golem](https://github.com/RobBlackwell/golem) was used to conduct large-scale model predictions for the above models. 

### Installation 

```bash copy
cd knowledge_base_instantiation
git clone https://github.com/RobBlackwell/golem.git
cd golem
uv pip install -e .
```

### Run Commands

The JSONL files used in experiments can be found in [here](knowledge_base_instantiation\data\interim\PoliticalPositions\prompts\prompts.jsonl). 

The run command used was:

```bash copy
golem --provider <provider> --model <model> --repeat "0:5" --temperature "0" --top_p "0.1" --seed 123 -f <path-to-prompts>.jsonl > <path-to-results>.jsonl
```

Follow the instructions on [Golem](https://github.com/RobBlackwell/golem)'s GitHub repository for more details.

The raw predictions for each model can be found [here](knowledge_base_instantiation\data\interim\PoliticalPositions).

### Prompts

An example of the prompt used for testing is shown below.

```python
sys_msg = {"role" : "system",
           "content" : """You will be provided with the text of a locution and its corresponding propositional content that forms part of an argument from a UK political debating TV programme. 
           Your task is to decide where does the speaker stand on the 'left' to 'right' wing scale using the speaker's locution and propositional content? 
           Provide your response as a score between 0 and 100 where 0 means 'Extremely left' and 100 means 'Extremely right'. If the text does not have political content, set the score to “NA”. 
           Output in JSON format using the following template: {'Score' : int}. 
           
           Do not include any additional context, preamble, or explanation."""
           }

human_msg = {"role" : "user",
                 "content" : """Score the speaker's political position between 0 ('Extremely left') and 100 ('Extremely right'), and 'NA' if there is no political content, using the following locution and proposition.
                 
                 Proposition: '""" + records[0]["n"]._properties["proposition"] + """'

                 Locution: '""" + records[0]["n"]._properties["locution"].split(":", 1)[-1].strip() + """'

                 Do not write an introduction or summary. Output in JSON format using the following template: {'Score' : int}"""}
```


## Getting Started

### Prerequisites

- Python (see [`.python-version`](knowledge_base_instantiation/.python-version))
- [uv](https://docs.astral.sh/uv/) for dependency management
- Neo4j (a Docker setup is available at [`docker/Dockerfile.neo4j`](docker/Dockerfile.neo4j))
- API keys for the LLM providers you wish to use

### Installation

```sh
cd knowledge_base_instantiation
uv sync
```

### Importing the Pre-built Graph

To load the pre-built knowledge base, follow the instructions [here](../README.md/##neo4j-database-setup).

### Running the Notebooks

Notebooks were executed in numerical order within each sub-directory:

1. **`notebooks/PoliticalPositionResults/1.0` → `1.9`** - Generate and process political position predictions
2. **`notebooks/GDBMS/1.0` → `1.4`** - Build and populate the graph database

## License

This project is released under the [MIT License](../LICENSE).