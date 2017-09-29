import React from 'react'
import EnvConstants from './../../constants/EnvConstants';
import ReportRepository from './../../repositories/ReportRepository'
import Api from './../../utils/Api'
const FileUpload = require('react-fileupload');
import { Line, Circle } from 'rc-progress';

export default class FileUploadComponent extends React.Component {
    constructor(props) {
        super(props)
        this.state = {
            fileData:null,
            percent:0,
            fileurl:'/api/v1/type/wf/state/data/detail/upload/file/nnid/',
            lineview:false
            };
        this.getFileData= this.getFileData.bind(this);
        this._handleUploading = this._handleUploading.bind(this);
        this.fileOption={
            baseUrl:EnvConstants.getApiServerUrl()+this.state.fileurl,
            param:{
                fid:0
            }
            ,chooseAndUpload : true
            ,multiple : true
            ,uploadSuccess : this.getFileData
            ,uploading: this._handleUploading
        };

    }
    
    componentDidMount() {
        this.getFileData()
    }

    _handleUploading(progress, mill){
        this.state.lineview = true
        let per = Math.round(progress.loaded/progress.total * 100)
        this.setState({ percent : per})
        if(progress.total == 0){
            this.state.lineview = false
        }
    }

    getFileData(){
        let nn_id = this.props.nn_id
        let nn_wf_ver_id = this.props.nn_wf_ver_id
        let nn_node_name = this.props.nn_node_name
        this.props.reportRepository.getFileUpload(nn_id, nn_wf_ver_id, nn_node_name, this.props.nn_path_type).then((tableData) => {
                                        this.setState({ fileData : tableData})
                                    });
    }

    deleteFileData(value){
        let fparam = {}
        fparam["filename"] = value.target.alt
        fparam["type"] = this.props.nn_path_type
        let re = confirm( "Are you delete?" )
        if(re == true){
            this.props.reportRepository.deleteFileUpload(this.props.nn_id, this.props.nn_wf_ver_id, this.props.nn_node_name, fparam).then((tableData) => {
                                                    this.getFileData()
                                                    });
        }
    }

    render() {
        let k = 1
        let listFile = []

        this.fileOption.baseUrl = EnvConstants.getApiServerUrl()+this.state.fileurl
        this.fileOption.baseUrl += this.props.nn_id+'/ver/'+this.props.nn_wf_ver_id+'/dir/'+this.props.nn_node_name+'/type/'+this.props.nn_path_type+'/'

        if (this.state.fileData != null) {
            listFile = this.state.fileData
        }

        //File upload Header
        let tableHeader = []; //make header
        let colDatas = ["File Name"]
        if(this.props.deletebtnflag == undefined || this.props.deletebtnflag == true ){
          colDatas = ["File Name", "Del"]
        }

        let headerData = []
        for (let i=0;i < colDatas.length;i++){
            headerData.push(<th key={k++} style={{"textAlign":"center"}} >{colDatas[i]}</th>)
        }
        
        tableHeader.push(<tr key={k++} >{headerData}</tr>)

        //File Upload Data
        let tableData = []; // make tabledata
        for(let rows in listFile){
            let colData = [];
            let row = listFile[rows]

            for(let cols in row){
                colData.push(<td key={k++} > {row[cols]} </td>) 
            }

            //add delete image
            if(this.props.deletebtnflag == undefined || this.props.deletebtnflag == true ){
              if(row["filename"] != null){
                  colData.push(<td key={k++} > <img style ={{width:20, "cursor":"pointer"}} alt = {row["filename"]}
                                                      onClick={this.deleteFileData.bind(this)} 
                                                      src="./images/del.png" /></td>)
              }
            }else{

            }
            
            
            tableData.push(<tr key={k++}>{colData}</tr>)
        }

        let fileTable = []
        fileTable.push(<thead ref='thead' key={k++} className="center">{tableHeader}</thead>)
        fileTable.push(<tbody ref='tbody' key={k++} className="center" >{tableData}</tbody>)
//"float":"left",
        return (
            <div>
                <h2 style={{"margin-right":"5px","verticalAlign":"top"}}>{this.props.title}</h2>
              {this.props.uploadbtnflag ?
                <div>
        
                <div> 
            
                    <FileUpload options={this.fileOption} >
                        <button ref="chooseAndUpload" id='fileeval' name = 'eval'>FileUpload</button>
                    </FileUpload></div>
                
                </div>
                :
                    <div>
                    </div>
                  }

                <div>
                    <table className="table detail" ref= 'master1' >
                        {fileTable}
                    </table>
                </div>

                {this.state.lineview ?
                    <div>
                        <h3>Line Progress {this.state.percent}%</h3>
                        <div style={{"width":'100%'}}>
                          <Line percent={this.state.percent} strokeWidth="1" strokeColor={'#3FC7FA'} />
                        </div>
                    </div>
                    :
                    <div>
                    </div>
                }
  
                </div>
        )
    }
}

FileUploadComponent.defaultProps = {
    reportRepository: new ReportRepository(new Api())
};
