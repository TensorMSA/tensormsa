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

    uploadDataFiles(){
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

    uploadData(){
        let selectedFile = document.getElementById('text1').value
        let jsonParam = {}
        jsonParam["input_data"] = selectedFile

        this.props.reportRepository.postPredictNn(this.props.nn_net_type, this.props.nn_id, 'active', jsonParam).then((tableData) => {
            this.setState({ NN_TableResult: tableData })
            });
    }

    render() {
        let k = 10000
        this.getPredictAPI()
        let data = []
        data.push(<tr key={k++}><td key={k++} style={{"textAlign":"left", "fontWeight":"bold"}} >  import request </td></tr>)
        data.push(<tr key={k++}><td key={k++} style={{"textAlign":"left", "fontWeight":"bold"}} >  url={"'"+this.state.NN_TableData+"'"} </td></tr>)
        

        if(this.props.nn_net_type == "resnet" || this.props.nn_net_type == "cnn"){      
            let imgStr = "file = {'files000001':open('/hoya_src_root/test.jpg','rb')}"
            data.push(<tr key={k++}><td key={k++} style={{"textAlign":"left", "fontWeight":"bold"}} > {imgStr}  </td></tr>)
            data.push(<tr key={k++}><td key={k++} style={{"textAlign":"left", "fontWeight":"bold"}} >  resp = requests.post(url, files=file) </td></tr>)
        }else{
            data.push(<tr key={k++}><td key={k++} style={{"textAlign":"left", "fontWeight":"bold"}} >   resp = requests.post(url) </td></tr>)
        }
        data.push(<br />)

        let datadetail = []
        if(this.props.nn_net_type != "wcnn"){
            datadetail.push(<tr key={k++}><td key={k++} style={{"textAlign":"left", "fontWeight":"bold"}} >
                        <form key={k++} style={{"marginLeft":"15px"}} method="post">
                        <label key={k++} htmlFor="file">Choose file to upload(최초 Loading시 Cach에 저장으로 인해 오래걸림.)</label>
                        <br />
                        <input key={k++} type="file" id="file" name="file" multiple />
                        <div><br/>
                        <button key={k++} type="button" onClick={() => this.uploadDataFiles()} >Submit</button><br/>
                        </div>
                        </form></td></tr>)

            
        }else{
            datadetail.push(<tr key={k++}><td key={k++} style={{"textAlign":"left", "fontWeight":"bold"}} >
                        <form key={k++} style={{"marginLeft":"15px"}} >
                        <label key={k++} >Choose file to upload(최초 Loading시 Cach에 저장으로 인해 오래걸림.)</label>
                        <br/>
                        Input Data : <input type="text" id="text1" name = "text1" style={{"width":"400"}} />
                        <div><br/>
                        <button key={k++} type="button" onClick={() => this.uploadData()} >Submit</button><br/>
                        </div>
                        </form></td></tr>
                        )

           
        }

        let datadetailjson = []
        datadetailjson.push(<tr key={k++}><td key={k++} style={{"textAlign":"left", "fontWeight":"bold"}}>
                <div key={k++} style={{ "overflow":"auto", "height":300}}> 
                <ReactJson style={{"marginLeft":"15px"}} key={k++} src={this.state.NN_TableResult} collapsed = {true} />
                </div></td></tr>)
        
        return (  
            <div>
                <h1> Predict API </h1>
                <div className="container paddingT10">
                    <div id="tab1">
                        <article>
                            <table key={k++} className="table detail" style={{"marginLeft":"13px"}}>
                                <tbody key={k++}>
                                {data}
                                </tbody>
                            </table>
                            <table key={k++} className="table detail" style={{"marginLeft":"13px"}}>
                                <tbody key={k++}>
                                {datadetail}
                                </tbody>
                            </table>
                            <br />
                            <table key={k++} className="table detail" style={{"marginLeft":"13px"}} >
                                <tbody key={k++}>
                                {datadetailjson}
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
