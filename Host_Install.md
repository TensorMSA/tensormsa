## How to install
Download the latest version of TensorMSA from https://github.com/TensorMSA/tensormsa.git and unzip it.
Also, consider to use wget like followings.
```
    git clone https://github.com/TensorMSA/tensormsa.git
    unzip tensormsa-master.zip
```
Install PostgreSQL https://www.postgresql.org/download/
```
    ./manage.py makemigrations
    ./manage.py migrate --fake master zero (Optional)
    ./manage.py migrate
```
Install Python Packages (https://github.com/TensorMSA/tensormsa_docker/blob/master/requirements.txt)
```
    ./pip install -r requirements.txt
```
Build Javascript
```
    ./gui/static/npm install
    ./gui/static/npm run build
```
Run for Service
```
    ./start_hoyai.sh 1
```
Then you can see in your browser
```
    http://your_ip:8000
```
Call APIs (In IDE)
```
    ./demo/python api_basic_0_node_rule.py
    ./demo/python api_basic_0_automl_rule.py
    ...
```
Then you can see the main page.