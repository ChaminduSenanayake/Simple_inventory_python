from tkinter import *
import pymysql
import tkinter.ttk as ttk
from tkinter import messagebox
import time


def dbConnection():
    global db,cursor
    db= pymysql.connect("localhost","root","26010","Inventory" )
    cursor=db.cursor()
   
def clearItemTextFields():
    t1.config(state="normal")
    t1.delete(0, 'end')
    t2.delete(0, 'end')
    t3.delete(0, 'end')
    t4.delete(0, 'end')
    t5.delete(0, 'end')
 
def addItem():
    dbConnection()
    cursor.execute("select * from item where itemCode=%s", e1.get())
    searchResult=cursor.fetchall()
    
    if(len(searchResult)!=0):
        item=searchResult[0]
        if(item[0]==e1.get()):
            
            newQty=item[3]+int(e4.get())
            sql = "update item set itemName=%s,description=%s,quantity=%s,price=%s where itemCode =%s;"
            val = (e2.get(),e3.get(),newQty,float(e5.get()),e1.get())
            cursor.execute(sql, val)
    else:
        sql = "insert into item values(%s,%s,%s,%s,%s)"
        val = (e1.get(),e2.get(),e3.get(),int(e4.get()),float(e5.get()))
        cursor.execute(sql, val)
    db.commit()
    db.close()
    viewAllItems()
    addItemWin.destroy()
    
def editItem():
    dbConnection()
    sql = "update item set itemName=%s,description=%s,quantity=%s,price=%s where itemCode =%s;"
    val = (t2.get(),t3.get(),int(t4.get()),float(t5.get()),t1.get())
    cursor.execute(sql, val)
    db.commit()
    db.close()
    viewAllItems()
    clearItemTextFields()
    
def deleteItem():
    result = messagebox.askokcancel("Python","Would you like to delete the data?")
    if(result):
        dbConnection()
        sql = "delete from item where itemCode = %s"
        val = (t1.get())
        cursor.execute(sql, val)
        db.commit()
        db.close()
        viewAllItems()
        clearItemTextFields()
def loadItem(event):
    if not itemTree.selection():
       print("ERROR")
    else:
        curItem = itemTree.focus()
        contents =(itemTree.item(curItem))
        selecteditem = contents['values']
        clearItemTextFields()
        t1.insert(0,selecteditem[0])
        t1.config(state="disabled")
        t2.insert(0,selecteditem[1])
        t3.insert(0,selecteditem[2])
        t4.insert(0,selecteditem[3])
        t5.insert(0,selecteditem[4])
       
def viewAllItems():
    dbConnection()
    cursor.execute("select * from item")
    itemList = cursor.fetchall()
    db.commit()
    db.close()
    for i in itemTree.get_children():
        itemTree.delete(i)
    for item in itemList:
        itemTree.insert('', 'end', values=item)
        
    
def newItemWindow():
    global addItemWin,e1,e2,e3,e4,e5
    addItemWin = Toplevel()
    addItemWin.configure(bg='white',bd=30)
    Label(addItemWin, text="Item Code",bg='white',width=20,height=3).grid(row=0)
    Label(addItemWin, text="Name",bg='white',width=20,height=3).grid(row=1)
    Label(addItemWin, text="Description",bg='white',width=20,height=3).grid(row=2)
    Label(addItemWin, text="Quantity",bg='white',width=20,height=3).grid(row=3)
    Label(addItemWin, text="Price",bg='white',width=20,height=3).grid(row=4)
    e1 = Entry(addItemWin,width=20,bg='white',relief="solid")
    e2 = Entry(addItemWin,width=50,bg='white',relief="solid")
    e3 = Entry(addItemWin,width=100,bg='white',relief="solid")
    e4 = Entry(addItemWin,width=20,bg='white',relief="solid")
    e5 = Entry(addItemWin,width=20,bg='white',relief="solid")
    e1.grid(row=0, column=2,sticky=W, ipadx=10, ipady=4)
    e2.grid(row=1, column=2,sticky=W, ipadx=10, ipady=4)
    e3.grid(row=2, column=2,sticky=W, ipadx=10, ipady=4)
    e4.grid(row=3, column=2,sticky=W, ipadx=10, ipady=4)
    e5.grid(row=4, column=2,sticky=W, ipadx=10, ipady=4)

    btnAdd = Button(addItemWin,text="Add Item",fg="blue",bg='gray66',width=20,height=2,bd=0,command=addItem)
    btnAdd.place(x=640,y=230)
    addItemWin.mainloop()
#=========================================================================Frame==============================================================================
root = Tk()
root.title("Inventory System")
root.geometry("1218x696+150+50")
root.configure(bg='white',bd=20)


itemFrame = Frame(root)
itemFrame.configure(bg="white",width=1476,height=750)

Label(itemFrame, text="Inventory",bg='white',fg='darkcyan',font=('vardhana', 25,'bold')).place(x=500,y=0)
frame1=Frame(itemFrame)
lb_header = ['Item Code','Name', 'Description','quantity','Price']
itemTree =ttk.Treeview(frame1,height = 10,columns=lb_header, show="headings")
vsb = Scrollbar(frame1,orient="vertical", command=itemTree.yview)
hsb = Scrollbar(frame1,orient="horizontal", command=itemTree.xview)
itemTree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
itemTree.grid(column=0, row=0, sticky='nsew', in_=frame1)
vsb.grid(column=1, row=0, sticky='ns', in_=frame1)
hsb.grid(column=0, row=1, sticky='ew', in_=frame1)
itemTree.bind("<<TreeviewSelect>>", loadItem)
itemTree.grid(in_=frame1)
for col in lb_header:
    itemTree.heading(col, text=col.title())
frame1.place(x = 50, y = 70)

btnAddNew = Button(itemFrame,text="Add new Item",fg='darkcyan',width=20,height=2,bd=0,command=newItemWindow)
btnAddNew.place(x = 50, y = 350)

middleItemFrame=Frame(itemFrame)
middleItemFrame.configure(bg='white')
Label(middleItemFrame, text="Item Code",bg='white',width=20,height=3).grid(row=0)
Label(middleItemFrame, text="Name",bg='white',width=20,height=3).grid(row=1)
Label(middleItemFrame, text="Description",bg='white',width=20,height=3).grid(row=2)
Label(middleItemFrame, text="Quantity",bg='white',width=20,height=3).grid(row=3)
Label(middleItemFrame, text="Price",bg='white',width=20,height=3).grid(row=4)
t1 = Entry(middleItemFrame,width=20,relief=RIDGE)
t2 = Entry(middleItemFrame,width=50,relief=RIDGE)
t3 = Entry(middleItemFrame,width=100,relief=RIDGE)
t4 = Entry(middleItemFrame,width=20,relief=RIDGE)
t5 = Entry(middleItemFrame,width=20,relief=RIDGE)
t1.grid(row=0, column=2,sticky=W, ipadx=10, ipady=4)
t2.grid(row=1, column=2,sticky=W, ipadx=10, ipady=4)
t3.grid(row=2, column=2,sticky=W, ipadx=10, ipady=4)
t4.grid(row=3, column=2,sticky=W, ipadx=10, ipady=4)
t5.grid(row=4, column=2,sticky=W, ipadx=10, ipady=4)
middleItemFrame.place(x = 40, y = 400)

btnEditItem = Button(itemFrame,text="Edit Item",fg='blue',bg='gray76',width=15,height=2,bd=0,command=editItem)
btnEditItem.place(x=760,y=620)
btnDeleteItem = Button(itemFrame,text="Delete Item",fg='red',bg='gray76',width=15,height=2,bd=0,command=deleteItem)
btnDeleteItem.place(x=890,y=620)
itemFrame.grid()

viewAllItems()
root.mainloop()
    
    





    






