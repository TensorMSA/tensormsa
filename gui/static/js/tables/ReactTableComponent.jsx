import React from 'react'
import SpinnerComponent from './../NNLayout/common/SpinnerComponent'
import ReactTable from 'react-table'
import 'react-table/react-table.css'

export default class ReactTableComponent extends React.Component {
    constructor(props) {
        super(props)
    }

    render() {
    	if( this.props.TableData != null){
    		console.log("Table Search>>>>>>>>>>>>>>>>>>>>>")
	        return (
	            <div className="tblTableArea">
					<table className="form-table align-left">
						<ReactTable data={this.props.TableData} columns={this.props.TableColumn} 
									getTdProps={(state, rowInfo, column, instance) => {
									    return {
									      onClick: e => {
									        console.log('getTdProps column:', column)
									        console.log('getTdProps row:', rowInfo)
									      }
									    }
									  }}
									getTrProps={(state, rowInfo, column) => {
									    return {
									      // style: {
									      //   background: rowInfo.row.nn_id === 'mro001' ? 'green' : null
									      // }
									      onClick: e => {
									        console.log('getTrProps row:', rowInfo.index%2)
									      }
									    }
									  }}
						/>
					</table>
				</div>
	        )
	    }else{
	    	return (
	            <div className="tblTableArea">
				</div>
	        )
	    }
    }
}



