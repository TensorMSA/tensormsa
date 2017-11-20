<div align="center">
  <img src="http://hugrypiggykim.com/wp-content/uploads/2017/09/header.png"><br><br>
</div>

| **`Linux CPU`** | **`Linux GPU`** |
|-----------------|---------------------|
| [![Build Status](https://ci.tensorflow.org/buildStatus/icon?job=tensorflow-master-cpu)](https://ci.tensorflow.org/job/tensorflow-master-cpu) | [![Build Status](https://ci.tensorflow.org/buildStatus/icon?job=tensorflow-master-linux-gpu)](https://ci.tensorflow.org/job/tensorflow-master-linux-gpu) |

# [TensorMSA](http://hugrypiggykim.com) : Tensorflow Micro Service Architecture
## [OSS World Challenge 2017 - The Second Prize](https://www.slideshare.net/healess/11sw-tensormsa) 
**TensorMSA** is a framework for machine learning and deep learning. Main purpose of developing this framework is to provide automated pipe lines (data extraction > data preprocessing > train model > evaluate model > service model). Use of effective pipeline is really important when we proceed real project. There are so many hard tasks which has to be done to build data driven model. 

**Problems**
* Set up environment for deep learning is not a easy task (os, gpu, tensorflow, hadoop, etc..) 
* Build pipe line from data to train model 
* Difficulties of understading deep learning and implement those algorithms (even with tensorflow it's not that easy) 
* Manage model and data for service on legacy systems (usually works on Java)
* Build applications with using data driven models 
* Continuously update model by the environment and data changes 
* Hyper Parameter tunning for deep learning is also very exhausting job
* Managing and scheduling GPU server resource 

**Solutions**
* Easy to set up cluster with Docker images 
* Manage GPU resources with Celery and own job manager 
* REST APIs corresponding to Tensorflow
* JAVA API component interface with python REST APIS
* Easy to use UI for deep learning and machine learning 
* Pipe lines for various type of data and algorithms 
* Data collectors from various kind of source and types 
* Data preprocess for text, image and frame data sets 
* Support various deep learning and machine learning reusable componets 
* AutoML for hyperparameter tunning (genetic algorithm, random hp search, gpu cluster)

**Stack**
* Front End : React(ES6 + Webpack), Pure CSS + Scss, D3, jQuery Mobile(for Chatbot Client)
* Back End : Django(Python 3.5), Tensorflow(v1.2), Restful Service(Micro Service Architecture), PostgreSQL, Memcache, Celery, HDF5, Ngix, Gensim(W2V), Konlpy

## Overview - Framework introduction video 

Our framework provide easy to use UI/UX and AutoML based super easy process of build & service deep learning models

[![TensorMSA DeepLearning Layer](http://hugrypiggykim.com/wp-content/uploads/2017/09/user_main_page.png)](https://youtu.be/oShf9N7rdAE "TensorMSA ver0.1 - Click to Watch!")


## How to install
You can install and use our framework with docker. If you are not familiar with Docker( [Docker Install](https://docs.docker.com/engine/installation/) ) or Docker Compose ( [Docker Compose Install](https://docs.docker.com/compose/install/) ) check the link. If you have to install framework on multi server (cluster version) check this link [Detail Install Guide](https://github.com/TensorMSA/tensormsa_docker), If you have to install our project on your host server without using docker check this link [Host install guide](./Host_Install.md)

**1.download docker project**
```
    git clone --recursive https://github.com/TensorMSA/tensormsa_docker.git
```

**2.select GPU.CPU version to install**
```
    cd ./tensormsa_docker/docker_compose_gpu
```
```
    cd ./tensormsa_docker/docker_compose_cpu
```

**3.create docker volume**
```
    docker volume create --name=pg_data
    docker volume inspect pg_data
```

**4.run docker-compose**
```
    #first time you start docker-compose : create new containers
    docker-compose up -d
    #just to restart docker-compose 
    docker-compose restart
```

**5.migrate database**
```
    docker-compose run web python /home/dev/tensormsa/manage.py collectstatic
    docker-compose run web python /home/dev/tensormsa/manage.py makemigrations
    docker-compose run web python /home/dev/tensormsa/manage.py migrate
```

**6.choose number of celery/ap server**
```
    docker-compose scale celery=3
```

**Service Ports ( all service started automatically on docker start )**
* ***Easy UI/UX :*** [your ip address] : 8000 
* ***API Server :*** [your ip address] : 8000 
* ***Celery Monitor :*** [your ip address] : 5555 
* ***Jupter :*** [your ip address] : 8018 
* ***VNC :*** [your ip address] : 5901 


## For more information  

* [TensorMSA install guide with docker](https://github.com/TensorMSA/hoyai_docker)
* [TensorMSA API guide](http://13.124.133.117:8989/docs)
* [TensorMSA PyDoc guide](https://tensormsa.github.io/tensormsa/)
* [TensorMSA Project Design Document](https://docs.google.com/presentation/d/1SKYQ85l29PApQu8aUOFbkTMpxxefpJH3NhiR_GYr66I/pub?start=false&loop=false&delayms=3000)
* [TensorMSA User Guide](http://hugrypiggykim.com/category/tensormsa-guide/)
* [*etc* : Google syntaxNet Korean docker](https://github.com/TensorMSA/syntax_docker)
* [*etc* : Tensorflow education Jupyter notebooks](https://github.com/TensorMSA/hoyai_jupyter)
* [*etc* : Deep Learning Education Materials](http://hugrypiggykim.com/2017/08/24/%EB%94%A5%EB%9F%AC%EB%8B%9D-%EA%B5%90%EC%9C%A1-%EC%9E%90%EB%A3%8C-deep-learning-lecture/)


## License

* [Apache License 2.0](LICENSE)
