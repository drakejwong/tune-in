import React, { Component } from 'react';
import axios from "axios";
import {
  Button,
} from "reactstrap";

export default class Dashboard extends Component {
  constructor(props) {
    super(props);
  
  this.state = {
    loggedIn: "FALSE",
    

    joinPartyInput: '',
    joinPartySubmit: '',

    findPartyInput: '',
    findPartySubmit: '',

    createPartyResult: '',

    playlistLink: ''
  }
  

  this.handleJoinPartySubmit = this.handleJoinPartySubmit.bind(this);
  this.handleJoinPartyChange = this.handleJoinPartyChange.bind(this);
  
  this.handleFindPartySubmit = this.handleFindPartySubmit.bind(this);
  this.handleFindPartyChange = this.handleFindPartyChange.bind(this);


  this.handleCreateTheParty = this.handleCreateTheParty.bind(this);
  this.handleJoinTheParty = this.handleJoinTheParty.bind(this);
  this.handleFindTheParty = this.handleFindTheParty.bind(this);
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
    axios.get('/api/create').then(res => {
      this.setState({createPartyResult: res.data});
    });
  }
  //impressive-armadillo-of-imagination
  handleJoinTheParty() {
    if (this.state.joinPartyInput !== '') {
      this.setState({joinPartySubmit: this.state.joinPartyInput})
      let postObj = {partyNameToJoin: this.state.joinPartyInput};
      axios.post('/api/join', postObj).then( 
        (response) => { 
            var result = response.data; 
            console.log(result);
        }
    ).catch((error) => {
      console.log(error);
    });; 
      } 
  }

  handleFindTheParty(){
    if (this.state.findPartyInput !== '') {
      this.setState({findPartySubmit: this.state.findPartyInput})
      let postObj = {partyNameToFind: this.state.findPartyInput};
      axios.post('/api/find', postObj).then( 
        (response) => { 
            var result = response.data; 
            console.log(result);
            this.setState({playlistLink: result})
        }
    ).catch((error) => {
      console.log(error);
    });; 
      } 
  }

  render() {
    return (
      <div>
        <div>
          <h1>Dashboard</h1>
          <h1>Welcome {this.props.location.state.userID}, we have been expecting you.</h1>
          <h1>Log-In Status: {this.props.location.state.loggedIn}</h1><br/>

          <h1>Create Party</h1>
          <Button className="btn-round ml-auto" color="success" onClick={()=>this.handleCreateTheParty()}>
              <i className="tim-icons icon-single-02" /> Create your party now!
          </Button>
                
          <h1>Party Name Created: {this.state.createPartyResult}</h1>
          <h1>remember to make the bottom thing only show up after they press the button.</h1>
          <h2>Share this link to your friends now and tell them to paste the party name into the "Join Party" field. Then, have them press the "Join Party" button, so they can join your party!</h2>
          
          <label for="joinParty">Join Party</label><br/>
        
          <input name="partyToJoin" id="partyToJoin" value={this.state.joinPartyInput} onChange={this.handleJoinPartyChange} /> 
          <Button className="btn-round ml-auto" color="success" onClick={()=>this.handleJoinTheParty()}>
            <i className="tim-icons icon-single-02" /> Join Party!
          </Button>
        
          <h1>Party Name Joined: {this.state.joinPartySubmit}</h1>

          <label for="findParty">Get Your Party's Playlist!</label><br/>
  
          <h1>Type in your party's name and hit the button to get your new playlist!</h1>
          <input name="partyToFind" id="partyToFind" value={this.state.findPartyInput} onChange={this.handleFindPartyChange} />
          <Button className="btn-round ml-auto" color="success" onClick={()=>this.handleFindTheParty()}>
            <i className="tim-icons icon-single-02" /> Find Your Party's Playlist!
          </Button> 
          
          <h1>Party Name Found! Here is your party's playlist: {this.state.playlistLink}</h1>
        </div>
      </div>
    );
  }
}

