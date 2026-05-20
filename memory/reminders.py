from datetime import datetime
from database.db import get_connection


# =====================================
# ADD REMINDER
# =====================================
def add_reminder(
    reminder_text,
    trigger_time
):
    """
    Adds a reminder to the database.
    
    trigger_time format:
    YYYY-MM-DD HH:MM:SS
    """

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO reminders (
        reminder_text,
        trigger_time
    )
    VALUES (?, ?)
    """, (
        reminder_text,
        trigger_time
    ))

    conn.commit()
    conn.close()


# =====================================
# GET DUE REMINDERS
# =====================================
def get_due_reminders():
    """
    Returns reminders that are due.
    """

    conn = get_connection()
    cursor = conn.cursor()

    current_time = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    cursor.execute("""
    SELECT *
    FROM reminders
    WHERE completed = 0
    AND trigger_time <= ?
    ORDER BY trigger_time ASC
    """, (current_time,))

    reminders = cursor.fetchall()

    conn.close()

    return reminders


# =====================================
# MARK REMINDER AS COMPLETED
# =====================================
def complete_reminder(reminder_id):
    """
    Marks a reminder as completed.
    """

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    UPDATE reminders
    SET completed = 1
    WHERE id = ?
    """, (reminder_id,))

    conn.commit()
    conn.close()


# =====================================
# GET ALL REMINDERS
# =====================================
def get_all_reminders():
    """
    Returns all reminders.
    """

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT *
    FROM reminders
    ORDER BY trigger_time ASC
    """)

    reminders = cursor.fetchall()

    conn.close()

    return reminders


# =====================================
# DELETE REMINDER
# =====================================
def delete_reminder(reminder_id):
    """
    Deletes a reminder by ID.
    """

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    DELETE FROM reminders
    WHERE id = ?
    """, (reminder_id,))

    conn.commit()
    conn.close()