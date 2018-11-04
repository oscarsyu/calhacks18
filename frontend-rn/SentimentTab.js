import React from 'react';
import { StyleSheet, TextInput, View } from 'react-native';
import { connect } from 'react-redux';

import { ENDPOINT_BASE } from './constants.js';
import Playlist from './Playlist.js';

class SentimentTab extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            text: '',
            playlist: [],
        };
    }

    render() {
        return (
            <View style={styles.container}>
                <TextInput
                    style={styles.text}
                    multiline={true}
                    numberOfLines={4}
                    value={this.state.text}
                    onChangeText={(text) => {
                        this.setState({ text }, () => this.fetchPlaylist());
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

        const response = await fetch(`${ENDPOINT_BASE}/playlist/create/text?text=${this.state.text}`, {
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
    text: {
        height: 96,
        padding: 16,
        borderBottomWidth: 1,
        borderBottomColor: 'gray',
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

export default connect(mapStateToProps, mapDispatchToProps)(SentimentTab);
