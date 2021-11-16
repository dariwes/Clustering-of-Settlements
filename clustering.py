import matplotlib.pyplot as plt
import pandas as pd
from sklearn.cluster import KMeans
from db_manager import DatabaseManager
from config import db_settings


def cluster_amount(x, hours):
    wcss = []
    for count in range(1, 11):
        kmeans = KMeans(n_clusters=count, init='k-means++', random_state=int())
        kmeans.fit(x)
        wcss.append(kmeans.inertia_)
    plt.plot(range(1, 11), wcss)
    plt.title(f'The Elbow Method ({hours} hours)')
    plt.xlabel('Number of clusters')
    plt.ylabel('WCSS')
    plt.show()


def split_clusters(hours):
    durations = {
        0.5: dict(min_duration=0, max_duration=1800),
        1: dict(min_duration=1800, max_duration=3600),
        1.5: dict(min_duration=3600, max_duration=5400),
    }.get(hours)
    db_manager = DatabaseManager(**db_settings)
    dataset = db_manager.get_certain_durations(**durations)
    dataset = pd.DataFrame(
        columns=['name', 'latitude', 'longitude'], data=dataset
    )
    x = dataset.iloc[:, [1, 2]].values
    cluster_amount(x, hours)
    kmeans = KMeans(n_clusters=5, init='k-means++', random_state=int())
    y_kmeans = kmeans.fit_predict(x)
    plt.scatter(
        x[y_kmeans == 0, 0], x[y_kmeans == 0, 1],
        s=10, c='red', label='Cluster 1'
    )
    plt.scatter(
        x[y_kmeans == 1, 0], x[y_kmeans == 1, 1],
        s=10, c='forestgreen', label='Cluster 2'
    )
    plt.scatter(
        x[y_kmeans == 2, 0], x[y_kmeans == 2, 1],
        s=10, c='blue', label='Cluster 3'
    )
    plt.scatter(
        x[y_kmeans == 3, 0], x[y_kmeans == 3, 1],
        s=10, c='orange', label='Cluster 4'
    )
    plt.scatter(
        x[y_kmeans == 4, 0], x[y_kmeans == 4, 1],
        s=10, c='purple', label='Cluster 5'
    )
    plt.scatter(
        kmeans.cluster_centers_[:, 0], kmeans.cluster_centers_[:, 1],
        s=100, c='yellow', label='Centroids'
    )
    plt.title(f'Clusters of durations ({hours} hours)')
    plt.xlabel('Latitude')
    plt.ylabel('Longitude')
    plt.legend()
    plt.show()


split_clusters(0.5)
