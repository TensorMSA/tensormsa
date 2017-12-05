import ngram

# import requests,os
# url = "{0}:{1}".format(os.environ['HOSTNAME'] , "8989")
# restURL = 'http://' + url + '/api/v1/type/service/state/predict/type/ngram/nnid/mro_compare/ver/active/'
#
# jsonStr = {'list':[], 'standard': 0.95}
#
# jsonStr['list'].append({'item_code':'Q2172233', 'item_leaf': 'Power/Control Cable', 'item_desc': 'KIV,450/750V,70Cel,Color:SELECT(BK-WH-RD-YL-GN-BL),185MM2x1C,Conductor:ANNEALED COPPER WIRE,Sheath:NO SHEATH,Inst:PVC,KSC IEC 60227-3 '})
# jsonStr['list'].append({'item_code':'Q2174258', 'item_leaf': 'Power/Control Cable', 'item_desc': 'KIV,450/750V,70Cel,Color:SELECT(BK-WH-RD-YL-GN-BL),1.5MM2x1C,Conductor:ANNEALED COPPER WIRE,Sheath:NO SHEATH,Inst:PVC,KSC IEC 60227-3 '})
# jsonStr['list'].append({'item_code':'Q2174259', 'item_leaf': 'Power/Control Cable', 'item_desc': 'KIV,450/750V,70Cel,Color:SELECT(BK-WH-RD-YL-GN-BL),10MM2x1C,Conductor:ANNEALED COPPER WIRE,Sheath:NO SHEATH,Inst:PVC,KSC IEC 60227-3 '})
# jsonStr['list'].append({'item_code':'Q2174261', 'item_leaf': 'Power/Control Cable', 'item_desc': 'KIV,450/750V,70Cel,Color:SELECT(BK-WH-RD-YL-GN-BL),16MM2x1C,Conductor:ANNEALED COPPER WIRE,Sheath:NO SHEATH,Inst:PVC,KSC IEC 60227-3 '})
# jsonStr['list'].append({'item_code':'Q2174263', 'item_leaf': 'Power/Control Cable', 'item_desc': 'KIV,450/750V,70Cel,Color:SELECT(BK-WH-RD-YL-GN-BL),2.5MM2x1C,Conductor:ANNEALED COPPER WIRE,Sheath:NO SHEATH,Inst:PVC,KSC IEC 60227-3 '})
#
#
# resp = requests.post(restURL
#                      , json=jsonStr
#                      )

class ThirdPartyNgram():
    def predict(self, node_id, param):
        item = []

        sParam = sorted(param['list'], key=lambda x: x['item_code'])
        for val in sParam:
            item_tuple = (val['item_code'].strip(), val['item_leaf'].strip(), val['item_desc'].strip())
            item.append(item_tuple)

        dataset = ngram.NGram(item, key=lambda x: x[2])
        findset = ngram.NGram(item, key=lambda x: x[2])

        return_data = {}
        for data in dataset:
            findset.remove(data)
            result = findset.search(data[2])
            for r in range(len(result)):
                if result[r][1] > param['standard']:
                    if return_data.get(data[0]) == None:
                        return_data[data[0]] = {}
                    return_data[data[0]][result[r][0][0]] = {'item_desc': result[r][0][2], 'item_perc': result[r][1]}

        return return_data