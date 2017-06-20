import React from 'react'

export default class NN_ModalComponent extends React.Component {
    render() {
        return (   
            <div className="modal" id="modal-one" aria-hidden="true">
                <div className="modal-dialog">
                    <div className="modal-header">
                    <h2>Modal Head</h2>
                    <a href="#close" className="btn-close" aria-hidden="true">×</a>
                    </div>
                    <div className="modal-body">
                    <p>Body Area</p>
                    </div>
                    <div className="modal-footer">
                    <a href="#close" className="btn">Close</a>
                    </div>
                </div>
            </div>
        )
    }
}