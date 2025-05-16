# import modules 
from tkcalendar import DateEntry
from tkinter import *
from tkinter import ttk
import datetime as dt
from mydb import *
from tkinter import messagebox

# object for database
data = Database(db='expense_record.db')

# Create table if not exists
data.cur.execute("""
CREATE TABLE IF NOT EXISTS expense_record (
    item_name TEXT,
    item_price REAL,
    purchase_date TEXT
);
""")
data.conn.commit()
# import modules 
from tkinter import *
from tkinter import ttk
import datetime as dt
from mydb import *
from tkinter import messagebox

# object for database
data = Database(db='expense_record.db')

# global variables
count = 0
selected_rowid = 0


def fetch_records():
    f = data.fetchRecord('select rowid, * from expense_record')
    global count
    for rec in f:
        tv.insert(parent='', index='0', iid=count, values=(rec[0], rec[1], rec[2], rec[3]))
        count += 1
    tv.after(400, refreshData)

def select_record(event):
    global selected_rowid
    selected = tv.focus()    
    val = tv.item(selected, 'values')
  
    try:
        selected_rowid = val[0]
        d = val[3]
        namevar.set(val[1])
        amtvar.set(val[2])
        dopvar.set(str(d))
    except Exception as ep:
        pass

def refreshData():
    for item in tv.get_children():
      tv.delete(item)
    fetch_records()
    
# global variables
count = 0
selected_rowid = 0

# functions
def saveRecord():
    global data
    data.insertRecord(item_name=item_name.get(), item_price=item_amt.get(), purchase_date=transaction_date.get())
       
def setDate():
    date = dt.datetime.now()
    dopvar.set(f'{date:%d %B %Y}')

def clearEntries():
    item_name.delete(0, 'end')
    item_amt.delete(0, 'end')
    transaction_date.delete(0, 'end')

def fetch_records():
    f = data.fetchRecord('select rowid, * from expense_record')
    global count
    for rec in f:
        tv.insert(parent='', index='0', iid=count, values=(rec[0], rec[1], rec[2], rec[3]))
        count += 1
    tv.after(400, refreshData)

def select_record(event):
    global selected_rowid
    selected = tv.focus()    
    val = tv.item(selected, 'values')
  
    try:
        selected_rowid = val[0]
        d = val[3]
        namevar.set(val[1])
        amtvar.set(val[2])
        dopvar.set(str(d))
    except Exception as ep:
        pass


def update_record():
    global selected_rowid

    if not selected_rowid:
        messagebox.showerror("Error", "No record selected!")
        return

    selected = tv.focus()
    try:
        data.updateRecord(namevar.get(), amtvar.get(), dopvar.get(), selected_rowid)
        tv.item(selected, text="", values=(namevar.get(), amtvar.get(), dopvar.get()))
    except Exception as ep:
        messagebox.showerror('Error', ep)

    # Clear entry boxes
    item_name.delete(0, END)
    item_amt.delete(0, END)
    transaction_date.delete(0, END)
    tv.after(400, refreshData)
    
def totalBalance():
    budget = data.fetchRecord("SELECT amount FROM budget LIMIT 1")
    expenses = data.fetchRecord("SELECT sum(item_price) FROM expense_record")[0][0] or 0
    
    if budget:
        budget = budget[0][0]
        messagebox.showinfo('Balance', f"Budget: ₹{budget}\nTotal Spent: ₹{expenses}\nRemaining: ₹{budget - expenses}")
    else:
        messagebox.showwarning('Warning', 'Please set budget first!')

def refreshData():
    for item in tv.get_children():
      tv.delete(item)
    fetch_records()
    
def deleteRow():
    global selected_rowid
    data.removeRecord(selected_rowid)
    refreshData()

def set_budget():
    budget_dialog = Toplevel(ws)
    budget_dialog.title('Set Budget')
    
    Label(budget_dialog, text="Monthly Budget:", font=f).pack(pady=5)
    budget_entry = Entry(budget_dialog, font=f)
    budget_entry.pack(pady=5)
    
    Button(budget_dialog, text="Save", command=lambda: save_budget(budget_entry.get(), budget_dialog)).pack(pady=5)

def save_budget(amount, dialog):
    try:
        data.cur.execute("CREATE TABLE IF NOT EXISTS budget (amount REAL)")
        data.cur.execute("DELETE FROM budget")  # Single record system
        data.cur.execute("INSERT INTO budget VALUES (?)", (float(amount),))
        data.conn.commit()
        dialog.destroy()
    except ValueError:
        messagebox.showerror("Error", "Invalid budget amount")

# create tkinter object
ws = Tk()
ws.title('Daily Expenses')

# variables
f = ('Times new roman', 14)
namevar = StringVar()
amtvar = IntVar()
dopvar = StringVar()

# Frame widget
f2 = Frame(ws)
f2.pack() 

f1 = Frame(
    ws,
    padx=10,
    pady=10,
)
f1.pack(expand=True, fill=BOTH)


# Label widget
Label(f1, text='ITEM NAME', font=f).grid(row=0, column=0, sticky=W)
Label(f1, text='ITEM PRICE', font=f).grid(row=1, column=0, sticky=W)
Label(f1, text='PURCHASE DATE', font=f).grid(row=2, column=0, sticky=W)

# Entry widgets 
item_name = Entry(f1, font=f, textvariable=namevar)
item_amt = Entry(f1, font=f, textvariable=amtvar)
transaction_date = DateEntry(f1, font=f, textvariable=dopvar, date_pattern='d/m/y')

# Entry grid placement
item_name.grid(row=0, column=1, sticky=EW, padx=(10, 0))
item_amt.grid(row=1, column=1, sticky=EW, padx=(10, 0))
transaction_date.grid(row=2, column=1, sticky=EW, padx=(10, 0))


# Action buttons
cur_date = Button(
    f1, 
    text='Current Date', 
    font=f, 
    bg='#04C4D9', 
    command= setDate,
    width=15
    )

submit_btn = Button(
    f1, 
    text='Save Record',
    font=f, 
    command=saveRecord, 
    bg='#42602D', 
    fg='white'
    )

clr_btn = Button(
    f1, 
    text='Clear Entry', 
    font=f, 
    command=clearEntries, 
    bg='#D9B036', 
    fg='white'
    )

quit_btn = Button(
    f1, 
    text='Exit', 
    font=f, 
    command=lambda:ws.destroy(), 
    bg='#D33532', 
    fg='white'
    )

total_bal = Button(
    f1,
    text='Total Balance',
    font=f,
    bg='#486966',
    command=totalBalance
)

total_spent = Button(
    f1,
    text='Total Spent',
    font=f,
    command=lambda: messagebox.showinfo("Total Spent", f"₹{data.fetchRecord('SELECT SUM(item_price) FROM expense_record')[0][0] or 0}")
)

update_btn = Button(
    f1, 
    text='Update',
    bg='#C2BB00',
    command=update_record,
    font=f
)

del_btn = Button(
    f1, 
    text='Delete',
    bg='#BD2A2E',
    command=deleteRow,
    font=f
)

budget_btn = Button(
    f1,
    text='Set Budget',
    font=f,
    command=set_budget,
    bg='#2E5D42',
    fg='white'
)
budget_btn.grid(row=3, column=3, sticky=EW, padx=(10, 0))

# grid placement
cur_date.grid(row=3, column=1, sticky=EW, padx=(10, 0))
submit_btn.grid(row=0, column=2, sticky=EW, padx=(10, 0))
clr_btn.grid(row=1, column=2, sticky=EW, padx=(10, 0))
quit_btn.grid(row=2, column=2, sticky=EW, padx=(10, 0))
total_bal.grid(row=0, column=3, sticky=EW, padx=(10, 0))
update_btn.grid(row=1, column=3, sticky=EW, padx=(10, 0))
del_btn.grid(row=2, column=3, sticky=EW, padx=(10, 0))

# Treeview widget
tv = ttk.Treeview(f2, columns=(1, 2, 3, 4), show="headings", height=8)
tv.pack(side="left", fill="both", expand=True)

# Vertical scrollbar
scrollbar = Scrollbar(f2, orient='vertical')
scrollbar.configure(command=tv.yview)
scrollbar.pack(side="right", fill="y")
tv.config(yscrollcommand=scrollbar.set)

def filter_by_date():
    selected_date = dopvar.get()
    for item in tv.get_children():
        tv.delete(item)
    records = data.fetchRecord(f"SELECT rowid, * FROM expense_record WHERE purchase_date = '{selected_date}'")
    for rec in records:
        tv.insert(parent='', index='end', values=(rec[0], rec[1], rec[2], rec[3]))

# add heading to treeview
tv.column(1, anchor=CENTER, stretch=NO, width=70)
tv.column(2, anchor=CENTER)
tv.column(3, anchor=CENTER)
tv.column(4, anchor=CENTER)
tv.heading(1, text="Serial no")
tv.heading(2, text="Item Name", )
tv.heading(3, text="Item Price")
tv.heading(4, text="Purchase Date")

# binding treeview
tv.bind("<ButtonRelease-1>", select_record)

# style for treeview
style = ttk.Style()
style.theme_use("default")
style.map("Treeview")

# calling function 
fetch_records()

# infinite loop
ws.mainloop()