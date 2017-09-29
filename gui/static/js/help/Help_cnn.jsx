import React from 'react'
import ReportRepository from './../repositories/ReportRepository'
import Api from './../utils/Api'


export default class Help_cnn extends React.Component {
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
        let url1 = "./images/help_cnn1.png"
        let url2 = "./images/help_cnn2.png"
        let url3 = "./images/help_cnn3.png"
        let url4 = "./images/help_cnn4.png"
        let url5 = "./images/help_cnn5.png"
        let url6 = "./images/help_cnn6.png"
        let url7 = "./images/help_cnn7.png"
        let url8 = "./images/help_cnn8.png"
        let url9 = "./images/help_cnn9.png"
        return (  

            <div>
                <h1> Cnn </h1>
                
                <div className="container tabBody">
        <img src={url1} />
                <br />
                <br />
                <h2>컨볼루션 신경망 (ConvNet)</h2>

                <h3>컨볼루션 신경망 (Convolutional Neural Network, 이하 ConvNet)은 앞 장에서 다룬 일반 신경망과 매우 유사하다.<br />
                 ConvNet은 학습 가능한 가중치 (weight)와 바이어스(bias)로 구성되어 있다. <br />
                 각 뉴런은 입력을 받아 내적 연산( dot product )을 한 뒤 선택에 따라 비선형 (non-linear) 연산을 한다. <br />
                 전체 네트워크는 일반 신경망과 마찬가지로 미분 가능한 하나의 스코어 함수 (score function)을 갖게 된다 <br />
                 (맨 앞쪽에서 로우 이미지 (raw image)를 읽고 맨 뒤쪽에서 각 클래스에 대한 점수를 구하게 됨). <br />
                 또한 ConvNet은 마지막 레이어에 (SVM/Softmax와 같은) 손실 함수 (loss function)을 가지며, 우리가 일반 신경망을 학습시킬 때 <br />
                 사용하던 각종 기법들을 동일하게 적용할 수 있다.<br /><br />

                ConvNet과 일반 신경망의 차이점은 무엇일까? ConvNet 아키텍쳐는 입력 데이터가 이미지라는 가정 덕분에 이미지 데이터가 갖는 <br />
                특성들을 인코딩 할 수 있다. 이러한 아키텍쳐는 포워드 함수 (forward function)을 더욱 효과적으로 구현할 수 있고 네트워크를 <br />
                학습시키는데 필요한 모수 (parameter)의 수를 크게 줄일 수 있게 해준다.<br /><br />

                </h3>
                <h2>아키텍쳐 개요</h2>
                <h3>
                앞 장에서 보았듯이 신경망은 입력받은 벡터를 일련의 히든 레이어 (hidden layer) 를 통해 변형 (transform) 시킨다. <br />
                각 히든 레이어는 뉴런들로 이뤄져 있으며, 각 뉴런은 앞쪽 레이어 (previous layer)의 모든 뉴런과 연결되어 있다 (fully connected).<br />
                 같은 레이어 내에 있는 뉴런들 끼리는 연결이 존재하지 않고 서로 독립적이다. 마지막 Fully-connected 레이어는 출력 레이어라고 불리며,<br />
                  분류 문제에서 클래스 점수 (class score)를 나타낸다.<br /><br />

                일반 신경망은 이미지를 다루기에 적절하지 않다. CIFAR-10 데이터의 경우 각 이미지가 32x32x3 (가로,세로 32, 3개 컬러 채널)로 <br />
                이뤄져 있어서 첫 번째 히든 레이어 내의 하나의 뉴런의 경우 32x32x3=3072개의 가중치가 필요하지만, 더 큰 이미지를 사용할 경우에는 <br />
                같은 구조를 이용하는 것이 불가능하다. 예를 들어 200x200x3의 크기를 가진 이미지는 같은 뉴런에 대해 200x200x3=120,000개의 가중치를 <br />
                필요로 하기 때문이다. 더욱이, 이런 뉴런이 레이어 내에 여러개 존재하므로 모수의 개수가 크게 증가하게 된다. 이와 같이 Fully-connectivity는<br />
                 심한 낭비이며 많은 수의 모수는 곧 오버피팅(overfitting)으로 귀결된다.<br /><br />

                ConvNet은 입력이 이미지로 이뤄져 있다는 특징을 살려 좀 더 합리적인 방향으로 아키텍쳐를 구성할 수 있다. 특히 일반 신경망과 달리, ConvNet의<br />
                 레이어들은 가로,세로,깊이의 3개 차원을 갖게 된다 ( 여기에서 말하는 깊이란 전체 신경망의 깊이가 아니라 액티베이션 볼륨 ( activation volume )<br />
                  에서의 3번 째 차원을 이야기 함 ). 예를 들어 CIFAR-10 이미지는 32x32x3 (가로,세로,깊이) 의 차원을 갖는 입력 액티베이션 <br />
                 볼륨 (activation volume)이라고 볼 수 있다. 조만간 보겠지만, 하나의 레이어에 위치한 뉴런들은 일반 신경망과는 달리 앞 레이어의 전체 뉴런이 <br />
                 아닌 일부에만 연결이 되어 있다. ConvNet 아키텍쳐는 전체 이미지를 클래스 점수들로 이뤄진 하나의 벡터로 만들어주기 때문에 마지막 출력 <br />
                 레이어는 1x1x10(10은 CIFAR-10 데이터의 클래스 개수)의 차원을 가지게 된다. 이에 대한 그럼은 아래와 같다:<br />


                </h3>
<br />
                <br />
<img src={url2} />
                <br />
 
                <h2>ConvNet을 이루는 레이어들</h2>

                <h3>위에서 다룬 것과 같이, ConvNet의 각 레이어는 미분 가능한 변환 함수를 통해 하나의 액티베이션 볼륨을 또다른 액티베이션 볼륨으로<br />
                 변환 (transform) 시킨다. ConvNet 아키텍쳐에서는 크게 컨볼루셔널 레이어, 풀링 레이어, Fully-connected 레이어라는 3개 종류의 <br />
                 레이어가 사용된다. 전체 ConvNet 아키텍쳐는 이 3 종류의 레이어들을 쌓아 만들어진다.<br /><br />

                *예제: 아래에서 더 자세하게 배우겠지만, CIFAR-10 데이터를 다루기 위한 간단한 ConvNet은 [INPUT-CONV-RELU-POOL-FC]로 구축할 수 있다.<br /><br />

                INPUT 입력 이미지가 가로32, 세로32, 그리고 RGB 채널을 가지는 경우 입력의 크기는 [32x32x3].<br />
                CONV 레이어는 입력 이미지의 일부 영역과 연결되어 있으며, 이 연결된 영역과 자신의 가중치의 내적 연산 (dot product) 을 계산하게 된다. <br />
                결과 볼륨은 [32x32x12]와 같은 크기를 갖게 된다.<br />
                RELU 레이어는 max(0,x)와 같이 각 요소에 적용되는 액티베이션 함수 (activation function)이다. <br />
                이 레이어는 볼륨의 크기를 변화시키지 않는다 ([32x32x12])<br />
                POOL 레이어는 (가로,세로) 차원에 대해 다운샘플링 (downsampling)을 수행해 [16x16x12]와 같이 줄어든 볼륨을 출력한다.<br />
                FC (fully-connected) 레이어는 클래스 점수들을 계산해 [1x1x10]의 크기를 갖는 볼륨을 출력한다. <br />
                10개 숫자들은 10개 카테고리에 대한 클래스 점수에 해당한다. 레이어의 이름에서 유추 가능하듯, 이 레이어는 이전 볼륨의 모든 요소와 연결되어 있다.<br /><br />

                이와 같이, ConvNet은 픽셀 값으로 이뤄진 원본 이미지를 각 레이어를 거치며 클래스 점수로 변환 (transform) 시킨다. <br />
                한 가지 기억할 것은, 어떤 레이어는 모수 (parameter)를 갖지만 어떤 레이어는 모수를 갖지 않는다는 것이다. <br />
                특히 CONV/FC 레이어들은 단순히 입력 볼륨만이 아니라 가중치(weight)와 바이어스(bias) 또한 포함하는 액티베이션(activation) 함수이다. <br />
                반면 RELU/POOL 레이어들은 고정된 함수이다. CONV/FC 레이어의 모수 (parameter)들은 각 이미지에 대한 클래스 점수가 해당 이미지의 레이블과 <br />
                같아지도록 그라디언트 디센트 (gradient descent)로 학습된다.<br /><br />

                요약해보면:<br /><br />

                ConvNet 아키텍쳐는 여러 레이어를 통해 입력 이미지 볼륨을 출력 볼륨 ( 클래스 점수 )으로 변환시켜 준다.<br />
                ConvNet은 몇 가지 종류의 레이어로 구성되어 있다. CONV/FC/RELU/POOL 레이어가 현재 가장 많이 쓰인다.<br />
                각 레이어는 3차원의 입력 볼륨을 미분 가능한 함수를 통해 3차원 출력 볼륨으로 변환시킨다.<br />
                모수(parameter)가 있는 레이어도 있고 그렇지 않은 레이어도 있다 (FC/CONV는 모수를 갖고 있고, RELU/POOL 등은 모수가 없음).<br />
                초모수 (hyperparameter)가 있는 레이어도 있고 그렇지 않은 레이어도 있다 (CONV/FC/POOL 레이어는 초모수를 가지며 RELU는 가지지 않음).<br />

                </h3>

                </div>
            </div>
        )
    }
}


