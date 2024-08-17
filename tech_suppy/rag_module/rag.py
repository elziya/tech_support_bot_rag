import os
import locale
from langchain.chains import RetrievalQA
from langchain import PromptTemplate
from langchain.retrievers import ContextualCompressionRetriever
from langchain.retrievers.document_compressors import CrossEncoderReranker
from langchain_community.cross_encoders import HuggingFaceCrossEncoder
from langchain_community.vectorstores import Clickhouse, ClickhouseSettings

from .utils import load_docs_from_jsonl
from .rag_constants import CHUNKS_PATH, CROSS_ENCODER_NAME


def get_vector_db(embedding_model):
    settings = ClickhouseSettings(
        username=os.getenv('CH_USERNAME'),
        password=os.getenv('CH_PASSWORD'),
        host=os.getenv('CH_HOST'),
        port=os.getenv('CH_PORT'),
        table=os.getenv('CH_PORT')
    )

    texts = load_docs_from_jsonl(CHUNKS_PATH)
    vector_db = Clickhouse.from_documents(texts, embedding_model, config=settings)
    return vector_db


def get_chain(vectordb, model, tokenizer):
    locale.getpreferredencoding = getpreferredencoding

    local_llm = model
    retriever = vectordb.as_retriever(search_kwargs={"k": 20})

    cross_encoder = HuggingFaceCrossEncoder(model_name=CROSS_ENCODER_NAME)
    compressor = CrossEncoderReranker(model=cross_encoder, top_n=3)
    compression_retriever = ContextualCompressionRetriever(
        base_compressor=compressor, base_retriever=retriever
    )

    template = '''
    Контекст: {context}

    Используя контекст, ответь на вопрос: {question}. Этот вопрос очень важен для меня. Помоги, пожалуйста.
    Ответ:
    '''
    prompt = PromptTemplate(
        template=template,
        input_variables=[
            'context',
            'question',
        ]
    )

    qa_chain = RetrievalQA.from_chain_type(
        local_llm,
        retriever=compression_retriever,
        return_source_documents=True,
        chain_type="stuff",
        chain_type_kwargs={"prompt": prompt}
    )

    return qa_chain


def getpreferredencoding(do_setlocale=True):
    return "UTF-8"
