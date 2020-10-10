import React, { Component } from "react";
import { BrowserRouter, Switch, Route } from "react-router-dom";
//import { Provider } from 'react-redux';
import PropTypes from 'prop-types'

//import axios from "axios";

import Home from "./components/Home";
import Dashboard from "./components/Dashboard";
import Preview from "./components/Preview";

export default class App extends Component {
  constructor() {
    super();
  }

  render() {
    return (
      <div className="App">
        
        <BrowserRouter>
          <Switch>
            <Route
              exact
              path={"/"}
              render={props => (
                <Home
                  {...props}
                  
                />
              )}
            />
            <Route
              exact
              path={"/partytime"}
              render={props => (
                <Dashboard
                  {...props}
                />
              )}
            />
             <Route
              exact
              path={"/preview"}
              render={props => (
                <Preview
                  {...props}
                />
              )}
            />
          </Switch>
        </BrowserRouter>
        
        
      </div>
    );
  }
}