import pickle
import pandas as pd
import numpy as np

with open('app/lm.pickle', 'rb') as fi:
    lm = pickle.load(fi)


def suggest_playlist(all_tracks_with_features, mood):
    data = pd.DataFrame.from_dict(all_tracks_with_features)
    new_labels = {'tempo': 'bpm', 'danceability': 'dnce', 'energy': 'nrgy', 'loudness': 'dB', 'liveliness': 'live',
                  'valence': 'val', 'duration_ms': 'dur', 'acousticness': 'acous'}
    data = data.rename(columns=new_labels)

    def prep_data(frame):
        frame_data = frame
        # zero_bpm = frame_data[frame_data['bpm'] == 0].index[0]
        # frame_data = frame_data.drop([zero_bpm])
        frame_data['dur'] = frame_data['dur'].astype('float')
        return frame_data

    def normalize(col):
        col_range = max(col) - min(col)
        avg = np.mean(col)
        return (col - avg) / col_range

    def prep_features(tbl):
        tbl_norm = tbl
        tbl_norm['bpm'] = normalize(tbl_norm['bpm'])
        tbl_norm['nrgy'] = normalize(tbl_norm['nrgy'] * 100)
        tbl_norm['dnce'] = normalize(tbl_norm['dnce'] * 100)
        tbl_norm['val'] = normalize(tbl_norm['val'] * 100)
        tbl_norm['acous'] = normalize(tbl_norm['acous'] * 100)
        tbl_norm['dur'] = tbl_norm['dur'] / 100000
        return tbl_norm

    data = prep_data(data)
    data = prep_features(data)

    def predict_songs(tbl):
        tbl_predicted = tbl
        predicted = lm.predict(tbl.loc[:, ['bpm', 'nrgy', 'dnce', 'dB', 'val', 'dur', 'acous']])
        tbl_predicted['mood_predicted'] = predicted
        return tbl_predicted

    predicted = predict_songs(data)

    def find_predicted_songs(tbl, score, num_songs):
        songs = num_songs
        if songs > 25:
            songs = 25
        in_range = tbl

        in_range['dists'] = abs(in_range['mood_predicted'] - score)
        sort_by_dist = in_range.sort_values('dists')

        return sort_by_dist[:num_songs]

    return find_predicted_songs(predicted, mood, 25).to_dict(orient='records')
