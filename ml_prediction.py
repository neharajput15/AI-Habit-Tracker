import sqlite3
import pandas as pd
from sklearn.linear_model import LogisticRegression


# =====================================================
# DATABASE CONNECTION
# =====================================================

def get_connection():
    return sqlite3.connect("habit_tracker.db")


# =====================================================
# GET HABIT HISTORY
# =====================================================

def get_habit_history(habit_id):

    conn = get_connection()

    query = """
    SELECT
        completed_date,
        completed
    FROM progress
    WHERE habit_id = ?
    ORDER BY completed_date ASC
    """

    df = pd.read_sql_query(
        query,
        conn,
        params=(habit_id,)
    )

    conn.close()

    return df


# =====================================================
# GET LAST 5 DAYS
# =====================================================

def get_last_five_days(habit_id):

    df = get_habit_history(habit_id)

    if df.empty:
        return []

    # Keep the latest 5 records
    df = df.tail(5)

    result = []

    for _, row in df.iterrows():

        completed = int(row["completed"])

        if completed == 1:
            symbol = "✅"
        else:
            symbol = "❌"

        result.append(
            (
                row["completed_date"],
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

    # Use latest 5 records
    recent = df.tail(5)

    consistency = (
        recent["completed"].sum()
        / len(recent)
    ) * 100

    return round(
        consistency,
        2
    )


# =====================================================
# ML HABIT COMPLETION PREDICTION
# =====================================================

def predict_habit_completion(habit_id):

    df = get_habit_history(habit_id)

    # =================================================
    # NO DATA
    # =================================================

    if df.empty:

        return None, (
            "No habit history found."
        )

    # =================================================
    # CLEAN DATA
    # =================================================

    df = df.dropna(
        subset=[
            "completed_date",
            "completed"
        ]
    )

    df["completed"] = pd.to_numeric(
        df["completed"],
        errors="coerce"
    )

    df = df.dropna(
        subset=["completed"]
    )

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
    # REMOVE FIRST ROW
    # =================================================

    training_df = df.iloc[1:].copy()

    # Need enough rows after feature creation
    if len(training_df) < 4:

        return None, (
            "Not enough history for ML prediction."
        )

    # =================================================
    # FEATURES
    # =================================================

    X = training_df[
        [
            "day_number",
            "recent_rate",
            "previous_completed"
        ]
    ]

    y = training_df[
        "completed"
    ]

    # =================================================
    # CHECK BOTH CLASSES AGAIN
    # =================================================

    if y.nunique() < 2:

        return None, (
            "Need both completed and missed days "
            "for ML prediction."
        )

    # =================================================
    # CREATE MODEL
    # =================================================

    model = LogisticRegression(
        max_iter=1000
    )

    # =================================================
    # TRAIN MODEL
    # =================================================

    model.fit(
        X,
        y
    )

    # =================================================
    # PREPARE NEXT-DAY DATA
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
    # PREDICT PROBABILITY
    # =================================================

    probabilities = model.predict_proba(
        next_day
    )[0]

    classes = list(
        model.classes_
    )

    # =================================================
    # GET COMPLETION PROBABILITY
    # =================================================

    if 1 in classes:

        completed_index = classes.index(
            1
        )

        prediction = (
            probabilities[
                completed_index
            ] * 100
        )

    else:

        prediction = 0

    # =================================================
    # LIMIT RESULT
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