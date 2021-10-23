from tkinter import *
import sqlite3

#Setup GUI 'screen'
root = Tk()
root.title("Welcome to Sales Database for Max's Clothing Store!")
root.geometry("450x600")

#Create a database and cursor then connect to the database
conn = sqlite3.connect('apparel_store.db') 
c = conn.cursor()

#Create table for apparel sales; sqlite's built in oid primary key will represent the product_id 

#c.execute("""CREATE TABLE apparel_sales (
#         product_name text,
#         category text,
#         colour text,
#         price_CAD integer,
#         units_sold integer)""")

#This function will update the record in the apparel database
def update():
    conn = sqlite3.connect('apparel_store.db') 
    c = conn.cursor()

    record_id = delete_box.get()
    c.execute("""UPDATE apparel_sales SET
        product_name = :product,
        category = :category,
        colour = :colour,
        price_CAD = :price,
        units_sold = :units

        WHERE oid = :oid""",
        {
        'product':product_editor.get(),
        'category':category_editor.get(),
        'colour':colour_editor.get(),
        'price':price_editor.get(),
        'units':units_editor.get(),

        'oid':record_id
        }
    )
    #Commit changes
    conn.commit()
    #Close connection
    conn.close()
    #Close window
    editor.destroy()

def edit():
    global editor
    editor = Tk()
    editor.title("Update a Record")
    editor.geometry("400x200")

    #Connect to database and create cursor
    conn = sqlite3.connect('apparel_store.db') 
    c = conn.cursor()

    record_id = delete_box.get()

    #Query the database (oid is the primary key sqlite makes for you)
    c.execute("SELECT * FROM apparel_sales WHERE oid = " + record_id)
    records = c.fetchall()

    # Create Global variables for text box names
    global product_editor
    global category_editor
    global colour_editor
    global price_editor
    global units_editor

    # Create text boxes
    product_editor = Entry(editor, width=30)
    product_editor.grid(row=0, column=1, padx=20, pady=(10, 0))
    category_editor = Entry(editor, width=30)
    category_editor.grid(row=1, column=1, padx=20)
    colour_editor = Entry(editor, width=30)
    colour_editor.grid(row=2, column=1, padx=20)
    price_editor = Entry(editor, width=30)
    price_editor.grid(row=3, column=1, padx=20)
    units_editor = Entry(editor, width=30)
    units_editor.grid(row=4, column=1, padx=20)

    # Create Text Box Labels
    product_label_editor = Label(editor, text='Product Name')
    product_label_editor.grid(row=0, column=0, pady=(10, 0))

    category_label_editor = Label(editor, text='Category')
    category_label_editor.grid(row=1, column=0)

    colour_label_editor = Label(editor, text='Colour')
    colour_label_editor.grid(row=2, column=0)

    price_label_editor = Label(editor, text='Price ($CAD)')
    price_label_editor.grid(row=3, column=0)

    units_label_editor = Label(editor, text='Units Sold')
    units_label_editor.grid(row=4, column=0)

    #Loop thru results
    for record in records:
        product_editor.insert(0, record[0])
        category_editor.insert(0, record[1])
        colour_editor.insert(0, record[2])
        price_editor.insert(0, record[3])
        units_editor.insert(0, record[4])

    # Create a save button to save edited record
    edit_btn = Button(editor, text='Save record', command=update)
    edit_btn.grid(row=5, column=0, columnspan=2, pady=10, padx=10, ipadx=145)


# Create function to delete a record
def delete():
    conn = sqlite3.connect('apparel_store.db') 
    c = conn.cursor()
    
    #Delete a record
    c.execute("DELETE from apparel_sales WHERE oid = " + delete_box.get())

    #Commit changes and close connection
    conn.commit()
    conn.close()

# Create Submit function for database
def submit():
    conn = sqlite3.connect('apparel_store.db') 
    c = conn.cursor()

    # Insert into table
    c.execute("INSERT INTO apparel_sales VALUES (:product, :category, :colour, :price, :units)",
        {
            'product': product.get(),
            'category': category.get(),
            'colour' : colour.get(),
            'price': price.get(),
            'units': units.get()
        })

    #Clear the text boxes
    product.delete(0, END)
    category.delete(0, END)
    colour.delete(0, END)
    price.delete(0, END)
    units.delete(0, END)

    #Commit changes and close connection
    conn.commit()
    conn.close()

# Create query function
def query():
    conn = sqlite3.connect('apparel_store.db') 
    c = conn.cursor()
    #Query the database (oid is the primary key sqlite makes for you)
    c.execute("SELECT *, oid FROM apparel_sales")
    records = c.fetchall()

    # Loop thru results
    print_records = ''
    for record in records:
        print_records += str(record[0]) + " " + str(record[2]) + "\t" + str(record[5]) + " " + "\n"

    query_label = Label(root, text=print_records)
    query_label.grid(row=13, column=0, columnspan=2)
    #Commit Changes and close connection
    conn.commit()
    conn.close()

# Create best seller function
def best_seller():
    conn = sqlite3.connect('apparel_store.db') 
    c = conn.cursor()
    c.execute("SELECT product_name, max(units_sold), oid FROM apparel_sales")
    best_seller = c.fetchall()
    print_best_seller = " The best selling item is: " + str(best_seller[0][0]) + " (product ID: " + str(best_seller[0][2]) + ") with " + str(best_seller[0][1]) + " units sold!"

    best_seller_label = Label(root, text=print_best_seller)
    best_seller_label.grid(row=12, column=0, columnspan=2)

    #Commit Changes and close connection
    conn.commit()
    conn.close() 

# Create text boxes
product = Entry(root, width=30)
product.grid(row=0, column=1, padx=20, pady=(10, 0))

category = Entry(root, width=30)
category.grid(row=1, column=1, padx=20)

colour = Entry(root, width=30)
colour.grid(row=2, column=1, padx=20)

price = Entry(root, width=30)
price.grid(row=3, column=1, padx=20)

units = Entry(root, width=30)
units.grid(row=4, column=1, padx=20)

delete_box = Entry(root, width=30)
delete_box.grid(row=8, column=1)


# Create Text Box Labels
product_label = Label(root, text='Product Name')
product_label.grid(row=0, column=0, pady=(10, 0))

category_label = Label(root, text='Category')
category_label.grid(row=1, column=0)

colour_label = Label(root, text='Colour')
colour_label.grid(row=2, column=0)

price_label = Label(root, text='Price ($CAD)')
price_label.grid(row=3, column=0)

units_label = Label(root, text='Units Sold')
units_label.grid(row=4, column=0)

delete_box_label = Label(root, text="Select Product ID")
delete_box_label.grid(row=8, column=0)

# Create Submit Button
submit_btn = Button(root, text='Add Record to Database', command=submit)
submit_btn.grid(row=5, column=0, columnspan=2, pady=10, padx=10, ipadx=100)

# Create query button
query_btn = Button(root, text='Show records', command=query)
query_btn.grid(row=6, column=0, columnspan=2, pady=10, padx=10, ipadx=137)

# Create delete button
delete_btn = Button(root, text='Delete record', command=delete)
delete_btn.grid(row=9, column=0, columnspan=2, pady=10, padx=10, ipadx=136)

# Create an update button
edit_btn = Button(root, text='Edit record', command=edit)
edit_btn.grid(row=10, column=0, columnspan=2, pady=10, padx=10, ipadx=143)

# Create a Best Seller button
best_seller_btn = Button(root, text='Best Seller', command=best_seller)
best_seller_btn.grid(row=11, column=0, columnspan=2, pady=10, padx=20, ipadx=143)

#Commit Changes
conn.commit()

#Close connection
conn.close()

#Loop for GUI
root.mainloop() 
  