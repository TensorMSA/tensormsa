import requests
import json, os

url = "{0}:{1}".format(os.environ['HOSTNAME'] , "8000")



# resp = requests.put('http://' + url + '/api/v1/type/wf/state/dataconf/detail/frame/nnid/nn00001/ver/1/node/dataconf_node/',
#                      json={"label": "income_bracket"
#                          , "Transformations":
#                                {"age_buckets": {"boundaries": [18, 25, 30, 35, 40, 45, 50, 55, 60, 65], "column_name": "age"}}
#                          , "cross_cell": {"col3": ["age_buckets", "education", "occupation"]
#                              ,"col2": ["native_country", "occupation"]
#                                ,"col1": ["occupation", "education"]}
#                          , "cell_feature":
#                                {"hours_per_week": {"column_type": "CONTINUOUS"}
#                                    , "capital_loss": {"column_type": "CONTINUOUS"}
#                                    , "age": {"column_type": "CONTINUOUS"}
#                                    , "capital_gain": {"column_type": "CONTINUOUS"}
#                                    , "education_num": {"column_type": "CONTINUOUS"}
#                                    , "education": {"column_type": "CATEGORICAL"}
#                                    , "occupation": {"column_type": "CATEGORICAL"}
#                                    , "workclass": {"column_type": "CATEGORICAL"}
#                                    , "sex":  {"column_type": "CATEGORICAL"}
#                                    , "native_country": {"column_type": "CATEGORICAL"}
#                                    , "relationship": {"column_type": "CATEGORICAL"}
#                                    , "marital_status":  {"column_type": "CATEGORICAL"}
#                                    , "race":  {"column_type": "CATEGORICAL"}
#                                 }
#                            , "extend_cell_feature" :
#                                {
#                                     "sex": {"keys": ["female", "male"], "column_type": "CATEGORICAL_KEY"}
#                                    , "race": {"column_type": "NONE"}
#                                    , "marital_status": {"column_type": "NONE"}
#                                }
#                            ,"label_values" : []
#                            ,"label_type" : "CATEGORICAL"

#                            })
# data = json.loads(resp.json())

#
# resp = requests.put('http://' + url + '/api/v1/type/wf/state/dataconf/detail/frame/nnid/nn00001/ver/1/node/dataconf_node/',
#                      json={"label": "AT"
#                             , "Transformations":{}
#                             , "cross_cell":{}
#                             , "cell_feature":{}
#                             , "extend_cell_feature" :{}
#                             , "label_values" : []
#                             , "label_type" : "CONTINUOUS"
#                            })
# data = json.loads(resp.json())
#
# print("evaluation result : {0}".format(data))
#
#

resp = requests.put('http://' + url + '/api/v1/type/wf/state/dataconf/detail/frame/nnid/nn00031/ver/1/node/dataconf_node/',
                     json={"label": "SUCCESSFUL_BID_PRICE"
                            , "Transformations":{}
                            , "cross_cell":{}
                            , "cell_feature":{}
                            , "extend_cell_feature" :{}
                            , "label_values" : []
                            , "label_type" : "CONTINUOUS"
                           })
data = json.loads(resp.json())


#
# resp = requests.put('http://' + url + '/api/v1/type/wf/state/dataconf/detail/frame/nnid/nn00001/ver/1/node/dataconf_node/',
#                      json={"label": "SLAB_SUR_MAIN_DEF_CD2"
#                             , "Transformations":{}
#                             , "cross_cell":{}
#                             , "cell_feature":{}
#                             , "extend_cell_feature" :{}
#                             , "label_values" : []
#                             , "label_type" : "CATEGORICAL"
#                            })
# data = json.loads(resp.json())


#resp = requests.get('http://' + url + '/api/v1/type/wf/state/dataconf/detail/frame/nnid/nn00031/ver/1/node/dataconf_node/')
data = json.loads(resp.json())


#nn00031_1_dataconf_node


print("evaluation result : {0}".format(data))