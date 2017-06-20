import React from 'react'
import d3 from "d3"
//import GaugeChart from './d3_gauge.js'

export default class TrainGaugeChartComponent extends React.Component {
    constructor(props) {
        super(props);

        }

        componentDidMount() { //after DOM make D3 Chart
            let percent = .40
            this.makeChart(percent);
        }


        makeChart(percent){
            var needle;

            (function(){

            var barWidth, chart, chartInset, degToRad, repaintGauge,
                height, margin, numSections, padRad, percToDeg, percToRad, 
                radius, sectionIndx, svg, totalPercent, width, sectionPerc, el;

            numSections = 1;
            sectionPerc = 1 / numSections / 2;
            padRad = 0.025;
            chartInset = 10;

            // Orientation of gauge:
            totalPercent = .75;

            el = d3.select('.chart-gauge');

            margin = {
                top: 20,
                right: 20,
                bottom: 30,
                left: 20
            };

            width = el[0][0].offsetWidth - margin.left - margin.right;
            height = width;
            radius = Math.min(width, height) / 2;
            barWidth = 40 * width / 300;

            /*
                Utility methods 
            */
            percToDeg = function(perc) {
                return perc * 360;
            };

            percToRad = function(perc) {
                return degToRad(percToDeg(perc));
            };

            degToRad = function(deg) {
                return deg * Math.PI / 180;
            };

            // Create SVG element
            svg = el.append('svg').attr('width', width + margin.left + margin.right).attr('height', height + margin.top + margin.bottom);

            // Add layer for the panel
            chart = svg.append('g').attr('transform', "translate(" + ((width + margin.left) / 2) + ", " + ((height + margin.top) / 2) + ")");
            chart.append('path').attr('class', "arc chart-filled");
            chart.append('path').attr('class', "arc chart-empty");

            let arc2 = d3.svg.arc().outerRadius(radius - chartInset).innerRadius(radius - chartInset - barWidth)
            let arc1 = d3.svg.arc().outerRadius(radius - chartInset).innerRadius(radius - chartInset - barWidth)

            repaintGauge = function (perc) 
            {
                var next_start = totalPercent;
                let arcStartRad = percToRad(next_start);
                let arcEndRad = arcStartRad + percToRad(perc / 2);
                next_start += perc / 2;

                arc1.startAngle(arcStartRad).endAngle(arcEndRad);
                arcStartRad = percToRad(next_start);
                arcEndRad = arcStartRad + percToRad((1 - perc) / 2);
                arc2.startAngle(arcStartRad + padRad).endAngle(arcEndRad);
                chart.select(".chart-filled").attr('d', arc1);
                chart.select(".chart-empty").attr('d', arc2);

            }


            var Needle = (function() {

                /** 
                 * Helper function that returns the `d` value
                * for moving the needle
                **/
                var recalcPointerPos = function(perc) {
                var centerX, centerY, leftX, leftY, rightX, rightY, thetaRad, topX, topY;
                thetaRad = percToRad(perc / 2);
                centerX = 0;
                centerY = 0;
                topX = centerX - this.len * Math.cos(thetaRad);
                topY = centerY - this.len * Math.sin(thetaRad);
                leftX = centerX - this.radius * Math.cos(thetaRad - Math.PI / 2);
                leftY = centerY - this.radius * Math.sin(thetaRad - Math.PI / 2);
                rightX = centerX - this.radius * Math.cos(thetaRad + Math.PI / 2);
                rightY = centerY - this.radius * Math.sin(thetaRad + Math.PI / 2);
                return "M " + leftX + " " + leftY + " L " + topX + " " + topY + " L " + rightX + " " + rightY;
                };

                function Needle(el) {
                this.el = el;
                this.len = width / 3;
                this.radius = this.len / 6;
                }

                Needle.prototype.render = function() {
                this.el.append('circle').attr('class', 'needle-center').attr('cx', 0).attr('cy', 0).attr('r', this.radius);
                return this.el.append('path').attr('class', 'needle').attr('d', recalcPointerPos.call(this, 0));
                };

                Needle.prototype.moveTo = function(perc) {
                var self,
                    oldValue = this.perc || 0;

                this.perc = perc;
                self = this;

                // Reset pointer position
                this.el.transition().delay(100).ease('quad').duration(200).select('.needle').tween('reset-progress', function() {
                    return function(percentOfPercent) {
                    var progress = (1 - percentOfPercent) * oldValue;
                    
                    repaintGauge(progress);
                    return d3.select(this).attr('d', recalcPointerPos.call(self, progress));
                    };
                });

                this.el.transition().delay(300).ease('bounce').duration(1500).select('.needle').tween('progress', function() {
                    return function(percentOfPercent) {
                    var progress = percentOfPercent * perc;
                    
                    repaintGauge(progress);
                    return d3.select(this).attr('d', recalcPointerPos.call(self, progress));
                    };
                });

                };

                return Needle;

            })();

            needle = new Needle(chart);
            needle.render();

            needle.moveTo(percent);

            })();
        }


    render() {

        const css = `
  			.chart-gauge
			{
			  width: 300px;
			  margin: 10px auto  
			 } 
			.chart-filled
			{
				fill: #ed4d64;
			}
			.chart-empty
			{
				fill: #dedede;
			}
		
			.needle, .needle-center
			{
				fill: #464A4F;
			}

			svg {
			  font: 10px sans-serif;
			}`

        return (   

                    <article>
                        <style>{css}</style>
	                	<div className="chart-gauge">
                        </div>
                    </article>
        )
    }
}