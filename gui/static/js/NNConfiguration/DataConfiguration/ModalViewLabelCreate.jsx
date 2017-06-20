import React from 'react'
import ReportRepository from './../../repositories/ReportRepository';
import Api from './../../utils/Api';

export default class ModalViewLabelCreate extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
                networkId : null,
                labelRows : null,
                labelName : null
               
                };
    }

    //set label name on state variable
    setLabelName(obj){
        this.setState({labelName: obj.target.value});
    }

    // searh label list
    getLabelList(){
        let requestUrl = "label/" + this.props.networkId + "/";
        this.props.reportRepository.getImageLabelData(requestUrl, "").then((data) => {
            let labelList = data['result'];
            let rows = [];
            let i = 0 ;
            for(let label of labelList){
                rows.push(<tr key={i++}><td>{label}</td></tr>)
            }
            this.setState({labelRows : rows})
        });
    }

    // add label list
    postLabelList(){
        let requestUrl = "label/" + this.state.labelName + "/nnid/" + this.props.networkId +"/";
        this.props.reportRepository.postImageLabelData(requestUrl, "").then((data) => {
            let labelList = data['result'];
            let rows = [];
            let i = 0 ;
            for(let label of labelList){
                rows.push(<tr key={i++}><td>{label}</td></tr>)
            }
            this.setState({labelRows : rows})
        });
    }

    //delete label list
    deleteLabelList(){
        let requestUrl = "label/" + this.state.labelName + "/nnid/" + this.props.networkId +"/";
        this.props.reportRepository.deleteImageLabelData(requestUrl, "").then((data) => {
            let labelList = data['result'];
            let rows = [];
            let i = 0 ;
            for(let label of labelList){
                rows.push(<tr key={i++}><td>{label}</td></tr>)
            }
            this.setState({labelRows : rows})
        });
    }

    searchBtn(){
        this.props.searchBtn(this.props.networkId);
        this.props.closeModal();
    }

    render() {
        return (   
            <div>
                <h1>Table Management</h1>
                
                <div className="container tabBody">
                    <div id="tab1">
                        <article>
                            <table className="form-table align-left">
                                <colgroup>
                                <col width="50" />
                                <col width="60" />
                                <col width="250" />
                                </colgroup> 
                                <tbody>
                                <tr>
                                    <th>Insert New</th>
                                    <td>
                                        <input type="text" name="label_name" placeholder="label_name" 
                                        onChange={this.setLabelName.bind(this)} value={this.state.value} />
                                    </td>
                                    <td>
                                        <button type="button" onClick={this.getLabelList.bind(this)}>Search</button>
                                        <button type="button" onClick={this.postLabelList.bind(this)}>Add</button>
                                        <button type="button" onClick={this.deleteLabelList.bind(this)}>Delete</button>
                                    </td>
                                </tr>
                                </tbody>
                            </table>
                            <div className="scroll-container">
                                <div className="scroll-wrap">
                                    <table className="table">
                                        <thead>
                                            <tr>
                                                <th><div>Label Name</div></th>
                                            </tr>
                                        </thead>
                                        <tbody className="center">    
                                            {this.state.labelRows}  
                                        </tbody>
                                    </table>
                                </div>
                            </div>
                        </article>
                    </div>
                </div>
                <span className="modal-footer">
                    <button onClick={this.searchBtn.bind(this)}>Load</button>
                    <button onClick={this.props.closeModal}>Close</button>
                </span>
            </div>
        )
    }
} 

ModalViewLabelCreate.defaultProps = {
    reportRepository: new ReportRepository(new Api())
};