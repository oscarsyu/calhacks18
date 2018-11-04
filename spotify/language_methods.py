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

def main():


if __name__ == '__main__': main()