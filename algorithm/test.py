# Imports the Google Cloud client library

from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types
import pickle
import pandas as pd
# Instantiates a client
client = language.LanguageServiceClient()

# The text to analyze
text = u'I am feeling super duper duper happy!! Lets party'
# u'I am feeling very very extremely sad.  I just want to cry'
text1 = u'I am feeling super duper duper happy!! Lets party'
document = types.Document(
    content=text,
    type=enums.Document.Type.PLAIN_TEXT)

# Detects the sentiment of the text
sentiment = client.analyze_sentiment(document=document).document_sentiment

print('Text: {}'.format(text))
print('Sentiment: {}, {}'.format(sentiment.score, sentiment.magnitude))

mood_score = sentiment.score * 1.5
print(mood_score)

with open('lm.pickle', 'rb') as fi:
    lm = pickle.load(fi)
data = pd.read_csv("test_set.csv")

def predict_songs(tbl):
    tbl_predicted = tbl
    predicted = lm.predict(tbl.loc[:, ["bpm", "nrgy", "dnce", "dB", "val", "dur", "acous"]])
    tbl_predicted["mood_predicted"] = predicted
    return tbl_predicted
test_norm = predict_songs(data)

def find_predicted_songs(tbl, score, num_songs):
    in_range = tbl

    in_range["dists"] = abs(in_range["mood_predicted"] - score)
    sort_by_dist = in_range.sort_values("dists")

    return sort_by_dist[:num_songs]
playlist = find_predicted_songs(test_norm, mood_score, 25)
print(playlist)
