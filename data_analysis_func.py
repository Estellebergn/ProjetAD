from sklearn.decomposition import PCA
import pandas as pd
import util_func as util

def get_pca(data):
    # Normalisation des données
    data_norm = util.standardise(data)

    # Regarder valeurs manquantes
    if data_norm.isnull().sum().sum() > 10:
        print("Il y a trop de valeurs manquantes")
        print(data_norm[data_norm.isnull().any(axis=1)])
        print(data_norm.columns[data_norm.isnull().any()])
    elif data_norm.isnull().sum().sum() in range(1, 10):
        # remplacer les valeurs manquantes par la moyenne
        data_norm.fillna(data_norm.mean(), inplace=True)    

    pca = PCA(n_components=2)  # Choisissez le nombre de composantes souhaité
    principal_components = pca.fit_transform(data_norm)
    principal_df = pd.DataFrame(data=principal_components, columns=['PC1', 'PC2'])
    # Récupérer les autres colonnes
    principal_df[['Country','Regional indicator', 'Happiness Score', 'Generosity', 'Social support', 'Logged GDP per capita', 'Healthy life expectancy', 'Freedom', 'Perceptions of corruption']] = data[['Country','Regional indicator', 'Happiness Score', 'Generosity', 'Social support', 'Logged GDP per capita', 'Healthy life expectancy', 'Freedom', 'Perceptions of corruption']]

    return principal_df

## CLUSTERING

from sklearn.metrics import silhouette_score
from sklearn.preprocessing import StandardScaler
import tools as t
from sklearn.mixture import GaussianMixture
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score

# KMEANS

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


def silhouette_scores(df, n_clusters,method) :
    """
    Calcule les scores de silhouette pour un nombre de clusters donné et une méthode donnée

    :param df: DataFrame contenant les données
    :type df: pandas.DataFrame
    :param n_clusters: Nombre de clusters maximal
    :type n_clusters: int
    :param method: Méthode de clustering ("kmeans" ou "gmm")
    :type method: str
    :return: Dictionnaire des scores de silhouette
    :rtype: dict
    """
    silhouette_scores = {}
    for i in range(2, n_clusters+1) :
        if method == "kmeans":
            kmeans, label, centroid = kmeans_clustering(df, i)
        elif method == "gmm":
            gmm, label, centroid = gausian_mixture_clustering(df, i)
        else :
            print("Méthode pour silhouette non reconnue")
            return
        silhouette_scores[i] = silhouette_score(df, label)
    return silhouette_scores


