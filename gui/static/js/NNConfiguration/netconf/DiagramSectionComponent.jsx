import React from 'react'
import ReportRepository from './../../repositories/ReportRepository'
import Api from './../../utils/Api'
import CnnTableSectionComponent from './CnnTableSectionComponent';
import WdnnTableSectionComponent from './WdnnTableSectionComponent';
import StepArrowComponent from './../../NNLayout/common/StepArrowComponent'

export default class DiagramSectionComponent extends React.Component {
    constructor(props){
        super(props);
        
        this.state = {
            nnConfigFeatureInfoField : null,
            nnConfigLabelInfoField : null,
            stepBack : 3,
            stepForward : 5
        };
        
        // CNN
        this._getNetConfigCommonInfo = this._getNetConfigCommonInfo.bind(this);
        this._getNetConfigFormatInfo = this._getNetConfigFormatInfo.bind(this);
        this._getDataObject = this._getDataObject.bind(this);
        this._postNNNetConfigInfo = this._postNNNetConfigInfo.bind(this);

        // WDNN
        this._getNetConfigDataframeInfo = this._getNetConfigDataframeInfo.bind(this);
    }

    // component creation -> constructor 이후 실행
    // execute just once
    componentWillMount(){
        // choose CNN or WDNN
        localStorage.setItem('nn_type', (this.context.NN_TYPE).toUpperCase());
        (this.context.NN_TYPE).toUpperCase() ===  'CNN' ? this._getNetConfigCommonInfo(this.context.NN_ID):this._getNetConfigDataframeInfo(this.context.NN_ID)
    }

    componentDidUpdate(prevProps,prevState){
        
        if(prevState.nnConfigFeatureInfoField !== null && prevState.nnConfigLabelInfoField === null)
        {           
            const libScript = document.createElement("script");
            const tsScript = document.createElement("script");

            libScript.src = "../../../dist/lib.js";
            libScript.async = false;
            
            tsScript.src = "../../../dist/NetConf.js";
            tsScript.async = true;
        
            document.body.appendChild(libScript);
            document.body.appendChild(tsScript);
        }
    }

    // 3!
    shouldComponentUpdate(nextProps, nextState) {
        return (nextState.nnConfigFeatureInfoField !== null && nextState.nnConfigLabelInfoField === null)
            || (nextState.nnConfigFeatureInfoField !== null && nextState.nnConfigLabelInfoField !== null);
    }    

    //4!
    componentWillUpdate(nextProps, nextState){
        if(nextState.nnConfigFeatureInfoField !== null && nextState.nnConfigLabelInfoField === null && (this.context.NN_TYPE).toUpperCase() ===  'CNN') 
        {           
            this._getNetConfigFormatInfo(nextState.nnConfigFeatureInfoField, this.context.NN_ID);
        }
    }

    //2
    _getNetConfigCommonInfo(params) {
        this.props.reportRepository.getNetConfigCommonInfo(params).then((tableData) => {
            var nnConfigCommonInfoJson;
            if(typeof tableData === 'object')
            {
                nnConfigCommonInfoJson = JSON.parse(JSON.stringify(tableData));
            }
            else 
            {
                nnConfigCommonInfoJson = JSON.parse(tableData);
            }            

            for(let i=0; i < nnConfigCommonInfoJson.result.length; i++) 
            {
                if(params === nnConfigCommonInfoJson.result[i].pk)
                {
                    this.setState({nnConfigFeatureInfoField: nnConfigCommonInfoJson.result[i].fields});
                    break;
                }
            }
        });
    }

    //5!
    _getNetConfigFormatInfo(params, nnid) {
        this.props.reportRepository.getNetConfigFormatInfo(params, nnid).then((tableData) => {
            var nnConfigFormatInfoJson = JSON.parse(tableData);
            this.setState({nnConfigLabelInfoField: nnConfigFormatInfoJson.result});
        });
    }    

    _getDataObject() {
        let dataObj = {}; 
        
        dataObj.datalen = this.state.nnConfigLabelInfoField.x_size*this.state.nnConfigLabelInfoField.y_size;
        dataObj.taglen = JSON.parse(this.state.nnConfigFeatureInfoField.datasets).length;
        dataObj.matrix = [parseInt(this.state.nnConfigLabelInfoField.x_size),parseInt(this.state.nnConfigLabelInfoField.y_size)];
        dataObj.learnrate = 0.01;
        dataObj.label = JSON.parse(this.state.nnConfigFeatureInfoField.datasets);
        dataObj.epoch = 10;

        return dataObj;
    }

    _clickSaveButton(){
        console.log("click post!!");
        if((this.context.NN_TYPE).toUpperCase() === 'CNN')
        {
            this._postNNNetConfigInfo();
        }
        else if((this.context.NN_TYPE).toUpperCase() === 'WDNN')
        {
            this._postNNNetConfigWdnnInfo();
        }
    }

    _postNNNetConfigWdnnInfo(){
        console.log(this.context.NN_ID);

        this.props.reportRepository.postWdnnConf(this.context.NN_ID, JSON.parse(localStorage.wdnn_config));
    }

    _postNNNetConfigInfo(){
        console.log(this.context.NN_ID);
        let layerArray = [];
        let postObj = {};
        let propName;
        let propValue;

        // data json object 
        let dataObj = this._getDataObject();

        postObj.data = dataObj;
        
        // layer json array
        let domHiddenTable = document.getElementsByClassName('hidden_table');

        for(let i=0; i < domHiddenTable.length; i++)
        {
            var tr = (domHiddenTable[i]).querySelectorAll('tbody > tr');
            let layerObj = {};

            for(let j=0; j < tr.length; j++)
            {
                if([0,1,7,8,9].indexOf(j) >= 0)
                {
                    propName = tr[j].querySelector('td:nth-child(1)').innerText;
                    propValue = tr[j].querySelector('td:nth-child(2) > input[type=text]').value;

                    layerObj[propName] = propValue;
                    
                }
                else {
                    propName = tr[j].querySelector('td:nth-child(1)').innerText;
                    propValue = tr[j].querySelector('td:nth-child(2) > input[type=text]').value.split(",").map(Number);

                    layerObj[propName] = propValue;
                }
            }

            layerArray[i] = layerObj;
        }

        postObj.layer = layerArray;

        this.props.reportRepository.postNNNetConfigInfo(this.context.NN_ID, postObj);
    }

    // WDNN
    _getNetConfigDataframeInfo(nnId) {
        var nnConfigWdnnFeatureInfoJson;
        var nnConfigWdnnLabelInfoJson;
        var nnConfigWdnnConfJson;

        this.props.reportRepository.getDataFrameOnNetworkConfig('all', nnId).then((tableData) => {
            if(typeof tableData === 'object')
            {
                nnConfigWdnnFeatureInfoJson = JSON.parse(JSON.stringify(tableData));
            }
            else 
            {
                nnConfigWdnnFeatureInfoJson = JSON.parse(tableData);
            }
            
            this.setState({nnConfigFeatureInfoField: nnConfigWdnnFeatureInfoJson.result});
        }); 

        this.props.reportRepository.getDataFrameOnNetworkConfig('labels', nnId).then((tableData) => {
            if(typeof tableData === 'object')
            {
                nnConfigWdnnLabelInfoJson = JSON.parse(JSON.stringify(tableData));
            }
            else 
            {
                nnConfigWdnnLabelInfoJson = JSON.parse(tableData);
            }
            
            this.setState({nnConfigLabelInfoField: nnConfigWdnnLabelInfoJson.result});
        }); 

        this.props.reportRepository.getWdnnConf(nnId).then((tableData) => {
            if(typeof tableData === 'object')
            {
                nnConfigWdnnConfJson = JSON.parse(JSON.stringify(tableData));
            }
            else 
            {
                nnConfigWdnnConfJson = JSON.parse(tableData);
            }

            if(nnConfigWdnnConfJson.status === '404')
            {
                localStorage.setItem('wdnn_config', "{}");
            }
            else{
                localStorage.setItem('wdnn_config', nnConfigWdnnConfJson.result[0]);
            }
            
            localStorage.setItem('init_flag', 'true');
        });              
    }

    render() {
        return (
                <section >
                    <ul className="tabHeader">
                        <li className="current"><a href="#">{(this.context.NN_TYPE).toUpperCase()}</a></li>
                        <div className="btnArea">
                            <StepArrowComponent getHeaderEvent={this.props.getHeaderEvent} stepBack={this.state.stepBack} stepForward={this.state.stepForward}/>
                        </div>                        
                    </ul> 
                        <div id='netconf-diagram' className="container tabBody">
                            <div className="btnArea">
                                <button type="button" onClick={this._clickSaveButton.bind(this)}>Save</button>
                            </div>
                            <div id="main-part" className="l--page">
                                {/* Data Column */}
                                <div className="column data">
                                    <h4>
                                        <span>CONFIG DATA</span>
                                    </h4>
                                    <div className="ui-dataset">
                                        <div className="dataset-list">
                                            <div className="dataset" title="Circle">
                                                <canvas className="data-thumbnail" data-dataset="circle"></canvas>
                                            </div>
                                            <div className="dataset" title="Exclusive or">
                                                <canvas className="data-thumbnail" data-dataset="xor"></canvas>
                                            </div>
                                            <div className="dataset" title="Gaussian">
                                                <canvas className="data-thumbnail" data-dataset="gauss"></canvas>
                                            </div>
                                            <div className="dataset" title="Spiral">
                                                <canvas className="data-thumbnail" data-dataset="spiral"></canvas>
                                            </div>
                                            <div className="dataset" title="Plane">
                                                <canvas className="data-thumbnail" data-regDataset="reg-plane"></canvas>
                                            </div>
                                            <div className="dataset" title="Multi gaussian">
                                                <canvas className="data-thumbnail" data-regDataset="reg-gauss"></canvas>
                                            </div>
                                        </div>
                                    </div>
                                    <div>
                                        <div className="ui-percTrainData">
                                            <label htmlFor="percTrainData">Learning&nbsp;Rate:&nbsp;&nbsp;<span className="value">XX</span>%</label>
                                            <p className="slider">
                                                <input className="mdl-slider mdl-js-slider" type="range" id="percTrainData" min="0" max="99" step="1"/>
                                            </p>
                                        </div>
                                        <div className="ui-batchSize">
                                            <label htmlFor="batchSize">Batch size:&nbsp;&nbsp;<span className="value">XX</span></label>
                                            <p className="slider">
                                                <input className="mdl-slider mdl-js-slider" type="range" id="batchSize" min="1" max="30" step="1"/>
                                            </p>
                                        </div>
                                    </div>
                                </div>

                                {/* Features Column */}
                                <div className='column features'>
                                    <div id="network">
                                        <svg id="svg" width="510" height="450">
                                            <defs>
                                                <marker id="markerArrow" markerWidth="7" markerHeight="13" refX="1" refY="6" orient="auto" markerUnits="userSpaceOnUse">
                                                    <path d="M2,11 L7,6 L2,2" />
                                                </marker>
                                            </defs>
                                        </svg> 
                                        <div id="hovercard">
                                            <div>Click anywhere to edit.</div>
                                            <div><span className="type">Weight/Bias</span> is <span className="value">0.2</span><span><input type="number" /></span>.</div>
                                        </div>
                                        <div className="callout thumbnail">
                                            <svg viewBox="0 0 30 30">
                                                <defs>
                                                    <marker id="arrow" markerWidth="5" markerHeight="5" refX="5" refY="2.5" orient="auto" markerUnits="userSpaceOnUse">
                                                        <path d="M0,0 L5,2.5 L0,5 z" />
                                                    </marker>
                                                </defs>
                                            </svg>
                                        </div>
                                        <div className="callout weights">
                                            <svg viewBox="0 0 30 30">
                                                <defs>
                                                    <marker id="arrow" markerWidth="5" markerHeight="5" refX="5" refY="2.5" orient="auto" markerUnits="userSpaceOnUse">
                                                        <path d="M0,0 L5,2.5 L0,5 z" />
                                                    </marker>
                                                </defs>
                                            </svg>
                                        </div>
                                    </div>                        
                                </div>                        
                
                                {/* Hidden Layers Column */} 
                                <div className='column hidden-layers'>
                                    <h4>
                                        <div className="ui-numHiddenLayers">
                                            <button id="add-layers" className="mdl-button mdl-js-button mdl-button--icon">
                                                <i className="material-icons">add</i>
                                            </button>
                                            <button id="remove-layers" className="mdl-button mdl-js-button mdl-button--icon">
                                                <i className="material-icons">remove</i>
                                            </button>
                                        </div>
                                        <span id="num-layers"></span>
                                        <span id="layers-label"></span>
                                    </h4>
                                    <div className="bracket"></div>
                                </div>

                                {/* Output Column */}
                                <div className='column output'>
                                    <div className="metrics">
                                        <div className="output-stats ui-percTrainData">
                                        </div>
                                        <div className="output-stats train">
                                        </div>
                                        <div id="linechart"></div>
                                    </div>
                                </div>
                                {/* CNN */}
                                {
                                    (this.context.NN_TYPE).toUpperCase() === 'CNN' && this.state.nnConfigFeatureInfoField !== null && this.state.nnConfigLabelInfoField !== null &&
                                    <CnnTableSectionComponent nnConfigFeatureInfoField={this.state.nnConfigFeatureInfoField}
                                                            nnConfigLabelInfoField={this.state.nnConfigLabelInfoField}
                                    />
                                }

                                {/* WDNN */}
                                {
                                    (this.context.NN_TYPE).toUpperCase() === 'WDNN' && this.state.nnConfigFeatureInfoField !== null && this.state.nnConfigLabelInfoField !== null &&
                                    <WdnnTableSectionComponent nnConfigFeatureInfoField={this.state.nnConfigFeatureInfoField}
                                                            nnConfigLabelInfoField={this.state.nnConfigLabelInfoField}
                                    />
                                }                                
                            </div>
                        </div>   
                </section>
        )
    }
}

DiagramSectionComponent.defaultProps = {
    reportRepository: new ReportRepository(new Api())
}

DiagramSectionComponent.contextTypes = {
    NN_ID        : React.PropTypes.string,
    NN_TYPE      : React.PropTypes.string,
    NN_DATAVALID : React.PropTypes.string,
    NN_CONFIG    : React.PropTypes.string,
    NN_CONFVALID : React.PropTypes.string,
    NN_TRAIN     : React.PropTypes.string,
    NN_DATATYPE  : React.PropTypes.string
};

DiagramSectionComponent.childContextTypes = {
  NN_ID        : React.PropTypes.string,
  NN_TYPE      : React.PropTypes.string,
  NN_DATAVALID : React.PropTypes.string,
  NN_CONFIG    : React.PropTypes.string,
  NN_CONFVALID : React.PropTypes.string,
  NN_TRAIN     : React.PropTypes.string,
  NN_DATATYPE  : React.PropTypes.string
}
