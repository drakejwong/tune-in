import React from 'react';
import { Redirect } from 'react-router';
import axios from "axios";
// reactstrap components
import {
    Button,
} from "reactstrap";

//import { AUTH_LINK } from '../constants';

class LoginButton extends React.Component {

    constructor(props) {
        super(props);

        this.state = {
            msg: this.props.msg ? this.props.msg : "Log In",
            redirect: false,
            userid:"xd"
        }
        this.doTheLogin = this.doTheLogin.bind(this);
    }

    doTheLogin() {
        axios.get('/api/login').then(res => {
                this.setState({
                    redirect: true, 
                    userid: res.data
                }
                );
            }
        );
    }
    
    render() {
        const redirectCheck = this.state.redirect;

        if (redirectCheck) {
            return <Redirect to={
                {pathname:'/dashboard',
            state : {loggedIn: "TRUE", userID:this.state.userid}
        }
            }/>
        } else {
            return (
                <>
                    <Button className="btn-round ml-auto" color="success" onClick={()=>this.doTheLogin()}>
                        <i className="tim-icons icon-single-02" /> {this.state.msg}
                    </Button>
                </>
                );
        }
        
    }
}

export default LoginButton;