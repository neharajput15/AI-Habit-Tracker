import pandas as pd
from sklearn.linear_model import LogisticRegression

from database import get_connection


# =====================================================
# GET HABIT HISTORY
# =====================================================

def get_habit_history(habit_id):

    conn = get_connection()

    try:

        query = """
        SELECT
            completed_date,
            completed
        FROM progress
        WHERE habit_id = %s
        ORDER BY completed_date ASC
        """

        df = pd.read_sql_query(
            query,
            conn,
            params=(habit_id,)
        )

    finally:

        conn.close()

    return df


# =====================================================
# GET LAST 5 DAYS
# =====================================================

def get_last_five_days(habit_id):

    df = get_habit_history(habit_id)

    if df.empty:
        return []

    df = df.tail(5).copy()

    result = []

    for _, row in df.iterrows():

        completed = int(row["completed"])

        symbol = "✅" if completed == 1 else "❌"

        result.append(
            (
                str(row["completed_date"]),
                symbol
            )
        )

    return result


# =====================================================
# CALCULATE RECENT CONSISTENCY
# =====================================================

def get_recent_consistency(habit_id):

    df = get_habit_history(habit_id)

    if df.empty:
        return 0

    recent = df.tail(5).copy()

    recent["completed"] = pd.to_numeric(
        recent["completed"],
        errors="coerce"
    )

    recent = recent.dropna(
        subset=["completed"]
    )

    if recent.empty:
        return 0

    consistency = (
        recent["completed"].sum()
        / len(recent)
    ) * 100

    return round(consistency, 2)


# =====================================================
# ML HABIT COMPLETION PREDICTION
# =====================================================

def predict_habit_completion(habit_id):

    df = get_habit_history(habit_id)

    if df.empty:
        return None, "No habit history found."

    # =================================================
    # CLEAN DATA
    # =================================================

    df = df.dropna(
        subset=[
            "completed_date",
            "completed"
        ]
    ).copy()

    df["completed"] = pd.to_numeric(
        df["completed"],
        errors="coerce"
    )

    df = df.dropna(
        subset=["completed"]
    ).copy()

    df["completed"] = df[
        "completed"
    ].astype(int)

    # =================================================
    # MINIMUM 5 RECORDS
    # =================================================

    if len(df) < 5:

        return None, (
            "Need at least 5 days of habit history."
        )

    # =================================================
    # NEED BOTH CLASSES
    # =================================================

    if df["completed"].nunique() < 2:

        return None, (
            "Need both completed and missed days "
            "for ML prediction."
        )

    # =================================================
    # DAY NUMBER
    # =================================================

    df["day_number"] = range(
        1,
        len(df) + 1
    )

    # =================================================
    # RECENT COMPLETION RATE
    # =================================================

    df["recent_rate"] = (
        df["completed"]
        .rolling(
            window=5,
            min_periods=1
        )
        .mean()
    )

    # =================================================
    # PREVIOUS DAY STATUS
    # =================================================

    df["previous_completed"] = (
        df["completed"]
        .shift(1)
        .fillna(0)
    )

    # =================================================
    # TRAINING DATA
    # =================================================

    training_df = df.iloc[1:].copy()

    if len(training_df) < 4:

        return None, (
            "Not enough history for ML prediction."
        )

    X = training_df[
        [
            "day_number",
            "recent_rate",
            "previous_completed"
        ]
    ]

    y = training_df["completed"]

    # =================================================
    # CHECK BOTH CLASSES
    # =================================================

    if y.nunique() < 2:

        return None, (
            "Need both completed and missed days "
            "for ML prediction."
        )

    # =================================================
    # CREATE AND TRAIN MODEL
    # =================================================

    model = LogisticRegression(
        max_iter=1000
    )

    model.fit(X, y)

    # =================================================
    # PREPARE NEXT DAY
    # =================================================

    recent_rate = (
        df["completed"]
        .tail(5)
        .mean()
    )

    previous_completed = int(
        df["completed"].iloc[-1]
    )

    next_day = [[
        len(df) + 1,
        recent_rate,
        previous_completed
    ]]

    # =================================================
    # PREDICT
    # =================================================

    probabilities = model.predict_proba(
        next_day
    )[0]

    classes = list(
        model.classes_
    )

    if 1 in classes:

        completed_index = classes.index(1)

        prediction = (
            probabilities[completed_index]
            * 100
        )

    else:

        prediction = 0

    # =================================================
    # LIMIT 0–100
    # =================================================

    prediction = max(
        0,
        min(
            100,
            prediction
        )
    )

    return round(
        prediction,
        2
    ), None