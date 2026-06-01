from datetime import datetime
from database.db import get_connection


# =====================================================
# ADD REMINDER
# =====================================================

def add_reminder(reminder_text, trigger_time):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO reminders (
            reminder_text,
            trigger_time
        )
        VALUES (?, ?)
    """, (reminder_text, trigger_time))

    conn.commit()
    conn.close()


# =====================================================
# GET DUE REMINDERS
# =====================================================

def get_due_reminders():

    conn = get_connection()
    cursor = conn.cursor()

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    cursor.execute("""
        SELECT *
        FROM reminders
        WHERE completed = 0
        AND trigger_time <= ?
        ORDER BY trigger_time ASC
    """, (now,))

    rows = cursor.fetchall()
    conn.close()

    return rows


# =====================================================
# MARK COMPLETE
# =====================================================

def complete_reminder(reminder_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE reminders
        SET completed = 1
        WHERE id = ?
    """, (reminder_id,))

    conn.commit()
    conn.close()


# =====================================================
# DELETE REMINDER
# =====================================================

def delete_reminder(reminder_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM reminders
        WHERE id = ?
    """, (reminder_id,))

    conn.commit()
    conn.close()


# =====================================================
# GET ALL REMINDERS
# =====================================================

def get_all_reminders():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM reminders
        ORDER BY trigger_time ASC
    """)

    rows = cursor.fetchall()
    conn.close()

    return rows