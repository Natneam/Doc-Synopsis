from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import PyPDFLoader, DirectoryLoader
import pandas as pd
from transformers import pipeline, T5Tokenizer, T5ForConditionalGeneration, T5ForQuestionAnswering, AutoTokenizer
import torch

# Load pre-trained model and tokenizer for summarization
summarization_tokenizer = AutoTokenizer.from_pretrained("t5-small")
summarization_model = T5ForConditionalGeneration.from_pretrained("t5-small", device_map='auto', torch_dtype=torch.float32)

# Load pre-trained model and tokenizer for question answering
question_answering_model = T5ForQuestionAnswering.from_pretrained("t5-small")
question_answering_tokenizer = T5Tokenizer.from_pretrained("t5-small")

def pdf_preprocessing(file):
    loader =  PyPDFLoader(file)
    pages = loader.load_and_split()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=200, chunk_overlap=50)
    texts = text_splitter.split_documents(pages)
    final_texts = ""
    for text in texts:
        final_texts = final_texts + text.page_content
    return final_texts

def csv_preprocessing(filepath):
    result = {}
    for chunk in pd.read_csv(filepath, encoding='utf-8', chunksize=200):
        grouped_data = chunk.groupby('doc_name')['text'].agg(list).reset_index()
        pdf_dict = dict(zip(grouped_data['doc_name'], grouped_data['text']))
        for key in pdf_dict:
            if key in result:
                result[key] += " ".join([str(x) for x in pdf_dict[key]])
            else:
                result[key] = " ".join([str(x) for x in pdf_dict[key]])

    return result

# LLM pipelines
def summary_pipeline(filepath, filetype, token_size=1000):
    pipe_summarize = pipeline(
        'summarization',
        model=summarization_model,
        tokenizer=summarization_tokenizer,
        max_length=512,
        min_length=50,
        batch_size=1
    )
    
    if (filetype == 'csv'):
        result = []
        input_text = csv_preprocessing(filepath)
        for item in input_text.values():
            result.append(pipe_summarize(item[:min(token_size, len(item) - 1)])[0]['summary_text'])
        return " ".join([r.capitalize() for r in result])
    
    elif (filetype == 'pdf'):
        input_text = pdf_preprocessing(filepath)
        return pipe_summarize(input_text)

def answer_question(question, context):
    inputs = question_answering_tokenizer(text=question, text_pair=context, return_tensors="pt")
    with torch.no_grad():
        outputs = question_answering_model(**inputs)

    start_positions = outputs.start_logits.argmax()
    end_positions = outputs.end_logits.argmin()

    # Extract the answer span using the positions
    answer = question_answering_tokenizer.decode(inputs["input_ids"][0, start_positions:end_positions + 1])

    return answer

def question_answering_pipeline(file_path, filetype, question):
    result = []

    if (filetype == "csv"):
        text_data = csv_preprocessing(file_path)
        for item in text_data:
            result.append(answer_question(question, item))
    elif (filetype == "pdf"):
        text_data = pdf_preprocessing(file_path)
        result.append(answer_question(question, text_data))

    return " ".join(result)
