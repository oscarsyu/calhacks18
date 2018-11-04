import React from 'react';
import { Picker, StyleSheet, Slider, View } from 'react-native';
import { connect } from 'react-redux';

import { ENDPOINT_BASE } from './constants.js';
import Playlist from './Playlist.js';

class MoodPickerTab extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            mood: 0,
            playlist: [],
        };
    }

    render() {
        return (
            <View style={styles.container}>
                <Slider
                    selectedValue={this.state.mood}
                    minimumValue={-1}
                    maximumValue={1}
                    onValueChange={(value) => {
                        this.setState({ mood: value }, () => this.fetchPlaylist());
                    }}
                    />
                <Playlist styles={styles.playlist} playlist={this.state.playlist} />
            </View>
        );
    }

    componentDidMount() {
        this.fetchPlaylist();
    }

    async fetchPlaylist() {
        this.setState({ playlist: [] }); // Empty the playlist first

        const response = await fetch(`${ENDPOINT_BASE}/playlist/create?mood=${this.state.mood}`, {
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
