import React from 'react';
import Api from './../utils/Api'
import Modal from 'react-modal';
import { BootstrapTable, TableHeaderColumn } from 'react-bootstrap-table';
import ReportRepository from './../repositories/ReportRepository'
import EnvConstants from './../constants/EnvConstants';


export default class NN_InfoMonitering extends React.Component {
    constructor(props, context) {
        super(props);
        this.state = {
            tableData:null,
            NN_TableData:null,
            NN_TableDataLog:null,
            line:0,
            nn_color:"#14c0f2",
            NN_TableColArr:[ {index:0, id:"uuid",             name:"TaskID"}
                            ,{index:1, id:"nn_id",          name:"ID"}
                            ,{index:2, id:"nn_wf_ver_id",   name:"Ver"}
                            ,{index:3, id:"state",         name:"Status"}
                            ,{index:4, id:"received",       name:"Received"}
                            ,{index:5, id:"started",        name:"Started"}     
                            ,{index:6, id:"successed",        name:"Successed"}                          
                            ]
        };
    }

    componentDidMount(){
        this.props.setActiveItem('init', null, null, null, null, null, null, null);
        let nn_id = ''
        if (this.props.nn_id == undefined){
            nn_id = 'all'
        }else{
            nn_id = this.props.nn_id
        }
        this.getTaskInfo("all", nn_id);// 화면에 들어 올때 검색을 해준다.
    }

    getTaskInfo(params) {
        this.props.reportRepository.getMoniteringInfo('all', 'all', 'all', 'all').then((tableData) => {
            this.setState({ NN_TableData: tableData})//조회한 것을 화면에 반영한다.
        });   
    }

    searchData() {
        this.getTaskInfo("all")
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

    handleClick(row){// Table Cell Clcik and Call log
        // row["uuid"]
        // this.getTaskLogInfo('log.txt', this.state.line)
        let altuuid = row["nn_id"].trim()+'/'+row["nn_wf_ver_id"].trim()+'/'+row["uuid"]+'.log'
        this.props.setActiveItem(altuuid, null, null, null, null, null, null, null);
        return this.props.getHeaderEvent(34); //call Net Info 
    }

    render() {
        let k = 1
        // Data sort
        function sortByKey(array, key) {
            return array.sort(function(a, b) {
                var x = a[key]; var y = b[key];
                return ((x < y) ? -1 : ((x > y) ? 1 : 0));
            });
        }

        function sortByKeyDesc(array, key) {
            return array.sort(function(a, b) {
                var x = a[key]; var y = b[key];
                return ((x > y) ? -1 : ((x < y) ? 1 : 0));
            });
        }

        function sortData(data, id){
            let nnInfoNewList = [];
            if (data != null) {
                for (var i in data) {
                    nnInfoNewList[i] = data[i];
                }
            }

            nnInfoNewList = sortByKeyDesc(nnInfoNewList, id);
            return nnInfoNewList
        }
        
        // Make header
        function makeHeader(data){
            let headerData = []
            for(let i in data){
                headerData.push(<th key={k++} style={{"textAlign":"center"}} >{data[i].name}</th>)
            }
            let tableHeader = []; //make header
            tableHeader.push(<tr key={k++} >{headerData}</tr>)
            return tableHeader
        }

        this.state.NN_TableData = sortData(this.state.NN_TableData, "receivedtime")
        let tableHeader = makeHeader(this.state.NN_TableColArr)

        //Network Select Data
        let tableData = []; // make tabledata

        for(let rows in this.state.NN_TableData){
            let colData = [];
            let row = this.state.NN_TableData[rows]
            if(this.props.nn_id != undefined && this.props.nn_id != row["nn_id"]){
                continue
            }
            
            colData.push(<td key={k++} alt = {row["uuid"]} 
                                style ={{"color":this.state.nn_color, "cursor":"pointer", "fontWeight":"bold"}}
                                onClick={() => this.handleClick(row) } > {row["uuid"]} </td>)   
            colData.push(<td key={k++} alt = {row["uuid"]} > {row["nn_id"]} </td>) 
            colData.push(<td key={k++} alt = {row["uuid"]} > {row["nn_wf_ver_id"]}  </td>) 
            colData.push(<td key={k++} alt = {row["uuid"]} > {row["state"]} </td>) 
            colData.push(<td key={k++} alt = {row["uuid"]} > {row["received"]} </td>) 
            colData.push(<td key={k++} alt = {row["uuid"]} > {row["started"]} </td>) 
            colData.push(<td key={k++} alt = {row["uuid"]} > {row["succeeded"]} </td>) 

            tableData.push(<tr key={k++}>{colData}</tr>)
        }


        let nnInfoListTable = []
        nnInfoListTable.push(<thead ref='thead' key={k++} className="center">{tableHeader}</thead>)
        nnInfoListTable.push(<tbody ref='tbody' key={k++} className="center" >{tableData}</tbody>)

        return (
            <section>
                <h1 className="hidden">tensor MSA main table</h1>
                <div className="container paddingT10">
                    <div className="tblBtnArea">
                        <button type="button" className="addnew" style={{"marginRight":"5px"}} onClick={() => this.searchData()} >Search</button>
                    </div>
                    <div style={{ "overflow":"auto", "height":800}} >
                        <h1 className="bullet"> Celery Task List </h1>
                        <table className="table detail" ref= 'task' >
                            {nnInfoListTable}
                        </table>
                    </div>
                    <br/>



                </div>
            </section>
        );
    }
}

NN_InfoMonitering.defaultProps = {
    reportRepository: new ReportRepository(new Api())
};

