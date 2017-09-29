export default {
      getApiServerUrl() {
          return  'http://localhost:8989';//if docker exist, use container name
     },
     getWebServerUrl() {
         return  'http://localhost:8889';
      }
  };	 