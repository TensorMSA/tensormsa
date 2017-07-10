# Develop Guide for HOYA AI
### Git Guide 
 - Commit 주기는 기능이 완성된 상태에서 할 것(빌드나 동작의 완성 상태)
 - 한줄로 간결하게 요약 끝에는 마침표(.)을 찍지 않음
 - 제목 첫글자는 대문자로 쓸것
 - 무엇을 왜 했는지만 쓰면됨 (어떻게는 쓸필요없음 - 코드로 확인가능)
 
[Commit Message Example]
 - "[동사] + [목적어] + [보어]"
 - "[행위] + [대상] + [사유]"
 - "Modify CNN parameter for train"
 - "Add new class to make node"
 - "Fix the bug returns a type error"
 - "Merge workflow neuralnet_node to add function"

Frequently Use Command 
```sh
$ git status
$ git pull -r
 ```
Git flow is (Modified -> Staged(ADD) -> Commit)
 ```sh
$ git add "파일명"
$ git commit -m "내용"
$ git push
  ```
Set Global PATH
```sh
$ git config --global user.namenode "ID" 
$ git config --global user.email "ID@XXX.XXX"
```
Cancel PUSH
```sh
$ git push -f origin (last commit id):master
```
Local RESET
```sh
$ git fetch origin
$ git reset --hard origin/master
```
Fix conflict (After pull and pop)
```sh
$ git stash
$ git stash pop 
```


### Mark Down Guide
* [Mark Down Editor] (http://dillinger.io) - Online Guide

### Set Debug in Pycharm
Run -> Edit Configurations -> Python (+)
```sh
Name : django
Scripts : /home/dev/hoyai/manage.py
Scripts Parameter : runserver HOSTNAME:8000 (ex:HOSTNAME - Docker Container ID)
```

### HOYAI Drop Table and Create Table Again
delete /master/migrations/*.py (except __init__.py)
```sh
drop table master_NN_DEF_LIST_INFO ,
master_NN_VER_WFLIST_INFO, 
master_NN_VER_BATCHLIST_INFO, 
master_TRAIN_SUMMARY_RESULT_INFO, 
master_TRAIN_SUMMARY_ACCLOSS_INFO, 
master_BATCH_INFO_JOBCONFIG,
master_NN_WF_STATE_INFO, 
master_NN_WF_EASY_MODE_RULE, 
master_NN_WF_NODE_RELATION, 
master_WF_TASK_MENU_RULE, 
master_WF_TASK_SUBMENU_RULE, 
master_NN_WF_NODE_INFO, 
master_WF_TASK_REALATION_RULE
```
make migrations
```sh
./manage.py makemigrations
./manage.py migrate --fake master zero
./manage.py migrate
```
or 
delete from django_migrations where app = 'master'; 

./manage.py migrate

### Chatbot Drop Table and Create Table Again
delete /chatbot/migrations/*.py (except __init__.py)
```sh
drop table
Chatbot_CB_ENTITY_SYNONYM_LIST,
Chatbot_CB_ONTOLOGY_INFO,
Chatbot_CB_TAGGING_INFO,
Chatbot_CB_RESPONSE_LIST_INFO,
Chatbot_CB_SERVICE_LIST_INFO,
Chatbot_CB_MODEL_LIST_INFO,
Chatbot_CB_ENTITY_LIST_INFO,
Chatbot_CB_STORYBOARD_LIST_INFO,
Chatbot_CB_INTENT_LIST_INFO,
Chatbot_CB_ENTITY_RELATION_INFO,
Chatbot_CB_DEF_LIST_INFO
```
make migrations
```sh
./manage.py makemigrations chatbot
./manage.py migrate --fake chatbot zero
./manage.py migrate chatbot
```
### Sync Table
```sh
./manage.py migrate --fake (Model.py before add something)
./manage.py makemigrations chatbot
./manage.py migrate chatbot
```

### Run Jupyter for API Test
```sh
vi jupyter_notebook_config.py 
c.NotebookApp.ip = '*'
Find in vi - /ip n N
```

## Add Corpus (Mecab)
- mecab-0.996-ko-0.9.2.tar.gz (2017.06 recent) [링크](https://bitbucket.org/eunjeon/mecab-ko/downloads/)
- mecab-ko-dic-2.0.1-20150920.tar.gz (2017.06 recent) [링크](https://bitbucket.org/eunjeon/mecab-ko-dic/downloads/)
- tar xvf mecab-ko-dic-2.0.1-20150920.tar.gz
- go to dic directory and userdic
- add csv(1 line : 김수상,,,,NNP,*,F,김수상,*,*,*,*) 1)T/F : 받침유무
- [링크](http://andersonjo.github.io/nlp/2016/12/28/NLP/)
- run mecab-ko-dic-2.0.1-20150920/tools/add-userdic.sh

