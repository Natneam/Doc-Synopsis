from sentence_transformers import SentenceTransformer
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import PyPDFLoader
from faiss import IndexFlatIP
import torch
from transformers import LongformerForQuestionAnswering, LongformerTokenizer
from .utils import csv_preprocessing, pdf_preprocessing

# Load pre-trained model and tokenizer for question answering
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

    if filetype == "pdf":
        final_texts = pdf_preprocessing(file_path)
    elif filetype == "csv":
        final_texts = " ".join(csv_preprocessing(file_path).values())

    embedder = SentenceTransformer('paraphrase-MiniLM-L6-v2')
    document_embedding = embedder.encode(final_texts)

    document_embedding = document_embedding.reshape((1, -1))

    vector_store = IndexFlatIP(document_embedding.shape[1])
    vector_store.add(document_embedding)

    query_vector = embedder.encode(question)
    query_vector = query_vector.reshape((1, -1))
    _, relevant_indexes = vector_store.search(query_vector, 5)

    relevant_contexts = [final_texts[i] for i in relevant_indexes[0]]

    for context in relevant_contexts:
        result.append(answer_question(question, context))

    return " ".join(result)