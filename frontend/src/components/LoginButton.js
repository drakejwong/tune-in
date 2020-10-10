import React from 'react';
import { Redirect } from 'react-router';
import axios from "axios";
import 'font-awesome/css/font-awesome.min.css';
// reactstrap components
import {
    Button
} from "reactstrap";

//import { AUTH_LINK } from '../constants';

class LoginButton extends React.Component {

    constructor(props) {
        super(props);

        this.state = {
            msg: this.props.msg ? this.props.msg : "Log In",
            redirect: false,
            userid: "xd",
            loading: false
        }
        this.showLoading = this.showLoading.bind(this);
        this.hideLoading = this.hideLoading.bind(this);
        this.doTheLogin = this.doTheLogin.bind(this);
        
    }
    showLoading() {
        this.setState({loading: true});
    }
    hideLoading() {
        setTimeout(()=> {this.setState({loading: false});}, 2000)
    }
    doTheLogin() {
        this.showLoading();
        axios.get('/api/login').then(res => {
                this.setState({
                    redirect: true, 
                    userid: res.data,
                }
                );
                this.hideLoading();
            }
        );
    }
    
    render() {
        const redirectCheck = this.state.redirect;
        const loadingCheck = this.state.loading;
        if (redirectCheck) {
            return <Redirect to={
                {pathname:'/partytime',
            state : {loggedIn: true, userID:this.state.userid}
        }
            }/>
        } else {
            return (
                <>
                    <Button className="btn-round ml-auto" size="lg" color="success" onClick={()=>this.doTheLogin()}>
                        {!loadingCheck ? <span><i className="tim-icons icon-key-25"/> {this.state.msg} </span> : <span><i className="fa fa-refresh fa-spin"/> Logging You In...</span>}
                    </Button>
                </>
                );
        }
        
    }
}

export default LoginButton;