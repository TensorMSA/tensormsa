import React from 'react'
import ReportRepository from './../repositories/ReportRepository'
import Api from './../utils/Api'
import EnvConstants from './../constants/EnvConstants';

export default class Help_bilstmcrf_iob extends React.Component {
    constructor(props, context) {
        super(props);
        this.state = {
        	NN_TableData: null,
            url1:EnvConstants.getImgUrl()+"help_bilstm1.png"
        };

    }
    /////////////////////////////////////////////////////////////////////////////////////////
    // Search Function
    /////////////////////////////////////////////////////////////////////////////////////////
    componentDidMount() {
    }

    render() {
        return (  

            <div>
                <h1> Bilstmcrf Iob </h1>
                
                <div className="container tabBody">
        <img src={this.state.url1} />
                <br />
                <br />
                <h3>
                
                </h3>
                </div>
            </div>
        )
    }
}


