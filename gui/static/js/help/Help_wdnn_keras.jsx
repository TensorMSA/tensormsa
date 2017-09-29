import React from 'react'
import ReportRepository from './../repositories/ReportRepository'
import Api from './../utils/Api'


export default class Help_wdnn_keras extends React.Component {
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
let url1 = "./images/help_wdnn1.png"
let url2 = "./images/help_wdnn2.png"
        return (  

            <div>
                <h1> Wdnn Keras</h1>
                
                <div className="container tabBody">
        <img src={url1} />
                    <br />
                <br />
                <h3>
                구글 리서치 블로그에서 머신 러닝의 로지스틱 회귀(Regression)와 뉴럴 네트워크 모델을 조합하여 추천 시스템에 <br />
                적용한 연구 내용을 올렸습니다. 두 모델을 조합하는 API는 TF learn에 위치해 있습니다. <br />
                TF Learn은 이전에 독립된 레파지토리에 있다가 0.8 버전에서 합쳐진 scikit flow(skflow)를 다르게 부르는 것 같습니다. <br />
                하지만 또 다른 서드파티 라이브러리 tflearn과 헷갈리게 됐습니다.
                와이드앤 딥 러닝 모델은 검색이나 추천시스템, 랭킹 모델에서 전체 트래픽은 많지만 매칭된 데이터는 드문 경우 모델이 <br />
                너무 구체화(overfit)되거나 너무 일반화(underfit) 되는 것을 적절히 안배하기 위하여 고안되었다고 합니다. <br />
                블로그에서는 음식 추천을 예로 들어 설명하고 있는데요. 로지스틱 회귀의 경우 주어진 검색어에 대해 어떤 음식이 추천되었을 때 <br />
                주문이 일어날 가능성이 높은 순으로 추천이 일어나게 될 것입니다. <br />
                이런 경우 추천시스템 쪽에서 이야기하는 세렌티피티(Serendipity)가 부족하다고 말합니다. <br />
                즉 사용자가 깜짝 놀랄 추천을 하지 못하고 판에박힌 아이템만 늘어놓게 되는 경우입니다. <br />
                임베딩 벡터를 사용한 딥 뉴럴 네트워크를 이용할 경우 프라이드 치킨을 검색한 사용자에게 햄버거를 추천할 수 있다고 합니다. <br />
                하지만 딥 러닝 모델은 아이스 라떼를 요청한 사람에게 뜨거운 라떼를 추천할 수도 있기에 와이드한 것과 딥한 두 모델을 적절히 안배하는 <br />
                것이 좋다고 말하고 있습니다.
<br /><br />
                와이드 모델과 딥 모델에 각각 어떤 피처(feature)를 사용할지 뉴럴 네트워크의 레이어를 어떻게 구성할지는 당연히 이용자의 몫입니다. <br />
                와이드앤 딥 러닝 모델을 위해 skflow에 추가된 API는 tf.contrib.learn.DNNLinearCombinedClassifier 와 <br />
                tf.contrib.learn.DNNLinearCombinedRegressor 입니다. 아마도 로지스틱 회귀를 위한 펼쳐진 뉴런의 모습에서 와이드(wide)하다는<br />
                 표현을 쓰는 것으로 보입니다. <br />

</h3>
<img src={url2} />
<br />
<br />
<h3>

                Word2Vec 는 기본적으로 유사한 의미를 갖는 단어는 비슷한 문맥에서 등장한다는 이론을 바탕에 두고 있다. <br />
                예를들면 (음식)을 먹는다. 형태의 문맥이 있다고 하면 “사과를 먹는다. 포도를 먹는다. 밥을 먹는다. <br />
                모든 문장은 먹는다와 근처에서 발생하게 된다. <br />
                이러한 특징을 바탕으로 백터를 훈련하면 유사한 의미를 갖는 단어들은 유사한 백터 분포를 갖는다라고 말한다.  <br />
                Word Embedding 기법은 모든 자연어 처리 알고리즘에 있어서 가장 중요한 전처리 작업으로 최근에는 전체 도큐먼트의 <br />
                발생 빈도를 고려하는 Glove나 Ngram 방법을 접목한 FastText 등이 주로 사용되고 있으며, 순수한 Word2Vector <br />
                알고리즘 자체는 잘 사용하지 않는 추세이긴 하지만 매우 중요한 개념이라는 것은 변함 없다.<br />

</h3>
                </div>
            </div>
        )
    }
}


