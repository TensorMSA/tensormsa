import requests
import json, os
url = "{0}:{1}".format(os.environ['HOSTNAME'] , "8000")

resp = requests.post('http://' + url + '/api/v1/type/service/botbuilder/story/',
                     json={
                        # #story
                        'story_id': "1",
                        'story_type': "type1",
                        'story_desc': "find_tel",
                        'intent_id': "1",
                     })
data = json.loads(resp.json())
print("evaluation result : {0}".format(data))
