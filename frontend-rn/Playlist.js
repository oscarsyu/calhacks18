import React from 'react';
import { FlatList, StyleSheet, Text, View } from 'react-native';

export default class Playlist extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            items: [],
        };
    }

    render() {
        return (
            <FlatList
                data={this.state.items}
                renderItem={({ item }) =>
                    <View style={styles.item}>
                        <Text>{item.key}</Text>
                    </View>
                }
            />
        );
    }

    componentWillReceiveProps(nextProps) {
        this.updatePlaylist(nextProps.playlist);
    }

    componentDidMount() {
        this.updatePlaylist(this.props.playlist);
    }

    updatePlaylist(playlist) {
        this.setState({
            items: playlist.map((song) => {
                return {
                    key: song
                };
            }),
        });
    }
}

const styles = StyleSheet.create({
    item: {
        height: 40,
        flexDirection: 'row',
        alignItems: 'center',
        borderTopColor: 'lightgray',
        borderTopWidth: 1,
    },
});
