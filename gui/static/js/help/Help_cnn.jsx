import React from 'react'
import ReportRepository from './../repositories/ReportRepository'
import Api from './../utils/Api'
import EnvConstants from './../constants/EnvConstants';

export default class Help_cnn extends React.Component {
    constructor(props, context) {
        super(props);
        this.state = {
        	NN_TableData: null,
            url1:EnvConstants.getImgUrl()+"help_cnn1.png",
            url2:EnvConstants.getImgUrl()+"help_cnn2.png",
            url3:EnvConstants.getImgUrl()+"help_cnn3.png",
            url4:EnvConstants.getImgUrl()+"help_cnn4.png",
            url5:EnvConstants.getImgUrl()+"help_cnn5.png",
            url6:EnvConstants.getImgUrl()+"help_cnn6.png",
            url7:EnvConstants.getImgUrl()+"help_cnn7.png",
            url8:EnvConstants.getImgUrl()+"help_cnn8.png",
            url9:EnvConstants.getImgUrl()+"help_cnn9.png"
        };

    }
    /////////////////////////////////////////////////////////////////////////////////////////
    // Search Function
    /////////////////////////////////////////////////////////////////////////////////////////
    componentDidMount() {
    }

    render() {
        return (  

            <div>
                
                <div className="container tabBody">
                <br/><br/><br/>                
        <table>
<tr>
<td></td>
<td style={{"width":"60%"}}>
<h1> Convolutional Neural Network </h1><br/><br/>
<img src={this.state.url1} style={{"width":"100%"}}/><br/>
</td>
<td></td>
</tr>
<tr>
<td></td>
<td style={{"textAlign":"left","width":"60%"}}>
<h3>
ConvNet의 각 레이어는 미분 가능한 변환 함수를 통해 하나의 액티베이션 볼륨을 또다른 액티베이션 볼륨으로 변환 (transform) 시킨다.
ConvNet 아키텍쳐에서는 크게 컨볼루셔널 레이어, 풀링 레이어, Fully-connected 레이어라는 3개 종류의 레이어가 사용된다.
전체 ConvNet 아키텍쳐는 이 3 종류의 레이어들을 쌓아 만들어진다.<br/>
<br/>
- INPUT 입력 이미지가 가로32, 세로32, 그리고 RGB 채널을 가지는 경우 입력의 크기는 [32x32x3].<br/>
- CONV 레이어는 입력 이미지의 일부 영역과 연결되어 있으며, 이 연결된 영역과 자신의 가중치의 내적 연산 (dot product) 을 계산하게 된다.<br/>
&nbsp;&nbsp;결과 볼륨은 [32x32x12]와 같은 크기를 갖게 된다.<br/>
- RELU 레이어는 max(0,x)와 같이 각 요소에 적용되는 액티베이션 함수 (activation function)이다.<br/>
&nbsp;&nbsp;이 레이어는 볼륨의 크기를 변화시키지 않는다 ([32x32x12])<br/>
- POOL 레이어는 (가로,세로) 차원에 대해 다운샘플링 (downsampling)을 수행해 [16x16x12]와 같이 줄어든 볼륨을 출력한다.<br/>
- FC (fully-connected) 레이어는 클래스 점수들을 계산해 [1x1x10]의 크기를 갖는 볼륨을 출력한다.<br/>
&nbsp;&nbsp;10개 숫자들은 10개 카테고리에 대한 클래스 점수에 해당한다. 레이어의 이름에서 유추 가능하듯,<br/>
&nbsp;&nbsp;이 레이어는 이전 볼륨의 모든 요소와 연결되어 있다.<br/>
<br/>
이와 같이, ConvNet은 픽셀 값으로 이뤄진 원본 이미지를 각 레이어를 거치며 클래스 점수로 변환 (transform) 시킨다.
한 가지 기억할 것은, 어떤 레이어는 모수 (parameter)를 갖지만 어떤 레이어는 모수를 갖지 않는다는 것이다.
특히 CONV/FC 레이어들은 단순히 입력 볼륨만이 아니라 가중치(weight)와 바이어스(bias) 또한 포함하는
액티베이션(activation) 함수이다. 반면 RELU/POOL 레이어들은 고정된 함수이다.
CONV/FC 레이어의 모수 (parameter)들은 각 이미지에 대한 클래스 점수가 해당 이미지의 레이블과 같아지도록
그라디언트 디센트 (gradient descent)로 학습된다.<br/>
<br/>
요약해보면:<br/>
- ConvNet 아키텍쳐는 여러 레이어를 통해 입력 이미지 볼륨을 출력 볼륨 ( 클래스 점수 )으로 변환시켜 준다.<br/>
- ConvNet은 몇 가지 종류의 레이어로 구성되어 있다. CONV/FC/RELU/POOL 레이어가 현재 가장 많이 쓰인다.<br/>
- 각 레이어는 3차원의 입력 볼륨을 미분 가능한 함수를 통해 3차원 출력 볼륨으로 변환시킨다.<br/>
- 모수(parameter)가 있는 레이어도 있고 그렇지 않은 레이어도 있다 (FC/CONV는 모수를 갖고 있고, RELU/POOL 등은 모수가 없음).<br/>
- 초모수 (hyperparameter)가 있는 레이어도 있고 그렇지 않은 레이어도 있다 (CONV/FC/POOL 레이어는 초모수를 가지며 RELU는 가지지 않음).
</h3>
</td>
<td></td>
</tr>
</table>
<br/><br/>

                </div>
            </div>
        )
    }
}


