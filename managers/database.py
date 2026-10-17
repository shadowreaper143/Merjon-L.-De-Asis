import mysql.connector
import hashlib
import hmac
import os


class DatabaseManager:
    def __init__(self, host="localhost", port=3306, user="root", password="", database="space_invaders_db"):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.database = database
        self.initialize_database()

    def connect_server(self):
        return mysql.connector.connect(host=self.host, port=self.port, user=self.user, password=self.password)

    def connect(self):
        return mysql.connector.connect(host=self.host, port=self.port, user=self.user, password=self.password, database=self.database)

    def initialize_database(self):
        connection = None
        cursor = None
        try:
            connection = self.connect_server()
            cursor = connection.cursor(buffered=True)
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS `{self.database}`")
            connection.commit()
            cursor.close(); cursor = None
            connection.close(); connection = None

            connection = self.connect()
            cursor = connection.cursor(buffered=True)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS players (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    username VARCHAR(50) NOT NULL UNIQUE,
                    password_hash VARCHAR(255) NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS scores (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    player_id INT NOT NULL,
                    score INT NOT NULL DEFAULT 0,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (player_id) REFERENCES players(id) ON DELETE CASCADE
                )
            """)
            connection.commit()
            print("Database initialized successfully.")
        except mysql.connector.Error as error:
            print("Database initialization error:", error)
        finally:
            if cursor is not None:
                try: cursor.close()
                except mysql.connector.Error: pass
            if connection is not None:
                try: connection.close()
                except mysql.connector.Error: pass

    def hash_password(self, password):
        iterations = 200000
        salt = os.urandom(16)
        digest = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, iterations)
        return f"pbkdf2_sha256${iterations}${salt.hex()}${digest.hex()}"

    def verify_password(self, password, stored_hash):
        try:
            algorithm, iterations, salt_hex, digest_hex = stored_hash.split("$")
            if algorithm != "pbkdf2_sha256":
                return False
            iterations = int(iterations)
            salt = bytes.fromhex(salt_hex)
            stored = bytes.fromhex(digest_hex)
            actual = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, iterations)
            return hmac.compare_digest(actual, stored)
        except Exception:
            return False

    def register_player(self, username, password):
        connection = None
        cursor = None
        try:
            username = username.strip()
            if len(username) < 3:
                return False, "Username must be at least 3 characters."
            if len(password) < 6:
                return False, "Password must be at least 6 characters."

            connection = self.connect()
            cursor = connection.cursor(buffered=True)
            cursor.execute("SELECT id FROM players WHERE username=%s LIMIT 1", (username,))
            if cursor.fetchone() is not None:
                return False, "Username already exists."

            cursor.execute(
                "INSERT INTO players (username, password_hash) VALUES (%s, %s)",
                (username, self.hash_password(password))
            )
            connection.commit()
            return True, cursor.lastrowid
        except mysql.connector.IntegrityError:
            return False, "Username already exists."
        except mysql.connector.Error as error:
            print("Registration error:", error)
            return False, str(error)
        finally:
            if cursor is not None:
                try: cursor.close()
                except mysql.connector.Error: pass
            if connection is not None:
                try: connection.close()
                except mysql.connector.Error: pass

    def authenticate_player(self, username, password):
        connection = None
        cursor = None
        try:
            connection = self.connect()
            cursor = connection.cursor(dictionary=True, buffered=True)
            cursor.execute("SELECT id, username, password_hash FROM players WHERE username=%s LIMIT 1", (username.strip(),))
            player = cursor.fetchone()
            if player is None or not self.verify_password(password, player["password_hash"]):
                return None
            return {"id": player["id"], "username": player["username"]}
        except mysql.connector.Error as error:
            print("Authentication error:", error)
            return None
        finally:
            if cursor is not None:
                try: cursor.close()
                except mysql.connector.Error: pass
            if connection is not None:
                try: connection.close()
                except mysql.connector.Error: pass

    def username_exists(self, username):
        connection = None
        cursor = None
        try:
            connection = self.connect()
            cursor = connection.cursor(buffered=True)
            cursor.execute("SELECT id FROM players WHERE username=%s LIMIT 1", (username.strip(),))
            return cursor.fetchone() is not None
        except mysql.connector.Error:
            return False
        finally:
            if cursor is not None:
                try: cursor.close()
                except mysql.connector.Error: pass
            if connection is not None:
                try: connection.close()
                except mysql.connector.Error: pass

    def save_score(self, player_id, score):
        connection = None
        cursor = None
        try:
            connection = self.connect()
            cursor = connection.cursor(buffered=True)
            cursor.execute("INSERT INTO scores (player_id, score) VALUES (%s, %s)", (player_id, int(score)))
            connection.commit()
            return True
        except mysql.connector.Error as error:
            print("Save score error:", error)
            return False
        finally:
            if cursor is not None:
                try: cursor.close()
                except mysql.connector.Error: pass
            if connection is not None:
                try: connection.close()
                except mysql.connector.Error: pass

    def get_leaderboard(self, limit=10):
        connection = None
        cursor = None
        try:
            limit = max(1, min(int(limit), 100))
            connection = self.connect()
            cursor = connection.cursor(dictionary=True, buffered=True)
            cursor.execute(f"""
                SELECT p.username, MAX(s.score) AS score
                FROM players p
                INNER JOIN scores s ON p.id=s.player_id
                GROUP BY p.id, p.username
                ORDER BY score DESC
                LIMIT {limit}
            """)
            return cursor.fetchall()
        except mysql.connector.Error as error:
            print("Leaderboard error:", error)
            return []
        finally:
            if cursor is not None:
                try: cursor.close()
                except mysql.connector.Error: pass
            if connection is not None:
                try: connection.close()
                except mysql.connector.Error: pass

    def get_player_scores(self, player_id):
        connection = None
        cursor = None
        try:
            connection = self.connect()
            cursor = connection.cursor(dictionary=True, buffered=True)
            cursor.execute("SELECT id, score, created_at FROM scores WHERE player_id=%s ORDER BY score DESC", (player_id,))
            return cursor.fetchall()
        except mysql.connector.Error as error:
            print("Player scores error:", error)
            return []
        finally:
            if cursor is not None:
                try: cursor.close()
                except mysql.connector.Error: pass
            if connection is not None:
                try: connection.close()
                except mysql.connector.Error: pass
