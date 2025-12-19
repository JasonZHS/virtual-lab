import networkx as nx
from alzkb.utils.io import load_graph_robust

class GraphDriver:
    _instance = None
    _graph = None

    def __new__(cls, filepath="alzkb/data/alzkb_knowledge_graph.graphml"):
        if cls._instance is None:
            cls._instance = super(GraphDriver, cls).__new__(cls)
            cls._instance.filepath = filepath
            cls._instance.load_data()
        return cls._instance

    def load_data(self):
        try:
            self._graph = load_graph_robust(self.filepath)
        except Exception as e:
            print(f"  > [GraphDriver] CRITICAL: Persisted graph missing or invalid at {self.filepath}: {e}")
            self._graph = nx.DiGraph()

    @staticmethod
    def get_deep_context(query, min_conf):
        """
        Retrieves context subgraph for RAG.
        """
        driver = GraphDriver()
        if not driver._graph: return nx.DiGraph()
        
        # Simple string matching for query node
        # In real system, use an index.
        target_node = None
        for node in driver._graph.nodes():
            if query.lower() in str(node).lower():
                target_node = node
                break
        
        if target_node:
            return nx.ego_graph(driver._graph, target_node, radius=2)
        return nx.DiGraph()

    @staticmethod
    def get_visual_subgraph(query, context_graph, limit=50, strategy=None, rank_by=None):
        """
        Returns subgraph for Visualization. 
        Context graph is already a subgraph, so we just return it or prune it.
        """
        return context_graph

    @staticmethod
    def display_provenance(node_id):
        import streamlit as st
        driver = GraphDriver()
        if driver._graph and node_id in driver._graph.nodes:
            data = driver._graph.nodes[node_id]
            st.write(data)
        else:
            st.write(f"Node {node_id} not found.")

# Keep Backend Stubs for RAG and Viz if they haven't been migrated yet, 
# or import them if they exist in separate files.
# Looking at previous __init__.py, they were stubs.
# We should preserve them or import simple versions.

class RAGEngine:
    @staticmethod
    def generate_safe_narrative(query, context_graph, strictness):
        from alzkb.retrieval.rag_wrapper import graph_to_text
        # We need to adapt the rag wrapper to return HTML or just text
        return type('obj', (object,), {'html_content': f"<b>RAG Result for {query}</b><br>Graph Size: {len(context_graph)}"})

class VizBuilder:
    @staticmethod
    def render_interactive(graph, style_profile, flatten_reified_edges):
        import streamlit as st
        import graphviz
        
        dot = graphviz.Digraph()
        
        # Limit nodes to prevent crash
        nodes = list(graph.nodes())[:50]
        
        for n in nodes:
            dot.node(str(n), str(n))
            
        for u, v, data in list(graph.edges(data=True))[:50]:
            # Extract predicate for label, strip 'biolink:' for brevity if preferred
            label = data.get('predicate', '')
            if label.startswith('biolink:'):
                label = label.replace('biolink:', '')
            # Replace underscores for readability
            label = label.replace('_', ' ')
            
            dot.edge(str(u), str(v), label=label, fontsize='10')
            
        st.graphviz_chart(dot)
        return None
