-- Setup the database for a very simple 'social network'.
-- Friends - Users - Messages 

\c postgres
DROP DATABASE IF EXISTS ebay;

CREATE database ebay;
\c ebay

\i ebay_create.SQL

-- Users.csv
-- Customers.csv
-- Products.csv
-- Transactions.csv


\copy Users(user_id, f_name, l_name, address, phone_number, email, user_name) FROM users.csv csv header;

\copy Customers(customer_id) FROM customers.csv csv header;

\copy Sellers(seller_id) FROM sellers.csv csv header;

\copy Products(product_id, product_name, price, amount_in_stock, category, seller_id) FROM products.csv csv header;

\copy Transactions(transaction_id,date,amount,customer_id,product_id) FROM transactions.csv csv header;

\copy Auctions(transaction_id, min_auc_price, time_duration) FROM auctions.csv csv header;

\copy Bids(bid_id, auction_id, bidded_amount) FROM bids.csv csv header;

\copy Reviews(review_id,rating,description,product_id) FROM reviews.csv csv header;

\copy Complaints(complaint_id,problem_type,problem_description,transaction_id) FROM complaints.csv csv header;












-- ============================================================
  
