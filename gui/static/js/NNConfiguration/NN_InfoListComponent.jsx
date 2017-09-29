import React from 'react';
import Api from './../utils/Api'
import Modal from 'react-modal';
import { BootstrapTable, TableHeaderColumn } from 'react-bootstrap-table';
import ReportRepository from './../repositories/ReportRepository'


export default class NN_InfoListComponent extends React.Component {
    constructor(props, context) {
        super(props);
        this.state = {
            tableData:null,
            NN_TableData:null,
            NN_TableDataFilter:null,
            NN_TableDataCheck:[],
            NN_TableColArr:[ {index:0, id:"sel",            name:"Sel"}
                            ,{index:1, id:"biz_cate",       name:"Category"}
                            ,{index:2, id:"biz_sub_cate",   name:"SubCategory"}
                            ,{index:3, id:"nn_title",       name:"Title"}
                            ,{index:4, id:"nn_desc",        name:"Description"}
                            ,{index:5, id:"dir",            name:"Network Type"}
                            ,{index:6, id:"autosingle",     name:"Train Type"}
                            ,{index:7, id:"nn_id",          name:"ID"}
                            ,{index:8, id:"nn_wf_ver_id",   name:"Ver"}
                            ],
            selModalView: null,
            NN_ID : null,
            nextpageInit:"init",
            nn_color:"#14c0f2",
            NN_TableAPI:null
        };
    }

    componentDidMount(){
        this.getCommonNNInfo("all");// 화면에 들어 올때 검색을 해준다.
        this.props.setActiveItem(this.state.nextpageInit,'U',null,null,null,null,null,null);//테이블의 NNID를 클릭할때 넘어갈수 있게 초기화를 해준다.
    }

    getCommonNNInfo(params) {
        this.props.reportRepository.getCommonNNInfo(params).then((tableData) => {
            this.setState({ NN_TableData: null })//조회시 한번 Reset을 해주어야 테이블이 새로고침 된다.
            this.setState({ NN_TableData: tableData['fields'] })//조회한 것을 화면에 반영한다.
            this.state.NN_TableDataFilter = tableData['fields']//Filter Search할때 기준이 되는 데이터를 넘겨준다.
        });   
    }

    searchCommonNNInfo() {
        this.state.NN_TableDataCheck = []
        this.refs.search_text.value = null
        this.getCommonNNInfo("all")
    }

    deleteCommonNNInfo(params) { 
        let nn_id = ''
        let re = confirm( "Are you delete?" )
        let table = this.refs.master2
        if(re == true){
            for(let i=1 ; i < table.rows.length ; i++){
                let key = table.rows[i].children[0].children.rd1
                if(key.checked == true){
                    nn_id = key.alt
                    params = { use_flag : 'N' }
                    this.props.reportRepository.putCommonNNInfo(nn_id, params).then((tableData) => {
                        this.getCommonNNInfo("all");
                    });
                }
            }
        }
    }

    findColInfo(col, idxType, idxName){
        let fItem = ""
        if(idxType == "index"){
            fItem = col.find(data => { return data.index == idxName})
        }else if(idxType == "id"){
            fItem = col.find(data => { return data.id == idxName})
        }else if(idxType == "name"){
            fItem = col.find(data => { return data.name == idxName})
        }

        return fItem
    }

    updateCommonNNInfo(params){   
        let nn_id = ''
        let bc = ''
        let bc_sub = ''
        let bc_title = ''
        let bc_desc = ''
        let re = confirm( "Are you update?" )
        let col = this.state.NN_TableColArr
        let table = this.refs.master2
        if(re == true){
            for(let i=1 ; i < table.rows.length ; i++){
                let key = table.rows[i].children[0].children.rd1
                if(key.checked == true){

                    bc = table.rows[i].children[this.findColInfo(col, "id", "biz_cate").index].children[0].value
                    bc_sub = table.rows[i].children[this.findColInfo(col, "id", "biz_sub_cate").index].children[0].value
                    bc_title = table.rows[i].children[this.findColInfo(col, "id", "nn_title").index].children[0].value
                    bc_desc = table.rows[i].children[this.findColInfo(col, "id", "nn_desc").index].children[0].value
                    nn_id = table.rows[i].children[this.findColInfo(col, "id", "nn_id").index].innerText

                    params = { biz_cate : bc, biz_sub_cate : bc_sub, nn_title: bc_title, nn_desc :bc_desc }
                    this.props.reportRepository.putCommonNNInfo(nn_id, params).then((tableData) => {
                        this.getCommonNNInfo("all");
                    });
                }
            }
        }
        this.searchCommonNNInfo()
    }

    handleChange(selectedValue){
        let value = selectedValue.target.alt //radio button cell
        let table = this.refs.master2
        if(value != undefined){// key, desc cell
            for(let i=1 ; i < table.rows.length ; i++){
                let key = table.rows[i].children[0].children.rd1
                if(key.alt == value){
                    key.checked = true
                    this.handleClickCheckBox(key)
                }
            }
        }
    }

    handleSearch(value){
        let filterBy = value.target.value.toString().toLowerCase();
        let size = this.state.NN_TableDataFilter.length;
        let col = this.state.NN_TableColArr
        let filteredList = [];
        for (let index = 0; index < size; index++) {
            for(let colidx = 1; colidx < col.length ; colidx ++ ){
                let v = this.state.NN_TableDataFilter[index][this.findColInfo(col, "index", colidx).id];
                if (v != null && v.toString().toLowerCase().indexOf(filterBy) !== -1) {
                    filteredList.push(this.state.NN_TableDataFilter[index]);
                    break;
                }
            } 
        }

        this.setState({
            NN_TableData: filteredList,
        });
    }

    handleClick(row){// Table Cell Clcik and Call Net Detail
        this.props.setActiveItem(row["nn_id"], 'U', null, null, null, null, null, null);
        return this.props.getHeaderEvent(2); //call Net Info 
    }

    handleClickCheckBox(value){//마지막 체크 박스 클릭 한 것을 체크 한다.
        let checkbox = value.target
        if(checkbox == undefined){
            checkbox = value
        }
        if(checkbox.checked == true){
            value = checkbox.alt
            this.state.NN_TableDataCheck.push(value)
            this.props.setActiveItem(value, 'U', null, null, null, null, null, null);
        }else{
            value = checkbox.alt
            let fidx = this.state.NN_TableDataCheck.indexOf(value)
            if(fidx != -1){
                this.state.NN_TableDataCheck.splice(fidx,1)
            }
            value = this.state.NN_TableDataCheck[this.state.NN_TableDataCheck.length-1]
            if(value == undefined){
                this.props.setActiveItem(this.state.nextpageInit, 'U', null, null, null, null, null, null);
            }else{
                this.props.setActiveItem(value, 'U', null, null, null, null, null, null);
            }
        }
    }

    addCommonNNInfo(params) {//Add New Button Click and Call Net Create   
        return this.props.getHeaderEvent(4); 
    }

    render() {
        let k = 1
        // Data sort
        function sortByKey(array, key) {
            return array.sort(function(a, b) {
                var x = a[key]; var y = b[key];
                return ((x < y) ? -1 : ((x > y) ? 1 : 0));
            });
        }

        function sortData(data, id){
            let nnInfoNewList = [];
            if (data != null) {
                for (var i in data) {
                    nnInfoNewList[i] = data[i];
                }
            }

            nnInfoNewList = sortByKey(nnInfoNewList, id);
            return nnInfoNewList
        }
        
        // Make header
        function makeHeader(data){
            let headerData = []
            for(let i in data){
                headerData.push(<th key={k++} style={{"textAlign":"center"}} >{data[i].name}</th>)
            }
            let tableHeader = []; //make header
            tableHeader.push(<tr key={k++} >{headerData}</tr>)
            return tableHeader
        }

        this.state.NN_TableData = sortData(this.state.NN_TableData, "nn_id")
        let tableHeader = makeHeader(this.state.NN_TableColArr)

        //Network Select Data
        let tableData = []; // make tabledata

        for(let rows in this.state.NN_TableData){
            let colData = [];
            let row = this.state.NN_TableData[rows]
            let autokeys = Object.keys(row["automl_parms"])

            colData.push(<td key={k++} > < input type = "checkbox" name="rd1"
                                                                    alt = {row["nn_id"]}
                                                                    onClick = {this.handleClickCheckBox.bind(this)}
                                                                    style={{"textAlign":"center", "width":"100%"}} />  </td>)
            // colData.push(<td key={k++} > < input type = {"string"} style={{"textAlign":"center", "width":"100%"}} defaultValue = {row["biz_cate"]}
            //                                             maxLength = "10"
            //                                              alt = {row["nn_id"]} onChange = {this.handleChange.bind(this)} />  </td>)
            // colData.push(<td key={k++} > < input type = {"string"} style={{"textAlign":"center", "width":"100%"}} defaultValue = {row["biz_sub_cate"]} 
            //                                             maxLength = "10"
            //                                              alt = {row["nn_id"]} onChange = {this.handleChange.bind(this)} />  </td>)
            // colData.push(<td key={k++} > < input type = {"string"} style={{"textAlign":"center", "width":"100%"}} defaultValue = {row["nn_title"]} 
            //                                              maxLength = "100"
            //                                              alt = {row["nn_id"]} onChange = {this.handleChange.bind(this)} />  </td>)
            // colData.push(<td key={k++} > < input type = {"string"} style={{"textAlign":"center", "width":"100%"}} defaultValue = {row["nn_desc"]} 
            //                                              maxLength = "5000"
            //                                              alt = {row["nn_id"]} onChange = {this.handleChange.bind(this)} />  </td>)
            
            colData.push(<td key={k++} alt = {row["nn_id"]} > {row["biz_cate"]} </td>) 
            colData.push(<td key={k++} alt = {row["nn_id"]} > {row["biz_sub_cate"]} </td>) 
            colData.push(<td key={k++} alt = {row["nn_id"]} > {row["nn_title"]}  </td>) 
            colData.push(<td key={k++} alt = {row["nn_id"]} > {row["nn_desc"]} </td>) 



            colData.push(<td key={k++} alt = {row["nn_id"]} > {row["dir"]} </td>) 
            if(autokeys.length == 0){
                colData.push(<td key={k++} alt = {row["nn_id"]} > {"Single"} </td>) 
            }else{
                colData.push(<td key={k++} alt = {row["nn_id"]} > {"Auto"} </td>) 
            }
            colData.push(<td key={k++} alt = {row["nn_id"]} 
                                style ={{"color":this.state.nn_color, "cursor":"pointer", "fontWeight":"bold"}}
                                onClick={() => this.handleClick(row) } > {row["nn_id"]} </td>) 
            colData.push(<td key={k++} alt = {row["nn_id"]} > {row["nn_wf_ver_id"]} </td>)

            tableData.push(<tr key={k++}>{colData}</tr>)
        }


        let nnInfoNewListTable = []
        nnInfoNewListTable.push(<thead ref='thead' key={k++} className="center">{tableHeader}</thead>)
        nnInfoNewListTable.push(<tbody ref='tbody' key={k++} className="center" >{tableData}</tbody>)

                    //         <div>
                    //     <h1> Network List </h1>
                    //     < input type = {"string"} style={{ "width":500, "height":30}}
                    //                 placeholder="Search for names.." ref='search_text'
                    //                  onChange = {this.handleSearch.bind(this)} />
                    //     <br style={{ "height":20}}></br>

                    // </div>
                        // <button type="button" className="search" onClick={() => this.searchCommonNNInfo()} >Search</button> 
                        // <button type="button" className="modify" onClick={() => this.updateCommonNNInfo()} >Modify</button>
        return (
            <section>
                <h1 className="hidden">tensor MSA main table</h1>
                <div className="container paddingT10">
                    <div className="tblBtnArea">
                        <button type="button" className="addnew" 
                                style={{"marginRight":"5px"}}
                                onClick={() => this.addCommonNNInfo() } >Add Net</button>
                        <button type="button" className="delete" onClick={() => this.deleteCommonNNInfo()} >Delete</button>
                    </div>

                    <div>
                        <h1 className="bullet"> Network List </h1>
                        <table className="table detail" ref= 'master2' >
                            {nnInfoNewListTable}
                        </table>
                    </div>

                </div>
            </section>
        );
    }
}

NN_InfoListComponent.defaultProps = {
    reportRepository: new ReportRepository(new Api())
};

