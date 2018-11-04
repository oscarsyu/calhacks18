import React from 'react';
import { Picker, StyleSheet, View } from 'react-native';
import { connect } from 'react-redux';

import { ENDPOINT_BASE } from './constants.js';
import Playlist from './Playlist.js';

class MoodPickerTab extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            mood: 'happy',
            playlist: [],
        };
    }

    render() {
        return (
            <View style={styles.container}>
                <Picker
                    selectedValue={this.state.mood}
                    onValueChange={(itemValue, itemIndex) => {
                        this.setState({ mood: itemValue }, () => this.fetchPlaylist());
                    }}>
                    <Picker.Item value='happy' label='Happy mood' />
                    <Picker.Item value='sad' label='Sad mood' />
                </Picker>
                <Playlist styles={styles.playlist} playlist={this.state.playlist} />
            </View>
        );
    }

    componentDidMount() {
        this.fetchPlaylist();
    }

    async fetchPlaylist() {
        const response = await fetch(`${ENDPOINT_BASE}/playlist/create`, {
            headers: {
                'Authorization': this.props.userId,
            },
        });
        const playlist = await response.json();
        this.setState({ playlist });
    }
}

const styles = StyleSheet.create({
    container: {
        flex: 1,
    },
    playlist: {
        flex: 1,
    },
});

const mapStateToProps = (state) => {
    return {
        userId: state.userId
    };
};

const mapDispatchToProps = (dispatch) => {
    return {};
};

export default connect(mapStateToProps, mapDispatchToProps)(MoodPickerTab);
