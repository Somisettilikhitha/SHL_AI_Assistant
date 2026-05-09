def classify_intent(query):

    query = query.lower()

    # -----------------------------------
    # COMPARISON
    # -----------------------------------

    if "compare" in query:

        return "comparison"

    # -----------------------------------
    # NON-SHL / OUT-OF-DOMAIN
    # -----------------------------------

    non_shl_keywords = [

        "ipl",
        "cricket",
        "movie",
        "weather",
        "salary",
        "politics",
        "election",
        "stock",
        "bitcoin",
        "news",
        "sports",
        "football",
        "match",
        "who will win",
        "actor",
        "instagram",
        "youtube"

    ]

    for word in non_shl_keywords:

        if word in query:

            return "out_of_scope"

    # -----------------------------------
    # VAGUE QUERIES
    # -----------------------------------

    vague_queries = [

        "need assessment",
        "assessment",
        "test",
        "need test"

    ]

    for vague in vague_queries:

        if vague == query.strip():

            return "clarification"

    # -----------------------------------
    # DEFAULT
    # -----------------------------------

    return "recommendation"