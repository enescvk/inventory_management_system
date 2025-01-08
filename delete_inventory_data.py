import sqlite3

# Connect to the database
conn = sqlite3.connect('inventory.db')
cursor = conn.cursor()

# Confirm deletion
confirm = input("Are you sure you want to delete all records in the inventory table? (yes/no): ")
if confirm.lower() == "yes":
    # Delete all records
    cursor.execute("DELETE FROM inventory")
    conn.commit()
    print("All records in the inventory table have been deleted.")
else:
    print("Operation cancelled.")

# Close the connection
conn.close()
