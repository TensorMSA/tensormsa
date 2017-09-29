import React from 'react'
import ReportRepository from './../repositories/ReportRepository'
import Api from './../utils/Api'
import EnvConstants from './../constants/EnvConstants';


export default class NN_InfoDetailPredictAPIModal extends React.Component {
    constructor(props, context) {
        super(props);
        this.state = {
        	NN_TableData: null
        };

    }
    /////////////////////////////////////////////////////////////////////////////////////////
    // Search Function
    /////////////////////////////////////////////////////////////////////////////////////////
    componentDidMount() {
    }

    getPredictAPI() {
    	let url = EnvConstants.getWebServerUrl() 
        url += '/api/v1/type/service/state/predict/type/'+this.props.nn_net_type
        url += '/nnid/'+this.props.nn_id+'/ver/'+this.props.nn_wf_ver_id+'/'

        this.state.NN_TableData = url
    }

    handleClickAPIView(row){

        
        console.log(url)
    }

    render() {
        let k = 10000
        this.getPredictAPI()
        let data = []
        data.push(<tr key={k++}><td key={k++}><h3>  import request </h3></td></tr>)
        data.push(<tr key={k++}><td key={k++}><h3>  url={"'"+this.state.NN_TableData+"'"} </h3></td></tr>)
        

        if(this.props.nn_net_type == "resnet"){      
            let imgStr = "file = {'files000001':open('/hoya_src_root/test.jpg','rb')}"
            data.push(<tr key={k++}><td key={k++}><h3>  {imgStr}  </h3></td></tr>)
            data.push(<tr key={k++}><td key={k++}><h3>  resp = requests.post(url, files=file) </h3></td></tr>)
        }else{
            data.push(<tr key={k++}><td key={k++}><h3>  resp = requests.post(url) </h3></td></tr>)
        }
        

        return (  

            <div>
                <h1> Predict API </h1>
                
                <div className="container tabBody">
                    <div id="tab1">
                        <article>
                            <table key={k++} className="form-table align-left">
                                <tbody key={k++}>
                                <pre key={k++}>

                                {data}
                                </pre>
                                </tbody>
                            </table>
                            
                        </article>
                    </div>
                </div>
                <span className="modal-footer">
                    <button key={k++} onClick={this.props.closeModalPredictAPI}>Close</button>
                </span>
            </div>
        )
    }
}

NN_InfoDetailPredictAPIModal.defaultProps = {
    reportRepository: new ReportRepository(new Api())
};
