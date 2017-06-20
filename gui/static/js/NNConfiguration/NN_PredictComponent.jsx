import React from 'react';

const FileUpload = require('react-fileupload');


export default class NN_PredictComponent extends React.Component {
    constructor(props) {
        super(props);
    }


    

    render() {


        /*set properties*/
    const options={
        baseUrl:'http://api/v1/type/imagefile/base/mes/table/testtable2/label/2/data/nn0000090/',
        param:{
            fid:0
        },
        fileFieldName(file) {
          this.name = 'file';
        },
    }
    /*Use FileUpload with options*/
    /*Set two dom with ref*/
    return (
        <FileUpload options={options}>
            <button ref="chooseBtn">12345</button>
            <button ref="uploadBtn">upload</button>
        </FileUpload>
    )           
    }
}

                       