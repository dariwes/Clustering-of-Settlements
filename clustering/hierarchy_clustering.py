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
        coordinates = self.dataset.iloc[:, [1, 2]].values
        populations = self.dataset.iloc[:, [3]].values
        table_labels, table_text = [], []
        y_hc = hc.fit_predict(coordinates)
        for index in range(cluster_amount):
            boolean_list = y_hc == index
            label = f'Cluster {index + 1}'
            color = '#' + ''.join(
                [random.choice('0123456789ABCDEF') for _ in range(6)]
            )
            plt.scatter(
                coordinates[boolean_list, 0],
                coordinates[boolean_list, 1],
                s=10, c=color, label=label
            )
            table_labels.append(label)
            table_text.append(sum(populations[boolean_list, 0]))
        plt.title('Clusters of settlements')
        plt.xlabel('latitude')
        plt.ylabel('longitude')
        plt.legend()
        plt.show()
        self.show_table(table_labels, [table_text])

    @staticmethod
    def show_table(labels, text, cellLoc='center', loc='center'):
        fig, ax = plt.subplots()
        fig.patch.set_visible(False)
        ax.axis('off')
        ax.axis('tight')
        ax.table(cellText=text, colLabels=labels, cellLoc=cellLoc, loc=loc)
        fig.tight_layout()
        plt.show()
