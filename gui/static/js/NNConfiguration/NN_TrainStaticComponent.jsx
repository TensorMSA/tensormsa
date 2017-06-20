import React from 'react';
import StepArrowComponent from './../NNLayout/common/StepArrowComponent';
import LabelByChartComponent from './TrainStatic/LabelByChartComponent'
import TrainRealTimeChartComponent from './TrainStatic/TrainRealTimeChartComponent'
import RealTimeLineChartComponent from './TrainStatic/RealTimeLineChartComponent'
import ReportRepository from './../repositories/ReportRepository'
import ModalViewTrainParm from './TrainStatic/ModalSetTrainParmComponent'
import TrainGaugeChartComponent from './TrainStatic/TrainGaugeChartComponent'
import Modal from 'react-modal';
import Api from './../utils/Api'

export default class NN_TrainStaticComponent extends React.Component {
    constructor(props) {
        super(props);
        this.historyData = [];
        this.threadFlag = false;
        this.closeModal = this.closeModal.bind(this);
        this.saveModal = this.saveModal.bind(this);
        this.state = {
                stepBack : 4,
                stepForward : 6,
                graphLoss : null,
                graphSummary : null,
                graphSummaryDetail : null,
                graphLabel : null,
                searchDisable : false,
                trainSteps : null,
                selModalView : null,
                open : false
            };
    }

    componentDidMount(){
        this.threadFlag = true;
        this.getNeuralNetStat();
    }

    componentWillUnmount(){
        this.threadFlag = false;
    }

    checkNeuralNet(){
        this.props.reportRepository.postNeuralNetCheck(this.context.NN_TYPE , this.context.NN_ID, "").then((data) => {
            if(data.status == '200'){
                msg.show("Check Result OK")
            }else{
                msg.show("Error on Net config!!")
            }
            
        });
    }
    // close modal 
    closeModal() { 
        this.setState({open: false}); 
    }

    // save modal 
    saveModal() { 
        this.setState({open: false});
    }

    trainNeuralNet(){
        let parm = {}
        parm.nnType = this.context.NN_TYPE;
        parm.nnId = this.context.NN_ID;
        this.setState({selModalView : <ModalViewTrainParm saveModal={this.saveModal} closeModal={this.closeModal} parm={parm}
            afterTrainPost={this.afterTrainPost.bind(this)} />} )
        this.setState({open: true})
    }

    afterTrainPost(){
        this.threadFlag = true;
        this.getNeuralNetStat();
    }

    evalNeuralNet(){
        msg.show("Start Evaluation")
        var params = {samplenum : '1' , samplemethod : 'random'}
        this.props.reportRepository.postNeuralNetEval(this.context.NN_TYPE, this.context.NN_ID, params).then((data) => {
            this.setState({graphSummary : <dd><span>0%</span></dd>})
            this.setState({graphSummaryDetail : <dd><span>0/0</span></dd>})
            this.threadFlag = true;
            this.getNeuralNetStat();
            msg.show("Finish Evaluation")
        });
    }

    getNeuralNetStat(){
        this.props.reportRepository.getNeuralNetStat(this.context.NN_ID).then((data) => { 
            if(this.threadFlag == true){
                this.renderGraphs(data);
                setTimeout(this.getNeuralNetStat.bind(this), 15000);    
            }else{
                this.threadFlag = true
            }
        });
    }

    renderGraphs(data){
        let labelData = data['detail']
        let lossData = data['loss']
        let summaryData = data['summary']
        let jobparm = data['jobparm']

        this.threadFlag = jobparm['status']=='3'?true:false
        let accuracy = Math.round(parseInt(summaryData['testpass'],10)/(parseInt(summaryData['testpass'],10) + parseInt(summaryData['testfail'],10)) * 100)
        let summatDetail = summaryData['testpass'] + "/" + (parseInt(summaryData['testfail']) + parseInt(summaryData['testpass']))
        //let trainSteps = jobparm['datapointer'] + "/" + jobparm['endpointer']

        this.setState({graphLoss : <RealTimeLineChartComponent historyData={this.historyData} currData={lossData}/>})
        this.historyData = lossData;
        this.setState({graphLabel : <LabelByChartComponent data={labelData}/>})
        this.setState({graphSummary : <dd><span>{accuracy}%</span></dd>})
        this.setState({graphSummaryDetail : <dd><span>{summatDetail}</span></dd>})
        this.setState({trainSteps : <TrainGaugeChartComponent datapointer={jobparm['datapointer']} endpointer={jobparm['endpointer']}/>})
    }
 
    render() {
        return (
            <section>
                <h1 className="hidden">Network Configuration</h1>
                <ul className="tabHeader">
                    <li className="current"><a href="#">{(this.context.NN_TYPE).toUpperCase()}</a></li>
                    <div className="btnArea">
                        <StepArrowComponent getHeaderEvent={this.props.getHeaderEvent} stepBack={this.state.stepBack} stepForward={this.state.stepForward}/>
                    </div>
                </ul>
                <div className="container tabBody">
                <div className="inner-btnArea">
                    <button type="button" className="search" onClick={this.checkNeuralNet.bind(this)}>Error Check</button>
                    <button type="button" className="search" onClick={this.trainNeuralNet.bind(this)}>Train</button>
                    <button type="button" className="search" onClick={this.evalNeuralNet.bind(this)}>Eval</button>    
                    <button type="button" className="search" onClick={this.getNeuralNetStat.bind(this)} disabled={this.state.searchDisable}>Search</button>    
                </div>
                    <article className="train min-width-2">
                        <section className="train-result">
                            <div className="train-wrap-top">
                                <dl className="statistics">
                                    <dt><span className="circle-yellow">Train Loss Graph</span></dt>
                                        {this.state.graphLoss}
                                    <dd></dd>
                                </dl>
                                <dl className="test-result">
                                    <dt><span className="circle-yellow">Train Summary Result</span></dt>
                                    {this.state.graphSummary}
                                    {this.state.graphSummaryDetail}
                                </dl>
                                <dl className="test-step">
                                    <dt><span className="circle-yellow">Train Steps</span></dt>
                                        {this.state.trainSteps}
                                </dl>
                            </div>
                        </section>
                        <section className="graph">
                            <div className="train-wrap-bottom">
                                {this.state.graphLabel}
                            </div>
                        </section>

                        <Modal
                            className="modal"
                            overlayClassName="modal"
                            isOpen={this.state.open}
                            onRequestClose={this.closeModal}>
                            <div className="modal-dialog modal-lg">
                                {this.state.selModalView}
                            </div>
                        </Modal>
                    </article>
                 </div>  
            </section>
        )
    }
}

NN_TrainStaticComponent.defaultProps = {
    reportRepository: new ReportRepository(new Api())
};     

NN_TrainStaticComponent.contextTypes = {
    NN_ID        : React.PropTypes.string,
    NN_TYPE      : React.PropTypes.string,
    NN_DATAVALID : React.PropTypes.string,
    NN_CONFIG    : React.PropTypes.string,
    NN_CONFVALID : React.PropTypes.string,
    NN_TRAIN     : React.PropTypes.string,
    NN_DATATYPE  : React.PropTypes.string
};