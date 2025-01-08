import sqlite3

# Connect to the database
conn = sqlite3.connect('inventory.db')
cursor = conn.cursor()

# Create a new table with the correct schema
cursor.execute('''
CREATE TABLE IF NOT EXISTS inventory_temp (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    barcode TEXT,
    item_name TEXT,
    date DATETIME,
    responsible_name TEXT,
    expiration_date TEXT,
    container_type TEXT,
    deactive_datetime TEXT
)
''')

# Copy data from the old table to the new table
cursor.execute('''
INSERT INTO inventory_temp (id, barcode, item_name, date, responsible_name, expiration_date, container_type, deactive_datetime)
SELECT id, barcode, item_name, date, responsible_name, expiration_date, container_type, deactive_datetime
FROM inventory
''')

# Commit changes
conn.commit()

# Rename the old table and the new table
cursor.execute("ALTER TABLE inventory RENAME TO inventory_old")
cursor.execute("ALTER TABLE inventory_temp RENAME TO inventory")

# Drop the old table
cursor.execute("DROP TABLE inventory_old")

# Commit changes and close the connection
conn.commit()
conn.close()

print("Successfully converted the 'date' column to DATETIME type.")
