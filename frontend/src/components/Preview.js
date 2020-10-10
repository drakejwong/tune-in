import React, { Component } from 'react';

import { Redirect } from 'react-router';
import './Card.css';
import './Preview.css';
import {
  Button,
} from "reactstrap";

export default class Preview extends Component {
    constructor(props) {
        super(props);
    
        this.state = {
            loggedIn: false,
            redirect: false,
            playlist: ""
        }
        this.redirectBack = this.redirectBack.bind(this)
        this.generateCard = this.generateCard.bind(this)
    }
    redirectBack() {
        this.setState({redirect: true})
    }
    generateCard(info) {

        return <article class="card">
        <header class="card-header">
          <h2><a rel="noopener noreferrer" target="_blank" href={info[3]}>{info[0]}</a></h2>
          <div class="author-name">
              {info[1]}
          </div>
        </header>
        <div class="card-author">
          <a class="author-avatar" href="" target="_blank">
            <img src={info[2]}/>
          </a>
        </div>
        
      </article>
      
        
    }
    render() {
      try{
        const redirectCheck = this.state.redirect;
        const playlistLink = this.props.location.state.playlistLink;
        const cardInfo = this.props.location.state.cardInfo;
        const loginCheck = this.props.location.state.loggedIn;

        return <div className="preview">
        <div id="logo">Tune-in <i className="tim-icons icon-sound-wave"/></div>
        {loginCheck ? null : <Redirect to={{pathname:'/',state : {}}}/>}

        {redirectCheck ? <Redirect to={{pathname:'/', state : {}}}/> : null}

        <h1 className="previewHeader">Playlist Preview</h1> 

        <section class="card-list">
            {cardInfo.map((card) => this.generateCard(card))}
        </section>
        
        <h1> Playlist Link: <a href={playlistLink}> {playlistLink}</a></h1>
        
        

          <footer><p>Created by:   
              <a className="credit" rel="noopener noreferrer" target="_blank" href="https://www.linkedin.com/in/david-bao/">David Bao</a>,
              <a className="credit" rel="noopener noreferrer" target="_blank" href="https://www.linkedin.com/in/drakewong/">Drake Wong</a>,
              <a className="credit" rel="noopener noreferrer" target="_blank" href="https://www.linkedin.com/in/vincent-ngo/">Vincent Ngo</a>,
              <a className="credit" rel="noopener noreferrer" target="_blank" href="https://www.linkedin.com/in/youngcai/">Young Cai</a></p>
              <p>© 2020 Panoramic Partners, LLC </p>
            </footer>
            <div><Button className="btn-round ml-auto" size="lg" color="warning" onClick={()=>this.redirectBack()}>
          Create, join, or find another party! 
          </Button> </div>

        </div>
      }
        catch(err) {
          return <Redirect to={{pathname:'/',state : {}}}/>;
        }
    }
}


