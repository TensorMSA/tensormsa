import React from 'react'
import dc from 'dc'
import crossfilter from 'crossfilter'
import '../../node_modules/dc/dc.css'
import StepArrowComponent from './../NNLayout/common/StepArrowComponent'

export default class NN_PreProcessingComponent extends React.Component {
    constructor(props) {
        super(props);
        this.state = { 
                        spendData : [
                {Name: 'KSS', Spent: '$40', Year: 2011},
                {Name: 'KSW', Spent: '$10', Year: 2011},
                {Name: 'BJH', Spent: '$40', Year: 2011},
                {Name: 'KSS', Spent: '$70', Year: 2012},
                {Name: 'BJH', Spent: '$20', Year: 2012},
                {Name: 'BJH', Spent: '$50', Year: 2013},
                {Name: 'KSW', Spent: '$30', Year: 2013},
                {Name: 'KGH', Spent: '$30', Year: 2013},
                {Name: 'KSS', Spent: '$40', Year: 2011},
                {Name: 'KSW', Spent: '$10', Year: 2011},
                {Name: 'BJH', Spent: '$40', Year: 2011},
                {Name: 'KSS', Spent: '$70', Year: 2012},
                {Name: 'BJH', Spent: '$20', Year: 2012},
                {Name: 'BJH', Spent: '$50', Year: 2013},
                {Name: 'KSW', Spent: '$30', Year: 2013},
                {Name: 'KGH', Spent: '$30', Year: 2013}
            ],
            stepBack : 1,
            stepForward : 3
        }
    }

    componentDidMount() {
        this.createChart(this.state.spendData);
    }

    createChart(spendData){
        let yearRingChart   = dc.pieChart("#chart-ring-year"),
            spendHistChart  = dc.barChart("#chart-hist-spend"),
            spenderRowChart = dc.rowChart("#chart-row-spenders");
        var table = dc.dataTable('#table');
 
        spendData.forEach(function(d) {
            d.Spent = d.Spent.match(/\d+/)[0];
        });
        // set crossfilter
        var ndx = crossfilter(spendData),
            yearDim  = ndx.dimension(function(d) {return +d.Year;}),
            spendDim = ndx.dimension(function(d) {return Math.floor(d.Spent/10);}),
            nameDim  = ndx.dimension(function(d) {return d.Name;}),
            spendPerYear = yearDim.group().reduceSum(function(d) {return +d.Spent;}),
            spendPerName = nameDim.group().reduceSum(function(d) {return +d.Spent;}),
            spendHist    = spendDim.group().reduceCount();

        yearRingChart
            .width(200)
            .height(200)
            .dimension(yearDim)
            .group(spendPerYear)
            .innerRadius(40)
            .controlsUseVisibility(true);

        spendHistChart
            .dimension(spendDim)
            .group(spendHist)
            .x(d3.scale.linear().domain([0,10]))
            .elasticY(true)
            .controlsUseVisibility(true);

        spendHistChart.xAxis().tickFormat(function(d) {return d*10}); // convert back to base unit

        spendHistChart.yAxis().ticks(2);

        spenderRowChart
            .dimension(nameDim)
            .group(spendPerName)
            .elasticX(true)
            .controlsUseVisibility(true);

        var allDollars = ndx.groupAll().reduceSum(function(d) { return +d.Spent; });

        table
            .dimension(spendDim)
            .group(function(d) {
                return d.value;
            })
            .showGroups(false)
            .columns(['Name',
                    {
                        label: 'Spent',
                        format: function(d) {
                            return '$' + d.Spent;
                        }
                    },
                    'Year',
                    {
                        label: 'Percent',
                        format: function(d) {
                            return Math.floor((d.Spent / allDollars.value()) * 100) + '%';
                        }
                    }]);

        d3.select('#download')
            .on('click', function() {
                var data = nameDim.top(Infinity);
                if(d3.select('#download-type input:checked').node().value==='table') {
                    data = data.map(function(d) {
                        var row = {};
                        table.columns().forEach(function(c) {
                            row[table._doColumnHeaderFormat(c)] = table._doColumnValueFormat(c, d);
                        });
                        return row;
                    });
                }
                console.log("Table Data : " + data);
                //var blob = new Blob([d3.csv.format(data)], {type: "text/csv;charset=utf-8"});
                //saveAs(blob, 'data.csv');
            });
        dc.renderAll();
    }

    render() {
        return (  
            <section>
                <h1 className="hidden">Preprocessing</h1>
                <ul className="tabHeader">
                    <li className="current"><a href="#">Data</a></li>
                    <div className="btnArea">
                        <StepArrowComponent getHeaderEvent={this.props.getHeaderEvent} stepBack={this.state.stepBack} stepForward={this.state.stepForward}/>
                    </div>
                </ul>
                 <div className="container tabBody">
                    <article className="min-width-1">
                    <div className="data-box-wrap">
                        <div className="center-box">
                            <dl className="data-box">
                                <dt><span>Data info</span></dt>
                                <dd id="chart-ring-year"></dd>
                            </dl>
                            <dl className="data-box width350">
                                <dt><span>Train Status</span></dt>
                                <dd id="chart-hist-spend"></dd>
                            </dl>
                            <dl className="data-box width350">
                                <dt><span>TestResult</span></dt>
                                <dd id="chart-row-spenders"></dd>
                            </dl>
                        </div>
                    </div>
                    <div className="pre-tbl-wrap">
                            <table id="table" className="table"></table>
                        </div>
                    </article>
                 </div>  
            </section>
        )
    }
}