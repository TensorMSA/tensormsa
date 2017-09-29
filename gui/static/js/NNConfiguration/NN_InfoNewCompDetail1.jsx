import React from 'react';
import Api from './../utils/Api'
import Modal from 'react-modal';
import EnvConstants from './../constants/EnvConstants';
import { BootstrapTable, TableHeaderColumn } from 'react-bootstrap-table';

import ReportRepository from './../repositories/ReportRepository'
import FileUploadComponent from './../NNLayout/common/FileUploadComponent'
import JsonConfComponent from './../NNLayout/common/JsonConfComponent'
// import TabPanel from 'react-tab-panel'
// import 'react-tab-panel/index.css'

import { Tab, Tabs, TabList, TabPanel } from 'react-tabs';
import 'react-tabs/style/react-tabs.scss';

import { downloadFile } from 'download-url-file';

import Help_resnet from './../help/Help_resnet';
import Help_autoencoder_csv from './../help/Help_autoencoder_csv';
import Help_autoencoder_img from './../help/Help_autoencoder_img';
import Help_bilstmcrf_iob from './../help/Help_bilstmcrf_iob';
import Help_cnn from './../help/Help_cnn';
import Help_doc2vec from './../help/Help_doc2vec';
import Help_fasttext_txt from './../help/Help_fasttext_txt';
import Help_seq2seq from './../help/Help_seq2seq';
import Help_seq2seq_csv from './../help/Help_seq2seq_csv';
import Help_wcnn from './../help/Help_wcnn';
import Help_wdnn from './../help/Help_wdnn';
import Help_wdnn_keras from './../help/Help_wdnn_keras';
import Help_word2vec from './../help/Help_word2vec';
import Help_word2vec_frame from './../help/Help_word2vec_frame';

export default class NN_InfoNewCompDetail1 extends React.Component {
    constructor(props, context) {
        super(props);
        this.state = {
            tableData: null,
            NN_TableData: null,
            NN_TableDataDetail : null,
            color : "red",
            isViewImage: false,//Net Select Image view
            isViewImageDetail : null,//Net Select Image view
            netType : null,
            url : EnvConstants.getWebServerUrl(),
            NN_TableColArr1:[    {index:0,      id:"sel",                   name:"Sel"}
                                ,{index:1,      id:"network",               name:"Network"}
                                ,{index:2,      id:"description",           name:"Description"}
                                ,{index:3,      id:"sample",                name:"SampleFile"}
                                ,{index:4,      id:"help",                  name:"Help"}

                            ]
        };
        this.setConfigData = this.setConfigData.bind(this); 
    }

    // 최초 1회 실행하여 Network Config List를 가져온다.
    componentDidMount(){
        this.getCommonNNInfoAuto(this.props.tabIndex);
        
    }

    // get Network List ex)wdnn, resnet, charcnn_csv    
    getCommonNNInfoAuto(params) {
        this.props.reportRepository.getCommonNNInfoAuto(params).then((tableData) => {
            this.setState({ NN_TableData: tableData })
        });   
    }

    // get Network config list ex)netconf_node, dataconf_node
    getCommonNNInfoAutoDetail(row){
        this.props.reportRepository.getCommonNNInfoAuto(row).then((tableData) => {
            if(tableData[0] == undefined){
                this.setState({ NN_TableDataDetail: null })
            }else{
                let auto = [tableData[0]['fields']['graph_flow_data']]
                let single = [tableData[0]['fields']['graph_flow_data_single']]
                if(this.props.tabIndexAS == 1){
                    this.setState({ NN_TableDataDetail: auto })
                }else{
                    this.setState({ NN_TableDataDetail: single})
                }
            }
            
            
            
        });
    }

    findColInfo(col, idxType, idxName){
        let fItem = ""
        if(idxType == "index"){
            fItem = col.find(data => { return data.index == idxName})
        }else if(idxType == "id"){
            fItem = col.find(data => { return data.id == idxName})
        }else if(idxType == "name"){
            fItem = col.find(data => { return data.name == idxName})
        }

        return fItem
    }

    //Network List가 선택 되면 해당 Config를 조회해준다.
    handleChangeRadio(selectedValue){
        this.state.isViewImage = false
        let netSelectTable = this.refs.master2
        let value = selectedValue.target.value //radio button cell
        if(value == undefined && selectedValue.target.attributes[0] != undefined){// key, desc cell
            value = selectedValue.target.attributes [0].value
            for(let i=1 ; i < netSelectTable.rows.length ; i++){
                let key = netSelectTable.rows[i].children[0].children.rd1
                if(key.value == value && key.checked == false){
                    key.checked = true
                }else if(key.value == value && key.checked == true){
                    key.checked = false
                    value = ""
                }
            }
        }
        this.state.netType = value

        this.getCommonNNInfoAutoDetail(value)
    }

    setConfigData(){
        let netSelectTable = this.refs.master2
        for(let i=1 ; i < netSelectTable.rows.length ; i++){
            let key = netSelectTable.rows[i].children[0].children.rd1
            if(key.checked == true){
                this.getCommonNNInfoAutoDetail(key.value)
            }
        }
    }

    // Network 를 선택 하면 아래에 Image를 보여준다.
    viewNetImage(value){
        let url = value.target.alt
        if(this.state.isViewImage == true && this.state.isViewImageDetail == url ){//
            this.setState({ isViewImage: false })
            this.setState({ isViewImageDetail: null })
        }else{
            this.setState({ isViewImage: true })
            this.setState({ isViewImageDetail: url })
        }
    }

    fileDownloadFunc(selectedValue){
        let path = selectedValue.target.alt
        let url = this.state.url
        url = url+path
        console.log(url)
        // downloadFile(url);
    }

    render() {
        let k = 1
        function sortByKey(array, key) {
            return array.sort(function(a, b) {
                var x = a[key]; var y = b[key];
                return ((x < y) ? -1 : ((x > y) ? 1 : 0));
            });
        }

        function makeHeader(data){// Make header
            let headerData = []
            for(let i in data){
                headerData.push(<th key={k++} style={{"textAlign":"center"}} >{data[i].name}</th>)
            }
            let tableHeader = []; //make header
            tableHeader.push(<tr key={k++} >{headerData}</tr>)
            return tableHeader
        }
        /////////////////////////////////////////////////////////////////////////////////////////
        // Select Network List
        /////////////////////////////////////////////////////////////////////////////////////////

        // Network List
        let nnInfoNewList = [];
        if (this.state.NN_TableData != null) {
            for (var i in this.state.NN_TableData) {
                nnInfoNewList[i] = {id:this.state.NN_TableData[i]["pk"]
                                    , desc:this.state.NN_TableData[i]["fields"]["graph_flow_desc"]
                                    , path:this.state.NN_TableData[i]["fields"]["train_file_path"]
                                    };
            }
        }
        nnInfoNewList = sortByKey(nnInfoNewList, 'id');

        // Network Select Header
        let tableHeaderSL = makeHeader(this.state.NN_TableColArr1)

        //Network Select Data
        let clickUrl = ""
        let tableDataSL = []; // make tabledata

        for(let rows in nnInfoNewList){
            let colDataSL = [];
            let row = nnInfoNewList[rows]

            if(this.props.tabIndex == 10){
                colDataSL.push(<td key={k++} > < input type = "checkbox" name="rd1"
                                                                    value = {row["id"]}
                                                                    onClick={this.handleChangeRadio.bind(this)} 
                                                                    style={{"textAlign":"center"}} />  </td>)
            }else{
                colDataSL.push(<td key={k++} > < input type = "radio" name="rd1"
                                                                    value = {row["id"]}
                                                                    onClick={this.handleChangeRadio.bind(this)} 
                                                                    style={{"textAlign":"center"}} />  </td>)
            }
            
            colDataSL.push(<td key={k++} value = {row["id"]} onClick={this.handleChangeRadio.bind(this)} > {row["id"]} </td>) 
            colDataSL.push(<td key={k++} value = {row["id"]} style={{"textAlign":"left"}} onClick={this.handleChangeRadio.bind(this)} > {row["desc"]} </td>) 
            clickUrl = "./images/ico_menu03.png"
            colDataSL.push(<td key={k++} > <a href= {row["path"]} download ><img src={clickUrl} /></a></td>)
            clickUrl = "./images/ico_help_on.png"
            colDataSL.push(<td key={k++} > <img style ={{width:20, "cursor":"pointer"}} alt = {row["id"]}
                                                onClick={this.viewNetImage.bind(this)} 
                                                src={clickUrl} /></td>)

            

            tableDataSL.push(<tr key={k++}>{colDataSL}</tr>)
        }


        let nnInfoNewListTable = []
        nnInfoNewListTable.push(<thead ref='thead' key={k++} className="center">{tableHeaderSL}</thead>)
        nnInfoNewListTable.push(<tbody ref='tbody' key={k++} className="center" >{tableDataSL}</tbody>)

        let helpData = []
        let width = 800
        // helpData.push(<img key={k++} src = {this.state.isViewImageDetail} style={{"width":"800"}} />)
        if(this.state.isViewImageDetail == "resnet"){
            helpData.push(<Help_resnet key={k++} width={width} />)
        }else if(this.state.isViewImageDetail == "autoencoder_csv"){
            helpData.push(<Help_autoencoder_csv key={k++} width={width} />)
        }else if(this.state.isViewImageDetail == "autoencoder_img"){
            helpData.push(<Help_autoencoder_img key={k++} width={width} />)
        }else if(this.state.isViewImageDetail == "bilstmcrf_iob"){
            helpData.push(<Help_bilstmcrf_iob key={k++} width={width} />)
        }else if(this.state.isViewImageDetail == "cnn"){
            helpData.push(<Help_cnn key={k++} width={width} />)
        }else if(this.state.isViewImageDetail == "doc2vec"){
            helpData.push(<Help_doc2vec key={k++} width={width} />)
        }else if(this.state.isViewImageDetail == "fasttext_txt"){
            helpData.push(<Help_fasttext_txt key={k++} width={width} />)
        }else if(this.state.isViewImageDetail == "seq2seq"){
            helpData.push(<Help_seq2seq key={k++} width={width} />)
        }else if(this.state.isViewImageDetail == "seq2seq_csv"){
            helpData.push(<Help_seq2seq_csv key={k++} width={width} />)
        }else if(this.state.isViewImageDetail == "wcnn"){
            helpData.push(<Help_wcnn key={k++} width={width} />)
        }else if(this.state.isViewImageDetail == "wdnn"){
            helpData.push(<Help_wdnn key={k++} width={width} />)
        }else if(this.state.isViewImageDetail == "wdnn_keras"){
            helpData.push(<Help_wdnn_keras key={k++} width={width} />)
        }else if(this.state.isViewImageDetail == "word2vec"){
            helpData.push(<Help_word2vec key={k++} width={width} />)
        }else if(this.state.isViewImageDetail == "word2vec_frame"){
            helpData.push(<Help_word2vec_frame key={k++} width={width} />)
        }


        return (
            <section>
                    <div>
                        <table className="table detail" ref= 'master2' >
                            {nnInfoNewListTable}
                        </table>
                    </div>

                    {this.state.isViewImage ?
                        <div>
                        <table className="table detail" ref= 'master2_1' >
                        <tr><td style={{"textAlign":"center"}}>
                            {helpData}
                        </td></tr>
                        </table>
                        </div>
                        :
                        <div>
                        </div>
                    }

                    <div>
                        <h2> Network Config ({this.state.netType}) </h2>
                    </div>
  
                        <JsonConfComponent ref="netconfig"
                                            tabIndexAS = {this.props.tabIndexAS} 
                                            editable="Y" 
                                            NN_TableDataDetail={this.state.NN_TableDataDetail} />


 <div>
                    <table className="table detail">
                    <tr>
                    <td style={{"verticalAlign":"top"}}>

                        <FileUploadComponent ref="trainfilesrc" 
                                              title="Network Train Source File Upload"
                                                nn_id={this.props.tmp_train_node_name} 
                                                nn_wf_ver_id={"1"} 
                                                nn_node_name={this.props.train_node_name} 
                                                nn_path_type={"source"}
                                                uploadbtnflag={true} 
                                                deletebtnflag={true} />
                    </td>

                    <td style={{"verticalAlign":"top"}}>

                        <FileUploadComponent ref="evalfilesrc" 
                                                title="Network Eval Source File Upload"
                                                nn_id={this.props.tmp_eval_node_name} 
                                                nn_wf_ver_id={"1"} 
                                                nn_node_name={this.props.eval_node_name} 
                                                nn_path_type={"source"}
                                                uploadbtnflag={true} 
                                                deletebtnflag={true} />
                        </td>

                    </tr>
                    </table>

                    </div>
            </section>

        );
    }
}

NN_InfoNewCompDetail1.defaultProps = {
    reportRepository: new ReportRepository(new Api())
};




