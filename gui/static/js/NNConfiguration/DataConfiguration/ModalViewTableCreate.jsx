import React from 'react'
import ReportRepository from './../../repositories/ReportRepository';
import Api from './../../utils/Api';

export default class ModalViewTableCreate extends React.Component {
    constructor(props) {
        super(props);
        this.nameSpace = null;
        this.dataType = null;
        this.preProcess = null;
        this.cate = null;
        this.subCate = null;
        this.selectedTable = null;
        this.state = {
                tableName : null,
                tableRows : null,
                databaseName : null,
                categoryList : null,
                subCategoryList : null              
                };
    }

    // override : call after render
    componentDidMount(preProps, prevState){
        
    }

    //set category lov
    setCategoryLov(){  
        this.props.reportRepository.getCategoryList().then((categoryList) => {
            let rows = [];
            let i=0;
            for (let categoryName of categoryList['result']){
                rows.push(<option key={i++} value={categoryName}>{categoryName}</option>)
            }
            this.setState({categoryList : rows})
        });
    }

    //set subcategory lov
    setSubCategoryLov(obj){
        this.cate = obj.target.value
        this.props.reportRepository.getSubCategoryList(obj.target.value).then((subCategoryList) => {
            let rows = [];
            let i=0;
            for (let subCategoryName of subCategoryList['result']){
                rows.push(<option key={i++} value={subCategoryName}>{subCategoryName}</option>)
            }
            this.setState({subCategoryList : rows})
        });
    }

    //get table list on seleceted base name
    getTableList(){
        this.props.reportRepository.getNameSpaceList(this.dataType, this.preProcess , this.cate, this.subCate).then((ns) => {  
            console.log(ns['result']) 
            this.nameSpace = ns['result']
            let requestUrl = "base/" + ns['result'] + "/table/";
            this.props.reportRepository.getTableList(requestUrl).then((table_list) => {
            let rows = [];
            let i=0;
            for (let tableName of table_list['result']){
                rows.push(<tr key={i++}><td><input id={tableName} name ="modal" onClick={this.setSaveTableName.bind(this, tableName)} type="radio"/></td><td>{tableName}</td></tr>)
            }
            this.setState({tableRows : rows})
        });
        });
    }

    // add user request new table
    postTableName(){
        let requestUrl = this.get_add_url();
        this.props.reportRepository.postTableList(requestUrl, null).then((answer) => {
            this.getTableList()
        });;
    }

    //delete user request named table
    deleteTableName(){
        let requestUrl = this.get_delete_url();
        this.props.reportRepository.deleteTableList(requestUrl, null).then((answer) => {
            this.getTableList();
        });
    }

    //set table name on state variable
    setTableName(obj){
        this.setState({tableName: obj.target.value});
    }

    //set base name on state variable
    setDataType(obj){
        this.setCategoryLov()
        this.dataType = obj.target.value
    }

    //set base name on state variable
    setPreprocess(obj){
        this.setCategoryLov()
        this.preProcess = obj.target.value
    }

    //set sub category
    setSubCate(obj){
        this.subCate = obj.target.value
    }

    // combine post rest api url 
    get_add_url(){
        return "base/" + this.nameSpace + "/table/" + this.state.tableName + "/";
    }

    // combine delete rest api url 
    get_delete_url(){
        return "base/" + this.nameSpace + "/table/" + this.state.tableName + "/";
    }

    setSaveTableName(table){
        this.selectedTable = table
    }
    //
    saveModal(){
        this.props.saveModal(this.nameSpace, this.selectedTable)
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
                                    <col width="40" />
                                    <col width="40" />
                                    <col width="40" />
                                    <col width="40" />
                                    <col width="40" />
                                    <col width="40" />
                                    <col width="40" />
                                    <col width="40" />     
                                    <col width="40" />
                                </colgroup> 
                                <tbody>
                                <tr>
                                    <th>type</th>
                                    <td>
                                        <select onChange={this.setDataType.bind(this)} value={this.state.value}>
                                            <option value="">data type</option>
                                            <option value="frame">frame</option>
                                            <option value="image">image</option>
                                            <option value="text">text</option>
                                        </select>
                                    </td>
                                    <th>pre</th>
                                    <td>
                                         <select onChange={this.setPreprocess.bind(this)} value={this.state.value}>
                                            <option value="">preprocess</option>
                                            <option value="raw">raw</option>
                                            <option value="pre">pre</option>
                                        </select>
                                    </td>
                                    <th>Category</th>
                                    <td>
                                         <select onChange={this.setSubCategoryLov.bind(this)} value={this.state.value}>
                                            <option value="">category</option>
                                            {this.state.categoryList}
                                        </select>
                                    </td>
                                    <th>subcategory</th>
                                    <td>
                                         <select onChange={this.setSubCate.bind(this)} value={this.state.value}>
                                            <option value="">subcategory</option>
                                            {this.state.subCategoryList}
                                        </select>
                                    </td>
                                    <td>
                                        <button type="button" onClick={this.getTableList.bind(this)}>Search</button>
                                    </td>
                                </tr>
                                </tbody>
                            </table>
                            <table className="form-table align-left">
                                <colgroup>
                                    <col width="40" />
                                    <col width="300" />
                                </colgroup> 
                                <tbody>
                                <tr>
                                    <th>Modify</th>
                                    <td>
                                        <input type="text" name="tableName" placeholder="tableName" 
                                            onChange={this.setTableName.bind(this)} value={this.state.value} />
                                        <button type="button" onClick={this.postTableName.bind(this)}>Add</button>
                                        <button type="button" onClick={this.deleteTableName.bind(this)}>Delete</button>  
                                    </td>
                                </tr>
                                </tbody>
                            </table>
                            
                            <table className="table marginT10">
                                <colgroup>
                                    <col width="25" />
                                    <col width="300" />
                                </colgroup> 
                                <thead>
                                    <tr>
                                        <th><div>chk</div></th>
                                        <th><div>Table Name</div></th>
                                    </tr>
                                </thead>
                                <tbody className="center">      
                                    {this.state.tableRows}  
                                </tbody>
                            </table>
                        </article>
                    </div>
                </div>
                <span className="modal-footer">
                    <button onClick={this.saveModal.bind(this)}>Save</button>
                    <button onClick={this.props.closeModal}>Close</button>
                </span>
            </div>
        )
    }
} 

ModalViewTableCreate.defaultProps = {
    reportRepository: new ReportRepository(new Api())
};