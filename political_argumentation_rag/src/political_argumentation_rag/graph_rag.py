import numpy as np
from langchain_community.graphs import Neo4jGraph
from sentence_transformers import SentenceTransformer

from political_argumentation_rag.datatypes.dataclasses import (
    KnowledgeBaseConfig,
    GraphRAGConfig,
    Utterance,
    TypicalResponsesConfig,
    UserDefinedExamplesConfig,
    RetrievedExample,
    VectorBasedConfig
)

from political_argumentation_rag.datatypes.enums import (
    IllocutionaryForce,
    QueryDirection,
    ReturnType,
    RetrievalMethod
)



class GraphBasedRetrieval:
    def __init__(self, 
                 kb : KnowledgeBaseConfig, 
                 config: GraphRAGConfig
                 ):
        
        
        self.config = config

        self.kb_connection = Neo4jGraph(
                url=kb.endpoint,
                username=kb.username,
                password=kb.password
            )

        self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')

        self.relation_types = {
                "Support" : "SUPPORTS", 
                "Conflict" : "ATTACKS", 
                "Rephrase" : "IS_A_REPHRASE_OF", 
                "Default Transition" : "TRANSITIONS_TO"}

    def get_typical_responses(self, utterance: Utterance, typical_respones_config: TypicalResponsesConfig):

        if typical_respones_config.num_examples < 1:
            raise ValueError("'num_examples' must be greater than 0")


        embedded_locution_or_proposition = self.embedding_model.encode(utterance.utterance)

        relevant_graph_content = []
        for _, relation in self.relation_types.items():

            # for illocutionary_force in self.ALLOWED_NODE_TYPES:
            for name, member in IllocutionaryForce.__members__.items():
                illocutionary_force = member.value

                if typical_respones_config.query_direction == QueryDirection.INCOMING or typical_respones_config.query_direction == QueryDirection.BOTH: 
                    cypher = self._get_cypher(
                                    query_direction=QueryDirection.INCOMING,
                                    relation=relation, 
                                    utterance_illocutionary_force=utterance.illocutinary_force.value,
                                    example_illocutionary_force=illocutionary_force,
                                    sbert_embedding=embedded_locution_or_proposition,
                                    num_examples=typical_respones_config.num_examples
                                    )
                    
                    result = self._query_graph(cypher)

                    relevant_graph_content.extend(
                        self._parse_retrieved_relation_examples(
                            retrieved_data=result,
                            relation=relation,
                            input_text=utterance.utterance,
                            similar_illocutionary_force=utterance.illocutinary_force.value,
                            related_illocutionary_force=illocutionary_force,
                            query_direction=QueryDirection.INCOMING
                            )
                    )

                if typical_respones_config.query_direction == QueryDirection.OUTGOING or typical_respones_config.query_direction == QueryDirection.BOTH: 
                    cypher = self._get_cypher(
                                    query_direction=QueryDirection.OUTGOING,
                                    relation=relation, 
                                    utterance_illocutionary_force=utterance.illocutinary_force.value,
                                    example_illocutionary_force=illocutionary_force,
                                    sbert_embedding=embedded_locution_or_proposition,
                                    num_examples=typical_respones_config.num_examples
                                    )
                    
                    result = self._query_graph(cypher)

                    relevant_graph_content.extend(
                        self._parse_retrieved_relation_examples(
                            retrieved_data=result,
                            relation=relation,
                            input_text=utterance.utterance,
                            similar_illocutionary_force=utterance.illocutinary_force.value,
                            related_illocutionary_force=illocutionary_force,
                            query_direction=QueryDirection.OUTGOING
                            )
                    )

        return relevant_graph_content
    
    def get_explicit_examples(self, utterance: Utterance, example_config: UserDefinedExamplesConfig):
        if example_config.num_examples < 1:
            raise ValueError("'UserDefinedExamplesConfig.num_examples' must be greater than 0")
        
        embedded_locution_or_proposition = self.embedding_model.encode(utterance.utterance)
    
        user_defined_examples = []
        for relation_member in example_config.relation_choices:
            relation = self.relation_types[relation_member.value]

            for illoc_force_member in example_config.query_node_choices:
                illocutionary_force = illoc_force_member.value

                if example_config.query_direction == QueryDirection.INCOMING or example_config.query_direction == QueryDirection.BOTH: 
                    cypher = self._get_cypher(
                                    query_direction=QueryDirection.INCOMING,
                                    relation=relation, 
                                    utterance_illocutionary_force=utterance.illocutinary_force.value,
                                    example_illocutionary_force=illocutionary_force,
                                    sbert_embedding=embedded_locution_or_proposition,
                                    num_examples=example_config.num_examples
                                    )
                    
                    result = self._query_graph(cypher)

                    user_defined_examples.extend(
                        self._parse_retrieved_relation_examples(
                            retrieved_data=result,
                            relation=relation,
                            input_text=utterance.utterance,
                            similar_illocutionary_force=utterance.illocutinary_force.value,
                            related_illocutionary_force=illocutionary_force,
                            query_direction=QueryDirection.INCOMING
                            )
                    )

                if example_config.query_direction == QueryDirection.OUTGOING or example_config.query_direction == QueryDirection.BOTH: 
                    cypher = self._get_cypher(
                                    query_direction=QueryDirection.OUTGOING,
                                    relation=relation, 
                                    utterance_illocutionary_force=utterance.illocutinary_force.value,
                                    example_illocutionary_force=illocutionary_force,
                                    sbert_embedding=embedded_locution_or_proposition,
                                    num_examples=example_config.num_examples
                                    )
                    
                    result = self._query_graph(cypher)

                    user_defined_examples.extend(
                        self._parse_retrieved_relation_examples(
                            retrieved_data=result,
                            relation=relation,
                            input_text=utterance.utterance,
                            similar_illocutionary_force=utterance.illocutinary_force.value,
                            related_illocutionary_force=illocutionary_force,
                            query_direction=QueryDirection.OUTGOING
                            )
                    )

        return user_defined_examples
    
    def get_similar_examples(self, utterance: Utterance, vector_based_config: VectorBasedConfig):

        if vector_based_config.num_examples < 1:
            raise ValueError("'vector_based_config.num_examples' must be greater than 0")

        embedded_locution_or_proposition = self.embedding_model.encode(utterance.utterance)

        cypher = f"""MATCH (n)
    
            WHERE n.illocutionary_force='"""+vector_based_config.similar_nodes_illocutionary_force.value+f"""' AND {self.config.political_filter.position_min} <= n.{self.config.political_filter.ensemble_or_model_name.value}_political_position_mean <= {self.config.political_filter.position_max} AND n.{self.config.political_filter.ensemble_or_model_name.value}_political_position_probability_of_na <= {self.config.political_filter.probability_of_na} AND n.{self.config.political_filter.ensemble_or_model_name.value}_political_position_std <= {str(self.config.political_filter.position_std)}
            WITH n,
                gds.similarity.cosine(n.loc_and_prop_concat_embedding_from_all_MiniLM_L6_v2, {embedded_locution_or_proposition.tolist()}) AS similarity
            ORDER BY similarity DESC
            RETURN DISTINCT n.proposition, n.locution LIMIT {vector_based_config.num_examples}"""
        
        result = self._query_graph(cypher)

        return self._parse_vector_based_examples(result, utterance.utterance, vector_based_config.similar_nodes_illocutionary_force.value)


    def _parse_vector_based_examples(self,
                                     retrieved_data: list,
                                     input_text: str,
                                     similar_illocutionary_force:str):
        
        vector_based_examples = []

        for example in retrieved_data:
            if self.config.return_type == ReturnType.LOCUTION or self.config.return_type == ReturnType.BOTH:
                vector_based_examples.append(
                    RetrievedExample(
                        retrieval_method=RetrievalMethod.VECTOR_BASED.value,
                        content_type=ReturnType.LOCUTION.value,
                        relation="",
                        input_text=input_text,
                        similar_illocutionary_force=similar_illocutionary_force,
                        related_illocutionary_force="",
                        similar_text=example[f"n.{ReturnType.LOCUTION.value}"],
                        related_text="",
                        example_text_tuple=(),
                        query_direction=""
                    )
                )
            if self.config.return_type == ReturnType.PROPOSITION or self.config.return_type == ReturnType.BOTH:
                vector_based_examples.append(
                    RetrievedExample(
                        retrieval_method=RetrievalMethod.VECTOR_BASED.value,
                        content_type=ReturnType.PROPOSITION.value,
                        relation="",
                        input_text=input_text,
                        similar_illocutionary_force=similar_illocutionary_force,
                        related_illocutionary_force="",
                        similar_text=example[f"n.{ReturnType.PROPOSITION.value}"],
                        related_text="",
                        example_text_tuple=(),
                        query_direction=""
                    )
                )
        return vector_based_examples
    

    def _parse_retrieved_relation_examples(self, 
                                  retrieved_data: list,
                                  relation: str,
                                  input_text: str,
                                  similar_illocutionary_force: str,
                                  related_illocutionary_force: str,
                                  query_direction: QueryDirection
                                  ):
        parsed_data = []
        for example in retrieved_data:
            if self.config.return_type == ReturnType.LOCUTION or self.config.return_type == ReturnType.BOTH:
                parsed_data.append(
                    RetrievedExample(
                        retrieval_method=RetrievalMethod.GRAPH_BASED.value,
                        content_type=ReturnType.LOCUTION.value,
                        relation=relation,
                        input_text=input_text,
                        similar_illocutionary_force=similar_illocutionary_force,
                        related_illocutionary_force=related_illocutionary_force,
                        similar_text=example[f"n.{ReturnType.LOCUTION.value}"],
                        related_text=example[f"m.{ReturnType.LOCUTION.value}"],
                        example_text_tuple=(example[f"n.{ReturnType.LOCUTION.value}"], example[f"m.{ReturnType.LOCUTION.value}"]) if query_direction == QueryDirection.OUTGOING else (example[f"m.{ReturnType.LOCUTION.value}"], example[f"n.{ReturnType.LOCUTION.value}"]),
                        query_direction=query_direction.value
                    )
                )
            if self.config.return_type == ReturnType.PROPOSITION or self.config.return_type == ReturnType.BOTH:
                parsed_data.append(
                    RetrievedExample(
                        retrieval_method=RetrievalMethod.GRAPH_BASED.value,
                        content_type=ReturnType.LOCUTION.value,
                        relation=relation,
                        input_text=input_text,
                        similar_illocutionary_force=similar_illocutionary_force,
                        related_illocutionary_force=related_illocutionary_force,
                        similar_text=example[f"n.{ReturnType.PROPOSITION.value}"],
                        related_text=example[f"m.{ReturnType.PROPOSITION.value}"],
                        example_text_tuple=(example[f"n.{ReturnType.PROPOSITION.value}"], example[f"m.{ReturnType.PROPOSITION.value}"]) if query_direction == QueryDirection.OUTGOING else (example[f"m.{ReturnType.PROPOSITION.value}"], example[f"n.{ReturnType.PROPOSITION.value}"]),
                        query_direction=query_direction.value
                    )
                )

        return parsed_data

    def _get_cypher(self, 
                    query_direction: QueryDirection,
                    relation:str, 
                    utterance_illocutionary_force:str, 
                    example_illocutionary_force:str,
                    sbert_embedding: np.ndarray,
                    num_examples:int                    
                    ):
        if query_direction.INCOMING:
            cypher = f"""MATCH (n)<-[r:{relation}]-(m)"""
        else:
            cypher = f"""MATCH (n)-[r:{relation}]->(m)"""

        cypher += f"""
                WHERE n.illocutionary_force='"""+utterance_illocutionary_force+"""' and m.illocutionary_force='"""+example_illocutionary_force+f"""' AND {self.config.political_filter.position_min} <= n.{self.config.political_filter.ensemble_or_model_name.value}_political_position_mean <= {self.config.political_filter.position_max} AND n.{self.config.political_filter.ensemble_or_model_name.value}_political_position_probability_of_na <= {self.config.political_filter.probability_of_na} AND n.{self.config.political_filter.ensemble_or_model_name.value}_political_position_std <= {str(self.config.political_filter.position_std)}
                WITH m, n,
                    gds.similarity.cosine(n.loc_and_prop_concat_embedding_from_all_MiniLM_L6_v2, {sbert_embedding.tolist()}) AS similarity
                ORDER BY similarity DESC
                RETURN DISTINCT m.proposition, m.locution, n.proposition, n.locution LIMIT {num_examples}"""
        
        return cypher


    def _query_graph(self, cypher):
        result = self.kb_connection.query(cypher)
        return result