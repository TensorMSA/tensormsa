import React from 'react'
import ReportRepository from './../repositories/ReportRepository'
import Api from './../utils/Api'
import EnvConstants from './../constants/EnvConstants';
import ReactJson from 'react-json-view'
import SpinnerComponent from './../NNLayout/common/SpinnerComponent'

export default class NN_InfoDetailPredictAPIModal extends React.Component {
    constructor(props, context) {
        super(props);
        this.state = {
        	NN_TableData: null,
            NN_TableResult:{'result':'Empty'}
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

    uploadData(){
        function pad(n, width) {
          n = n + '';
          return n.length >= width ? n : new Array(width - n.length + 1).join('0') + n;
        }

        let selectedFile = document.getElementById('file').files

        let files = new FormData()
        for(let i=0 ; i < selectedFile.length ; i++){
            let key = selectedFile[i]
            files.append("file"+pad(i, 5), key)
        }

        this.props.reportRepository.postPredictNnFiles(this.props.nn_net_type, this.props.nn_id, this.props.nn_wf_ver_id, files).then((tableData) => {
            this.setState({ NN_TableResult: tableData })
            });
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
        data.push(<hr />)
        if(this.props.nn_net_type != "wcnn"){
            data.push(<form key={k++} style={{"marginLeft":"15px"}} method="post">
                        <label key={k++} htmlFor="file"><h3>Choose file to upload</h3></label>
                        <input key={k++} type="file" id="file" name="file" multiple />
                        <div><br/>
                        <button key={k++} type="button" onClick={() => this.uploadData()} >Submit</button><br/>
                        </div>
                        </form>)

            data.push(<div key={k++} style={{ "overflow":"auto", "height":300}}> 
                <ReactJson key={k++} src={this.state.NN_TableResult} collapsed = {true} />
                </div>)
        }
        
        return (  
            <div>
                <h1> Predict API </h1>
                <div className="container paddingT10">
                    <div id="tab1">
                        <article>
                            <table key={k++} className="form-table align-left">
                                <tbody key={k++}>
                                <pre>
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
