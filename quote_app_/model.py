import sqlite3

def init_db():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()

    # Create tables first
    c.execute('''CREATE TABLE IF NOT EXISTS quotes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        text TEXT NOT NULL,
        author TEXT NOT NULL
    )''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL
    )''')

    # Now safe to delete duplicates
    c.execute("""
DELETE FROM quotes
WHERE id NOT IN (
    SELECT MIN(id)
    FROM quotes
    GROUP BY text, author
)
""")

    # Insert sample quotes only if table is empty
    c.execute("SELECT COUNT(*) FROM quotes")
    if c.fetchone()[0] == 0:
        c.executemany("INSERT INTO quotes (text, author) VALUES (?, ?)", [
            ("Believe you can and you're halfway there.", "Theodore Roosevelt"),
            ("The best way to get started is to quit talking and begin doing.", "Walt Disney"),
            ("Your time is limited, so don’t waste it living someone else’s life.", "Steve Jobs"),
            ("To be, or not to be, that is the question.", "William Shakespeare"),
            ("Be kind, for everyone you meet is fighting a hard battle.","Plato"),
            ("One cannot think well, love well, sleep well, if one has not dined well.","Virginia Woolf"),
            ("The only way to do great work is to love what you do.", "Steve Jobs"),
            ("Life is what happens when you're busy making other plans.", "John Lennon"),
            ("Get busy living or get busy dying.", "Stephen King"),
            ("You have within you right now, everything you need to deal with whatever the world can throw at you.", "Brian Tracy"),
            ("Act as if what you do makes a difference. It does.", "William James"),
            ("Success is not final, failure is not fatal: It is the courage to continue that counts.", "Winston Churchill"),
            ("The only limit to our realization of tomorrow will be our doubts of today.", "Franklin D. Roosevelt"),
            ("The future belongs to those who believe in the beauty of their dreams.", "Eleanor Roosevelt"),
            ("It does not matter how slowly you go as long as you do not stop.", "Confucius"),
            ("Everything you've ever wanted is on the other side of fear.", "George Addair"),
            ("Opportunities don't happen, you create them.", "Chris Grosser"),
        ])

    conn.commit()
    conn.close()

if __name__ == '__main__':
    init_db()
    print("Database and tables created, sample quotes inserted.")