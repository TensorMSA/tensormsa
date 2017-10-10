let ip = location.origin //'http://52.78.67.19:8989'

export default {
    
      getApiServerUrl() {
          return  ip;//if docker exist, use container name
     },
     getWebServerUrl() {
         return  ip;
      },
      getImgUrl(){
      	return './../templates/images/';
      }
  };	 