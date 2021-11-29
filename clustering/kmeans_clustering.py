import random
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans


class KMeansClustering:
    def __init__(self, dataset):
        self.dataset = dataset

    def elbow_method(self):
        X = self.dataset.iloc[:, [1, 2]].values
        wcss = []
        for count in range(1, 11):
            kmeans = KMeans(
                n_clusters=count, init='k-means++', random_state=int()
            )
            kmeans.fit(X)
            wcss.append(kmeans.inertia_)
        plt.plot(range(1, 11), wcss)
        plt.title(f'The Elbow Method')
        plt.xlabel('Number of clusters')
        plt.ylabel('WCSS')
        plt.show()

    def show_clusters(self, cluster_amount):
        X = self.dataset.iloc[:, [1, 2]].values
        kmeans = KMeans(
            n_clusters=cluster_amount, init='k-means++', random_state=int()
        )
        y_kmeans = kmeans.fit_predict(X)
        for index in range(cluster_amount):
            color = '#' + ''.join(
                [random.choice('0123456789ABCDEF') for _ in range(6)]
            )
            plt.scatter(
                X[y_kmeans == index, 0], X[y_kmeans == index, 1],
                s=10, c=color, label=f'Cluster {index + 1}'
            )
        plt.scatter(
            kmeans.cluster_centers_[:, 0], kmeans.cluster_centers_[:, 1],
            s=100, c='yellow', label='Centroids'
        )
        plt.title(f'Clusters of settlements')
        plt.xlabel('Latitude')
        plt.ylabel('Longitude')
        plt.legend()
        plt.show()
