import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from barcode_generation import generate_barcode  # Import barcode generation function
import datetime

# Create or connect to SQLite database
conn = sqlite3.connect('inventory.db')
cursor = conn.cursor()

# Function to view data
def view_data():
    def fetch_data():
        # Fetch all rows from the inventory table
        cursor.execute("SELECT * FROM inventory")
        rows = cursor.fetchall()
        return rows

    # Create a new window to display the data
    view_window = tk.Toplevel()
    view_window.title("Inventory Data")

    # Create a Treeview widget
    tree = ttk.Treeview(view_window, columns=("id", "barcode", "item_name", "date", "responsible_name", "expiration_date", "container_type", "deactive_datetime"), show="headings")

    # Define column headings
    tree.heading("id", text="ID")
    tree.heading("barcode", text="Barcode")
    tree.heading("item_name", text="Item Name")
    tree.heading("date", text="Date")
    tree.heading("responsible_name", text="Responsible Name")
    tree.heading("expiration_date", text="Expiration Date")
    tree.heading("container_type", text="Container Type")
    tree.heading("deactive_datetime", text="Deactive Datetime")

    # Define column widths
    for col in tree["columns"]:
        tree.column(col, width=150)

    # Insert data into the Treeview
    rows = fetch_data()
    for row in rows:
        tree.insert("", "end", values=row)

    # Place the Treeview in the window
    tree.pack(fill="both", expand=True)

import datetime
import tkinter as tk
from tkinter import messagebox

def add_item():
    def save_item():
        item_name = entry_item_name.get()
        date = entry_date.get()
        responsible_name = entry_responsible.get()
        expiration_date = entry_expiration.get()
        container_type = entry_container.get()

        if all([item_name, responsible_name, expiration_date, container_type]):
            # Generate a unique barcode based on item data
            barcode_data = f"{item_name}_{responsible_name}"
            unique_barcode = generate_barcode(barcode_data, folder_path="barcodes")

            # Save data to the database
            cursor.execute('''INSERT INTO inventory (barcode, item_name, date, responsible_name, expiration_date, container_type, deactive_datetime)
                              VALUES (?, ?, ?, ?, ?, ?, NULL)''',
                           (unique_barcode, item_name, date, responsible_name, expiration_date, container_type))
            conn.commit()

            messagebox.showinfo("Success", f"Item added successfully with barcode: {unique_barcode}")
            form_window.destroy()
        else:
            messagebox.showerror("Error", "All fields are required!")

    # Create the form window
    form_window = tk.Toplevel()
    form_window.title("Add Item")

    # Pre-fill the current timestamp
    current_timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Form fields
    tk.Label(form_window, text="Item Name").grid(row=0, column=0)
    entry_item_name = tk.Entry(form_window)
    entry_item_name.grid(row=0, column=1)

    tk.Label(form_window, text="Date").grid(row=1, column=0)
    entry_date = tk.Entry(form_window)
    entry_date.insert(0, current_timestamp)  # Insert current timestamp
    entry_date.config(state="disabled", disabledforeground="gray")  # Make it read-only and shady
    entry_date.grid(row=1, column=1)

    tk.Label(form_window, text="Responsible Name").grid(row=2, column=0)
    entry_responsible = tk.Entry(form_window)
    entry_responsible.grid(row=2, column=1)

    tk.Label(form_window, text="Expiration Date").grid(row=3, column=0)
    entry_expiration = tk.Entry(form_window)
    entry_expiration.grid(row=3, column=1)

    tk.Label(form_window, text="Container Type").grid(row=4, column=0)
    entry_container = tk.Entry(form_window)
    entry_container.grid(row=4, column=1)

    tk.Button(form_window, text="Save", command=save_item).grid(row=5, columnspan=2)


# Function to remove finished item
def remove_item():
    def remove_by_barcode():
        barcode = entry_barcode.get()
        if barcode:
            # Update deactive_datetime with the current timestamp
            current_timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            cursor.execute("UPDATE inventory SET deactive_datetime = ? WHERE barcode = ? AND deactive_datetime IS NULL",
                           (current_timestamp, barcode))
            conn.commit()

            if cursor.rowcount > 0:
                messagebox.showinfo("Success", f"Item with barcode {barcode} deactivated successfully!")
                remove_window.destroy()
            else:
                messagebox.showerror("Error", f"No active item found with barcode {barcode}.")
        else:
            messagebox.showerror("Error", "Please enter a barcode!")

    # Window to input barcode for removal
    remove_window = tk.Toplevel()
    remove_window.title("Remove Item")

    tk.Label(remove_window, text="Enter Barcode:").grid(row=0, column=0)
    entry_barcode = tk.Entry(remove_window)
    entry_barcode.grid(row=0, column=1)

    tk.Button(remove_window, text="Remove", command=remove_by_barcode).grid(row=1, columnspan=2)

# Main application window
def main_window():
    root = tk.Tk()
    root.title("Inventory Management System")

    tk.Label(root, text="Welcome to Inventory Management").grid(row=0, column=0, columnspan=3, pady=10)

    tk.Button(root, text="Add a New Item", command=add_item).grid(row=1, column=0, padx=10, pady=10)
    tk.Button(root, text="View Data", command=view_data).grid(row=1, column=1, padx=10, pady=10)
    tk.Button(root, text="Remove Finished Item", command=remove_item).grid(row=1, column=2, padx=10, pady=10)

    root.mainloop()

# Run the application
if __name__ == "__main__":
    main_window()
