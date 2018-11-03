import React from 'react';
import { StyleSheet, View } from 'react-native';

import { ENDPOINT_BASE } from './constants.js';
import Playlist from './Playlist.js';

export default class App extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      playlist: [],
    };
  }

  render() {
    return (
      <View style={styles.container}>
        <View style={styles.header}></View>
        <Playlist styles={styles.playlist} playlist={this.state.playlist}/>
      </View>
    );
  }

  componentDidMount() {
    let mood = "happy";
    this.fetchPlaylist(mood);
  }

  async fetchPlaylist(mood) {
    const response = await fetch(`${ENDPOINT_BASE}/mock/playlists/${mood}`);
    const playlist = await response.json();
    this.setState({ playlist });
  }
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#fff',
  },
  header: {
    height: 60,
    backgroundColor: 'gray',
  },
  playlist: {
    flex: 1,
  },
});
