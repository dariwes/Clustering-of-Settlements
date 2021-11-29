import pandas as pd
from clustering.kmeans_clustering import KMeansClustering
from clustering.hierarchy_clustering import HierarchyClustering
from config import db_settings
from database.db_manager import DatabaseManager


def main():
    durations = {
        0.5: dict(min_duration=0, max_duration=1800),
        1: dict(min_duration=1800, max_duration=3600),
        1.5: dict(min_duration=3600, max_duration=5400),
    }
    db_manager = DatabaseManager(**db_settings)
    for duration in durations.values():
        dataset = db_manager.get_certain_durations(**duration)
        dataset = pd.DataFrame(
            columns=['name', 'latitude', 'longitude'], data=dataset
        )
        # k-means clustering
        kmeans = KMeansClustering(dataset)
        kmeans.elbow_method()
        kmeans.show_clusters(cluster_amount=5)
        # hierarchy clustering
        hierarchy = HierarchyClustering(dataset)
        hierarchy.show_dendrogram()
        hierarchy.show_clusters(cluster_amount=5)


if __name__ == '__main__':
    main()
