"""
This module contains a function to build a T-SNE object
"""
from sklearn.manifold import TSNE

default_tsne_config = {
    "perplexity": 30,
    "n_components": 2,
    "early_exaggeration": 12,
    "learning_rate": "auto",
    "n_iter": 1000,
    "n_iter_without_progress": 300,
    "min_grad_norm": 1e-7,
    "metric": "euclidean",
    "metric_params": None,
    "init": "random",
    "verbose": 0,
    "random_state": None,
    "method": "barnes_hut",
    "angle": 0.5,
    "n_jobs": None,
}


def build_tsne(tsne_config: dict) -> TSNE:
    """
    This function builds a T_SNE object based on the tsne_config parameter
    """
    return TSNE(
        n_components=tsne_config["n_components"],
        perplexity=tsne_config["perplexity"],
        early_exaggeration=tsne_config["early_exaggeration"],
        learning_rate=tsne_config["learning_rate"],
        n_iter=tsne_config["n_iter"],
        n_iter_without_progress=tsne_config["n_iter_without_progress"],
        min_grad_norm=tsne_config["min_grad_norm"],
        metric=tsne_config["metric"],
        metric_params=tsne_config["metric_params"],
        init=tsne_config["init"],
        verbose=tsne_config["verbose"],
        random_state=tsne_config["random_state"],
        method=tsne_config["method"],
        angle=tsne_config["angle"],
        n_jobs=tsne_config["n_jobs"],
    )
