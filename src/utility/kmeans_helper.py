"""
This module contains a function to build a KMeans object
"""

from sklearn.cluster import KMeans

default_kmeans_config = {
    "n_clusters": 10,
    "init": "k-means++",
    "n_init": "warn",
    "max_iter": 300,
    "tol": 0.0001,
    "verbose": 0,
    "random_state": None,
    "copy_x": True,
    "algorithm": "lloyd",
    "max_cluster": 7,
}


def build_kmeans(kmeans_config: dict) -> KMeans:
    """
    This function builds a T_SNE object based on the tsne_config parameter
    """
    return KMeans(
        n_clusters=kmeans_config["n_clusters"],
        init=kmeans_config["init"],
        n_init=kmeans_config["n_init"],
        max_iter=kmeans_config["max_iter"],
        tol=kmeans_config["tol"],
        verbose=kmeans_config["verbose"],
        random_state=kmeans_config["random_state"],
        copy_x=kmeans_config["copy_x"],
        algorithm=kmeans_config["algorithm"],
    )
