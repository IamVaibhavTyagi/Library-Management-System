# Library Management System
A Django application to maintain books in the library.

## Programming Languages and Libraries used:
This is the list of programming languages, libraries, web framework and database used.
- Web Framework: Django
- Languages: Python, SQL, HTML, CSS, Bootstrap
- Libraries: Pandas, PyMySQL, mysqlclient
- Database: MySQL

## Architecture:
Below is the architecture diagram of the system:

![image](https://user-images.githubusercontent.com/39727591/210276418-1d83018c-7df2-429b-b459-160e980097c2.png)

At the backend, we have MySQL database to store all the data related to the books and borrowers. This data can be only accessed through middleware and not directly by the user.

Then we have a middleware where all the business logic is written. It consists of multiple apps (modules) for each required functionality. As you can see, we have, Login app to manage the authentication of the user. Then we have Search Book app which can be used to search a book and then check it out. We also have a separate app to check in the book. There is also a Pay fine app which is used to refresh the fines, pay the fines and list the users with unpaid and paid fines. Lastly, we got borrower management app which is used to add the new borrower information.

All the above functionalities are accessed with the help of a GUI (frontend), through which the user interacts and gives their input as per requirement to carry out some function.

Further, the interaction between all the layers is bi-directional. The flow of data happens both ways between given two layers.

### Upon starting the application, the user will see the first page as a Login screen.

## Login:

![image](https://user-images.githubusercontent.com/39727591/210275884-7b139095-0472-4c7a-9ea4-258f8f739741.png)

On the login screen the user will asked to enter their credentials to access the library management system. They will be logged-in into the system if the credentials are correct or an error message will be shown to enter the correct credentials.

![image](https://user-images.githubusercontent.com/39727591/210275913-2bb037d8-6cd6-4307-98cf-d35e8ef507b5.png)

The user won’t be able to access the system unless they login with the correct username and password.


## Sign Up:

![image](https://user-images.githubusercontent.com/39727591/210275951-c2831d16-67f8-484f-a02e-aaa9da42cb70.png)

If a user is not registered then, they can register themselves with the sign up button and access the library management system.

![image](https://user-images.githubusercontent.com/39727591/210275964-9c9798d1-91da-4cee-8d23-96bcf17ed724.png)


Incase there is an error while registering the error will be shown to the user and they can correct the registration information.

![image](https://user-images.githubusercontent.com/39727591/210275972-cd1bfbf6-cbbe-4827-aae7-66300570ffa5.png)


After successful sign up/login the user will be directed to the home page of the book search.

## Book Search:
User will be directed to book search after successfully authenticating themselves. On this page the user can search any book in the system by entering the Book Name, Book ISBN, or Author Name.

![image](https://user-images.githubusercontent.com/39727591/210276020-becec01e-46c9-4ac5-a6a1-08bc22729301.png)

For example, if “Harry Potter” is searched then all the results consisting of Harry Potter in the title will be displayed to the user. Additionally, the user will be able to navigate to
other functionalities at all times when logged into the system through the navigation bar at the top.

## Check-Out:
After searching for the book, the user will be able to check-out a book in the search result by clicking on “Check Out” button respectively for each book.
![image](https://user-images.githubusercontent.com/39727591/210276061-9d31bcc9-81a8-46c3-8fe1-f6f699ba21c9.png)

A prompt will be displayed asking for the borrower’s card no to be entered. A book will be successfully checkout if it meets the requirements given in the instructions such as, if the book is available or if the borrower hasn’t borrowed three books already.
![image](https://user-images.githubusercontent.com/39727591/210276069-f6dfaf10-e51c-48ea-b56b-4d1c21522a4f.png)

Upon successfully checking out the book, the system will display a success message. If it fails then a failing message.
## Check-In:
![image](https://user-images.githubusercontent.com/39727591/210276077-28f5c688-e9a3-4f4e-9d6b-0f24d9efb45a.png)

The books can be checked in, by going to the check-in page and searching for the book name, borrower name or borrower card no. If a book/User has a book checked out then the search results will be displayed accordingly, else a no book found message will be displayed.
![image](https://user-images.githubusercontent.com/39727591/210276107-799193c3-7e24-4074-af26-94f10dfa0b28.png)

After checking-in a book a success message will be displayed along with the fine amount.

## Pay fines:
![image](https://user-images.githubusercontent.com/39727591/210276133-d35f1888-f9f2-437d-8a5d-8ba2e2e555bc.png)

![image](https://user-images.githubusercontent.com/39727591/210276141-2105a4c2-c19e-4944-abb7-948b2f88f389.png)

There is a pay fine functionality which can be used by the librarian to refresh the fine amount and mark the fine to paid if it is paid by the borrower. It also provides with a button to filter and display all the fines that were paid previously.
A fine can not be paid until all books issued by the borrower are returned. Appropriate messages will be displayed to user incase of any failure or success.

## Add borrower:
![image](https://user-images.githubusercontent.com/39727591/210276157-33f687df-10ea-457a-a7ec-3199c5c40f65.png)

A borrower can be added through this page. The form will ask basic details about the borrower and add it to the database.
Further in the navigation bar, a functionality to logout out of the system will be provided to the user at all times. Once logged out of the system the system will take the user back to login page and ask for the credentials again to access the system.
![image](https://user-images.githubusercontent.com/39727591/210276165-a6a8e8eb-b57e-4741-b40c-19e7f839ce82.png)


## Install the below stated required software/libraries to your system before running the application:

1. Windows 10
2. MySQL database
3. Python 3 and above
4. Django 3.2.16
5. mysqlclient 1.4.6
6. PyMySQL 1.0.2
7. Pandas
8. Web browser of your preference (Chrome/Edge/Mozilla)

### Steps to execute the application:

1. Check the Backend: 

Check whether MySQL is installed properly and running. You can check that by going to command line and type "mysql -u root -p" 
OR 
by directly going to the MySQL command line tool.

2. Extract the project folder. Activate the virtual env using - env\Scripts\activate

3. Open the folder and go to dbConfig.json. Enter your database details such as username and password. Save it

4. Open the createSchema.py file and run the code to create a new database.

Check path of dbConfig file before running the code. If any error, replace dbCongif file path with the complete file path of dbConfig file in the createSchema file.

5. open intializeTablesData.py file and run the code to initialize the tables with the data.
 
Check path of book.csv and borrower.csv file before running the code. If any error, replace path with the complete file path of book.csv and borrower.csv file in the intializeTablesData file.

6. After creating the schema, Go to LibraryManagementSystem\LibraryManagementSystem\settings.py and change the DATABASES config as per your username/password.

7. Then Go to LibraryManagementSystem and locate the manage.py file

execute the below command as following:

- python manage.py makemigrations
- python manage.py migrate
- python manage.py createsuperuser

create a superuser with a username and password, which can be later used to login into the system.

8. Run the command below to start the server.

- python manage.py runserver

This should start your server with a message to go to 127.0.0.1:8000 

9. Go to web browser of your choice and go to URL 127.0.0.1:8000

You should see a login page. Use the super user credentials created in the previous step to login and use the web application.

