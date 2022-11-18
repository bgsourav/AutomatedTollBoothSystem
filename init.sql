CREATE USER 'ADMIN01'@'localhost' IDENTIFIED BY 'ADMIN1';
CREATE USER 'ADMIN02'@'localhost' IDENTIFIED BY 'ADMIN2';

GRANT ALL PRIVILEGES ON *.* TO 'ADMIN01'@'localhost';
GRANT ALL PRIVILEGES ON *.* TO 'ADMIN02'@'localhost';
GRANT GRANT OPTION ON tollboothmanagementsystem.* TO 'ADMIN01'@'localhost';
GRANT GRANT OPTION ON tollboothmanagementsystem.* TO 'ADMIN02'@'localhost';

create user 'Staff01'@'localhost' identified by 'Staff1';
create user 'Staff02'@'localhost' identified by 'Staff2';
-- grant PRIVILEGES to be given to staff


-- Create a database for the project
create database TollBoothManagementSystem;

-- Use Database
use TollBoothManagementSystem 

--Creation of User table
create table User
(User_type bit, User_Name varchar(20),
 User_Password varchar(20), 
 PRIMARY KEY(User_Name)
 );

insert into User values
(1, 'ADMIN01', 'ADMIN01'),
(1, 'ADMIN02', 'ADMIN02'),
(0, 'STAFF01', 'STAFF01'),
(0, 'STAFF02', 'STAFF02');

-- Creation of Account_Details table
create table Account_Details
(Account_Number float(10),
 FName varchar(20), 
 LName varchar(20), 
 Balance float(10),
  PRIMARY KEY (Account_Number));

insert into Account_Details values
(10001, 'JOHN', 'DOE', 500),
(10002, 'JANE', 'PETERS', 1040.50),
(10003, 'MATT', 'SMITH', 100.23),
(10004, 'STEVEN', 'KING', 0),
(10006, 'JHON', 'WICK', 144.23);

-- Creation of Fare Table
create table Fare_Table 
(Vehicle_Type varchar(20),
Toll_Price float(10),
PRIMARY key(Vehicle_Type));

insert into Fare_Table values
("Short_vehicle", 50), 
("Two_axle_truck",75),
 ("Three_axle_truck",100),
("Four_axle_truck",150);

-- Creation of Vehicle_Details table
create table Vehicle_Details
(Check_Flag int, Vehicle_Type varchar(20),
 Registration_Number varchar(20),
 PRIMARY KEY(Registration_Number),
FOREIGN KEY(Vehicle_Type) REFERENCES Fare_Table(Vehicle_Type) );

insert into Vehicle_Details values
(2, 'Short_vehicle', 'NY0987'),
(1, 'Two_axle_truck', 'ATL231'),
(0, 'Four_axle_truck', 'CH6540'),
(0, 'Four_axle_truck', 'KA5872'),
(0, 'Three_axle_truck', 'HW4105');


-- Creation of Toll_Booth table
create table Toll_Booth
(Toll_Booth_No int, Operator varchar(20),
 Toll_Revenue int,
 PRIMARY KEY(Toll_Booth_No));

insert into Toll_Booth values 
(1, 'OPERATOR1', 1163),
(2, 'OPERATOR2', 1239),
(3, 'OPERATOR3', 150),
(4, 'OPERATOR4', 600);

-- Creation of Transaction_Details table
create table Transaction_Details
(Transaction_ID varchar(20),
 Account_Number float(10),
 Phone_Number float(10),
 Registration_Number varchar(20),
 PRIMARY KEY(Transaction_ID),
 FOREIGN KEY(Account_Number) REFERENCES Account_Details(Account_Number),
 FOREIGN KEY(Registration_Number) REFERENCES Vehicle_Details(Registration_Number));

insert into Transaction_Details values
('TR120001', 10001, 6453178874, 'NY0987'),
('TR120024', 10002, 9962378498, 'ATL231'),
('TR008732', 10003, 7894569325, 'CH6540'),
('TR450067', 10001, 7649193298, 'NY0987'),
('TR450013', 10004, 1122334455, 'KA5872'),
('TR450034', 10006, 9988776655, 'HW4105');


Create table Access
(Registration_Number varchar(20),
Toll_Booth_No int,
FOREIGN KEY (Registration_Number) REFERENCES Vehicle_Details(Registration_Number),
FOREIGN KEY (Toll_Booth_No) REFERENCES Toll_Booth(Toll_Booth_No));

insert into Access values 
('HW4105', 1),
('NY0987', 3);

Create table Uses
(Toll_Booth_No int, User_Name varchar(20),
 FOREIGN KEY (Toll_Booth_No) REFERENCES Toll_Booth(Toll_Booth_No),
 FOREIGN KEY (User_Name) REFERENCES User(User_Name));

insert into Uses values
(1, 'STAFF01'),
(3,'STAFF02');
