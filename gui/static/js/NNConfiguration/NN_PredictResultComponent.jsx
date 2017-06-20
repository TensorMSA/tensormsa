import React from 'react'
import PredictResultCNNComponent from './PredictResult/PredictResultCNN'
import PredictResultWDNNComponent from './PredictResult/PredictResultWDNN'
import PredictResultCIFAComponent from './PredictResult/PredictResultCIFA'
import StepArrowComponent from './../NNLayout/common/StepArrowComponent'


export default class NN_PredictResultComponent extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
                PredictResultComponent : null,
                selected: null, //this.context.NN_TYPE.toUpperCase(), //initail lodaing is WDNN
                stepBack : 5,                
                stepForward : 6
                };
    }

     componentDidMount(){
        console.log("Predict Main did mounted!!!!!")
        console.log('NN_TYPE : ' + this.context.NN_TYPE)   
        this.setFilter(this.context.NN_TYPE.toUpperCase())
    } 

    setFilter(filter){
        this.setState({selected  : filter})
        if (filter == 'WDNN') {
           // return this.getTableData();
            return this.setState({PredictResultComponent  : <PredictResultWDNNComponent/>});
        }
        else if (filter == 'CNN'){
            return this.setState({PredictResultComponent  : <PredictResultCNNComponent/>});
        }
        else if (filter == 'CIFAR'){
            return this.setState({PredictResultComponent  : <PredictResultCIFAComponent/>});
        }
        else {
          console.log("setFilter : " + filter)
          //  return this.setState({PredictResultComponent  : <PredictResultCIFAComponent/>});
        }
    }

    

    isActive(value){
        return ((value===this.state.selected) ? 'current':'not_current');
    }


    render() {
        return (
            <section>
                <h1 className="hidden">Network Configuration</h1>
                    <ul className="tabHeader">
                        <li className={this.isActive('WDNN')} onClick={this.setFilter.bind(this, 'WDNN')}><a href="#">WDNN</a></li>
                        <li className={this.isActive('CNN')} onClick={this.setFilter.bind(this, 'CNN')}><a href="#">CNN</a></li>
                        <li className={this.isActive('CIFAR')} onClick={this.setFilter.bind(this, 'CIFAR')}><a href="#">CIFAR</a></li>
                    <div className="btnArea">
                        <StepArrowComponent getHeaderEvent={this.props.getHeaderEvent} stepBack={this.state.stepBack} stepForward={this.state.stepForward}/>
                    </div>
                    </ul>
				    {this.state.PredictResultComponent}
            </section>
        )
    }
}


NN_PredictResultComponent.contextTypes = {
    //NN_ID: React.PropTypes.string
    NN_TYPE: React.PropTypes.string
};