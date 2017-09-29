import React from 'react';
import Api from './../utils/Api'
import Modal from 'react-modal';
import ReportRepository from './../repositories/ReportRepository'
import FileUploadComponent from './../NNLayout/common/FileUploadComponent'
import JsonConfComponent from './../NNLayout/common/JsonConfComponent'
import NN_InfoNewCompDetail1 from './../NNConfiguration/NN_InfoNewCompDetail1'
import { Tab, Tabs, TabList, TabPanel } from 'react-tabs';
import 'react-tabs/style/react-tabs.scss';
import EnvConstants from './../constants/EnvConstants';

export default class NN_InfoApplicationList extends React.Component {
    constructor(props, context) {
        super(props);
        this.state = {
            tableData: null,
            NN_TableMaster: null,
            NN_TableData: null,
            NN_TableDataDetail : null,
            nn_id : null,
            wf_ver_id : null,
            color : "red",
            train_node_name:null,
            eval_node_name:null,
            tmp_train_node_name:"tmpTrainNodeName",
            tmp_eval_node_name:"tmpEvalNodeName",
            NN_TableColArr1:[    {index:0,      id:"title",                 name:"Title"}
                                ,{index:1,      id:"input_data",            name:"Input Data"}
                                ,{index:2,      id:"example",               name:"Example"}
                            ],
            tabIndex:1
        };
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

    // Network Create
    saveData() {
        let flag = "T"
        let title = ""
        let input_data = ""
        let table = this.refs.master1
        let col = this.state.NN_TableColArr1
        
        // Validation Check
        for (let i=1 ; i < table.rows.length ; i++) {
            title = table.rows[i].cells[this.findColInfo(col, "id", "title").index].innerText
            input_data = table.rows[i].cells[this.findColInfo(col, "id", "input_data").index].children[0].value
            if(input_data == null || input_data == ""){ alert( title + " is not exist." );return; flag = "F"; break;}
        }
        
        // Make NN Info
        let inDefault = ["test", "cb_id","intent_id"]// "biz_cate","biz_sub_cate","nn_title","nn_desc"]
        let dparam = {}
        //for (let i=1 ; i < table.rows.length ; i++) {
        for (let i=1 ; i < 2 ; i++) {
            title = table.rows[i].cells[this.findColInfo(col, "id", "title").index].innerText
            input_data = table.rows[i].cells[this.findColInfo(col, "id", "input_data").index].children[0].value
            dparam[inDefault[i]] = input_data
            console.log(inDefault[i] + " " + input_data )
        }
        console.log(dparam)


        dparam["chat_cate"]=  "service",
        dparam["chat_sub_cate"] = "info_bot",
        dparam["cb_title"] = "info_bot",
        dparam["cb_desc"] = "info_bot",
        dparam["creation_date"]= "2017-05-22T18:00:00.000",
        dparam["last_update_date"]= "2017-05-22T18:00:00.000",
        dparam["created_by"] = "KSS",
        dparam["last_updated_by"] = "KSS"
        // Make NN Info
        this.props.reportRepository.putBotSetupInfo("", dparam).then((dparam) => {
            dparam["use_flag"] = "Y"

        });

    }

    runChat(){
        let params = "width=800,height=1000";
        window.open(EnvConstants.getWebServerUrl()+"/chatbot/index.html","chatbot",params)
    }

    render() {
        let k = 1
        /////////////////////////////////////////////////////////////////////////////////////////
        // First Network Default
        /////////////////////////////////////////////////////////////////////////////////////////
        if (this.state.NN_TableMaster == null){
            this.state.NN_TableMaster = [   
                                            {title:"Chatbot ID" , width:10 , input_data:"cb0002", ex:"chatbot id"}
                                            ,{title:"Chatbot Category" , width:10 , input_data:"service", ex:"Category"}
                                            ,{title:"Chatbot SubCategory" , width:10 , input_data:"info_bot", ex:"Sub"}
                                            ,{title:"Tagging Type" , width:10  , input_data:"dict", ex:"Tagging Info"}
                                            ,{title:"Proper Noun" , width:10 , input_data:"{'tagdate': [1, '/hoya_model_root/chatbot/date.txt', False]}", ex:"Proper Noun"}
                                         ];
        }

        if (this.state.NN_TableMaster2 == null){
            this.state.NN_TableMaster2 = [   

                                            {title:"Intent Model" , width:10 , input_data:"wcnntest02", ex:"Intent Model Name"}
                                            ,{title:"Intent ID" , width:10 , input_data:"1", ex:"Intent"}
                                            ,{title:"entity_type" , width:10 , input_data:"key", ex:"Key, extra"}
                                            ,{title:"entity_list" , width:10 , input_data:"{'key': ['tagdate', 'tagloc', 'tagmenu']}", ex:"JSON Format"}
                                         ];
        }


        if (this.state.NN_TableMaster3 == null){
            this.state.NN_TableMaster3 = [   
                                            {title:"Story ID" , width:10 , input_data:"1", ex:"1,2,3,4,5"}
                                            ,{title:"Story Type" , width:10 , input_data:"response", ex:"response / default"}
                                            ,{title:"Entity Type" , width:10 ,input_data:"key", ex:"ex) key, extra"}
                                            ,{title:"Output_Entity" , width:10 ,input_data:"{'entity':['tagdate','tagloc','tagmenu']}", ex:"display entity"}
                                            ,{title:"output_data" , width:10 ,input_data:"주문이 완료", ex:"display sentence"}
                                            ,{title:"Response Type" , width:10 , input_data:"entity", ex:"entity / default"}
                                         ];
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

        let tableHeader = makeHeader(this.state.NN_TableColArr1)
        let tableData = []
        for(let rows in this.state.NN_TableMaster){
            let colData = [];
            let row = this.state.NN_TableMaster[rows]
            colData.push(<td key={k++} style={{ "width":"20%"}}> {row["title"]} </td>)
            colData.push(<td key={k++} > < input type = {"string"} style={{"textAlign":"center", "width":"100%"}} 
                                                        defaultValue = {row["input_data"]}
                                                        maxLength = {row["width"]}  />  </td>)
            colData.push(<td key={k++} style={{"textAlign":"left", "width":"30%"}} > {row["ex"]} </td>)
            tableData.push(<tr key={k++}>{colData}</tr>)
        }

        let tableData2 = []
        for(let rows in this.state.NN_TableMaster2){
            let colData = [];
            let row = this.state.NN_TableMaster2[rows]
            colData.push(<td key={k++} style={{ "width":"20%"}}> {row["title"]} </td>)
            colData.push(<td key={k++} > < input type = {"string"} style={{"textAlign":"center", "width":"100%"}} 
                                                        defaultValue = {row["input_data"]}
                                                        maxLength = {row["width"]}  />  </td>)
            colData.push(<td key={k++} style={{"textAlign":"left", "width":"30%"}} > {row["ex"]} </td>)
            tableData2.push(<tr key={k++}>{colData}</tr>)
        }

        let tableData3 = []
        for(let rows in this.state.NN_TableMaster3){
            let colData = [];
            let row = this.state.NN_TableMaster3[rows]
            colData.push(<td key={k++} style={{ "width":"20%"}}> {row["title"]} </td>)
            colData.push(<td key={k++} > < input type = {"string"} style={{"textAlign":"center", "width":"100%"}} 
                                                        defaultValue = {row["input_data"]}
                                                        maxLength = {row["width"]}  />  </td>)
            colData.push(<td key={k++} style={{"textAlign":"left", "width":"30%"}} > {row["ex"]} </td>)
            tableData3.push(<tr key={k++}>{colData}</tr>)
        }

        let masterListTable = []
        masterListTable.push(<thead ref='thead' key={k++} className="center">{tableHeader}</thead>)
        masterListTable.push(<tbody ref='tbody' key={k++} className="center" >{tableData}</tbody>)

        let intentInfoTable = []
        intentInfoTable.push(<thead ref='thead' key={k++} className="center">{tableHeader}</thead>)
        intentInfoTable.push(<tbody ref='tbody' key={k++} className="center" >{tableData2}</tbody>)

        let storyInfoTable = []
        storyInfoTable.push(<thead ref='thead' key={k++} className="center">{tableHeader}</thead>)
        storyInfoTable.push(<tbody ref='tbody' key={k++} className="center" >{tableData3}</tbody>)

        return (
            <section>
                <h1 className="hidden">tensor MSA main table</h1>
                <div className="container paddingT10">
                    <div><img src="./images/chatbot_ico.png" width="128" height="128"></img></div>
                    <div className="tblBtnArea">
                        <button type="button" className="addnew" style={{"marginRight":"5px"}} onClick={() => this.saveData()} >Save</button>
                        <button type="button" className="save" onClick={() => this.runChat()} >Run Chat</button>
                    </div>

                    <div>
                        <h1> Bot Info </h1>
                    </div>


                    <div ref="masterInfo">
                        <table className="table detail" ref= 'master1' >
                            {masterListTable}
                        </table>
                    </div>
                    <div>
                        <h1> Intend Info </h1>
                    </div>
                    <div ref="intentInfo">
                        <table className="table detail" ref= 'master2' >
                            {intentInfoTable}
                        </table>
                    </div>
                    <div>
                        <h1> Story Info </h1>
                    </div>
                    <div ref="nerInfo">
                        <table className="table detail" ref= 'master3' >
                            {storyInfoTable}
                        </table>
                    </div>
                </div>
            </section>

        );
    }
}

NN_InfoApplicationList.defaultProps = {
    reportRepository: new ReportRepository(new Api())
};




