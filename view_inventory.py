import sqlite3

# Connect to the database
conn = sqlite3.connect('inventory.db')
cursor = conn.cursor()

# Fetch all rows from the inventory table
cursor.execute("SELECT * FROM inventory")
rows = cursor.fetchall()

# Print the data in a readable format
if rows:
    print(f"{'ID':<5} {'Barcode':<30} {'Item Name':<20} {'Date':<15} {'Responsible Name':<20} {'Expiration Date':<15} {'Container Type':<15}")
    print("=" * 130)
    for row in rows:
        print(f"{row[0]:<5} {row[1]:<30} {row[2]:<20} {row[3]:<15} {row[4]:<20} {row[5]:<15} {row[6]:<15}")
else:
    print("No data found in the inventory table.")

# Close the connection
conn.close()
