-- this is used for creation of a user
create USER 'me' IDENTIFIED BY '1234';
-- Create a database for the project
create database TollBoothManagementSystem;
 -- Grant Permissions ******** IMPORTANT ******** skipped  ** https://www.javatpoint.com/mysql-create-user
 use TollBoothManagementSystem;
 --Creation of fare table
 create table Fare_Details(Type varchar(40),Fare integer,PRIMARY KEY(Type));
 --Insertion of values into the table
 insert into Fare_Details values('Class 1',35),('Class 2',45),('Class 3',60),('Class 4',135),('Class 5','195'),('Class 6',195),('Class 7',195),('Class 8',195),('Class 9',210),('Class 10',235),('Class 11',250),('Class 12',325);
 
