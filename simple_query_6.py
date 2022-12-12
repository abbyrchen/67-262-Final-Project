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
print("\n\n\n\n As a Seller, I want to Update the amount of product left in stock so that I The ebay website displays an accurate number of products left in stock after a restock.")
def show_menu():
    menu = '''

--------------------------------------------------
1. Filter items

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
            print("After a restock of a certain product, update the amount of product left in stock.")
            print("\n product_id = 2, added amount = 7 \n")
            actions[choice](p_id = 2, added_amount = 7)
            show_menu()
        else:
            print("\n\n* Invalid choice (%s). Choose again." % choice)
            show_menu()
    finally:
        if cur != None:
            cur.close() 
        if conn != None:
            conn.close()

def apply_filters_menu():
    apply_filters()

def apply_filters(p_id, added_amount):
    tmpl_0 = f'''
        SELECT product_id, product_name, amount_in_stock
          FROM Products
         WHERE product_id = {p_id}
    '''
    cmd_0 = cur.mogrify(tmpl_0)
    print_cmd(cmd_0)
    cur.execute(cmd_0)
    rows_0 = cur.fetchall()
    print_rows(rows_0)
    print("=================================")
    print("(((Product before update)))\n")
    print("product_id,product_name,amount_in_stock")
    for row_0 in rows_0:
       pid0,pname0,pamt0 = row_0
       print(f"{pid0},{pname0},{pamt0}")
    print("=================================")
    print("=================================")
    print("=================================")
    print("=================================")
    

    tmpl = f'''
        UPDATE Products
           SET amount_in_stock = amount_in_stock + {added_amount}
         WHERE product_id = '{p_id}'
    '''
    cmd = cur.mogrify(tmpl)
    print_cmd(cmd)
    cur.execute(cmd)
    print("=================================")
    print(f"stock of {added_amount} was added to product_id = {p_id}")
    print("=================================")

    tmpl_2 = f'''
        SELECT product_id, product_name, amount_in_stock
          FROM Products
         WHERE product_id = {p_id}
    '''
    cmd_2 = cur.mogrify(tmpl_2)
    print_cmd(cmd_2)
    cur.execute(cmd_2)
    rows_2 = cur.fetchall()
    print_rows(rows_2)
    print("=================================")
    print("(((Product after update)))\n")
    print("product_id,product_name,amount_in_stock")
    for row_2 in rows_2:
       pid2,pname2,pamt2 = row_2
       print(f"{pid2},{pname2},{pamt2}")






actions = { 1:apply_filters }




if __name__ == '__main__':
    try:
        # default database and user
        db, user = 'ebay', 'isdb'
        # you may have to adjust the user
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
