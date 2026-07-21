INTENT_CONFIG = {

"definition": {

    "rewrite_templates": [
        "{topic} means",
        "definition of {topic}",
        "{topic}"
    ],

    "boost_phrases": [
        "means",
        "defined as"
    ]
},

"eligibility": {

    "rewrite_templates": [
        "who may file {topic}",
        "{topic} may be filed by",
        "{topic} filed by",
        "{topic}"
    ],

    "boost_phrases": [
        "may be filed by",
        "shall be filed by",
        "eligible",
        "entitled"
    ]
},

"jurisdiction": {

    "rewrite_templates": [
        "jurisdiction of {topic}",
        "{topic} shall have jurisdiction",
        "{topic}"
    ],

    "boost_phrases": [
        "shall have jurisdiction",
        "pecuniary jurisdiction",
        "territorial jurisdiction"
    ]
},

"penalty": {

    "rewrite_templates": [
        "penalty for {topic}",
        "punishment for {topic}",
        "{topic}"
    ],

    "boost_phrases": [
        "punishable",
        "liable",
        "imprisonment",
        "fine"
    ]
},

"procedure": {

    "rewrite_templates": [
        "procedure for {topic}",
        "steps for {topic}",
        "{topic}"
    ],

    "boost_phrases": [
        "procedure",
        "application",
        "shall"
    ]
}

}
