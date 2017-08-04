# TensorMSA : Tensorflow Micro Service Architecture

<b>1.TensorMSA </b> </br>
   - Tensor Micro Service Architecture is a project started to make TensorFlow more accessable from Java legacy systems
   with out modifying too much source codes.
   - We know there are AI platforms like Azure ML,Nvidia digits, AWS ML and etc, but our goal is little bit diffrent form theirs.
   - We saw many models that work perfect on lab environment but don't works properly on real field or accuracy start to drop by the time goes. That's why we started this project. 
   - Our project's goal is real time upgrading AI system from data collet,train,eval to prediction service, for that purpose we seperate action definition process and running processs. 
   - Our system gathers data from specified web page, RDB or Hadoop and train, eval automatically. If the train reault is better than before our system chages prediction service model to new one. 
   - More focus on enterprise support (continuous training, neural network management, history management, user managemetn and etc)
   - More focus on neural network (UI/UX based network configuration, work flow based management and etc)

<b>2. Function </b></br>
   - REST APIs corresponding to Tensorflow
   - JAVA API component interface with python REST APIS
   - Easy to use UI component provide NN configuration, train remotly, save & load NN models, handling train data sets
   - Data collectors from various kind of source and types 
   - Data preprocess for text, image and frame data sets 
   - Neural Network models and continuous training, evaluation service 
   - Android mobile SDK are also part of the plan (gather data and predict)

<b>3. Schedule </b></br>
   - start project : 2016.8
   - start dev : 2016.9
   - pilot version : 2016.12 *[(Link)](https://github.com/TensorMSA/TensorMSA)*
   - version 0.1 target date : 2017.5

<b>4. Stack </b></br>
   - FE(not supported this version) : React(ES6), SVG, D3, Pure CSS, Mobile(for Chatbot FW)
   - BE : Django(Python 3.5), Restful Service(Micro Service Architecture), Tensorflow(v1.2), PostgreSQL, Memcache, Celery, Spqrk QL, HDF5, Ngix, Gensim, Konlpy

<b>5. Methodology </b></br>
   - Agile (CI, TDD, Pair programming and Cloud)

# Overview - NeuralNetwork Management
Bellow is the pratice version of hoya which shows the concept of our project well. Though our current project aims much more complicated and powerful system, concepts make easy to use system for enterprise is quite similar.
[![HOYA ver0.1](https://github.com/TensorMSA/tensormsa_old/blob/master/video.PNG?raw=true)](https://youtu.be/sxx9l5gWbk0 "HOYA ver0.1 - Click to Watch!")

# Overview - ChatBot Frame Work
We are working on chatbot F/W based on stroy board and ontology. Benefit of this chatbot F/W is it uses neural networks created on Hoyai neural network management system. This means you can reuse various kind of AI models (※ CNN,ReNet, Wdnn, Seq2Seq, Word2Vec, Doc2Vec, Autoencode) on this chat bot F/W.   
[![HOYA ChatBot ver0.1](https://github.com/TensorMSA/tensormsa_old/blob/master/chat_bot_alpha.jpg?raw=true)](https://youtu.be/TZsLuGv6_bU "HOYA ChatBot ver0.1 - Click to Watch!")

# Set Development & Run Env with Docker  *[(Link)](https://github.com/TensorMSA/hoyai_docker)*
<b>1.Download Docker Images </b> </br>
   ```bash
     docker pull hoyai/hoyai_dev_docker
   ```
<b>2.Run Docker Container </b> </br>
   - Changes Resolution for vnc = VNC_RESOLUTION=<b>"1920x1080"</b> </br>
```bash
     docker run -itd --env="VNC_RESOLUTION=1920x1080" --env="DISPLAY" --env="QT_X11_NO_MITSHM=1" --volume="/tmp/.X11-unix:/tmp/.X11-unix:rw" --name hoyai_dev -p 5672:5672 -p 2266:2266 -p 5432:5432 -p 8000:8000 -p 6006:6006 -p 8888:8888 -p 5901:5901 hoyai/hoyai_dev_docker
```
# Google SyntaxNet Korean Docker *[(Link)](https://github.com/TensorMSA/syntax_docker)*
Google SyntaxNet provide 20 default languages but Korean is not included so you must do some tricky jobs to train Korean Corpus and build Rest API service environment with Google Syntaxnet so we build up some Docker script make those process
easy and simple

# Tensorflow Jupyter Sample Codes *[(Link)](https://github.com/TensorMSA/hoyai_jupyter)* 
Tensorflow version upgrades really fast and seems like usages changes fast too, our goal on the project is build various kind of samples codes works on latest Tensorflow version. And also with basic tensorflow with python example, we are going to provide HOYA api examples codes step by step 

# REST API *[(Link)](http://13.124.133.117:8989/docs)* 
All functions (100%) developed on this project linked to REST API, so that you can access it via console, jupyter or UI/UX 

# Contributions *[(Desigin Link)](https://docs.google.com/presentation/d/1SKYQ85l29PApQu8aUOFbkTMpxxefpJH3NhiR_GYr66I/pub?start=false&loop=false&delayms=3000)*
 <p align="center">
  <img src="https://github.com/TensorMSA/tensormsa_old/blob/master/HOYA%20F_W%20Design%20Document.jpg?raw=true" width="750"/>
 </p>
