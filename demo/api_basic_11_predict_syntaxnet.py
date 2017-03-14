import requests
import json, os
url = "{0}:{1}".format("syntaxnet-rest-api" , "9000")

# [Required]
# make new docker for rest-service and add model "syntaxnet"
# add option to docker run "--link syntaxnet:syntaxnet-rest-api"
# Reference : https://github.com/ljm625/syntaxnet-rest-api

# Call Syntaxnet
resp = requests.post('http://' + url + '/api/v1/query',
                         json={
                                 "strings": ["Google is awesome!"]
                         }
                     )
"""
    return value is (On AWS console tested not use docker)
    [{'pos_tag': 'JJ', 'dep': 'ROOT', 'contains':
    [{'pos_tag': 'NNP', 'dep': 'nsubj', 'name': 'Google'},
    {'pos_tag': 'VBZ', 'dep': 'cop', 'name': 'is'},
    {'pos_tag': '.', 'dep': 'punct', 'name': '!'}],
    'name': 'awesome'}]
"""


print(resp.json())




