import React from 'react';
import { StyleSheet, View } from 'react-native';

import MoodPickerTab from './MoodPickerTab.js';

const TABS = {
  MOOD_PICKER: 'mood-picker',
};

export default class App extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      tab: TABS.MOOD_PICKER,
    };
  }

  renderTabView() {
    switch (this.state.tab) {
      case TABS.MOOD_PICKER: return <MoodPickerTab/>;
    }
  }

  render() {
    return (
      <View style={styles.container}>
        <View style={styles.header}></View>
        {this.renderTabView()}
      </View>
    );
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
});
