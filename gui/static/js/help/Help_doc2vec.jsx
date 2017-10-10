import React from 'react'
import ReportRepository from './../repositories/ReportRepository'
import Api from './../utils/Api'
import EnvConstants from './../constants/EnvConstants';

export default class Help_doc2vec extends React.Component {
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

        return (  

            <div>
                <h1> Doc2Vec </h1>
                
                <div className="container tabBody">
        
                </div>
            </div>
        )
    }
}


