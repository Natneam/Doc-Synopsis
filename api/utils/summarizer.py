from transformers import pipeline, T5ForConditionalGeneration, AutoTokenizer
import torch
from .utils import csv_preprocessing, pdf_preprocessing

# Load pre-trained model and tokenizer for summarization
summarization_tokenizer = AutoTokenizer.from_pretrained("MBZUAI/LaMini-T5-738M")
summarization_model = T5ForConditionalGeneration.from_pretrained("MBZUAI/LaMini-T5-738M", device_map='auto', torch_dtype=torch.float32)


def summary_pipeline(filepath, filetype, token_size=2000): # Adjust token_size based on machine capacity.
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
            result.append(pipe_summarize(item[:min(token_size, len(item) - 1)])[0]['summary_text'] + "\n\n")
        return " ".join([r.capitalize() for r in result])
    
    elif (filetype == 'pdf'):
        input_text = pdf_preprocessing(filepath)
        return pipe_summarize(input_text)[0]["summary_text"]