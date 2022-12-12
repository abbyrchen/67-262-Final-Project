#-----------------------------------------------------------------
# Working with psycopg2
#-----------------------------------------------------------------

import psycopg2
import sys

def heading(str):
    print('-'*60)
    print("** %s:" % (str,))
    print('-'*60, '\n')

SHOW_CMD = True
def print_cmd(cmd):
    if SHOW_CMD:
        print(cmd.decode('utf-8'))

def print_rows(rows):
    for row in rows:
        print(row)

#------------------------------------------------------------
# show_menu
#------------------------------------------------------------

def show_menu():
    print('''User Story 2 - As a user, I want to buy an item
    ''')
    menu = '''

--------------------------------------------------
1. Buy an item


Choose (1-1, 0 to quit): '''
    try:
        choice = int(input( menu ))
    except ValueError:
        print("\n\n* Invalid choice. Choose again.")
        show_menu()
    else:
        if choice == 0:
            print('Done.')
            cur.close()
            conn.close()
        elif choice == 1:
            print("Purchasing the following item")
            actions[choice](t_id=18, dte='2022-12-11', amt=1, c_id=13, p_id=1)
            show_menu()
        else:
            print("\n\n* Invalid choice (%s). Choose again." % choice)
            show_menu()
    finally:
        if cur != None:
            cur.close() 
        if conn != None:
            conn.close()

def purchase_item_menu():
    t_id = input("transaction id: ")
    dte = input("date: ")
    amount = input("amount: ")
    c_id = input("customer id: ")
    p_id = input("product id: ")
    purchase_item(t_id, dte, amount, c_id, p_id)
    
def purchase_item(t_id, dte, amt, c_id, p_id):
    tmpl0 = f'''
        SELECT *
          FROM Transactions
    '''
    cmd0 = cur.mogrify(tmpl0)
    cur.execute(cmd0)
    rows0 = cur.fetchall()
    print("=================================")
    print("(Transactions before)\n")
    print("transaction_id, date, amount, customer_id, product_id")
    for row0 in rows0:
       t_id0, dte0, amt0, c_id0, p_id0 = row0
       print(f"{t_id0},{dte0}, {amt0}, {c_id0}, {p_id0}")
    print("=================================")
    print("=================================")
    print("=================================")
    print("=================================")

    tmpl = f'''
    INSERT INTO Transactions (transaction_id, date, amount, customer_id, product_id)
      VALUES({t_id}, '{dte}', {amt}, {c_id}, {p_id});
    
    UPDATE Products
       SET amount_in_stock = amount_in_stock - 1
     WHERE product_id = {p_id}
    '''
    cmd = cur.mogrify(tmpl)
    print_cmd(cmd)
    cur.execute(cmd)
    print("=================================")
    print(f"A transaction on {dte} of {amt} was added to product_id = {p_id} for customer_id = {c_id}")
    print("=================================")
    
    tmpl1 = f'''
        SELECT *
          FROM Transactions
    '''
    cmd1 = cur.mogrify(tmpl1)
    cur.execute(cmd1)
    rows1 = cur.fetchall()
    print("=================================")
    print("(Transactions after)\n")
    print("transaction_id, date, amount, customer_id, product_id")
    for row1 in rows1:
       t_id1, dte1, amt1, c_id1, p_id1 = row1
       print(f"{t_id1},{dte1}, {amt1}, {c_id1}, {p_id1}")

actions = { 1:purchase_item }

if __name__ == '__main__':
    try:
        db, user = 'ebay', 'isdb'
        if len(sys.argv) >= 2:
            db = sys.argv[1]
        if len(sys.argv) >= 3:
            user = sys.argv[2]
        # by assigning to conn and cur here they become
        # global variables.  Hence they are not passed
        # into the various SQL interface functions
        conn = psycopg2.connect(database=db, user=user)
        conn.autocommit = True
        cur = conn.cursor()
        show_menu()
    except psycopg2.Error as e:
        print("Unable to open connection: %s" % (e,))
