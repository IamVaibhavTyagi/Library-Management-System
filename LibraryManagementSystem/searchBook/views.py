from django.contrib.auth.decorators import login_required
from msilib.schema import Condition
from pickle import NONE
from django.shortcuts import render
from django.db import connection
from .models import Book, Authors, BookAuthors
from django.core.paginator import Paginator, EmptyPage

cursor = connection.cursor()


@login_required(login_url="login:login")
def index(request):
    # flag = True
    searchValue = False
    global books_list
    print("inside index")
    # print(request)
    if (request.method == "POST"):
        if(request.POST['searchBox'] != ''):
            # flag = False
            words = request.POST['searchBox'].split(',')
            condition = ""
            for word in words:
                word = word.strip()
                word = "%"+word+"%"
                if condition != "":
                    condition += "AND"
                condition += "(bookAuthorTemp.Isbn LIKE '"+word+"' OR bookAuthorTemp.Title LIKE '" + \
                    word+"' OR bookAuthorTemp.authors LIKE '"+word+"')"
            query = "SELECT bookAuthorTemp.Isbn, bookAuthorTemp.Title, bookAuthorTemp.authors, bookAuthorTemp.Available FROM (SELECT Book.ISBN, Book.TITLE, GROUP_CONCAT(Authors.Name) authors, Book.Available FROM Book,Book_Authors,Authors WHERE Book.Isbn = Book_Authors.Isbn AND Book_Authors.Author_id = Authors.Author_id GROUP BY Book.Isbn) AS bookAuthorTemp WHERE "+condition
            cursor.execute(query)

            books_list = list(cursor.fetchall())

            p = Paginator(books_list, 6)

            page = p.get_page(1)

            return render(request, "index.html", {"page": page, "flag": False, "totalpages": p.num_pages, "searchValue": True, 'books_list': books_list})
        else:
            print("Search text box is Empty!")
            return render(request, "index.html", {"searchValue": searchValue, "flag": False})
    elif (request.method == "GET"):
        if 'previousbtn' in request.GET or 'nextbtn' in request.GET or 'firstbtn' in request.GET or 'lastbtn' in request.GET:
            print("inside else of search")
            print(request.GET.get('nextbtn'))
            print(request.GET.get('previousbtn'))
            print(request.GET.get('firstbtn'))
            print(request.GET.get('lastbtn'))
            print(books_list[:10])

            p = Paginator(books_list, 6)

            page_num = request.GET.get(
                'nextbtn') if 'nextbtn' in request.GET else request.GET.get('previousbtn') if 'previousbtn' in request.GET else request.GET.get('firstbtn') if 'firstbtn' in request.GET else request.GET.get('lastbtn')
            page = p.get_page(page_num)

            return render(request, "index.html", {"page": page, "flag": False, "totalpages": p.num_pages, "searchValue": True})

    print("Outside ifelse")
    return render(request, 'index.html', {"searchValue": searchValue, "flag": True})


def checkout(request):
    print("inside checkout")
    words = request.POST['cardno'].split(',')
    print(words)

    message = ""

    cardno = words[0]
    isbn = words[1]

    query = "SELECT COUNT(Card_id) FROM Borrower WHERE Card_id = '" + \
        cardno+"' GROUP BY Card_id"
    cursor.execute(query)

    if(cursor.fetchone() != None):
        query = "SELECT COUNT(Loan_id) FROM Book_Loans WHERE Book_Loans.Card_id = '"+str(
            cardno)+"' AND Book_Loans.Date_in IS NULL GROUP BY Book_Loans.Card_id"
        cursor.execute(query)
        result = cursor.fetchone()
        if(result == None):
            query = "SELECT Book.Available FROM Book WHERE Book.Isbn = '"+isbn+"'"
            cursor.execute(query)
            availabile = cursor.fetchone()
            if(availabile[0] == 1):
                query = 'INSERT INTO Book_Loans(Isbn, Card_id, Date_out, Due_date, Date_in) VALUES("' + \
                    isbn + '","' + \
                        str(cardno) + \
                    '",CURDATE(),DATE_ADD(Date_out,INTERVAL 14 DAY),NULL)'
                cursor.execute(query)
                query = 'UPDATE Book SET Book.Available = "0" WHERE Book.isbn = "'+isbn+'"'
                cursor.execute(query)
                message = "Successfully checked out book. Return within 14 days to avoid fine."
                query = "Select Loan_id from book_loans WHERE Book_Loans.Card_id = '" + \
                    str(cardno)+"'"
                cursor.execute(query)
                loanId = cursor.fetchall()
                print("loan id printing", loanId[-1][0])
                cursor.execute("INSERT INTO Fines(Loan_id,Fine_amt,Paid) VALUES('" +
                               str(loanId[-1][0]) + "','" + str(0.00) + "','0')")
            else:
                message = "Book is not available."
        else:
            query = "SELECT Book.Available FROM Book WHERE Book.Isbn = '"+isbn+"'"
            cursor.execute(query)
            if(result[0] < 3):
                query = 'INSERT INTO Book_Loans(Isbn, Card_id, Date_out, Due_date, Date_in) VALUES("' + \
                    isbn + '","' + \
                        str(cardno) + \
                    '",CURDATE(),DATE_ADD(Date_out,INTERVAL 14 DAY),NULL)'
                cursor.execute(query)
                query = 'UPDATE Book SET Book.Available = "0" WHERE Book.isbn = "'+isbn+'"'
                cursor.execute(query)
                message = "Successfully checked out book. Return within 14 days to avoid fine."
                query = "Select Loan_id from book_loans WHERE Book_Loans.Card_id = '" + \
                    str(cardno)+"'"
                cursor.execute(query)
                loanId = cursor.fetchall()
                print("printing loanid", type(loanId[-1][0]))
                cursor.execute("INSERT INTO Fines(Loan_id,Fine_amt,Paid) VALUES('" +
                               str(loanId[-1][0]) + "','" + str(0.00) + "','0')")
            else:
                message = "Maximum of only 3 books can be checked out by each individual."

    context = {'message': message, 'update': True}
    return render(request, 'index.html', context)
