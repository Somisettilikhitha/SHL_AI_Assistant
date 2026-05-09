import json

# -----------------------------------
# LOAD FULL SHL CATALOG
# -----------------------------------

with open(
    "full_catalog.json",
    "r",
    encoding="utf-8"
) as f:

    raw_data = json.load(f)

# -----------------------------------
# CLEANED CATALOG
# -----------------------------------

cleaned_catalog = []

# -----------------------------------
# PROCESS EACH ASSESSMENT
# -----------------------------------

for item in raw_data:

    # -----------------------------------
    # SAFE FIELD EXTRACTION
    # -----------------------------------

    name = item.get(
        "name",
        ""
    ).strip()

    url = item.get(
        "link",
        ""
    ).strip()

    description = item.get(
        "description",
        ""
    ).strip()

    keys = item.get(
        "keys",
        []
    )

    job_levels = item.get(
        "job_levels",
        []
    )

    duration = item.get(
        "duration",
        ""
    )

    adaptive = item.get(
        "adaptive",
        "No"
    )

    remote = item.get(
        "remote",
        "Yes"
    )

    languages = item.get(
        "languages",
        []
    )

    # -----------------------------------
    # FULL SEARCHABLE TEXT
    # -----------------------------------

    key_text = " ".join(
        [str(k) for k in keys]
    ).lower()

    full_text = (

        name + " " +

        description + " " +

        key_text

    ).lower()

    # -----------------------------------
    # TEST TYPE DETECTION
    # -----------------------------------

    test_type = "General"

    # -----------------------------------
    # COGNITIVE
    # STRICT RULES
    # -----------------------------------

    if (

        "cognitive ability" in full_text
        or
        "general ability" in full_text
        or
        "numerical reasoning" in full_text
        or
        "verbal reasoning" in full_text
        or
        "logical reasoning" in full_text
        or
        "inductive reasoning" in full_text
        or
        "deductive reasoning" in full_text
        or
        "aptitude test" in full_text
        or
        "critical thinking" in full_text
        or
        "gsa" in full_text

    ):

        test_type = "Cognitive"

    # -----------------------------------
    # PERSONALITY
    # -----------------------------------

    elif (

        "personality" in full_text
        or
        "behavior" in full_text
        or
        "behaviour" in full_text
        or
        "opq" in full_text
        or
        "leadership style" in full_text

    ):

        test_type = "Personality"

    # -----------------------------------
    # TECHNICAL
    # -----------------------------------

    elif (

        "technical" in full_text
        or
        "java" in full_text
        or
        ".net" in full_text
        or
        "python" in full_text
        or
        "aws" in full_text
        or
        "cloud" in full_text
        or
        "software engineer" in full_text
        or
        "developer" in full_text
        or
        "coding" in full_text
        or
        "programming" in full_text

    ):

        test_type = "Technical"

    # -----------------------------------
    # FINANCE
    # -----------------------------------

    elif (

        "finance" in full_text
        or
        "accounting" in full_text
        or
        "banking" in full_text
        or
        "accounts payable" in full_text
        or
        "accounts receivable" in full_text

    ):

        test_type = "Finance"

    # -----------------------------------
    # SIMULATION
    # -----------------------------------

    elif (

        "simulation" in full_text

    ):

        test_type = "Simulation"

    # -----------------------------------
    # SALES
    # -----------------------------------

    elif (

        "sales" in full_text
        or
        "customer service" in full_text
        or
        "retail" in full_text

    ):

        test_type = "Sales"

    # -----------------------------------
    # MANAGEMENT
    # -----------------------------------

    elif (

        "manager" in full_text
        or
        "management" in full_text
        or
        "supervisor" in full_text

    ):

        test_type = "Management"

    # -----------------------------------
    # ENRICHED DESCRIPTION
    # -----------------------------------

    enriched_description = (

        f"{description} "

        f"Job Levels: "
        f"{', '.join(job_levels)}. "

        f"Duration: "
        f"{duration}. "

        f"Adaptive: "
        f"{adaptive}. "

        f"Remote Testing: "
        f"{remote}. "

        f"Languages: "
        f"{', '.join(languages)}. "

        f"Categories: "
        f"{', '.join(keys)}."
    )

    # -----------------------------------
    # FINAL OBJECT
    # -----------------------------------

    cleaned_item = {

        "name": name,

        "url": url,

        "description": enriched_description,

        "test_type": test_type,

        "job_levels": job_levels,

        "duration": duration,

        "adaptive": adaptive,

        "remote": remote,

        "languages": languages,

        "keys": keys
    }

    # -----------------------------------
    # REMOVE INVALID ENTRIES
    # -----------------------------------

    if (

        name
        and
        url
        and
        len(name) > 2
        and
        url.startswith("http")

    ):

        cleaned_catalog.append(
            cleaned_item
        )

# -----------------------------------
# REMOVE DUPLICATES
# -----------------------------------

unique_catalog = []

seen_urls = set()

for item in cleaned_catalog:

    if item["url"] not in seen_urls:

        seen_urls.add(
            item["url"]
        )

        unique_catalog.append(
            item
        )

# -----------------------------------
# SAVE FINAL catalog.json
# -----------------------------------

with open(
    "catalog.json",
    "w",
    encoding="utf-8"
) as f:

    json.dump(
        unique_catalog,
        f,
        indent=4,
        ensure_ascii=False
    )

# -----------------------------------
# SUCCESS MESSAGE
# -----------------------------------

print(
    "catalog.json created successfully"
)

print(
    "Total assessments:",
    len(unique_catalog)
)