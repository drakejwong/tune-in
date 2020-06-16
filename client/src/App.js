import React, { Component } from 'react';
import './App.css';
import SpotifyWebApi from "spotify-web-api-js";
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
      topTracks: []
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

  getTopTracks() {
    spot.getMyTopTracks()
      .then((response) => {
        this.setState({
          topTracks: response.items
        });
      })
    console.log(this.state)
  }

  namesOfTopTracks() {
    if (this.state.topTracks.length === 0) {
      this.getTopTracks();
    }
    var ret = [];
    this.state.topTracks.forEach(t => ret.push(t.name));
    return ret.join("\n");
  }

  renderTableData() {
    return this.state.topTracks.map((track) => {
       const name = track.name;
       const artists = track.artists.map((x) => x.name).join(", ");
       return (
          <tr key={name}>
             <td>{name}</td>
             <td>{artists}</td>
          </tr>
       )
    })
  }

  renderTableHeader() {
    // let header = Object.keys(this.state.topTracks[0]);
    let header = ["Name", "Artist(s)"];
    return header.map((key) => {
       return <th key={key}>{key.toUpperCase()}</th>
    })
  }

  renderTrackTable() {
    this.getTopTracks();
    return (
      <div>
         <h1 id='title'>Top Tracks</h1>
         <table id='tracks'>
            <tbody>
               <tr> {this.renderTableHeader()} </tr>
               {this.renderTableData()}
            </tbody>
         </table>
      </div>
   )
  }

  render() {
    return (
      <div className="App">
        <div>
          { !this.state.loggedIn &&
            <a href='http://localhost:8888' > Login to Spotify </a>
          }
        </div>
        <div>
          { this.state.loggedIn &&
            <div>
              { this.renderTrackTable() }
            </div>
          }
        </div>
      </div>
    );
  }
}

export default App;
