import os
import json
import shutil
import tempfile
import datetime
import networkx as nx

def serialize_attributes(G):
    """
    PRE-PROCESSING: Prepares graph for GraphML export.
    1. Flattens 'name'/'description' lists into strings (RAG Optimization).
    2. Serializes other lists/dicts into JSON strings (GraphML Compat).
    """
    G_clean = G.copy()
    
    # Inject Provenance
    G_clean.graph['export_timestamp'] = datetime.datetime.now().isoformat()
    G_clean.graph['schema_version'] = "Phase_VII_Alpha"

    # NODE PROCESSING
    for node, data in G_clean.nodes(data=True):
        for k, v in data.items():
            # RAG OPTIMIZATION: Force text fields to be single strings
            if k in ['name', 'description']:
                if isinstance(v, (list, tuple, set)):
                    data[k] = "; ".join(str(x) for x in v)
                continue 
            
            # JSON SERIALIZATION for data types
            if isinstance(v, (list, dict)):
                try:
                    data[k] = json.dumps(v)
                except TypeError:
                    data[k] = str(v)

    # EDGE PROCESSING
    for u, v, data in G_clean.edges(data=True):
        for k, val in data.items():
            if isinstance(val, (list, dict)):
                try:
                    data[k] = json.dumps(val)
                except TypeError:
                    data[k] = str(val)

    return G_clean

def deserialize_attributes(G):
    """
    POST-PROCESSING: Restores Python objects from JSON strings after loading.
    """
    def try_parse(val):
        if isinstance(val, str) and (val.strip().startswith('[') or val.strip().startswith('{')):
            try:
                return json.loads(val)
            except (json.JSONDecodeError, TypeError):
                return val
        return val

    for node, data in G.nodes(data=True):
        for k, v in data.items():
            data[k] = try_parse(v)
            
    for u, v, data in G.edges(data=True):
        for k, val in data.items():
            data[k] = try_parse(val)
            
    return G

def export_graph_atomically(G, filepath):
    """
    ACID-COMPLIANT WRITE: Writes to temp file, then atomic rename.
    """
    print(f"  > Initiating Atomic Export to {filepath}...")
    G_ready = serialize_attributes(G)
    
    dirname = os.path.dirname(filepath)
    if not os.path.exists(dirname):
        os.makedirs(dirname)
        
    fd, temp_path = tempfile.mkstemp(dir=dirname, suffix='.tmp')
    os.close(fd) 
    
    try:
        nx.write_graphml(G_ready, temp_path)
        os.replace(temp_path, filepath) # Atomic Operation
        print(f"  > SUCCESS: Graph persisted. Nodes: {len(G)}, Edges: {len(G.edges())}")
    except Exception as e:
        if os.path.exists(temp_path):
            os.remove(temp_path)
        raise IOError(f"CRITICAL: Atomic export failed. {e}")

def load_graph_robust(filepath):
    """
    Robust loader with deserialization.
    """
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Graph file not found at {filepath}")
    G = nx.read_graphml(filepath)
    return deserialize_attributes(G)
