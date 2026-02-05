import streamlit as st
import networkx as nx
from pyvis.network import Network
from groq import Groq
import json
import os
import streamlit.components.v1 as components

# --- Page Configuration ---
st.set_page_config(
    page_title="Knowledge Graph Generator",
    page_icon="🕸️",
    layout="wide"
)

st.title("🕸️ Instant Knowledge Graph (Groq Edition ⚡)")
st.markdown("Generate interactive knowledge graphs instantly using **Llama-3** on **Groq's LPU**.")

# --- API Key Management ---
def get_groq_api_key():
    api_key = None
    # 1. Try fetching from Streamlit secrets
    try:
        if "GROQ_API_KEY" in st.secrets:
            api_key = st.secrets["GROQ_API_KEY"]
    except Exception:
        pass

    # 2. Try fetching from environment variables
    if not api_key:
        api_key = os.getenv("GROQ_API_KEY")

    # 3. Manual input via Sidebar
    if not api_key:
        with st.sidebar:
            st.header("🔑 Authentication")
            api_key = st.text_input(
                "Enter Groq API Key", 
                type="password", 
                help="Get a free key here: https://console.groq.com/keys"
            )
            st.markdown("[Get Free API Key](https://console.groq.com/keys)")
    
    return api_key

# --- Core Logic: Knowledge Extraction ---
def extract_knowledge_graph(text, api_key):
    """
    Sends text to Llama-3 via Groq to extract entities and relationships in JSON format.
    """
    client = Groq(api_key=api_key)
    
    prompt = f"""
    You are an expert Knowledge Graph Extractor.
    Analyze the following text and extract key concepts and their relationships.
    
    Return ONLY a JSON object with this exact structure:
    {{
      "concepts": ["Concept 1", "Concept 2"],
      "relationships": [
        {{"source": "Concept 1", "target": "Concept 2", "relationship": "verb phrase"}}
      ]
    }}

    Text to analyze:
    {text}
    """

    try:
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile", # Using the latest versatile model
            messages=[
                {"role": "system", "content": "You are a helpful assistant that outputs only valid JSON."},
                {"role": "user", "content": prompt}
            ],
            temperature=0,
            response_format={"type": "json_object"}
        )
        
        content = completion.choices[0].message.content
        return json.loads(content)

    except Exception as e:
        st.error(f"Error calling Groq API: {e}")
        return None

# --- Graph Construction (NetworkX) ---
def create_networkx_graph(data):
    """
    Converts JSON data into a NetworkX graph object with visual attributes.
    """
    G = nx.Graph()
    
    # Add nodes
    for concept in data.get("concepts", []):
        G.add_node(concept, title=concept)
    
    # Add edges
    for rel in data.get("relationships", []):
        source = rel.get("source")
        target = rel.get("target")
        relationship = rel.get("relationship", "")
        if source and target:
            G.add_edge(source, target, title=relationship, label=relationship)
            
    # Calculate degree centrality for node sizing
    degrees = dict(G.degree())
    
    # Community detection for coloring
    try:
        from networkx.algorithms import community
        communities = community.greedy_modularity_communities(G)
        
        # Cyberpunk / Neon color palette
        colors = ["#FF5733", "#33FF57", "#3357FF", "#F333FF", "#33FFF5", "#FFFF33"]
        
        node_colors = {}
        for i, comm in enumerate(communities):
            color = colors[i % len(colors)]
            for node in comm:
                node_colors[node] = color
    except:
        # Fallback color if community detection fails
        node_colors = {node: "#97c2fc" for node in G.nodes()}

    # Apply visual attributes to nodes
    for node in G.nodes():
        size = 20 + (degrees[node] * 5)
        color = node_colors.get(node, "#97c2fc")
        
        G.nodes[node]['size'] = size
        G.nodes[node]['color'] = color
        G.nodes[node]['font'] = {
            'color': 'white', 
            'size': 16, 
            'face': 'Verdana',
            'background': 'rgba(0,0,0,0.7)',
            'strokeWidth': 2,
            'strokeColor': '#000000'
        }

    return G

# --- Visualization (PyVis) ---
def create_pyvis_graph(nx_graph):
    """
    Generates the interactive HTML graph using PyVis.
    Includes stabilization logic to prevent 'wobbly' graphs.
    """
    net = Network(height="650px", width="100%", bgcolor="#0E1117", font_color="white", directed=False)
    net.from_nx(nx_graph)
    
    # Physics and Layout options
    net.set_options("""
    {
      "nodes": {
        "shape": "dot",
        "size": 20,
        "font": {
          "size": 18,
          "face": "Tahoma",
          "background": "rgba(0,0,0,0.7)",
          "strokeWidth": 0,
          "color": "white"
        },
        "borderWidth": 2,
        "shadow": true
      },
      "edges": {
        "color": {
          "color": "rgba(255,255,255,0.5)",
          "highlight": "#ffffff"
        },
        "width": 1.5,
        "smooth": {
          "type": "continuous", 
          "roundness": 0
        }
      },
      "physics": {
        "enabled": true,
        "barnesHut": {
          "gravitationalConstant": -4000,
          "centralGravity": 0.1,
          "springLength": 300,
          "springConstant": 0.02,
          "damping": 0.09,
          "avoidOverlap": 1
        },
        "stabilization": {
          "enabled": true,
          "iterations": 1000,
          "updateInterval": 50,
          "onlyDynamicEdges": false,
          "fit": true
        },
        "minVelocity": 0.75
      }
    }
    """)
    
    import tempfile
    with tempfile.NamedTemporaryFile(delete=False, suffix=".html") as tmp:
        net.save_graph(tmp.name)
        with open(tmp.name, 'r', encoding='utf-8') as f:
            return f.read()

# --- Main Application Logic ---
def main():
    api_key = get_groq_api_key()
    
    if not api_key:
        st.warning("⬅️ Please enter your Groq API Key in the sidebar to start.")
        st.stop()
    
    text_input = st.text_area(
        "📝 Enter Text (Syllabus, Article, Summary):", 
        height=150, 
        placeholder="Paste your text here..."
    )
    
    if st.button("🚀 Generate Graph", type="primary", use_container_width=True):
        if not text_input.strip():
            st.warning("Please enter some text first.")
            return
        
        with st.spinner("⚡ Processing with Llama-3 on Groq..."):
            data = extract_knowledge_graph(text_input, api_key)
            
            if data:
                nx_graph = create_networkx_graph(data)
                
                if len(nx_graph.nodes()) > 0:
                    col1, col2 = st.columns(2)
                    col1.metric("Concepts Found", len(nx_graph.nodes()))
                    col2.metric("Connections", len(nx_graph.edges()))
                    
                    html_string = create_pyvis_graph(nx_graph)
                    st.subheader("Interactive Graph Result:")
                    components.html(html_string, height=650, scrolling=True)
                else:
                    st.warning("No concepts found in the text. Try a different text.")

if __name__ == "__main__":
    main()
