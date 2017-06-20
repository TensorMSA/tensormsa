import React from 'react'
import MetaStoreConfigurationComponent from './DataConfiguration/MetaStoreConfigurationComponent'
import ImagesConfigurationComponent from './DataConfiguration/ImagesConfigurationComponent'
import StepArrowComponent from './../NNLayout/common/StepArrowComponent'

export default class NN_DataConfigurationComponent extends React.Component {
    constructor(props) {
        super(props);
        this.selected = 'meta';
        this.state = {
                DataConfigurationComponent : null,
                tabMeta : null,
                tabImage : null,
                tabText : null,
                stepBack : 2,
                stepForward : 4
            };
    }

    componentDidMount(){
        this.setTabContent();
    }

    setFilter(filter){
        this.selected  = filter
        if (filter == 'meta') {
            return this.getTableData();
        }
        else{
            return this.getImageData();
        }
    }

    getTableData(){
        this.setTabContent()
        this.setState({DataConfigurationComponent  : <MetaStoreConfigurationComponent/>});
    }

    getImageData(){
        this.setTabContent()
        this.setState({DataConfigurationComponent  : <ImagesConfigurationComponent/>});
    }

    isActive(value){
        return ((value===this.selected) ? 'current':'');
    }

    setTabContent(){
        if(!this.context.NN_DATATYPE){
            this.setState({tabMeta : <li className={this.isActive('meta')} onClick={this.setFilter.bind(this, 'meta')}><a href="#">Meta Store</a></li>})
            this.setState({tabImage : <li className={this.isActive('images')} onClick={this.setFilter.bind(this, 'images')}><a href="#">Images</a></li>})
            this.setState({tabText : <li className={this.isActive('texts')} onClick={this.setFilter.bind(this, 'texts')}><a href="#">Raw Texts</a></li>})
            this.setState({DataConfigurationComponent  : <MetaStoreConfigurationComponent/>});
        }else if(this.context.NN_DATATYPE == '1'){
            this.setState({tabMeta : <li className={this.isActive('meta')} onClick={this.setFilter.bind(this, 'meta')}><a href="#">Meta Store</a></li>})
            this.setState({DataConfigurationComponent  : <MetaStoreConfigurationComponent/>});
        }else if(this.context.NN_DATATYPE == '2'){
            this.setState({tabImage : <li className={this.isActive('images')} onClick={this.setFilter.bind(this, 'images')}><a href="#">Images</a></li>})
            this.setState({DataConfigurationComponent  : <ImagesConfigurationComponent/>});
        }else if(this.context.NN_DATATYPE == '3'){
            this.setState({tabText : <li className={this.isActive('texts')} onClick={this.setFilter.bind(this, 'texts')}><a href="#">Raw Texts</a></li>})
        }else{
            this.setState({tabMeta : <li className={this.isActive('meta')} onClick={this.setFilter.bind(this, 'meta')}><a href="#">Meta Store</a></li>})
            this.setState({DataConfigurationComponent  : <MetaStoreConfigurationComponent/>});
        }        
    }


    render() {
        return (
            <section>
                <h1 className="hidden">tensor MSA main table</h1>
                    <ul className="tabHeader">
                        {this.state.tabMeta}
                        {this.state.tabImage}
                        {this.state.tabText}
                        <StepArrowComponent getHeaderEvent={this.props.getHeaderEvent} stepBack={this.state.stepBack} stepForward={this.state.stepForward}/>
                    </ul>
				    {this.state.DataConfigurationComponent}
            </section>
        )
    }
}


NN_DataConfigurationComponent.contextTypes = {
    NN_ID        : React.PropTypes.string,
    NN_TYPE      : React.PropTypes.string,
    NN_DATAVALID : React.PropTypes.string,
    NN_CONFIG    : React.PropTypes.string,
    NN_CONFVALID : React.PropTypes.string,
    NN_TRAIN     : React.PropTypes.string,
    NN_DATATYPE  : React.PropTypes.string
};