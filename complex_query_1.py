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
            actions[choice](p_id=1)
            show_menu()
        else:
            print("\n\n* Invalid choice (%s). Choose again." % choice)
            show_menu()
    finally:
        if cur != None:
            cur.close() 
        if conn != None:
            conn.close()

def place_bid_menu():
    place_bid()
    
#------------------------------------------------------------
# list_users
#------------------------------------------------------------

def place_bid(p_id):
    tmpl = f'''
    DELETE FROM Products
      WHERE product_id = p_id

    INSERT INTO Transactions
      VALUES()
    '''
    cmd = cur.mogrify(tmpl)
    print_cmd(cmd)
    cur.execute(cmd)
    rows = cur.fetchall()
    print_rows(rows)
    print("=================================")
    print("p_id")
    for row in rows:
        b_id, a_id, amt = row
        print(f"{b_id}, {a_id}, {amt}")

actions = { 1:place_bid }

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
