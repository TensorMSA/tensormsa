import ngram
import pandas as pd
import logging
from common.utils import *
from master.network.nn_common_manager import NNCommonManager
from third_party.ngram.db_conn import dbConnection
import os

# tsv file needs
# 1	Q4389348	Power/Control Cable	HFCO,6/10KV,240MM2x1C
# 2	Q4384414	Power/Control Cable	TFR-CV,0.6/1KV,90Cel,Color:BK,70MM2x1C,Conductor:ANNEALED COPPER WIRE,Sheath:TFR PVC,Inst:XLPE,LS/GAON/THIHAN/DAEWON/NEXANS,KSC IEC 60502-1
# 3	Q4384415	Power/Control Cable	TFR-CV,0.6/1KV,90Cel,Color:BK,4MM2x2C,Conductor:ANNEALED COPPER WIRE,Sheath:TFR PVC,Inst:XLPE,LS/GAON/THIHAN/DAEWON/NEXANS,KSC IEC 60502-1
# 4	Q4387746	Power/Control Cable	300V,70Cel,Color:RD,1.5MM2x8P,Conductor:TINNED COPPER,Sheath:PVC,Inst:PE,Shield:ALUMUNIUM TAPE INDIVIDUAL SHIELDED,TYPE: IPEV-IS
# 5	Q4389358	Power/Control Cable	TFR-8,400MM2x1C

class ThirdPartyNgram():
    def ngram_mro(self):
        graph = NNCommonManager().get_nn_node_name(self.nn_id)
        for net in graph:
            if net['fields']['graph_node'] == 'netconf_data':
                data_node = net['fields']['graph_node_name']
            elif net['fields']['graph_node'] == 'netconf_node':
                net_node = net['fields']['graph_node_name']

        netconf = NNCommonManager().get_nn_node_info(self.nn_id, str(self.ver), net_node)[0]['fields']['node_config_data']

        self.param['list'] = []
        self.param['standard'] = float(netconf['standard'])
        self.param['datatype'] = netconf['datatype']
        self.param['conninfo'] = netconf['conninfo']

        if self.param['datatype'] == 'file':
            self.get_file_data(data_node)
        elif self.param['datatype'] == 'db':
            self.get_db_data()

        item = []
        for val in self.param['list']:
            try:
                item_tuple = (val['item_code'].strip(), val['item_leaf'].strip(), val['item_desc'].strip())
                item.append(item_tuple)
            except:
                logging.info('Error Data' + val['item_code'])

        dataset = ngram.NGram(item, key=lambda x: x[2])
        dataset = sorted(dataset, key=lambda x: x[0])
        findset = ngram.NGram(item, key=lambda x: x[2])

        logging.info('================================================================================================')
        return_data = {}
        for data in dataset:
            findset.remove(data)
            result = findset.search(data[2], self.param['standard'])

            for r in range(len(result)):
                if return_data.get(data[0]) == None:
                    return_data[data[0]] = {}
                    return_data[data[0]]['desc'] = data[2]
                    # logging.info(str(data[0]) + ':' + str(data[2]))
                return_data[data[0]][result[r][0][0]] = {'item_desc': result[r][0][2], 'item_perc': result[r][1]}
                # logging.info(' - '+str(result[r][0][0])+'('+str(result[r][1])+')' + ':' + str(result[r][0][2]))
                logging.info(str(data[0]) + '-' + str(result[r][0][0]) + '(' + str(result[r][1]) + ')')

        return return_data

    def get_file_data(self, data_node):
        file_path = get_source_path(self.nn_id, '', data_node)
        file_list = os.listdir(file_path)

        for file in file_list:
            df = pd.DataFrame.from_csv(file_path + '/' + file, sep='\t', encoding='ISO-8859-1')

            for dfdata in df.values:
                self.param['list'].append({'item_code': dfdata[0], 'item_leaf': dfdata[1], 'item_desc': dfdata[2]})

    def get_db_data(self):
        self.param['list'] = dbConnection().conn(self.param)

    def predict(self, type, nn_id, ver):
        '''
        
        :param node_id: 
        :param param: param['list'] = 1(seq), q1(item_code), q1group(item_group), q1desc(item_description) tsv file
        :return: 
        '''
        if type == 'ngram_mro':
            self.nn_id = nn_id
            self.ver = ver
            self.param = {}
            return self.ngram_mro()

