import random
import matplotlib.pyplot as plt
import scipy.cluster.hierarchy as sch
from sklearn.cluster import AgglomerativeClustering


class HierarchyClustering:
    METHODS = (
        'average', 'centroid', 'complete',
        'median', 'single', 'weighted', 'ward',
    )

    def __init__(self, dataset):
        self.dataset = dataset

    def show_dendrogram(self):
        X = self.dataset.iloc[:, [1, 2]].values
        for method in HierarchyClustering.METHODS:
            _ = sch.dendrogram(sch.linkage(X, method=method))
            plt.title(f'Dendrogram ({method} method)')
            plt.xlabel('Settlements')
            plt.ylabel('Euclidean distances')
            plt.show()

    def show_clusters(
        self, cluster_amount, affinity='euclidean', method='ward'
    ):
        hc = AgglomerativeClustering(
            n_clusters=cluster_amount, affinity=affinity, linkage=method
        )
        X = self.dataset.iloc[:, [1, 2]].values
        y_hc = hc.fit_predict(X)
        for index in range(cluster_amount):
            color = '#' + ''.join(
                [random.choice('0123456789ABCDEF') for _ in range(6)]
            )
            plt.scatter(
                X[y_hc == index, 0],
                X[y_hc == index, 1],
                s=10, c=color, label=f'Cluster {index + 1}'
            )
        plt.title('Clusters of settlements')
        plt.xlabel('latitude')
        plt.ylabel('longitude')
        plt.legend()
        plt.show()
