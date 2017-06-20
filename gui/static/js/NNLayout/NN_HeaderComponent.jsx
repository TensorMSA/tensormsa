import React from 'react'
import StepArrowComponent from './common/StepArrowComponent'
import AlertContainer from 'react-alert';

export default class NN_HeaderComponent extends React.Component {
    constructor(props) {
        super(props);
        this.checkPrerequirement = null;
        this.state = {
                selected:null,
                };
		this.alertOptions = {
			offset: 14,
			position: 'top right',
			theme: 'dark',
			time: 5000,
			transition: 'scale'
		};
    }

    setFilter(filter){
		console.log("[Header]" + filter + "," + JSON.stringify(this.context))
        this.setState({selected  : filter})
        switch (filter) {
            case 1:
            	return this.props.getHeaderEvent(1); //call Net Info
            case 2:
            	if(this.context.NN_ID && this.context.NN_TYPE != 'cifar'){
            		return this.props.getHeaderEvent(2);
            	}
				break;
            case 3:
            	if(this.context.NN_ID && this.context.NN_TYPE != 'cifar'){
            		return this.props.getHeaderEvent(3);
            	}
				break;
            case 4:
            	if(this.context.NN_DATAVALID && this.context.NN_TYPE != 'cifar'){
            		return this.props.getHeaderEvent(4);
            	} else {
					if (!this.context.NN_DATAVALID) {
						msg.show("데이터가 유효하지 않습니다.")
					}
				}
				break;
            case 5:
            	if(this.context.NN_CONFIG && this.context.NN_TYPE != 'cifar'){
	                return this.props.getHeaderEvent(5); 
            	} else {
					if (!this.context.NN_CONFIG) {
						msg.show("설정이 완료되지 않았습니다.")
					}
				}
				break;
            case 6:
            	if(this.context.NN_TRAIN || this.context.NN_TYPE == 'cifar'){
	                return this.props.getHeaderEvent(6); 
	            } else {
					console.log("Can't predict. - " + JSON.stringify(this.context))
					if (!this.context.NN_TRAIN) {
						msg.show("학습이 완료되지 않았습니다.")
					}
				}
	        
        }
    }

    isActive(value){
        //console.log(this.context.NN_TYPE == 'cifar')
    	switch (value) {
            case 1:
        		this.checkPrerequirement = 1;
            	return ((value===this.state.selected) ? 'current':'');
            case 2:
            	if(this.context.NN_ID && this.context.NN_TYPE != 'cifar'){
            		return ((value===this.state.selected) ? 'current':'');
            	}
            case 3:
            	if(this.context.NN_ID && this.context.NN_TYPE != 'cifar'){
            		return ((value===this.state.selected) ? 'current':'');
            	}
            case 4:
            	if(this.context.NN_DATAVALID && this.context.NN_TYPE != 'cifar'){
            		return ((value===this.state.selected) ? 'current':'');
            	}
            case 5:
            	if(this.context.NN_CONFIG && this.context.NN_TYPE != 'cifar'){
	                return ((value===this.state.selected) ? 'current':'');
            	}
            case 6:
            	if(this.context.NN_TYPE == 'cifar' || this.context.NN_TRAIN){
	                return ((value===this.state.selected) ? 'current':'');
	            }
        }   	
    }

    render() {
        return (   
			<header className="mainHeader">
				<div className="mainHeader_area">
					<AlertContainer ref={(a) => global.msg = a} {...this.alertOptions} />
					
						<a href="#" onClick={() => this.props.getHeaderEvent(0)}>
							<h1 className="logo">
							<span className="hidden">HOYA</span>
							<span className="logo-image"></span>
							</h1>
						</a>
				<nav>
					<h1 className="hidden">Navigator</h1>
					<ul>
						<li className={this.isActive(1)}><a href="#" onClick={this.setFilter.bind(this, 1)}>Net Info</a></li>
						<li className={this.isActive(2)}><a href="#" onClick={this.setFilter.bind(this, 2)}>Pre Process</a></li>
						<li className={this.isActive(3)}><a href="#" onClick={this.setFilter.bind(this, 3)}>Data Process</a></li>
						<li className={this.isActive(4)}><a href="#" onClick={this.setFilter.bind(this, 4)}>Net conf</a></li>  
						<li className={this.isActive(5)}><a href="#" onClick={this.setFilter.bind(this, 5)}>Train Statistics</a></li>
						<li className={this.isActive(6)}><a href="#" onClick={this.setFilter.bind(this, 6)}>Predict Test</a></li>
					</ul>
				</nav>
					<dl className="utilMenu">
						<dt>Menu</dt>
						<dd className="utilMenu-user-info"><a href="#"><span className="user-name">Suk Jae-Ho</span></a></dd>
						<dd className="utilMenu-help"><a href="#"><span>Help</span></a></dd>
						<dd className="utilMenu-logout"><a href="#"><span>Logout</span></a></dd>
					</dl>
				</div>
			</header>
        )
    }
}

NN_HeaderComponent.contextTypes = {
	NN_ID        : React.PropTypes.string,
	NN_TYPE      : React.PropTypes.string,
	NN_DATAVALID : React.PropTypes.string,
	NN_CONFIG    : React.PropTypes.string,
	NN_CONFVALID : React.PropTypes.string,
	NN_TRAIN     : React.PropTypes.string,
	NN_DATATYPE  : React.PropTypes.string
};
