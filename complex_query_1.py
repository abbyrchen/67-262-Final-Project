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
            actions[choice](t_id=12, dte='2022-12-11', price=90, amt=1, c_id=13, p_id=1)
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
    price = input("price: ")
    amount = input("amount: ")
    c_id = input("customer id: ")
    p_id = input("product id: ")
    purchase_item(t_id, dte, price, amount, c_id, p_id)
    
#------------------------------------------------------------
# list_users
#------------------------------------------------------------

def purchase_item(t_id, dte, price, amt, c_id, p_id):
    tmpl = f'''
    INSERT INTO Transactions (transaction_id, date, price, amount, customer_id, product_id)
      VALUES({t_id}, '{dte}', {price}, {amt}, {c_id}, {p_id});
    
    UPDATE Products
       SET amount = amount - 1
     WHERE product_id = {p_id}
    '''
    cmd = cur.mogrify(tmpl)
    print_cmd(cmd)
    cur.execute(cmd)
    rows = cur.fetchall()
    print_rows(rows)
    print("=================================")
    print("p_id, price")
    for row in rows:
       date, p_id, price = row
       print(f"{date}, {p_id}, {price}")

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
