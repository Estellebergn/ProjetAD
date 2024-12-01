import plotly.express as px
import networkx as nx
import plotly.graph_objects as go
import community.community_louvain as community

def display_heatmap(df) : 
    fig = px.imshow(
    df,
    title="Correlation Heatmap",
    labels=dict(x="Columns", y="Columns", color="Correlation"),
    color_continuous_scale="RdBu",
    zmin=-1, zmax=1, text_auto=True
)
    fig.update_layout(width=900, height=800)
    fig.show()

def create_graphe(correlation_matrix, threshold, countries):
    # Créer un graphe NetworkX
    graph = nx.Graph()

    # Ajouter les nœuds (entités)
    for i, country in enumerate(countries):
        graph.add_node(i, label=country)

    # Ajouter les arêtes si la corrélation dépasse le seuil
    for i in range(len(correlation_matrix)):
        for j in range(i + 1, len(correlation_matrix)):
            if correlation_matrix[i, j] > threshold :
                graph.add_edge(i, j, weight=correlation_matrix[i, j])
    
    return graph

def display_graph(graph, color_by) :
    # Positionnement des nœuds avec spring_layout
    pos = nx.spring_layout(graph, seed=42)

    # Préparer les données pour Plotly
    edge_x = []
    edge_y = []

    # Ajout des arêtes
    for edge in graph.edges(data=True):
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_x.append(x0)
        edge_x.append(x1)
        edge_x.append(None)  # None pour séparer les lignes
        edge_y.append(y0)
        edge_y.append(y1)
        edge_y.append(None)

    # Tracer les arêtes
    edge_trace = go.Scatter(
        x=edge_x,
        y=edge_y,
        line=dict(width=0.5, color="#888"),
        hoverinfo="none",
        mode="lines"
    )

    # Ajouter les nœuds
    node_x = []
    node_y = []
    node_labels = []

    for node in graph.nodes(data=True):
        x, y = pos[node[0]]
        node_x.append(x)
        node_y.append(y)
        node_labels.append(node[1]['label'])

    node_trace = go.Scatter(
        x=node_x,
        y=node_y,
        mode="markers+text",
        text=node_labels,
        textposition="top center",
        hoverinfo="text",
        marker=dict(
            color = color_by,
            colorscale="Plasma",
            size=10,
            line_width=2
        )
    )

    # Créer la figure Plotly
    fig = go.Figure(data=[edge_trace, node_trace],
                    layout=go.Layout(
                        title=f"Réseau des corrélations",
                        titlefont_size=16,
                        showlegend=False,
                        hovermode="closest",
                        margin=dict(b=0, l=0, r=0, t=40),
                        xaxis=dict(showgrid=False, zeroline=False),
                        yaxis=dict(showgrid=False, zeroline=False)
                    ))

    fig.show()


def communaute(graph) :
    #Appliquer louvain
    partition = community.best_partition(graph)
    nx.set_node_attributes(graph, partition, 'community')
    return graph, partition

"""
    #Ajouter les communaute comme partition
    
    for node, community_id in partition.items():
        print(f"Pays : {node}, Communauté : {community_id}")

"""