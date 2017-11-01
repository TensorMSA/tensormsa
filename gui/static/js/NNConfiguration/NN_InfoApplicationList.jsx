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
            NN_TableNet:null,
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
            tabIndex:1,
            color : "#14c0f2"
        };
    }

    componentDidMount(){
        this.getCommonNNInfo("all");// 화면에 들어 올때 검색을 해준다.
    }

    getCommonNNInfo(params) {
        this.props.reportRepository.getCommonNNInfo(params).then((tableData) => {
            this.setState({ NN_TableNet: null })//조회시 한번 Reset을 해주어야 테이블이 새로고침 된다.
            let wcnnData = []
            for(let i in tableData['fields']){
                if(tableData['fields'][i]['dir'] == 'wcnn'){
                    wcnnData.push(tableData['fields'][i])
                }
            }
            this.setState({ NN_TableNet: wcnnData })//조회한 것을 화면에 반영한다.
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

    // Network Create
    saveData() {
        let flag = "T"
        let title = ""
        let input_data = ""
        let table = this.refs.master1
        let col = this.state.NN_TableColArr1
        // Make Chatbot Info
        let bot_def_list = {}
        let bot_tagging = {}
        let bot_entity_list = {}
        let bot_entity_relation = {}
        let bot_intent_list = {}
        let bot_model_list = {}
        let bot_response_list = {}
        let bot_story_list = {}

        // Validation Check
        for (let i=1 ; i < table.rows.length ; i++) {
            title = table.rows[i].cells[this.findColInfo(col, "id", "title").index].innerText
            input_data = table.rows[i].cells[this.findColInfo(col, "id", "input_data").index].children[0].value
            if(input_data == null || input_data == ""){ alert( title + " is not exist." );return; flag = "F"; break;}
        }
        
        let inDefault = ["", "cb_id","chat_cate","chat_sub_cate","pos_type","proper_noun"]

        for (let i=1 ; i < 6 ; i++) {
            title = table.rows[i].cells[this.findColInfo(col, "id", "title").index].innerText
            input_data = table.rows[i].cells[this.findColInfo(col, "id", "input_data").index].children[0].value
            bot_def_list[inDefault[i]] = input_data
        }
        console.log(bot_def_list)

        bot_tagging["cb_id"] = bot_def_list["cb_id"]
        bot_tagging["pos_type"] = bot_def_list["pos_type"]
        //Tagging Table에 들어갈 단어의 경로
        bot_tagging["proper_noun"] = {
                        "tagdate": [1,bot_def_list["proper_noun"] + "/data/date.txt", false],
                        "tagloc": [2, bot_def_list["proper_noun"] + "/data/loc.txt", false],
                        "tagmenu": [3,bot_def_list["proper_noun"] + "/data/menu.txt", false]
                        }
        console.log("proper_noun" + bot_tagging["proper_noun"])

        bot_def_list["cb_title"] = "info_bot",
        bot_def_list["cb_desc"] = "info_bot",
        bot_def_list["creation_date"]= "2017-05-22T18:00:00.000",
        bot_def_list["last_update_date"]= "2017-05-22T18:00:00.000",
        bot_def_list["created_by"] = "KSS",
        bot_def_list["last_updated_by"] = "KSS"

        //Add Intent Info
        let table2 = this.refs.master2

        // Validation Check
        for (let i=1 ; i < table2.rows.length ; i++) {
            title = table2.rows[i].cells[this.findColInfo(col, "id", "title").index].innerText
            input_data = table2.rows[i].cells[this.findColInfo(col, "id", "input_data").index].children[0].value
            if(input_data == undefined){
                input_data = table2.rows[i].cells[this.findColInfo(col, "id", "input_data").index].children[0].children[0].value
            }
            if(input_data == null || input_data == ""){ alert( title + " is not exist." );return; flag = "F"; break;}
        }
        
        // Make Chatbot Info
        let inDefault2 = ["", "nn_id","intent_id","entity_type","entity_list"]

        for (let i=1 ; i < 5 ; i++) {
            title = table2.rows[i].cells[this.findColInfo(col, "id", "title").index].innerText
            input_data = table2.rows[i].cells[this.findColInfo(col, "id", "input_data").index].children[0].value
            if(input_data == undefined){
                input_data = table2.rows[i].cells[this.findColInfo(col, "id", "input_data").index].children[0].children[0].value
            }
            bot_entity_list[inDefault2[i]] = input_data
        }
        console.log(bot_entity_list)

        bot_entity_list["cb_id"] = bot_def_list["cb_id"]
        //Entity에 대한 테이블 구성 필요(Slot내 항목 정의)
        //bot_entity_list["entity_list"] = {'key': bot_entity_list["entity_list"]}
        bot_entity_list["entity_list"] = {'key':['tagdate', 'tagloc', 'tagmenu']}
        bot_intent_list["cb_id"] = bot_def_list["cb_id"]
        bot_intent_list["intent_id"] = bot_entity_list["intent_id"]
        bot_intent_list["intent_type"] = "model"
        bot_intent_list["intent_uuid"] = ""
        bot_intent_list["intent_desc"] = ""
        bot_intent_list["rule_value"] = {"key": ["알려줘"]}
        bot_intent_list["nn_type"] = "Seq2Seq"

        bot_model_list["cb_id"] = bot_def_list["cb_id"]
        bot_model_list["nn_id"] = bot_entity_list["nn_id"]
        bot_model_list["nn_purpose"] = "Intent" //의도 파악 모델에 대한 정의 필수
        bot_model_list["nn_type"] = ""
        bot_model_list["nn_label_data"] = ""
        bot_model_list["nn_desc"] = ""

        //Add Story Info
        let table3 = this.refs.master3
        
        // Validation Check
        for (let i=1 ; i < table3.rows.length ; i++) {
            title = table3.rows[i].cells[this.findColInfo(col, "id", "title").index].innerText
            input_data = table3.rows[i].cells[this.findColInfo(col, "id", "input_data").index].children[0].value
            if(input_data == null || input_data == ""){ alert( title + " is not exist." );return; flag = "F"; break;}
        }
        
        // Make Chatbot Info
        let inDefault3 = ["", "story_id","story_type","entity_type","output_entity","output_data","response_type"]

        for (let i=1 ; i < 6 ; i++) {
            title = table3.rows[i].cells[this.findColInfo(col, "id", "title").index].innerText
            input_data = table3.rows[i].cells[this.findColInfo(col, "id", "input_data").index].children[0].value
            bot_story_list[inDefault3[i]] = input_data
        }


        bot_story_list["intent_id"] = bot_entity_list["intent_id"]
        bot_story_list["story_desc"] = ""
        console.log(bot_story_list)

        bot_response_list["story_id"] = bot_story_list["story_id"]
        bot_response_list["nn_id"] = ""
        bot_response_list["output_entity"] = bot_story_list["output_entity"]
        bot_response_list["output_data"] = bot_story_list["output_data"]
        bot_response_list["response_type"] = bot_story_list["response_type"]

        // Make NN Info
        this.props.reportRepository.putBotSetupInfo("def", bot_def_list).then(() => {
            this.props.reportRepository.putBotSetupInfo("tag", bot_tagging).then(() => {
                //Add tag second row
                bot_tagging["pos_type"] = "ngram"
                bot_tagging["proper_noun"] = {}
            this.props.reportRepository.putBotSetupInfo("tag", bot_tagging).then(() => {
                this.props.reportRepository.putBotSetupInfo("model", bot_model_list).then(() => {
                    this.props.reportRepository.putBotSetupInfo("intent", bot_intent_list).then(() => {
                        this.props.reportRepository.putBotSetupInfo("entity", bot_entity_list).then(() => {
                            this.props.reportRepository.putBotSetupInfo("story", bot_story_list).then(() => {
                                this.props.reportRepository.putBotSetupInfo("response", bot_response_list).then(() => {
                                    console.log("Bot is set up")
                                });
                            });
                        });
                    });
                });
            });
            });
        });
    }

    runChat(){
        let table = this.refs.master1
        let col = this.state.NN_TableColArr1
        let chat_id = table.rows[1].cells[this.findColInfo(col, "id", "input_data").index].children[0].value
        let params = "width=800,height=1000";
        window.open(EnvConstants.getWebServerUrl()+"/chatbot?chat_id="+chat_id,"chatbot",params)
    }

    render() {
        let k = 1
        /////////////////////////////////////////////////////////////////////////////////////////
        // First Network Default
        /////////////////////////////////////////////////////////////////////////////////////////
        if (this.state.NN_TableMaster == null){
            this.state.NN_TableMaster = [   
                                            {title:"Chatbot ID" , width:10 , input_data:"cb01", ex:"chatbot id"}
                                            ,{title:"Chatbot Category" , width:10 , input_data:"service", ex:"Category"}
                                            ,{title:"Chatbot SubCategory" , width:10 , input_data:"info_bot", ex:"Sub Category"}
                                            ,{title:"Tagging Type" , width:10  , input_data:"dict", ex:"Tagging Info"}
                                            ,{title:"Proper Noun" , width:10 , input_data: "/home/dev/tensormsa/demo/botbuilder", ex:"Proper Noun Path"}
                                         ];
        }

        if (this.state.NN_TableMaster2 == null){
            this.state.NN_TableMaster2 = [   

                                            {title:"Intent Model" , width:10 , input_data:"wcnntest02", ex:"Intent Model Name"}
                                            ,{title:"Intent ID" , width:10 , input_data:"1", ex:"Intent"}
                                            ,{title:"entity_type" , width:10 , input_data:"key", ex:"Key, extra"}
                                            ,{title:"entity_list" , width:10 , input_data:"{'key':['tagdate', 'tagloc', 'tagmenu']}", ex:"JSON Format"}
                                         ];
        }


        if (this.state.NN_TableMaster3 == null){
            this.state.NN_TableMaster3 = [   
                                            {title:"Story ID" , width:10 , input_data:"1", ex:"1,2,3,4,5"}
                                            ,{title:"Story Type" , width:10 , input_data:"response", ex:"response / default"}
                                            ,{title:"Entity Type" , width:10 ,input_data:"key", ex:"ex) key, extra"}
                                            ,{title:"Output_Entity" , width:10 ,input_data:"{'entity':['tagdate','tagloc','tagmenu']}", ex:"display entity"}
                                            ,{title:"output_data" , width:10 ,input_data:"주문이 완료되 었습니다", ex:"display sentence"}
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

            let rowNet = this.state.NN_TableNet

            colData.push(<td key={k++} style={{ "width":"20%"}}> {row["title"]} </td>)

            if(rows == 0){
                let option = []
                for(let op in rowNet){
                    option.push(<option key={k++} value={rowNet[op]["nn_id"]}>{rowNet[op]["nn_id"]}</option>)
                }   
                colData.push(<td key={k++}>
                                            <div>
                                            <select ref={"sel"+k} 
                                                   id={k} 

                                                   style={{ "textAlign":"center", "width":"100%", "fontWeight":"bold", "color":this.state.color}}
                                                   rowSpan={1}>
                                               {option}
                                            </select>
                                            </div>
                                        </td>)
            }else{
                colData.push(<td key={k++} > < input type = {"string"} style={{"textAlign":"center", "width":"100%"}} 
                                                        defaultValue = {row["input_data"]}
                                                        maxLength = {row["width"]}  />  </td>)
            }
            
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
                    <div><img src="./templates/images/chatbot_ico.png" width="128" height="128"></img></div>
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




