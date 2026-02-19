import pandas as pd
import networkx as nx
import os
import json
from tqdm import tqdm


class TranslationFromAIF2ASPIC2DAF:
    def __init__(self, path_to_folder_with_json):
        self.data_path = path_to_folder_with_json

        #extra_node_data, logical_language, lang, lang_R, conflicts, self.rephrases, preferences = self.process_inferences_conflicts_and_rephrases_from_AIF()
        self.data, logical_language, lang, lang_R, conflicts, self.rephrases, preferences = self.process_inferences_conflicts_and_rephrases_from_AIF()

      
   
        self.args, self.relations = self.instantiate_ASPIC_argumentation_theory_and_convert_to_DAF(logical_language=logical_language,
                                                                                            lang_R=lang_R,
                                                                                            conflicts=[(conflict["Default Conflict"][0], conflict["Default Conflict"][1]) for conflict in conflicts])#,
                                                                                            #extra_data_from_nodes=extra_node_data)

 


    def process_inferences_conflicts_and_rephrases_from_AIF(self):

        logical_language = []
        lang = []
        lang_R = []
        conflicts = []
        rephrases = []
        preferences = []
        rule_count = 0
        data = []
        propositions_locutions_and_illocutionary_force_and_transitions = []

        for file in tqdm(os.listdir(self.data_path)):
            if file.endswith('.json'):
                #print(file)
                with open(self.data_path +"\\"+ file, encoding="utf-8") as json_file:
                    arg_map = json.load(json_file)
                    if "AIF" in arg_map.keys():
                        aif_nodes = arg_map['AIF']['nodes']
                        aif_edges = arg_map["AIF"]["edges"]

                    else:
                        aif_nodes = arg_map['nodes']
                        aif_edges = arg_map["edges"]

                    for node in aif_nodes:
                        if node["type"] == "I":
                            for edge1 in aif_edges:
                                
                                if edge1["toID"] == node["nodeID"]:
                                    #print(edge1)
                                    for node2 in aif_nodes:
                                        if (node2["type"] == "YA") and (edge1["fromID"] == node2["nodeID"]):
                                            #print(node2["text"])
                                            if node2["text"] == "Asserting":
                                                """ 
                                                The asserting node type can be an instance of a ___Claim___, ___NotClaim___, and ___Since___ moves
                                                """
                                                for edge2 in aif_edges:
                                                    if edge2["toID"] == node2["nodeID"]:
                                                        #print(edge2)
                                                        for node3 in aif_nodes:
                                                            if (node3["type"] == "L") and (node3["nodeID"] == edge2["fromID"]):
                                                                propositional_content = node["text"]
                                                                locution = node3["text"]
                                                                speaker = node3["text"].split(":", 1)[0]
                                                                illocutionary_force = "Asserting"
                                                                data.append([propositional_content, locution, illocutionary_force, speaker, node["timestamp"]])


                                            elif (node2["text"] == "Pure Questioning"):
                                                """ 
                                                This node type corresponding to an information-seeking question and also the ___Question___ move
                                                """
                                                for edge2 in aif_edges:
                                                    if edge2["toID"] == node2["nodeID"]:
                                                        #print(edge2)
                                                        for node3 in aif_nodes:
                                                            if (node3["type"] == "L") and (node3["nodeID"] == edge2["fromID"]):
                                                                propositional_content = node["text"]
                                                                locution = node3["text"]
                                                                speaker = node3["text"].split(":", 1)[0]
                                                                illocutionary_force = "Pure Questioning"
                                                                data.append([propositional_content, locution, illocutionary_force, speaker, node["timestamp"]])
                                            
                                            elif (node2["text"] == "Assertive Questioning"):
                                                """ 
                                                This type of question is a biased one where the locutor usually knows the answer to the question they are asking, and
                                                corresponds to the ___Question___ move
                                                """
                                                for edge2 in aif_edges:
                                                    if edge2["toID"] == node2["nodeID"]:
                                                        #print(edge2)
                                                        for node3 in aif_nodes:
                                                            if (node3["type"] == "L") and (node3["nodeID"] == edge2["fromID"]):
                                                                propositional_content = node["text"]
                                                                locution = node3["text"]
                                                                speaker = node3["text"].split(":", 1)[0]
                                                                illocutionary_force = "Assertive Questioning"
                                                                data.append([propositional_content, locution, illocutionary_force, speaker, node["timestamp"]])
                                            
                                            elif (node2["text"] == "Rhetorical Questioning"):
                                                """ 
                                                Rhetorical questions are most likely part of eristic dialgoues but can be used to make an obvious point, and we assume that
                                                rhetorical questions also correspond to the ___Question___ move"""
                                                for edge2 in aif_edges:
                                                    if edge2["toID"] == node2["nodeID"]:
                                                        #print(edge2)
                                                        for node3 in aif_nodes:
                                                            if (node3["type"] == "L") and (node3["nodeID"] == edge2["fromID"]):
                                                                propositional_content = node["text"]
                                                                locution = node3["text"]
                                                                speaker = node3["text"].split(":", 1)[0]
                                                                illocutionary_force = "Rhetorical Questioning"
                                                                data.append([propositional_content, locution, illocutionary_force, speaker, node["timestamp"]])

                                            elif (node2["text"] == "Challenging"):
                                                """ 
                                                This node type corresponds to the ___Why___ move
                                                """
                                                for edge2 in aif_edges:
                                                    if edge2["toID"] == node2["nodeID"]:
                                                        #print(edge2)
                                                        for node3 in aif_nodes:
                                                            if (node3["type"] == "L") and (node3["nodeID"] == edge2["fromID"]):
                                                                propositional_content = node["text"]
                                                                locution = node3["text"]
                                                                speaker = node3["text"].split(":", 1)[0]
                                                                illocutionary_force = "Challenging"
                                                                data.append([propositional_content, locution, illocutionary_force, speaker, node["timestamp"]])

                                            elif (node2["text"] == "Agreeing"):
                                                """ 
                                                This node type corresponds to the ___Why___ move
                                                """
                                                for edge2 in aif_edges:
                                                    if edge2["toID"] == node2["nodeID"]:
                                                        #print(edge2)
                                                        for node3 in aif_nodes:
                                                            if (node3["type"] == "L") and (node3["nodeID"] == edge2["fromID"]):
                                                                propositional_content = node["text"]
                                                                locution = node3["text"]
                                                                speaker = node3["text"].split(":", 1)[0]
                                                                illocutionary_force = "Agreeing"
                                                                data.append([propositional_content, locution, illocutionary_force, speaker, node["timestamp"]])


                                            elif (node2["text"] == "Disagreeing"):
                                                """ 
                                                This node type corresponds to the ___Why___ move
                                                """
                                                for edge2 in aif_edges:
                                                    if edge2["toID"] == node2["nodeID"]:
                                                        #print(edge2)
                                                        for node3 in aif_nodes:
                                                            if (node3["type"] == "L") and (node3["nodeID"] == edge2["fromID"]):
                                                                propositional_content = node["text"]
                                                                locution = node3["text"]
                                                                speaker = node3["text"].split(":", 1)[0]
                                                                illocutionary_force = "Disagreeing"
                                                                data.append([propositional_content, locution, illocutionary_force, speaker, node["timestamp"]])
                    
                            

        
                            logical_language.append({"text" : node["text"],
                                                    "ID"   : node["nodeID"]})
                            lang.append(node["text"])

                        # Finding edges towards/from RA node
                        if node["type"] == "RA":
                            t1 = []
                            t2 = None
                            c1 = []
                            c2 = None
                            link = None
                            type_of_node = None
                            from_id = []
                            to_id = None
                            ck1 = False
                            ck2 = False

                            # Link node detected of type RA node
                            link = node['nodeID']
                            type_of_node = node['type']

                            for edge in aif_edges:

                                if link == edge['toID']:
                                    c1.append(edge['fromID'])
                                    ck1 = True

                                elif link == edge['fromID']:
                                    c2 = edge['toID']
                                    ck2 = True

                            # Retrieving the text from the nodes
                            if (not t1 and ck1 == True) or (t2 == None and ck2 == True):
                                for node2 in aif_nodes:
                                    if node2['nodeID'] in c1 and node2['type'] == 'I':
                                        t1.append(node2['text'])
                                        from_id.append(node2["nodeID"])

                                    elif node2['nodeID'] == c2 and node2['type'] == 'I':
                                        t2 = node2['text']
                                        to_id = node2["nodeID"]

                            if t1 and t2 != None:
                                lang_R.append({"rule_{}".format(rule_count) : (list(set(t1)), t2),
                                            "RA_ID" : node["nodeID"],
                                                "nodeIDs"                       : (list(set(from_id)), to_id)})

                                lang.append("rule_{}".format(rule_count))
                                rule_count += 1

                        if node["type"] == "CA":
                            t1 = None
                            t2 = None
                            c1 = None
                            c2 = None
                            link = None
                            type_of_node = None
                            from_id = None
                            to_id = None

                            # Link node detected of type RA node
                            link = node['nodeID']
                            type_of_node = node['type']

                            for edge in aif_edges:
                                ck1 = False
                                ck2 = False

                                if link == edge['toID']:
                                    c1 = edge['fromID']
                                    ck1 = True

                                elif link == edge['fromID']:
                                    c2 = edge['toID']
                                    ck2 = True

                                # Retrieving the text from the nodes
                                if (t1 == None and ck1 == True) or (t2 == None and ck2 == True):
                                    for node2 in aif_nodes:
                                        if node2['nodeID'] == c1 and node2['type'] == 'I':
                                            t1 = node2['text']
                                            from_id = node2["nodeID"]

                                        elif node2['nodeID'] == c2 and node2['type'] == 'I':
                                            t2 = node2['text']
                                            to_id = node2["nodeID"]


                            if t1 and t2 != None:
                                conflicts.append({"Default Conflict" : (t1, t2),
                                                "CA_ID": node["nodeID"],
                                                "nodeIDs"           : (from_id, to_id)})

                        if node["type"] == "MA":
                            t1 = None
                            t2 = None
                            c1 = None
                            c2 = None
                            link = None
                            type_of_node = None
                            from_id = None
                            to_id = None

                            # Link node detected of type RA node
                            link = node['nodeID']
                            type_of_node = node['type']

                            for edge in aif_edges:
                                ck1 = False
                                ck2 = False

                                if link == edge['toID']:
                                    c1 = edge['fromID']
                                    ck1 = True

                                elif link == edge['fromID']:
                                    c2 = edge['toID']
                                    ck2 = True

                                # Retrieving the text from the nodes
                                if (t1 == None and ck1 == True) or (t2 == None and ck2 == True):
                                    for node2 in aif_nodes:
                                        if node2['nodeID'] == c1 and node2['type'] == 'I':
                                            t1 = node2['text']
                                            from_id = node2["nodeID"]

                                        elif node2['nodeID'] == c2 and node2['type'] == 'I':
                                            t2 = node2['text']
                                            to_id = node2["nodeID"]

                            if t1 and t2 != None:
                                rephrases.append({node["text"] : (t1, t2),
                                                "MA_ID": node["nodeID"],
                                                "nodeIDs"           : (from_id, to_id)})
                            
                                
        return data, logical_language, lang, lang_R, conflicts, rephrases, preferences
    

    def instantiate_ASPIC_argumentation_theory_and_convert_to_DAF(self, 
                                                                  logical_language,
                                                                  lang_R,
                                                                  conflicts):#,
                                                                  #extra_data_from_nodes):
        predecessor_nodes = []
        K_p = []

        for node in logical_language:
            for index, rule in enumerate(lang_R):

                if node["text"] == rule["rule_{}".format(index)][1]:
                    predecessor_nodes.append(node["text"])

        for node in logical_language:
            if node["text"] not in predecessor_nodes:
                K_p.append(node["text"])


        args = []
        count = 0

        print("args")
        for index, arg in enumerate(tqdm(K_p)):
            from_arg = arg
            args.append({"{}".format(count) : ([str(arg)],None)})
            count += 1
            
        for rule_index, rule in enumerate(tqdm(lang_R)):
            check =  set(rule["rule_{}".format(rule_index)][0]) <= set(K_p)
            if check == False:
                continue
            conclusion = None
            premises = []
            premise_check = []
            for arg_index, arg in enumerate(args):
                for premise in arg["{}".format(arg_index)][0]:
                    if premise in rule["rule_{}".format(rule_index)][0]:
                        premises.append("{}".format(arg_index)) 
                        premise_check.append(premise)     
            if check == True:
                conclusion = rule["rule_{}".format(rule_index)][1]
                if premises and conclusion != None:
                    args.append({"{}".format(str(count)) : (premises,conclusion)})        
                    count += 1   
        R_lang = []
        for rule in reversed(lang_R):
            R_lang.append(rule)

        print("R_lang")
        for r_index, rule in enumerate(tqdm(R_lang)):
            rule_index = len(lang_R) - r_index - 1
            check =  set(rule["rule_{}".format(rule_index)][0]) <= set(K_p)
            if check == True:
                continue  
            conclusion = None
            premises = []

            for arg_index, arg in enumerate(args):
                for premise in arg["{}".format(arg_index)][0]:
                    if premise in rule["rule_{}".format(rule_index)][0]:
                        premises.append("{}".format(arg_index))

                conc_check = arg["{}".format(arg_index)][1]

                if conc_check == None:
                    continue
                else:
                    if conc_check in rule["rule_{}".format(rule_index)][0]:
                        premises.append("{}".format(arg_index))

            conclusion = rule["rule_{}".format(rule_index)][1]        
            if premises and conclusion != None:
                args.append({"{}".format(str(count)) : (premises,conclusion)})        
                count += 1    
        

        attacks = []

        print("conflicts")
        for conflict in tqdm(conflicts):
            attack_from = None
            attack_to = None

            for arg_index, arg in enumerate(args):
                if (conflict[0] in arg["{}".format(arg_index)][0]) or (conflict[0] == arg["{}".format(arg_index)][1]):
                    attack_from = "{}".format(arg_index)


                if (conflict[1] in arg["{}".format(arg_index)][0]) or (conflict[1] == arg["{}".format(arg_index)][1]):
                    attack_to = "{}".format(arg_index)

                if (attack_from != None) and (attack_to != None) and ((attack_from, attack_to) not in attacks):
                    attacks.append((attack_from, attack_to))

        return args, attacks

    def return_DAF(self):
        return self.args, list(set(self.relations)), self.data, self.rephrases