import React from 'react'
import ReportRepository from './../../repositories/ReportRepository';
import Api from './../../utils/Api';

export default class ModalViewFormatCreate extends React.Component {
    constructor(props) {
        super(props);
        this.state = {};
    }

    // post format data
    postFormatData(){
        let requestUrl = "base/" + this.props.formatData.databaseName + "/table/" + this.props.formatData.tableName 
        + "/format/" + this.props.formatData.networkId + "/";
        let formatSize = {"x_size" : this.props.formatData.xSize, "y_size" : this.props.formatData.ySize}

        console.log(requestUrl)
        console.log(formatSize)
        this.props.reportRepository.postImageFormatData(requestUrl, formatSize).then((format) => {
            console.log(format)
        });
    }

    render() {
        return (   
            <div>
                <h1>Warning</h1>
                
                <div className="container tabBody">
                    <div id="tab1">
                        <article>
                            This Action will delete all currently 
                            updated images. still want to continue?
                            <button type="button" onClick={() => this.postFormatData()}>Confirm</button>
                        </article>
                    </div>
                </div>
            </div>
        )
    }
} 

ModalViewFormatCreate.defaultProps = {
    reportRepository: new ReportRepository(new Api())
};