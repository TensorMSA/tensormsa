import React from 'react';
import Api from './../utils/Api'
import Modal from 'react-modal';
import { BootstrapTable, TableHeaderColumn } from 'react-bootstrap-table';
import ReportRepository from './../repositories/ReportRepository'
import EnvConstants from './../constants/EnvConstants';
import ReactTimeout from 'react-timeout'

export default class NN_InfoMoniteringDetail extends React.Component {
    constructor(props, context) {
        super(props);
        this.state = {
            tableData:null,
            NN_TableData:null,
            NN_TableDataLog:"",
            line:5000,
            nn_color:"#14c0f2",
            smove_flag : "N",
            on: false,
            interval:null,
            timerText:"Timer Off",
            timerColor:"gray"
        };
        this.searchData= this.searchData.bind(this);
    }

    componentDidMount(){
        this.getTaskLogInfo(this.props.nn_id);// 화면에 들어 올때 검색을 해준다.
    }

    componentDidUpdate(){
        if(this.state.smove_flag == "Y"){
            // this.refs.logta.focus()
            let ta = this.refs.logta
            if(ta != undefined){
                ta.scrollTop = ta.scrollHeight 

                // console.log(ta.scrollTop + ta.offsetHeight)
                // console.log(ta.scrollHeight)
            }
        }
    }

    componentWillUnmount() {
        clearInterval(this.state.interval)
    }

    getTaskLogInfo(file) {
        file = "log.txt"
        this.props.reportRepository.getMoniteringInfo('log', file, this.state.line).then((tableData) => {
            if(tableData[0] != undefined){
                // if(tableData[0]['line'] == null || tableData[0]['line'] == undefined){
                //     this.state.line = 0
                // }else{
                //     this.state.line = tableData[0]['line']
                // }
                let log = this.state.NN_TableDataLog + tableData[0]['log']
                this.setState({ NN_TableDataLog: log})//조회한 것을 화면에 반영한다.
            }
        });   
    }

    searchData() {
        this.getTaskLogInfo(this.props.nn_id)  
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

    toggle(){
        this.searchData()
    }

    timerClick(){
        if(this.state.on == false){
            this.state.on = true
            this.setState({ timerText: "Timer On"})
            this.setState({ timerColor: "white"})
            this.state.interval = setInterval(() => this.searchData(), 3000) // call the `toggle` function after 5000ms 
        }else{
            this.state.on = false
            this.setState({ timerText: "Timer Off"})
            this.setState({ timerColor: "gray"})
            clearInterval(this.state.interval)
        }
    }

    render() {
        let k = 1

        let ta = this.refs.logta
        if(ta != undefined){
            if(ta.scrollTop + ta.offsetHeight + ta.offsetHeight >= ta.scrollHeight){
                this.state.smove_flag = "Y"
            }else{
                this.state.smove_flag = "N"
            }
        }
        
        return (
            <section>
                <h1 className="hidden">tensor MSA main table</h1>
                <div className="container paddingT10">
                    <div className="tblBtnArea">
                        <button type="button" className="addnew" style={{"marginRight":"5px", "color":this.state.timerColor}} 
                                                onClick={() => this.timerClick()}>{this.state.timerText}</button>
                        <button type="button" className="addnew" onClick={() => this.searchData()} >Search</button>
                                      
                    
                
                    </div>
                    <h1 className="bullet"> Celery Task Log </h1>
                    <div style={{ "overflow":"auto", "height":760}} >
                        
                            <textarea key={k++} ref="textarea" style={{"width":"95%", "height":"95%"}}  
                                        name="logta" 
                                        ref="logta" 
                                        value = {this.state.NN_TableDataLog} 
                                        />

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

