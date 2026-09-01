import sqlite3

# =====================================================
# DATABASE
# =====================================================

conn = sqlite3.connect("habit_tracker.db")
cursor = conn.cursor()

# =====================================================
# TARGET HABIT
# =====================================================

habit_id = 11

# =====================================================
# SHOW RECORDS BEFORE DELETE
# =====================================================

cursor.execute(
    """
    SELECT id, completed_date, completed
    FROM progress
    WHERE habit_id = ?
    ORDER BY completed_date
    """,
    (habit_id,)
)

records = cursor.fetchall()

print("Records that will be deleted:")

for record in records:
    status = "Completed" if record[2] == 1 else "Missed"
    print(
        f"ID: {record[0]} | "
        f"Date: {record[1]} | "
        f"Status: {status}"
    )

# =====================================================
# DELETE ONLY PROGRESS RECORDS
# =====================================================

cursor.execute(
    """
    DELETE FROM progress
    WHERE habit_id = ?
    """,
    (habit_id,)
)

# =====================================================
# RESET HABIT STATUS
# =====================================================

cursor.execute(
    """
    UPDATE habits
    SET status = 'Pending'
    WHERE id = ?
    """,
    (habit_id,)
)

conn.commit()

# =====================================================
# VERIFY
# =====================================================

cursor.execute(
    """
    SELECT COUNT(*)
    FROM progress
    WHERE habit_id = ?
    """,
    (habit_id,)
)

remaining = cursor.fetchone()[0]

# Check that the habit still exists
cursor.execute(
    """
    SELECT id, habit_name, status
    FROM habits
    WHERE id = ?
    """,
    (habit_id,)
)

habit = cursor.fetchone()

conn.close()

print()
print("========================================")
print("✅ CLEANUP COMPLETED")
print("========================================")

print(f"Remaining progress records: {remaining}")

if habit:
    print(
        f"Habit still exists: "
        f"{habit[1]} (ID {habit[0]})"
    )
    print(f"Status: {habit[2]}")
else:
    print("❌ Habit was not found.")
    