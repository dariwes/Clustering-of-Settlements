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
        coordinates = self.dataset.iloc[:, [1, 2]].values
        populations = self.dataset.iloc[:, [3]].values
        table_labels, table_text = [], []
        kmeans = KMeans(
            n_clusters=cluster_amount, init='k-means++', random_state=int()
        )
        y_kmeans = kmeans.fit_predict(coordinates)
        for index in range(cluster_amount):
            boolean_list = y_kmeans == index
            label = f'Cluster {index + 1}'
            color = '#' + ''.join(
                [random.choice('0123456789ABCDEF') for _ in range(6)]
            )
            plt.scatter(
                coordinates[boolean_list, 0], coordinates[boolean_list, 1],
                s=10, c=color, label=label
            )
            table_labels.append(label)
            table_text.append(sum(populations[boolean_list, 0]))
        plt.scatter(
            kmeans.cluster_centers_[:, 0], kmeans.cluster_centers_[:, 1],
            s=100, c='yellow', label='Centroids'
        )
        plt.title(f'Clusters of settlements')
        plt.xlabel('Latitude')
        plt.ylabel('Longitude')
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
