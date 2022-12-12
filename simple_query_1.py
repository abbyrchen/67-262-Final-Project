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
    print('''User Story 1 - As a bidder, I want to place a bid on an item
    ''')
    menu = '''

--------------------------------------------------
1. Place bid


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
            print("Placing a bid on the following item")
            print("\n Bid amount = 90 \n")
            actions[choice](bid_id=9, auction_id=9, amount=90)
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
    bid_id = input("bid id: ")
    auction_id = input("auction id: ")
    amount = input("amount: ")
    place_bid(bid_id, auction_id, amount)
    
#------------------------------------------------------------
# list_users
#------------------------------------------------------------

def place_bid(bid_id, auction_id, amount):
    tmpl0 = f'''
        SELECT *
          FROM Bids
    '''
    cmd0 = cur.mogrify(tmpl0)
    cur.execute(cmd0)
    rows0 = cur.fetchall()
    print("=================================")
    print("(Bids before)\n")
    print("bid_id, auction_id, bidded_amount")
    for row0 in rows0:
       bid_id, auction_id, amount = row0
       print(f"{bid_id},{auction_id}, {amount}")
    print("=================================")
    print("=================================")
    print("=================================")
    print("=================================")

    tmpl = f'''
    INSERT INTO Bids(bid_id, auction_id, bidded_amount)
        VALUES (%s, %s, %s);
    '''
    cmd = cur.mogrify(tmpl, (bid_id, auction_id, amount,))
    print_cmd(cmd)
    cur.execute(cmd)
    print("=================================")
    print(f"A bid for auction id = {auction_id} was placed on bid_id = {bid_id} of {amount}")
    print("=================================")

    tmpl1 = f'''
        SELECT *
          FROM Bids
    '''
    cmd1 = cur.mogrify(tmpl1)
    cur.execute(cmd1)
    rows1 = cur.fetchall()
    print("=================================")
    print("(Bids after)\n")
    print("bid_id, auction_id, amount")
    for row1 in rows1:
       bid_id1, auction_id1, amount1 = row1
       print(f"{bid_id1},{auction_id1}, {amount1}")

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
