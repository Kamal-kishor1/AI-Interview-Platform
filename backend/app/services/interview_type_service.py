import re

CATEGORIES = {
    "AI/ML": {
        "machine learning",
        "deep learning",
        "tensorflow",
        "pytorch",
        "nlp",
        "computer vision",
        "opencv",
    },
    "Data Science": {
        "pandas",
        "numpy",
        "statistics",
        "scikit-learn",
        "regression",
    },
    "Software Engineering": {
        "python",
        "java",
        "c++",
        "react",
        "fastapi",
        "node.js",
    },
    "Embedded / Electronics": {
        "arduino",
        "raspberry pi",
        "embedded",
        "microcontroller",
        "sensor",
    },
}


DEFAULT_CATEGORY = "General Technical"


def detect_interview_type(resume_text: str) -> dict:
    if not resume_text or not resume_text.strip():
        return {
            "interview_type": DEFAULT_CATEGORY,
            "matched_keywords": [],
            "match_count": 0,
        }

    clean_text = re.sub(r"\s+", " ", resume_text.lower()).strip()

    best_category = DEFAULT_CATEGORY
    best_matches = []
    max_match_count = 0

    for category, keywords in CATEGORIES.items():
        current_matches = []

        for keyword in keywords:
            normalized_keyword = keyword.lower().strip()
            pattern = rf"\b{re.escape(normalized_keyword)}\b"

            if re.search(pattern, clean_text):
                current_matches.append(keyword)

        if len(current_matches) > max_match_count:
            max_match_count = len(current_matches)
            best_category = category
            best_matches = current_matches

    return {
        "interview_type": best_category,
        "matched_keywords": best_matches,
        "match_count": max_match_count,
    }
