import React from 'react'
import EnvConstants from './../../constants/EnvConstants';
import ReportRepository from './../../repositories/ReportRepository'
import Api from './../../utils/Api'
const FileUpload = require('react-fileupload');
import { Line, Circle } from 'rc-progress';

export default class JsonConfComponent extends React.Component {
	constructor(props) {
        super(props)
        this.state = {
            fileData:null,
            nn_id:null,
            nn_wf_ver_id:null,
            color : "#14c0f2",
            lastdata:"last",
            arrayData : "[ ]",
            jsonData : "{ }",
            config:{}
        };
        this.getConfigData = this.getConfigData.bind(this);
    }
    
    componentDidMount() {
    
    }

    // getConfigData에서 Table 값을 가져와 로우 단위로 값을 편성하여 Json을 만들기 쉽게 하기 위함이다.
    setConfigData(data){
        let redata = []
        let childcnt = data.childElementCount // Table Cell Child Count
        let text = data.textContent.trim() // Table Cell Text innerText
        let rowspan = data.rowSpan // Table Cell RowSpan
        let edit = data.contentEditable // Table Cell Editable
        let type = data.getAttribute("type") // Table Last Cell Type ex) number, string

        let lastdata = ""
        if(data.attributes.alt != undefined){
            lastdata = data.attributes.alt.value
        }
        // let color = data.style.color

        if(childcnt > 0){// 마지막 값인 경우 childcnt를 가진다.
            let childN = data.children[0]
            // Select Box의 선택 값을 가져와 넣어준다.
            if(childN != undefined && childN.childNodes[0] != undefined && childN.childNodes[0].type == "select-one"){
                let selectedValue = ""
                if(childN.childNodes[0].selectedOptions[0] != null){
                   text = childN.childNodes[0].selectedOptions[0].value
                }
                type = "sel"
                // color = childN.childNodes[0].style.color
                lastdata = this.state.lastdata
            }else{// 일반적인 Text 값을 가져온다.
                text = data.children[0].value
                type = data.children[0].type
            }

            rowspan = 1
            edit = "true"
        }

        if(type == "number"){
            type = "int"
        }else if(type == "string"){
            type = "str"
        }

        redata.push(text)
        redata.push(rowspan)
        redata.push(edit)
        redata.push(type)
        redata.push(lastdata)

        return redata
    }

    // Table에 있는 값을 가져와 Json으로 만들어주는 함수.
    getConfigData(){
        let noconfTable = this.refs.master3
        let tdata = noconfTable.rows
        let sColor = this.state.lastdata
 
        let preAllData = []
        let maxrowcnt = noconfTable.tHead.children[0].childElementCount
        
        // Table Cell 이 Group 으로 묶여 있어 Rowspan 을 재정의 하여 배열로 만들어 주며 이를 Json으로 만들어준다.
        for(let rowcnt=1;rowcnt < tdata.length;rowcnt++){
            let preData = []
            let row = tdata[rowcnt].cells
            let groupcnt = maxrowcnt-row.length
            // Row 단위로 주요 정보를 배열 형태로 만들어 준다.
            let colcol = 0
            for(let colcnt=0;colcnt < maxrowcnt;colcnt++){
                if(groupcnt == 0){
                    preData.push(this.setConfigData(row[colcol]))
                    colcol += 1
                }else{
                    preData.push(preAllData[rowcnt-2][colcnt]) //Tile 때문에 -2를 해준다.
                    groupcnt -= 1
                }
            }
            
            preAllData.push(preData)

        }

        let preAllDataJ = this.makeJson(preAllData)

        return preAllDataJ
    }

    makeJson(preAllData){
        //만들어진 Data를 그대로 Json으로 만들어준다.
        let params = {}
        let arrkey = null

        for(let arowcnt in preAllData){
            let param = params
            let arow = preAllData[arowcnt]
            let arrcnt = 0
            for(let acolcnt = 0 ; acolcnt < arow.length -1; acolcnt++){
                let acol = arow[acolcnt]
                let vcol = arow[acolcnt+1]

                let data = acol[0]
                let last = acol[4] 
                let vdata = vcol[0]
                let vtype = vcol[3]
                let vlast = vcol[4]
                // Json Key값이 숫자인 경우는 배열로 인식을 해준다.

                if(vlast == "last"){// 마지막 값인경
                    let dataType = Object.prototype.toString.call(data)
                    if(vdata*1 >= 0){
                        vdata *= 1
                    }
                    if(dataType == "[object Array]"){
                        param.push(vdata)
                    }else{
                        if(vdata == this.state.arrayData){
                            param[data] = []
                        }else if(vdata == this.state.jsonData){
                            param[data] = {}
                        }else if(vdata == "null"){
                            param[data] = null
                        }else{
                            param[data] = vdata
                        }
                        

                        //Auto Ml로 돌릴경우 Type과 optino을 넣어주어야 한다. Extention
                        if(this.props.tabIndexAS == 1){
                            let param1 = params
                            for(let toa=0 ;toa <= acolcnt ; toa++){
                                
                                let row1 = arow[toa]
                                let row2 = arow[toa+2]
                                param1 = param1[row1[0]]
                                
                                //만약 마지막 값이 아니면서 숫자일경우는 배열로서 auto, option등을 넣어준다. 배열
                                if(row2[4] != "last" && row2[0] != "" && row2[0]*1 >= 0){
                                    if(param1["option"] == undefined ){
                                        param1["option"] = null
                                    }
                                    if(param1["auto"] == undefined){
                                        param1["auto"] = false 
                                    }
                                    if(param1["type"] == undefined){
                                        param1["type"] = vtype
                                    }
                                    break
                                }else if(row2[4] == "last"){
                                    if(param1["option"] == undefined ){
                                        param1["option"] = null
                                    }
                                    if(param1["auto"] == undefined){
                                        param1["auto"] = false
                                    }
                                    if(param1["type"] == undefined){
                                        param1["type"] = vtype
                                    }
                                    break
                                }
                            }
                        }
                    }
                    
                    break
                }else if(isNaN(data) == true && isNaN(vdata) == false){//최초 Json에 배열 선언시 들어온다.
                    if(param[data] == undefined){
                        param[data] = []
                        
                    }
                    param = param[data]
                }else if(isNaN(data) == false && isNaN(vdata) == false){//이중 배열 이상일때 들어온다. 
                    if(param[data] == undefined){
                        param[data] = []
                    }

                    param = param[data]
                }else{//배열이 아닌 일반 계층 값을 넣을때 사용한다.

                    if(param[data] == undefined || param[data] == false || param[data] == null){
                        param[data] = {}
                    }
                    param = param[data]
                }

            }
            
            
        }
        return params
    }

    handleChangeConf(value){
        // this.state.config[this.props.nodeType] = this.getConfigData()
        // console.log(this.state.config)
    }

    render() {
        let k = 1
        /////////////////////////////////////////////////////////////////////////////////////////
        // Network Config List
        /////////////////////////////////////////////////////////////////////////////////////////
        const jsonData = this.state.jsonData
        const arrayData = this.state.arrayData
        // 테이블 구릅핑에 필요한 수를 넣어준다.
        function setRspanCount(data, colcnt){
            let prev = []
            let redata = data
            for(let i in data){
                let sameflag = "Y"
                for(let j in data[i]){
                    let coldata = data[i][j] // 현재 값의 데이터를 넣어준다.
                    let prevdata = prev[j] // 이전 Row의 Data 값을 넣어준다.
                     if(coldata != null){ // Table Data 가 존재 할 경우
                        coldata.rspancnt += 1
                        prev[j] = coldata
                        
                        if(prevdata != null && prevdata.key == coldata.key && sameflag == "Y"){// 이전 데이터가 있으며 동일할 경우
                            
                        }else{// 앞에서 동일하지 않으면 해당 Row는 더이상 컬럼이 동일하지 않다고 판단해야 한다.
                            sameflag == "N"
                        }
                    }else{//Table Data가 존재 하지 않을 경우 이전 Row값에 Null을 넣어준다. 
                        prev[j] = null
                    }
                }
            }

            return redata
        }

        //테이블에 출력시 정렬을 위해 사용한다.
        function jsonKeySort(data){
            let keys = null
            let suflag = true
            if(data != null && typeof(data) != "string"){
                keys = Object.keys(data)
                for(let i in keys){
                    if(isNaN(keys[i]) == false){
                        keys[i] = keys[i]*1
                    }else{
                        suflag = false
                    }
                }
                if(suflag){
                    keys.sort(function(a,b){return a-b;})
                }else{
                    keys.sort()
                }
            }
            
            return keys
        }

        // Json 을 기준으로 빈 노드를 계층구조로 만들어 준다.
        function setNode(ppNode){
            let recnt = 0
            let pNode = null
            let data = ppNode.data
            ppNode.flag = "Y"
            
            if(ppNode.child == null){
                let keyArray1 = jsonKeySort(data)//data를 기준으로 자식을 찾아 소팅해준다.

                let dataType = Object.prototype.toString.call(data)
                if(dataType == "[object Object]" && keyArray1.length == 0 ){ // && ppNode.key == "option"
                    ppNode.data = jsonData
                }else if(dataType == "[object Array]" && keyArray1.length == 0 ){ // && ppNode.key == "option"
                    ppNode.data = arrayData
                }
                for(let key1 in keyArray1){
                    const node ={
                        key : keyArray1[key1],
                        rspancnt:0,
                        next : null,
                        child : null,
                        parents:ppNode,
                        data : data[keyArray1[key1]],
                        prev : null,
                        flag : "N", // Node생성시 사
                        dataflag : "N", // Node Data 입력시 사용 
                        type:""
                    }
                    
                    if(key1 == 0){
                        pNode = node
                        ppNode.child = pNode    
                    }else{
                        node.prev = pNode
                        pNode.next = node
                        pNode = node
                    } 
                }
                
                if(keyArray1 != null){
                    recnt = keyArray1.length
                }
            } 
            
            return recnt
        }

        
        // 노드를 만들어 data 를 넣어 주는 기능을 한다.
        function makeNode(data){
            const rNode ={
                key :"root",
                rspancnt:0,
                next : null,
                child : null,
                parents:null,
                data : null,
                prev : null,
                flag : "N",
                dataflag : "Y",
                type:"",
                colcnt :0
            }
            
            // // Key Make Array
            let checkcnt = 0

            for (let i in data) {// 최초 Root를 만들어준다.
                rNode.data = data[i]
                checkcnt = setNode(rNode)
            }
            
            let node = rNode
            let outcnt = 0
            while(true){
                if(node.child != null && node.child.flag == "N"){ // 자식이 있고 자식이 Load 한 적이 없다면 자식으로 내려간다.
                    node = node.child
                }else if(node.next != null){  
                    node = node.next  
                }else if(node.child == null && node.next == null && node.parents != null){
                    node = node.parents
                }else if(node.child != null && node.child.flag == "Y" && node.parents != null){
                    node = node.parents
                }

                let selflag = "N"
                let tmpnode = node
                while(true){// type이 sel 인 경우는 배열로 표기 되야 해서 Child를 만들면 안된다.
                    if(tmpnode.next != null){
                        tmpnode = tmpnode.next
                    }else{
                        break
                    }

                    if(node.key == "option" && tmpnode.key == "type" && tmpnode.data == "sel"){
                        selflag = "Y"
                    }
                }


                if(selflag == "N"){
                    checkcnt = setNode(node)
                }
                
                if(node.parents == null){
                    break
                }
                
                outcnt += 1
                if(outcnt>3000){
                    break
                }
            }
            return rNode
        }

        // 최종 데이터를 표현하는 Type은 표시하지 않는다. 또한 해당 값은 Option의 Type에 넣어 Numver, String을 판단한다.
        // Auto 값이 false인 경우 표현 하지 않는다. 
        function makeTableData(node, tabIndexAS){
            // Data Make Array
            let outcnt = 0
            let k = 1
            let nnInfoNewListDetail = []
            while(true){
                if(node.child != null && node.child.dataflag == "N"){
                    node.dataflag = "Y"
                    node = node.child  
                }else if(node.child == null && node.dataflag == "N") {
                    let data = []
                    let tmpnode = node
                    while(true){
                        //Option Type을 넣어줘야 한다.
                        let ttmpnode = tmpnode
                        while(true){
                            if(ttmpnode.next == null){
                                break
                            }
                            ttmpnode = ttmpnode.next
                            if(ttmpnode.key == "type"){
                                tmpnode.type = ttmpnode.data
                            }
                        }
                        // 배열인 경우 상위 부모의 type을 찾아야 한다.
                        if(tmpnode.type == ""){
                            while(true){
                                if(ttmpnode.next == null && ttmpnode.parents == null){
                                    break
                                }else if(ttmpnode.next == null ){
                                    ttmpnode = ttmpnode.parents
                                }else{
                                    ttmpnode = ttmpnode.next
                                }
                                
                                if(ttmpnode.key == "type"){
                                    tmpnode.type = ttmpnode.data
                                    break
                                }
                            }
                        }

                        //Data를 넣어준다.
                        data.push(tmpnode)
                        tmpnode = tmpnode.parents
                        if(tmpnode.parents == null){
                            break
                        }
                    }

                    // 마지막 값부터 저장되어 있는 것을 처음 것부터 쌓이게 변겨해 준다.
                    let redata = []
                    for(let i=data.length-1;i >= 0;i--){
                        redata.push(data[i])
                    }

                    let vflag = "Y"
                    let keydata = redata[redata.length-1]
                    let datatype = Object.prototype.toString.call(keydata.data)

                    if(keydata.key == "type" && tabIndexAS == 1){ // 마지막에 위치한 Type은 화면에 표시 하지 않는다. Auto인 경우만 적용 
                        vflag = "N"
                    }else if(keydata.key == "auto" && keydata.data == false){// 마지막에 위치한 auto false는 표기하지 않음.
                        vflag = "N"
                    }else if(keydata.key == "option" && keydata.data == null){//option이 Null이면 표기하지 않음.
                        vflag = "N"
                        //auto, option이 모두 없는 경우는 option을 표기해 주어야 한다.
                        let tmpnode = node
                        while(true){
                            if(tmpnode.prev != null){
                                tmpnode = tmpnode.prev
                            }else{
                                break
                            }
                            if(tmpnode.key == "auto" && tmpnode.data == false){
                                vflag = "Y"
                            }
                        }
                    }else if(datatype == "[object Object]" && keydata.type == "sel"){// array는 list로 그림.
                        vflag = "N"
                    }

                    if(vflag == "Y"){
                        nnInfoNewListDetail[k++] = redata
                        if(rNode.colcnt < redata.length){//타이틀 수를 판단해줌. 
                            rNode.colcnt = redata.length
                        }
                    }
                    
                    node.dataflag = "Y"
                }else{
                    if(node.next != null){
                        node = node.next
                    }else{
                        node = node.parents
                    }
                }

                if(node == null || node.parents == null){
                    break
                }

                outcnt += 1
                if(outcnt>3000){
                    break
                }
            }
            rNode.colcnt = rNode.colcnt + 1
            return nnInfoNewListDetail
        }

        // Network List Detail Node를 만들고 Data를 넣어준다.
        let rNode = makeNode(this.props.NN_TableDataDetail)
        // Table에 넣어주는 구조로 Data를 만들어준다.
        let nnInfoNewListDetail = makeTableData(rNode, this.props.tabIndexAS)
        // Table을 만들기 위해 span을 계산해 넣어준다.
        nnInfoNewListDetail = setRspanCount(nnInfoNewListDetail, rNode.colcnt)

        // console.log(rNode)
        // console.log(nnInfoNewListDetail)

        /////////////////////////////////////////////////////////////////////////////////////////
        // NetConf Table Header Make
        /////////////////////////////////////////////////////////////////////////////////////////
        let tableHeader = []; //make header
        let colDatas = ["Depth1"]
        if(rNode.colcnt > 0){
            colDatas = []
            for(let i=0;i < rNode.colcnt ; i++){
                colDatas.push("Depth"+(i+1))
            }
        }
        let headerData = []
        for (let i=0;i < colDatas.length;i++){
            headerData.push(<th key={k++} style={{"textAlign":"center"}} >{colDatas[i]}</th>)
        }
        
        tableHeader.push(<tr key={k++} >{headerData}</tr>)

        /////////////////////////////////////////////////////////////////////////////////////////
        // NetConf Table Data Make
        /////////////////////////////////////////////////////////////////////////////////////////
        let tableData = []; // make tabledata
        for(let rows in nnInfoNewListDetail){
            let colData = [];

            let rspantext = []

            let row = nnInfoNewListDetail[rows]
            let option = []

            for(let cols in row){
                if(cols == row.length-1){ 
                    colData.push(<td key={k++} rowSpan= {1}> {row[cols].key} </td>)    
                    let rowData = row[cols].data
                    if(Object.prototype.toString.call(rowData) == "[object Array]" && row[cols].type == "sel"){
                        let defaultVal = ""
                        if(row[cols].data.length > 0){
                            defaultVal = rowData[0]
                        }

                        for(let op in rowData){
                            option.push(<option key={k++} value={rowData[op]}>{rowData[op]}</option>)
                        }   

                        colData.push(<td key={k++}>
                                        <div>
                                        <select ref={"sel"+k} 
                                               id={k} 
                                               alt ={this.state.lastdata}
                                               onChange = {this.handleChangeConf.bind(this)}
                                                defaultValue={defaultVal[0]}
                                               style={{"color":this.state.color, "width":"100%", "fontWeight":"bold"}}
                                               rowSpan={1}>
                                           {option}
                                        </select>
                                        </div>
                                    </td>)
                    }else{
                        let datatype = row[cols].type

                        if(datatype == "int"){
                            datatype = "number"
                        }else{
                            datatype = "string"
                        }
                        

                        if(rowData == arrayData){
                            colData.push(<td key={k++} type={datatype} alt ={this.state.lastdata} 
                                style={{"color":this.state.color}} > {rowData} </td>)
                        }else if(rowData == jsonData){
                            colData.push(<td key={k++} type={datatype} alt ={this.state.lastdata} 
                                style={{"color":this.state.color}} > {rowData} </td>)
                        }else if(rowData == null){
                            rowData = "null"
                            colData.push(<td key={k++} type={datatype} alt ={this.state.lastdata} 
                                style={{"color":this.state.color}} > {rowData} </td>)
                        }else{
                            if(this.props.editable == "Y"){
                                colData.push(<td key={k++} alt ={this.state.lastdata} style={{"color":this.state.color}} > 
                                    < input type = {datatype} 
                                            style={{"color":this.state.color
                                                    ,"textAlign":"center"
                                                    , "width":"100%"
                                                    , "fontWeight":"bold"}} 
                                            onChange = {this.handleChangeConf.bind(this)}
                                            defaultValue = {rowData} />  </td>)
                            }else{
                                colData.push(<td key={k++} alt ={this.state.lastdata} type={datatype} 
                                                           style={{"color":this.state.color, "fontWeight":"bold"}} > {rowData} </td>)
                            }
                        }
                        
                    }
                }else{
                    if(row[cols].rspancnt > 0){
                        colData.push(<td key={k++} 
                                        rowSpan= {row[cols].rspancnt}> {row[cols].key} </td>) 
                        row[cols].rspancnt = 0
                    }   
                }
            }

            //add column
            for(let i=0;i<colDatas.length - row.length-1;i++){
                colData.push(<td key={k++} ></td>) 
            }

            tableData.push(<tr key={k++}>{colData}</tr>)
        }
        

        let nnInfoNewListDetailTable = []
        nnInfoNewListDetailTable.push(<thead ref='thead' key={k++} className="center">{tableHeader}</thead>)
        nnInfoNewListDetailTable.push(<tbody ref='tbody' key={k++} className="center" >{tableData}</tbody>)

        return (
            <div>
                <table className="table detail" ref= 'master3' >
                    {nnInfoNewListDetailTable}
                </table>
            </div>
        )
    }
}

JsonConfComponent.defaultProps = {
    reportRepository: new ReportRepository(new Api())
};
