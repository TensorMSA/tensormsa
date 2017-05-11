import os
import zipfile
import numpy as np
from PIL import Image, ImageFilter
from cluster.data.data_node import DataNode
from master.workflow.data.workflow_data_image import WorkFlowDataImage
from time import gmtime, strftime
from common import utils
from common.utils import *
import shutil

class DataNodeImage(DataNode):
    """
    """
    def run(self, conf_data):
        try:
            println("run DataNodeImage")
            nnid = conf_data['nn_id']
            node_id = conf_data['node_id']
            wf_ver = conf_data['wf_ver']
            net_conf_id = self._find_netconf_node_id(nnid, wf_ver = wf_ver)
            netconf = WorkFlowDataImage().get_step_source(net_conf_id)
            dataconf = WorkFlowDataImage().get_step_source(node_id)
            if dataconf == {}:
                println("/cluster/data/data_node_image DataNodeImage run dataconf("+node_id+") is not Exist")
                return
            else:
                println(node_id)

            directory = dataconf["source_path"]
            output_directory = dataconf["store_path"]
            output_filename = strftime("%Y-%m-%d-%H:%M:%S", gmtime())
            output_path = os.path.join(output_directory, output_filename)

            x_size = dataconf["preprocess"]["x_size"]
            y_size = dataconf["preprocess"]["y_size"]
            channel = dataconf["preprocess"]["channel"]

            labels = netconf['labels']
            try:
                filesize = dataconf["preprocess"]["filesize"]
            except:
                filesize = 1000000

            # unzip & remove zip
            ziplist = os.listdir(directory)
            for zipname in ziplist:
                if zipname.find(".zip") > -1:
                    print("Zip=" + zipname)
                    fantasy_zip = zipfile.ZipFile(directory + '/' + zipname)
                    fantasy_zip.extractall(directory)
                    fantasy_zip.close()
                    os.remove(directory + "/" + zipname)

            forderlist = os.listdir(directory)

            filecnt = 0
            image_arr = []
            lable_arr = []
            shape_arr = []
            name_arr = []
            processcnt = 1
            createcnt = 1

            for forder in forderlist:
                filelist = os.listdir(directory + '/' + forder)
                for filename in filelist:
                    try:
                        #PNG -> JPEG
                        img = Image.open(directory + '/' + forder + '/' + filename)
                        pngidx = str(type(img)).find("PngImageFile")
                        if pngidx > -1:
                            img = img.convert("RGBA")
                            bg = Image.new("RGBA", img.size, (255, 255, 255))
                            bg.paste(img, (0, 0), img)
                            filename = "Conv_" + str(filename)
                            bg.save(directory + '/' + forder + '/' + filename)

                        if channel == 1:
                            img = img.convert('L')

                        img = img.resize((x_size, y_size), Image.ANTIALIAS)
                        img = np.array(img)

                        img = img.reshape([-1, x_size, y_size, channel])
                        img = img.flatten()
                        image_arr.append(img)
                        shape_arr.append(img.shape)
                        lable_arr.append(forder.encode('utf8'))
                        name_arr.append(filename.encode('utf8'))
                        filecnt += 1

                        if filecnt >= filesize :
                            output_path_sub = output_path+"_"+str(createcnt)
                            hdf_create(self, output_path_sub, filecnt, channel, image_arr, shape_arr, lable_arr, name_arr)

                            filecnt = 0
                            image_arr = []
                            lable_arr = []
                            shape_arr = []
                            name_arr = []
                            createcnt += 1

                        print("Processcnt="+ str(processcnt) + " File=" + directory + " forder=" + forder + "  name=" + filename)
                    except:
                        print("Processcnt="+ str(processcnt) + " ErrorFile=" + directory + " forder=" + forder + "  name=" + filename)
                    processcnt += 1
                shutil.rmtree(directory + "/" + forder)
                try:
                    idx = labels.index(forder)
                except:
                    labels.append(forder)

            if filecnt > 0:
                output_path_sub = output_path + "_" + str(createcnt)
                hdf_create(self, output_path_sub, filecnt, channel, image_arr, shape_arr, lable_arr, name_arr)

            netconf["labels"] = labels
            WorkFlowDataImage().put_step_source_ori(net_conf_id, netconf)

            return None

        except Exception as e:
            println(e)
            raise Exception(e)



    def _init_node_parm(self, node_id):
        return None

    def _set_progress_state(self):
        return None

    def load_data(self, node_id="", parm = 'all'):
        dataconf = WorkFlowDataImage().get_step_source(node_id)
        output_directory = dataconf["store_path"]
        return  utils.get_filepaths(output_directory)
