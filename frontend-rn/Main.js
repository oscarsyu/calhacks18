import React from 'react';
import { StyleSheet, View, WebView } from 'react-native';
import { connect } from 'react-redux';

import { ENDPOINT_BASE } from './constants.js';
import { setUser } from './reducer.js';
import MoodPickerTab from './MoodPickerTab.js';

const TABS = {
    MOOD_PICKER: 'mood-picker',
};

class Main extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            tab: TABS.MOOD_PICKER,
        };
    }

    renderTabView() {
        switch (this.state.tab) {
            case TABS.MOOD_PICKER: return <MoodPickerTab />;
        }
    }

    renderAuthView() {
        const webViewProps = {
            ref: 'webview',
            onMessage: (event) => {
                this.props.setUser(event.nativeEvent.data);
            },
            javaScriptEnabled: true,
            source: {
                uri: `${ENDPOINT_BASE}/spotify/auth`,
            }
        }

        return <WebView {...webViewProps} style={{ flex: 1 }} />;
    }

    renderInvisibleLogoutView() {
        const webViewProps = {
            source: {
                uri: `${ENDPOINT_BASE}/spotify/logout`,
            }
        }

        return <WebView {...webViewProps} style={{ width: 0, height: 0, flex: 0 }} />;
    }

    render() {
        return (
            <View style={styles.container}>
                <View style={styles.header}></View>
                {this.props.userId ? this.renderTabView() : null}
                {this.props.userId ? this.renderInvisibleLogoutView() : this.renderAuthView()}
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

const mapStateToProps = (state) => {
    return {
        userId: state.userId
    };
};

const mapDispatchToProps = (dispatch) => {
    return {
        setUser(userId) {
            dispatch(setUser(userId));
        }
    };
};

export default connect(mapStateToProps, mapDispatchToProps)(Main);
