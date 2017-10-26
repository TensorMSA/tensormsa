import React from 'react';
import Api from './../utils/Api'
import Modal from 'react-modal';
import { BootstrapTable, TableHeaderColumn } from 'react-bootstrap-table';
import ReportRepository from './../repositories/ReportRepository'
import EnvConstants from './../constants/EnvConstants';

export default class NN_InfoSetup extends React.Component {
    constructor(props, context) {
        super(props);
        this.state = {
            tableData:null,
            NN_TableData:null,
            NN_TableColArr:[ {index:0, id:"sel",            name:"Sel"}
                            ,{index:1, id:"biz_cate",       name:"Category"}
                            ,{index:2, id:"biz_sub_cate",   name:"SubCategory"}
                            ,{index:3, id:"nn_title",       name:"Title"}
                            ]
        };
    }

    componentDidMount(){
        this.getCommonInfo("all");// 화면에 들어 올때 검색을 해준다.
    }

    getCommonInfo(params) {
    }

    searchCommonNNInfo() {
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

    render() {
        let k = 1
        // Data sort
        function sortByKey(array, key) {
            return array.sort(function(a, b) {
                var x = a[key]; var y = b[key];
                return ((x < y) ? -1 : ((x > y) ? 1 : 0));
            });
        }

        function sortData(data, id){
            let nnInfoNewList = [];
            if (data != null) {
                for (var i in data) {
                    nnInfoNewList[i] = data[i];
                }
            }

            nnInfoNewList = sortByKey(nnInfoNewList, id);
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

        let tableHeader = makeHeader(this.state.NN_TableColArr)


        return (
            <section>
                <h1 className="hidden">tensor MSA setup table</h1>
                <div className="container paddingT10">


                    <div style={{ "overflow":"auto", "height":830}}>
                        <h1 className="bullet"> Setup List </h1>
                        <table className="table detail" ref= 'master2' >
                            
                        </table>
                    </div>

                </div>
            </section>
        );
    }
}

NN_InfoSetup.defaultProps = {
    reportRepository: new ReportRepository(new Api())
};

