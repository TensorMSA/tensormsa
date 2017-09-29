import React from 'react'
import ReportRepository from './../repositories/ReportRepository'
import Api from './../utils/Api'

import {LineChart, Line, Area, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer}  from 'recharts';

export default class NN_InfoDetailLine extends React.Component {
    constructor(props, context) {
        super(props);
        this.state = {
            NN_DataPre:null,
            NN_Data:null,
            NN_Labels:[],
            lineChartLabels:null,
            lineChartData:null,
            accColor:"#14c0f2",
            lossColor:"#ff8022"
        };
    }
    /////////////////////////////////////////////////////////////////////////////////////////
    // Search Function
    /////////////////////////////////////////////////////////////////////////////////////////
    componentDidMount() {
    }
    /////////////////////////////////////////////////////////////////////////////////////////
    // Version Batch Bar Chart
    /////////////////////////////////////////////////////////////////////////////////////////   
    setLineChartData(lineData){
      let data = null
      if(lineData['train_acc_info'] != null && lineData['train_loss_info'] != null){
        let acc = lineData['train_acc_info']['acc']
        let loss = lineData['train_loss_info']['loss']
        data = []
        for(let rows in acc){
          let key = rows*1+1
          let accrow = acc[rows]*1
          let lossrow = loss[rows]*1
          data.push({name: key, acc: accrow, loss: lossrow})
        }
      }
      

      this.state.NN_Data = data
      // this.setState({NN_Data: data})
    }

    lineChartOnClick(value){//Chart의 세부 카테고리 정보를 보여준다.
    }


    render() {
        let k = 1

        const CustomizedLabel = React.createClass({
          render () {
            const {x, y, stroke, value} = this.props;
            
            return <text key={k++} x={x} y={y} dy={-4} fill={stroke} fontSize={10} textAnchor="middle">{value}</text>
          }
        });
        const CustomizedAxisTick = React.createClass({
          render () {
            const {x, y, stroke, payload} = this.props;
            
            return (
              <g transform={`translate(${x},${y})`}>
                <text key={k++} x={0} y={0} dy={16} textAnchor="end" fill="#666" transform="rotate(-35)">{payload.value}</text>
              </g>
            );
          }
        });
        /////////////////////////////////////////////////////////////////////////////////////////
        // Common Function
        /////////////////////////////////////////////////////////////////////////////////////////
        let lineData = this.props.NN_Data

        if(lineData != null && this.state.NN_DataPre == this.state.NN_Data){
          this.setLineChartData(lineData)
        }

        this.state.NN_DataPre = this.state.NN_Data

        // let lineChartacc = [];

        // lineChartacc.push(    <Line key={k++} type="monotone" dataKey="acc" 
        //                         stroke={this.state.accColor} label={<CustomizedLabel />}/> )

        // let lineChartloss = [];

        // lineChartloss.push(    <Line key={k++} type="monotone" dataKey="loss" 
        //                         stroke={this.state.lossColor} label={<CustomizedLabel />}/> )

        return (  

            <section>
            <div className="container paddingT10">

            <table ref="linechart_rechart" className="chart">
                        <tr>
                        <td>
              <ResponsiveContainer key={k++} width='100%' height={200}>
                <LineChart key={k++} data={this.state.NN_Data}
                      margin={{top: 20, right: 30, left: 20, bottom: 10}}>
                 <XAxis key={k++} dataKey="name" height={60} tick={<CustomizedAxisTick/>}/>
                 <YAxis key={k++} />
                 <CartesianGrid key={k++} strokeDasharray="3 3"/>
                 <Tooltip key={k++} />
                 <Legend key={k++} />
                 <Line key={k++} type="monotone" dataKey="acc" 
                                 stroke={this.state.accColor} />
                </LineChart>
              </ResponsiveContainer >
              </td>

              <td>
              <ResponsiveContainer key={k++} width='100%' height={200}>
                <LineChart key={k++} data={this.state.NN_Data}
                      margin={{top: 20, right: 30, left: 20, bottom: 10}}>
                 <XAxis key={k++} dataKey="name" height={60} tick={<CustomizedAxisTick/>}/>
                 <YAxis key={k++} />
                 <CartesianGrid key={k++} strokeDasharray="3 3"/>
                 <Tooltip key={k++} />
                 <Legend key={k++} />
                 <Line key={k++} type="monotone" dataKey="loss" 
                                 stroke={this.state.lossColor} />
                </LineChart>
              </ResponsiveContainer >
              </td>

              </tr>
              </table>


               
            </div>
            </section>
        )
    }
}

