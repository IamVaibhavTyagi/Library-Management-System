
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.db import connection
from .models import Borrower

cursor = connection.cursor()

# Create your views here.


@login_required(login_url="login:login")
def index(request):
    if(request.method == "POST"):
        name = request.POST['Bname']
        ssn = request.POST['inputSSN']
        address = request.POST['inputAddress']
        phone = request.POST['inputPhoneNo']
        print(name, ssn, address, phone)
        fphno = "("
        for i in range(len(phone)):
            if i == 2:
                fphno += phone[i]+') '
            elif i == 5:
                fphno += phone[i]+'-'
            else:
                fphno += phone[i]
        print(fphno)
        cursor.execute("SELECT ssn FROM Borrower WHERE ssn = '" + ssn + "'")
        if (cursor.fetchone() == None):
            cursor.execute('INSERT INTO Borrower(Ssn,Bname,Address,Phone) VALUES("' +
                           ssn + '","' + name + '","' + address + '","' + fphno + '");')
            return render(request, "manageBorrower.html", {'message': "Borrower added successfully"})
        else:
            return render(request, "manageBorrower.html", {'message': "Borrower with same SSN already exist. Hence cannot add the borrower."})
    return render(request, "manageBorrower.html")
