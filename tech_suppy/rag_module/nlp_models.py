from langchain.embeddings import HuggingFaceEmbeddings
from sentence_transformers import SentenceTransformer
from transformers import GPT2LMHeadModel, GPT2Tokenizer
from langchain.chat_models.gigachat import GigaChat
import os

from .rag_constants import EMBEDDING_MODEL_NAME, GPT_MODEL_NAME


def get_embeddings_model():
    return HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL_NAME)


def get_sent_transformer_model():
    return SentenceTransformer(EMBEDDING_MODEL_NAME)


def get_model():
    return GigaChat(credentials=os.getenv('GIGA_AUTH'), verify_ssl_certs=False)


def get_tokenizer():
    return GPT2Tokenizer.from_pretrained(GPT_MODEL_NAME, token=os.getenv('HF_TOKEN'))
