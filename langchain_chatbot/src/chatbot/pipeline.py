from .bm25_search import search_bm25
from .search_faiss import search_faiss_index
from .llm_services import call_llama_api
from .query_expansion import rewrite_by_intent, classify_query



def main(query: str) -> str:
    list_queries = rewrite_by_intent(query, classify_query(query))
    # save_txt_file()
    # json_file_path = data_prep()
    json_file_path = r"C:\Mohit\Dance\chatbot\data\processed\sections_debug.json"
    # build_faiss_index(json_file_path)
    combined_result = []
    seen_keys = set()
    for q in list_queries:
        # print(f"Results for query: {q}")
        faiss_results = search_faiss_index(q, metadata_path=json_file_path, top_k=5)
        bm25_results = search_bm25(q, json_file_path, k=5)
        for item in faiss_results + bm25_results:
            key = (item.get("section_number", ""), item.get("subsection", ""))
            if key not in seen_keys:
                seen_keys.add(key)
                combined_result.append(item)
    print("Combined Results for LLM Context:", combined_result)
    llm_response = call_llama_api(query, combined_result[:4])  # using top 4 results as context
    print("LLM Response:", llm_response)
    return llm_response

