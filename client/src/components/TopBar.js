import React from 'react';

// reactstrap components
import {
    NavbarBrand,
    Navbar,
  } from "reactstrap";
  
import LoginButton from './loginButton';
import '../styles/TopBar.css';
  
  class TopBar extends React.Component {
    render() {
      return (
        <>
          <Navbar color-on-scroll="100" className="navbar-transparent tuneinnav sticky-top" expand="lg">
            <NavbarBrand href="#" onClick={e => e.preventDefault()}>
                <h3 id="content" style={{margin:0}}>TuneIn</h3>
            </NavbarBrand>
            <LoginButton />
          </Navbar>
        </>
      );
    }
  }
  
  export default TopBar;