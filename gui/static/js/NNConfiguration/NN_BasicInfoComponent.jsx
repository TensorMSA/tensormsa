import React from 'react';
import Api from './../utils/Api'
import ReportRepository from './../repositories/ReportRepository'

export default class NN_BasicInfoComponent extends React.Component {
    constructor(props) {
        super(props);
        this.key_id = null;
        this.state = {
                nn_id     : null,
                category  : null,
                categoryList : null,
                subcate   : null,
                subcateList   : null,
                type      : null,
                name      : null,
                desc      : null               
                };
    }

    componentDidMount(){
        this.getCategoryList();
        console.log(this.state.categoryList)
        
    }
    //set category name on state variable
    setCategory(obj){
        console.log("setCategory : " + obj.target.value)
        this.setState({category: obj.target.value}, function(){this.getSubCategoryList()});
    }

    //set subCategory on state variable
    setSubCategory(obj){
        console.log("setSubCategory : " + obj.target.value)
        this.setState({subcate: obj.target.value});
    }

    //set netWorkType on state variable
    setNetWorkType(obj){
        console.log("setNetWorkType : " + obj.target.value)
        this.setState({type: obj.target.value});
    }

    //set netWorkType on state variable
    setTitle(obj){
        this.setState({name: obj.target.value});        
    }

    //set netWorkType on state variable
    setDescription(obj){
        this.setState({desc: obj.target.value});
    }

    make_nn_id(){
        this.key_id = this.state.category + '_' + this.state.subcate + '_' + this.state.type + '_' + Math.floor((Math.random() * 100000) + 1);
    }
    // add user request new table
    postCommonNNInfo(){
        this.make_nn_id();
        console.log("키는 : " + this.key_id);

        this.props.reportRepository.postCommonNNInfo(null, this.key_id, this.state).then((answer) => {
            //console.log(answer.status);
            if(answer.status == "200") {
                msg.show("New neural network registered!");
            }
        });
    }

    getCategoryList(){
        let defaultUrl = "category";
        this.props.reportRepository.getCategoryList(defaultUrl).then((category_list) => {
        let option = [];
        let i=0;
        for (let categoryValue of category_list['result']){
            option.push(<option key={i++} value={categoryValue}>{categoryValue}</option>)
        }
        this.setState({categoryList : option})
        });
    }
    
    getSubCategoryList(){
        this.props.reportRepository.getSubCategoryList(this.state.category).then((subCate_list) => {
        let option = [];
        let i=0;
        for (let subCateValue of subCate_list['result']){
            option.push(<option key={i++} value={subCateValue}>{subCateValue}</option>)
        }
        this.setState({subcateList : option})
        });
    }

    render() {
        return (
                <section>
                    <h1 className="hidden">tensor MSA main table</h1>
                    <ul className="tabHeader">
                        <li className="current"><a href="#">Network Basic Information</a></li>
                        <div className="btnArea">
                            <button type="button" onClick={this.postCommonNNInfo.bind(this)}>Save</button>
                        </div>
                    </ul>   
                        <div className="container tabBody">
                            <div id="tab1">
                                <article>
                                    <table className="form-table align-left">
                                        <colgroup>
                                        <col width="250" />
                                        <col width="500" />
                                        <col width="250" />
                                        <col width="500" />
                                        </colgroup> 
                                        <tbody>
                                        <tr>
                                            <th>GROUP(Business Category)</th>
                                            <td>
                                                <select onChange={this.setCategory.bind(this)} >
                                                  <option key="default1">Category List</option>
                                                  {this.state.categoryList}  
                                                </select>
                                            </td>
                                            <td>
                                                <select onChange={this.setSubCategory.bind(this)}>
                                                <option key="default1">subCategory List</option>
                                                   {this.state.subcateList}
                                                </select>
                                            </td>
                                            <th>Neural Network Type</th>
                                            <td>
                                                <select onChange={this.setNetWorkType.bind(this)} value={this.state.value}>
                                                <option value="1">Network Type</option>
                                                <option value="cnn">CNN</option>
                                                <option value="wdnn">WDNN</option>
                                                <option value="cifar">CIFAR</option>
                                                </select>
                                            </td>
                                        </tr>
                                        <tr>
                                            <th>Title</th>
                                            <td colSpan="3"><input type="text" className="w100p" onChange={this.setTitle.bind(this)} value={this.state.value}></input></td>
                                        </tr>
                                        <tr>
                                            <td colSpan="4">
                                                <span className="label-blue positionA">Description</span>
                                                <textarea rows="30" className="w100p paddingT30" onChange={this.setDescription.bind(this)} value={this.state.value}></textarea>
                                            </td>
                                        </tr>
                                        </tbody>
                                    </table>
                                </article>
                            </div>
                        </div>
                </section>
        )
    }
}

NN_BasicInfoComponent.defaultProps = {
    reportRepository: new ReportRepository(new Api())
};