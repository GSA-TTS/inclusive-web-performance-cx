"""Cluster URLs from an input file and output the clusters in JSON format to an output file."""

import re
import json
import click
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
import nltk
from nltk.tokenize import word_tokenize

# Ensure you have the necessary NLTK tokenizer data
nltk.download("punkt", quiet=True)


def tokenize_url(url):
    """extract tokens from URL"""
    url = re.sub(r"http[s]?://", "", url)  # Remove HTTP/S protocol
    url = re.sub(r"www\.", "", url)  # Remove 'www.'
    tokens = word_tokenize(
        re.sub(r"\W+", " ", url)
    )  # Tokenize by splitting non-alphanumeric characters
    return " ".join(tokens)


@click.command()
@click.option("--input", "input_file", required=True, help="Input file containing URLs")
@click.option(
    "--output",
    "output_file",
    required=True,
    help="Output file for JSON formatted array of clusters",
)
@click.option(
    "--clusters",
    "-c",
    default=10,
    type=int,
    help="Number of url clusters",
)
def main(input_file, output_file, clusters):
    """Cluster URLs from an input file and output the clusters in JSON format to an output file."""
    # Read URLs from file
    with open(input_file, "r", encoding="utf8") as file:
        urls = file.read().splitlines()

    # Tokenize the URL paths
    tokens = [tokenize_url(url) for url in urls]

    # Use TfidfVectorizer with tokenization for feature extraction
    vectorizer = TfidfVectorizer(
        ngram_range=(1, 3)
    )  # Using n-grams for better granularity
    vector_fit = vectorizer.fit_transform(tokens)

    # Use K-Means to cluster the URLs
    num_clusters = (
        clusters  # You can change the number of clusters, or make it a parameter
    )
    kmeans = KMeans(n_clusters=num_clusters)
    kmeans.fit(vector_fit)

    # Collect the clustered URLs
    item_clusters = []
    for i in range(num_clusters):
        cluster_urls = [urls[idx] for idx, label in enumerate(kmeans.labels_) if label == i]
        item_clusters.append({
            "items": cluster_urls,
            "total_items": len(cluster_urls)
        })

    results = {
        "clusters": item_clusters
    }

    # Write JSON output
    with open(output_file, "w", encoding="utf8") as outfile:
        json.dump(results, outfile, indent=4)

    print(f"Clustering complete. Output written to: {output_file}")


if __name__ == "__main__":
    main()  # pylint: disable=no-value-for-parameter
