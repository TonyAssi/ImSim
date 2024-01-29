# ImSim
Image Similarity Module built on top of 🤗 Datasets and Transformers

Given a query image, this module will search through a folder of images for the most similar images.

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
