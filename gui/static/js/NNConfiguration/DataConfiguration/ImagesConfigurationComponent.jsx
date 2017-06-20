import React from 'react';
import ImagePreviewLayout from './ImageData_PreviewLayout';
import ReportRepository from './../../repositories/ReportRepository';
import Api from './../../utils/Api';
import FileUpload from 'react-fileupload';
import ModalViewTableCreate from './ModalViewTableCreate';
import ModalViewLabelCreate from './ModalViewLabelCreate';
import ModalViewFormatCreate from './ModalViewFormatCreate';
import ReactDOM from 'react-dom';
import Modal from 'react-modal';

export default class ImagesConfigurationComponent extends React.Component {
    constructor(props) {
        super(props);
        this.closeModal = this.closeModal.bind(this);
        this.networkId = null;
        this.saveModal = this.saveModal.bind(this);
        this.databaseName = null;
        this.tableName = null;
        this.labelName = null;
        this.xSize = null;
        this.ySize = null;
        this.state = {
                imagePaths : null,
                formAction : null,
                uploadFileList : [],
                rate : 0,
                selModalView : null,
                tableSelectList : null,
                formatData : {},
                baseDom : null,
                tableDom : null,
                domSizeX : null, 
                domSizeY : null,
                setBtn : null
                };
    }

    //when page called on first 
    componentDidMount(){
        this.networkId = this.context.NN_ID
        this.initDataBaseLov();
    }

    // 
    initDataBaseLov(){
        this.props.reportRepository.getNetBaseInfo(this.networkId).then((nnBaseInfo) => {
            let base = nnBaseInfo['result'][0]['fields']['dir'];
            let table = nnBaseInfo['result'][0]['fields']['table'];   
            this.setState({baseDom : base});
            this.setState({tableDom : table});
            if(base && table){
                this.initTableLov(base, table); 
            }else{
                this.initTableLov('all', 'all'); 
            }
        });
    }

    // init table lov
    initTableLov(base, table){

        let requestUrl = "base/" + base + "/table/" + table + "/format/" + this.networkId + "/";
            this.props.reportRepository.getImageFormatData(requestUrl, "").then((format) => {
                let formatData = format['result']
                let xSize = formatData['x_size'];
                let ySize = formatData['y_size'];
                let setBtn = "";

                if(!xSize){
                    xSize = <input type="text" name="xsize" placeholder="xsize" 
                                            onChange={this.setXSize.bind(this)} value={this.state.xSize} /> 
                    setBtn = <button onClick={this.postFormatData.bind(this)}>SET</button> 
                } 

                if(!ySize){
                    ySize= <input type="text" name="ysize" placeholder="ysize" 
                                            onChange={this.setYSize.bind(this)} value={this.state.ySize} />
                    setBtn = <button onClick={this.postFormatData.bind(this)}>SET</button>
                }
                this.setState({domSizeX : xSize});
                this.setState({domSizeY : ySize});  
                this.setState({setBtn : setBtn});
                this.searchBtn(this.networkId);
            });       
    }

    // post format data
    postFormatData(){
        let requestUrl = "base/" + this.databaseName + "/table/" + this.tableName
        + "/format/" + this.networkId + "/";
        let formatSize = {"x_size" : this.xSize, "y_size" : this.ySize}

        this.props.reportRepository.postImageFormatData(requestUrl, formatSize).then((format) => {
            this.initDataBaseLov();
        });
    }

    // on Search button event occurs 
    searchBtn(nnid){
        this.props.reportRepository.getPreviewImagePath(this.networkId).then((previewPaths) => {
            this.setState({imagePaths: previewPaths['result']})
        });
    }

    // on label name
    setXSize(obj){
        this.xSize = obj.target.value;
    }
    
    // on label name
    setYSize(obj){
        this.ySize = obj.target.value;
    }

    //route modal view 
    openModal(type){
        if(type == 'table'){
            this.setState({selModalView : <ModalViewTableCreate saveModal={this.saveModal} closeModal={this.closeModal}/>} )
        }
        else if (type == 'label'){
            this.setState({selModalView : <ModalViewLabelCreate networkId={this.networkId} closeModal={this.closeModal.bind(this)} searchBtn={this.searchBtn.bind(this)}/>})
        }
        this.setState({open: true})
    }

    // close modal 
    closeModal() { this.setState({open: false}); }

    // save modal 
    saveModal(base, table) { 
        this.databaseName = base
        this.tableName = table
        this.setState({baseDom : base})
        this.setState({tableDom : table})
        this.setState({open: false});
    }

    render() {
        return (
            <div className="container tabBody">
                <div id="tab1">
                    <article>
                        <table className="form-table align-left">
                            <colgroup>
                            <col width="40" />
                            <col width="40" />
                            <col width="40" />
                            <col width="40" />
                            <col width="40" />
                            <col width="40" />
                            <col width="60" />
                            <col width="100" />
                            <col width="250" />
                            </colgroup>
                            <tbody>
                                <tr>
                                    <th>Network ID</th>
                                    <td width>{this.networkId}</td>
                                    <th>*DataBase</th>
                                    <td width>
                                        {this.state.baseDom}
                                    </td>
                                    <th>*Table</th>
                                    <td width>
                                        {this.state.tableDom}
                                    </td>
                                    <th>*Format</th>
                                    <td width>
                                        <p>{this.state.domSizeX} x {this.state.domSizeY}</p>
                                    </td>
                                    <td width>
                                        {this.state.setBtn}
                                        <button onClick={this.openModal.bind(this ,'table')}>table</button>
                                        <button onClick={this.openModal.bind(this ,'label')}>label</button>
                                        <button type="button" onClick={() => this.searchBtn()}>Search</button>
                                    </td>
                                </tr>
                            </tbody>
                        </table>
                        
                        <Modal
                            className="modal"
                            overlayClassName="modal"
                            isOpen={this.state.open}
                            onRequestClose={this.closeModal}>
                            <div className="modal-dialog modal-lg">
                                {this.state.selModalView}
                            </div>
                        </Modal>
                        
                        <div className="img-box-wrap">
                                <ImagePreviewLayout imageDataSet={this.state} netId={this.networkId}/>
                        </div>
                    </article>
                </div>
            </div>
        )
    }
}

ImagesConfigurationComponent.defaultProps = {
    reportRepository: new ReportRepository(new Api())
};

ImagesConfigurationComponent.contextTypes = {
    NN_ID: React.PropTypes.string
};
