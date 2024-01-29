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

Generates image embeddings and upload to 🤗
- **query_image** path to query image
- **image_path** folder containing images
- **num** number of similar images that will be returned
```python
scores, retrieved_examples = get_similar_image(query_image='image.jpg',
                                               image_path='images',
                                               num=4)
```
- **scores** list of similarity scores
- **retrieved_examples** dictionary containing a list of most similar images and a list of most similar embeddings
- 
