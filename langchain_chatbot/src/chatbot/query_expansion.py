import re
from .intent_config import INTENT_CONFIG

def extract_topic(query: str) -> str:
    """
    Extract the main legal topic/entity from the query.
    """

    q = query.lower()

    patterns = [
        r"who is (.+)",
        r"what is (.+)",
        r"define (.+)",
        r"meaning of (.+)",
        r"rights of (.+)",
        r"how to (.+)",
        r"procedure for (.+)"
    ]

    for pattern in patterns:
        match = re.search(pattern, q)

        if match:
            topic = match.group(1)

            # clean noisy words
            noise_words = [
                "under indian consumer law",
                "under consumer law",
                "under the act",
                "in india"
            ]

            for word in noise_words:
                topic = topic.replace(word, "")

            return topic.strip()

    return q.strip()


def classify_query(query: str) -> str:
    q = query.lower()

    if any(x in q for x in ["who is", "what is", "define", "meaning"]):
        return "definition"

    elif any(x in q for x in ["how", "procedure", "steps"]):
        return "procedure"

    elif any(x in q for x in ["rights"]):
        return "rights"

    elif any(x in q for x in ["penalty", "punishment", "fine"]):
        return "penalty"

    elif any(x in q for x in ["jurisdiction"]):
        return "jurisdiction"

    return "general"

def rewrite_by_intent(query: str, intent: str) -> list:
    topic = extract_topic(query)

    config = INTENT_CONFIG.get(intent)

    if not config: 
        print(f"No config found for intent: {intent}. Returning original query.")
        return [query]

    rewrites = [query]

    for template in config["rewrite_templates"]: 
        rewrites.append( 
            template.format(topic=topic) 
            ) 
    return list(set(rewrites))

    # if intent == "definition":

    #     rewrites.extend([
    #         f"{topic} means",
    #         f"definition of {topic}",
    #         topic
    #     ])

    # elif intent == "procedure":

    #     rewrites.extend([
    #         f"procedure for {topic}",
    #         f"{topic} may be filed",
    #         f"steps for {topic}",
    #         topic
    #     ])

    # elif intent == "rights":

    #     rewrites.extend([
    #         f"{topic} rights",
    #         f"right to {topic}",
    #         topic
    #     ])

    # elif intent == "penalty":

    #     rewrites.extend([
    #         f"penalty for {topic}",
    #         f"punishment for {topic}",
    #         f"fine for {topic}",
    #         topic
    #     ])

    # elif intent == "jurisdiction":

    #     rewrites.extend([
    #         f"jurisdiction of {topic}",
    #         f"{topic} shall have jurisdiction",
    #         topic
    #     ])

    # else:
    #     rewrites.append(topic)

    # return list(set(rewrites))