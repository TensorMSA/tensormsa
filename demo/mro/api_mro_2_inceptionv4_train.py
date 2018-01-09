import requests
import json, os

url = "{0}:{1}".format('0.0.0.0' , "8989")
nn_id = "nn00000046"
wf_ver_id = str(1)
# ########################################################################################################################
resp = requests.post('http://127.0.0.1:8989/api/v1/type/runmanager/state/train/nnid/'+nn_id+'/ver/'+wf_ver_id+'/')
data = json.loads(resp.json())
print(data)
for row in data:
    rowdata = data[row]['result_info']
    true_name = rowdata['true_name']
    file_name= rowdata['file_name']
    pred_name= rowdata['pred_name']
    pred_value= rowdata['pred_value']

    print(true_name)
    print(file_name)
    print(pred_name)
    print(pred_value)
    for rowsub in range(len(true_name)):
        if true_name != pred_name[rowsub]:
            print(true_name[rowsub]+'   ('+file_name[rowsub]+')')
            print(pred_name[rowsub])
            print(pred_value[rowsub])
    print('end')


    # print(print(true_name[i])+'('+file_name[i]+')')
    # print(' - '+str(pred_name)+'('+str(pred_value)+')')
# #
# # def spaceprint(val, cnt):
# #     leng = len(str(val))
# #     cnt = cnt - leng
# #     restr = ""
# #     for i in range(cnt):
# #         restr += " "
# #     restr = restr+str(val)
# #     return restr
# #
# # if data == None:
# #     print(data)
# # else:
# #     try:
# #         if data["status"] == "404":
# #             print(data["result"])
# #     except:
# #         for train in data:
# #             if train != None and train != "" and train != {} and train != "status" and train != "result":
# #                 try:
# #                     for tr in train["TrainResult"]:
# #                         print(tr)
# #                 except:
# #                     maxcnt = 0
# #                     line = ""
# #                     for label in train["labels"]:
# #                         if maxcnt<len(label)+2:
# #                             maxcnt = len(label)+2
# #
# #                     for i in range(len(train["labels"])):
# #                         for j in range(maxcnt+4):
# #                             line += "="
# #
# #                     label_sub = []
# #                     for label in train["labels"]:
# #                         label = spaceprint(label,maxcnt)
# #                         label_sub.append(label)
# #
# #                     space = ""
# #                     for s in range(maxcnt):
# #                         space +=" "
# #
# #                     print(space, label_sub)
# #                     print(space, line)
# #                     for i in range(len(train["labels"])):
# #                         truecnt = 0
# #                         totcnt = 0
# #                         predict_sub = []
# #                         for j in range(len(train["predicts"][i])):
# #                             pred = spaceprint(train["predicts"][i][j],maxcnt)
# #
# #                             predict_sub.append(pred)
# #                             totcnt += int(pred)
# #                             # print(train["labels"].index(train["labels"][i]))
# #                             if train["labels"].index(train["labels"][i]) == j:
# #                                 truecnt = int(pred)
# #                         if totcnt == 0:
# #                             percent = 0
# #                         else:
# #                             percent = round(truecnt/totcnt*100,2)
# #                         print(spaceprint(train["labels"][i],maxcnt), predict_sub, str(percent)+"%")
#
#
# # println("E")
#
#
#


