from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.db import connection
from .models import Borrower, BookLoans, Fines

from django.core.paginator import Paginator, EmptyPage

cursor = connection.cursor()

# Create your views here.


@login_required(login_url="login:login")
def index(request):
    print("inside payFine index")
    searchValue = False
    global fine_list
    if(request.method == "POST"):
        if('payFineBox' in request.POST and request.POST['payFineBox'] != ''):
            words = request.POST['payFineBox'].split(',')
            condition = ""
            for word in words:
                word = word.strip()
                word = "%"+word+"%"
                if condition != "":
                    condition += "AND"
                condition += "(borrowerFine.Card_id LIKE '"+word+"' OR borrowerFine.Ssn LIKE '" + \
                    word+"' OR borrowerFine.Bname LIKE '"+word+"')"

            query = "SELECT borrowerFine.Card_id, borrowerFine.Ssn, borrowerFine.Bname, borrowerFine.Totalfine, borrowerFine.Loan_id FROM (SELECT Borrower.Card_id, Borrower.Ssn, Borrower.Bname, SUM(Fines.Fine_amt) Totalfine, Book_Loans.Loan_id FROM Borrower,Book_Loans,Fines WHERE Borrower.Card_id = Book_Loans.Card_id AND Book_Loans.Loan_id = Fines.Loan_id AND Fines.Paid = '0' GROUP BY Borrower.Card_id) AS borrowerFine WHERE "+condition
            cursor.execute(query)
            fine_list = list(cursor.fetchall())
            print(fine_list)
            p = Paginator(fine_list, 6)

            page = p.get_page(1)
            return render(request, 'payFine.html', {"page": page, "flag": False, "totalpages": p.num_pages, "searchValue": True, 'books_list': fine_list})
        elif ('paidfinesbtn' in request.POST):
            query = "SELECT borrowerFine.Card_id, borrowerFine.Ssn, borrowerFine.Bname, borrowerFine.Totalfine, borrowerFine.Loan_id FROM (SELECT Borrower.Card_id, Borrower.Ssn, Borrower.Bname, SUM(Fines.Fine_amt) Totalfine, Book_Loans.Loan_id FROM Borrower,Book_Loans,Fines WHERE Borrower.Card_id = Book_Loans.Card_id AND Book_Loans.Loan_id = Fines.Loan_id AND Fines.Paid = '1' GROUP BY Borrower.Card_id) AS borrowerFine"
            cursor.execute(query)
            fine_list = list(cursor.fetchall())
            print(fine_list)
            p = Paginator(fine_list, 6)

            page = p.get_page(1)
            return render(request, 'payFine.html', {"page": page, "flag": False, "totalpages": p.num_pages, "searchValue": True, 'books_list': fine_list})
        else:
            print("Search text box is Empty!")
            return render(request, "payFine.html", {"searchValue": searchValue, "flag": False})
    elif (request.method == "GET"):
        if 'previousbtn' in request.GET or 'nextbtn' in request.GET or 'firstbtn' in request.GET or 'lastbtn' in request.GET:
            print("inside else of search")
            print(request.GET.get('nextbtn'))
            print(request.GET.get('previousbtn'))
            print(request.GET.get('firstbtn'))
            print(request.GET.get('lastbtn'))
            print(fine_list[:10])

            p = Paginator(fine_list, 6)

            page_num = request.GET.get(
                'nextbtn') if 'nextbtn' in request.GET else request.GET.get('previousbtn') if 'previousbtn' in request.GET else request.GET.get('firstbtn') if 'firstbtn' in request.GET else request.GET.get('lastbtn')
            page = p.get_page(page_num)

            return render(request, "payFine.html", {"page": page, "flag": False, "totalpages": p.num_pages, "searchValue": True})
    return render(request, "payFine.html", {"searchValue": searchValue, "flag": True})


def refreshFines(request):

    # For books that are not returned yet
    cursor.execute(
        "SELECT Loan_id, DATEDIFF(CURDATE(),Due_date)*0.25 difference FROM Book_Loans WHERE DATEDIFF(CURDATE(),Due_date)*0.25 > 0 and Date_in IS NULL")
    results = cursor.fetchall()
    for result in results:
        # cursor.execute("SELECT Loan_id FROM Fines WHERE Loan_id = '" +
        #                str(result[0])+"'")
        # if(cursor.fetchone() == None):
        #     query = "INSERT INTO Fines(Loan_id,Fine_amt,Paid) VALUES('" + \
        #         str(result[0]) + "', '"+str(result[1])+"', '0')"
        #     cursor.execute(query)
        # else:
        query = "UPDATE Fines SET Fines.Fine_amt = '" + \
            str(result[1])+"' WHERE Fines.Loan_id = '" + \
            str(result[0])+"' AND Fines.Paid = '0'"
        cursor.execute(query)

    return render(request, "payFine.html", {'message': "Successfully Refreshed Fines"})


def makePayment(request):
    cardno = request.POST['cardno']

    cursor.execute(
        "SELECT count(Loan_id) FROM Book_Loans WHERE Card_id = '"+str(cardno)+"'")
    totalbook = cursor.fetchall()
    print(totalbook[0][0])
    cursor.execute(
        "SELECT Loan_id FROM Book_Loans WHERE Date_in IS NOT NULL AND Card_id = '"+str(cardno)+"'")
    loan_ids = cursor.fetchall()
    print(len(loan_ids))

    if len(loan_ids) < totalbook[0][0]:
        return render(request, "payFine.html", {'message': "Return/Check-In all the books borrowed before paying the fine."})
    else:
        for loanid in loan_ids:
            if cursor.execute("UPDATE Fines SET Fines.Paid = '1' WHERE Fines.Loan_id = '" +
                              str(loanid[0])+"' AND Fines.Paid = '0'") == 0:
                return render(request, "payFine.html", {'message': "Fine already paid."})
        return render(request, "payFine.html", {'message': "Successfully Paid fine."})
