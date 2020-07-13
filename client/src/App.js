import React, { Component } from 'react';
import './App.css';
import SpotifyWebApi from "spotify-web-api-js";
import TopBar from './components/TopBar';
import LoginButton from './components/loginButton';

import {
  Row,
  Col,
  Container
} from "reactstrap";

const spot = new SpotifyWebApi();


class App extends Component {
  constructor(){
    super();
    const params = this.getHashParams();
    const token = params.access_token;
    if (token) {
      spot.setAccessToken(token);
    }
    this.state = {
      loggedIn: token ? true : false,
      topTracks: [],
      topArtists: [],
      user_id: ""
    }
  }

  getHashParams() {
    var hashParams = {};
    var e, r = /([^&;=]+)=?([^&;]*)/g,
        q = window.location.hash.substring(1);
    e = r.exec(q)
    while (e) {
       hashParams[e[1]] = decodeURIComponent(e[2]);
       e = r.exec(q);
    }
    return hashParams;
  }

  getTops() {
    spot.getMe()
      .then((user) => {
        this.setState({
          user_id: user.id
        });
      })
    spot.getMyTopTracks({
      limit: 50,
      time_range: "short_term"
    })
      .then((response) => {
        this.setState({
          topTracks: response.items
        });
      })
    console.log(this.state)
    spot.getMyTopArtists({
      limit: 50,
      time_range: "short_term"
    })
      .then((response) => {
        this.setState({
          topArtists: response.items
        });
      })
    console.log(this.state)
  }

  renderTracksTableData() {
    var rank = 0;
    return this.state.topTracks.map((track) => {
       rank++;
       const name = track.name;
       const artists = track.artists.map((x) => x.name).join(", ");
       const preview = track.preview_url;
       return (
          <tr key={name}>
             <td>{rank}</td>
             <td>{name}</td>
             <td>{artists}</td>
             <td><a href={preview}> Click to listen </a></td>
          </tr>
       )
    })
  }
//TODO: get album art
  renderTableHeader() {
    // let header = Object.keys(this.state.topTracks[0]);
    let header = ["Rank", "Name", "Artist(s)", "Preview"];
    return header.map((key) => {
       return <th key={key}>{key.toUpperCase()}</th>
    })
  }

  renderTrackTable() {
    this.getTops();
    return (
      <div>
         <h1 id='title'>Top Tracks</h1>
         <table id='tracks'>
            <tbody>
               <tr> {this.renderTracksTableHeader()} </tr>
               {this.renderTracksTableData()}
            </tbody>
         </table>
      </div>
   )
  }

  renderArtistsTableData() {
    var rank = 0;
    return this.state.topArtists.map((artist) => {
       const name = artist.name;
       rank++
       return (
          <tr key={name}>
             <td>{rank}</td>
             <td>{name}</td>
          </tr>
       )
    })
  }

  renderArtistsTableHeader() {
    let header = ["Rank", "Name"];
    return header.map((key) => {
       return <th key={key}>{key.toUpperCase()}</th>
    })
  }

  renderArtistTable() {
    // this.getTops();
    return (
      <div>
         <h1 id='title'>Artists</h1>
         <table id='tracks'>
            <tbody>
               <tr> {this.renderArtistsTableHeader()} </tr>
               {this.renderArtistsTableData()}
            </tbody>
         </table>
      </div>
   )
  }

  render() {
    return (
      <div>
        <TopBar />

        <div className="App">
          <div>
            { !this.state.loggedIn &&
              <div>
                <h1>Do you even know a brother?</h1>
                <Container>
                  <Row className="justify-content-md-center">
                    <Col lg="6">
                      <p>What the fuck did you just fucking say about me, you little bitch? I'll have you know I graduated top of my class in the Navy Seals, and I've been involved in numerous secret raids on Al-Quaeda, and I have over 300 confirmed kills. I am trained in gorilla warfare and I'm the top sniper in the entire US armed forces. You are nothing to me but just another target. I will wipe you the fuck out with precision the likes of which has never been seen before on this Earth, mark my fucking words. You think you can get away with saying that shit to me over the Internet? Think again, fucker. As we speak I am contacting my secret network of spies across the USA and your IP is being traced right now so you better prepare for the storm, maggot. The storm that wipes out the pathetic little thing you call your life. You're fucking dead, kid. I can be anywhere, anytime, and I can kill you in over seven hundred ways, and that's just with my bare hands. Not only am I extensively trained in unarmed combat, but I have access to the entire arsenal of the United States Marine Corps and I will use it to its full extent to wipe your miserable ass off the face of the continent, you little shit. If only you could have known what unholy retribution your little "clever" comment was about to bring down upon you, maybe you would have held your fucking tongue. But you couldn't, you didn't, and now you're paying the price, you goddamn idiot. I will shit fury all over you and you will drown in it. You're fucking dead, kiddo.</p>
                    </Col>
                  </Row>
                </Container>
                <br />
                <a href='http://localhost:8888' > <LoginButton msg="Log In To Spotify Now, CMON!!!!"/> </a>
              </div>
            }
          </div>
          <div>
            { this.state.loggedIn &&
              <div>
                { this.renderTrackTable() }
              </div>
            }
          </div>
          <div>
            { this.state.loggedIn &&
              <div>
                { this.renderArtistTable() }
              </div>
            }
          </div>
        </div>
      </div>
    );
  }
}

export default App;
