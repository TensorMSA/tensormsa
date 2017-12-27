from master.runmanager.run_manager import RunManager
import celery
import os, requests, json, time
from django.conf import settings
from common.utils import *
import socket

class RunManagerMoniter(RunManager):
    """

    """

    def get_view_obj(self):
        """
        get view data for net config
        :return:
        """
        return None

    def set_view_obj(self, obj):
        """
        set net config data edited on view
        :param obj:
        :return:
        """
        return None

    def change_float_str_time(self, ftime):
        ctime = time.ctime(ftime)
        dtime = time.strptime(ctime, '%a %b %d %H:%M:%S %Y')
        year = str(dtime.tm_year)
        mon = str(dtime.tm_mon)
        day = str(dtime.tm_mday)
        hour = str(dtime.tm_hour)
        min = str(dtime.tm_min)
        sec = str(dtime.tm_sec)

        if len(mon) == 1:
            mon = '0'+mon
        if len(day) == 1:
            day = '0' + day
        if len(hour) == 1:
            hour = '0'+hour
        if len(min) == 1:
            min = '0'+min
        if len(sec) == 1:
            sec = '0'+sec

        ddtime = year + '-' + mon + '-' + day + ' ' + hour + ':' + min + ':' + sec
        return ddtime

    def get_view_obj_list(self, type, id):
        """
        get view data for net config
        :return:
        """
        # cel = celery.task.control.inspect()
        # celActive = cel.active()
        return_data = []
        if settings.CELERY_FLAG == True:
            # furl = "{0}:{1}".format(os.environ['HOSTNAME'], settings.FLOWER_PORT)
            resp = requests.get('http://' + settings.FLOWER_PORT + '/api/tasks')

            resp_data = resp.text
            resp_data = json.loads(resp_data)
            for re in resp_data:
                re_data = {}
                nn_id = ''
                nn_wf_ver_id = ''
                if resp_data[re]['args'] != None:
                    replace_data = resp_data[re]['args'].replace("'", '').replace("(", '').replace(")", '')
                    replace_data = replace_data.split(',')
                    nn_id = replace_data[0]
                    nn_wf_ver_id = replace_data[1]

                if type == 'run_check' :
                    if nn_id != id:
                        continue
                    substate = resp_data[re]['state']
                    if substate == 'PENDING' or substate == 'SUCCESS' or substate == 'FAILURE' or substate == 'REVOKED' or substate == 'RETRY':
                        continue

                if id != 'all' and id != nn_id:
                    continue
                re_data['nn_id'] = nn_id
                re_data['nn_wf_ver_id'] = nn_wf_ver_id
                re_data['uuid'] = resp_data[re]['uuid']
                re_data['clock'] = resp_data[re]['clock']
                re_data['name'] = resp_data[re]['name']
                re_data['failed'] = resp_data[re]['failed']
                re_data['result'] = resp_data[re]['result']
                re_data['state'] = resp_data[re]['state']

                re_data['received'] = self.change_float_str_time(resp_data[re]['received'])
                re_data['started'] = self.change_float_str_time(resp_data[re]['started'])
                re_data['succeeded'] = self.change_float_str_time(resp_data[re]['succeeded'])
                re_data['rejected'] = self.change_float_str_time(resp_data[re]['rejected'])
                re_data['timestamp'] = self.change_float_str_time(resp_data[re]['timestamp'])

                re_data['receivedtime'] = resp_data[re]['received']
                re_data['startedtime'] = resp_data[re]['started']
                re_data['succeededtime'] = resp_data[re]['succeeded']
                re_data['rejectedtime'] = resp_data[re]['rejected']
                re_data['timestamptime'] = resp_data[re]['timestamp']

                return_data.append(re_data)
                # url = 'http://' + furl + '/api/task/info/'+return_data[re]['uuid']
                # respd = requests.get(url)
                # return_data[re]['worker'] = respd
                # print(respd)

        return return_data

    def get_view_obj_log(self, id, line):
        """
        get view data for net config
        :return:
        """
        # cel = celery.task.control.inspect()
        # celActive = cel.active()
        line = int(line)
        return_data = []
        re_data = {}
        # file = '/hoya_log_root/'+id
        file = get_log_path()+id
        f = open(file)

        f.seek(line)
        latest_data = f.read()
        line = f.tell()
        if latest_data:
            re_data['log'] = latest_data
            re_data['line'] = line
            return_data.append(re_data)

        return return_data