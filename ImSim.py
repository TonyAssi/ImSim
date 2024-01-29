import numpy as np
from PIL import Image
from transformers import AutoFeatureExtractor, AutoModel
from datasets import load_dataset
import glob
import pandas as pd
import os
from ast import literal_eval


# Load computer vision model
model_ckpt = "google/vit-base-patch16-224"
extractor = AutoFeatureExtractor.from_pretrained(model_ckpt)
model = AutoModel.from_pretrained(model_ckpt)
hidden_dim = model.config.hidden_size

# Computes embeddings of an image
def extract_embeddings(image):
    image_pp = extractor(image, return_tensors="pt")
    features = model(**image_pp).last_hidden_state[:, 0].detach().numpy()
    return features.squeeze()

# Finds similar embedding
def get_neighbors(query_image, dataset_with_embeddings, top_k=5):
    qi_embedding = model(**extractor(query_image, return_tensors="pt"))
    qi_embedding = qi_embedding.last_hidden_state[:, 0].detach().numpy().squeeze()
    scores, retrieved_examples = dataset_with_embeddings.get_nearest_examples('embeddings', qi_embedding, k=top_k)
    return scores, retrieved_examples


def get_similar_image(query_image, image_path, num):

    # Load dataset
    dataset = load_dataset(image_path, split="train")

    # If .csv embeddings file doesn't exist then compute embeddings
    if(os.path.isfile(image_path + '/embeddings.csv') == False):
        print('Computing embeddings...')
        # Compute embeddings and add column to dataset
        dataset_with_embeddings = dataset.map(lambda example: {'embeddings': extract_embeddings(example["image"].convert('RGB'))})

        # Create a dataset dict 
        ds_dict = {'image': dataset_with_embeddings['image'], 'embeddings': dataset_with_embeddings['embeddings']}

        # Pandas dataframe
        df = pd.DataFrame(ds_dict)
        
        # Save the dataframe to .csv
        df.to_csv(image_path + '/embeddings.csv')
    else:
        print('Embedding CSV already exists')
        # Load embeddings from .csv file
        df = pd.read_csv(image_path + '/embeddings.csv', sep=',', converters=dict(embeddings=literal_eval))

        # Add embeddings column to dataset
        dataset_with_embeddings = dataset.add_column("embeddings", df['embeddings'].tolist())
    
    # add_faiss_index() to compute similar embeddings
    dataset_with_embeddings.add_faiss_index(column='embeddings')

    # Load query image
    query = Image.open(query_image).convert('RGB')

    # Find similar images
    scores, retrieved_examples = get_neighbors(query, dataset_with_embeddings, top_k=num)
    
    return scores, retrieved_examples



