import React from 'react';
import MetaStore_TableLayout from './MetaStore_TableLayout';
import ReportRepository from './../../repositories/ReportRepository';
import Api from './../../utils/Api';
import ModalViewWdnnCsvCreate from './ModalViewWdnnCsvCreate';
import Modal from 'react-modal';
import FileUpload from 'react-fileupload'; //why?? 

export default class MetaStoreConfigurationComponent extends React.Component {
    
    constructor(props) {
        super(props);
        this.saveModal = this.saveModal.bind(this);
        this.closeModal = this.closeModal.bind(this);
        this.databaseName = null,
        this.tableName = null,
        this.c_tableName = null;
        this.networkId = null;
        this.state = {  
                MetaStore_TableLayout : null,
                WdnnTableData : null,
                WdnnTableColumnType:null,
                dataFormatTypes : {},
                selModalView : null,
                uploadFileList : [],
                tableRows : null,
                dataBaseList : null,
                tableList : null,
                nnid : null,
                baseDom : null,
                tableDom : null,
                };
                        
            //this.addDataframeType = this.addDataframeType.bind(this, param);                 
    }
    //when page called on first 
    componentDidMount(){
        this.setState({nnid: this.context.NN_ID})
        this.networkId = this.context.NN_ID
        this.initDataBaseLov()
        console.log(this.state.dataBaseList)       
    }
    saveModal(base, table) { 
        this.databaseName = base
        this.tableName = table
        this.setState({baseDom : base})
        this.setState({tableDom : table})
        this.setState({open: false});
    }
        // combine get rest api url getNetBaseInfo

 
    get_searchUrl(){
        return "base/" + this.state.databaseName + "/table/" ;
    }
        // 
    initDataBaseLov(){
        console.log("initDataBaseLov")
        console.log(this.state.nnid)
        this.props.reportRepository.getNetBaseInfo(this.networkId).then((nnBaseInfo) => {
            console.log(nnBaseInfo['result'])
            let base = nnBaseInfo['result'][0]['fields']['dir'];
            let table = nnBaseInfo['result'][0]['fields']['table'];   
            this.setState({baseDom : base});
            this.setState({tableDom : table});
            if(base && table){
                this.search_btn() ;
            }
            
        });
    }
    // init table lov

    search_btn(){
        let limit_cnt = {}
        limit_cnt["limits"] = 0
        let opt_url =  this.state.baseDom + '/table/' + this.state.tableDom + '/data/'
        this.props.reportRepository.getWdnnTableDataFromHbase(opt_url).then((tableData) => {
            console.log('data configuration search end')
        if(tableData['status'] == '200'){
            this.setState({WdnnTableData: tableData['result']})
        }
        });

        let colum_type = this.getDataframeColumnOnDataConfig()    
    }

    child_dataframe_format_post_btn(params){
        let opt_url =  this.state.baseDom + '/table/' + this.state.tableDom + '/format/' + this.state.nnid + '/'
        this.refs.child.dataFramePost(opt_url)
    }
    child_check_Column_dataType(){
         this.refs.child.getDataFrameType()
    }
    openModal(type){
        this.setState({selModalView : <ModalViewWdnnCsvCreate saveModal={this.saveModal} closeModal={this.closeModal}/>})
        this.setState({open: true})
    }
    closeModal () { this.setState({open: false}); }
        //get table list on seleceted base name
    getTableListOnDataConfig(){
        console.log("getTableListOnDataConfig")
        console.log(this.state.databaseName)
        //let requestUrl = this.get_searchUrl();
        this.props.reportRepository.getTableListOnDataConfig(this.state.databaseName).then((table_list) => {
        let option = [];
        let i=0;
        for (let tableNameValue of table_list['result']){
            option.push(<option key={i++} value={tableNameValue}>{tableNameValue}</option>)
        }
        this.setState({tableList : option})
        });
    }

    getDataBaseOnDataConfig(){
        //let request
        this.props.reportRepository.getDataBaseOnDataConfig().then((database_list) => {
            let optionRows = [];
            let i=0;
            for (let dbName of database_list['result']){
                optionRows.push(<option key={i++} value={dbName}>{dbName}</option>)
            }
            this.setState({dataBaseList : optionRows})
        });
    }
    getDataframeColumnOnDataConfig(){
        //let request
        let col_type = {}
        this.props.reportRepository.getDataFrameOnNetworkConfig("all", this.context.NN_ID).then((column_type) => {
            let optionRows = [];
            let i=0;

            col_type = column_type['result']
            this.setState({WdnnTableColumnType:col_type})  
        });
        return col_type
    }
    setDataBaseOnDataConfig(obj)
    {
        console.log(obj.target.value)
        //let selectedDatabaseName = this.state.databaseName
        this.setState({databaseName: obj.target.value}, function(){this.getTableListOnDataConfig()});
        console.log("setDataBaseOnDataConfig")
        console.log(this.state.databaseName)
        
    }
    setTableListOnDataConfig(obj)
    {
        console.log(obj.target.value)
        let selectedtb = obj.target.value
        //let selectedTablename = this.state.tablename
        //this.setState({tablename: selectedtb, function(){render()}});
        this.c_tableName = obj.target.value 
        //c_tableName =  obj.target.value
        console.log(this.c_tableName)
    }
    wdnnconfPost(opt_url){
        console.log("dataframpost")
          let _url =  this.state.nnid+"/"
          let wdnn_conf = {}
          wdnn_conf['layer'] = [50,70,50]
        this.props.reportRepository.postWdnnConf(_url,wdnn_conf).then((resultData) => {
            if(resultData['status'] == "200"){
                alert("정상 처리 되었습니다.")
            }
        }); 
    }
    wdnnTrainPost(){
        console.log("wdnnTrainPost")
        console.log(this.state.nnid)
        
        let _url =  this.state.nnid+"/"
        this.props.reportRepository.postWdnnTrain(_url).then((resultData) => {
            console.log('dataframepost results')
            if(resultData['status'] == "200"){
                alert("정상 처리 되었습니다.")
            }
            //this.setState({dataFramePost: resultData['result']})
        });
    }
    wdnnEvalPost(){
        console.log("wdnnEvalPost")
        console.log(this.state.nnid)
        
        let _url =  this.state.nnid+"/"
        this.props.reportRepository.postWdnnEval(_url).then((resultData) => {
            console.log('dataframepost results')
            if(resultData['status'] == "200"){
                alert("정상 처리 되었습니다.")
            }
            //this.setState({dataFramePost: resultData['result']})
        });
    }

    render() {
        return (
                       <div className="container tabBody">
                            <div id="tab1">
                                <article>
                                <div className="inner-btnArea">
                                    <button type="button" className="btn imgBtn search" onClick={() => this.search_btn()} >Search</button>
                                    <button className="btn imgBtn save" type="button" onClick={() => this.child_dataframe_format_post_btn(this)} >Format Save</button>
                                    <button className="btn imgBtn upload" onClick={this.openModal.bind(this ,'table')}>Upload</button>
                                </div>
                                    <table className="form-table align-left">
                                        <colgroup>
                                            <col width="10%"/>
                                            <col width="10%"/>
                                            <col width="10%"/>
                                            <col width="10%"/>
                                            <col width="60%"/>
                                        </colgroup> 
                                        <tbody>
                                        <tr>
                                            <th>Data Base List</th>
                                            <td>
                                                {this.state.baseDom}
                                            </td>
                                            <th>Table List</th>
                                            <td>
                                                {this.state.tableDom}
                                            </td>
                                            <td>

                                            </td>
                                        </tr>
                                        </tbody>
                                    </table>
                                    <MetaStore_TableLayout WdnnTableData={this.state.WdnnTableData} WdnnTableColumnType={this.state.WdnnTableColumnType} ref="child"/>
                                </article>
                                <Modal className="modal" overlayClassName="modal" isOpen={this.state.open}
                                        onRequestClose={this.closeModal}>
                                    <div className="modal-dialog modal-lg">
                                      {this.state.selModalView}
                                    </div>
                                </Modal>                        
                            </div>
                        </div>
        )
    }
}
MetaStoreConfigurationComponent.defaultProps = {
    reportRepository: new ReportRepository(new Api())
};

MetaStoreConfigurationComponent.contextTypes = {
    NN_ID: React.PropTypes.string
};