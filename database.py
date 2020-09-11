#!/usr/bin/env python3
"""
DeviceManagement Database module.
Contains all interactions between the webapp and the queries to the database.
"""

import configparser
import datetime

import setup_vendor_path  # noqa
import pg8000

################################################################################
#   Welcome to the database file, where all the query magic happens.
#   My biggest tip is look at the *week 9 lab*.
#   Important information:
#       - If you're getting issues and getting locked out of your database.
#           You may have reached the maximum number of connections.
#           Why? (You're not closing things!) Be careful!
#       - Check things *carefully*.
#       - There may be better ways to do things, this is just for example
#           purposes
#       - ORDERING MATTERS
#           - Unfortunately to make it easier for everyone, we have to ask that
#               your columns are in order. WATCH YOUR SELECTS!! :)
#   Good luck!
#       And remember to have some fun :D
################################################################################


#####################################################
#   Database Connect
#   (No need to touch
#       (unless the exception is potatoing))
#####################################################

def database_connect():
    """
    Connects to the database using the connection string.
    If 'None' was returned it means there was an issue connecting to
    the database. It would be wise to handle this ;)
    """
    # Read the config file
    config = configparser.ConfigParser()
    config.read('config.ini')
    if 'database' not in config['DATABASE']:
        config['DATABASE']['database'] = config['DATABASE']['user']

    # Create a connection to the database
    connection = None
    try:
        # Parses the config file and connects using the connect string
        connection = pg8000.connect(database=config['DATABASE']['database'],
                                    user=config['DATABASE']['user'],
                                    password=config['DATABASE']['password'],
                                    host=config['DATABASE']['host'])
    except pg8000.OperationalError as operation_error:
        print("""Error, you haven't updated your config.ini or you have a bad
        connection, please try again. (Update your files first, then check
        internet connection)
        """)
        print(operation_error)
        return None

    # return the connection to use
    return connection


#####################################################
#   Query (a + a[i])
#   Login
#####################################################

def check_login(employee_id, password):
    """
    Check that the users information exists in the database.
        - True => return the user data
        - False => return None
    """

    #check connection
    conn = database_connect()
    if(conn is None):
        return None
    cur = conn.cursor()
    #if connection success
    try:
        # Try executing the SQL and get from the database
        sql = """SELECT *
                 FROM employee
                 WHERE empid=%s AND password=%s"""
        cur.execute(sql, (employee_id, password))
        # fetch the row using given id and pw
        r = cur.fetchone()              # Fetch the first row
        cur.close()                     # Close the cursor
        conn.close()                    # Close the connection to the db
        emp_info={
            'empid': r[0],
            'name': r[1],
            'homeAddress': r[2],
            'dateOfBirth': r[3]
        }
        return emp_info
    except:
        # If there were any errors, return a NULL row printing an error to the debug
        print("Error Invalid Login")
    cur.close()                     # Close the cursor
    conn.close()                    # Close the connection to the db
    return None


#####################################################
#   Query (f[i])
#   Is Manager?
#####################################################

def is_manager(employee_id):
    """
    Get the department the employee is a manager of, if any.
    Returns None if the employee doesn't manage a department.
    """

    # TODO Dummy Data - Change to be useful!
    # check connection
    conn = database_connect()
    if conn is None:
        return None
    cur = conn.cursor()
    # if connection success
    # Try executing the SQL and get from the database
    sql = """SELECT name
                 FROM Department
                 WHERE manager=%s"""
    cur.execute(sql, (str(employee_id),))
    # fetch the row using given id and pw
    r = cur.fetchone()  # Fetch the first row
    cur.close()  # Close the cursor
    conn.close()  # Close the connection to the db
    if not r:
        return None
    return r[0]


#####################################################
#   Query (a[ii])
#   Get My Used Devices
#####################################################

def get_devices_used_by(employee_id):
    """
    Get a list of all the devices used by the employee.
    """
    # check connection
    conn = database_connect()
    if conn is None:
        return None
    cur = conn.cursor()
    r = None
    # if connection success
    try:
        cur.execute("""SELECT B.deviceID,B.modelNumber,B.manufacturer FROM DeviceUsedBy A JOIN Device B ON A.deviceID = B.deviceID
                     WHERE empID="""+str(employee_id))
        r = cur.fetchall()
    except:
        print ('invalid fatch')
    cur.close()                     # Close the cursor
    conn.close()                    # Close the connection to the db
    return r


def get_search(employee_id):
    """
    Get a list of all the devices used by the employee.
    """
    # check connection
    conn = database_connect()
    if conn is None:
        print("r3")
        return None
    cur = conn.cursor()
    r = None
    # if connection success
    try:
        cur.execute("""SELECT phoneNumber from Employeephonenumbers
                     WHERE empID=%s""", (employee_id, ))
    except:
        print("r1")
        cur.close()  # Close the cursor
        conn.close()
        return None
    r = cur.fetchone()
    if not r:
        print("r2")
        cur.close()  # Close the cursor
        conn.close()
        return None
    cur.close()                     # Close the cursor
    conn.close()                    # Close the connection to the db
    search_result={
        'mobilenumber': r[0]
    }

    return search_result

#####################################################
#   Query (a[iii])
#   Get departments employee works in
#####################################################


def employee_works_in(employee_id):
    """
    Return the departments that the employee works in.
    """

    # TODO Dummy Data - Change to be useful!
    # Return a list of departments
    # check connection
    conn = database_connect()
    if conn is None:
        return None
    cur = conn.cursor()
    r = None
    # if connection success
    try:
        cur.execute("SELECT department FROM EmployeeDepartments WHERE empID=" + str(employee_id))
        r = cur.fetchall()
    except:
        cur.close()  # Close the cursor
        conn.close()  # Close the connection to the db
        return None
        print ('invalid fetch')
    if not r:
        return None
    cur.close()  # Close the cursor
    conn.close()  # Close the connection to the db
    return r[0]


#####################################################
#   Query (c)
#   Get My Issued Devices
#####################################################

def get_issued_devices_for_user(employee_id):
    """
    Get all devices issued to the user.
        - Return a list of all devices to the user.
    """

    # TODO Dummy Data - Change to be useful!
    # Return a list of devices issued to the user!
    # Each "Row" contains [ deviceID, purchaseDate, manufacturer, modelNumber ]
    # If no devices = empty list []
    # check connection
    conn = database_connect ()
    if conn is None:
        return None
    cur = conn.cursor ()
    r = None
    # if connection success
    try:
        cur.execute ("SELECT * FROM Device WHERE issuedTo=" + str(employee_id))
        r = cur.fetchall ()
    except:
        print ('invalid fatch')
    cur.close ()  # Close the cursor
    conn.close ()  # Close the connection to the db
    return r
    # devices = [
    #     [7, datetime.date(2017, 8, 28), 'Zava', '1146805551'],
    #     [8, datetime.date(2017, 9, 22), 'Topicware', '5798231046'],
    #     [6123, datetime.date(2017, 9, 5), 'Dabshots', '6481799600'],
    #     [1373, datetime.date(2018, 4, 19), 'Cogibox', '6700815444'],
    #     [8, datetime.date(2018, 2, 10), 'Feednation', '2050267274'],
    #     [36, datetime.date(2017, 11, 5), 'Muxo', '8768929463'],
    #     [17, datetime.date(2018, 1, 14), 'Izio', '5886976558'],
    #     [13, datetime.date(2017, 9, 8), 'Skyndu', '5296853075'],
    #     [24, datetime.date(2017, 10, 22), 'Yakitri', '8406089423'],
    # ]
    #
    # return devices


#####################################################
#   Query (b)
#   Get All Models
#####################################################

def get_all_models():
    """
    Get all models available.
    """
    # Return the list of models with information from the model table.
    # Each "Row" contains: [manufacturer, description, modelnumber, weight]
    # If No Models = EMPTY LIST []
    s = 'SELECT manufacturer, description, modelnumber, weight FROM model'
    conn = database_connect()
    if conn is None:
        return None
    cur = conn.cursor()
    cur.execute(s)
    models = cur.fetchall()
    cur.close()
    conn.close()
    return models


#####################################################
#   Query (d[ii])
#   Get Device Repairs
#####################################################

def get_device_repairs(device_id):
    """
    Get all repairs made to a device.
    """

    # TODO Dummy Data - Change to be useful!
    # Return the repairs done to a certain device
    # Each "Row" contains:
    #       - repairid
    #       - faultreport
    #       - startdate
    #       - enddate
    #       - cost
    # If no repairs = empty list
    conn = database_connect()
    if conn is None:
        return None
    cur = conn.cursor()
    r = None
    # if connection success
    try:
        cur.execute("SELECT repairID, faultReport, startDate, endDate, cost FROM Repair WHERE doneTo=" + str(device_id))
        r = cur.fetchall()
    except:
        print('invalid fatch')
    cur.close()  # Close the cursor
    conn.close()  # Close the connection to the db
    return r


#####################################################
#   Query (d[i])
#   Get Device Info
#####################################################

def get_device_information(device_id):
    """
    Get related device information in detail.
    """

    # TODO Dummy Data - Change to be useful!
    # Return all the relevant device information for the device
    conn = database_connect()
    if conn is None:
        return None
    cur = conn.cursor()
    device = None
    # if connection success
    try:
        cur.execute (
            "SELECT * FROM Device WHERE deviceID=" + str (device_id))
        device_info = cur.fetchone()
        device = {
            'device_id': device_info[0],
            'serial_number': device_info[1],
            'purchase_date': device_info[2],
            'purchase_cost': device_info[3],
            'manufacturer': device_info[4],
            'model_number': device_info[5],
            'issued_to': device_info[6],
        }
    except:
        print('invalid fatch')
    cur.close()  # Close the cursor
    conn.close()  # Close the connection to the db

    return device


#####################################################
#   Query (d[iii/iv])
#   Get Model Info by Device
#####################################################

def get_device_model(device_id):
    conn = database_connect()
    if conn is None:
        return None
    cur = conn.cursor()
    model = None
    # if connection success
    sql = """ SELECT * FROM Model WHERE modelNumber=(SELECT modelNumber from device where deviceId=%s) 
              and manufacturer=(SELECT manufacturer from device where deviceId=%s)"""
    try:
        cur.execute(sql,(str(device_id),str(device_id)))
        model_info = cur.fetchone ()
        model = {
            'manufacturer': model_info[0],
            'model_number': model_info[1],
            'description': model_info[2],
            'weight': model_info[3],
        }
    except:
        print('invalid fatch')
    cur.close()  # Close the cursor
    conn.close()  # Close the connection to the db
    return model


#####################################################
#   Query (e)
#   Get Repair Details
#####################################################

def get_repair_details(repair_id):
    """
    Get information about a repair in detail, including service information.
    """
    s ='''SELECT R.repairID, R.faultReport,
           R.startDate, R.endDate, R.cost,
           S.abn, S.serviceName, S.email,
	       R.doneTo
	       FROM repair R JOIN service S ON R.doneBy=S.abn
	       WHERE repairid=%s'''

    conn = database_connect()

    if conn is None:
        return None
    cur = conn.cursor()
    cur.execute(s, (repair_id,))
    repair_info = cur.fetchone()
    cur.close()
    conn.close()

    repair = {
        'repair_id': repair_info[0],
        'fault_report': repair_info[1],
        'start_date': repair_info[2],
        'end_date': repair_info[3],
        'cost': repair_info[4],
        'done_by': {
            'abn': repair_info[5],
            'service_name': repair_info[6],
            'email': repair_info[7],
        },
        'done_to': repair_info[8],
    }
    return repair


#####################################################
#   Query (f[ii])
#   Get Models assigned to Department
#####################################################


def get_department_models(department_name):
    """
    Return all models assigned to a department.
    """

    # TODO Dummy Data - Change to be useful!
    # Return the models allocated to the department.
    # Each "row" has: [ manufacturer, modelnumber, maxnumber ]
    conn = database_connect()
    if conn is None:
        return None
    cur = conn.cursor()
    r = None
    # if connection success
    try:
        cur.execute(
            "SELECT manufacturer, modelnumber, maxnumber FROM ModelAllocations WHERE department=%s ", (department_name,))
        r = cur.fetchall()
    except Exception as e:
        raise e
        print('invalid fatch f')
    cur.close()  # Close the cursor
    conn.close()  # Close the connection to the db
    return r

#####################################################
#   Query (f[iii])
#   Get Number of Devices of Model owned
#   by Employee in Department
#####################################################


def get_employee_department_model_device(department_name, manufacturer, model_number):
    """
    Get the number of devices owned per employee in a department
    matching the model.

    E.g. Model = iPhone, Manufacturer = Apple, Department = "Accounting"
        - [ 1337, Misty, 20 ]
        - [ 351, Pikachu, 10 ]
    """

    # TODO DEBUG
    # Return the number of devices owned by each employee matching department,
    #   manufacturer and model.
    # Each "row" has: [ empid, name, number of devices issued that match ]
    s = '''
    SELECT E.empid, E.name, COUNT(D.deviceID)
    FROM Employee E
        JOIN EmployeeDepartments ED USING (empID)
        JOIN Device D ON D.issuedTo=empID
    WHERE ED.department=%s
          AND D.manufacturer=%s
          AND modelNumber=%s
    GROUP BY E.empid
    '''
    conn = database_connect()
    cur = conn.cursor()
    arg = (department_name, manufacturer, model_number)
    cur.execute(s, arg)
    r = cur.fetchall()
    cur.close()
    conn.close()
    return r if r else []

#####################################################
#   Query (f[iv])
#   Get a list of devices for a certain model and
#       have a boolean showing if the employee has
#       it issued.
#####################################################


def get_model_device_assigned(model_number, manufacturer, employee_id):
    """
    Get all devices matching the model and manufacturer and show True/False
    if the employee has the device assigned.

    E.g. Model = Pixel 2, Manufacturer = Google, employee_id = 1337
        - [123656, False]
        - [123132, True]
        - [51413, True]
        - [8765, False]
    """
    # Return each device of this model and whether the employee has it
    # issued.
    # Each "row" has: [ device_id, True if issued, else False.]

    s = """
    SELECT deviceID, issuedTo=%s
    FROM Device
    WHERE modelNumber=%s
        AND manufacturer=%s
    """
    conn = database_connect()
    cur = conn.cursor()
    cur.execute(s, (employee_id, model_number, manufacturer))
    r = cur.fetchall()
    cur.close()
    conn.close()
    return r

    #
    # device_assigned = [
    #     [123656, False],
    #     [123132, True],
    #     [51413, True],
    #     [8765, False],
    # ]
    #
    # return device_assigned


#####################################################
#   Query (f[iv])
#   Get a list of devices for this model and
#       manufacturer that have not been assigned.
#####################################################


def get_unassigned_devices_for_model(model_number, manufacturer):
    """
    Get all unassigned devices for the model.
    """

    # Return each device of this model that has not been issued
    # Each "row" has: [ device_id ]

    s = """
    SELECT deviceID
    FROM Device
    WHERE modelNumber=%s
        AND manufacturer=%s
        AND issuedTo IS null
    """
    conn = database_connect()
    cur = conn.cursor()
    cur.execute(s, (model_number, manufacturer))
    r = cur.fetchall()
    cur.close()
    conn.close()
    return r


#####################################################
#   Query (f[iv])
#   Get Employees in Department
#####################################################


def get_employees_in_department(department_name):
    """
    Return the name of all employees in the department.
    """

    # Return the employees in the department.
    # Each "row" has: [ empid, name ]
    s = '''
    SELECT E.empid, E.name
    FROM Employee E JOIN EmployeeDepartments ED USING (empID)
    WHERE department=%s
    '''
    conn = database_connect()
    cur = conn.cursor()
    cur.execute(s, (department_name,))
    r = cur.fetchall()
    cur.close()
    conn.close()
    return r

#####################################################
#   Query (f[iv])
#   Get Device Employee Assignment
#####################################################


def get_device_employee_department(manufacturer, modelNumber, department_name):
    """
    Return the list of devices and who owns them for a given model
    and department.
    """
    # Return the devices matching the manufacturer and model number in the
    #   department with the employees assigned.
    # Each row has: [ deviceid, serialnumber, empid, employee name ]

    s = '''
    SELECT D.deviceID, D.serialNumber, E.empid, E.name
    FROM Device D
        JOIN Employee E ON D.issuedTo = E.empid
        JOIN EmployeeDepartments ED USING (empID)
    WHERE D.manufacturer=%s
        AND D.modelNumber=%s
        AND D.department_name=%s
    '''
    conn = database_connect()
    cur = conn.cursor()
    cur.execute(s, (manufacturer, modelNumber, department_name))
    r = cur.fetchall()
    cur.close()
    conn.close()
    return r

#####################################################
#   Query (f[v])
#   Issue Device
#####################################################


def issue_device_to_employee(employee_id, device_id):
    """
    Issue the device to the chosen employee.
    """
    # Return (True, None) if all good
    # Else return (False, ErrorMsg)
    # Error messages:
    #       - Device already issued?
    #       - Employee not in department?
    # update if employee in department and dev not issued
    s = """
        UPDATE Device
        SET issuedTo=%s
        WHERE deviceID=%s
            AND issuedTo IS null
            AND EXISTS
                (
                    SELECT TRUE
                    FROM ModelAllocations
                        JOIN Device D USING (manufacturer, modelNumber)
                        JOIN EmployeeDepartments ED USING (department)
                    WHERE ED.empID=%s
                        AND D.deviceID=%s
                ) """
    conn = database_connect()
    cur = conn.cursor()
    cur.execute(s, (employee_id, device_id, employee_id, device_id))
    conn.commit()
    # check for successful update
    s2 = """
    SELECT issuedTo
    FROM Device
    WHERE DeviceID=%s
    """
    cur.execute(s2, (device_id,))
    r = cur.fetchone()
    if not r:
        cur.close()
        conn.close()
        print(False, 'race condition')
    r = r[0]
    if str(r) == str(employee_id):
        cur.close()
        conn.close()
        return (True, None)
    elif r is None:
        cur.close ()
        conn.close ()
        return (False, 'Employee not in department')
    else:
        cur.close()
        conn.close()
        return (False, 'Device already issued')

#####################################################
#   Query (f[vi])
#   Revoke Device Issued to User
#####################################################


def revoke_device_from_employee(employee_id, device_id):
    """
    Revoke the device from the employee.
    """

    # TODO revoke the device from the employee.
    # Return (True, None) if all good
    # Else return (False, ErrorMsg)
    # Error messages:
    #       - Device already revoked?
    #       - employee not assigned to device?

    # return (False, "Device already unassigned")
    s = """
            UPDATE Device
            SET issuedTo= null 
            WHERE deviceID=%s
                AND issuedTo=%s"""
    conn = database_connect()
    cur = conn.cursor()
    cur.execute(s, (device_id, employee_id))
    conn.commit()
    # check revoked
    s2 = """
        SELECT issuedTo
        FROM Device
        WHERE DeviceID=%s
        """
    cur.execute(s2, (device_id,))
    r = cur.fetchone()
    if r[0] is not None:
        print(r)
        cur.close()
        conn.close()
        return (False, 'mork')
    else:
        cur.close()
        conn.close()
        return (True, None)
        
#####################################################
#   Query (ex-1)
#   Remove employee
#####################################################


def remove_employee(employee_id):
    """
    Revoke the device from the employee.
    """

    # TODO revoke the device from the employee.
    # Return (True, None) if all good
    # Else return (False, ErrorMsg)
    # Error messages:
    #       - Device already revoked?
    #       - employee not assigned to device?

    # return (False, "Device already unassigned")
    t="""UPDATE Department
            SET manager= null 
            WHERE manager=%s
        """

    t1="""UPDATE Device
            SET issuedTo = null 
            WHERE issuedTo=%s"""

    s = """
            DELETE FROM employee CASCADE
            WHERE empid=%s
            """
    conn = database_connect()
    cur = conn.cursor()
    cur.execute (t, (str (employee_id),))
    cur.execute (t1, (str (employee_id),))
    cur.execute(s,  (str(employee_id),))
    conn.commit()
    # check revoked
    s2 = """
        SELECT *
        FROM employee
        WHERE empid=%s
        """
    cur.execute(s2, (str(employee_id),))
    r = cur.fetchone()
    if r is not None:
        print(r)
        cur.close()
        conn.close()
        return (False, 'mork')
    else:
        cur.close()
        conn.close()
        return (True, None)

#####################################################
#   Query Part C (Extension - Data Entry)
#   Add employee    
#####################################################

def add_employee(employee_info):
    """
    Issue the device to the chosen employee.
    """
    # Return (True, None) if all good
    # Else return (False, ErrorMsg)
    # Error messages:
    #       - Device already issued?
    #       - Employee not in department?
    conn = database_connect()
    cur = conn.cursor()
    print('empid', employee_info[0], 'name', employee_info[1], 'homeaddress', employee_info[2], 'dateofbirth', employee_info[3], 'password', employee_info[4])

    # check if employee does not exist
    s1 ='''
    SELECT TRUE
    FROM Employee
    WHERE empid = %s
    '''
    cur.execute(s1, (employee_info[0],))
    exists = True if cur.fetchone() else False
    if exists:
        cur.close()
        conn.close()
        return (False, "Employee already exists in database.")

    # Add employee to database
    s2 = '''
        INSERT INTO Employee
        VALUES (%s, %s, %s, %s, %s)
        '''
    conn = database_connect()
    cur = conn.cursor()
    cur.execute(s2, (employee_info[0], employee_info[1], employee_info[2], employee_info[3], employee_info[4]))
    conn.commit()
    
    # check for successful update
    s3 = """
    SELECT *
    FROM Employee
    WHERE empid = %s
       AND name = %s
       AND homeaddress = %s
       AND dateofbirth = %s
       AND password = %s
    """
    cur.execute(s3, (employee_info[0], employee_info[1], employee_info[2], employee_info[3], employee_info[4]))
    r = cur.fetchone()

    for result in r:
        if result not in employee_info:
            cur.close()
            conn.close()
            return (False, 'Unsuccessful in adding employee. Possible missing information.')
    
    cur.close()
    conn.close()
    return (True, None)