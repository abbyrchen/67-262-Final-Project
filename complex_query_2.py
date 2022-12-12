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
print("\n\n\n\n As a Seller, I want to to figure out the total revenue of products sold for the day. so that I can know how successful the day's business was. ")
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
            print("\n seller=17, sold_date='2022-11-21' \n")
            actions[choice](seller=17, sold_date='2022-11-21')
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

def apply_filters(seller, sold_date):
    tmpl = f'''
        SELECT p.seller_id, t.date, sum(t.amount), sum(p.price * t.amount)
          FROM Transactions as t
               JOIN Products as p ON t.product_id = p.product_id
               JOIN Sellers as s ON s.seller_id = p.seller_id
         WHERE p.seller_id = '{seller}' and t.date = '{sold_date}'
         GROUP BY p.seller_id, t. date
    '''
    cmd = cur.mogrify(tmpl)
    print_cmd(cmd)
    cur.execute(cmd)
    rows = cur.fetchall()
    print_rows(rows)
    print("=================================")
    print("seller_id, date, products sold, revenue")
    for row in rows:
       s_id, date, p_sold, revenue= row
       print(f"{s_id}, {date}, {p_sold}, {revenue}")





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
