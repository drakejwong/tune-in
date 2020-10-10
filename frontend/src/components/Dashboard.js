import React, { Component } from 'react';
import axios from "axios";
import './Dashboard.css';
import { Redirect } from 'react-router';
import {
  Button,
} from "reactstrap";

export default class Dashboard extends Component {
  constructor(props) {
    super(props);
  
  this.state = {
    loggedIn: false,
    loadingCreate: false,
    loadingJoin: false,
    loadingFind: false,

    joinPartySuccess: false,
    createPartySuccess: false,
    findPartySuccess: false,

    joinPartyInput: '',
    joinPartySubmit: '',
    joinPartyResponse: '',

    findPartyInput: '',
    findPartySubmit: '',

    createPartyResult: '',

    findPartyResponse: '',
    playlistLink: '',
    cardInfo: '',


  }
  this.showLoadingCreate = this.showLoadingCreate.bind(this);
  this.hideLoadingCreate = this.hideLoadingCreate.bind(this);

  this.showLoadingJoin = this.showLoadingJoin.bind(this);
  this.hideLoadingJoin = this.hideLoadingJoin.bind(this);

  this.showLoadingFind = this.showLoadingFind.bind(this);
  this.hideLoadingFind = this.hideLoadingFind.bind(this);

  this.handleJoinPartySubmit = this.handleJoinPartySubmit.bind(this);
  this.handleJoinPartyChange = this.handleJoinPartyChange.bind(this);
  
  this.handleFindPartySubmit = this.handleFindPartySubmit.bind(this);
  this.handleFindPartyChange = this.handleFindPartyChange.bind(this);


  this.handleCreateTheParty = this.handleCreateTheParty.bind(this);
  this.handleJoinTheParty = this.handleJoinTheParty.bind(this);
  this.handleFindTheParty = this.handleFindTheParty.bind(this);
}
  showLoadingCreate() {
    this.setState({loadingCreate: true});
  }
  hideLoadingCreate() {
    setTimeout(()=> {this.setState({loadingCreate: false});}, 2000)
  }

  showLoadingJoin() {
    this.setState({loadingJoin: true});
  }
  hideLoadingJoin() {
    setTimeout(()=> {this.setState({loadingJoin: false});}, 2000)
  }

  showLoadingFind() {
    this.setState({loadingFind: true});
  }
  hideLoadingFind() {
    setTimeout(()=> {this.setState({loadingFind: false});}, 2000)
  }

  handleJoinPartyChange(event) {
    this.setState({joinPartyInput: event.target.value});
  }

  handleJoinPartySubmit(event) {
    event.preventDefault()
    this.setState({joinPartySubmit: this.state.joinPartyInput})
  }

  handleFindPartyChange(event) {
    this.setState({findPartyInput: event.target.value});
  }

  handleFindPartySubmit(event) {
    event.preventDefault()
    this.setState({findPartySubmit: this.state.findPartyInput})
  }

  handleCreateTheParty() {
    this.showLoadingCreate();
    axios.get('/api/create').then(res => {
      this.setState({createPartyResult: res.data});
      this.hideLoadingCreate();
      setTimeout(()=> {this.setState({createPartySuccess: true});}, 2000);
    });
    
  }
  //impressive-armadillo-of-imagination
  handleJoinTheParty() {
    if (this.state.joinPartyInput !== '') {
      this.showLoadingJoin();
      this.setState({joinPartySubmit: this.state.joinPartyInput})
      let postObj = {partyNameToJoin: this.state.joinPartyInput};
      axios.post('/api/join', postObj).then( 
        (response) => { 
            var result = response.data; 
            //console.log(result);
            this.setState({joinPartyResponse: result})
            this.hideLoadingJoin();
            setTimeout(()=> {this.setState({joinPartySuccess: true});}, 2000);
        }
    ).catch((error) => {
      console.log(error);
    });; 
      } 
  }

  handleFindTheParty(){
    if (this.state.findPartyInput !== '') {
      this.showLoadingFind();
      this.setState({findPartySubmit: this.state.findPartyInput})
      let postObj = {partyNameToFind: this.state.findPartyInput};
      axios.post('/api/find', postObj).then( 
        (response) => { 
            var result = response.data; 
            //console.log(result);
            if (typeof result === 'string'){
              this.setState({findPartyResponse: result});
            } else {
              this.setState({playlistLink: result.playlistLink, cardInfo: result.cardInfo})
            }
            
            this.hideLoadingFind();
            setTimeout(()=> {this.setState({findPartySuccess: true});}, 2000);
        }
    ).catch((error) => {
      console.log(error);
    });; 
      } 
  }

  render() {
    try{
      const loginCheck = this.props.location.state.loggedIn;
      const loadingCreateCheck = this.state.loadingCreate;
      const loadingJoinCheck = this.state.loadingJoin;
      const loadingFindCheck = this.state.loadingFind;
      const createdPartySuccessfully = this.state.createPartySuccess;
      const joinedPartySuccessfully = this.state.joinPartySuccess;
      const foundPartySuccessfully = this.state.findPartySuccess;
      return (
        <div >
          <div className="dashboard">
            <div id="logo">Tune-in <i className="tim-icons icon-sound-wave"/></div>
            {loginCheck ? <span><h1>Welcome, {this.props.location.state.userID}. Your new music awaits.</h1></span> : <Redirect to={{pathname:'/',state : {}}}/>}
            
            
            <blockquote className="blockquote text-center">
            <h3>You can create your own party and invite people, or you can type in your friend's party name to join theirs!</h3> 

            <Button className="btn-round ml-auto" size="lg" color="default" onClick={()=>this.handleCreateTheParty()}>
            {!loadingCreateCheck ? <span><i className="tim-icons icon-single-02" /> Create a Party! </span> : <span><i className="fa fa-refresh fa-spin"/> Creating party...</span>}
            </Button>
          
            <input name="partyToJoin" id="partyToJoin" placeholder="Party name to join"value={this.state.joinPartyInput} onChange={this.handleJoinPartyChange} /> 
            <Button className="btn-round ml-auto" size = "lg" color="primary" onClick={()=>this.handleJoinTheParty()}>
            {!loadingJoinCheck ? <span><i className="tim-icons icon-simple-add" /> Join a Party!</span> : <span><i className="fa fa-refresh fa-spin"/> Joining party...</span>}
            </Button>
            </blockquote>
            {createdPartySuccessfully ? <span><h2>Party Name: {this.state.createPartyResult}</h2>
            <h2>Share this link and party name to your friends now!</h2> </span> : null}

            {joinedPartySuccessfully ? <span><h1>{this.state.joinPartyResponse}</h1></span> : null}
            
            <blockquote className="blockquote text-center"> 
            <h3>Once your party is ready to generate a playlist, type in your party's name and hit the button to get your new playlist!</h3>
            <input name="partyToFind" id="partyToFind" placeholder = "Party name to find" value={this.state.findPartyInput} onChange={this.handleFindPartyChange} />
            <Button className="btn-round ml-auto" size="lg" color="warning" onClick={()=>this.handleFindTheParty()}>
            {!loadingFindCheck ? <span><i className="tim-icons icon-headphones"/> Find Your Party's Playlist!</span> : <span><i className="fa fa-refresh fa-spin"/> Finding party...</span>} 
            </Button> 
            </blockquote>
            {foundPartySuccessfully ? <Redirect to={
                  {pathname:'/preview',
              state : {playlist:this.state.findPartyResponse, playlistLink:this.state.playlistLink, cardInfo:this.state.cardInfo, loggedIn: true}
          }
              }/> : <span><h1>{this.state.findPartyResponse}</h1></span>}

            <footer><p>Created by:   
                <a className="credit" rel="noopener noreferrer" target="_blank" href="https://www.linkedin.com/in/david-bao/">David Bao</a>,
                <a className="credit" rel="noopener noreferrer" target="_blank" href="https://www.linkedin.com/in/drakewong/">Drake Wong</a>,
                <a className="credit" rel="noopener noreferrer" target="_blank" href="https://www.linkedin.com/in/vincent-ngo/">Vincent Ngo</a>,
                <a className="credit" rel="noopener noreferrer" target="_blank" href="https://www.linkedin.com/in/youngcai/">Young Cai</a></p>
                <p>© 2020 Panoramic Partners, LLC </p>
              </footer>
          </div>
        </div>
      );
            }
            catch(err) {
              return <Redirect to={{pathname:'/',state : {}}}/>;
            }
  }
}

/* 

          
          */
/*<h1>Party Name Found! Here is your party's playlist: {this.state.playlistLink}</h1>*/
