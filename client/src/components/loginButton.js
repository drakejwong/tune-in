import React from 'react';

// reactstrap components
import {
    Button,
} from "reactstrap";

import { AUTH_LINK } from '../constants';
  
class LoginButton extends React.Component {

    constructor(props) {
        super(props);

        this.state = {
            msg: this.props.msg ? this.props.msg : "Log In"
        }
    }

    doTheLogin() {
        window.open(AUTH_LINK);
    }

    render() {
        return (
        <>
            <Button className="btn-round ml-auto" color="success">
                <i className="tim-icons icon-single-02" /> {this.state.msg}
            </Button>
        </>
        );
    }
}

export default LoginButton;