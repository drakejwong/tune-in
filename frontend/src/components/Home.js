import React, { Component } from 'react';
import './App.css';
import LoginButton from './LoginButton';

export default class Home extends Component {
  constructor(props) {
    super(props);
  
  this.state = {
    loggedIn: false,
    user_id: ""
  }
}
  render() {
    return (
      <div>
        <div className="App">
          <div id="logo">Tune-in <i className="tim-icons icon-sound-wave"/></div>
          <div>
              <div>
                <h1 class="welcome">Welcome to Tune-in!</h1>
                <h2 class="desc">Create playlists with songs based on you and your friends' favorite songs! </h2>
                <h3 class="explanation">To get started, log into your Spotify account! We use a special algorithm to make sure you and your friends' taste in music is represented in the generated playlist. </h3>
                <div class="login"> <LoginButton location={this.props.location} msg="Log into Spotify!!"/> </div>
              </div>
            <footer><p>Created by:   
              <a className="credit" rel="noopener noreferrer" target="_blank" href="https://www.linkedin.com/in/david-bao/">David Bao</a>,
              <a className="credit" rel="noopener noreferrer" target="_blank" href="https://www.linkedin.com/in/drakewong/">Drake Wong</a>,
              <a className="credit" rel="noopener noreferrer" target="_blank" href="https://www.linkedin.com/in/vincent-ngo/">Vincent Ngo</a>,
              <a className="credit" rel="noopener noreferrer" target="_blank" href="https://www.linkedin.com/in/youngcai/">Young Cai</a></p>
              <p>© 2020 Panoramic Partners, LLC </p>
            </footer>
          </div>
        </div>
      </div>
    )
  }
} 

/*<p>What the fuck did you just fucking say about me, you little bitch? I'll have you know I graduated top of my class in the Navy Seals, and I've been involved in numerous secret raids on Al-Quaeda, and I have over 300 confirmed kills. I am trained in gorilla warfare and I'm the top sniper in the entire US armed forces. You are nothing to me but just another target. I will wipe you the fuck out with precision the likes of which has never been seen before on this Earth, mark my fucking words. You think you can get away with saying that shit to me over the Internet? Think again, fucker. As we speak I am contacting my secret network of spies across the USA and your IP is being traced right now so you better prepare for the storm, maggot. The storm that wipes out the pathetic little thing you call your life. You're fucking dead, kid. I can be anywhere, anytime, and I can kill you in over seven hundred ways, and that's just with my bare hands. Not only am I extensively trained in unarmed combat, but I have access to the entire arsenal of the United States Marine Corps and I will use it to its full extent to wipe your miserable ass off the face of the continent, you little shit. If only you could have known what unholy retribution your little "clever" comment was about to bring down upon you, maybe you would have held your fucking tongue. But you couldn't, you didn't, and now you're paying the price, you goddamn idiot. I will shit fury all over you and you will drown in it. You're fucking dead, kiddo.</p>
*/