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
Run for Service
```
    ./start_hoyai.sh 1
```
Call APIs
```
    ./demo/python api_basic_0_node_rule.py
    ./demo/python api_basic_0_automl_rule.py
    ...
```
