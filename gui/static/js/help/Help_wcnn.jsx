import React from 'react'
import ReportRepository from './../repositories/ReportRepository'
import Api from './../utils/Api'


export default class Help_wcnn extends React.Component {
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
            let url1 = "./images/help_charCNN1.png"
            let url2 = "./images/help_charCNN2.png"
        return (  
            
            <div>
                <h1> Wcnn </h1>
                
                <div className="container tabBody">
<img src={url1} />
                <br />
                <br />
                <h3>
                워드 임베딩이 인기를 끌고 그 성능 또한 검증된 이후, 단어 결합이나 n-gram으로부터 높은 수준의 피처를 추출해내는 <br />
                효율적인 함수의 필요성이 증대됐다. 이러한 추상화된 피처들은 감성분석, 요약, 기계번역, 질의응답(QA) 같은 다양한 NLP <br />
                문제에 사용될 수 있다. <br />
                콘볼루션 신경망은 컴퓨터 비전 분야에서 뛰어난 성능으로 인해 자연스런 선택이었다<br />
                (Krizhevsky et al., 2012; Sharif Razavian et al., 2014; Jia et al., 2014). <br />
                문장 모델링에서 CNN을 활용하는 것은 Colobert and Weston(2008)로 거슬러 올라간다. <br />
                이 연구는 다범주 예측 결과를 출력하기 위해 multi-task learning을 사용했다. <br />
                품사태깅, 청킹, 개체명인식, 의미역결정, 의미적으로 유사한 단어 찾기, 랭귀지모델 같은 NLP 과제 수행을 위해서다. <br />
                참조테이블(look up table)은 각 단어를 사용자가 정의한 차원의 벡터로 변형해 사용된다. <br />
                따라서 n개의 단어로 이뤄진 입력문장 (s1,s2,..,sn)은 참조테이블을 활용해 벡터들의 나열인 (ws1,ws2,…,wsn)으로 변환된다.<br />
                </h3>
                <img src={url2} />
                <br />
                <br />
                <h3>
                이는 학습 과정에서 단어 벡터(가중치)가 학습되는 초기 단어 임베딩 기법의 아이디어로 생각할 수 있다. <br />
                Collobert et al. (2011)은 넘쳐나는 NLP 문제를 해결하기 위해 그의 이전 업적을 확장해 일반적인 CNN 기반의 프레임워크를 제안했다.<br />
                 Colobert and Weston(2008)과 Collobert et al. (2011)은 NLP 연구자들 사이에 CNN이 큰 인기를 끌도록 촉발시켰다.<br />
                  CNN이 이미 컴퓨터 비전 태스크에서 괄목할 만한 성능을 보인 상황에서 사람들이 CNN의 성능을 믿는 것은 쉬웠다. <br />
                  CNN은 문장의 잠재적인 semantic represention을 만들어내기 위해 입력 문장으로부터 핵심적인 n-gram 피처를 추출하는 능력을 갖고 있다.<br />
                   이 분야의 선구적인 업적은 Collobert et al. (2011), Kalchbrenner et al. (2014), Kim(2014)이다(본 블로그). <br />
                   이들은 후속 연구에서 CNN 기반의 네트워크가 크게 확산되도록 했다.<br />
                   </h3>
                </div>
            </div>
        )
    }
}


