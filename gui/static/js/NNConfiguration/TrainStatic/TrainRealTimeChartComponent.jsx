import React from 'react'
import * as d3 from "d3"

export default class TrainRealTimeChartComponent extends React.Component {
    constructor(props) {
        super(props);
        this.svg = null;
        this.x = null;
        this.y = null;
        this.line = null;
        this.axis = null;
        this.paths = null;
        this.dataLen = 0;
        this.groups = null;
        this.group = null;
    }

    componentDidMount() { //after DOM make D3 Chart
        console.log("history");
        console.log(this.props.historyData);
                console.log("currData");
        console.log(this.props.currData);

        this.createChart(this.props.historyData, this.props.currData);
    }

    componentDidUpdate() { //after DOM make D3 Chart
                console.log("history2");
        console.log(this.props.historyData);
                console.log("currData2");
        this.createChart(this.props.historyData, this.props.currData);
    }

    createChart(historyData, currData){
        var historyData = historyData,
            currData = currData,
            repeatTime =  repeatTime,
            limit = 0,
            count = 0,
            width = 500,
            height = 150,
            duration = 100,
            maxY = 0

        if(currData.length > 0){
            maxY = currData.reduce(function(previous, current){
                return previous > current ? previous:current;
            })
        }else{
            return false;
        }
        

        if(this.svg){

            for (var name in this.groups) {
                this.group = this.groups[name]
                this.group.path = this.paths.append('path')
                    .data([this.group.data])
                    .attr('class', name + ' group')
                    .style('stroke', this.group.color)
            }
 
            
            tick(historyData, currData, this.groups, this.group, this.line, this.x, this.y, this.axis, this.paths, maxY)
            return false;
        }


        this.groups = {
            current: {
                value: 0,
                color: 'green',
                data: d3.range(limit).map(function() {
                    return 0
                })
            }
        }

        this.x = d3.time.scale()
            .domain([currData.length -100  > 0 ? currData.length -100:0, currData.length])
            .range([0, width])

        this.y = d3.scale.linear()
            .domain([0, maxY])
            .range([height, 0])

        this.line = d3.svg.line()
            .interpolate('basis')
            .x(function(d, i) {
                //count = count + 1
                return x(i)
            })
            .y(function(d) {
                return y(d)
            })

        var x = this.x 
        var y = this.y

        this.svg = d3.select('.graph').append('svg')
        .attr('class', 'chart')
        .attr('width', width)
        .attr('height', height + 100)
        

        this.axis = this.svg.append('g')
            .attr('class', 'x axis')
            .attr('transform', 'translate(0,' + height + ')')
            .call(x.axis = d3.svg.axis().scale(x).orient('bottom'))

        this.paths = this.svg.append('g')
        
        for (var name in this.groups) {
            this.group = this.groups[name]
            this.group.path = this.paths.append('path')
                .data([this.group.data])
                .attr('id', 'loss_line')
                .attr('class', name + ' group')
                .style('stroke', this.group.color)
        }

        function tick(historyData, currData, groups, group, line, x, y, axis, paths, maxY) {
            //deprecated : chaged to replace all graph at once 
            //var appendData = currData.slice(historyData.length, currData.length)

            // Add new values
            for (var name in groups) {
                var group = groups[name]
                group.data = []
                for(var val of currData)
                {
                    group.data.push(val)
                }  

                group.path = paths.append('path')
                .data([group.data])
                .attr('id', 'loss_line')
                .attr('class', name + ' group')
                .style('stroke', group.color)

                // remove old one
                d3.select("#loss_line").remove();

                // draw new one 
                group.path.attr('d', line)  
            }

            // Shift domain
            x.domain([currData.length -100  > 0 ? currData.length -100:0, currData.length]);
            y.domain([0, maxY]);
            // Slide x-axis left
            axis.transition()
                .duration(duration)
                .ease('linear')
                .call(x.axis)

        }
        tick(historyData, currData, this.groups, this.group, this.line, this.x, this.y, this.axis, this.paths, maxY)
    }

    render() {
        const css = `
        .graph .axis {
            stroke-width: 1;
        }

        .graph .axis .tick line {
            stroke: black;
        }

        .graph .axis .tick text {
            fill: black;
            font-size: 0.7em;
        }

        .graph .axis .domain {
            fill: none;
            stroke: black;
        }

        .graph .group {
            fill: none;
            stroke: black;
            stroke-width: 1.5;
        }`
        
        return (   

                    <article>
                      <style>{css}</style>
                        <div className="graph"></div>
                    </article>
        )
    }
}