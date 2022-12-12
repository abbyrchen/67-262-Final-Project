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
print("\n\n\n\n As a Customer Service Manager, I want to Obtain the email address of the customer that has reported an issue in transaction so that I can send an email to apologize for the inconvenient experience and give them updates on the actions being taken.")
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
            print("Obtain the email address of the customer that has reported an issue in transaction ")
            print("\n complaint_id = 3\n")
            actions[choice](comp_id = 3)
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

def apply_filters(comp_id):
    tmpl = f'''
        SELECT c.complaint_id, u.user_id, u.email
          FROM Complaints as c 
               JOIN Transactions as t ON t.transaction_id = c.transaction_id
               JOIN Customers as ctm ON ctm.customer_id = t.customer_id
               JOIN Users as u ON u.user_id = ctm.customer_id 
         WHERE c.complaint_id = {comp_id}
    '''
    cmd = cur.mogrify(tmpl)
    print_cmd(cmd)
    cur.execute(cmd)
    rows = cur.fetchall()
    print_rows(rows)
    print("=================================")
    print("complaint_id, user_id, email\n")
    for row in rows:
       c_id, u_id, u_email = row
       print(f"{c_id}, {u_id}, {u_email}")





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
