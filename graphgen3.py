import streamlit as st
import pandas as pd
from pyvis.network import Network
import networkx as nx
from io import BytesIO, StringIO

# Streamlit app title and description
st.image ("NIDLogo.jpg")
st.title ("Gerador de Grafos Interativos Baseado em Ontologias")
st.markdown ('*Ferramenta Desenvolvida pelo NID/LABCOM/UFMA  em projeto apoiado pela FAPEMA*')
st.markdown ("_[Conheça o LABCOM](https://www.labcomdata.com.br/)_")
st.markdown (" **_[Para gerar uma ontologia para o seu texto use nossa ferramenta GRAPHMaker](https://chatgpt.com/g/g-HSkRbqVrk-graphmaker)_**")


st.write("Carregue um arquivo CSV com as colunas 'Node 1', 'Node 2' e 'Edge' para criar um gráfico de ontologia interativo.")

# File uploader
uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

# Check if a file has been uploaded
if uploaded_file is not None:
    # Load the CSV data
    data = pd.read_csv(uploaded_file)
    data.columns = data.columns.str.strip()	
    
    # Validate that required columns are present
    if set(["Node 1", "Node 2", "Edge"]).issubset(data.columns):
        
        # Create the NetworkX graph
        G = nx.DiGraph()
        for _, row in data.iterrows():
            G.add_edge(row["Node 1"], row["Node 2"], label=row["Edge"])

        # Create a Pyvis Network object
        net = Network(height="750px", width="100%", directed=True)
        
        # Convert NetworkX graph to Pyvis network
        for node in G.nodes:
            net.add_node(node, label=node)

        for source, target, data in G.edges(data=True):
            net.add_edge(source, target, label=data["label"])

        # Generate interactive visualization in HTML
        net.show_buttons(filter_=['physics'])  # Optionally add physics controls
        html_path = "interactive_graph.html"
        net.save_graph(html_path)

        # Display interactive graph in Streamlit
        st.components.v1.html(open(html_path, "r").read(), height=750)

        # Option to save the visualization
        save_option = st.checkbox("Save interactive graph as HTML")
        if save_option:
            st.download_button(
                label="Download Interactive Graph",
                data=open(html_path, "r").read(),
                file_name="interactive_ontology_graph.html",
                mime="text/html"
            )
    else:
        st.error("The CSV file must contain columns: 'Node 1', 'Node 2', and 'Edge'.")
else:
    st.info("Please upload a CSV file to visualize the graph.")
