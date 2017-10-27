import React from 'react'
import ReportRepository from './../repositories/ReportRepository'
import Api from './../utils/Api'
import EnvConstants from './../constants/EnvConstants';

export default class Help_wdnn extends React.Component {
    constructor(props, context) {
        super(props);
        this.state = {
        	NN_TableData: null,
            url1:EnvConstants.getImgUrl()+"help_wdnn1.png",
            url2:EnvConstants.getImgUrl()+"help_wdnn2.png",
            url3:EnvConstants.getImgUrl()+"help_wdnn3.png",
            url4:EnvConstants.getImgUrl()+"help_wdnn4.png",
            url5:EnvConstants.getImgUrl()+"help_wdnn5.png"                        
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
                <br />

                    <table>
                    <tr>
                    <td></td>
                    <td style={{"textAlign":"center", "width":"800px"}}>
                    <h1> Wide and Deep Neural Network</h1>                    
                    <br /><br />

                    <h1> Monetization and Wide model (기억과 와이드 모델) </h1> </td>
                    <td></td>
                    </tr>
                    <br />

                    <tr>
                    <td></td>
                    <td style={{"textAlign":"left", "width":"800px"}}>                                  
                    <h3>
                    로지스틱 회귀 모델을 이용하여 추천 알고리즘을 작성하여 학습을 시킨 경우, 학습 데이타를 기반으로 상세화된 예측 결과를 리턴해준다.
                    예를 들어 검색 키워드 (프라이드 치킨)으로 검색한 사용자가(치킨과 와플)을 주문한 기록이 많았다면,
                    이 모델은 (프라이드 치킨)으로 검색한 사용자는 항상 (치킨과 와플)을 추천해주게 된다.
                    즉 예전에 기억된 값 (Memorization된 값)을 통해서 예측을 하는데, 이러한 모델을 와이드 모델이라고 한다.</h3></td>
                    <td></td>
                    </tr>
                    <br />

                    <tr>
                    <td></td>
                    <td style={{"textAlign":"center", "width":"800px"}}> <img src={this.state.url3} /> <br />
                    그림-와이드 모델 </td>
                    <td></td>
                    </tr>

                    <br />
                    <tr>
                    <td></td>
                    <td style={{"textAlign":"left", "width":"800px"}}> 
                    <h3>그러나 (프라이드 치킨)으로 검색한 사용자에게 같은 패스트 푸드 종류인 햄버거나 프렌치프라이등을 추천해도
                    잘 구매가 되지만 와이드 모델은 기존에 기억된 결과로만 추천을 하기 때문에 이러한 결과를 얻기가 어렵다.</h3></td>
                    <td></td>
                    </tr>

                    <br /><br />
                    <tr>
                    <td></td>
                    <td style={{"textAlign":"center", "width":"800px"}}> <tr />
                    <h1> Generalization and Deep model (일반화와 딥모델) </h1><br /></td>
                    <td></td>
                    </tr>

                    <tr>
                    <td></td>
                    <td style={{"textAlign":"left", "width":"800px"}}>                    
                    <h3>
                    뉴럴네트워크 모델의 경우 프라이드 치킨을 햄버거, 프랜치 프라이등을 일반화 시켜서 패스트 푸드로 분류하여 프라이드 치킨으로 검색을 해도 이와 같은 종류의 햄버거를 추천해도 사용자가 택할 가능성이 높다.
                    </h3><br /></td>
                    <td></td>
                    </tr>

                    <tr>
                    <td></td>
                    <td style={{"textAlign":"center", "width":"800px"}}> <img src={this.state.url4} /> <br />
                    그림- 딥 모델 <br /> </td>
                    <td></td>
                    </tr>

                    <br />

                    <tr>
                    <td></td>
                    <td style={{"textAlign":"left", "width":"800px"}}>                     
                    <h3>이러한 모델을 딥모델이라고 하는데, 딥 모델의 경우 문제점이, 너무 일반화가(under fitting)되서 엉뚱한 결과가 나올 수 있다는 것인데, 
                    예를 들어서 따뜻한 아메리카노를 검색했는데, 커피라는 일반화 범주에서 아이스 라떼를 추천해줄 수 있다는 것이다. 
                    즉 커피라는 일반화 범주에서 라떼는 맞는 추천일 수 있지만, 따뜻한 음료를 원하는 사람에게 차가운 음료를 추천하는 지나친 일반화가 발생할 수 있다.
                    그래서 이런 문제를 해결하기 위해서 와이드 모델과 딥모델을 합친 “Wide & deep model”이라는 것을 구글이 개발하였고 이를 구글 플레이 스토어에 적용한 결과, 
                    큰 효과를 얻었다고 한다. (https://arxiv.org/abs/1606.07792) 
                    </h3>
                    <br /></td>
                    <td></td>
                    </tr>

                    <tr>
                    <td></td>
                    <td style={{"textAlign":"center", "width":"800px"}}> <img src={this.state.url5} /> <br /><br />
                    그림- 와이드 앤 딥모델 <br /> </td>
                    <td></td>
                    </tr>
                    </table>

                    <br /><br />
            </div>
        </div>
        )
    }
}


