import re


def analyze_habit(text):

    text = text.lower()

    result = {
        "habit": None,
        "duration": None,
        "frequency": None,
        "category": None
    }

    # -------------------------
    # Detect duration
    # -------------------------

    duration_match = re.search(
        r"(\d+)\s*(hour|hours|hr|hrs|minute|minutes|min|mins)",
        text
    )

    if duration_match:

        number = duration_match.group(1)
        unit = duration_match.group(2)

        result["duration"] = f"{number} {unit}"

    # -------------------------
    # Detect frequency
    # -------------------------

    if "every day" in text or "daily" in text:

        result["frequency"] = "Daily"

    elif "every week" in text or "weekly" in text:

        result["frequency"] = "Weekly"

    elif "three times" in text:

        result["frequency"] = "3 times per week"

    else:

        result["frequency"] = "Not specified"

    # -------------------------
    # Detect category
    # -------------------------

    if any(word in text for word in [
        "study",
        "java",
        "python",
        "read",
        "learning"
    ]):

        result["category"] = "Study"

    elif any(word in text for word in [
        "exercise",
        "gym",
        "workout",
        "running"
    ]):

        result["category"] = "Fitness"

    elif any(word in text for word in [
        "water",
        "sleep",
        "health"
    ]):

        result["category"] = "Health"

    else:

        result["category"] = "Personal"

    # -------------------------
    # Detect habit
    # -------------------------

    if "study" in text:

        result["habit"] = "Study"

    elif "exercise" in text:

        result["habit"] = "Exercise"

    elif "read" in text:

        result["habit"] = "Reading"

    elif "water" in text:

        result["habit"] = "Drink Water"

    else:

        result["habit"] = "General Habit"

    return result