import React from 'react'
import ReportRepository from './../repositories/ReportRepository'
import Api from './../utils/Api'

import {ComposedChart, Line, Area, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer}  from 'recharts';

export default class NN_InfoDetailBarLine extends React.Component {
    constructor(props, context) {
        super(props);
        this.state = {
            NN_DataPre:null,
            NN_Data:null,
            NN_Labels:[],
            lineChartLabels:null,
            lineChartData:null,
            barCnt : 5,
            color:['#ef867a','#69f3cf','#cf7425','#995f7c','#68299f','#a37178','#8893a4','f2584f','#469da9','#5dda73'] 
        };
    }
    /////////////////////////////////////////////////////////////////////////////////////////
    // Search Function "#ff8022","#ffcf3b","#47de8a","#999966","#33cccc","#ff66ff","#F85F73"
    //'#ef867a','#69f3cf',#cf7425','','','','','','',''
    /////////////////////////////////////////////////////////////////////////////////////////
    componentDidMount() {
    }
    /////////////////////////////////////////////////////////////////////////////////////////
    // Version Batch Bar Chart
    /////////////////////////////////////////////////////////////////////////////////////////   
    setLineChartData(lineData){
      function pad(n, width) {
        n = n + '';
        return n.length >= width ? n : new Array(width - n.length + 1).join('0') + n;
      }

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

      let best = lineData['best']
      let bygen = lineData['bygen']

      let data = []
      
      
      for(let rows in bygen){
        let subData = {}
        let row = bygen[rows]
        let rowSort = sortData(row, "acc")
        let avg = 0
        let maxcnt =1
        subData['name'] = 'Gen'+pad(rows*1+1,3)
        for(let i=rowSort.length-1 ; i>=0 ; i--){
          subData[pad(maxcnt,2)] = (rowSort[i]['acc']*100).toFixed(2)*1
          avg = avg + (rowSort[i]['acc']*100).toFixed(2)*1
          if(this.state.NN_Labels.indexOf(pad(maxcnt,2)) == -1){
            this.state.NN_Labels.push(pad(maxcnt,2))
          }
          
          if(maxcnt >= this.state.barCnt){
            break
          }
          maxcnt += 1
        }

        subData['avg'] = (avg/row.length).toFixed(2)*1
        data.push(subData)

      }

      this.state.NN_Labels = this.state.NN_Labels.sort()
      this.setState({ NN_Data: data })
    }

    lineChartOnClick(value){//Chart의 세부 카테고리 정보를 보여준다.
    }


    render() {
        let k = 1
        /////////////////////////////////////////////////////////////////////////////////////////
        // Common Function
        /////////////////////////////////////////////////////////////////////////////////////////
        function getRandomColor() {
          var letters = '0123456789ABCDEF';
          var color = '#';
          for (var i = 0; i < 6; i++) {
            color += letters[Math.floor(Math.random() * 16)];
          }
          return color;
        }

        let lineData = this.props.NN_Data

        if(lineData != null && this.state.NN_Data == null){
          this.setLineChartData(lineData)
        }

        let lineChart = [];
        let color = ""
        for(let i in this.state.NN_Labels){
          if(this.state.color.length > i){
            color = this.state.color[i]
          }else{
            color = getRandomColor()
          }
          lineChart.push(    <Bar key={k++} dataKey={this.state.NN_Labels[i]} barSize={20} fill={color}/>)
        }
        if(this.state.NN_Labels.length == 0){
          lineChart.push(    <Bar key={k++} dataKey={"1"} barSize={20} fill={color}/>)
        }
        lineChart.push(    <Line key={k++}  dataKey='avg' type='monotone' stroke='#ff7300'/>)

        return (  

            <section>
            <div className="container paddingT10">

            <table ref="linechart_rechart" className="chart">
                        <tr>
                        <td>
              <ResponsiveContainer key={k++} width='100%' height={200}>
                <ComposedChart key={k++} data={this.state.NN_Data} margin={{top: 20, right: 20, bottom: 20, left: 20}}>
                  <XAxis key={k++} dataKey="name"/>
                  <YAxis key={k++} />
                  <Tooltip key={k++} />
                  <Legend key={k++} />
                  <CartesianGrid key={k++} stroke='#f5f5f5'/>
                  {lineChart}
               </ComposedChart >
              </ResponsiveContainer >
              </td>
              </tr>
              </table>


               
            </div>
            </section>
        )
    }
}

