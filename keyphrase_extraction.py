import nltk
import sys

from nltk.corpus import stopwords

stopwords = stopwords.words('english')

lemmatizer = nltk.WordNetLemmatizer()
stemmer = nltk.stem.porter.PorterStemmer()
grammar = r"""
    NBAR:
        {<NN.*|JJ>*<NN.*>}  # Nouns and Adjectives, terminated with Nouns
        
    NP:
        {<NBAR>}
        {<NBAR><IN><NBAR>}  # Above, connected with in/of/etc...
"""

def start(text):
    # enter whatever text needed
    #text = """Alcohol is a problem in life. Beer is love."""

    """
    Handle verbose regexps, abbreviations, words with hyphens, currency, percentages, ellipsis, separate tokens
    """
    sentence_re = r'(?:(?:[A-Z])(?:.[A-Z])+.?)|(?:\w+(?:-\w+)*)|(?:\$?\d+(?:.\d+)?%?)|(?:...|)(?:[][.,;"\'?():-_`])'

    keywords = []
    chunker = nltk.RegexpParser(grammar)
    toks = nltk.regexp_tokenize(text, sentence_re)
    postoks = nltk.tag.pos_tag(toks)
    tree = chunker.parse(postoks)
    terms = get_terms(tree)

    for term in terms:
        for word in term:
            if word.isalpha():
                keywords.append(word)
    return keywords

def leaves(tree):
    """Finds NP (nounphrase) leaf nodes of a chunk tree."""
    for subtree in tree.subtrees(filter = lambda t: t.label()=='NP'):
        yield subtree.leaves()

def normalise(word):
    """Normalises words to lowercase and stems and lemmatizes it."""
    word = word.lower()
    word = stemmer.stem(word)
    word = lemmatizer.lemmatize(word)
    return word

def acceptable_word(word):
    """Checks conditions for acceptable word: length, stopword."""
    accepted = bool(2 <= len(word) <= 40
        and word.lower() not in stopwords)
    return accepted


def get_terms(tree):
    for leaf in leaves(tree):
        term = [normalise(w) for w,t in leaf if acceptable_word(w)]
        yield term

def simulate_problems():
    problem_list = ['I cannot control myself once I start drinking.', 
                    'I cannot complete a day without 2 bottles of vodka.',
                    'I get wasted every other day.',
                    'I feel like alcohol is taken over my life.',
                    'I cannot imagine my life without scotch.',
                    'I spend all my money on booze.',
                    'My wife will leave me if I don\'t give up drinking.',
                    'I drink a lot.',
                    'I try to quit drinking but my friends won\'t let me.',
                    'I am alone because of my drinking habits.',
                    'I lost my friends due to my alcohol addiction.',
                    'My health has gone down because I drink too much.',
                    'I might have liver problems because of my drinking habit.',
                    'I just want to open up to someone about my booze addiction.',
                    'I don\'t understand why people have a problem with my drinking.',
                    'I drink more whiskey than I do water.'
                    ]
    for sent in problem_list:
        print sent, start(str(sent.split()))
        print

if __name__ == '__main__':
    simulate_problems()
    