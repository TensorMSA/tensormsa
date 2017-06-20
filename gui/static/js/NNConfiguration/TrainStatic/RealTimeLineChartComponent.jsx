import React from 'react'
import * as d3 from "d3"
import dc from 'dc'
import crossfilter from 'crossfilter'
import '../../../node_modules/dc/dc.css'

export default class RealTimeLineChartComponent extends React.Component {
    constructor(props) {
        super(props);
    }
    
    componentDidMount() { //after DOM make D3 Chart
        this.createChart();
    }

    componentDidUpdate() { 
        this.createChart();
    }

    createChart(){
            let startTime = 0;
            let cf = crossfilter([{date: startTime, lossValue: 0}]);
            let lossData = this.props.currData;

            AddData();
            
            let timeDimension = cf.dimension(function(d){ return d.date; });
            let totalGroup = timeDimension.group().reduceSum(function(d){ return d.lossValue; });
            
            let lineChart = dc.lineChart("#loss","lossChart")
                .brushOn(false)
                .width(500)
                .height(220)
                .elasticY(true)
                .x(d3.scale.linear().domain([0, lossData.length-1]))
                .dimension(timeDimension)
                .group(totalGroup);
                
               let loop = setInterval(function(){
                AddData();
                    if(lossData.length == startTime){
                        clearInterval(loop);
                    }
                lineChart.x(d3.scale.linear().domain([0, lossData.length-1]));
                lineChart.render("lossChart");
                }, 1000);
                /*
                lossData.forEach(function(element) {
                    AddData();
                    lineChart.x(d3.scale.linear().domain([0, lossData.length-1]));
                    lineChart.render("lossChart");
                });
                */
            function AddData(){
                let lossValue = lossData[startTime];
                cf.add( [{date: startTime++, lossValue: lossValue}]);  
            }
    }

    render() {
        return (   
                    <article>
                        <div id="loss"></div>
                    </article>
        )
    }
}