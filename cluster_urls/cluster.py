import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
import nltk
from nltk.tokenize import word_tokenize

# Ensure you have the necessary NLTK tokenizer data
nltk.download('punkt')

# Read URLs from file
with open('gsa-urls.txt', 'r') as file:
    urls = file.read().splitlines()


# Function to extract tokens from URL
def tokenize_url(url):
    url = re.sub(r'http[s]?://', '', url)  # Remove HTTP/S protocol
    url = re.sub(r'www\.', '', url)  # Remove 'www.'
    tokens = word_tokenize(re.sub(r'\W+', ' ', url))  # Tokenize by splitting non-alphanumeric characters
    return ' '.join(tokens)


# Tokenize the URL paths
tokens = [tokenize_url(url) for url in urls]

# Use TfidfVectorizer with tokenization for feature extraction
vectorizer = TfidfVectorizer(ngram_range=(1, 3))  # Using n-grams for better granularity
X = vectorizer.fit_transform(tokens)

# Use K-Means to cluster the URLs
num_clusters = 8  # You can change the number of clusters
kmeans = KMeans(n_clusters=num_clusters)
kmeans.fit(X)

# Print out the clustered URLs
clusters = {}
for i in range(num_clusters):
    clusters[i] = [urls[idx] for idx, label in enumerate(kmeans.labels_) if label == i]

for cluster_id, cluster_urls in clusters.items():
    print(f"Cluster {cluster_id}: {len(cluster_urls)} URLs")
    for url in cluster_urls:
        print(f" - {url}")
    print()
