def extract_context(messages):

    full_text = " ".join(
        [msg["content"] for msg in messages]
    ).lower()

    context = {
        "role": None,
        "seniority": None,
        "personality": False
    }

    # Role detection

    if "java" in full_text:
        context["role"] = "Java Developer"

    if "python" in full_text:
        context["role"] = "Python Developer"

    # Seniority

    if "mid" in full_text:
        context["seniority"] = "Mid-level"

    if "senior" in full_text:
        context["seniority"] = "Senior"

    # Personality

    if "personality" in full_text:
        context["personality"] = True

    return context