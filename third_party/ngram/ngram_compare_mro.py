import ngram
import pandas as pd
import logging
from common.utils import *
from master.network.nn_common_manager import NNCommonManager
import os

class ThirdPartyNgram():
    def ngram_mro(self, nn_id, ver):
        graph = NNCommonManager().get_nn_node_name(nn_id)
        for net in graph:
            if net['fields']['graph_node'] == 'netconf_data':
                data_node = net['fields']['graph_node_name']
            elif net['fields']['graph_node'] == 'netconf_node':
                net_node = net['fields']['graph_node_name']

        file_path = get_source_path(nn_id, '', data_node)
        file_list = os.listdir(file_path)

        param = {}
        param['list'] = []
        param['standard'] = 0.95
        standard = NNCommonManager().get_nn_node_info(nn_id, str(ver), net_node)[0]['fields']['node_config_data']['standard']

        for file in file_list:
            df = pd.DataFrame.from_csv(file_path+'/'+file, sep='\t', encoding='ISO-8859-1')

            for dfdata in df.values:
                param['list'].append({'item_code': dfdata[0], 'item_leaf': dfdata[1], 'item_desc': dfdata[2]})

        item = []
        for val in param['list']:
            try:
                item_tuple = (val['item_code'].strip(), val['item_leaf'].strip(), val['item_desc'].strip())
                item.append(item_tuple)
            except:
                logging.info('Error Data' + val['item_code'])

        dataset = ngram.NGram(item, key=lambda x: x[2])
        dataset = sorted(dataset, key=lambda x: x[0])
        findset = ngram.NGram(item, key=lambda x: x[2])

        return_data = {}
        for data in dataset:
            findset.remove(data)
            result = findset.search(data[2], param['standard'])
            for r in range(len(result)):
                if return_data.get(data[0]) == None:
                    return_data[data[0]] = {}
                    return_data[data[0]]['desc'] = data[2]
                return_data[data[0]][result[r][0][0]] = {'item_desc': result[r][0][2], 'item_perc': result[r][1]}

        return return_data

    def predict(self, type, nn_id, ver):
        '''
        
        :param node_id: 
        :param param: param['list'] = 1(seq), q1(item_code), q1group(item_group), q1desc(item_description) tsv file
        :return: 
        '''
        if type == 'ngram_mro':
            return self.ngram_mro(nn_id, ver)

