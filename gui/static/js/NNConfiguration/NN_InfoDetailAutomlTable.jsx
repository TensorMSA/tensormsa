import React from 'react'
import ReportRepository from './../repositories/ReportRepository'
import Api from './../utils/Api'

import {ComposedChart, Line, Area, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer}  from 'recharts';

export default class NN_InfoDetailAutomlTable extends React.Component {
    constructor(props, context) {
        super(props);
        this.state = {
            NN_DataPre:null,
            NN_Data:null,
            NN_TableColArr0:[    {index:0,      id:"generation"     , name:"Generation"}
                                ,{index:1,      id:"population"     , name:"Population"}
                                ,{index:2,      id:"survive"        , name:"Survive"}
                            ],
            NN_TableColArr1:[    {index:0,      id:"generation"   , name:"Generation"}
                                ,{index:1,      id:"nn_wf_ver_id" , name:"Network Version"}
                                ,{index:2,      id:"acc"          , name:"Acc"}
                                ,{index:3,      id:"survive"      , name:"Survive"}
                            ],
            NN_TableColArr2:[    {index:0,      id:"depth"        , name:"Depth"}
                                ,{index:1,      id:"generation"   , name:"Generation"}
                                ,{index:2,      id:"nn_wf_ver_id" , name:"Network Version"}
                                ,{index:3,      id:"acc"          , name:"Acc"}
                                ,{index:4,      id:"survive"      , name:"Survive"}
                            ]
        };
    }

    componentDidMount() {
    }


    render() {
        let k = 1
        let yImg = "./images/ic_state_y.png"
        let nImg = "./images/ic_state_n.png"
        /////////////////////////////////////////////////////////////////////////////////////////
        // Common Function
        /////////////////////////////////////////////////////////////////////////////////////////
        function sortByKey(array, key) {// Data sort key
            return array.sort(function(a, b) {
                var x = a[key]; var y = b[key];
                return ((x < y) ? -1 : ((x > y) ? 1 : 0));
            });
        }

        function sortData(data, id){// Data sort
            let nnInfoNewList = [];
            if (data != null) {
                for (var i in data) {
                    nnInfoNewList[i] = data[i];
                }
            }

            nnInfoNewList = sortByKey(nnInfoNewList, id);
            return nnInfoNewList
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
        let lineData = this.props.NN_Data

        if(lineData != null && this.state.NN_Data == null){
          this.state.NN_Data = lineData
        }
        /////////////////////////////////////////////////////////////////////////////////////////
        // Genetation
        /////////////////////////////////////////////////////////////////////////////////////////
        let tableH = makeHeader(this.state.NN_TableColArr0)
        let tableD = []; // make tabledata
        let colD = [];
        colD.push(<td key={k++} > {this.props.NN_Auto['automl_runtime']["generation"]} </td>)
        colD.push(<td key={k++} > {this.props.NN_Auto['automl_runtime']["population"]} </td>)
        colD.push(<td key={k++} > {this.props.NN_Auto['automl_runtime']["survive"]} </td>)

        tableD.push(<tr key={k++}>{colD}</tr>)

        let tdTable = []
        tdTable.push(<thead ref='thead' key={k++} className="center">{tableH}</thead>)
        tdTable.push(<tbody ref='tbody' key={k++} className="center" >{tableD}</tbody>)
        /////////////////////////////////////////////////////////////////////////////////////////
        // Best
        /////////////////////////////////////////////////////////////////////////////////////////
        let tableHeader = makeHeader(this.state.NN_TableColArr1)

        let tableData = []; // make tabledata
        for(let rows in lineData['best']){
          let colData = [];
          let row = lineData['best'][rows]
          colData.push(<td key={k++} > {row["generation"]*1+1} </td>)
          colData.push(<td key={k++} > {row["nn_wf_ver_id"]} </td>)
          colData.push(<td key={k++} > {row["acc"]} </td>)
          if(row["survive"] == true){
            colData.push(<td key={k++} > <img src={yImg} /></td>)
          }else{
            colData.push(<td key={k++} > <img src={nImg} /></td>)
          }
          

          tableData.push(<tr key={k++}>{colData}</tr>)
        }

        let bestListTable = []
        bestListTable.push(<thead ref='thead' key={k++} className="center">{tableHeader}</thead>)
        bestListTable.push(<tbody ref='tbody' key={k++} className="center" >{tableData}</tbody>)
        /////////////////////////////////////////////////////////////////////////////////////////
        // Detail
        ////////////////////////////////////////////////////////////////////////////////////////
        let tableGHeader = makeHeader(this.state.NN_TableColArr2)

        let depth = 1
        let tableGData = []; // make tabledata
        for(let rows in lineData['bygen']){
          let row = lineData['bygen'][rows]
          for(let col in row){
            let colData = [];
            colData.push(<td key={k++} > {depth} </td>)
            colData.push(<td key={k++} > {row[col]["generation"]*1+1} </td>)
            colData.push(<td key={k++} > {row[col]["nn_wf_ver_id"]} </td>)
            colData.push(<td key={k++} > {row[col]["acc"]} </td>)
            if(row[col]["survive"] == true){
              colData.push(<td key={k++} > <img src={yImg} /></td>)
            }else{
              colData.push(<td key={k++} > <img src={nImg} /></td>)
            }
            

            tableGData.push(<tr key={k++}>{colData}</tr>)
            
          }
          let blankData = []
          blankData.push(<td key={k++} style={{"backgroundColor":"#f1f1f1"}} >  </td>)
          blankData.push(<td key={k++} style={{"backgroundColor":"#f1f1f1"}} >  </td>)
          blankData.push(<td key={k++} style={{"backgroundColor":"#f1f1f1"}} >  </td>)
          blankData.push(<td key={k++} style={{"backgroundColor":"#f1f1f1"}} >  </td>)
          blankData.push(<td key={k++} style={{"backgroundColor":"#f1f1f1"}} >  </td>)
          tableGData.push(<tr key={k++}>{blankData}</tr>)
          depth += 1
          
        }

        let bestListGTable = []
        bestListGTable.push(<thead ref='thead' key={k++} className="center">{tableGHeader}</thead>)
        bestListGTable.push(<tbody ref='tbody' key={k++} className="center" >{tableGData}</tbody>)

        return (  

            <section>
            <div className="container paddingT10">

            <h2> Auto ML Best</h2>
            <table className="table detail" ref= 'master1'  >
                    
                {tdTable}
            
            </table>
            
            <h2> Auto ML Best</h2>
            <table className="table detail" ref= 'master1'  >
                    
                {bestListTable}
            
            </table>
          
          <h2> Auto ML Generation</h2>
            <table className="table detail" ref= 'master2'  >
                    
                {bestListGTable}
            
            </table>


               
            </div>
            </section>
        )
    }
}

