import React from 'react'

export default class PersonalDataTableRowComponent extends React.Component {
    constructor(props) {
        super(props)
    }

    render() {
        return (
            <tr>
                <td>{this.props.tableData.name}</td>
                <td>{this.props.tableData.univ}</td>
                <td>{this.props.tableData.org}</td>
                <td>{this.props.tableData.eng}</td>
            </tr>
        )
    }
}