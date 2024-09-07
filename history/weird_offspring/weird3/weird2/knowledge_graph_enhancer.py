import networkx as nx

class KnowledgeGraphEnhancer:
    def __init__(self):
        self.graph = nx.DiGraph()

    def add_concept(self, concept, attributes):
        self.graph.add_node(concept, **attributes)

    def add_relation(self, concept1, concept2, relation_type):
        self.graph.add_edge(concept1, concept2, type=relation_type)

    def find_connections(self, concept, max_depth=3):
        return nx.dfs_successors(self.graph, concept, depth_limit=max_depth)

    def generate_insights(self, concept):
        connections = self.find_connections(concept)
        return f"Insights for {concept}: {connections}"

kg_enhancer = KnowledgeGraphEnhancer()
kg_enhancer.add_concept("AI", {"domain": "technology"})
kg_enhancer.add_concept("Ethics", {"domain": "philosophy"})
kg_enhancer.add_relation("AI", "Ethics", "requires consideration of")
