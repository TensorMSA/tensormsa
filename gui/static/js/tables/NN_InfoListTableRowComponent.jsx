import React from 'react'

export default class NN_InfoListTableRowComponent extends React.Component {
    constructor(props) {
        super(props)
    }

    render() {
        return (
            <tr>
                <td>{this.props.NN_TableData.fields.category}</td>
                <td>{this.props.NN_TableData.fields.subcate}</td>
                <td>{this.props.NN_TableData.fields.desc}</td>
                <td>{this.props.NN_TableData.fields.name}</td>
                <td>{this.props.NN_TableData.fields.created}</td>
            </tr>
        )
    }
}