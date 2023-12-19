import re
import string
import nltk
nltk.download('stopwords')
nltk.download('wordnet')
from nltk.corpus import stopwords
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import PyPDFLoader
import pandas as pd


def clean_text(text):
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

def pdf_preprocessing(file):
    loader =  PyPDFLoader(file)
    pages = loader.load_and_split()
    text_splitter = RecursiveCharacterTextSplitter(separator="\n", chunk_size=200, chunk_overlap=50, length_function=len)
    texts = text_splitter.split_documents(pages)
    final_texts = ""
    for text in texts:
        final_texts = final_texts + text.page_content

    return clean_text(final_texts)

def csv_preprocessing(filepath):
    result = {}
    for chunk in pd.read_csv(filepath, encoding='utf-8', chunksize=200):
        grouped_data = chunk.groupby('doc_name')['text'].agg(list).reset_index()
        pdf_dict = dict(zip(grouped_data['doc_name'], grouped_data['text']))
        for key in pdf_dict:
            if key in result:
                result[key] += clean_text(" ".join([str(x) for x in pdf_dict[key]]))
            else:
                result[key] = clean_text(" ".join([str(x) for x in pdf_dict[key]]))
    return result
