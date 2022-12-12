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
print("\n\n\n\n As a Seller, I want to see how many different products I have currently listed so that The seller can decide wheter or not to list more products.")
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
            print("How many products are listed by seller_id")
            print("\n seller_id = 9 \n")
            actions[choice](s_id = 9)
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

def apply_filters(s_id):

    tmpl = f'''
    SELECT seller_id, count(product_id)
      FROM Products
     WHERE seller_id = '{s_id}'
     GROUP BY seller_id
    '''
    cmd = cur.mogrify(tmpl)
    print_cmd(cmd)
    cur.execute(cmd)
    rows = cur.fetchall()
    print_rows(rows)
    print("=================================")
    print("seller_id, number of products listed\n")
    for row in rows:
       sid, np_listed = row
       print(f"{sid}, {np_listed}")





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
