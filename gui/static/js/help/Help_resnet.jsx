import React from 'react'
import ReportRepository from './../repositories/ReportRepository'
import Api from './../utils/Api'


export default class Help_resnet extends React.Component {
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
        let url1 = "./images/help_resnet1.png"
        let url2 = "./images/help_resnet2.png"
        return (  

            <div>
                <h1> Resnet </h1>
                
                <div className="container tabBody">
                <img src={url1} />
                <br />
                <br />
                <h3>
                ILSVRC의 winning 네트워크들의 추세를 봐도 알수 있는 사실이지만 네트워크의 레이어를 층층이 쌓아서 깊게 구현하면 더 <br />
                좋은 성능을 낸다. 하지만 레이어를 깊게 쌓는 것이 항상 좋은 결과를 낼 까? 네트워크를 깊게 쌓으면 gradient vanishing<br />
                exploding 현상이 발생할 수 있기 때문에 네트워크는 학습의 초기 단계부터 saturated되어 버릴 우려가 있다. 하지만 이 <br />
                문제는 BN, Xavier 초기화(PReLU-net 참조) 등을 이용하면 수십개의 레이어까지는 해결이 된 상태이다. 하지만 네트워크가 <br />
                더 깊어지면 degradation 이라 불리는 문제가 발생한다. 네트워크는 깊어지는데 정확도는 saturated 되는 현상이다. 사실 <br />
                이는 overfit을 생각하면 당연하다고 생각 할 수 있지만 놀랍게도 degradation은 overfit에 의한 것이 아닌 애초에 트레<br />
                이닝 에러 자체가 높아지는 현상이다. 아래 그림은 degradation의 예시를 보여준다.<br />
                </h3>

                <img src={url2} />
                 <br />
                  <br />
                <h3>
                일반적인(Plain) 네트워크는 위와 같은 레이어 구조를 가진다. 이 때 두 레이어를 거친 후 매핑된 결과는 H(x) 로 표현하며 <br />
                아래와 같이 표현 H(x)=F(x,Wi) 여기서 위 네트워크는 2개의 레이어를 가지고 있기 때문에 F=W2σ(W1x) 이다. x 는 입력 <br />
                벡터이며 σ 는 ReLU activation을 의미한다. 식을 간단히 쓰기 위해서 바이어스는 생략하였다. residual 네트워크는 일반<br />
                적인 네트워크와는 달리 몇개의 레이어 (여기에서는 2개의 레이어)를 건너 뛴 shortcut을 활용한 것이 특징이다. H(x) 는 <br />
                H(x)=F+x 으로 표현할 수 있다.<br />
                </h3>
                </div>
            </div>
        )
    }
}


