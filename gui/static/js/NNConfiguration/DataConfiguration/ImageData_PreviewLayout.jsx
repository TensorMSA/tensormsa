import React from 'react'
import FileUpload from 'react-fileupload';

export default class ImagePreviewLayout extends React.Component {
	constructor(props) {
        super(props)
        this.fileUploadSettings = {
                    baseUrl : null,
                    param:
                    {
                        fid:0
                    },
                    multiple:true,
                    chooseAndUpload:true,
                    doUpload : this._handleDoUpload.bind(),
                    uploading : this._handleUploading.bind(this),
                    uploadSuccess : this._handleUploadSuccess.bind(this),
                    uploadError : this._handleUploadError.bind(this),
                    uploadFail : this._handleUploadFail.bind(this)
                }
        this.state={
        		rate : 'Upload'
        }
    }

    _handleUploadError(err){
        this.setState({rate:'Error'})
    }

    _handleUploadFail(resp){
        this.setState({rate:'Fail'})
    }

    _handleUploadSuccess(progress, mill){
        this.setState({rate:'Upload'})
    }

    _handleDoUpload(progress, mill){
        this.setState({rate:'Upload'})
    }

    _handleUploading(progress, mill){
        let rate_round = Math.round(progress.loaded/progress.total * 100)
        this.setState({rate:rate_round})
    }

    componentDidMount(){
        console.log("componentDidMount")
    }

    componentDidUpdate(){
        console.log("componentDidUpdate")
    }

    shouldComponentUpdate(){
        console.log("shouldComponentUpdate")
        return true;
    }

    // return ftp upload rest api url
    setFormUrl(label){
        let testIp = "http://52.78.19.96:8989"  // will be deleted on jango server
        let uploadUrl = "/api/v1/type/imagefile/base/" + this.props.imageDataSet.baseDom + "/table/" + 
        this.props.imageDataSet.tableDom + "/label/" + label +"/data/"+ this.props.netId +"/"
        testIp = testIp + uploadUrl
        this.setState({formAction: testIp})

        let fileUploadSettings = this.fileUploadSettings
        this.fileUploadSettings.baseUrl = testIp 
    }

    render() {
    	if (!this.props.imageDataSet.imagePaths) {return null;}
    	let rows2 = [];
    	let fileUploadOptions = this.fileUploadSettings;
        console.log(fileUploadOptions)
    	let i=0, j=0;
    	let key_set = Object.keys(this.props.imageDataSet.imagePaths);

		for(let key of key_set)
		{
			let imagePaths_info = this.props.imageDataSet.imagePaths[key];
			let rows = [];
			let clickEvent = this.setFormUrl.bind(this, key)
			for(let path_info of imagePaths_info){
				let path = "http://52.78.19.96:8989" + path_info;
				rows.push(<div><img src= {path} key={i++} width='200' height='200'/></div>)
			}
			rows2.push(<dl className='img-box'>
						   <dt>
						   		<h1 className="circle-blue">{key}</h1>
						   		<FileUpload options={fileUploadOptions}>
					           		<button onClick={clickEvent} className="upload" ref="chooseAndUpload">{this.state.rate}</button>
					       		</FileUpload>
						   </dt>
						   <dd>
					   			{rows}
					   	   </dd>						
					   </dl>);
		}
    	

        return (   
					<div>
						{rows2}
					</div>
        )
    }
}