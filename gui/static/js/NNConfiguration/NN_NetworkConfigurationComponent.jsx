import React from 'react';
import DiagramSectionComponent from './netconf/DiagramSectionComponent';

export default class NN_NetworkConfigurationComponent extends React.Component {
    constructor(props) {
        super(props);
    }

    render() {
        return (
                <DiagramSectionComponent getHeaderEvent={this.props.getHeaderEvent}/>
        )
    }
}