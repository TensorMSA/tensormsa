import requests
import json, os

url = "{0}:{1}".format(os.environ['HOSTNAME'] , "8989")
# url = '127.0.0.1:8989'
nn_id = "nn00000019" # nn_id = "nn00000045"
wf_ver_id = str(4)
# ########################################################################################################################
resp = requests.post('http://' + url + '/api/v1/type/runmanager/state/train/nnid/'+nn_id+'/ver/'+wf_ver_id+'/')
data = json.loads(resp.json())
print(data)
for row in data:
    rowdata = data[row]['result_info']
    true_name = rowdata['true_name']
    file_name= rowdata['file_name']
    pred_name= rowdata['pred_name']
    pred_value= rowdata['pred_value']

    # print(true_name)
    # print(file_name)
    # print(pred_name)
    # print(pred_value)
    for rowsub in range(len(true_name)):
        if true_name[rowsub] != pred_name[rowsub][0]:
            print('---------------------------------------------------------------------------------------------------')
            try:
                index = pred_name[rowsub].index(true_name[rowsub])
                if float(pred_value[rowsub][index]) < 20:
                    print(true_name[rowsub] + '   (' + file_name[rowsub] + ')')
                    print(pred_name[rowsub])
                    print(pred_value[rowsub])
            except:
                print(true_name[rowsub] + '   (' + file_name[rowsub] + ')')
                print(pred_name[rowsub])
                print(pred_value[rowsub])


# true_name = ['airplain', 'bolt', 'airplain', 'airplain', 'ship']
# file_name = ['images (49).jpg', 'images (14).jpg', 'images (24).jpg', 'images (27).jpg', 'images (11).jpg']
# pred_name = [['airplain', 'car', 'bird'], ['airplain', 'car'], ['car', 'airplain'], ['car', 'airplain'], ['airplain', 'ship']]
# pred_value = [['98.9', '0.89', '0.10'], ['100.', '3.44'], ['99.9', '0.04'], ['99.9', '15.00'], ['99.9', '23.00']]

# for rowsub in range(len(true_name)):
#     if true_name[rowsub] != pred_name[rowsub][0]:
#         try:
#             index = pred_name[rowsub].index(true_name[rowsub])
#             if float(pred_value[rowsub][index]) < 100:
#                 print(true_name[rowsub] + '   (' + file_name[rowsub] + ')')
#                 print(pred_name[rowsub])
#                 print(pred_value[rowsub])
#         except:
#             print(true_name[rowsub] + '   (' + file_name[rowsub] + ')')
#             print(pred_name[rowsub])
#             print(pred_value[rowsub])

