import React from 'react';

// reactstrap components
import {
    NavbarBrand,
    Navbar,
    Button,
  } from "reactstrap";
  
  class TopBar extends React.Component {
    render() {
      return (
        <>
          <Navbar color-on-scroll="100" className="navbar-transparent" expand="lg">
            <NavbarBrand href="#" onClick={e => e.preventDefault()}>
                <h3 id="content" style={{margin:0}}>TuneIn</h3>
            </NavbarBrand>
            <Button className="btn-round ml-auto" color="success">
                <i className="tim-icons icon-single-02" /> Sign In
            </Button>
          </Navbar>
        </>
      );
    }
  }
  
  export default TopBar;