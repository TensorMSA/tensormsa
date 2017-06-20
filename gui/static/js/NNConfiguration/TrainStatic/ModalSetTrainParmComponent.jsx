import React from 'react'
import ReportRepository from './../../repositories/ReportRepository';
import Api from './../../utils/Api';

export default class ModalViewTrainParm extends React.Component {
    constructor(props) {
        super(props);
        this.batch = 0;
        this.repeat = 0;
        this.state = {
                networkId : null,
                labelRows : null,
                labelName : null,
                batchDom : null,
                repeatDom : null,
                trainStatus : null
                };
    }

    componentDidMount(preProps, prevState){
        this.getTrainParm()
    }

    //set label name on state variable
    setBatchSize(obj){
        this.setState({batchDom:obj.target.value})
        this.batch = obj.target.value
    }

    setRepeatSize(obj){
        this.setState({repeatDom:obj.target.value})
        this.repeat = obj.target.value
    }

    postTrain(){
        this.props.reportRepository.postNeuralNetTrain(this.props.parm.nnType, this.props.parm.nnId, "").then((data) => {
            this.getTrainParm();
            this.props.afterTrainPost();
        });
        this.getTrainParm();
    }

    getTrainParm(){
        this.props.reportRepository.getJobInfo(this.props.parm.nnId).then((data) => {
            if(data['status'] == '200'){
                let result = data['result'];
                let status = ''
                if(result['status'] == '3'){status = "Running"}
                else if(result['status'] == '5'){status = "Finish"}
                else if(result['status'] == '9'){status = "Error"}
                this.setState({repeatDom : result['epoch']})
                this.setState({batchDom : result['batchsize']})
                this.setState({trainStatus : status})
            }else{
                msg.show("Server Error")
            }
        });
    }

    setTrainParm(){
        let insert_data = {};
        insert_data.epoch = this.state.repeatDom;
        insert_data.batchsize = this.state.batchDom;
        if(this.repeat){insert_data.epoch = this.repeat;}
        if(this.batch){insert_data.batchsize = this.batch;}
        
        this.props.reportRepository.setJobInfo(this.props.parm.nnId, insert_data).then((data) => {
            if(data['status'] == '200'){
                let result = data['result'];
                let status = ''
                if(result['status'] == '3'){status = "Running"}
                else if(result['status'] == '5'){status = "Finish"}
                else if(result['status'] == '9'){status = "Error"}
                this.setState({repeatDom : result['epoch']})
                this.setState({batchDom : result['batchsize']})
                this.setState({trainStatus : status})
            }else{
                msg.show("Server Error")
            }
        });
    }

    render() {
        return (   
            <div>
                <h1>Train Module</h1>
                
                <div className="container tabBody">
                    <div id="tab1">
                        <article>
                            <table className="form-table align-left">
                                <colgroup>
                                <col width="50" />
                                <col width="60" />
                                <col width="50" />
                                <col width="60" />
                                <col width="65" />
                                <col width="75" />
                                <col width="80" />
                                </colgroup> 
                                <tbody>
                                <tr>
                                    <th>BatchSize</th>
                                    <td>
                                        <input type="text" name="batch_size" placeholder="batch_size" 
                                        onChange={this.setBatchSize.bind(this)} value={this.state.batchDom} />
                                    </td>
                                    <th>RepeatTime</th>
                                    <td>
                                        <input type="text" name="repeat_time" placeholder="repeat_time" 
                                        onChange={this.setRepeatSize.bind(this)} value={this.state.repeatDom} />
                                    </td>
                                    <th>Status</th>
                                    <td>
                                        {this.state.trainStatus}
                                    </td>
                                    <td>
                                        <button type="button" onClick={this.setTrainParm.bind(this)}>Set</button>
                                    </td>
                                </tr>
                                <tr>

                                </tr>
                                </tbody>
                            </table>
                        </article>
                    </div>
                </div>
                <span className="modal-footer">
                    <button onClick={this.postTrain.bind(this)}>Train</button>
                    <button onClick={this.props.closeModal}>Close</button>
                </span>
            </div>
        )
    }
} 

ModalViewTrainParm.defaultProps = {
    reportRepository: new ReportRepository(new Api())
};