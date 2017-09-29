import React from 'react'
import { Router, Route, Link, browserHistory } from 'react-router'
import HomeComponent from './HomeComponent'
import LoginComponent from './LoginComponent'

export default class RouterComponent extends React.Component {
    render() {
        return (   
                <Router history = {browserHistory}>
                    <Route path="/" component={HomeComponent} />
                    <Route path="login" component={HomeComponent} />
                </Router>
        )
    }
}