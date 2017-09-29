import React from 'react'
import ReportRepository from './../repositories/ReportRepository'
import Api from './../utils/Api'

import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import {Pie} from 'react-chartjs-2';


export default class NN_InfoDetailStackBar extends React.Component {
    constructor(props, context) {
        super(props);
        this.state = {
            NN_DataPre:null,
            NN_Data:null,
            NN_Labels:null,
            barChartLabels:null,
            barChartData:null,
            pieChartData:{
                                labels: [
                                    'Blank'
                                ],
                                datasets: [{
                                    data: [100],
                                    backgroundColor: [
                                    '#FF6384'
                                    ],
                                    hoverBackgroundColor: [
                                    '#FF6384'
                                    ]
                                }]
                            },
            trueColor:"#14c0f2",
            falseColor:"#ff8022",
            pieMainColor:"#14c0f2",
            pieSubColor:["#ff4622","#ff8022","#ffab27","#ffcd21","#ffed87","#ff66ff","#F85F73"] 
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
    setBatchBarChartData(batchData){
      let nndata= []
      let labels = ""
      let predicts = ""
      if(batchData != null){
        labels = batchData["labels"]
        predicts = batchData["predicts"]
      }
      
      for(let j=0 ; j < labels.length ; j++){
        let ttt = 0
        let fff = 0
        for(let k=0 ; k < predicts[j].length ; k++){//총 합을 구하고 맞춘 값과 못 맞춘 값을 나누어야 한다.
            if(j == k){
                ttt = predicts[j][k]
            }else{
                fff += predicts[j][k]
            }
        }
        nndata.push({name: labels[j], trueData: ttt, falseData: fff, predicts:predicts[j]})
      }

      this.state.NN_Labels = labels
      this.state.NN_Data = nndata 
      // this.setState({ NN_Data: nndata })
      // 최초 Pie 차트를 보여준다.
      if(batchData == null){
        labels = ["blank"]
      }
      this.stackBarChartOnClick(labels[0])
    }

    stackBarChartOnClick(value){//Chart의 세부 카테고리 정보를 보여준다.
        function sortByKey(array, key) {// Data sort key
            return array.sort(function(a, b) {
                var x = a[key]; var y = b[key];
                return ((x < y) ? -1 : ((x > y) ? 1 : 0));
            });
        }

        if(value != null && value.activeLabel != undefined){
            value = value.activeLabel
        }

        let labels = this.state.NN_Labels
        let batchData = this.state.NN_Data

        if(batchData == null){
          return null
        }
        
        let label = []
        let data = []

        let plabel = []
        let pdata = []
        let pcolor = []
        for(let j=0 ; j < batchData.length ; j++){
            if(value == batchData[j]["name"]){
                let predicts = batchData[j]["predicts"]
                for(let k=0 ; k < predicts.length ; k++){
                    if(predicts[k] > 0){// 값이 있는 경우만을 표기 한다.
                        if(value == labels[k]){
                            plabel.push(labels[k])
                            pdata.push(predicts[k])
                            pcolor.push(this.state.pieMainColor)
                        }else{
                          label.push(labels[k])
                          data.push(predicts[k])
                        }
                    }
                }
            }
        }

        //Sort 
        let top = 3
        let sData = []
        for(let i in label){
          let ssdata = {key:label[i], val:data[i]}
          sData.push(ssdata)
        }

        let sortData = sortByKey(sData, "val")
        let j=0
        let etc = 0
        for(let i = sortData.length-1 ; i >= 0 ; i--){
          if(i >= sortData.length-top){
            plabel.push(sortData[i]["key"])
            pdata.push(sortData[i]["val"])
            pcolor.push(this.state.pieSubColor[j])
            j += 1
          }else{
            etc += sortData[i]["val"]
          }
        }
        if(etc > 0){
          plabel.push("etc")
          pdata.push(etc)
          pcolor.push(this.state.pieSubColor[j])
        }

        let pieChartData = {
            labels: plabel,
            datasets: [{
                data: pdata,
                backgroundColor: pcolor,
                hoverBackgroundColor: pcolor
            }]
        };

        this.setState({ pieChartData: pieChartData })

    }


    render() {
        /////////////////////////////////////////////////////////////////////////////////////////
        // Common Function
        /////////////////////////////////////////////////////////////////////////////////////////

        let batchData = this.props.NN_Data

        if(batchData != this.state.NN_DataPre){
          this.setBatchBarChartData(batchData)
        }


        this.state.NN_DataPre = batchData
        
        const CustomTooltip1  = React.createClass({// Batch Bar Chart Tooltip
            getIntroOfPage(label) {
                return label
            },

            render() {
                const { active } = this.props;

                if (active) {
                  const { payload, label } = this.props;
                  let avg = 0
                  let tot = 0
                  let payloadValue0 = 0
                  let payloadValue1 = 0
                  let payloadName0 = 0
                  let payloadName1 = 0
                  if(payload != null){
                    payloadValue0 = payload[0]["value"]
                    payloadValue1 = payload[1]["value"]
                    payloadName0 = payload[0]["name"]
                    payloadName1 = payload[1]["name"]
                    tot = payloadValue0 + payloadValue1
                  }

                  if(tot != 0){
                    avg = Math.round(payloadValue0 / tot *100)+"%"
                  }

                  return (
                    <div className="custom-tooltip" style={{"backgroundColor":"white"}}>

                            <p style={{"color":"black"}}>{this.getIntroOfPage(label)}</p>
                   
                            <p style={{"color":"black"}}>
                                {" "+this.getIntroOfPage(payloadName0+" : "+payloadValue0)+" "}</p>
                     
                            <p style={{"color":"black"}}>
                                {" "+this.getIntroOfPage(payloadName1+" : "+payloadValue1)+" "}</p>
                        
                            <p style={{"color":"black"}}>
                                {" "+this.getIntroOfPage("Acc : "+avg)+" "}</p>
                 
                    </div>
                  );
                }

            return null;
          }
        });
                             
        return (  

            <section>
            <div className="container paddingT10">

                
                    <table ref="barchart_rechart" className="chart">
                        <tr>
                        <td width="60%">
                            <ResponsiveContainer width='100%' height={200}>
                                <BarChart  data={this.state.NN_Data} ref="tBarChart"
                                             onClick={this.stackBarChartOnClick.bind(this)}>
                                       <XAxis dataKey="name"/>
                                       <YAxis/>
                                       <CartesianGrid strokeDasharray="3 3"/>
                                       <Tooltip content={ <CustomTooltip1 /> }  />
                                       <Legend />
                                       <Bar stackId="a" dataKey="trueData" fill={this.state.trueColor} />
                                       <Bar stackId="a" dataKey="falseData" fill={this.state.falseColor} />
                                      </BarChart>
                            </ResponsiveContainer>
                        </td>
                        <td width="40%">
                            <ResponsiveContainer width='80%' height={200}>
                                <Pie data={this.state.pieChartData} options={{animateRotate: true}} />
                            </ResponsiveContainer>  
                        </td>
                        </tr>
                </table>  

               
            </div>
            </section>
        )
    }
}

