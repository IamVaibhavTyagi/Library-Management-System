from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.db import connection
from .models import Book, Borrower, Fines, BookLoans, Authors, BookAuthors
from django.core.paginator import Paginator, EmptyPage
# Create your views here.

cursor = connection.cursor()


@login_required(login_url="login:login")
def index(request):
    print("inside checkin index")
    searchValue = False
    global books_list
    if(request.method == "POST"):
        if('checkInBox' in request.POST and request.POST['checkInBox'] != ''):
            words = request.POST['checkInBox'].split(',')
            condition = ""
            for word in words:
                word = word.strip()
                word = "%"+word+"%"
                if condition != "":
                    condition += "AND"
                condition += "(bookAuthorTemp.Isbn LIKE '"+word+"' OR bookAuthorTemp.Title LIKE '"+word+"' OR bookAuthorTemp.authors LIKE '" + \
                    word+"' OR bookAuthorTemp.Card_id LIKE '"+word + \
                    "' OR bookAuthorTemp.Bname LIKE '"+word + \
                    "' OR bookAuthorTemp.Ssn LIKE '"+word+"')"
            query = "SELECT bookAuthorTemp.Isbn, bookAuthorTemp.Title, bookAuthorTemp.authors, bookAuthorTemp.Card_id, bookAuthorTemp.Bname, bookAuthorTemp.Ssn, bookAuthorTemp.Loan_id FROM (SELECT Book.Isbn, Book.Title, GROUP_CONCAT(Authors.Name) authors, Borrower.Card_id, Borrower.Bname, Borrower.Ssn, Book_Loans.Loan_id FROM Book,Book_Authors,Authors,Borrower,Book_Loans WHERE Book.Isbn = Book_Authors.Isbn AND Book_Authors.Author_id = Authors.Author_id AND Book.Isbn = Book_Loans.Isbn AND Borrower.Card_id = Book_Loans.Card_id AND Book_Loans.Date_in IS NULL GROUP BY Book.Isbn) AS bookAuthorTemp WHERE "+condition
            cursor.execute(query)
            books_list = list(cursor.fetchall())
            p = Paginator(books_list, 6)

            page = p.get_page(1)
            return render(request, 'checkinIndex.html', {"page": page, "flag": False, "totalpages": p.num_pages, "searchValue": True, 'books_list': books_list})
        else:
            print("Search text box is Empty!")
            return render(request, "checkinIndex.html", {"searchValue": searchValue, "flag": False})
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

            return render(request, "checkinIndex.html", {"page": page, "flag": False, "totalpages": p.num_pages, "searchValue": True})
    return render(request, "checkinIndex.html", {"searchValue": searchValue, "flag": True})


def calculateFine(days, loan_id):
    print("inside calfine")
    fineAmount = 0.25*days if days != None else 0
    print(days, loan_id)
    # query = "SELECT Fine_amt FROM Fines WHERE Loan_id = '" + loan_id + "'"
    # cursor.execute(query)
    # print(cursor.fetchall())
    # if (cursor.fetchone() == None):
    #     print("inside fineamount insert")
    #     if fineAmount > 0:
    #         cursor.execute("INSERT INTO Fines(Loan_id,Fine_amt,Paid) VALUES('" +
    #                        loan_id + "','" + str(fineAmount) + "','0')")
    #     else:
    #         cursor.execute("INSERT INTO Fines(Loan_id,Fine_amt,Paid) VALUES('" +
    #                        loan_id + "','" + str(0) + "','0')")
    # else:
    # result = list(cursor.fetchall())
    # print(result)
    # if(cursor.fetchall()[0] > fineAmount):
    print("fineAmount", fineAmount)
    query = "UPDATE Fines SET Fine_amt = '" + \
        str(fineAmount) + "' WHERE Loan_id = '"+loan_id + \
        "' and fine_amt < '"+str(fineAmount)+"'"
    cursor.execute(query)

    return fineAmount if fineAmount > 0 else 0


def checkin(request):
    print("inside checkin fn")
    loan_id = request.POST['loanId']
    isbn = request.POST['isbn']
    message = ""

    query = "SELECT DATEDIFF(CURDATE(),Due_date) FROM Book_Loans WHERE Book_Loans.Loan_id = '"+loan_id+"'"
    cursor.execute(query)
    days = cursor.fetchone()[0]
    print(days, loan_id)
    fineAmount = calculateFine(days, loan_id)
    query = "UPDATE Book_Loans SET Date_in = CURDATE() WHERE Loan_id = '" + \
        loan_id + "'"
    cursor.execute(query)

    cursor.execute(
        "UPDATE Book SET Available = '1' WHERE Isbn = '"+isbn+"'")

    message = "Checked-In successfully. The fine amount for this book is: $"

    return render(request, 'checkinIndex.html', {"message": message, "fineAmount": fineAmount})
