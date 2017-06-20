import React from 'react';
import NN_InfoListTableRowComponent from './NN_InfoListTableRowComponent';

export default class NN_InfoListTableComponent extends React.Component {
    constructor(props) {
        super(props)
    }

    render() {
        let i=0;//React needs key for make table
        //check null for initialize dom
        if (!this.props.NN_TableData) {return null;}
        let tableDataDatas = this.props.NN_TableData.map(function(tableData) {
            return (<NN_InfoListTableRowComponent key={i++} NN_TableData={tableData}/>);
        });

        return (
            <div>
                <table className="table">
                    <thead>
                    <tr>
                        <th>category</th>
                        <th>subcate</th>
                        <th>desc</th>
                        <th>name</th>
                        <th>created</th>
                    </tr>
                    </thead>
                    <tbody>
                    {tableDataDatas}
                    </tbody>
                </table>
            </div>
        )
    }
}