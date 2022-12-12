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
print("\n\n\n\n As a Customer Service Manager, I want to See how many complaints on different problem types were reported on a given day so that I can know which problem types are there to be taken care of for the day.")
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
            print("\n target_date='2022-11-21' \n")
            actions[choice](target_date='2022-11-21')
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

def apply_filters(target_date):
    tmpl = f'''
        SELECT t.date, problem_type, count(c.complaint_id)
          FROM Complaints as c 
               JOIN Transactions as t on t.transaction_id = c.transaction_id
         WHERE t.date = '{target_date}'
         GROUP BY problem_type, t.date
    '''
    cmd = cur.mogrify(tmpl)
    print_cmd(cmd)
    cur.execute(cmd)
    rows = cur.fetchall()
    print_rows(rows)
    print("=================================")
    print("date, complaint_type, complaints count\n")
    for row in rows:
       p_date, p_type, p_cnt = row
       print(f"{p_date}, {p_type}, {p_cnt}")





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
