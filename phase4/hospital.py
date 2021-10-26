from os import initgroups
import subprocess as sp
import pymysql
import pymysql.cursors

gender_list = ["M", "F", "O"]
blood_group_list = ["A-", "A+", "B+", "B-", "O+", "O-", "AB-", "AB+"]
rooms = []
last_patient_added = 10
last_medical_dept_added = 5
last_doctor_added = 9
last_nurse_added = 3
last_labtech_added = 5
last_employee_added = 5

def option2():
    """
    Function to implement option 1
    """
    print("Not implemented")


def option3():
    """
    Function to implement option 2
    """
    print("Not implemented")


def option4():
    """
    Function to implement option 3
    """
    print("Not implemented")


def count_num_digits(number):
    dig = 0
    while number != 0:
        number /= 10
        dig = dig + 1
    return dig
      
def InitBedsList():
    query= "SELECT * FROM BEDS_OCCUPIED;"
    try:
        print(query)
        cur.execute(query)
        con.commit()
        room_list = cur.fetchall()
        DisplayQuery(room_list)
        for row in room_list:
            rooms[int(row["BED_NUMBER"])] = int(row["OCCUPIED"])
            
    except Exception as e:
        con.rollback()
        print("Failed to retrieve rooms data")
        print(">>>>>>>>>>>>>", e)
        exit(1)
      
def DisplayQuery(fetched_results):
    if len(fetched_results) == 0:
        return 0
    else:
        for row in fetched_results:
            print(row)
def ExecuteQuery(query):
    try:
        print(query)
        cur.execute(query)
        con.commit()
        DisplayQuery(cur.fetchall())

    except Exception as e:
        con.rollback()
        print("Failed to insert into database")
        print(">>>>>>>>>>>>>", e)
        return 0
    return 1
def AddEmergencyContact(query):
    global last_patient_added
    row = {}
    name = (input("NAME : ")).split(' ')
    row["VISITOR_NAME"] = name[0]
    row["REL_WITH_PATIENT"] = input("RELATION WITH THE PATIENT: ")
    row["PATIENT_ID"] = int(input("PATIENT ID : "))
    row["PHONE"] = input("PHONE : ")
    query += "INSERT INTO EMERGENCY_CONTACT( CONTACT_NAME ,REL_WITH_PATIENT,PATIENT_ID,PHONE) VALUES('%s', '%s','%d','%s');" % (
        row["VISITOR_NAME"], row["REL_WITH_PATIENT"], row["PATIENT_ID"], row["PHONE"])

    flag = ExecuteQuery(query)
    if flag == 1:
        print("Inserted Into Database")
    else:
        last_patient_added = last_patient_added - 1
    return
def AddDiseasePatient(id):
    patient_id = id
    disease_id = int(input("Enter Disease Id : "))
    query = "INSERT INTO DIS_PAT( PATIENT_ID ,DISEASE_ID)VALUES('%d','%d')" % (
        patient_id, disease_id)

    flag = ExecuteQuery(query)
    if flag == 1:
        print("Inserted Into Database")      
def AddOutPatient(query, id):
    query += "INSERT INTO OUT_PATIENT(PATIENT_ID) VALUES('%d');" % (id
        )
    AddEmergencyContact(query) 

def NumberOfBedsAvaialable():
    count = 0 
    for i in range(0,len(rooms)):
        if rooms[i] == 0:
            count = count + 1
    return count
        

def AddInPatient(query,id):
    beds = NumberOfBedsAvaialable()
    if beds == 0:
        print("No Beds available\npatient cant be admitted\n")
        return
        
def AddPatient():
    row = {}
    global last_patient_added
    print("Enter Patient details: ")
    name = (input("NAME (First_Name Middle_Name Last_Name): ")).split(' ')
    row["PATIENT_ID"] = last_patient_added + 1
    last_patient_added = last_patient_added + 1
    row["FIRST_NAME"] = name[0]
    row["MIDDLE_NAME"] = name[1]
    row["LAST_NAME"] = name[2]
    row["DOB"] = input("DATE OF BIRTH (YYYY-MM-DD): ")
    row["GENDER"] = input("GENDER(M/F/O): ")
    row["BLOOD_GROUP"] = input(
        "BLOOD_GROUP [A-,A+,B+,B-,O+,O-,AB-,AB+] : ")
    row["PHONE"] = (input("PHONE: "))
    patient_type = int(input("INPATIENT - 0 \nOUTPATIENT - 1\n"))
    if(patient_type != 0 or patient_type != 1):
        print("Invalid Patient Type \n")
        return
    query = "INSERT INTO PATIENT(FIRST_NAME, MIDDLE_NAME, LAST_NAME,DOB, GENDER, BLOOD_GROUP,PHONE) VALUES('%s', '%s', '%s', '%s' , '%s', '%s', '%s');" % (
        row["FIRST_NAME"], row["MIDDLE_NAME"], row["LAST_NAME"], row["DOB"], row["GENDER"], row["BLOOD_GROUP"], row["PHONE"])

    gender_count = gender_list.count(row["GENDER"])

    if gender_count == 0:
        print("Invalid Input for gender\nRecord Not added\nInvalid Input!!!\n")
        return

    blood_group_exists = blood_group_list.count(row["BLOOD_GROUP"])

    if blood_group_exists == 0:
        print("Invalid Input for blood_group\nRecord Not added\nInvalid Input!!!\n")
        return
    if patient_type == 1:
        AddOutPatient(query,row["PATIENT_ID"])
    else:
        AddInPatient(query)

    return
def AddLabTechnician():
    row = {}
    global last_labtech_added
    print("Enter Lab Technician's details: ")
    name = (input("NAME (First_Name Middle_Name Last_Name): ")).split(' ')
    row["FIRST_NAME"] = name[0]
    row["MIDDLE_NAME"] = name[1]
    row["LAST_NAME"] = name[2]
    row["LAB_TECH_ID"] = last_labtech_added+1
    last_nurse_added = last_labtech_added+1
    row["DOB"] = input("DATE OF BIRTH (YYYY-MM-DD): ")
    row["GENDER"] = input("GENDER(M/F/O): ")
    row["BLOOD_GROUP"] = input(
        "BLOOD_GROUP [A-,A+,B+,B-,O+,O-,AB-,AB+] : ")
    row["PHONE"] = (input("PHONE: "))
    #row["EMAIL"] = input("EMAIL : ")
    row["ZIP_CODE"] = int(input("ZIP_CODE : "))
    row["HOUSE"] = input("HOME ADDRESS : ")
    row["QUALIFICATION"] = int(input("QUALIFICATION : "))
    row["EXPERIENCE"] = int(input("EXPERIENCE (in years) : "))
    row["LAB_DEPAR_ID"] = int(input(
        "LAB DEPARTMENT ID (\n1 - Covid Testing lab\n2 - Ultrasound\n3 - X-RAY\n4 - General Purpose testing\n5 - MRI\nenter option value : "))

    query = "INSERT INTO NURSES(FIRST_NAME, MIDDLE_NAME, LAST_NAME, NURSE_ID, DOB,GENDER,BLOOD_GROUP,PHONE,HOUSE,ZIP_CODE,QUALIFICATION,EXPERIENCE) VALUES('%s', '%s', '%s', '%d', '%s', '%c', '%s', %s, %s , %s, %d. %s,%d,%d)" % (
        row["FIRST_NAME"], row["MIDDLE_NAME"], row["LAST_NAME"], row["LAB_TECH_ID"], row["DOB"], row["GENDER"], row["BLOOD_GROUP"], row["PHONE"], row["HOUSE"], row["ZIP_CODE"], row["QUALIFICATION"], row["EXPERIENCE"], row["LAB_DEPAR_ID"])

    gender_count = gender_list.count(row["GENDER"])

    if gender_count == 0:
        print("Invalid Input for gender\nRecord Not added\nInvalid Input!!!\n")
        return

    blood_group_exists = blood_group_list.count(row["BLOOD_GROUP"])

    if blood_group_exists == 0:
        print("Invalid Input for blood_group\nRecord Not added\nInvalid Input!!!\n")
        return

    if row["EXPERIENCE"] < 0:
        print("Enter non-negative value for Experience Field\n")
        return

    if count_num_digits(row["ZIP_CODE"]) != 6:
        print("ZIP_CODE should be 6 digits long\n")
        return

    flag = ExecuteQuery(query)
    if flag == 1:
        print("Inserted Into Database")
    else:
        last_labtech_added = last_labtech_added - 1
    return
def AddNurse():
    row = {}
    global last_nurse_added
    print("Enter Nurse's details: ")
    name = (input("NAME (First_Name Middle_Name Last_Name): ")).split(' ')
    row["FIRST_NAME"] = name[0]
    row["MIDDLE_NAME"] = name[1]
    row["LAST_NAME"] = name[2]
    row["NURSE_ID"] = last_nurse_added+1
    last_nurse_added = last_nurse_added+1
    row["DOB"] = input("DATE OF BIRTH (YYYY-MM-DD): ")
    row["GENDER"] = input("GENDER(M/F/O): ")
    row["BLOOD_GROUP"] = input(
        "BLOOD_GROUP [A-,A+,B+,B-,O+,O-,AB-,AB+] : ")
    row["PHONE"] = (input("PHONE: "))
    #row["EMAIL"] = input("EMAIL : ")
    row["ZIP_CODE"] = int(input("ZIP_CODE : "))
    row["HOUSE"] = input("HOME ADDRESS : ")
    row["QUALIFICATION"] = int(input("QUALIFICATION : "))
    row["EXPERIENCE"] = int(input("EXPERIENCE (in years) : "))
    #row["MED_DEPAR_ID"] = int(input("MEDICAL DEPARTMENT ID (\n1 - Cardiologists\n2 - Dermatologists\n3 - Neurologists\n4 - Pathologists\n5 - Psychiatrists\nenter option value : "))

    query = "INSERT INTO NURSES(FIRST_NAME, MIDDLE_NAME, LAST_NAME, NURSE_ID, DOB,GENDER,BLOOD_GROUP,PHONE,HOUSE,ZIP_CODE,QUALIFICATION,EXPERIENCE) VALUES('%s', '%s', '%s', '%d', '%s', '%c', '%s', %s, %s , %s, %d. %s,%d)" % (
        row["FIRST_NAME"], row["MIDDLE_NAME"], row["LAST_NAME"], row["NURSE_ID"], row["DOB"], row["GENDER"], row["BLOOD_GROUP"], row["PHONE"], row["HOUSE"], row["ZIP_CODE"], row["QUALIFICATION"], row["EXPERIENCE"])

    gender_count = gender_list.count(row["GENDER"])

    if gender_count == 0:
        print("Invalid Input for gender\nRecord Not added\nInvalid Input!!!\n")
        return

    blood_group_exists = blood_group_list.count(row["BLOOD_GROUP"])

    if blood_group_exists == 0:
        print("Invalid Input for blood_group\nRecord Not added\nInvalid Input!!!\n")
        return

    if row["EXPERIENCE"] < 0:
        print("Enter non-negative value for Experience Field\n")
        return

    if count_num_digits(row["ZIP_CODE"]) != 6:
        print("ZIP_CODE should be 6 digits long\n")
        return

    flag = ExecuteQuery(query)
    if flag == 1:
            print("Inserted Into Database")
    else :
        last_nurse_added = last_nurse_added - 1
    return
def AddVisitingHours(query,id):
    global last_doctor_added
    VisitingHours=input("Enter Visting Hours : ")
    query+="INSERT INTO VISITING_HOURS(DOCTOR_ID,VISITING_HOURS) VALUES ('%d', '%s');" % (
        id,VisitingHours)
    flag = ExecuteQuery(query)
    if flag == 1:
        print("Inserted Into Database")
    else:
        last_doctor_added = last_doctor_added - 1  
def AddTrainee(id, query):
    row = {}
    row["DOCTOR_ID"] = id
    print("Enter Doctor's ID supervising the trainee: ")
    super_id = int(input())

    query += "INSERT INTO TRAINEE(DOCTOR_ID, TEMPORARY_ID) VALUES('%d','%d');" % (
        super_id, id)  
    AddVisitingHours(query,id)   
    return
def AddPermanent(id, query):
    row = {}
    row["DOCTOR_ID"] = id
    position = input("Enter Doctor's Position ")

    query += "INSERT INTO PERMANENT(DOCTOR_ID, POSITION) VALUES('%d','%s');" % (
        id, position)

    AddVisitingHours(query,id)   
    return
def AddDoctor():
    global last_doctor_added
    row = {}
    row["DOCTOR_ID"] = last_doctor_added + 1
    last_doctor_added = last_doctor_added + 1
    print("Enter Doctor's details: ")
    name = (input("NAME (First_Name Middle_Name Last_Name): ")).split(' ')
    row["FIRST_NAME"] = name[0]
    row["MIDDLE_NAME"] = name[1]
    row["LAST_NAME"] = name[2]
    row["DOB"] = input("DATE OF BIRTH (YYYY-MM-DD): ")
    row["GENDER"] = input("GENDER(M/F/O): ")
    row["BLOOD_GROUP"] = input(
        "BLOOD_GROUP [A-,A+,B+,B-,O+,O-,AB-,AB+] : ")
    row["PHONE"] = (input("PHONE: "))
    row["EMAIL"] = input("EMAIL : ")
    row["ZIP_CODE"] = int(input("ZIP_CODE : "))
    row["HOUSE"] = input("HOME ADDRESS : ")
    row["QUALIFICATION"] = int(input("QUALIFICATION : "))
    row["EXPERIENCE"] = int(input("EXPERIENCE (in years) : "))
    row["MED_DEPAR_ID"] = int(input(
        "MEDICAL DEPARTMENT ID (\n1 - Cardiologists\n2 - Dermatologists\n3 - Neurologists\n4 - Pathologists\n5 - Psychiatrists\nenter option value : "))
    doc_type = int(input("Trainee - 0\nPermanent - 1\n"))
    if(doc_type != 0 or doc_type != 1):
        print("Invalid Input\n")
        return
    query = "INSERT INTO DOCTOR(FIRST_NAME, MIDDLE_NAME, LAST_NAME, DOCTOR_ID, DOB,GENDER,BLOOD_GROUP,PHONE,EMAIL,HOUSE,ZIP_CODE,QUALIFICATION,EXPERIENCE,MED_DEPAR_ID) VALUES('%s', '%s', '%s', '%d', '%s', '%c', '%s', %d, %s , %s, %d. %s,%d,%d);" % (
        row["FIRST_NAME"], row["MIDDLE_NAME"], row["LAST_NAME"], row["DOCTOR_ID"], row["DOB"], row["GENDER"], row["BLOOD_GROUP"], row["PHONE"], row["EMAIL"], row["HOUSE"], row["ZIP_CODE"], row["QUALIFICATION"], row["EXPERIENCE"], row["MED_DEPAR_ID"])
    gender_count = gender_list.count(row["GENDER"])
    if gender_count == 0:
        print("Invalid Input for gender\nRecord Not added\nInvalid Input!!!\n")
        return
    blood_group_exists = blood_group_list.count(row["BLOOD_GROUP"])
    if blood_group_exists == 0:
        print("Invalid Input for blood_group\nRecord Not added\nInvalid Input!!!\n")
        return
    if row["EXPERIENCE"] < 0:
        print("Enter non-negative value for Experience Field\n")
        return
    if count_num_digits(row["ZIP_CODE"]) != 6:
        print("ZIP_CODE should be 6 digits long\n")
        return
    if doc_type == 0:
        AddTrainee(row["DOCTOR_ID"], query)
    else:
        AddPermanent(row["DOCTOR_ID"], query)
def AddMedicalDepartment():
    global last_medical_dept_added
    row = {}
    row["MED_DEPAR_ID"] = last_medical_dept_added + 1
    last_medical_dept_added = last_medical_dept_added + 1
    row["NAME"] = input("Enter Department Name : ")
    row["FLOOR"] = int(input("Enter Medical Dept Id :"))
    row["NUMBER"] = int(input("Department Number ( on the floor ): "))

    if row["MED_DEPAR_ID"] < 0 or row["FLOOR"] < 0 or row["NUMBER"] < 0:
        print("Invalid Input\nFailed to add\n")
        return

    query = "INSERT INTO MEDICAL_DEPARTMENT(MED_DEPAR_ID, FLOOR, NAME, NUMBER ) VALUES('%d', '%d', '%s', '%d')" % (
        row["MED_DEPAR_ID"], row["FLOOR"], row["NAME"], row["NUMBER"])

    flag = ExecuteQuery(query)
    if flag == 1:
        print("Inserted Into Database")
    else :
        last_medical_dept_added = last_medical_dept_added - 1

    return
def AddVisitor():
    row = {}
    name = (input("NAME : ")).split(' ')
    row["VISITOR_NAME"] = name[0]
    row["REL_WITH_PATIENT"] = input("RELATION WITH THE PATIENT: ")
    row["PATIENT_ID"] = int(input("PATIENT ID : "))

    query = "INSERT INTO VISITOR( VISITOR_NAME ,REL_WITH_PATIENT,PATIENT_ID) VALUES('%s', '%s','%d')" % (
        row["VISITOR_NAME"], row["REL_WITH_PATIENT"], row["PATIENT_ID"])

    flag = ExecuteQuery(query)
    if flag == 1:
        print("Inserted Into Database")   
    return
def AddDriver():
    global last_employee_added
    row = {}
    row["EMPLOYEE_ID"] = last_employee_added + 1
    last_employee_added = last_employee_added + 1
    print("Enter Employee details: ")
    name = (input("NAME (First_Name Middle_Name Last_Name): ")).split(' ')
    row["FIRST_NAME"] = name[0]
    row["MIDDLE_NAME"] = name[1]
    row["LAST_NAME"] = name[2]
    row["DOB"] = input("DATE OF BIRTH (YYYY-MM-DD): ")
    row["GENDER"] = input("GENDER(M/F/O): ")
    row["BLOOD_GROUP"] = input(
        "BLOOD_GROUP [A-,A+,B+,B-,O+,O-,AB-,AB+] : ")
    row["PHONE"] = (input("PHONE: "))
    row["LICENSE_NUMBER"] = input("LICENSE_NUMBER : ")
    row["ZIP_CODE"] = int(input("ZIP_CODE : "))
    row["VEHICLE_NUMBER"] = input("VEHICLE NUMBER : ")
    row["HOUSE"] = input("HOUSE ADDRESS : ")
    query = "INSERT INTO DRIVER(EMPLOYEE_ID,FIRST_NAME, MIDDLE_NAME, LAST_NAME,DOB,LICENSE_NUMBER,GENDER,INSURANCE_ID,BLOOD_GROUP,PHONE,HOUSE,ZIP_CODE,VEHICLE_NUM) VALUES('%d', '%s', '%s', '%s', '%s', '%s', '%c', '%s', '%s' , '%s', '%s'. '%s','%s');" % (
        row["EMPLOYEE_ID"],row["FIRST_NAME"], row["MIDDLE_NAME"], row["LAST_NAME"], row["DOB"],row["GENDER"],row["BLOOD_GROUP"],row["PHONE"],row["LICENSE_NUMBER"],row["ZIP_CODE"],row["VEHICLE_NUMBER"],row["HOUSE"])
    gender_count = gender_list.count(row["GENDER"])
    if gender_count == 0:
        print("Invalid Input for gender\nRecord Not added\nInvalid Input!!!\n")
        return
    blood_group_exists = blood_group_list.count(row["BLOOD_GROUP"])
    if blood_group_exists == 0:
        print("Invalid Input for blood_group\nRecord Not added\nInvalid Input!!!\n")
        return
    if count_num_digits(row["ZIP_CODE"]) != 6:
        print("ZIP_CODE should be 6 digits long\n")
        return
    flag = ExecuteQuery(query)
    if flag == 1:
        print("Inserted Into Database")
    else :
        last_employee_added = last_employee_added - 1

def CurrentDoctorsWorking():
    ExecuteQuery(
        "SELECT FIRST_NAME,LAST_NAME,NAME FROM DOCTOR INNER JOIN MEDICAL_DEPARTMENT AS MD ON DOCTOR.MED_DEPAR_ID = MD.MED_DEPAR_ID;")
def CurrentMedicalDept():
    ExecuteQuery("SELECT MED_DEPAR_ID,NAME FROM MEDICAL_DEPARTMENT;")

def CurrentLabTests():
    ExecuteQuery("SELECT TEST_DESCRIPTION FROM TEST")

    
def UpdateDocSalary():
    
    position = (int(input("Enter doctor position: ")))
    salary = (int(input("Enter updated salary: "))) 
    query= "UPDATE PERMANENT_SALARY SET SALARY='%d' WHERE POSITION='%s'" %(salary,position)
    ExecuteQuery(query)

def UpdateNurseSalary():
    exp = (int(input("Enter nurse's position: ")))
    salary = (int(input("Enter updated salary: ")))
    query = "UPDATE NURSE_SALARY SET SALARY='%d' WHERE EXPERIENCE='%d'" %(salary,exp)
    ExecuteQuery(query) 
    
    

def UpdateOtherStaffSalary():
    
    work=input("Enter work type: ")
    salary=(int(input("Enter updated Salary: ")))
    query = "UPDATE OTHER_STAFF_SALARY SET SALARY='%d' WHERE WORK='%s'" %(salary,work)
    ExecuteQuery(query) 
    
    
def GetDoctorFromPosition():
    position=input("Enter the position like HOD, specialist, pupil,expert")
    query = "SELECT DOCTOR.FIRST_NAME, DOCTOR.MIDDLE_NAME,DOCTOR.LAST_NAME FROM DOCTOR INNER JOIN PERMANENT ON DOCTOR.DOCTOR_ID=PERMANENT.DOCTOR_ID WHERE PERMANENT.POSITION = '%s'" %(position)
    returnvalue = ExecuteQuery(query) 
    if(returnvalue == 0 ):
        print("An error occured try again")
    return

def GetDoctorFromDepartment():
    position=input("Enter the medical department like Cardiologists, Dermatologists, Neurologists, Pathologists, Psychiatrists")
    query = "SELECT DOCTOR.FIRST_NAME, DOCTOR.MIDDLE_NAME,DOCTOR.LAST_NAME FROM DOCTOR INNER JOIN MEDICAL_DEPARTMENT ON DOCTOR.MED_DEPAR_ID=MEDICAL_DEPARTMENT.MED_DEPAR_ID WHERE MEDICAL_DEPARTMENT.NAME = '%s'" %(position)
    returnvalue = ExecuteQuery(query) 
    if(returnvalue == 0 ):
        print("An error occured try again")
    return

def CostOfLabTest():
    position=input("Enter the medical department like RTPCR COVID TEST Rapid antigen test for covid, Test to check dengue and malaria, Blood test, Protient test")
    query = "SELECT COST FROM TEST WHERE TEST_DECRIPTION = '%s'" %(position)
    returnvalue = ExecuteQuery(query) 
    if(returnvalue == 0 ):
        print("An error occured try again")
    return
    
def StockOfMedicine():
    position=input("Enter the medicine name like Crocin Bitadine Paracetamol Aspirin Noradrenaline Firminho")
    query = "SELECT STOCK FROM MEDICINE WHERE MEDICINE_NAME = '%s'" %(position)
    returnvalue = ExecuteQuery(query) 
    if(returnvalue == 0 ):
        print("An error occured try again")
    return

def AvgStayOfDay():
    query = "SELECT AVG(DATEDIFF(DATE_OF_DISCHARGE,DATE_OF_ARRIVAL)) AS too_much_dna FROM IN_PATIENT"
    cur.execute(query)
    con.commit()
    A = cur.fetchall()
    print("Average Stay Of Day : {}".A[0]["too_much_dna"])
    return A[0]["too_much_dna"]
    
def PatStayMoreThanAvg():
    position = AvgStayOfDay()
    query = "SELECT PATIENT.FIRST_NAME, PATIENT.MIDDLE_NAME, PATIENT.LAST_NAME FROM PATIENT INNER JOIN IN_PATIENT ON PATIENT.PATIENT_ID=IN_PATIENT.PATIENT_ID WHERE DATEDIFF(IN_PATIENT.DATE_OF_DISCHARGE,IN_PATIENT.DATE_OF_ARRIVAL) > '%f' "%(position)
    ExecuteQuery(query)

def dispatch(ch):

    """
    Function that maps helper functions to option entered
    """

    if(ch == 1):
        InitBedsList()
        NumberOfBedsAvaialable();
    elif(ch == 2):
        PatStayMoreThanAvg()
    elif(ch == 3):
        option3()
    elif(ch == 4):
        option4()
    else:
        print("Error: Invalid Option")


def deleteDriver(employee_id):
    '''
        Function that delete record of driver

    '''
    try:
        
        id=(int(input("Enter Driver_id: ")))
        query = "DELETE FROM DRIVER WHERE EMPLOYEE_ID='%s'" %(id) 
        ExecuteQuery(query)
    except Exception as e:
        con.rollback()
        print("Failed to Execute")
        print(">>>>>>",e)
    return 


# Global
while(1):
    tmp = sp.call('clear', shell=True)

    # Can be skipped if you want to hardcode username and password
    #  username = input("Username: ")
    # password = input("Password: ")

    try:
        # Set db name accordingly which have been create by you
        # Set host to the server's address if you don't want to use local SQL server
        con = pymysql.connect(host='localhost',
                              port=30306,
                              user="root",
                              password="table",
                              db='KAG-HOSPITAL',
                              cursorclass=pymysql.cursors.DictCursor)
        tmp = sp.call('clear', shell=True)

        if(con.open):
            print("Connected")
        else:
            print("Failed to connect")

        tmp = input("Enter any key to CONTINUE>")

        with con.cursor() as cur:
            while(1):
                tmp = sp.call('clear', shell=True)
                # Here taking example of Employee Mini-world
                print("1. Delete Driver")  # Hire an Employee
                print("2. Check stock of a medicine")  # Fire an Employee
                print("3. Check cost of a lab test")  # Promote Employee
                print("4. Show Doctors working in a certain department")  # Employee Statistics
                print("5. Show doctors working at a certain positon")
                print("6. Update salary of other staff")
                print("7. Update Nurse Salary")
                print("8. Update salary of doctors")
                print("9. Show vacant beds")
                print("10. Show lab tests")
                print("11. Show names of medical departments")
                print("12. Show names of doctors")
                print("13. Insert driver")
                print("14. Insert visitor")
                print("15. Insert medical department")
                print("16. Insert Doctor")
                print("17. Insert Permanent doctor")
                print("18. Insert trainee doctor")
                print("19. Insert visiting hours")
                print("20. Insert nurse")
                print("21. Insert Lab Technician")
                print("22. Insert patient")
                print("23. Insert inpatient")
                print("24. Insert outpatient")
                print("25. Show number of beds available")
                print("26. ")
                ch = int(input("Enter choice> "))
                tmp = sp.call('clear', shell=True)
                if ch == 25:
                    exit()
                else:
                    dispatch(ch)
                    tmp = input("Enter any key to CONTINUE>")

    except Exception as e:
        tmp = sp.call('clear', shell=True)
        print(e)
        print("Connection Refused: Either username or password is incorrect or user doesn't have access to database")
        tmp = input("Enter any key to CONTINUE>")
