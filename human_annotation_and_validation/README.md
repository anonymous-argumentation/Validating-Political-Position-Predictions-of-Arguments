# Human Annotation and Validation

This sub-directory contains the code, data, and guidelines for conducting human annotation studies to validate political position predictions in arguments. The annotations were collected via the [Prolific](https://www.prolific.com/) crowdsourcing platform.

## Overview

The validation pipeline consists of four main stages, each implemented as a Jupyter notebook:

1. **Sampling** ([`1 - sampling.ipynb`](1%20-%20sampling.ipynb)): Draws representative samples from the knowledge base for human annotation.
2. **Prolific Study Management** ([`2 - prolific.ipynb`](2%20-%20prolific.ipynb)): Manages the creation, configuration, and deployment of annotation tasks on the Prolific platform.
3. **Probabilistic NA Analysis** ([`3 - prob_na_analysis.ipynb`](3%20-%20prob_na_analysis.ipynb)): Analyses pointwise cases where models predicted with low and high certainty that a node contained political sentiment.
4. **Pairwise Political Position Analysis** ([`4 - pairwise_polpos_analysis.ipynb`](4%20-%20pairwise_polpos_analysis.ipynb)): Analyses pairwise comparisons of model political position predictions and human annotations.

## Supporting Files

| File | Description |
|------|-------------|
| [`prolific.py`](prolific.py) | Python helper module for interacting with the Prolific API |
| [`prolific.yaml`](prolific.yaml) | Configuration file for Prolific study parameters |
| [`annotation_guidelines.md`](annotation_guidelines.md) | Detailed guidelines provided to annotators for the labeling task |
| [`pyproject.toml`](pyproject.toml) | Python project configuration and dependencies |

## Data

The [`data/`](data/) directory contains all raw and processed data:

### Samples

- [`sample_10_2025-10-17.csv`](data/sample_10_2025-10-17.csv) - Small test sample (10 items) for piloting.

### Study 1: Political Position NA Analysis (`polpos_nan_2010/`)

Located in [`data/polpos_nan_2010/`](data/polpos_nan_2010/):

- `sample_1000_2025-10-17.csv` - Sample of 1,000 arguments where political positions were predicted with low and high confidence.
- `prolific_results.csv` / `prolific_demographics.csv` - Raw results and demographic data from Prolific.
- `results_merged.csv` / `results_long_merged.csv` - Merged and reshaped result datasets for analysis.

### Study 2: Pairwise Political Position Comparison (`polpos_pairs_2210/`)

Located in [`data/polpos_pairs_2210/`](data/polpos_pairs_2210/):

- `pairs_934_2025-10-27.csv` / `pairs_934_2025-10-27b.csv` - Generated argument pairs for pairwise annotation.
- `clean_pairs_934_2025-10-27.csv` / `clean_pairs_934_2025-10-27b.csv` - Cleaned pair datasets.
- `sample_100_from_nan_2025-10-23.csv` - Subset of 100 pairs sampled from the NA study.
- `prolific_results_left.csv` / `prolific_results_right.csv` - Raw Prolific results for left and right pair members.
- `prolific_results_left_merged.csv` / `prolific_results_right_merged.csv` - Merged result datasets.
- `prolific_results_right_clean.csv` - Cleaned right-side results.
- `prolific_demographic_left.csv` / `prolific_demographic_right.csv` - Demographic data for each annotator group.

### Outputs

- [`data/pairwise-llm-model-summary-table.tex`](data/pairwise-llm-model-summary-table.tex) - LaTeX summary table comparing LLM model predictions.
- [`data/pairwise-llm-model-summary-table-multirow.tex`](data/pairwise-llm-model-summary-table-multirow.tex) - Multi-row variant of the summary table.
- [`data/figures/`](data/figures/) - Generated figures from the analysis notebooks.

## Getting Started

### Installation
Using [uv](https://github.com/astral-sh/uv):

```bash
uv sync
```

### Running the Notebooks

Execute the notebooks in order (1 to 4). Make sure to configure your Prolific API credentials in [`prolific.yaml`](prolific.yaml) before running the study management notebook.

## License

This project is licensed under the MIT License. See the [LICENSE](../LICENSE) file for details.