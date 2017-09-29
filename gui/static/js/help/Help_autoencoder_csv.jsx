import React from 'react'
import ReportRepository from './../repositories/ReportRepository'
import Api from './../utils/Api'


export default class Help_autoencoder_csv extends React.Component {
    constructor(props, context) {
        super(props);
        this.state = {
        	NN_TableData: null
        };

    }
    /////////////////////////////////////////////////////////////////////////////////////////
    // Search Function
    /////////////////////////////////////////////////////////////////////////////////////////
    componentDidMount() {
    }

    render() {
        let url1 = "./images/help_autoencoder_csv.png"

        return (  

            <div>
                <h1> Autoencoder CSV </h1>
                
                <div className="container tabBody">
                    <img src={url1} />
                    <br />
                <br />
                <h3>
                AutoEncoder 를  정형 데이터 적용하기 위한 알고리즘을 제공한다. <br />
                AutoEncoder는  Unsupervised 형태의 훈련 알고리즘으로 별도의 레이블 값 없이 Encoder 와 Decoder 형태의 모델로 <br />
                인풋 데이터와 같은 아웃풋을 다시 생성해 내는 것을 목표로 하는 알고리즘이다.<br />
                Anomlay Detection 의 경우 데이터의 분포가 매우 불균형한 바이너리 클레시피케이션 문제를 풀기 위한 방법의 하나이다. <br />
                AutoEncoder 로  Anomlay Detection 문제를 접근 할 수 있는데, 풍부한 데이터 레이블을 기준으로 훈련하여 해당 데이터를 <br />
                잘 설명 할 수 있도록 훈련하여 자신의 데이터를 잘 복월할 수 있도록 훈련한다. 모델을 사용시에는 Feed Worwarding 하여 <br />
                Decoder 에서 복원된 데이터와 입력한 데이터의 백터간의 유사도 차이가 기준치보다 복원을 잘 못할 경우 비정상 데이터로 판별하는 <br />
                방법으로 사용할 수 있다.
                </h3>
                </div>
            </div>
        )
    }
}


