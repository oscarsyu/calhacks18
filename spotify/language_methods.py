from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types

import six

import sys

from thesaurus import Word

def mood_dict():
    """ Gives a dictionary of mood synonyms. """
    happy_synonyms = Word("happy").synonyms() + ["happy"]
    sad_synonyms = Word("sad").synonyms() + ["sad"]
    excited_synonyms = Word("excited").synonyms() + ["excited"]
    calm_synonyms = Word("calm").synonyms() + ["calm"]
    moods = {
        "happy" : happy_synonyms,
        "sad" : sad_synonyms,
        "excited" : excited_synonyms,
        "calm" : calm_synonyms
    }
    return moods

def mood_checker(text):
	"""Detects syntax in the text. """
	moods = mood_dict()
	client = language.LanguageServiceClient()
	if isinstance(text, six.binary_type):
		text = text.decode('utf-8')
	document = types.Document(
    	content=text,
    	type=enums.Document.Type.PLAIN_TEXT)
	tokens = client.analyze_syntax(document).tokens
	tokens = [t.text.content for t in tokens] 
	for token in tokens:
		for mood in moods.keys():
			if token in moods[mood]:
				return mood;

def sample_analyze_sentiment(content):

    client = language.LanguageServiceClient()

    # content = 'Your text to analyze, e.g. Hello, world!'

    if isinstance(content, six.binary_type):
        content = content.decode('utf-8')

    type_ = enums.Document.Type.PLAIN_TEXT
    document = {'type': type_, 'content': content}

    response = client.analyze_sentiment(document)
    sentiment = response.document_sentiment
    print('Score: {}'.format(sentiment.score))
    print('Magnitude: {}'.format(sentiment.magnitude))

def entity_sentiment_text(text):
    """Detects entity sentiment in the provided text."""
    client = language.LanguageServiceClient()

    if isinstance(text, six.binary_type):
        text = text.decode('utf-8')

    document = types.Document(
        content=text.encode('utf-8'),
        type=enums.Document.Type.PLAIN_TEXT)

    # Detect and send native Python encoding to receive correct word offsets.
    encoding = enums.EncodingType.UTF32
    if sys.maxunicode == 65535:
        encoding = enums.EncodingType.UTF16

    result = client.analyze_entity_sentiment(document, encoding)

    for entity in result.entities:
        print('Mentions: ')
        print(u'Name: "{}"'.format(entity.name))
        for mention in entity.mentions:
            print(u'  Begin Offset : {}'.format(mention.text.begin_offset))
            print(u'  Content : {}'.format(mention.text.content))
            print(u'  Magnitude : {}'.format(mention.sentiment.magnitude))
            print(u'  Sentiment : {}'.format(mention.sentiment.score))
            print(u'  Type : {}'.format(mention.type))
        print(u'Salience: {}'.format(entity.salience))
        print(u'Sentiment: {}\n'.format(entity.sentiment))


def main():
	entity_sentiment_text("sad in the feels R&B")


if __name__ == '__main__': main()