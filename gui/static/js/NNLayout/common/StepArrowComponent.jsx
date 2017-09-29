import React from 'react'

export default class StepArrowComponent extends React.Component {
    constructor(props) {
        super(props);
    }

    render() {
        return (   
            <div className="btnArea">
                <div className="PNBtn">
                    <button type="button" className="prev" onClick={() => this.props.getHeaderEvent(this.props.stepBack)}>Prev</button>
                    <button type="button" className="next" onClick={() => this.props.getHeaderEvent(this.props.stepForward)}>Next</button>
                </div>
            </div>
        )
    }
}