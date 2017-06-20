import React from 'react'
import NN_HeaderComponent from './NNLayout/NN_HeaderComponent'
import NN_SectionComponent from './NNLayout/NN_SectionComponent'
import NN_FooterComponent from './NNLayout/NN_FooterComponent'
import NN_InfoListComponent from './NNConfiguration/NN_InfoListComponent'
import NN_BasicInfoComponent from './NNConfiguration/NN_BasicInfoComponent'
import NN_DataConfigurationComponent from './NNConfiguration/NN_DataConfigurationComponent'
import NN_NetworkConfigurationComponent from './NNConfiguration/NN_NetworkConfigurationComponent'
import NN_TrainStaticComponent from './NNConfiguration/NN_TrainStaticComponent'
import NN_PredictResultComponent from './NNConfiguration/NN_PredictResultComponent'
import NN_ModalComponent from './NNLayout/NN_ModalComponent';
import MainSectionComponent from './NNLayout/MainSectionComponent';
import NN_PreProcessingComponent from './NNConfiguration/NN_PreProcessingComponent'
import ReportRepository from './repositories/ReportRepository';
import Api from './utils/Api';

export default class HomeComponent extends React.Component {
    constructor(props) {
        super(props);
            this.state = {  
                        NN_InfoList : <MainSectionComponent />,
                        NN_ID : null,
                        NN_TYPE : null,
                        NN_DATAVALID : null,
                        NN_CONFIG : null,
                        NN_CONFVALID : null,
                        NN_TRAIN : null,
                        NN_DATATYPE : null,
                        NN_TITLE : null,
                        netBaseInfo : null,
                        footerArea : <NN_FooterComponent netBaseInfo='Copyrights ⓒ POSCO ICT. All rights reserved.'/>
                         };
            this.addNewNNInfo = this.addNewNNInfo.bind(this); 
            this.getHeaderEvent = this.getHeaderEvent.bind(this);
            this.setActiveItem = this.setActiveItem.bind(this);
        }

    getChildContext() {
          return {NN_ID        : this.state.NN_ID,
                  NN_TYPE      : this.state.NN_TYPE,
                  NN_DATAVALID : this.state.NN_DATAVALID,
                  NN_CONFIG    : this.state.NN_CONFIG,
                  NN_CONFVALID : this.state.NN_CONFVALID,
                  NN_TRAIN     : this.state.NN_TRAIN,
                  NN_DATATYPE  : this.state.NN_DATATYPE,
                  NN_TITLE : this.state.NN_TITLE};
    }

    setActiveItem(item1, item2, item3, item4, item5, item6, item7, item8) {
        this.setState({NN_ID        : item1,
                       NN_TYPE      : item2,
                       NN_DATAVALID : item3,
                       NN_CONFIG    : item4,
                       NN_CONFVALID : item5,
                       NN_TRAIN     : item6,
                       NN_DATATYPE  : item7,
                       NN_TITLE     : item8
                });
        this.setFootContents(item1, item2, item8);
    }

    setFootContents(item1, item2, item8) {
      let footContens = 'Copyrights ⓒ POSCO ICT. All rights reserved.'
      if(item1){
            footContens = ' 1. Network Id : ' + item1;
            footContens += ' | 2. Title : ' + item8;
            footContens += ' | 3. Net Type : ' + item2;
        }

        this.setState({footerArea:<NN_FooterComponent netBaseInfo={footContens}/> })
    }

    getHeaderEvent(i){

        if(this.state.NN_ID){
            this.props.reportRepository.getNetBaseInfo(this.state.NN_ID).then((nnBaseInfo) => {
              if(nnBaseInfo && nnBaseInfo['result'].length > 0){
                this.setState({NN_TYPE : nnBaseInfo['result'][0]['fields']['type']});
                this.setState({NN_DATAVALID : nnBaseInfo['result'][0]['fields']['datavaild']});
                this.setState({NN_CONFIG : nnBaseInfo['result'][0]['fields']['config']});
                this.setState({NN_CONFVALID : nnBaseInfo['result'][0]['fields']['confvaild']});
                this.setState({NN_TRAIN : nnBaseInfo['result'][0]['fields']['train']});
                this.setState({NN_DATATYPE : nnBaseInfo['result'][0]['fields']['preprocess']});
                this.setState({NN_TITLE : nnBaseInfo['result'][0]['fields']['name']});
            }
              this.getHeaderSwitch(i);
              
            });  
        }else{
            this.getHeaderSwitch(i);
        }
    }

    getHeaderSwitch(i){
        switch (i) {
          case 0:
              return this.getMainInfo(); 
          case 1:
              return this.getNetInfo();
          case 2:
              return this.getPreProcessing(); 
          case 3:
              return this.setDataConfiguration();  
          case 4:
              return this.setNetConfiguration(); 
          case 5:
              return this.getTimeStatistics();
          case 6:
              return this.getPredictResult(); 
          }
    }

    getMainInfo(){
        this.setState({NN_InfoList: <MainSectionComponent getHeaderEvent={this.getHeaderEvent}/>});    
    }

    getNetInfo(){
       this.setState({NN_InfoList: <NN_InfoListComponent setActiveItem={this.setActiveItem} addNewNNInfo={this.addNewNNInfo} getHeaderEvent={this.getHeaderEvent} />});
    }
    
    addNewNNInfo(){
        this.setState({NN_InfoList: <NN_BasicInfoComponent getHeaderEvent={this.getHeaderEvent}/> });    
    }

    getPreProcessing(){
        if(this.state.NN_ID && this.state.NN_TYPE != 'cifar'){
            this.setState({NN_InfoList: <NN_PreProcessingComponent getHeaderEvent={this.getHeaderEvent}/> });  
        } 
    }
    
    setDataConfiguration(){
        if(this.state.NN_ID && this.state.NN_TYPE != 'cifar'){
            this.setState({NN_InfoList: <NN_DataConfigurationComponent getHeaderEvent={this.getHeaderEvent}/> });   
        }
    }

    setNetConfiguration(){
        if(this.state.NN_DATAVALID && this.state.NN_TYPE != 'cifar'){
            this.setState({NN_InfoList: <NN_NetworkConfigurationComponent getHeaderEvent={this.getHeaderEvent}/> });  
        }
    }

    getTimeStatistics(){
        if(this.state.NN_CONFIG && this.state.NN_TYPE != 'cifar'){
            this.setState({NN_InfoList: <NN_TrainStaticComponent getHeaderEvent={this.getHeaderEvent}/> }); 
        }  
    }

    getPredictResult(){
        if(this.state.NN_TRAIN || this.state.NN_TYPE == 'cifar'){
            this.setState({NN_InfoList: <NN_PredictResultComponent getHeaderEvent={this.getHeaderEvent}/> });   
        }
    }

    

    render() {
        return (
            <div>
				<NN_HeaderComponent getHeaderEvent={this.getHeaderEvent} /> 
				<NN_SectionComponent NN_InfoList={this.state.NN_InfoList} getHeaderEvent={this.getHeaderEvent} />
				{this.state.footerArea}                              
			</div>
        )
    }
}

HomeComponent.childContextTypes = {
  NN_ID        : React.PropTypes.string,
  NN_TYPE      : React.PropTypes.string,
  NN_DATAVALID : React.PropTypes.string,
  NN_CONFIG    : React.PropTypes.string,
  NN_CONFVALID : React.PropTypes.string,
  NN_TRAIN     : React.PropTypes.string,
  NN_DATATYPE  : React.PropTypes.string,
  NN_TITLE     : React.PropTypes.string
}

HomeComponent.contextTypes = {
    NN_ID        : React.PropTypes.string,
    NN_TYPE      : React.PropTypes.string,
    NN_DATAVALID : React.PropTypes.string,
    NN_CONFIG    : React.PropTypes.string,
    NN_CONFVALID : React.PropTypes.string,
    NN_TRAIN     : React.PropTypes.string,
    NN_DATATYPE  : React.PropTypes.string,
    NN_TITLE     : React.PropTypes.string
};

HomeComponent.defaultProps = {
    reportRepository: new ReportRepository(new Api())
};