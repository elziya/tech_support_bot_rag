from langchain.text_splitter import RecursiveCharacterTextSplitter
import regex as re
from langchain.document_loaders import UnstructuredURLLoader

from rag_module import get_tokenizer, save_docs_to_jsonl, CHUNKS_PATH, DOCS_PATH

TOKENIZER = get_tokenizer()


def upload_documentation(urls):
    docs = extract_text_from_url(urls)
    save_docs_to_jsonl(docs, DOCS_PATH)
    blocks = get_docs_chunks(docs, 256, 40)
    preprocess_text(blocks)
    save_docs_to_jsonl(blocks, CHUNKS_PATH)


def token_len(text):
    tokens = TOKENIZER.encode(text)
    return len(tokens)


def extract_text_from_url(urls):
    loader = UnstructuredURLLoader(urls=urls)
    documents = loader.load()
    return documents


def get_docs_chunks(docs, chunk_size, chunk_overlap):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=token_len,
        separators=['\n\n', '\n', ' ', '']
    )
    texts = text_splitter.split_documents(docs)
    return texts


def preprocess_text(texts):
    for text in texts:
        text.page_content = re.sub("\n\n", "\n", text.page_content)

