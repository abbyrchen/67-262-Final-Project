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
            print("searching product with the following filters")
            print("\n preferred_price=100,preferred_category='shoes' \n")
            actions[choice](preferred_price=100,preferred_category='shoes')
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

def apply_filters(preferred_price, preferred_category):
    tmpl = f'''
        SELECT product_id, product_name, p.price, p.category
          FROM Products AS p
               JOIN Transactions AS t
                    ON p.product_id = t.product
               JOIN Customers AS c
                    ON c.customer_id = t.customer
               JOIN Users as u
                    ON u.user_id = c.customer_id
         WHERE p.price <= {preferred_price} 
               AND p.category = '{preferred_category}'
    '''
    cmd = cur.mogrify(tmpl)
    print_cmd(cmd)
    cur.execute(cmd)
    rows = cur.fetchall()
    print_rows(rows)
    print("=================================")
    print("product_id, product_name, product_price, product_category")
    for row in rows:
       p_id, p_name, p_price, p_category= row
       print(f"{p_id}, {p_name}, {p_price}, {p_category}")
    
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
