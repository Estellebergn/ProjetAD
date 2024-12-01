import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.mixture import GaussianMixture
import numpy as np
from sklearn.cluster import SpectralClustering
from sklearn.decomposition import PCA

###Clustering
def standardise_data(df) :
    """
    Standardise data
    """
    scaler = StandardScaler()
    return scaler.fit_transform(df)

def kmeans_clustering(df, n_clusters) :
    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    kmeans.fit(df)
    label = kmeans.labels_
    centroid = kmeans.cluster_centers_
    return kmeans, label, centroid

def gausian_mixture_clustering(df, n_clusters) :
    gmm = GaussianMixture(n_components=n_clusters, random_state=42)
    gmm.fit(df)
    label = gmm.predict(df)
    centroid = gmm.means_
    return gmm, label, centroid

def display_silhouette_scores(scores, method_name) :
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=list(scores.keys()),
        y=list(scores.values()),
        mode='lines+markers',
        name='Silhouette Score',
        line=dict(color='blue'),
        marker=dict(size=8)
    ))

    fig.update_layout(
        title=f"Méthode de la silhouette pour {method_name}",
        xaxis_title='Nombre de clusters',
        yaxis_title='Indice de silhouette moyen',
        template='plotly_white'
    )

    fig.show()

def display_clustering(df) :
    fig_kmeans = px.scatter(
    template='plotly_white',
    data_frame=df, 
    x='PC1', 
    y='PC2', 
    color='cluster', 
    hover_name='Country name',
    color_discrete_sequence=px.colors.qualitative.G10,
)
    fig_kmeans.update_layout(showlegend=False)
    fig_kmeans.show()
    return fig_kmeans
    
def add_centroids(fig, centroids) :
    fig.add_trace(
    go.Scatter(
        x=centroids['PC1'],
        y=centroids['PC2'],
        mode='markers',
        marker=dict(size=12, color='black', symbol='x'),
        name='Centroïdes'
        )
    )
    
    # Cacher la légende
    fig.update_layout(showlegend=False)
    fig.show()

def consensus_plot(df, n_clusters):
    kmeans, kmeans_labels, _ = kmeans_clustering(df, n_clusters)
    gmm, gmm_labels, _ = gausian_mixture_clustering(df, n_clusters)

    #matrice de consensus
    n_samples = df.shape[0]
    C = np.zeros((n_samples, n_samples))

    #comparaison des labels
    for i in range(n_samples):
        for j in range(i + 1, n_samples):
            if kmeans_labels[i] == kmeans_labels[j]:
                C[i, j] += 1
                C[j, i] += 1
            if gmm_labels[i] == gmm_labels[j]:
                C[i, j] += 1
                C[j, i] += 1

    #normaliser la matrice de consensus
    C = C / 2

    #matrice de distance
    distance_matrix = 1 / (C + np.eye(n_samples))  # Ajout de l'identité pour éviter division par zéro
    distance_matrix[np.isinf(distance_matrix)] = 0  # Remplacer les infinis par 0
    distance_matrix[np.isnan(distance_matrix)] = 0

    #Clustering avec cette matrice de distance
    spectral = SpectralClustering(n_clusters=3, affinity='precomputed', random_state=42)
    final_labels = spectral.fit_predict(distance_matrix)
    return final_labels

def visualise_consensus(total_df, final_labels) :
    total_df['cluster'] = final_labels

    fig = px.scatter(
        total_df,
        x='PC1', 
        y='PC2', 
        color='cluster',
        title="Clustering Consensuel avec K-Means et GMM",
        labels={'cluster': 'Cluster'},
        color_continuous_scale="Viridis"
        )

    fig.update_layout(
        template="plotly_white",  # Fond blanc pour un look propre
        showlegend=False
    )

    fig.show()




    