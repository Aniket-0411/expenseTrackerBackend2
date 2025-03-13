import sqlite3, csv

conn = sqlite3.connect("mydb.db")
c = conn.cursor()

c.execute("DROP TABLE IF EXISTS finance")
c.execute("""
    CREATE TABLE finance (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date DATE,
        transaction_Description TEXT,
        category VARCHAR(255) NOT NULL,
        amount REAL NOT NULL,
        type VARCHAR(255) NOT NULL,
        user_id INTEGER default 1
    )
""")

with open("c:\\Users\\yffan\\Documents\\VScodeProject\\Web\\expense-tracker\\django-backend\\Personal_Finance_Dataset.csv", newline='', encoding="utf-8") as csvfile:
    reader = csv.reader(csvfile)
    next(reader)  # skip header row
    for row in reader:
        c.execute("INSERT INTO finance (Date, Transaction_Description, Category, Amount, type) VALUES (?,?,?,?,?)", row)
conn.commit()

c.execute("SELECT * FROM finance")
rows = c.fetchall()
conn.close()