from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types

import six

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