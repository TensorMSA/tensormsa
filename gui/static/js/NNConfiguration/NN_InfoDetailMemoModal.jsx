import React from 'react'
import ReportRepository from './../repositories/ReportRepository'
import Api from './../utils/Api'

export default class NN_InfoDetailMemoModal extends React.Component {
    constructor(props, context) {
        super(props);
        this.state = {
        	NN_TableWFData: null,
        	memoValue:'',
        	active_flag : 'N',
        	nnInfoNewListTable:[],
        	key:1
        };

    }
    /////////////////////////////////////////////////////////////////////////////////////////
    // Search Function
    /////////////////////////////////////////////////////////////////////////////////////////
    componentDidMount() {
    }

    getCommonNNInfoWF() {
    	this.props.reportRepository.getCommonNNInfoWF(this.props.nn_id).then((tableData) => {// Network Version Info
            for(let i in tableData){
	            if(this.props.nn_wf_ver_id == tableData[i]["nn_wf_ver_id"]){
	            	this.setState({ memoValue : tableData[i]["nn_wf_ver_desc"] })  
	             	// this.state.memoValue = tableData[i]["nn_wf_ver_desc"]
	             	this.setState({ NN_TableWFData : tableData[i] })
	            }  
	        }
        });
    }

    saveMemo(){
        let memo = this.refs.master1.value
        let wfparam = {}
        wfparam["nn_wf_ver_id"] = this.props.nn_wf_ver_id
        wfparam["nn_def_list_info_nn_id"] = ""
        wfparam["nn_wf_ver_info"] = "init"
        wfparam["condition"] = "1"
        wfparam["active_flag"] = this.state.NN_TableWFData["active_flag"]
        wfparam["nn_wf_ver_desc"] = memo
        // Version Active 변경.
        this.props.reportRepository.putCommonNNInfoWF(this.props.nn_id, wfparam).then((tableData) => {
        });
    }

    render() {
        if(this.state.NN_TableWFData == null){
        	this.getCommonNNInfoWF()
        }

        if(this.state.NN_TableWFData != null && this.state.nnInfoNewListTable.length == 0){
	        this.state.nnInfoNewListTable.push(<textarea key={this.state.key++} name="memoarea" 
	                                        		  ref= 'master1'
	                                                  maxLength="5000"
	                                                  placeholder="input memo"
	                                        		  style={{ "width":"100%", "height":100 }} 
	                                        		  defaultValue={this.state.memoValue} 
	                                        		  />)
		}
        return (  

            <div>
                <h1>Version Momo</h1>
                
                <div className="container tabBody">
                    <div id="tab1">
                        <article>
                            <table className="form-table align-left">
                                <colgroup>
                                    <col width="40" />
                                    <col width="300" />
                                </colgroup> 
                                <tbody>
                                <tr>
                                    <th>Memo</th>
  
                                    <td>

					                            {this.state.nnInfoNewListTable}
					
                                    </td>
                                </tr>
                                </tbody>
                            </table>
                            
                        </article>
                    </div>
                </div>
                <span className="modal-footer">
                    <button onClick={this.saveMemo.bind(this)}>Save</button>
                    <button onClick={this.props.closeModal}>Close</button>
                </span>
            </div>
        )
    }
}

NN_InfoDetailMemoModal.defaultProps = {
    reportRepository: new ReportRepository(new Api())
};
