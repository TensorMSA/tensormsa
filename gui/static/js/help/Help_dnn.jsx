import React from 'react'
import ReportRepository from './../repositories/ReportRepository'
import Api from './../utils/Api'
import EnvConstants from './../constants/EnvConstants';

export default class Help_wdnn extends React.Component {
    constructor(props, context) {
        super(props);
        this.state = {
        	NN_TableData: null,
            url1:EnvConstants.getImgUrl()+"help_dnn1.png"
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

                    <br />
                <br />
                <h3>
<table>
<tr>
<td></td>
<td style={{"width":"50%"}}>
<h1> Deep Neural Network </h1><br/><br/>
<img src={this.state.url1} />
</td>
<td></td>
</tr>
<tr>
<td></td>
<td style={{"textAlign":"left","width":"50%"}}><br />
Multi-Layer Perceptron이라고도 하며 입력층과 출력층 사이에 하나 이상의 중간층이 존재하는 신경망으로 그림에 나타낸 것과 같은 계층
구조를 갖는다. 이 때 입력층과 출력층 사이의 중간층을 은닉층 (hidden layer) 이라 부른다. 네트워크는 입력층, 은닉층, 출력층 방향으로
연결되어 있으며, 각 층내의 연결과 출력층에서 입력층으로의 직접적인 연결은 존재하지 않는 전방향 (Feedforward) 네트워크이다.
Multilayer perceptron 은 단층 perceptron 과 유사한 구조를 가지고 있지만 중간층과 각 unit 의 입출력 특성을 비선형으로 함으로써
네트워크의 능력을 향상시켜 단층 퍼셉트론 (Perceptron) 의 여러 가지 단점들을 극복했다. Multi layer perceptron 은 층의 갯수가
증가할수록 perceptron 이 형성하는 결정 구역의 특성은 더욱 고급화된다. 즉 단층일 경우 패턴공간을 두 구역으로 나누어주고, 2 층인
경우 볼록한 (convex) 개구역 또는 오목한 폐구역을 형성하며, 3 층인 경우에는 이론상 어떠한 형태의 구역도 형성할 수 있다.
지금까지는 주로 계단형 (hard limiting) 의 비선형 (noolinear) 활성함수를 사용하고 출력 unit 가 하나인 multilayer perceptron에
대하여 논의하였는데 이와 비슷한 결과가 시그모이드 비선형 활성함수를 적용한 한 개 이상의 출력 unit 를 가진 네트워크에도 나타난다.
시그모이드 비선형 활성함수를 적용할 경우 결정 영역이 통상 직선이 아닌 완만한 곡선으로 경계지워지므로 행위의 분석이 약간 복잡하지만
미분이 가능하므로 오히려 은닉층을 학습할 수 있는 Backpropagation 학습 알고리즘을 수행할 수 있다. 대부분의 multilayer perceptron은
역전파 (Back-propagation) 학습 알고리즘을 사용하여 학습시킬 수 있다.
</td>
<td></td>
</tr>
</table>
</h3>
<br />
<br />
                </div>
            </div>
        )
    }
}


