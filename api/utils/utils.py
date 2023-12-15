from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import PyPDFLoader, DirectoryLoader
import pandas as pd
from transformers import pipeline, T5Tokenizer, T5ForConditionalGeneration, AutoTokenizer
import torch


#model and tokenizer loading
model = "MBZUAI/LaMini-Flan-T5-248M"
tokenizer = AutoTokenizer.from_pretrained(model)
base_model = T5ForConditionalGeneration.from_pretrained(model, device_map='auto', torch_dtype=torch.float32)

def pdf_preprocessing(file):
    loader =  PyPDFLoader(file)
    pages = loader.load_and_split()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=200, chunk_overlap=50)
    texts = text_splitter.split_documents(pages)
    final_texts = ""
    for text in texts:
        final_texts = final_texts + text.page_content
    return final_texts

def csv_preprocessing(file):
    df = pd.read_csv(file, encoding='utf-8')
    grouped_data = df.groupby('doc_name')['text'].agg(list).reset_index()
    pdf_dict = dict(zip(grouped_data['doc_name'], grouped_data['text']))
    for key in pdf_dict:
        pdf_dict[key] = " ".join([str(x) for x in pdf_dict[key]])

    return pdf_dict

#LLM pipeline
def llm_pipeline(filepath, filetype):
    input_text = csv_preprocessing(filepath)
    pipe_summarize = pipeline(
        'summarization',
        model = base_model,
        tokenizer = tokenizer,
        max_length = 512, 
        min_length = 50)
    
    result = []
    for key in input_text:
        result.append(pipe_summarize(input_text[key]))
    return " ".join(result)
    

