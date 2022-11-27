Install the below stated required software/libraries to your system before running the application:

1. Windows 10
2. MySQL database
3. Python 3 and above
4. Django 3.2.16
5. mysqlclient 1.4.6
6. PyMySQL 1.0.2
7. Pandas
8. Web browser of your preference (Chrome/Edge/Mozilla)

Steps to execute the application:

1. Check the Backend: 

Check whether MySQL is installed properly and running. You can check that by going to command line and type "mysql -u root -p" 
OR 
by directly going to the MySQL command line tool.

2. Extract the project folder.

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

