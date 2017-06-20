import React from 'react'

export default class CnnTableSectionComponent extends React.Component {
    constructor(props){
        super(props);

        this.state = {
            datasets : null
        };
    }

    componentWillMount(){
        if(typeof this.props.nnConfigFeatureInfoField.datasets === 'string')
        {
            this.setState({datasets: JSON.parse(this.props.nnConfigFeatureInfoField.datasets)});
        }
        else {
            this.setState({datasets: this.props.nnConfigFeatureInfoField.datasets});
        }
    }

    render() {
        return (
            <div id='netconf-table'>                    
                <div className='l--body'>
                    <dl className="layer-box">
                        <dt><span className="circle-blue">Input Layer</span></dt>
                        <dd>
                            <table id='input_table' className='form-table align-center'>
                                <thead>
                                    <tr>
                                        <th>X size</th>
                                        <th>Y size</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    <tr>
                                        <td>{this.props.nnConfigLabelInfoField.x_size}</td>
                                        <td>{this.props.nnConfigLabelInfoField.y_size}</td>
                                    </tr>
                                </tbody>
                            </table>
                        </dd>
                    </dl>
                    <dl className="layer-box">
                        <dt><span className="circle-blue">Hidden Layer</span></dt>
                        <dd>
                        </dd>
                    </dl>
                    <dl className="layer-box">
                        <dt><span className="circle-blue">Output Layer</span></dt>
                        <dd>
                            <table id='output_table' className='form-table align-center'>
                                <thead>
                                    <tr>
                                        <th>Label</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    {
                                        this.state.datasets.map((dataset) =>
                                            <tr key={dataset}><td>{dataset}</td></tr>
                                        )
                                    }
                                </tbody>
                            </table>
                        </dd>
                    </dl>    
                </div>                
            </div>
        )
    }
}
