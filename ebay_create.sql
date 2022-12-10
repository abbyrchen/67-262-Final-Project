-- Created by Vertabelo (http://vertabelo.com)
-- Last modification date: 2022-12-06 23:25:01.685

-- tables
-- Table: Auctions
CREATE TABLE Auctions (
    transaction_id int  NOT NULL,
    min_auc_price int  NOT NULL,
    time_duration time  NOT NULL,
    CONSTRAINT Auctions_pk PRIMARY KEY (transaction_id)
);

-- Table: Bids
CREATE TABLE Bids (
    bid_id int  NOT NULL,
    auction_id int  NOT NULL,
    amount int  NOT NULL,
    CONSTRAINT Bids_pk PRIMARY KEY (bid_id)
);

-- Table: Complaints
CREATE TABLE Complaints (
    complaint_id int  NOT NULL,
    problem_type text  NOT NULL,
    problem_description text  NOT NULL,
    transaction_id int  NOT NULL,
    CONSTRAINT Complaints_pk PRIMARY KEY (complaint_id)
);

-- Table: Customers
CREATE TABLE Customers (
    customer_id int  NOT NULL,
    CONSTRAINT Customers_pk PRIMARY KEY (customer_id)
);

-- Table: Products
CREATE TABLE Products (
    product_id int  NOT NULL,
    product_name text  NOT NULL,
    price int  NOT NULL,
    amount int  NOT NULL,
    category text  NOT NULL,
    seller_id int  NOT NULL,
    CONSTRAINT Products_pk PRIMARY KEY (product_id)
);

-- Table: Reviews
CREATE TABLE Reviews (
    review_id int  NOT NULL,
    rating int  NOT NULL,
    description text  NOT NULL,
    product_id int  NOT NULL,
    CONSTRAINT Reviews_pk PRIMARY KEY (review_id)
);

-- Table: Sales
CREATE TABLE Sales (
    transaction_id int  NOT NULL,
    CONSTRAINT Sales_pk PRIMARY KEY (transaction_id)
);

-- Table: Sellers
CREATE TABLE Sellers (
    seller_id int  NOT NULL,
    CONSTRAINT Sellers_pk PRIMARY KEY (seller_id)
);

-- Table: Transactions
CREATE TABLE Transactions (
    transaction_id int  NOT NULL,
    date date  NOT NULL,
    price int  NOT NULL,
    amount int  NOT NULL,
    customer_id int  NOT NULL,
    product_id int  NOT NULL,
    CONSTRAINT Transactions_pk PRIMARY KEY (transaction_id)
);

-- Table: Users
CREATE TABLE Users (
    user_id int  NOT NULL,
    f_name text  NOT NULL,
    l_name text  NOT NULL,
    address text  NOT NULL,
    phone_number text  NOT NULL,
    email text  NOT NULL,
    user_name text  NOT NULL,
    CONSTRAINT Users_pk PRIMARY KEY (user_id)
);

-- foreign keys
-- Reference: Auctions_Transactions (table: Auctions)
ALTER TABLE Auctions ADD CONSTRAINT Auctions_Transactions
    FOREIGN KEY (transaction_id)
    REFERENCES Transactions (transaction_id)  
    NOT DEFERRABLE 
    INITIALLY IMMEDIATE
;

-- Reference: Bids_Auctions (table: Bids)
ALTER TABLE Bids ADD CONSTRAINT Bids_Auctions
    FOREIGN KEY (auction_id)
    REFERENCES Auctions (transaction_id)  
    NOT DEFERRABLE 
    INITIALLY IMMEDIATE
;

-- Reference: Complaints_Transactions (table: Complaints)
ALTER TABLE Complaints ADD CONSTRAINT Complaints_Transactions
    FOREIGN KEY (transaction_id)
    REFERENCES Transactions (transaction_id)  
    NOT DEFERRABLE 
    INITIALLY IMMEDIATE
;

-- Reference: Customers_Users (table: Customers)
ALTER TABLE Customers ADD CONSTRAINT Customers_Users
    FOREIGN KEY (customer_id)
    REFERENCES Users (user_id)  
    NOT DEFERRABLE 
    INITIALLY IMMEDIATE
;

-- Reference: Products_Sellers (table: Products)
ALTER TABLE Products ADD CONSTRAINT Products_Sellers
    FOREIGN KEY (seller_id)
    REFERENCES Sellers (seller_id)  
    NOT DEFERRABLE 
    INITIALLY IMMEDIATE
;

-- Reference: Reviews_Products (table: Reviews)
ALTER TABLE Reviews ADD CONSTRAINT Reviews_Products
    FOREIGN KEY (product_id)
    REFERENCES Products (product_id)  
    NOT DEFERRABLE 
    INITIALLY IMMEDIATE
;

-- Reference: Sales_Transactions (table: Sales)
ALTER TABLE Sales ADD CONSTRAINT Sales_Transactions
    FOREIGN KEY (transaction_id)
    REFERENCES Transactions (transaction_id)  
    NOT DEFERRABLE 
    INITIALLY IMMEDIATE
;

-- Reference: Sellers_Users (table: Sellers)
ALTER TABLE Sellers ADD CONSTRAINT Sellers_Users
    FOREIGN KEY (seller_id)
    REFERENCES Users (user_id)  
    NOT DEFERRABLE 
    INITIALLY IMMEDIATE
;

-- Reference: Transactions_Customers (table: Transactions)
ALTER TABLE Transactions ADD CONSTRAINT Transactions_Customers
    FOREIGN KEY (customer_id)
    REFERENCES Customers (customer_id)  
    NOT DEFERRABLE 
    INITIALLY IMMEDIATE
;

-- Reference: Transactions_Products (table: Transactions)
ALTER TABLE Transactions ADD CONSTRAINT Transactions_Products
    FOREIGN KEY (product_id)
    REFERENCES Products (product_id)  
    NOT DEFERRABLE 
    INITIALLY IMMEDIATE
;

-- End of file.

