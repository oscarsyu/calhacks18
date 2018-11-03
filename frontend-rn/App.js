import React from 'react';
import { StyleSheet, Text, View } from 'react-native';

import { ENDPOINT_BASE } from './constants.js';

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
        <Text>{this.state.playlist.join("\n")}</Text>
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
    this.setState((state) => {
      return {
        ...state,
        playlist
      };
    });
  }
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#fff',
    alignItems: 'center',
    justifyContent: 'center',
  },
});
