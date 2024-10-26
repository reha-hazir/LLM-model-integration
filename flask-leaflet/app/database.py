import sqlite3

def create_database():
    # Connect to the database
    conn = sqlite3.connect('./historical_figures.db')
    cursor = conn.cursor()

    # Create table for historical figures
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS figures (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE
        )
    ''')

    # Create table for attributes
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS attributes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            figure_id INTEGER,
            attribute_name TEXT,
            attribute_value TEXT,
            FOREIGN KEY (figure_id) REFERENCES figures(id),
            UNIQUE(figure_id, attribute_name)  -- Prevent duplicate attributes for the same figure
        )
    ''')

    # Commit changes and close the connection
    conn.commit()
    conn.close()

def insert_figure(name, attributes):
    # Connect to the database
    conn = sqlite3.connect('historical_figures.db')
    cursor = conn.cursor()

    try:
        # Insert the figure into the figures table
        cursor.execute('INSERT INTO figures (name) VALUES (?)', (name,))
        figure_id = cursor.lastrowid  # Get the id of the inserted figure

        # Insert attributes into the attributes table
        for attr_name, attr_value in attributes.items():
            cursor.execute('''
                INSERT INTO attributes (figure_id, attribute_name, attribute_value)
                VALUES (?, ?, ?)
            ''', (figure_id, attr_name, attr_value))

        # Commit changes
        conn.commit()
    except sqlite3.IntegrityError:
        print(f"Figure '{name}' already exists in the database.")
    finally:
        # Close the connection
        conn.close()

def main():
    # Create the database and tables
    create_database()

if __name__ == '__main__':
    main()
