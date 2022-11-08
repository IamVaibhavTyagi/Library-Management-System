from django import conf
import mysql.connector
import json
import pandas as pd

with open('dbConfig.json') as config_file:
    data = json.load(config_file)

print(data["host"])
myConnection = mysql.connector.connect(
    host=data["host"], user=data["user"], passwd=data["password"], db=data["database"])
cursor = myConnection.cursor()

initialQuery = ["DELETE FROM Book;",
                "DELETE FROM Book_Authors;",
                "DELETE FROM Authors;",
                "ALTER TABLE Book_Authors AUTO_INCREMENT = 1;",
                "ALTER TABLE Authors AUTO_INCREMENT = 1;",
                "ALTER TABLE Borrower AUTO_INCREMENT = 1;",
                "ALTER TABLE Book_Loans AUTO_INCREMENT = 1;",
                "ALTER TABLE Fines AUTO_INCREMENT = 1;"]

for query in initialQuery:
    cursor.execute(query)


books = pd.read_csv('book.csv')
borrowers = pd.read_csv('borrower.csv')


def insertDataBook(data, key):
    ISBN10 = data._get_value(key, 'ISBN10')
    title = data._get_value(key, 'Title')
    title = title.replace('"', '')
    authors = str(data._get_value(key, 'Author')).split(',')
    authors = [i.replace('"', '') for i in authors]
    availabitity = 1

    query = 'INSERT INTO Book VALUES("' + str(ISBN10) + \
        '","' + str(title) + '","' + str(availabitity) + '");'
    cursor.execute(query)

    for author in authors:
        query1 = 'INSERT INTO Book_Authors(Isbn) VALUES("' + \
            str(ISBN10) + '");'
        cursor.execute(query1)

    for author in authors:
        query2 = 'INSERT INTO Authors(Name) VALUES("' + author + '");'
        cursor.execute(query2)


def insertDataBorrower(data, key):
    ssn = str(data._get_value(key, 'borrower_id'))
    bname = str(data._get_value(key, 'first_name')) + \
        " " + str(data._get_value(key, 'last_name'))
    address = str(data._get_value(key, 'address')) + "," + \
        str(data._get_value(key, 'city')) + "," + \
        str(data._get_value(key, 'state'))
    phone = str(data._get_value(key, 'phone'))

    query = 'INSERT INTO Borrower(Ssn,Bname,Address,Phone) VALUES("' + \
        ssn + '","' + bname + '","' + address + '","' + phone + '");'
    cursor.execute(query)


for i in range(1, len(books)+1):
    insertDataBook(books[i-1:i], i-1)

for i in range(1, len(borrowers)+1):
    insertDataBorrower(borrowers[i-1:i], i-1)

print("Successfully initialized the tables")

myConnection.commit()
myConnection.close()
