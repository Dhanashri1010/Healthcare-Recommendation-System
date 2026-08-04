"""
Database Operations Manager Module
----------------------------------
Manages SQLite database initialization, user registration, credentials authentication,
and secure password hashing using PBKDF2-SHA256.
"""

import sqlite3
import hashlib
import os

DB_FILE = "healthcare_users.db"

def init_db():
    """Initializes the database and creates the users and predictions tables if they do not exist."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS predictions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            symptoms TEXT NOT NULL,
            disease TEXT NOT NULL,
            medicines TEXT NOT NULL,
            confidence REAL NOT NULL
        )
    """)
    conn.commit()
    conn.close()

def hash_password(password: str) -> str:
    """Hashes a password using PBKDF2-SHA256 with a random 16-byte salt."""
    salt = os.urandom(16)
    hash_name = 'sha256'
    iterations = 100000
    derived_key = hashlib.pbkdf2_hmac(hash_name, password.encode('utf-8'), salt, iterations)
    return f"{salt.hex()}:{derived_key.hex()}"

def verify_password(stored_password: str, provided_password: str) -> bool:
    """Verifies a password against its PBKDF2-SHA256 hashed representation."""
    try:
        salt_hex, key_hex = stored_password.split(':')
        salt = bytes.fromhex(salt_hex)
        hash_name = 'sha256'
        iterations = 100000
        derived_key = hashlib.pbkdf2_hmac(hash_name, provided_password.encode('utf-8'), salt, iterations)
        return derived_key.hex() == key_hex
    except Exception:
        return False

def register_user(username: str, email: str, password: str) -> tuple[bool, str]:
    """Registers a new user in the SQLite database. Returns (success, message)."""
    init_db()
    
    username_clean = username.strip()
    email_clean = email.strip().lower()
    
    if not username_clean:
        return False, "Username cannot be empty."
    if not email_clean:
        return False, "Email cannot be empty."
    if not password:
        return False, "Password cannot be empty."
        
    hashed = hash_password(password)
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO users (username, email, password) VALUES (?, ?, ?)",
            (username_clean, email_clean, hashed)
        )
        conn.commit()
        return True, "User registered successfully!"
    except sqlite3.IntegrityError as e:
        error_msg = str(e).lower()
        if "username" in error_msg:
            return False, "Username already exists."
        elif "email" in error_msg:
            return False, "Email already exists."
        else:
            return False, "Username or Email already exists."
    except Exception as e:
        return False, f"An error occurred: {str(e)}"
    finally:
        conn.close()

def authenticate_user(username_or_email: str, password: str) -> tuple[bool, dict | str]:
    """Verifies user credentials. Returns (success, user_dict_or_error_msg)."""
    init_db()
    
    user_input = username_or_email.strip()
    
    if not user_input or not password:
        return False, "Username/Email and Password are required."
        
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    try:
        # Check by username or email
        cursor.execute(
            "SELECT username, email, password FROM users WHERE username = ? OR email = ?",
            (user_input, user_input.lower())
        )
        row = cursor.fetchone()
        if row:
            db_username, db_email, db_password = row
            if verify_password(db_password, password):
                return True, {"username": db_username, "email": db_email}
        return False, "Invalid username/email or password."
    except Exception as e:
        return False, f"An error occurred: {str(e)}"
    finally:
        conn.close()

def save_prediction(username: str, symptoms: str, disease: str, medicines: str, confidence: float) -> tuple[bool, str]:
    """Saves a prediction record to the predictions table. Returns (success, message)."""
    init_db()
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO predictions (username, symptoms, disease, medicines, confidence)
            VALUES (?, ?, ?, ?, ?)
        """, (username, symptoms, disease, medicines, confidence))
        conn.commit()
        return True, "Prediction logged successfully."
    except Exception as e:
        return False, f"Failed to log prediction: {str(e)}"
    finally:
        conn.close()

def get_user_predictions(username: str) -> list[tuple]:
    """Retrieves all predictions for a specific user, ordered by timestamp descending."""
    init_db()
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    try:
        cursor.execute("""
            SELECT id, timestamp, symptoms, disease, medicines, confidence
            FROM predictions
            WHERE username = ?
            ORDER BY timestamp DESC, id DESC
        """, (username,))
        rows = cursor.fetchall()
        return rows
    except Exception:
        return []
    finally:
        conn.close()

def delete_prediction(prediction_id: int, username: str) -> tuple[bool, str]:
    """Deletes a specific prediction record ensuring it belongs to the logged-in user."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    try:
        cursor.execute("""
            DELETE FROM predictions
            WHERE id = ? AND username = ?
        """, (prediction_id, username))
        conn.commit()
        if cursor.rowcount > 0:
            return True, "Prediction deleted."
        return False, "Record not found or access denied."
    except Exception as e:
        return False, f"Error deleting prediction: {str(e)}"
    finally:
        conn.close()

def clear_user_history(username: str) -> tuple[bool, str]:
    """Deletes all prediction records for the logged-in user."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    try:
        cursor.execute("""
            DELETE FROM predictions
            WHERE username = ?
        """, (username,))
        conn.commit()
        return True, "Prediction history cleared."
    except Exception as e:
        return False, f"Error clearing history: {str(e)}"
    finally:
        conn.close()
