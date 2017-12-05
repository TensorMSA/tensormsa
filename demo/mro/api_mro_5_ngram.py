import requests,os
url = "{0}:{1}".format(os.environ['HOSTNAME'] , "8989")
restURL = 'http://' + url + '/api/v1/type/service/state/predict/type/ngram/nnid/mro_compare/ver/active/'

jsonStr = {'list':[], 'standard': 0.95, 'filepath':'/hoya_src_root/mro_compare/testtsv.tsv'}

resp = requests.post(restURL
                     , json=jsonStr
                     )
# data = json.loads(resp.json())
print(resp.json())