import React from 'react'
import ReportRepository from './../../repositories/ReportRepository'
import Api from './../../utils/Api'
import SpinnerComponent from './../../NNLayout/common/SpinnerComponent'

export default class MetaStore_TableLayout extends React.Component {
	constructor(props) {
        super(props)
        this.state = {
            selectValue:[],//initail lodaing is meta
            cellfeature:{},
            dataFormatTypes:{},
            dataFormatTypesLabel:{},
            dataFramePost:null,
            celStateHeaderSelectBoxValue:{},
            WdnnTableColumnType:{},
            //selectedStyle : {}
            };
        this.celHeaderSelectBoxValue = {};
        this.celHeaderSelectBoxValue2 = {};
        this.first_time = true;
    }
     componentDidUpdate() {
           this.getCategoryType3(this.props.WdnnTableColumnType)
    }
    setWdnnTableColumnType()
    {
            this.first_time = true;
    }
    /*
    calWdnnTableColumnType()
    {
        console.log("calWdnnTableColumnTypechild")
        if(!this.props.WdnnTableColumnType) {return null;}
        console.log("calWdnnTableColumnTypechild")
        let CalWdnnTableColumnType = {}
        for(let columnValuesType of this.props.WdnnTableColumnType){
            console.log(columnValuesType)
        }

    }

    shouldComponentUpdate(nextProps, nextState){
        console.log("shouldComponentUpdate: " + JSON.stringify(nextProps) + " " + JSON.stringify(nextState));
        return true;
    }
    */
    handleChange(selectedValue){
        let selectDataFormatType = this.state.dataFormatTypes
        let selectDataFormatLabel = this.state.dataFormatTypesLabel
        let selectCellFeature = this.state.cellfeature
        let selectDataFormatTypeCell = {}
        let selectDataFormatTypeLabel = {}
        let _celHeaderSelectBoxValue = {}
        let _celHeaderSelectBox = {}
        _celHeaderSelectBoxValue["conlumn_type"] = selectedValue.target.value
        _celHeaderSelectBox[selectedValue.target.id] = _celHeaderSelectBoxValue
        this.setState({celStateHeaderSelectBoxValue:_celHeaderSelectBox})

        //CONTINUOUS CATEGORICAL
        if ('CATEGORICAL' == selectedValue.target.value){
            selectDataFormatTypeCell['column_type'] = selectedValue.target.value
            selectDataFormatType[selectedValue.target.id] = selectDataFormatTypeCell
            this.setState({dataFormatTypes : selectDataFormatType})
            selectedValue.target.className = "selected"
        }
        else if ('CONTINUOUS' == selectedValue.target.value){
            selectDataFormatTypeCell['column_type'] = selectedValue.target.value
            selectDataFormatType[selectedValue.target.id] = selectDataFormatTypeCell
            this.setState({dataFormatTypes : selectDataFormatType})
            selectedValue.target.className = "selected"
        }
        else if ('LABEL' == selectedValue.target.value){
            selectDataFormatTypeLabel['column_type'] = selectedValue.target.value
            selectDataFormatLabel[selectedValue.target.id] = selectDataFormatTypeLabel
            this.setState({dataFormatTypesLabel : selectDataFormatLabel})
            selectedValue.target.className = "selected"
        }
        else if ('NONE' == selectedValue.target.value){
            selectedValue.target.className = ""
        }
        selectCellFeature['cell_feature'] = selectDataFormatType
        selectCellFeature['label'] = selectDataFormatLabel
        this.setState({cellfeature : selectCellFeature}) 
        this.celHeaderSelectBoxValue2 = selectCellFeature;
    }
    dataFramePost(opt_url){
        //error check assert
        msg.show("upload start")
        this.props.reportRepository.postWdnnDataFrameFormat(opt_url,this.state.cellfeature).then((resultData) => {
            if(resultData['status'] == "200"){
                msg.show("upload Finished")
            }
        });
    }
/*
    checkColumnDataType(){
        var numbers = [1, 4, 9];
        var dic_number = {"one":1, "two":2, "three":3}
        let flag = this.state.cellfeature
        console.log(flag)
        for (let [k, v] of Object.entries(flag)) {
            // do something with k and v
            console.log(k)
            console.log(v)
        } 
    }

    getDataFrameType () {
        console.log("ChildGetDataFrameType"); 
        if (!this.props.WdnnTableColumnType) {return null;}
    	
        for (let[k,v] of Object.entries(this.props.WdnnTableColumnType)){
            console.log(k); 
            console.log(v);
            }
        
     }
     */
    setWdnnTableColumnType()
    {
        this.props.reportRepository.getDataFrameOnNetworkConfig().then((resultData) => {
            this.setState({WdnnTableColumnType: resultData['result']});
            this.celHeaderSelectBoxValue = resultData['result'];
        });
        
    }

    getCategoryType2(WdnnTableColumnType)
    {
        let _celHeaderSelectBoxValue = {}
        let _celHeaderSelectBox = {}
        let _WdnnTableColumnType = {}

        if (this.first_time == true){
            _WdnnTableColumnType = WdnnTableColumnType
        }else{
            _WdnnTableColumnType = this.celHeaderSelectBoxValue
        }

        for(let columnValues of this.props.WdnnTableData[0])
        {
            try{
            _celHeaderSelectBoxValue["column_type"] = _WdnnTableColumnType[columnValues]["column_type"]
            }catch(e)
            {
            _celHeaderSelectBoxValue["column_type"] = "NONE"
            }
            _celHeaderSelectBox[columnValues] = _celHeaderSelectBoxValue

        }
        this.celHeaderSelectBoxValue = _celHeaderSelectBox
        this.first_time =false

        return this.celHeaderSelectBoxValue
    }
    getCategoryType3(WdnnTableColumnType)
    {

        if (!this.props.WdnnTableColumnType) {
            let column_type = {}
            let row_column_type = {}
            this.celHeaderSelectBoxValue2 = null
        }
        else{
            let _celHeaderSelectBoxValue = {}
            let _celHeaderSelectBox = {}
            let _WdnnTableColumnType = {}

            if (this.first_time == true){
                _WdnnTableColumnType = this.props.WdnnTableColumnType
            }else{
                _WdnnTableColumnType = this.celHeaderSelectBoxValue
            }

            this.first_time =false
            this.celHeaderSelectBoxValue2 = _WdnnTableColumnType 
        }

        return this.celHeaderSelectBoxValue2
    }

    render() {
        let metaStoreTableContent = [];
    	let i=0;
        let j=0;
        let k=0;
        //let tableHeaderCategory = []; //make Category
        let tableHeader = []; //make header
        let tableData = []; // make tabledata

        let noneSelected = null;
        let cateSelected = null;
        let contiSelected = null;
        let labelSelected = null;
        let getColumnType = {};

        if(!this.props.WdnnTableData){
            return (<div></div>)
        }

		for(let rows of this.props.WdnnTableData){

            let celHeaderCategory = [];
            let celHeaderCategory1 = [];
            let celHeaderCategory2 = [];
            let celHeader = [];
            let celData = [];
			for(let columnValues of rows){
                //add colums
                if( j==0 ){
                    let celHeaderCategoryTypeNone = [];
                    let celHeaderCategoryTypeConti = [];
                    let celHeaderCategoryTypeCate = [];
                    let celHeaderCategoryTypelabel = [];

                    if (this.celHeaderSelectBoxValue2 && this.celHeaderSelectBoxValue2[columnValues]){
                     celHeaderCategory.push(    <td key={k++}>
                                                    <div className="option-select">
                                                    <select ref="s1" onChange={this.handleChange.bind(this)}
                                                           id={columnValues} defaultValue={this.celHeaderSelectBoxValue2[columnValues]["column_type"]} className={this.celHeaderSelectBoxValue2[columnValues]["column_type"]!="NONE"?"selected":null}>
                                                       <option value="NONE">None</option>
                                                       <option value="CATEGORICAL">Category Type</option>
                                                       <option value="CONTINUOUS">Continuous Type</option>
                                                       <option value="LABEL">Label</option>
                                                    </select>
                                                    </div>
                                                </td>)
                    }else{
                                  celHeaderCategory.push(    
                                                <td key={k++}>
                                                    <div className="option-select">
                                                    <select ref="s1" onChange={this.handleChange.bind(this)}
                                                           id={columnValues}>
                                                       <option value="NONE">None</option>
                                                       <option value="CATEGORICAL">Category Type</option>
                                                       <option value="CONTINUOUS">Continuous Type</option>
                                                       <option value="LABEL">Label</option>
                                                    </select>
                                                    </div>
                                                </td>)
                    }

                    celHeader.push(<th key={i++} > {columnValues}</th>)
                }else{
                    celData.push(<td key={i++} > {columnValues}</td>)
                }
			}
            //add rows
            if(j==0){
                tableHeader.push(<tr className="option-select" key={j++}>{celHeaderCategory}</tr>)
                tableHeader.push(<tr key={j++}>{celHeader}</tr>)
            }else{
                tableData.push(<tr key={j++}>{celData}</tr>)
            }
		}

        //add table 
        metaStoreTableContent.push(<thead key={j++}>{tableHeader}</thead>)
        metaStoreTableContent.push(<tbody key={j++} className="center">{tableData}</tbody>)

        return (   
            <div>
                <table className="table marginT10">
                    {metaStoreTableContent}
                </table>
            </div>        
        )
    }
}
MetaStore_TableLayout.defaultProps = {
    reportRepository: new ReportRepository(new Api())
};
