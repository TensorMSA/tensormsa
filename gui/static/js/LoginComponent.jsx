import React from 'react'
import { Link } from 'react-router'

export default class LoginComponent extends React.Component {
    render() {
        return (
                <section data-reactroot="" id="login-section">
                    <div className="login_container">
                        <div className="login_desc">
                            <strong>
                            Thank you for visiting our website!
                            </strong>
                            Play with data, Enjoy deep learning
                        </div>
                        <div className="login_area">
                            <div className="login_title">HOYA LOGIN</div>
                            <div className="login_form">
                                <div className="login_input">
                                    <input type="text" placeholder="ID" />
                                    <input type="password" placeholder="password" />
                                </div>
                                <div className="login_btn">
                                    <Link to="login"><input type="button" value="Login" /></Link>
                                </div>
                            </div>
                        </div>
                    </div>
                    <div className="copyright_area">Copyrights POSCO ICT.All rights reserved</div>
                </section>
            )
    }
}