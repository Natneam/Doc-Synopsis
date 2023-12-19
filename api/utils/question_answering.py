from transformers import LongformerForQuestionAnswering, LongformerTokenizer
import torch
from .utils import csv_preprocessing, pdf_preprocessing

#Load pre-trained model and tokenizer for question answering
question_answering_model = LongformerForQuestionAnswering.from_pretrained("allenai/longformer-base-4096")
question_answering_tokenizer = LongformerTokenizer.from_pretrained("allenai/longformer-base-4096")


def answer_question(question, context):
    inputs = question_answering_tokenizer(text=question, text_pair=context, return_tensors="pt", max_length=4096, truncation=True)
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