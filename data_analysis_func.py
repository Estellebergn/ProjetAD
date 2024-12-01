from sklearn.decomposition import PCA
import pandas as pd
import util_func as util

def get_pca(data):
    # Normalisation des données
    data_norm = util.standardise(data)

    if data_norm.isnull().sum().sum() > 10:
        print("Il y a trop de valeurs manquantes")
        return None
        print(data_norm[data_norm.isnull().any(axis=1)])
        print(data_norm.columns[data_norm.isnull().any()])
    elif data_norm.isnull().sum().sum() in range(1, 10):
        # remplacer les valeurs manquantes par la moyenne
        data_norm.fillna(data_norm.mean(), inplace=True)    

    pca = PCA(n_components=2)  # Choisissez le nombre de composantes souhaité
    principal_components = pca.fit_transform(data_norm)
    principal_df = pd.DataFrame(data=principal_components, columns=['PC1', 'PC2'])
    print("columns\n\t", principal_df.columns)
    principal_df[['Country','Regional indicator', 'Happiness Score', 'Generosity', 'Social support', 'Logged GDP per capita', 'Healthy life expectancy', 'Freedom', 'Perceptions of corruption']] = data[['Country','Regional indicator', 'Happiness Score', 'Generosity', 'Social support', 'Logged GDP per capita', 'Healthy life expectancy', 'Freedom', 'Perceptions of corruption']]

    return principal_df
