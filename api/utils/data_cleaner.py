import re
import string
import nltk
nltk.download('stopwords')
nltk.download('wordnet')
from nltk.corpus import stopwords

def clean_text(text):
    '''
    Input: text
    Output: cleaned text
    '''
    # preprocess the text
    text = text.lower()
    text = re.sub(r'[^\w\s\d]', '', text)
    text = text.translate(str.maketrans('', '', string.punctuation))
    text = ' '.join(text.split())

    stop_words = set(stopwords.words('english'))
    lemmatizer = nltk.stem.WordNetLemmatizer()
    
    # tokenize the text
    tokens = nltk.word_tokenize(text)

    # remove stopwords and lemmatize
    tokens = [w for w in tokens if not w in stop_words]
    tokens = [lemmatizer.lemmatize(w) for w in tokens]
    return ' '.join(tokens)