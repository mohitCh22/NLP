import re

def chunk_sections(sections):
    chunked_data = []

    for section in sections:
        sec_num = str(section["section_number"]).strip()
        content = section["section_content"].strip()

        # Split using subsection markers like (1), (2), etc.
        parts = re.split(r'(\(\d+\))', content)
        
        # Case: No subsections found
        if len(parts) == 1:
            chunked_data.append({
                "section_number": sec_num,
                "subsection": None,
                "chunk_id": f"{sec_num}_0",
                "text": content
            })
            continue  

        # If there's text before the first subsection marker
        if parts[0].strip() and len(parts) > 1:  
            section_intro = parts[0]  
            chunked_data.append({
                    "section_number": sec_num,
                    "subsection": None,
                    "chunk_id": f"{sec_num}_0",
                    "text": section_intro.strip()
                })    
        

        # Pair subsection with its content
        for i in range(1, len(parts), 2):
            
            subsection = parts[i]  # (1), (2), etc.
            text = parts[i + 1].strip()
            if text:
                chunked_data.append({
                    "section_number": sec_num,
                    "subsection": subsection,
                    "chunk_id": f"{sec_num}_{subsection.strip('()')}",
                    "text": text
                })

    return chunked_data