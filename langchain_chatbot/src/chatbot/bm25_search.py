import json
import re
from typing import Any, Dict, List, Tuple

import numpy as np
from rank_bm25 import BM25Okapi

# # BM25 Search Implementation for Legal Texts AI-Generated

def tokenize_for_bm25(text: str) -> List[str]:
	"""Tokenize legal text while preserving section patterns like (1), (a), 10A."""
	text = text.lower().replace("\n", " ")
	token_pattern = r"\([a-z0-9]+\)|[a-z]+(?:'[a-z]+)?|\d+[a-z]?"
	return re.findall(token_pattern, text)


def build_bm25_corpus(metadata: List[Dict[str, Any]]) -> List[List[str]]:
	corpus: List[List[str]] = []
	for item in metadata:
		combined = (
			f"{item.get('section_number', '')} "
			f"{item.get('subsection', '')} "
			f"{item.get('text', '')}"
		)
		corpus.append(tokenize_for_bm25(combined))
	return corpus


def load_bm25(json_file_path: str) -> Tuple[BM25Okapi, List[Dict[str, Any]]]:
	with open(json_file_path, "r", encoding="utf-8") as json_file:
		metadata = json.load(json_file)

	tokenized_corpus = build_bm25_corpus(metadata)
	# Tokenized_corpus is a list of list of strings, where each inner list contains strings that are the tokens of the section, subsection, and its text e.g., '107','(2)','the','consumer','has','the','right','to','file','a'... etc.
	bm25 = BM25Okapi(tokenized_corpus) 
	# print(f"\nbm25: {bm25}\n")
	return bm25, metadata


def search_bm25(query: str, json_file_path: str, k: int = 3) -> List[Dict[str, Any]]:
	bm25, metadata = load_bm25(json_file_path)
	query_tokens = tokenize_for_bm25(query)
	scores = bm25.get_scores(query_tokens)

	top_indices = np.argsort(scores)[::-1][:k]
	# print ([metadata[i] for i in top_indices])
	return [metadata[i] for i in top_indices]


# if __name__ == "__main__":
# 	path = r"C:\Mohit\Dance\chatbot\sections.json"
# 	results = search_bm25("whos is consumer", path, k=3)
# 	for row in results:
# 		print(row)
# BM25 Search Implementation for Legal Texts AI-Generated till here
