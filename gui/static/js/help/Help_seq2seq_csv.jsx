import React from 'react'
import ReportRepository from './../repositories/ReportRepository'
import Api from './../utils/Api'


export default class Help_seq2seq_csv extends React.Component {
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
let url1 = "./images/help_seq2seq.png"
        return (  

            <div>
                <h1> Seq2Seq CSV </h1>
                
                <div className="container tabBody">
                <img src={url1} />
                    <br />
                <br />
                <h3>
        위 그림에 각 박스는 가장 일반적으로 GRU 쎌이거나 LSTM 쎌인 RNN 쎌을 나타낸다(RNN Tutorial를 참조하길 바란다). <br />
        인코더와 디코더는 가중치를 공유 할수 있거나, 더 일반적으로는 다른 매개변수 집합을 사용한다. <br />
        다중층 쎌들은 역시 시퀸스-투-시퀸스에서 성공적으로 사용되어 왔다. 예로 번역 Sutskever et al., 2014 (pdf)에서 알수 있다.<br />
        위에서 설명된 기본 모델에서, 모든 입력은 디코더에 전달되는 유일한 것이기 때문에 고정된 크기를 가진 상태 벡터로 인코딩 되어져야 한다. <br />
        디코더가 입력에 더 직접적인 접근을 가능케 하기 위해, 주의(attention) 메카니즘이 Bahdanau et al., 2014(pdf)에서 소개된다. <br />
        주의(attention) 메카나즘에 대해서 상세히 보지 않을 것이다(논문을 참고), 그것은 디코더가 모든 디코딩 단계에서 입력을 엿보게 해주는 <br />
        것이라고 언급하는 것만으로도 충분하다. LSTM 쎌을 가진 여러층의 시퀸스-투-시퀸스 네트워크와 디코더 안에 어탠션 메카니즘은 이처럼 보인다.<br />
<br />
        [번역] 가장 대표적인 사용예는 번역이 될 것이다. 요즘 Google 번역기가 매우 좋아진 것도 바로 이런 이유이다.<br />
        Encode : 안녕하세요. 오늘 기분은 어떠세요?<br />
        Decode : Hello. How are you feel today?<br />
        위와 같이 데이터를 구성하고 아래의 Network 을 이용하여 훈련을 시키면 “안녕하세요. 오늘 기분은 어떠세요?” 라고 입력을 하였을때, <br />
        “Hello. How are you feel today?”라는 답을 하는 네트워크가 구성되는 것이다.<br />
<br />
        [대화]번역뿐만 아니라 간단한 문/답에도 아래와 같이 적용해 볼 수 있을 것이다. (※단순 Seq2Seq 로 Alex 같은 것은 구현할 수 없다)<br />
        Encode : 안녕하세요!? <br />
        Decode : 잘가세요!?<br />

        [분류]Time Series 한 Classification 문제도 생각해 볼 수가 있다. 아래의 데이터를 주가의 흐름이라고 하자<br />
        Encode : 1900, 1800, 1700, 1600, 2000 <br />
        Decode : Up/Down<br />
        예를 들면 종합 주가지수가 1900, 1800, 1700, 1600, 2000 와 같이 변동해 왔을때, 내일의 주가는 내려갈까요? 올라갈까요? 와 같은 <br />
        형태의 질문도 훈련을 할 수가 있을 것이다.<br />
        </h3>
                </div>
            </div>
        )
    }
}


