import json
from pathlib import Path
import re

from .chunking import chunk_sections
from .config import EXTRACTED_TEXT_PATH, SECTIONS_JSON_PATH, SECTIONS_TEXT_PATH

def data_prep(
    txt_file_path: str | Path = EXTRACTED_TEXT_PATH,
    sections_text_path: str | Path = SECTIONS_TEXT_PATH,
    sections_json_path: str | Path = SECTIONS_JSON_PATH,
) -> str:
    txt_file_path = Path(txt_file_path)
    sections_text_path = Path(sections_text_path)
    sections_json_path = Path(sections_json_path)

    with open(txt_file_path, "r", encoding="utf-8") as txt_file:
        text = txt_file.read()
        section_numbers = re.findall(r"(^\d+\.?\s{0,1})", text, re.MULTILINE)
        print("Length of section_numbers: ",len(section_numbers))

        pattern = r"^\d+\.?\s*(.*?)(?=^\d+\.?|\Z)"
        sections = re.findall(pattern, text, re.MULTILINE | re.DOTALL)
        print("Length of section content: ",len(sections))
        
        # Making a list of dictionary with each dictionary containing keys 'section_number' and 'section_content'
        lst_cpa_dict = []
        for index,section_number in enumerate(section_numbers):
            cpa_dict = {}
            cpa_dict['section_number'] = section_number
            cpa_dict['section_content'] = sections[index]
            lst_cpa_dict.append(cpa_dict)

        sections_text_path.parent.mkdir(parents=True, exist_ok=True)
        with open(sections_text_path, "w", encoding="utf-8") as f:
            for item in lst_cpa_dict:
                f.write(f"Section Number: {item['section_number']}\n")
                f.write(f"Section Content: {item['section_content']}\n\n")

    chunked = chunk_sections(lst_cpa_dict)

    sections_json_path.parent.mkdir(parents=True, exist_ok=True)
    with open(sections_json_path, "w", encoding="utf-8") as json_file:
        json.dump(chunked, json_file, indent=2)
    
    return str(sections_json_path)