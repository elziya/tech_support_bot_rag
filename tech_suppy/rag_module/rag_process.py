from sklearn.metrics.pairwise import cosine_similarity


def count_groundedness(contexts, answer, emb_model):
    answer_emb = [emb_model.encode(answer, convert_to_tensor=True).tolist()]
    groundedness = []
    for context in contexts:
        context_emb = [emb_model.encode(context.page_content, convert_to_tensor=True).tolist()]
        groundedness.append(cosine_similarity(answer_emb, context_emb)[0][0])

    return sum(groundedness)/len(groundedness)


def count_context_relevance(contexts, query, emb_model):
    query_emb = [emb_model.encode(query, convert_to_tensor=True).tolist()]
    context_relevance = []
    for context in contexts:
        context_emb = [emb_model.encode(context[0].page_content, convert_to_tensor=True).tolist()]
        context_relevance.append(cosine_similarity(query_emb, context_emb)[0][0])
    return sum(context_relevance)/len(context_relevance)


def is_about_docs(query, vector_db, emb_model):
    search_result = vector_db.similarity_search_with_score(query, k=1)
    score = count_context_relevance(search_result, query, emb_model)
    return score > 0.6


def get_answer(query, rag_chain, emb_model):
    count = 0
    while count < 3:
        response = rag_chain.invoke({"query": query})
        response_text = response['result']
        source = response['source_documents'][0].metadata['source']
        contexts = response['source_documents']

        if count_groundedness(contexts, response_text, emb_model) >= 0.5:
            return response_text, source, False

        count += 1
        if count == 3:
            return response_text, source, True


