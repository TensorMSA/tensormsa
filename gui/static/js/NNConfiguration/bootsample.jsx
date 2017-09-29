import React from 'react';
import PersonalDataTableComponent from './../tables/PersonalDataTableComponent'
import ReportRepository from './../repositories/ReportRepository'
import Api from './../utils/Api'
import NN_InfoListTableComponent from './../tables/NN_InfoListTableComponent'
import StepArrowComponent from './../NNLayout/common/StepArrowComponent'
import { BootstrapTable, TableHeaderColumn } from 'react-bootstrap-table';
import NN_BasicInfoComponent from './NN_BasicInfoComponent';
import Modal from 'react-modal';



function signalFormatter(cell, row) {
    let color;
    //console.log("row : " + row);
    //console.log("cell : " + cell);
    if (cell == 'Y') {
        color = "signal-lamp-green";
    } else {
        color = "signal-lamp-red";
    }

    //return '<i className=' + color + '></i> ' + cell;
    return `<i class='` + color + `'></i>`;
}

function precisionFormatter(cell, row) {
    //console.log(cell);
  return (Math.round(Number(cell).toPrecision(2) * 100,1) ) + '%';
}

export default class NN_InfoListComponent extends React.Component {
    constructor(props, context) {
        super(props);
        this.closeModal = this.closeModal.bind(this);
        this.deleteCommonNNInfo = this.deleteCommonNNInfo.bind(this);
        this.state = {
            tableData: null,
            NN_TableData: null,
            selModalView: null,
            NN_ID : null,
            stepBack : 1,
            stepForward : 2
        };
    }

    componentDidMount(){
        //alert(this.context.NN_ID)
        this.getCommonNNInfo();
        
    }

    getCommonNNInfo(params) {
        this.props.reportRepository.getCommonNNInfo(params).then((tableData) => {
            this.setState({ NN_TableData: tableData })
        });
    }

    deleteCommonNNInfo(params) {
        this.props.reportRepository.deleteCommonNNInfo(params).then((tableData) => {
            this.getCommonNNInfo();
        });
    }

    NNButtonText(i) {
        switch (i) {
            case 0:
                return "Search";
            case 1:
                return "Add New";
            case 2:
                return "Delete";
            case 3:
                return "Modify";
            case 4:
                return "Detail";
            default:
                return "";
        }
    }

    openModal(type) {
        console.log(type)
        if (type == 'add New') {
            this.setState({ selModalView: <NN_BasicInfoComponent /> })
        }
        this.setState({ open: true })
    }

    // close modal 
    closeModal() {
        this.setState({ open: false });
        this.getCommonNNInfo();
    }
    
    render() {

        function onAfterDeleteRow(rowKeys) {
            console.log(typeof deleteCommonNNInfo);
            //alert('The rowkey you drop: ' + rowKeys);
            this.deleteCommonNNInfo(rowKeys);
        }

        function onSelectRow(row) {
            //alert(`You click row id: ${row.key}`);
            //console.log(this.thisClass.props)
            console.log("row정보 : " + row.type)
            console.log("row정보 : " + row.datavaild)
            console.log("row정보 : " + row.config)
            console.log("row정보 : " + row.confvaild)
            console.log("row정보 : " + row.train)
            console.log("row정보 : " + row.imagepre)
            this.thisClass.props.setActiveItem(row.key,
                                               row.type,
                                               row.datavaild,
                                               row.config,
                                               row.confvaild,
                                               row.train,
                                               row.preprocess,
                                               row.name);
        }

        const selectRowProp = {
            mode: 'radio',
            clickToSelect: true,
            onSelect: onSelectRow,
            thisClass : this
        }

        const options = {
            paginationShowsTotal: true,
            afterDeleteRow: onAfterDeleteRow,  // A hook for after droping rows.
            deleteCommonNNInfo: this.deleteCommonNNInfo
        }

        let result = [];

        if (this.state.NN_TableData != null) {
            for (var i in this.state.NN_TableData) {
                //console.log(this.state.NN_TableData[i].pk);
                this.state.NN_TableData[i].fields['key'] = this.state.NN_TableData[i].pk;
                result[i] = this.state.NN_TableData[i].fields;
            }
            console.log(result);
        }

        return (
            <section>
                <h1 className="hidden">tensor MSA main table</h1>
                <div className="searchArea">
                    <StepArrowComponent getHeaderEvent={this.props.getHeaderEvent} stepBack={this.state.stepBack} stepForward={this.state.stepForward}/>
                </div>
                <div className="container paddingT10">
                    <div className="tblBtnArea">
                        <button type="button" className="search" >
                             {this.NNButtonText(0)}
                        </button>
                        <button onClick={this.openModal.bind(this, "add New")}>
                             {this.NNButtonText(1)}
                        </button>
                        <button type="button" className="delete" >
                            {this.NNButtonText(2)}
                        </button>
                        <button type="button" className="modify" >
                            {this.NNButtonText(3)}
                        </button>
                        <button type="button" className="detail" >
                            {this.NNButtonText(4)}
                        </button>
                    </div>
                    <div className="net-info">
                        <BootstrapTable data={result} options={ options } 
                            striped={true}
                            hover={true}
                            condensed={true}
                            pagination={true}
                            selectRow={selectRowProp}
                            deleteRow={false}
                            search={false}>
                            <TableHeaderColumn isKey={true} dataField="key" width="120">ID</TableHeaderColumn>
                            <TableHeaderColumn dataField="category" width="70">Category</TableHeaderColumn>
                            <TableHeaderColumn dataField="type" width="70">Type</TableHeaderColumn>
                            <TableHeaderColumn dataField="name" width="120">Title</TableHeaderColumn>
                            <TableHeaderColumn dataField="desc" width="150">Description</TableHeaderColumn>
                            <TableHeaderColumn dataField="datavaild" width="80" editable={false} dataFormat={signalFormatter} dataAlign="center">DataVaild</TableHeaderColumn>
                            <TableHeaderColumn dataField="config" width="80" editable={false} dataFormat={signalFormatter} dataAlign="center">Config</TableHeaderColumn>
                            <TableHeaderColumn dataField="confvaild" width="80" editable={false} dataFormat={signalFormatter} dataAlign="center">Consistency</TableHeaderColumn>
                            <TableHeaderColumn dataField="train" width="80" editable={false} dataFormat={signalFormatter} dataAlign="center">Train</TableHeaderColumn>
                            <TableHeaderColumn dataField="acc" width="80" editable={false} dataFormat={precisionFormatter}>Accuracy</TableHeaderColumn>
                            <TableHeaderColumn dataField="imagepre" hidden>Imagepre</TableHeaderColumn>
                        </BootstrapTable>
                    </div>
                    <div>
                        <Modal className="modal" overlayClassName="modal" isOpen={this.state.open}
                            onRequestClose={this.closeModal}>
                            <div className="modal-dialog modal-lg">{this.state.selModalView}
                                <span className="modal-footer">
                                    <button onClick={this.closeModal}>Close</button>
                                </span>
                            </div>
                        </Modal>
                    </div>
                </div>
            </section>
        );
    }
}

NN_InfoListComponent.defaultProps = {
    reportRepository: new ReportRepository(new Api())
};

NN_InfoListComponent.contextTypes = {
    NN_ID: React.PropTypes.string
};