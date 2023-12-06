"""
This module contains a clustering class for segmenting data
"""
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from pandas import DataFrame
import plotly.express as px
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from sklearn.preprocessing import MinMaxScaler, StandardScaler
from src.utility.tsne_helper import default_tsne_config, build_tsne
from src.utility.kmeans_helper import default_kmeans_config, build_kmeans
from src.utility.logger import Logger
from src.utility.environment import Environment

CLUSTER_COLUMN_NAME = "CLUSTER_ID"


class DataSegmenter:
    """
    This class contains functions to find clusters within a data set
    """

    def __init__(
        self,
        env: Environment,
        pipeline_config: dict,
        segmentation_dataframe: DataFrame,
        demographic_dataframe: DataFrame,
        categorical_columns: [str] = None,
    ) -> None:
        assert env is not None
        self.env = env
        self.pipeline_config = pipeline_config
        self.segmentation_dataframe = segmentation_dataframe
        self.demographic_dataframe = demographic_dataframe
        self.final_dataframe = None
        self.cluster_labels = None
        self.categorical_columns = categorical_columns
        self.logger = Logger(env=env)
        self.segmenter_id = datetime.now().strftime("%Y%m%d%H%M%S")

    def elbow_method(
        self, kmeans_config: dict = default_kmeans_config, scaling_method: str = None
    ) -> None:
        """
        This function uses the elbow method to generate a graph to help find the optimal number of clusters
        and logs it to Weights & Biases
        """

        plt.clf()
        kmeans_config["n_init"] = 10
        kmeans_config["random_state"] = 42
        df = self.scale_data(scaling_method=scaling_method)

        # Calculate the sum of squared distances for a range of cluster numbers
        sse = []
        max_clusters = 7
        for n_clusters in range(1, max_clusters + 1):
            kmeans_config["n_clusters"] = n_clusters
            kmeans = build_kmeans(kmeans_config)
            kmeans.fit(df)
            sse.append(kmeans.inertia_)

        # Plot the Elbow Method graph
        fig = plt.figure()
        plt.plot(range(1, max_clusters + 1), sse, marker="o")
        plt.xlabel("Number of Clusters")
        plt.ylabel("Sum of Squared Distances (SSE)")
        plt.title("Elbow Method for Optimal Number of Clusters")

        run_config = {
            "pipeline_config": self.pipeline_config,
            "elbow_config": kmeans_config,
        }

        self.logger.save_cluster_analysis(
            run_config=run_config,
            method_name="Elbow Method",
            figure=fig,
            job_type=self.segmenter_id,
        )

    def silhouette_method(
        self, kmeans_config: dict = default_kmeans_config, scaling_method: str = None
    ) -> None:
        """
        This function uses the silhouette method to generate a graph to help find the optimal number of clusters
        and logs it to Weights & Biases
        """

        plt.clf()
        kmeans_config["n_init"] = 10
        kmeans_config["random_state"] = 42
        silhouette_scores = []
        df = self.scale_data(scaling_method=scaling_method)

        # Try different numbers of clusters (e.g., from 2 to 10)
        for n_clusters in range(2, 7):
            kmeans_config["n_clusters"] = n_clusters
            kmeans = build_kmeans(kmeans_config)
            kmeans.fit(df)
            labels = kmeans.labels_
            silhouette_avg = silhouette_score(df, labels)
            silhouette_scores.append(silhouette_avg)

        # Plot the silhouette scores
        fig = plt.figure(figsize=(10, 6))
        plt.plot(range(2, 7), silhouette_scores, marker="o")
        plt.xlabel("Number of Clusters")
        plt.ylabel("Silhouette Score")
        plt.title("Silhouette Score for Different Numbers of Clusters")
        plt.grid(True)

        run_config = {
            "pipeline_config": self.pipeline_config,
            "silhouette_config": kmeans_config,
        }

        self.logger.save_cluster_analysis(
            run_config=run_config,
            method_name="Silhouette Method",
            figure=fig,
            job_type=self.segmenter_id,
        )

    def segment_data(
        self,
        scaling_method: str = None,
        n_clusters: int = 2,
        tsne_config: dict = default_tsne_config,
    ) -> Figure:
        """
        Create a graph for clusters from all features using T-SNE and logs it to Weights & Biases

        Args:
            tsne_config (dict): Configuration for T-SNE
        """

        df = self.scale_data(scaling_method=scaling_method)

        kmeans = KMeans(n_init=10, n_clusters=n_clusters, random_state=42)
        self.cluster_labels = kmeans.fit_predict(df)
        self.demographic_dataframe[CLUSTER_COLUMN_NAME] = self.cluster_labels

        tsne_config["n_components"] = 3
        tsne = build_tsne(tsne_config=tsne_config)
        reduced_data = tsne.fit_transform(df)

        fig = px.scatter_3d(
            x=reduced_data[:, 0],
            y=reduced_data[:, 1],
            z=reduced_data[:, 2],
            color=self.cluster_labels,
            title="T-SNE Reduced Data Clusters",
            labels={"x": "Dimension 1", "y": "Dimension 2", "z": "Dimension 3"},
            color_continuous_scale=px.colors.sequential.Viridis,
        )

        fig.update_layout(legend_title_text="Legend")

        return fig

    def segment_sequence(
        self,
        scaling_method: str = None,
        n_clusters: int = 2,
        tsne_config: dict = default_tsne_config,
    ) -> "DataSegmenter":
        """
        This function executes the segmentation and extraction of thresholds
        """

        fig = self.segment_data(
            scaling_method=scaling_method,
            n_clusters=n_clusters,
            tsne_config=tsne_config,
        )

        # Get column order for concatenation (behavioral + )
        column_order = list(self.segmentation_dataframe.columns) + list(
            self.demographic_dataframe.columns.difference(
                self.segmentation_dataframe.columns
            )
        )

        # Concatenate the dataframes and reindex the columns
        self.final_dataframe = (
            pd.concat(
                [self.segmentation_dataframe, self.demographic_dataframe], axis=1
            )[column_order]
            .apply(pd.to_numeric, errors="coerce")
            .astype("float64")
            .round(2)
        )

        thresholds = self.get_thresholds()

        run_config = {
            "pipeline_config": self.pipeline_config,
            "tsne_vector_reduction_config": tsne_config,
            "thresholds": thresholds,
        }

        self.logger.save_segmentation_run(
            run_config=run_config,
            segmentation_name="T-SNE Reduced Clusters 3D",
            figure=fig,
            job_type=self.segmenter_id,
        )

        return self

    def get_thresholds(self) -> dict:
        """
        This function returns the thresholds for each cluster
        """
        thresholds = {}
        cluster_labels = self.final_dataframe[CLUSTER_COLUMN_NAME].unique()

        for label in cluster_labels:
            selected_rows = self.final_dataframe[
                self.final_dataframe[CLUSTER_COLUMN_NAME] == label
            ]
            proportion = self.get_cluster_distribution(label=label)
            thresholds[str(label)] = {"proportion": proportion}
            for column in selected_rows.columns:
                thresholds[str(label)][column] = {
                    "minimum": selected_rows[column].min(),
                    "maximum": selected_rows[column].max(),
                    "mean": round(selected_rows[column].mean(), 2),
                }
                if column in self.categorical_columns:
                    thresholds[str(label)][column] = {
                        "most_frequent_value": selected_rows[column]
                        .value_counts()
                        .head(1),
                    }
        return thresholds

    def get_cluster_distribution(self, label: float) -> float:
        """
        This function returns the proportion of a cluster in the entire dataset
        """
        filtered_df = self.final_dataframe[self.final_dataframe["CLUSTER_ID"] == label]
        percentage_size = (len(filtered_df) / len(self.final_dataframe)) * 100
        return round(percentage_size, 2)

    def scale_data(self, scaling_method: str = None) -> DataFrame:
        """
        This function returns a dataframe with a scaled version of the original data
        """

        df = self.segmentation_dataframe.copy()

        if scaling_method is not None:
            if scaling_method == "standard":
                scaler = StandardScaler()
            elif scaling_method == "minmax":
                scaler = MinMaxScaler()
            scaled_data = scaler.fit_transform(self.segmentation_dataframe.copy())
            # Convert the scaled data back to a DataFrame
            df = pd.DataFrame(scaled_data, columns=self.segmentation_dataframe.columns)

        return df
