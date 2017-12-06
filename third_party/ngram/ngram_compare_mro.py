import ngram
import pandas as pd
import logging

class ThirdPartyNgram():
    def predict(self, node_id, param):
        '''
        
        :param node_id: 
        :param param: param['list'] = 1(seq), q1(item_code), q1group(item_group), q1desc(item_description) tsv file
        :return: 
        '''
        file_path = param['filepath']
        df = pd.DataFrame.from_csv(file_path, sep='\t', encoding = 'ISO-8859-1')

        for dfdata in df.values:
            param['list'].append({'item_code': dfdata[0], 'item_leaf': dfdata[1], 'item_desc': dfdata[2]})

        item = []
        for val in param['list']:
            try:
                item_tuple = (val['item_code'].strip(), val['item_leaf'].strip(), val['item_desc'].strip())
                item.append(item_tuple)
            except:
                logging.info('Error Data'+val['item_code'])

        dataset = ngram.NGram(item, key=lambda x: x[2])
        dataset = sorted(dataset, key=lambda x: x[0])
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