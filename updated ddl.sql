--Creation of User table
create table User(User_type bit, User_Name varchar(20), User_Password varchar(20), PRIMARY KEY(User_Name));

-- Creation of Toll_Booth table
create table Toll_Booth(Toll_Booth_No int, Operator varchar(20), Toll_Revenue float(20), U_Name varchar(20), PRIMARY KEY(Toll_Booth_No), FOREIGN KEY(U_Name) REFERENCES USER(User_Name));

-- Creation of Account_Details table
create table Account_Details(Account_Number float(10), FName varchar(20), LName varchar(20), Balance float(10), PRIMARY KEY (Account_Number));

-- Creation of Transaction_Details table
create table Transaction_Details(Transaction_ID varchar(20), A_NO float(10),Phone_Number float(10), PRIMARY KEY(Transaction_ID),FOREIGN KEY(A_NO) REFERENCES Account_Details(Account_Number));

ALTER TABLE Account_Details
ADD FOREIGN KEY (Transact_ID) REFERENCES Transaction_Details(Transaction_ID);

-- Creation of Fare Table
create table FARE(CLASS varchar(20), PRICE FLOAT(20), PRIMARY KEY(CLASS,PRICE));

-- Creation of Vehicle_Details table
create table Vehicle_Details(Check_Flag bit, Vehicle_Type varchar(20), Registration_Number varchar(20), Toll_Price float(20), Transact_ID varchar(20), PRIMARY KEY(Registration_Number), FOREIGN KEY (Transact_ID) REFERENCES Transaction_Details(Transaction_ID), FOREIGN KEY(Vehicle_Type,Toll_Price) REFERENCES FARE(CLASS,PRICE));

--Creation of Relation access 
Create table Access(RN_NO varchar(20),TB_NO int,TIME_STAMP DATETIME, FLAG bit, Vehicle_Type Varchar(20), Toll_Price float(20), Operator varchar(20), Revenue float(20),FOREIGN KEY (RN_NO) REFERENCES Vehicle_Details(Registration_Number), FOREIGN KEY (TB_NO) REFERENCES Toll_Booth(Toll_Booth_No));

