from distutils.command.config import config
from matplotlib.pyplot import table
import mysql.connector
from mysql.connector import errorcode
import json

with open('dbConfig.json') as config_file:
    data = json.load(config_file)


# Establishing connection
myConnection = mysql.connector.connect(
    host=data["host"], user=data["user"], passwd=data["password"], db=data["database"])
cursor = myConnection.cursor()

# Tables dictionary
tables = {
    "Book": "CREATE TABLE Book(ISBN VARCHAR(10) NOT NULL, TITLE VARCHAR(255), AVAILABLE INT NOT NULL DEFAULT 1, CONSTRAINT BookPK PRIMARY KEY(ISBN));",
    "Book_Authors": "CREATE TABLE Book_Authors(Author_id INT NOT NULL AUTO_INCREMENT, ISBN VARCHAR(10), CONSTRAINT BookAuthorPK PRIMARY KEY(Author_id), CONSTRAINT BookAuthorFK FOREIGN KEY(ISBN) REFERENCES Book(ISBN) ON DELETE SET NULL);",
    "Authors": "CREATE TABLE Authors(Author_id INT NOT NULL AUTO_INCREMENT, Name VARCHAR(255) NOT NULL, CONSTRAINT AuthorIDPK PRIMARY KEY(Author_id), CONSTRAINT AuthorIDFK FOREIGN KEY(Author_id) REFERENCES Book_Authors(Author_id) ON DELETE CASCADE);",
    "Borrower": "CREATE TABLE Borrower(Card_id INT NOT NULL AUTO_INCREMENT, Ssn VARCHAR(9) NOT NULL UNIQUE, Bname VARCHAR(255), Address VARCHAR(255), Phone VARCHAR(14), CONSTRAINT BorrowerPK PRIMARY KEY(Card_id));",
    "Book_Loans": "CREATE TABLE Book_Loans(Loan_id INT NOT NULL AUTO_INCREMENT, ISBN VARCHAR(10),Card_id INT, Date_out DATE, Due_date DATE, Date_in DATE, CONSTRAINT BookLoanPK PRIMARY KEY(Loan_id), CONSTRAINT BookLoanISBNFK FOREIGN KEY(ISBN) REFERENCES Book(ISBN) ON DELETE SET NULL, CONSTRAINT BookLoanCardFK FOREIGN KEY(Card_id) REFERENCES Borrower(Card_id) ON DELETE SET NULL);",
    "Fines": "CREATE TABLE Fines(Loan_id INT NOT NULL , Fine_amt DECIMAL(9,2) NOT NULL DEFAULT 0, Paid INT DEFAULT 0, CONSTRAINT FinesPK PRIMARY KEY(Loan_id), CONSTRAINT FinesFK FOREIGN KEY(Loan_id) REFERENCES Book_Loans(Loan_id) ON DELETE CASCADE);"
}


DB_NAME = "librarymgt"


# Creating database function


def create_database(cursor):
    try:
        cursor.execute("CREATE DATABASE {};".format(DB_NAME))
    except mysql.connector.Error as err:
        print("Failed creating database: {}".format(err))
        exit(1)


# Connecting to database
try:
    cursor.execute("USE {}".format(DB_NAME))
    print("Using Database {}".format(DB_NAME))
except mysql.connector.Error as err:
    print("Database {} does not exists.".format(DB_NAME))
    if err.errno == errorcode.ER_BAD_DB_ERROR:
        create_database(cursor)
        print("Database {} created successfully.".format(DB_NAME))
        myConnection.database = DB_NAME
    else:
        print(err)
        exit(1)

# Creating tables

for table_name, table_description in tables.items():
    try:
        print("Creating Table {} .".format(table_name))
        print("Table description {} .".format(table_description))
        cursor.execute(table_description)
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
            print("already exists.")
        else:
            print(err.msg)


myConnection.close()
