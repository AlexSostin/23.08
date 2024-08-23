import sqlite3

# Connect to the SQLite3 database (it will create the file if it doesn't exist)
conn = sqlite3.connect('pets.db')
cursor = conn.cursor()

# Create a table for pets
cursor.execute('''
    CREATE TABLE IF NOT EXISTS pets (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        age INTEGER NOT NULL,
        picture_url TEXT
    )
''')

# Insert sample data into the pets table
cursor.executemany('''
    INSERT INTO pets (id, name, age, picture_url)
    VALUES (?, ?, ?, ?)
''', [
    (1, 'Dog 1', 3, 'https://www.pexels.com/uk-ua/photo/1805164/'),
    (2, 'Dog 2', 4, 'https://unsplash.com/photos/shallow-focus-photography-of-white-shih-tzu-puppy-running-on-the-grass-qO-PIF84Vxg'),
    (3, 'Dog 3', 5, 'https://unsplash.com/photos/selective-focus-photography-of-golden-labrador-retriever-pgUbpDLJh3E'),
    (4, 'Dog 4', 2, 'https://unsplash.com/photos/a-close-up-of-a-dog-with-its-tongue-out-E79-DwPNiMo'),
    (5, 'Dog 5', 6, 'https://unsplash.com/photos/short-coated-tan-and-white-dog-lying-on-teal-surface-i2DefZ6PCN0')
])

# Commit the changes and close the connection
conn.commit()
conn.close()
