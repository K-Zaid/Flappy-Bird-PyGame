# leaderboard handling functions
import sqlite3

DB_FILE = "leaderboard.db"

def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS leaderboard (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            score INTEGER NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# add new score to leaderboard
def add_score(name, score):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('INSERT INTO leaderboard (name, score) VALUES (?, ?)', (name, score))
    conn.commit()
    conn.close()

def top_scores(limit=10):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('SELECT name, score FROM leaderboard ORDER BY score DESC LIMIT ?', (limit,))
    results = c.fetchall()
    conn.close()
    return results

