-- ISYS2120 Assignment 3 Database

-- Note: This uses PostgreSQL's non-standard MONEY data type.
-- NUMERIC or DECIMAL is an acceptable alternative in these cases.

-- Note however that it is a bad idea to store monetary values as
-- floating point numbers due to rounding errors, so using REAL et al
-- should be avoided in such cases.

DROP TABLE IF EXISTS Model CASCADE;
DROP TABLE IF EXISTS Department CASCADE;
DROP TABLE IF EXISTS Offices CASCADE;
DROP TABLE IF EXISTS ModelAllocations CASCADE;
DROP TABLE IF EXISTS Employee CASCADE;
DROP TABLE IF EXISTS EmployeePhoneNumbers CASCADE;
DROP TABLE IF EXISTS EmployeeDepartments CASCADE;
DROP TABLE IF EXISTS Device CASCADE;
DROP TABLE IF EXISTS DeviceUsedBy CASCADE;
DROP TABLE IF EXISTS Service CASCADE;
DROP TABLE IF EXISTS Repair CASCADE;

BEGIN TRANSACTION;

CREATE TABLE Model (
	manufacturer VARCHAR(20),
	modelNumber VARCHAR(10),
	description VARCHAR(300),
	weight REAL,  -- any numeric type
	PRIMARY KEY (manufacturer, modelNumber)
);

CREATE TABLE Employee (
	empid INTEGER PRIMARY KEY,
	name VARCHAR(30),
	homeAddress VARCHAR(50),
	dateOfBirth DATE,
	password VARCHAR(100)
);

CREATE TABLE Department (
	name VARCHAR(20) PRIMARY KEY,
	budget MONEY,
	manager INTEGER  REFERENCES Employee(empid) ON DELETE CASCADE-- manager of the department
);

CREATE TABLE ModelAllocations (
	manufacturer VARCHAR(20),
	modelNumber VARCHAR(10),
	department VARCHAR(20) REFERENCES Department(name),
	maxNumber INTEGER NOT NULL,
	PRIMARY KEY (manufacturer, modelNumber, department),
	FOREIGN KEY (manufacturer, modelNumber) REFERENCES Model
);

CREATE TABLE Offices (
	department VARCHAR(20) REFERENCES Department(name),
	location VARCHAR(50),
	PRIMARY KEY (department, location)
);

CREATE TABLE EmployeePhoneNumbers (
	empID INTEGER REFERENCES Employee ON DELETE CASCADE,
	phoneNumber CHAR(10),
	PRIMARY KEY (empID, phoneNumber)
);

CREATE TABLE EmployeeDepartments (
	empID INTEGER REFERENCES Employee ON DELETE CASCADE,
	department VARCHAR(20) REFERENCES Department(name),
	fraction NUMERIC NOT NULL,  -- any non-integer numeric type
	PRIMARY KEY (empID, department)
);

CREATE TABLE Device (
	deviceID INTEGER PRIMARY KEY,
	serialNumber VARCHAR(10),
	purchaseDate DATE,
	purchaseCost MONEY,
	manufacturer VARCHAR(20) NOT NULL,
	modelNumber VARCHAR(10) NOT NULL,
	issuedTo INTEGER REFERENCES Employee(empID) ON DELETE CASCADE, 
	FOREIGN KEY (manufacturer, modelNumber) REFERENCES Model
);

CREATE TABLE DeviceUsedBy (
	deviceID INTEGER,
	empID INTEGER,
	PRIMARY KEY (deviceID, empID)
);

CREATE TABLE Service (
	abn NUMERIC(11) PRIMARY KEY,  -- or alternatively CHAR(11) - INTEGER is too small
	serviceName VARCHAR(20),
	email VARCHAR(300),
	owed MONEY
);

CREATE TABLE Repair (
	repairID INTEGER PRIMARY KEY,
	faultReport VARCHAR(60),
	startDate DATE,
	endDate DATE,
	cost MONEY,
	doneBy NUMERIC(11) REFERENCES Service(abn) NOT NULL,
	doneTo INTEGER REFERENCES Device(deviceID) NOT NULL
);


COMMIT;
