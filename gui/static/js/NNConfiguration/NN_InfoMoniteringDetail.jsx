import React from 'react';
import Api from './../utils/Api'
import Modal from 'react-modal';
import { BootstrapTable, TableHeaderColumn } from 'react-bootstrap-table';
import ReportRepository from './../repositories/ReportRepository'
import EnvConstants from './../constants/EnvConstants';


export default class NN_InfoMoniteringDetail extends React.Component {
    constructor(props, context) {
        super(props);
        this.state = {
            tableData:null,
            NN_TableData:null,
            NN_TableDataLog:null,
            line:0,
            nn_color:"#14c0f2"
        };
    }

    componentDidMount(){
        this.getTaskLogInfo(this.props.nn_id, 0);// 화면에 들어 올때 검색을 해준다.
    }

    getTaskLogInfo(file, line) {
        file = "log.txt"
        this.props.reportRepository.getMoniteringInfo('log', file, line).then((tableData) => {
            if(tableData[0] != undefined){
                if(tableData[0]['line'] == null || tableData[0]['line'] == undefined){
                    this.state.line = 0
                }else{
                    this.state.line = tableData[0]['line']
                }
                let log = this.state.NN_TableDataLog + tableData[0]['log']
                this.setState({ NN_TableDataLog: log})//조회한 것을 화면에 반영한다.
            }
        });   
    }

    searchData() {
        // this.getTaskInfo("all")
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
    }

    render() {
        let k = 1


        

        return (
            <section>
                <h1 className="hidden">tensor MSA main table</h1>
                <div className="container paddingT10">
                    <div className="tblBtnArea">
                        <button type="button" className="addnew" style={{"marginRight":"5px"}} onClick={() => this.searchData()} >Search</button>
                    </div>
                    <div style={{ "overflow":"auto", "height":830}} >
                        <h1 className="bullet"> Celery Task Log </h1>
                        

                    </div>
                    <br/>



                </div>
            </section>
        );
    }
}

NN_InfoMoniteringDetail.defaultProps = {
    reportRepository: new ReportRepository(new Api())
};

