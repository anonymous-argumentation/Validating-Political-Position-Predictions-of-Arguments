from dataclasses import dataclass, field
from typing import Optional, List, Tuple

from political_argumentation_rag.datatypes.enums import (
    PoliticalPositionEnsembleOrModelName,
    RelationType,
    IllocutionaryForce,
    QueryDirection,
    ReturnType,
    UtteranceType,
    RetrievalMethod
    )

@dataclass
class KnowledgeBaseConfig:
    "Configuration to make API calls to Neo4j"
    username:str="neo4j"
    password:str="password"
    endpoint:str="bolt://localhost:7687"

@dataclass
class PoliticalFilter:
    """Configuration for filtering nodes by political position."""
    ensemble_or_model_name: PoliticalPositionEnsembleOrModelName 
    position_min: int = 0
    position_max: int = 100
    position_std: int = 10
    probability_of_na: float = 1.0

@dataclass
class UserDefinedExamplesConfig:
    """Configuration for user-defined example retrieval."""
    relation_choices: List[RelationType]
    query_node_choices: List[IllocutionaryForce]
    num_examples: int
    query_direction: QueryDirection

@dataclass
class VectorBasedConfig:
    """Configuration for vector-based similarity search."""
    num_examples: int
    similar_nodes_illocutionary_force: IllocutionaryForce

@dataclass
class TypicalResponsesConfig:
    """Configuration for typical response retrieval."""
    num_examples: int
    query_direction: QueryDirection

@dataclass
class Utterance:
    utterance: str
    locution_or_proposition: UtteranceType
    illocutinary_force: IllocutionaryForce

@dataclass
class RetrievedExample:
    retrieval_method: RetrievalMethod
    content_type: str
    relation: str
    input_text: str                     # The user's original input
    similar_illocutionary_force: str      # Illocutionary force of the matched (similar) node
    related_illocutionary_force: str    # Illocutionary force of the related node
    similar_text: str                   # Text of the node similar to input (n)
    related_text: str                   # Text of the related node (m)
    example_text_tuple: Tuple[str, str] # Ordered (source, target) based on direction
    query_direction: str

@dataclass
class GraphRAGConfig:
    political_filter: PoliticalFilter
    return_type: ReturnType = ReturnType.BOTH