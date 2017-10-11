let ip = location.origin

export default {
    
      getApiServerUrl() {
          return  ip;//if docker exist, use container name
     },
     getWebServerUrl() {
         return  ip;
      },
      getImgUrl(){
      	return './../templates/images/';
      },
      getSampleFileUrl(){
        return './../templates/js/help/samples/';
      }
  };	 