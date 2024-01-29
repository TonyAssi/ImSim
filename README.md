# ImSim
Image Similarity Module built on top of 🤗 Datasets and Transformers

Given a query image, this module will search through a folder of images for the most similar images.

[Celebrity Look-a-Like Demo](https://huggingface.co/spaces/tonyassi/celebrity-look-a-like)

## Installation
```bash
pip install -r requirements.txt
```

## Usage

Import module
```python
from ImSim import get_similar_image
```

Searches for most similar image
- **query_image** path to query image
- **image_path** folder containing images
- **num** number of similar images that will be returned
```python
scores, retrieved_examples = get_similar_image(query_image='image.jpg',
                                               image_path='images',
                                               num=4)
```

Return values
- **scores** list of similarity scores
- **retrieved_examples** dictionary containing a list of most similar images and a list of most similar embeddings

Get a list of the most similar images. Each image is a PIL image
```python
similar_images = retrieved_examples['image']
```

Save the most similar image
```python
similar_images[0].save('similar.jpg')
```

## Theory
This module performs image similarity by comparing the embeddings of the candidate images to the embeddings of the query image.

The module goes through the candidate images and computes the embeddings for each one. Image embeddings are a numeric representation of an image. They represent high level visual concepts. Here is what they look like:
```python
[0.17519, -0.33182, -0.11692... 1.08443, -0.22943, 1.06595]
```
The embeddings will be computed and then saved into a .csv file inside the candidate image folder. The embeddings will only be computed the first time a query is made. The subsequent queries will load the embeddings from the .csv file so it'll be much faster. 

The computer vision model generating the embeddings is the famous [google/vit-base-patch16-224](https://huggingface.co/google/vit-base-patch16-224) model. It is a great general purpose encoder model. In theory you could use a vision model fine-tuned on your dataset, but I have found this model works as good if not better fine-tuned models.

After the candidate images, the query image embeddings are computed. We then use a handy [get_nearest_examples()](https://huggingface.co/docs/datasets/v2.16.1/en/package_reference/main_classes#datasets.Dataset.get_nearest_examples) function built into 🤗 Datasets which will look for most similar embeddings and return the correspondings images.

## Additional Resources
[Image Similarity with Hugging Face Datasets and Transformers](https://huggingface.co/blog/image-similarity) (blog)

[Building an image similarity system with 🤗 Datasets FAISS](https://colab.research.google.com/gist/sayakpaul/5b5b5a9deabd3c5d8cb5ef8c7b4bb536/image_similarity_faiss.ipynb) (notebook)
