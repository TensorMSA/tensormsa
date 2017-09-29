export default class ReportRepository {
    constructor(api) {
        this.api = api;
    }

    log(title, data){
        console.log(title+"....................................");
        console.log(data)
    }

    //Network Info
    postCommonNNInfo(params, jsonData) {
        return this.api.post('/api/v1/type/common/target/nninfo/nnid/'+params+'/', jsonData).then((data) => {
            data = JSON.parse(data);
            this.log("postCommonNNInfo", data)
            return data;
        });
    }

    putCommonNNInfo(params, jsonData) {
        return this.api.put('/api/v1/type/common/target/nninfo/nnid/'+params+'/', jsonData).then((data) => {
            this.log("putCommonNNInfo", data)
            return data;
        });
    }

    getCommonNNInfo(params) {
        return this.api.get('/api/v1/type/common/target/nninfo/nnid/'+params+'/', '').then((data) => {
            if(data != undefined){
                data = JSON.parse(data);
            }

            this.log("getCommonNNInfo", data)
            return data;
        });
    }


    //Network WF Info
    putBotSetupInfo(params, jsonData) {
        return this.api.post('/api/v1/type/service/botbuilder/def/', jsonData).then((data) => {
            this.log("putBotSetupInfo", data)
            data = JSON.parse(data);
            return data;
        });
    }

    //Network WF Info
    postCommonNNInfoWF(params, jsonData) {
        return this.api.post('/api/v1/type/common/target/nninfo/nnid/'+params+'/version/', jsonData).then((data) => {
            data = JSON.parse(data);
            this.log("postCommonNNInfoWF", data)
            return data;
        });
    }

    putCommonNNInfoWF(params, jsonData) {
        return this.api.put('/api/v1/type/common/target/nninfo/nnid/'+params+'/version/', jsonData).then((data) => {
            data = JSON.parse(data);
            this.log("getCommonNNInfoWF", data)
            return data;
        });
    }

    getCommonNNInfoWF(params) {
        return this.api.get('/api/v1/type/common/target/nninfo/nnid/'+params+'/version/', '').then((data) => {
            data = JSON.parse(data);
            this.log("getCommonNNInfoWF", data)
            return data;
        });
    }

    //Network Batch Info
    // postCommonNNInfoBatch(params, wf_ver_id, jsonData) {
    //     return this.api.post('/api/v1/type/common/target/nninfo/nnid/'+params+'/version/'+wf_ver_id+'/', jsonData).then((data) => {
    //         data = JSON.parse(data);
    //         this.log("postCommonNNInfoBatch", data)
    //         return data;
    //     });
    // }

    putCommonNNInfoBatch(params, wf_ver_id, jsonData) {
        return this.api.put('/api/v1/type/common/target/nninfo/nnid/'+params+'/version/'+wf_ver_id+'/', jsonData).then((data) => {
            data = JSON.parse(data);
            this.log("putCommonNNInfoBatch", data)
            return data;
        });
    }

    getCommonNNInfoBatch(params, wf_ver_id){
        return this.api.get('/api/v1/type/common/target/nninfo/nnid/'+params+'/version/'+wf_ver_id+'/', "").then((data) => {
            data = JSON.parse(data);
            this.log("getCommonBatchInfo", data)
            return data;
        });
    }

    //Network WF Node Info
    postCommonNNInfoWFNode(params, wf_ver_id, jsonData) {
        return this.api.post('/api/v1/type/wf/target/init/mode/simple/'+params+'/wfver/'+wf_ver_id+'/', jsonData).then((data) => {
            data = JSON.parse(data);
            this.log("postCommonNNInfoWFNode", data)
            return data;
        });
    }

    putCommonNNInfoWFNode(params, wf_ver_id, node, jsonData) {
        return this.api.put('/api/v1/type/wf/direct/nnid/'+params+'/ver/'+wf_ver_id+'/node/'+node+'/', jsonData).then((data) => {
            data = JSON.parse(data);
            this.log("putCommonNNInfoWFNode", data)
            return data;
        });
    }

    getCommonNNInfoWFNode(params, wf_ver_id, desc){
        return this.api.get('/api/v1/type/wf/target/init/mode/simple/'+params+'/wfver/'+wf_ver_id+'/desc/'+desc+'/', "").then((data) => {
            data = JSON.parse(data);
            this.log("getCommonNNInfoWFNode", data)
            return data;
        });
    }

    

    //File Upload
    putFileUpload(params, wf_ver_id, dir, jsonData){
        return this.api.put('/api/v1/type/wf/state/data/detail/upload/file/nnid/'+params+'/ver/'+wf_ver_id+'/dir/'+dir+'/', jsonData).then((data) => {
            data = JSON.parse(data);
            this.log("putFileUpload", data)
            return data;
        });
    }

    getFileUpload(params, wf_ver_id, dir, type){
        return this.api.get('/api/v1/type/wf/state/data/detail/upload/file/nnid/'+params+'/ver/'+wf_ver_id+'/dir/'+dir+'/type/'+type+'/', '').then((data) => {
            data = JSON.parse(data);
            this.log("getFileUploadPath:", data)
            return data;
        });
    }

    deleteFileUpload(params, wf_ver_id, dir, jsonData){
        return this.api.delete('/api/v1/type/wf/state/data/detail/upload/file/nnid/'+params+'/ver/'+wf_ver_id+'/dir/'+dir+'/', jsonData).then((data) => {
            data = JSON.parse(data);
            this.log("deleteFileUploadPath", data)
            return data;
        });
    }

    //Auto Ml Info
    getCommonNNInfoAuto(params) {
        return this.api.get('/api/v1/type/automl/state/rule/graph_id/'+params+'/', '').then((data) => {
            data = JSON.parse(data);
            this.log("getCommonNNInfoAuto", data)
           return data;
        });
    }

    //Auto Ml Run
    postCommonNNInfoAutoSetup(params, jsonData) {
        return this.api.post('/api/v1/type/automl/state/parm/nnid/'+params+'/', jsonData).then((data) => {
            data = JSON.parse(data);
            this.log("postCommonNNInfoAutoSetup", data)
            return data;
        });
    }

    //Auto Ml Run
    postCommonNNInfoAuto(params) {
        return this.api.post('/api/v1/type/automl/state/train/nnid/'+params+'/', '').then((data) => {
            data = JSON.parse(data);
            this.log("getCommonNNInfoAuto", data)
           return data;
        });
    }

    //Run Train
    postTainRun(params, wf_ver_id) {
        return this.api.post('/api/v1/type/runmanager/state/train/nnid/'+params+'/ver/'+wf_ver_id+'/', '').then((data) => {
            data = JSON.parse(data);
            this.log("postTainRun", data)
            return data;
        });
    }

    //View
    getCommonNodeInfoView(params) {
        return this.api.get('/api/v1/type/automl/state/stat/nnid/'+params+'/', '').then((data) => {
            data = JSON.parse(data);
            this.log("getCommonNodeInfoView", data)
           return data;
        });
    }




    

    putCommonNetConf(nn_id, wf_ver_id, net_type, conf_type, jsonData) {
        return this.api.put('/api/v1/type/wf/state/netconf/detail/'+net_type+'/nnid/'+nn_id+'/ver/'+wf_ver_id+'/node/'+conf_type+'/', jsonData).then((data) => {
            data = JSON.parse(data);
            this.log("putCommonNetConf", data)
            return data;
        });
    }

    putCommonDataConf(nn_id, wf_ver_id, data_Type, conf_type, jsonData) {
        return this.api.put('/api/v1/type/wf/state/'+data_Type+'/src/local/form/file/prg/source/nnid/'+nn_id+'/ver/'+wf_ver_id+'/node/'+conf_type+'/', jsonData).then((data) => {
            data = JSON.parse(data);
            this.log("putCommonDataConf", data)
            return data;
        });
    }

    putCommonFeedConf(nn_id, wf_ver_id, net_type, conf_type, jsonData) {
        return this.api.put('/api/v1/type/wf/state/pre/detail/feed/src/frame/net/'+net_type+'/nnid/'+nn_id+'/ver/'+wf_ver_id+'/node/'+conf_type+'/', jsonData).then((data) => {
            data = JSON.parse(data);
            this.log("putCommonFeedConf", data)
            return data;
        });
    }

    getCategoryList(opt_url, params) {
        let url='/api/v1/type/common/item/' + opt_url + '/';
        return this.api.get(url, params).then((data) => {
            data = JSON.parse(data);
           return data.result;
        });
    }

    getSubCategoryList(opt_url, params) {
        let url='/api/v1/type/common/item/subcategory/' + opt_url + '/';
        return this.api.get(url, params).then((data) => {
            data = JSON.parse(data);
           return data;
        });
    }

    getConfigNnCnn(params) {
        return this.api.get(`/api/v1/type/cnn/config/`, params).then((data) => {
           return data;
        });
    }

    putConfigNnCnn(params) {
        return this.api.put(`/api/v1/type/cnn/config/`, params).then((data) => {
           return data;
        });
    }

    postDataNnCnn(params) {
        return this.api.post(`/api/v1/type/cnn/data/`, params).then((data) => {
           return data;
        });
    }

    getDataNnCnn(params) {
        return this.api.get(`/api/v1/type/cnn/data/`, params).then((data) => {
           return data;
        });
    }

    putDataNnCnn(params) {
        return this.api.put(`/api/v1/type/cnn/data/`, params).then((data) => {
           return data;
        });
    }

    postTrainNnCnn(params) {
        return this.api.post(`/api/v1/type/cnn/train/`, params).then((data) => {
           return data;
        });
    }

    postPredictNnCnn(params) {
        return this.api.post(`/api/v1/type/cnn/predict/`, params).then((data) => {
           return data;
        });
    }

    getPreviewImagePath(params) {
        let url='/api/v1/type/imgpreview/nnid/';
        return this.api.get(url, params + "/").then((data) => {
            data = JSON.parse(data);
           return data;
        });
    }

    getTableList(params) {
        let url='/api/v1/type/imagefile/';
        return this.api.get(url, params).then((data) => {
            data = JSON.parse(data);
           return data;
        });
    }

    postTableList(opt_url, params) {
        let url='/api/v1/type/imagefile/' + opt_url;
        return this.api.post(url, params).then((data) => {
            data = JSON.parse(data);
            return data;
        });
    }

    deleteTableList(opt_url, params) {
        let url='/api/v1/type/imagefile/' + opt_url;
        return this.api.delete(url, params).then((data) => {
            data = JSON.parse(data);
            return data;
        });
    }

    getImageFormatData(opt_url, params) {
        let url='/api/v1/type/imagefile/' + opt_url;
        return this.api.get(url, params).then((data) => {
            data = JSON.parse(data);
           return data;
        });
    }

    postImageFormatData(opt_url, params) {
        let url='/api/v1/type/imagefile/' + opt_url;
        return this.api.post(url, params).then((data) => {
            data = JSON.parse(data);
           return data;
        });
    }

    //kyj
    getAllNetVerInfo(opt_url, params) {
        let url='/api/v1/type/common/target/nninfo/nnid/' + opt_url + '/version/';
        return this.api.get(url, "").then((data) => {
            data = JSON.parse(data);
           return data;
        });
    }
    //kyj
    getAllNetBatchInfo(opt_url, opt_url1, params){
        let url='/api/v1/type/common/target/nninfo/nnid/' + opt_url + '/version/' + opt_url1 + '/';
        return this.api.get(url, "").then((data) => {
            data = JSON.parse(data);
           return data;
        });
    }

    getAllNetBaseInfo(opt_url, params) {
        let url='/api/v1/type/common/nninfo/all/';
        return this.api.get(url, "").then((data) => {
            data = JSON.parse(data);
           return data;
        });
    }

    getImageLabelData(opt_url, params) {
        let url='/api/v1/type/imagefile/' + opt_url ;
        return this.api.get(url, "").then((data) => {
            data = JSON.parse(data);
           return data;
        });
    }

    postImageLabelData(opt_url, params) {
        let url='/api/v1/type/imagefile/' + opt_url ;
        return this.api.post(url, "").then((data) => {
            data = JSON.parse(data);
           return data;
        });
    }

    deleteImageLabelData(opt_url, params) {
        let url='/api/v1/type/imagefile/' + opt_url ;
        return this.api.delete(url, "").then((data) => {
            data = JSON.parse(data);
           return data;
        });
    }
    getWdnnTableList(params) {
        let url='/api/v1/type/dataframe/';
        return this.api.get(url, params).then((data) => {
            data = JSON.parse(data);
           return data;
        });
    }

    getWdnnTableDataFromHbase(opt_url, params) {
        let url = '/api/v1/type/dataframe/base/' + opt_url;
        return this.api.get(url, "").then((data) => {
            data = JSON.parse(data);
           return data;
        });
    }
    postWdnnDataFrameFormat(opt_url, params) {
        console.log(params)
        let key_set = Object.keys(params)
        for(let key of key_set){
            console.log(key +"---->"+ params[key]);
         }
        let url='/api/v1/type/dataframe/base/' + opt_url; 
        return this.api.post(url, params).then((data) => {
            data = JSON.parse(data);
           return data;
        });
    }

    getTableListOnDataConfig(opt_url, params) {
        let url='/api/v1/type/dataframe/base/' + opt_url +'/table/';
        return this.api.get(url, params).then((data) => {
            data = JSON.parse(data);
           return data;
        });
    }
    getDataBaseOnDataConfig(params) {
        let url='/api/v1/type/dataframe/base/';//local test for JSON
        return this.api.get(url, params).then((data) => {
            data = JSON.parse(data);
           return data;
        });
    }
    getDataFrameOnNetworkConfig(opt_url, nnId) {
        let url='/api/v1/type/dataframe/format/'+ nnId +'/type/' +opt_url + '/'
        console.log(url)
        return this.api.get(url, "").then((data) => {
            data = JSON.parse(data);
           return data;
        });
    }
    getWdnnConf(nnId) {
        let url='/api/v1/type/wdnn/conf/'+ nnId +'/';
        return this.api.get(url, "").then((data) => {
            data = JSON.parse(data);
            console.log(data);
           return data;
        });
    }
    postWdnnConf(opt_url, params) {
        let key_set = Object.keys(params)
        for(let key of key_set){
            console.log(key +"---->"+ params[key]);
         }
        let url='/api/v1/type/wdnn/conf/' + opt_url +'/'; 
        return this.api.post(url, params).then((data) => {
            data = JSON.parse(data);
           return data;
        });
    }

    postCnnTrain(opt_url, params) {
        opt_url = "mesm10cnn61110/";
        params = { epoch :"12", testset : "10"}
        let url='/api/v1/type/cnn/train/' + opt_url; 
        return this.api.post(url, params).then((data) => {
            //data = JSON.parse(data);
        });
    }

    postCnnEval(opt_url, params) {
        opt_url = "mesm10cnn61110/"
        params = { samplenum :"12", samplenethod : ""}
        let url='/api/v1/type/cnn/eval/' + opt_url; 
        //let url = '/api/v1/type/wdnn/eval/'
        return this.api.post(url, params).then((data) => {
            //data = JSON.parse(data);
        });
    }

    postWdnnTrain(opt_url, params) {
        let url='/api/v1/type/wdnn/train/' + opt_url; 
        return this.api.post(url, params).then((data) => {
           data = JSON.parse(data);
           return data;
        });
    }

    postWdnnEval(opt_url, params) {
        let url='/api/v1/type/wdnn/eval/' + opt_url; 
        return this.api.post(url, params).then((data) => {
            //data = JSON.parse(data);
        });
    }


    getCategoryList() {
        let url='/api/v1/type/common/item/category/all/';
        return this.api.get(url, "").then((data) => {
            data = JSON.parse(data);
           return data;
        });
    }

    getSubCategoryList(cate) {
        let url='/api/v1/type/common/item/subcategory/' + cate + '/';
        return this.api.get(url, "").then((data) => {
            data = JSON.parse(data);
           return data;
        });
    }   

    getNameSpaceList(datatype, preprocess , category, subcategory) {
        let url='/api/v1/type/schema/datatype/' +datatype+'/preprocess/'+preprocess+'/category/'+category+'/subcategory/'+subcategory+'/'
        return this.api.get(url, "").then((data) => {
            data = JSON.parse(data);
           return data;
        });
    }
    
    getNetConfigCommonInfo(nnid) {
        let url = '/api/v1/type/common/nninfo/'+ nnid +'/'
        return this.api.get(url).then((data) => {
           return data;
        });
    }
    
    getNetConfigFormatInfo(params, nnid) {
        let url = '/api/v1/type/imagefile/base/'+params.dir+'/table/'+params.table+'/format/'+nnid+'/';
        return this.api.get(url).then((data) => {
           return data;
        });
    }  

    postNNNetConfigInfo(nnid,params) {
        let url = '/api/v1/type/cnn/conf/' + nnid + '/';
        return this.api.post(url, params).then((data) => {
            return data
        });
    }     

    postNeuralNetTrain(netType, netId, params) {
        let url='/api/v1/type/' + netType + '/train/' + netId + '/'; 
        return this.api.post(url, params).then((data) => {
            return data
        });
    } 

    postNeuralNetEval(netType, netId, params) {
        let url='/api/v1/type/' + netType + '/eval/' + netId + '/'; 
        return this.api.post(url, params).then((data) => {
            return data
        });
    } 

    postNeuralNetCheck(netType, netId, params) {
        let url='/api/v1/type/'+ netType +'/checker/' + netId + '/'; 
        return this.api.post(url, "").then((data) => {
            return JSON.parse(data)
        });
    } 

    getNeuralNetStat(netId) {
        let url='/api/v1/type/common/stat/' + netId + '/'; 
        return this.api.get(url, "").then((data) => {
            data = JSON.parse(data);
            return data.result;
        });
    } 

    getJobInfo(netId) {
        let url='/api/v1/type/common/job/' + netId + '/'; 
        return this.api.get(url, "").then((data) => {
            return JSON.parse(data);
        });
    } 

    setJobInfo(netId, parm) {
        let url='/api/v1/type/common/job/' + netId + '/'; 
        return this.api.post(url, parm).then((data) => {
            return JSON.parse(data);
        });
    } 
}