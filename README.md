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
- **input_dataset** the source dataset
- **out_dataset** the name of dataset that will be created and uploaded to
- **token** HuggingFace write access token can be created [here](https://huggingface.co/settings/tokens)
```python
scores, retrieved_examples = get_similar_image(query_image='image.jpg',
                                               image_path='images',
                                               num=4)
```
