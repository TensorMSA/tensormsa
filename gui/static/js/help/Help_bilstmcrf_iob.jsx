import React from 'react'
import ReportRepository from './../repositories/ReportRepository'
import Api from './../utils/Api'


export default class Help_bilstmcrf_iob extends React.Component {
    constructor(props, context) {
        super(props);
        this.state = {
        	NN_TableData: null
        };

    }
    /////////////////////////////////////////////////////////////////////////////////////////
    // Search Function
    /////////////////////////////////////////////////////////////////////////////////////////
    componentDidMount() {
    }

    render() {
let url1 = "./images/help_bilstm1.png"
        return (  

            <div>
                <h1> Bilstmcrf Iob </h1>
                
                <div className="container tabBody">
        <img src={url1} />
                <br />
                <br />
                <h3>
                
                </h3>
                </div>
            </div>
        )
    }
}


