# Docker-ViT

## Description

The code presented here allows to:

* Run a local Vision Transformer (ViT) endpoint for image captioning
* Create a Docker image that can be used to run a ViT endpoint for image captioning on a cloud instance such as [Runpod](https://www.runpod.io/).

The motivation behind this project and the reason why I've used ViT are explained in the Motivation section, at the very end of this document. But do note that the code can easily be adapted to other models, both vision and non-vision ones.


## Run a local Vit endpoint

Running the ViT endpoint locally using the proposed code requires the use of the package manager [Poetry](https://python-poetry.org/). Please make sure to first install Poetry before moving to the next part. It is of course better if you are already familiar with it. Note that Poetry is not fundamental here and can easily be replaced by pip or conda.

### Install the dependencies

The presented code only requires a few very common libraries (Pillow, PyTorch, transformers, Flask and Gunicorn). If you only plan to use the endpoint without modifying it, you can install the dependencies using:

```
$ poetry install --without dev
```

If, however, you plan to modify the code, I'd suggest to install the main dependencies as well as the dev dependencies (Black, Flake8, isort, pre-commit) that will enforce better coding style:

```
$ poetry install
```

### Start the endpoint

Open a terminal and execute the following command to run the endpoint locally using Flask on the port 8000:

```
$ poetry run flask run --host 0.0.0.0 --port 8000
```

When the local server is up and running, you should see a message that looks like this:

```
WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
 * Running on all addresses (0.0.0.0)
 * Running on http://127.0.0.1:8000
 * Running on http://192.168.1.13:8000
```

### Use the endpoint

Now that the endpoind is running, you need to test it with an image. To call the endpoint, open a second terminal and execute the following command (adapt the path to your image):

```
$ curl -F "file=@/path/to/the/image.jpg" http://127.0.0.1:8000/
```

For my test, I've used the following [image](https://unsplash.com/fr/photos/tIWBJN8t7zE) from [Karsten Winegeart](https://unsplash.com/fr/@karsten116) available on Unsplash.

![French bulldog with a yellow sweater on a blue background](french_bulldog.jpg)

Using this image, the endpoint returned the following caption: `a small dog standing next to a bowl of food`. Seems good enough.


## Motivation

AI projects are becoming bigger and complex. I've recently struggled to have an open-source project running on my laptop, not because of the model size, but because of the insane number of dependencies causing several issues. With these huge projects, I personally find the code harder to read and difficult to adapt to create an endpoint for a specific use.

I like simple things. I need that to feel in control.

I wanted to see if it was possible to create a very simple piece of code that will allow me to use any AI/ML model through an endpoint running on a cloud GPU instance. My constraints were:

* Code should to be as minimal as possible (less is better)
* Code should use as little dependencies as possible
* No UI or fancy stuff

The only fancy tools I allowed myself to use were Poetry (to manage the dependencies) and pre-commit + Black + Flake8 + isort (to make sure the code is neat).

I designed this code to be a starting point for other endpoints (hence the need for dev dependencies). It was never meant to be a final project. I hope this will help some developers to create new endpoints.

Although the code was designed to work in a "minimalistic" way, it can of course be greatly improved in many ways. It was never designed to be a final project, but a foundation to create other endpoints (hence the need for dev dependencies).

Regarding the choice of ViT image captioning. I was already working on this project and I needed a model to use as an example. A friend of mine needed some code to give sight to his robot. So I used ViT, allowing me to kill two birds with one stone.
