import kagglehub

# Download latest version
path = kagglehub.dataset_download("sahideseker/tweet-sentiment-classification-dataset")

print("Path to dataset files:", path)
