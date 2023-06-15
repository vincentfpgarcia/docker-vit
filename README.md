# Docker-ViT

## Description

In this page, I will explain how to use the code of this repository to run a Vision Transformer (ViT) endpoint for image captioning. More precisely, I will show how to run the endpoint:

* Locally on your computer
* On a cloud GPU instance such as [Runpod](https://www.runpod.io/)

And finally, I will explain how to invoke these endpoints (i.e. send them an image and get an image description in return).

The motivation behind this project are explained in the Motivation section at the end of this page.

Please note that the code can easily be adapted to other models, both vision and non-vision ones.


## Run the ViT endpoint locally

Running the ViT endpoint locally relies on the use of the [Poetry](https://python-poetry.org/) package manager. Please make sure to first install Poetry and get familiar with it before moving to the next part. However, note that Poetry is not fundamental here and can easily be replaced by pip or conda.

### Install the dependencies

The code only requires a few very common libraries: Pillow, PyTorch, transformers, Flask and Gunicorn. If you only plan to use the endpoint without modifying it, you can install the main dependencies using:

```
$ poetry install --without dev
```

If, however, you plan to modify the code, I'd suggest to install the dev dependencies as well: Black, Flake8, isort, pre-commit. This will enforce better coding style:

```
$ poetry install
```

### Deploy the endpoint locally

To deploy the endpoint locally, open a terminal and execute the following command:

```
$ poetry run flask run --host 0.0.0.0 --port 8000
```

This will run the endpoint on a local development server on the port 8000. When the local server is up and running, you should see a message that looks like this:

```
WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
 * Running on all addresses (0.0.0.0)
 * Running on http://127.0.0.1:8000
 * Running on http://192.168.1.13:8000
```


## Run the ViT endpoint on a cloud instance

To explain how to run the ViT endpoint on a cloud GPU instance, I will use [Runpod](https://www.runpod.io) GPU cloud as an example, but other services should work more or less the same way.

This section relies both on [Docker](https://www.docker.com/) and [Runpod](https://www.runpod.io/). If you wish to follow the instruction described bellow, you need to create an account on both services and add some money on your Runpod account if you want to deploy the endpoint a cloud GPU instance.


### Build the image and push it to Docker Hub

To create an endpoint on Rundpod, you need to create a Docker image (containing the endpoint code) and host it on Docker Hub. You can probably host the Docker image somewhere else, but I haven't tried it to be honest.

In my case, I will host the Docker image on my Docker Hub repository named `vincentfpgarcia/docker-vit`. I will use that as an example.

Creating the Docker image and pushing it to Docker Hub can be achieved achieved using:

```
docker build -t vincentfpgarcia/docker-vit .
docker push vincentfpgarcia/docker-vit
```

Adapt the image tag / repository name to your needs. If you now visit your Docker Hub interface, you should see your Docker image available.

### Deploy the endpoint on Runpod

To deploy an endpoint on Runpod, you first need to create a new template that will use the Docker image you've just created. Go to [My Template](https://www.runpod.io/console/user/templates) and create a new template. Here are the information I used:

* Template Name: Docker Vit
* Container Image: `vincentfpgarcia/docker-vit`
* Docker command: `gunicorn -b 0.0.0.0:8000 app:app`
* Container Disk: 20GB
* Volume Disk: 0GB
* Expose HTTP PortsL `8000,`

All other values were left unchanged. Again, adapt these values to your needs.

You can now start a cloud GPU instance (a.k.a pod on Runpod) using the newly created template:

* Go to [Secure Cloud](https://www.runpod.io/console/gpu-secure-cloud) menu
* Select the GPU you are interested in (I've used a `RTX A4000`)
* Click `Deploy`
* Select your template
* Click `Continue` and click `Deploy`

If you now go to the menu [My Pods](https://www.runpod.io/console/pods), you should see your pod either starting or already running.


## Invoke the endpoint

To invoke the endpoint (meaning to use the service provided by the endpoint which is image captioning in this case) we need 2 things:

* One image
* The URL of the endpoint

For the image, I will use as an example this [image](https://unsplash.com/fr/photos/tIWBJN8t7zE) from [Karsten Winegeart](https://unsplash.com/fr/@karsten116) available on [Unsplash](https://unsplash.com).

![French bulldog with a yellow sweater on a blue background](french_bulldog.jpg)

If the endpoint is running locally, the endpoint's URL is `http://127.0.0.1:8000`. To invoke the endpoint, simply open a new terminal and execute the following command (adapt the image path):

```
$ curl -F "file=@/path/to/the/image.jpg" http://127.0.0.1:8000
```

If the endpoint is running on Runpod, the endpoint's URL is built using the pod's ID and the port used. Let us assume that the pod's ID is `abc123` and the port used is `8000`, the pod's URL will be `https://abc123-8000.proxy.runpod.net`. The pod's ID can be found on the [My Pods](https://www.runpod.io/console/pods) interface.

Invoking the Runpod endpoint is done exactly the same way the local endpoint is invoked, the difference being the endpoint's URL:

```
$ curl -F "file=@/path/to/the/image.jpg" https://abc123-8000.proxy.runpod.net
```

Using either the local or the cloud endpoint, the image description return by ViT for the dog image was "a small dog standing next to a bowl of food". Seems accurate enough!


## Motivation

AI projects are becoming bigger and complex. I've recently struggled to have an open-source project running on my laptop, not because of the model size, but because of the insane number of dependencies causing several issues. With these huge projects, I personally find the code harder to read and difficult to adapt to create an endpoint for a specific use.

I like simple things. I need that to feel in control.

I wanted to see if it was possible to create a very simple piece of code that will allow me to use any AI/ML model through an endpoint running on a cloud GPU instance. My constraints were:

* Code should to be as minimal as possible (less is better)
* Code should use as little dependencies as possible
* No UI or fancy stuff

The only fancy tools I allowed myself to use were Poetry (to manage the dependencies) and pre-commit + Black + Flake8 + isort (to make sure the code is neat).

I designed this code to be a starting point for other endpoints (hence the need for dev dependencies). It was never meant to be a final project. I hope this will help some developers to create new endpoints.

Regarding the choice of ViT image captioning. I was already working on this project and I needed a model to use as an example. Additionally, a friend of mine needed some code to give sight to his virtual avatar. So I used ViT, allowing me to kill two birds with one stone.
