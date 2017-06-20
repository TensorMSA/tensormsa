import React from 'react';
import PersonalDataTableRowComponent from './PersonalDataTableRowComponent';

export default class PersonalDataTableComponent extends React.Component {
    constructor(props) {
        super(props)
    }

    render() {
        let i=0;//React needs key for make table
        if (!this.props.tableData) {return null;}
        let tableDataDatas = this.props.tableData.map(function(tableData) {
            return (<PersonalDataTableRowComponent key={i++} tableData={tableData}/>);
        });
        return (
            <div>
                <table className="table">
                    <thead>
                    <tr>
                        <th>Name</th>
                        <th>Univ</th>
                        <th>Org</th>
                        <th>eng</th>
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