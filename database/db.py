import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent / "tina.db"


def get_connection():
    """
    Create and return a database connection.
    JARVIS-optimized SQLite setup.
    """
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row

    # AI performance optimizations
    conn.execute("PRAGMA foreign_keys = ON")
    conn.execute("PRAGMA journal_mode = WAL")
    conn.execute("PRAGMA synchronous = NORMAL")
    conn.execute("PRAGMA temp_store = MEMORY")

    return conn


def init_db():
    """
    Initialize all JARVIS-level memory systems.
    """

    with get_connection() as conn:
        cursor = conn.cursor()

        # ====================================
        # USER PROFILE
        # ====================================
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_profile (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            nickname TEXT,
            occupation TEXT,
            email TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)

        # ====================================
        # MEMORIES (JARVIS LEVEL 2 CORE)
        # ====================================
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS memories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            content TEXT NOT NULL,
            category TEXT DEFAULT 'general',
            importance INTEGER DEFAULT 5,

            -- JARVIS UPGRADE FIELDS
            hash TEXT UNIQUE,
            embedding TEXT,

            last_accessed TIMESTAMP,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)

        # ====================================
        # CONVERSATIONS (SESSION AWARE)
        # ====================================
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS conversations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id TEXT,
            role TEXT NOT NULL,
            message TEXT NOT NULL,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)

        # ====================================
        # TASKS
        # ====================================
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            status TEXT DEFAULT 'pending',
            priority INTEGER DEFAULT 3,
            due_date TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)

        # ====================================
        # REMINDERS
        # ====================================
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS reminders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            reminder_text TEXT NOT NULL,
            trigger_time TEXT NOT NULL,
            completed INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)

        # ====================================
        # CONTACTS
        # ====================================
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS contacts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            phone TEXT,
            email TEXT,
            notes TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)

        # ====================================
        # DEVICES
        # ====================================
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS devices (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            device_name TEXT NOT NULL,
            device_type TEXT,
            status TEXT DEFAULT 'offline',
            last_seen TIMESTAMP,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)

        # ====================================
        # SKILLS
        # ====================================
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS skills (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL,
            description TEXT,
            enabled INTEGER DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)

        # ====================================
        # EVENTS (EPISODIC BASE)
        # ====================================
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            location TEXT,
            start_time TEXT,
            end_time TEXT,
            notes TEXT,
            importance INTEGER DEFAULT 5,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)

        # ====================================
        # NOTIFICATIONS
        # ====================================
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS notifications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            body TEXT,
            is_read INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)

        # ====================================
        # SETTINGS (JARVIS CONFIG SYSTEM)
        # ====================================
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS settings (
            key TEXT PRIMARY KEY,
            value TEXT
        )
        """)

        # ====================================
        # SHORT-TERM MEMORY (CONTEXT CACHE)
        # ====================================
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS short_term_memory (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id TEXT,
            content TEXT NOT NULL,
            role TEXT DEFAULT 'user',
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)

        # ====================================
        # EPISODIC MEMORY (EVENTS / EXPERIENCES)
        # ====================================
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS episodic_memory (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            event_title TEXT,
            event_description TEXT,
            event_time TIMESTAMP,
            importance INTEGER DEFAULT 5,
            embedding TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)

        # ====================================
        # SEMANTIC MEMORY (FACT KNOWLEDGE)
        # ====================================
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS semantic_memory (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            subject TEXT NOT NULL,
            fact TEXT NOT NULL,
            confidence REAL DEFAULT 1.0,
            embedding TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)

        # ====================================
        # DEFAULT SETTINGS (JARVIS CORE IDENTITY)
        # ====================================
        cursor.execute("""
        INSERT OR IGNORE INTO settings (key, value)
        VALUES ('assistant_name', 'Tina')
        """)

        cursor.execute("""
        INSERT OR IGNORE INTO settings (key, value)
        VALUES ('wake_word', 'Tina')
        """)

        cursor.execute("""
        INSERT OR IGNORE INTO settings (key, value)
        VALUES ('voice_enabled', 'true')
        """)

        cursor.execute("""
        INSERT OR IGNORE INTO settings (key, value)
        VALUES ('theme', 'dark')
        """)

        conn.commit()

    print("✅ Tina database initialized successfully.")


if __name__ == "__main__":
    init_db()