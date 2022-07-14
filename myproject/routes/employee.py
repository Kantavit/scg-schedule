from .__init__ import employee
from ..extensions import db
from flask import render_template, redirect, url_for, request, session
import datetime;


@employee.route('/')
def employeeLoginPage():
    line_id = request.args.get("userId")

    if line_id is None:
        session['line_id'] = None
        return render_template('employee/welcome.html')
    
    toString = str(line_id)
    session['line_id'] = toString # send line_id to other page
    
    cur = db.connection.cursor()
    query = "SELECT employee_name FROM employee inner join employeeInfo on employee.employee_id = employeeInfo.employee_id WHERE line_id = " + "'" + toString + "'"
    cur.execute(query)
    first_name = cur.fetchall()  
    query = "SELECT employee_lastname FROM employee inner join employeeInfo on employee.employee_id = employeeInfo.employee_id WHERE line_id = " + "'" + toString + "'"
    cur.execute(query)
    last_name = cur.fetchall()
    query = "SELECT employee_id FROM employee WHERE line_id = " + "'" + toString + "'"
    cur.execute(query)
    employee_id = cur.fetchall() 
    cur.execute("SELECT sub_team FROM employeeInfo WHERE employee_id=%s",(employee_id))
    sub_team = cur.fetchall()

    cur.close()

    if bool(first_name) == False and bool(last_name) == False:
        session['first_name'] = "userNotFound" # send first_name to other page
        return render_template('employee/welcome.html')

    session['first_name'] = first_name # send first_name to other page
    session['last_name'] = last_name # send last_name to other page
    session['employee_id'] = employee_id[0][0] # send last_name to other page
    session['sub_team'] = sub_team[0][0]

    return render_template('employee/welcome.html')

@employee.route('/employee', methods=['POST','GET'])
def employeePage():
    line_id = session.get("line_id") # in case for query

    if line_id is None or session.get("first_name") == "userNotFound":
        return render_template('employee/warning.html')
    else:
        return render_template('employee/employee.html', first_name=session.get("first_name"), last_name=session.get("last_name"))
        

@employee.route('/employee/edit')
def chooseEdit():
    line_id = session.get("line_id") # in case for query
        
    if line_id is None or session.get("first_name") == "userNotFound":
        return render_template('employee/warning.html')
    else:
        return render_template('employee/employeeEdit.html', first_name=session.get("first_name"), last_name=session.get("last_name"))

####################################################################################################

@employee.route('/employee/edit/shift')
def chooseEditShift():
    line_id = session.get("line_id") # in case for query
        
    if line_id is None or session.get("first_name") == "userNotFound":
        return render_template('employee/warning.html')
    else:
        return render_template('employee/editShift.html', first_name=session.get("first_name"), last_name=session.get("last_name"))
    # return render_template('employee/editShift.html')

@employee.route('/employee/edit/shift/self', methods=['POST','GET'])
def editYourself():
    line_id = session.get("line_id") # in case for query
        
    if line_id is None or session.get("first_name") == "userNotFound":
        return render_template('employee/warning.html')
    else:
        return render_template('employee/selfEdit.html', first_name=session.get("first_name"), last_name=session.get("last_name"))
    # return render_template('employee/selfEdit.html')

@employee.route('/employee/edit/shift/cowork', methods=['POST','GET'])
def editCowork():
    line_id = session.get("line_id") # in case for query
    employee_id = session.get("employee_id")
    sub_team = session.get("sub_team")
        
    if line_id is None or session.get("first_name") == "userNotFound":
        return render_template('employee/warning.html')
    
    elif request.method == 'POST':
        if request.form['choose'] == "สองคน":
            cur = db.connection.cursor()
            # count employee
            cur.execute("SELECT COUNT(employee_id) FROM employeeInfo WHERE sub_team=%s AND employee_id!=%s ",(sub_team, employee_id))
            employee_count = cur.fetchall()
            count = employee_count[0][0]

            # get employee in same team
            cur.execute("SELECT employee_id, employee_name, employee_lastname FROM employeeInfo WHERE sub_team=%s AND employee_id!=%s ",(sub_team, employee_id))
            idSub_team = cur.fetchall()
            
            date = request.form['date2-1']
            OldShift = request.form['OldShift2-1']
            NewShift = request.form['NewShift2-1']
            employee_id2 = request.form['name2-2']
            
            for i in range(count):
                if idSub_team[i][0] == employee_id2:
                    employee_name2 = idSub_team[i][1] 
                    employee_lastname2 = idSub_team[i][2]
                    break
                    
            cur.close()
            
            OldShift2 = request.form['OldShift2-2']
            NewShift2 = request.form['NewShift2-2']
            reason = request.form['reason']
            current_time = datetime.datetime.now()
            TimeStamp = current_time.strftime("%Y-%m-%d %H:%M:%S")
              
            cur = db.connection.cursor()
            query = "SELECT * FROM employeeInfo WHERE employee_id = " + "'" + employee_id + "'"
            cur.execute(query)
            employeeinfo_db = cur.fetchall()
            approver_id = employeeinfo_db[0][4]

            session['date2-1'] = date

            session['name2-1'] = employee_id
            session['employee_name1'] = session.get("first_name")
            session['employee_lastname1'] = session.get("last_name")
            session['OldShift2-1'] = OldShift
            session['NewShift2-1'] = NewShift

            session['name2-2'] = employee_id2
            session['employee_name2'] = employee_name2
            session['employee_lastname2'] = employee_lastname2
            session['OldShift2-2'] = OldShift2
            session['NewShift2-2'] = NewShift2

            session['reason2p'] = reason
            session['TimeStamp2p'] = TimeStamp
            session['approver_id2p'] = approver_id
            session['status2p'] = "waiting"
            session['choose'] = "สองคน"

            cur.close()
            return redirect(url_for('employee.employeeCoworkTransaction'))
            # , date=date,employee_name1=session.get("first_name"),
            #         employee_lastname1=session.get("last_name"),OldShift=OldShift,NewShift=NewShift,employee_name2=employee_name2,
            #         employee_lastname2=employee_lastname2,OldShift2=OldShift2,NewShift2=NewShift2,reason=reason

        elif request.form['choose'] == "สามคน":
            cur = db.connection.cursor()
            # count employee
            cur.execute("SELECT COUNT(employee_id) FROM employeeInfo WHERE sub_team=%s AND employee_id!=%s ",(sub_team, employee_id))
            employee_count = cur.fetchall()
            count = employee_count[0][0]

            # get employee in same team
            cur.execute("SELECT employee_id, employee_name, employee_lastname FROM employeeInfo WHERE sub_team=%s AND employee_id!=%s ",(sub_team, employee_id))
            idSub_team = cur.fetchall()

            date = request.form['date3-1']
            OldShift = request.form['OldShift3-1']
            NewShift = request.form['NewShift3-1']
            employee_id2 = request.form['name3-2']

            for i in range(count):
                if idSub_team[i][0] == employee_id2:
                    employee_name2 = idSub_team[i][1] 
                    employee_lastname2 = idSub_team[i][2]
                    break
                    
            cur.close()

            OldShift2 = request.form['OldShift3-2']
            NewShift2 = request.form['NewShift3-2']
            employee_id3 = request.form['name3-3']

            for i in range(count):
                if idSub_team[i][0] == employee_id3:
                    employee_name3 = idSub_team[i][1] 
                    employee_lastname3 = idSub_team[i][2]
                    break
                    
            cur.close()

            OldShift3 = request.form['OldShift3-3']
            NewShift3 = request.form['NewShift3-3']
            reason = request.form['reason']
            current_time = datetime.datetime.now()
            TimeStamp = current_time.strftime("%Y-%m-%d %H:%M:%S")
              
            cur = db.connection.cursor()
            query = "SELECT * FROM employeeInfo WHERE employee_id = " + "'" + employee_id + "'"
            cur.execute(query)
            employeeinfo_db = cur.fetchall()
            approver_id = employeeinfo_db[0][4]

            session['date3-1'] = date

            session['name3-1'] = employee_id
            session['employee_name1'] = session.get("first_name")
            session['employee_lastname1'] = session.get("last_name")
            session['OldShift3-1'] = OldShift
            session['NewShift3-1'] = NewShift

            session['name3-2'] = employee_id2
            session['employee_name2'] = employee_name2
            session['employee_lastname2'] = employee_lastname2
            session['OldShift3-2'] = OldShift2
            session['NewShift3-2'] = NewShift2

            session['name3-3'] = employee_id3
            session['employee_name3'] = employee_name3
            session['employee_lastname3'] = employee_lastname3
            session['OldShift3-3'] = OldShift3
            session['NewShift3-3'] = NewShift3

            session['reason3p'] = reason
            session['TimeStamp3p'] = TimeStamp
            session['approver_id3p'] = approver_id
            session['status3p'] = "waiting"
            session['choose'] = "สามคน"

            cur.close()
            return redirect(url_for('employee.employeeCoworkTransaction'))
            # , date=date,employee_name1=session.get("first_name"),
            #         employee_lastname1=session.get("last_name"),OldShift=OldShift,NewShift=NewShift,employee_name2=employee_name2,
            #         employee_lastname2=employee_lastname2,OldShift2=OldShift2,NewShift2=NewShift2,employee_name3=employee_name3,
            #         employee_lastname3=employee_lastname3,OldShift3=OldShift3,NewShift3=NewShift3,reason=reason

    else:
        cur = db.connection.cursor()
        
        # count employee
        cur.execute("SELECT COUNT(employee_id) FROM employeeInfo WHERE sub_team=%s AND employee_id!=%s ",(sub_team, employee_id))
        employee_count = cur.fetchall()
        count = employee_count[0][0]

        # get employee in same team
        cur.execute("SELECT employee_id, employee_name, employee_lastname FROM employeeInfo WHERE sub_team=%s AND employee_id!=%s ",(sub_team, employee_id))
        idSub_team = cur.fetchall()

        otherEmployee = [0]*count
        for i in range(count):
            otherEmployee[i] = idSub_team[i][0]
        
        cur.execute("SELECT * FROM employeeShift WHERE employeeShift_id=%s ",[employee_id])
        shifts = cur.fetchall()
        cur.execute("SELECT * FROM employeeShift WHERE employeeShift_id=%s ",[otherEmployee[0]])
        shifts2 = cur.fetchall()
        cur.execute("SELECT * FROM employeeShift WHERE employeeShift_id=%s ",[otherEmployee[1]])
        shifts3 = cur.fetchall()
        cur.close()

        return render_template('employee/coworkEdit.html', first_name=session.get("first_name"), last_name=session.get("last_name"),
                                idSub_team=idSub_team, shifts=shifts, shifts2=shifts2, shifts3=shifts3 )


@employee.route('/employee/edit/shift/addshift', methods=['POST','GET'])
def editAddShift():
    line_id = session.get("line_id") # in case for query
    employee_id = session.get("employee_id")
        
    if line_id is None or session.get("first_name") == "userNotFound":
        return render_template('employee/warning.html')
    
    elif request.method == 'POST':
        if request.form['choose'] == "add":
            name = request.form['name']
            date = request.form['date']
            OldShift = request.form['OldShift']
            addShift = request.form['addShift']
            reason = request.form['reason']
            current_time = datetime.datetime.now()
            TimeStamp = current_time.strftime("%Y-%m-%d %H:%M:%S")
            
            status = "unsuccessful"
              
            cur = db.connection.cursor()
            query = "SELECT * FROM employeeInfo WHERE employee_id = " + "'" + employee_id + "'"
            cur.execute(query)
            employeeinfo_db = cur.fetchall()
            approver_id = employeeinfo_db[0][4]

            cur.execute("INSERT INTO transactionaddShift (employee_id , date , OldShift , addShift , TimeStamp ,  reason , status , approver_id ) VALUES (%s, %s, %s, %s, %s,%s,%s,%s)",(employee_id , date , OldShift , addShift , TimeStamp ,  reason , status , approver_id))
            db.connection.commit()
            cur.close()
            return redirect(url_for('employee.editAddShift'))

        elif request.form['choose'] == "update":
            transactionaddShift_id = request.form['transactionaddShift_id']
            date = request.form['date']
            OldShift = request.form['OldShift']
            addShift = request.form['addShift']
            reason = request.form['reason']
            current_time = datetime.datetime.now()
            TimeStamp = current_time.strftime("%Y-%m-%d %H:%M:%S")

            cur = db.connection.cursor()
            cur.execute("UPDATE transactionaddShift SET date=%s , OldShift=%s , addShift=%s , reason=%s , TimeStamp=%s WHERE transactionaddShift_id=%s",(date , OldShift , addShift , reason, TimeStamp, transactionaddShift_id))
            db.connection.commit()
            cur.close()
            return redirect(url_for('employee.editAddShift'))

        elif request.form['choose'] == "delete":
            transactionaddShift_id = request.form['transactionaddShift_id']

            cur = db.connection.cursor()
            cur.execute("DELETE FROM transactionaddShift WHERE transactionaddShift_id=%s",[transactionaddShift_id])
            db.connection.commit()
            cur.close()
            return redirect(url_for('employee.editAddShift'))

    else:
        cur = db.connection.cursor()
        transactionaddShift_element = cur.execute(" SELECT * FROM transactionaddShift WHERE employee_id=%s AND status=%s", (employee_id, "unsuccessful"))
        transactionaddShift = cur.fetchall()
        query = "SELECT * FROM employeeShift WHERE employeeShift_id = " + "'" + employee_id + "'"
        cur.execute(query)
        shifts = cur.fetchall()
        cur.close()

        return render_template('employee/addshiftEdit.html', first_name=session.get("first_name"), last_name=session.get("last_name"),
                        transactionaddShift_element=transactionaddShift_element, transactionaddShift=transactionaddShift, shifts=shifts)


####################################################################################################

@employee.route('/employee/edit/shiftandoff', methods=['POST','GET'])
def chooseEditShiftAndOff():
    line_id = session.get("line_id") # in case for query
    employee_id = session.get("employee_id")
    sub_team = session.get("sub_team")
        
    if line_id is None or session.get("first_name") == "userNotFound":
        return render_template('employee/warning.html')
    
    elif request.method == 'POST':
        if request.form['choose'] == "add":
            employee_id = request.form['name']

            cur = db.connection.cursor()
            cur.execute("SELECT employee_name, employee_lastname FROM employeeInfo WHERE employee_id = " + "'" + employee_id + "'")
            employeeinfo_db = cur.fetchone()
            
            employee_name = employeeinfo_db[0]
            employee_lastname = employeeinfo_db[1]
            date = request.form['date']
            Oldwork_type = request.form['Oldwork_type']
            Newwork_type = request.form['Newwork_type']
            Oldoff_code = request.form['Oldoff_code']
            Newoff_code = request.form['Newoff_code']
            section_code = request.form['section_code']
            section_code = section_code.split()[0]
            reason = request.form['reason']
            current_time = datetime.datetime.now()
            TimeStamp = current_time.strftime("%Y-%m-%d %H:%M:%S")
            
            status = "unsuccessful"
            
            cur.execute("SELECT approver_id FROM employeeInfo WHERE employee_id = " + "'" + employee_id + "'")
            employeeinfo_db = cur.fetchone()
            approver_id = employeeinfo_db[0]

            cur.execute("SELECT director_id FROM employeeInfo WHERE employee_id = " + "'" + employee_id + "'")
            employeeinfo_db = cur.fetchone()
            director_id = employeeinfo_db[0]

            cur.execute("INSERT INTO transactionChangeWork (employee_id , employee_name , employee_lastname, date, Oldwork_type, Newwork_type, Oldoff_code, Newoff_code, section_code, reason, TimeStamp, status, approver_id, director_id ) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(employee_id , employee_name , employee_lastname, date, Oldwork_type, Newwork_type, Oldoff_code, Newoff_code, section_code, reason, TimeStamp, status, approver_id, director_id))
            db.connection.commit()
            cur.close()
            return redirect(url_for('employee.chooseEditShiftAndOff'))

        elif request.form['choose'] == "update":
            transactionChangeWork_id = request.form['transactionChangeWork_id']
            employee_id = request.form['name']

            cur = db.connection.cursor()
            cur.execute("SELECT employee_name, employee_lastname FROM employeeInfo WHERE employee_id = " + "'" + employee_id + "'")
            employeeinfo_db = cur.fetchone()
            
            employee_name = employeeinfo_db[0]
            employee_lastname = employeeinfo_db[1]
            date = request.form['date']
            Oldwork_type = request.form['Oldwork_type']
            Newwork_type = request.form['Newwork_type']
            Oldoff_code = request.form['Oldoff_code']
            Newoff_code = request.form['Newoff_code']
            section_code = request.form['section_code']
            reason = request.form['reason']
            current_time = datetime.datetime.now()
            TimeStamp = current_time.strftime("%Y-%m-%d %H:%M:%S")
            
            status = "unsuccessful"
            
            cur.execute("SELECT approver_id FROM employeeInfo WHERE employee_id = " + "'" + employee_id + "'")
            employeeinfo_db = cur.fetchone()
            approver_id = employeeinfo_db[0]

            cur.execute("SELECT director_id FROM employeeInfo WHERE employee_id = " + "'" + employee_id + "'")
            employeeinfo_db = cur.fetchone()
            director_id = employeeinfo_db[0]

            cur.execute("UPDATE transactionChangeWork SET employee_id=%s , employee_name=%s , employee_lastname=%s, date=%s, Oldwork_type=%s, Newwork_type=%s, Oldoff_code=%s, Newoff_code=%s, section_code=%s, reason=%s, TimeStamp=%s, status=%s, approver_id=%s, director_id=%s WHERE transactionChangeWork_id=%s",(employee_id , employee_name , employee_lastname, date, Oldwork_type, Newwork_type, Oldoff_code, Newoff_code, section_code, reason, TimeStamp, status, approver_id, director_id, transactionChangeWork_id))
            db.connection.commit()
            cur.close()
            return redirect(url_for('employee.chooseEditShiftAndOff'))

        elif request.form['choose'] == "delete":
            transactionChangeWork_id = request.form['transactionChangeWork_id']

            cur = db.connection.cursor()
            cur.execute("DELETE FROM transactionChangeWork WHERE transactionChangeWork_id=%s",[transactionChangeWork_id])
            db.connection.commit()
            cur.close()
            return redirect(url_for('employee.chooseEditShiftAndOff'))

    else:
        cur = db.connection.cursor()

        # count employee
        cur.execute("SELECT COUNT(employee_id) FROM employeeInfo WHERE sub_team=%s AND employee_id!=%s ",(sub_team, employee_id))
        employee_count = cur.fetchall()
        count = employee_count[0][0]

        # get employee in same team (no logged in user)
        cur.execute("SELECT employee_id, employee_name, employee_lastname FROM employeeInfo WHERE sub_team=%s AND employee_id!=%s ",(sub_team, employee_id))
        idSub_team = cur.fetchall()

        # get all employee in same team 
        cur.execute("SELECT employee_id, employee_name, employee_lastname FROM employeeInfo WHERE sub_team=%s",[sub_team])
        idSub_teamAll = cur.fetchall()
        
        transactionChangeWork_element = cur.execute(" SELECT * FROM transactionChangeWork WHERE employee_id=%s AND status=%s", (employee_id, "unsuccessful"))
        transactionChangeWork = cur.fetchall()

        otherEmployee = [0]*count
        for i in range(count):
            otherEmployee[i] = idSub_team[i][0]

        cur.execute("SELECT employee_id,Remark , dayoff FROM filtershift INNER JOIN employeeInfo ON filtershift.section_code = employeeInfo.section_code WHERE employee_id=%s",[employee_id])
        workData1 = cur.fetchall()
        cur.execute("SELECT employee_id,Remark , dayoff FROM filtershift INNER JOIN employeeInfo ON filtershift.section_code = employeeInfo.section_code WHERE employee_id=%s",[otherEmployee[0]])
        workData2 = cur.fetchall()
        cur.execute("SELECT employee_id,Remark , dayoff FROM filtershift INNER JOIN employeeInfo ON filtershift.section_code = employeeInfo.section_code WHERE employee_id=%s",[otherEmployee[1]])
        workData3 = cur.fetchall()

        # get all section_code
        section_code_element = cur.execute("SELECT Remark, dayoff, section_code FROM filtershift")
        section_code_data = cur.fetchall()

        cur.close()

        return render_template('employee/editShiftAndOff.html', first_name=session.get("first_name"), last_name=session.get("last_name"),
                                idSub_teamAll=idSub_teamAll, workData1=workData1, workData2=workData2, workData3=workData3, section_code_element=section_code_element,
                                section_code_data=section_code_data, transactionChangeWork_element=transactionChangeWork_element, transactionChangeWork=transactionChangeWork )


@employee.route('/employee/edit/shiftandoff/viewshift', methods=['POST','GET']) # แก้เป็นให้เข้าไปแก้ตาม <int:id> 
def viewShift():
    line_id = session.get("line_id") # in case for query
        
    if line_id is None or session.get("first_name") == "userNotFound":
        return render_template('employee/warning.html')
    else:
        return render_template('employee/viewShift.html', first_name=session.get("first_name"), last_name=session.get("last_name"))
    # return render_template('employee/viewShift.html')

@employee.route('/employee/edit/shiftandoff/viewshiftonly', methods=['POST','GET']) 
def viewShiftOnly():
    line_id = session.get("line_id") # in case for query
        
    if line_id is None or session.get("first_name") == "userNotFound":
        return render_template('employee/warning.html')
    else:
        return render_template('employee/viewShiftOnly.html', first_name=session.get("first_name"), last_name=session.get("last_name"))
    # return render_template('employee/viewShiftOnly.html')

####################################################################################################

@employee.route('/employee/edit/status')
def chooseCheckStatus():
    line_id = session.get("line_id") # in case for query
        
    if line_id is None or session.get("first_name") == "userNotFound":
        return render_template('employee/warning.html')
    else:
        return render_template('employee/checkStatus.html', first_name=session.get("first_name"), last_name=session.get("last_name"))
    # return render_template('employee/checkStatus.html')

@employee.route('/employee/edit/status/pending')
def pending():
    line_id = session.get("line_id") # in case for query
        
    if line_id is None or session.get("first_name") == "userNotFound":
        return render_template('employee/warning.html')
    else:
        return render_template('employee/pending.html', first_name=session.get("first_name"), last_name=session.get("last_name"))
    # return render_template('employee/pending.html')

@employee.route('/employee/edit/status/approve')
def approve():
    line_id = session.get("line_id") # in case for query
        
    if line_id is None or session.get("first_name") == "userNotFound":
        return render_template('employee/warning.html')
    else:
        return render_template('employee/approve.html', first_name=session.get("first_name"), last_name=session.get("last_name"))
    # return render_template('employee/approve.html')

@employee.route('/employee/edit/status/reject')
def reject():
    line_id = session.get("line_id") # in case for query
        
    if line_id is None or session.get("first_name") == "userNotFound":
        return render_template('employee/warning.html')
    else:
        return render_template('employee/reject.html', first_name=session.get("first_name"), last_name=session.get("last_name"))
    # return render_template('employee/reject.html')

####################################################################################################

@employee.route('/employee/edit/addemployee', methods=['POST','GET'])
def addEmployee():
    line_id = session.get("line_id") # in case for query
        
    if line_id is None or session.get("first_name") == "userNotFound":
        return render_template('employee/warning.html')
    else:
        return render_template('employee/addEmployee.html', first_name=session.get("first_name"), last_name=session.get("last_name"))
    # return render_template('employee/addEmployee.html')

####################################################################################################

@employee.route('/employee/edit/shift/self/selflist', methods=['POST','GET'])
def editYourselfList():
    line_id = session.get("line_id") # in case for query
    employee_id = session.get("employee_id")
        
    if line_id is None or session.get("first_name") == "userNotFound":
        return render_template('employee/warning.html')
    
    elif request.method == 'POST':
        if request.form['choose'] == "add":
            name = request.form['name']
            date = request.form['date']
            OldShift = request.form['OldShift']
            NewShift = request.form['NewShift']
            reason = request.form['reason']
            current_time = datetime.datetime.now()
            TimeStamp = current_time.strftime("%Y-%m-%d %H:%M:%S")
            
            status = "unsuccessful"
              
            cur = db.connection.cursor()
            query = "SELECT * FROM employeeInfo WHERE employee_id = " + "'" + employee_id + "'"
            cur.execute(query)
            employeeinfo_db = cur.fetchall()
            approver_id = employeeinfo_db[0][4]

            cur.execute("INSERT INTO transactionChangeShift (employee_id , date , OldShift , NewShift , TimeStamp ,  reason , status , approver_id ) VALUES (%s, %s, %s, %s, %s,%s,%s,%s)",(employee_id , date , OldShift , NewShift , TimeStamp ,  reason , status , approver_id))
            db.connection.commit()
            cur.close()
            return redirect(url_for('employee.editYourselfList'))

        elif request.form['choose'] == "update":
            transactionChangeShift_id = request.form['transactionChangeShift_id']
            date = request.form['date']
            OldShift = request.form['OldShift']
            NewShift = request.form['NewShift']
            reason = request.form['reason']
            current_time = datetime.datetime.now()
            TimeStamp = current_time.strftime("%Y-%m-%d %H:%M:%S")

            cur = db.connection.cursor()
            cur.execute("UPDATE transactionChangeShift SET date=%s , OldShift=%s , NewShift=%s , reason=%s , TimeStamp=%s WHERE transactionChangeShift_id=%s",(date , OldShift , NewShift , reason, TimeStamp, transactionChangeShift_id))
            db.connection.commit()
            cur.close()
            return redirect(url_for('employee.editYourselfList'))

        elif request.form['choose'] == "delete":
            transactionChangeShift_id = request.form['transactionChangeShift_id']

            cur = db.connection.cursor()
            cur.execute("DELETE FROM transactionChangeShift WHERE transactionChangeShift_id=%s",[transactionChangeShift_id])
            db.connection.commit()
            cur.close()
            return redirect(url_for('employee.editYourselfList'))

    else:
        cur = db.connection.cursor()
        transactionChangeShift_element = cur.execute(" SELECT * FROM transactionChangeShift WHERE employee_id=%s AND status=%s", (employee_id, "unsuccessful"))
        transactionChangeShift = cur.fetchall()
        query = "SELECT * FROM employeeShift WHERE employeeShift_id = " + "'" + employee_id + "'"
        cur.execute(query)
        shifts = cur.fetchall()
        cur.close()

        return render_template('employee/selfEditList.html', first_name=session.get("first_name"), last_name=session.get("last_name"),
                        transactionChangeShift_element=transactionChangeShift_element, transactionChangeShift=transactionChangeShift, shifts=shifts)


@employee.route('/employee/edit/shift/self/selflist/selflistsummary', methods=['POST','GET'])
def employeeSelfTransaction():
    line_id = session.get("line_id") # in case for query
    employee_id = session.get("employee_id")
        
    if line_id is None or session.get("first_name") == "userNotFound":
        return render_template('employee/warning.html')

    elif request.method == 'POST':
        if request.form['choose'] == "cancel":
            cur = db.connection.cursor()
            cur.execute("DELETE FROM transactionChangeShift WHERE employee_id=%s AND status=%s", [employee_id, "unsuccessful"])
            db.connection.commit()
            cur.close()
            return redirect(url_for('employee.editYourselfList'))

        elif request.form['choose'] == "confirm":
            current_time = datetime.datetime.now()
            TimeStamp = current_time.strftime("%Y-%m-%d %H:%M:%S")

            cur = db.connection.cursor()
            cur.execute("UPDATE transactionChangeShift SET status=%s, TimeStamp=%s  WHERE  employee_id=%s AND status=%s", ("waiting", TimeStamp, employee_id, "unsuccessful"))
            db.connection.commit()
            cur.close()
            return redirect(url_for('employee.employeeSelfTransactionEnd'))

    else:
        cur = db.connection.cursor()
        transactionChangeShift_element = cur.execute(" SELECT * FROM transactionChangeShift WHERE employee_id=%s AND status=%s", (employee_id, "unsuccessful"))
        transactionChangeShift = cur.fetchall()
        query = "SELECT * FROM employeeShift WHERE employeeShift_id = " + "'" + employee_id + "'"
        cur.execute(query)
        shifts = cur.fetchall()
        cur.close()

        return render_template('employee/selfEditListSummary.html', first_name=session.get("first_name"), last_name=session.get("last_name"),
                        transactionChangeShift_element=transactionChangeShift_element, transactionChangeShift=transactionChangeShift, shifts=shifts)


@employee.route('/employee/edit/shift/cowork/coworksummary', methods=['POST','GET'])
def employeeCoworkTransaction():
    line_id = session.get("line_id") # in case for query
    employee_id = session.get("employee_id")

    if line_id is None or session.get("first_name") == "userNotFound":
        return render_template('employee/warning.html')

    elif session.get("choose") == "สองคน":
        date1 = session.get("date2-1")

        name1 = employee_id
        employee_name1 = session.get("first_name")
        employee_lastname1 = session.get("last_name")
        OldShift1 = session.get("OldShift2-1")
        NewShift1 = session.get("NewShift2-1")

        name2 = session.get("name2-2")
        employee_name2 = session.get("employee_name2")
        employee_lastname2 = session.get("employee_lastname2")
        OldShift2 = session.get("OldShift2-2")
        NewShift2 = session.get("NewShift2-2")

        employee_name3 = None

        reason = session.get("reason2p")
        approver_id = session.get("approver_id2p")
        status = "waiting"
        
        if request.method == 'POST':
            if request.form['choose'] == "cancel":
                return redirect(url_for('employee.editCowork'))

            elif request.form['choose'] == "confirm":
                current_time = datetime.datetime.now()
                TimeStamp = current_time.strftime("%Y-%m-%d %H:%M:%S")

                cur = db.connection.cursor()
                cur.execute("INSERT INTO transactionCoworkShift (employee_id , date , OldShift , NewShift , TimeStamp ,  reason , status , approver_id, employee_id2, employee_name2, employee_lastname2, OldShift2, NewShift2 ) VALUES (%s, %s, %s, %s, %s,%s,%s,%s,%s,%s,%s,%s,%s)",(employee_id , date1 , OldShift1 , NewShift1 , TimeStamp ,  reason , status , approver_id, name2, employee_name2, employee_lastname2, OldShift2, NewShift2))
                db.connection.commit()
                cur.close()
                return redirect(url_for('employee.employeeCoworkTransactionEnd'))

        return render_template('employee/coworkEditListSummary.html', first_name=session.get("first_name"), last_name=session.get("last_name"),
                    date1=date1,employee_name1=employee_name1,employee_lastname1=employee_lastname1,OldShift1=OldShift1,NewShift1=NewShift1,
                    employee_name2=employee_name2,employee_lastname2=employee_lastname2,OldShift2=OldShift2,NewShift2=NewShift2,reason=reason, employee_name3=employee_name3)

    elif session.get("choose") == "สามคน":
        date1 = session.get("date3-1")

        name1 = employee_id
        employee_name1 = session.get("first_name")
        employee_lastname1 = session.get("last_name")
        OldShift1 = session.get("OldShift3-1")
        NewShift1 = session.get("NewShift3-1")

        name2 = session.get("name3-2")
        employee_name2 = session.get("employee_name2")
        employee_lastname2 = session.get("employee_lastname2")
        OldShift2 = session.get("OldShift3-2")
        NewShift2 = session.get("NewShift3-2")

        name3 = session.get("name3-3")
        employee_name3 = session.get("employee_name3")
        employee_lastname3 = session.get("employee_lastname3")
        OldShift3 = session.get("OldShift3-3")
        NewShift3 = session.get("NewShift3-3")

        reason = session.get("reason3p")
        approver_id = session.get("approver_id3p")
        status = "waiting"
        
        if request.method == 'POST':
            if request.form['choose'] == "cancel":
                return redirect(url_for('employee.editCowork'))

            elif request.form['choose'] == "confirm":
                current_time = datetime.datetime.now()
                TimeStamp = current_time.strftime("%Y-%m-%d %H:%M:%S")

                cur = db.connection.cursor()
                cur.execute("INSERT INTO transactionCoworkShift (employee_id , date , OldShift , NewShift , TimeStamp ,  reason , status , approver_id, employee_id2, employee_name2, employee_lastname2, OldShift2, NewShift2, employee_id3, employee_name3, employee_lastname3, OldShift3, NewShift3 ) VALUES (%s, %s, %s, %s, %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(employee_id , date1 , OldShift1 , NewShift1 , TimeStamp ,  reason , status , approver_id, name2, employee_name2, employee_lastname2, OldShift2, NewShift2, name3, employee_name3, employee_lastname3, OldShift3, NewShift3))
                db.connection.commit()
                cur.close()
                return redirect(url_for('employee.employeeCoworkTransactionEnd'))

        return render_template('employee/coworkEditListSummary.html', first_name=session.get("first_name"), last_name=session.get("last_name"),
                    date1=date1,employee_name1=employee_name1,employee_lastname1=employee_lastname1,OldShift1=OldShift1,NewShift1=NewShift1,
                    employee_name2=employee_name2,employee_lastname2=employee_lastname2,OldShift2=OldShift2,NewShift2=NewShift2,employee_name3=employee_name3,
                    employee_lastname3=employee_lastname3,OldShift3=OldShift3,NewShift3=NewShift3,reason=reason)
        

    else:
        return render_template('employee/coworkEditListSummary.html', first_name=session.get("first_name"), last_name=session.get("last_name"))


@employee.route('/employee/edit/shift/addshift/addshiftsummary', methods=['POST','GET'])
def employeeAddShiftTransaction():
    line_id = session.get("line_id") # in case for query
    employee_id = session.get("employee_id")
        
    if line_id is None or session.get("first_name") == "userNotFound":
        return render_template('employee/warning.html')

    elif request.method == 'POST':
        if request.form['choose'] == "cancel":
            cur = db.connection.cursor()
            cur.execute("DELETE FROM transactionaddShift WHERE employee_id=%s AND status=%s", [employee_id, "unsuccessful"])
            db.connection.commit()
            cur.close()
            return redirect(url_for('employee.editAddShift'))

        elif request.form['choose'] == "confirm":
            current_time = datetime.datetime.now()
            TimeStamp = current_time.strftime("%Y-%m-%d %H:%M:%S")

            cur = db.connection.cursor()
            cur.execute("UPDATE transactionaddShift SET status=%s, TimeStamp=%s  WHERE  employee_id=%s AND status=%s", ("waiting", TimeStamp, employee_id, "unsuccessful"))
            db.connection.commit()
            cur.close()
            return redirect(url_for('employee.employeeAddShiftTransactionEnd'))

    else:
        cur = db.connection.cursor()
        transactionaddShift_element = cur.execute(" SELECT * FROM transactionaddShift WHERE employee_id=%s AND status=%s", (employee_id, "unsuccessful"))
        transactionaddShift = cur.fetchall()
        query = "SELECT * FROM employeeShift WHERE employeeShift_id = " + "'" + employee_id + "'"
        cur.execute(query)
        shifts = cur.fetchall()
        cur.close()

        return render_template('employee/addShiftEditListSummary.html', first_name=session.get("first_name"), last_name=session.get("last_name"),
                        transactionaddShift_element=transactionaddShift_element, transactionaddShift=transactionaddShift, shifts=shifts)


@employee.route('/employee/edit/shiftandoff/shiftandoffsummary', methods=['POST','GET'])
def employeeShiftAndOffTransaction():
    line_id = session.get("line_id") # in case for query
    employee_id = session.get("employee_id")
        
    if line_id is None or session.get("first_name") == "userNotFound":
        return render_template('employee/warning.html')

    elif request.method == 'POST':
        if request.form['choose'] == "cancel":
            cur = db.connection.cursor()
            cur.execute("DELETE FROM transactionChangeWork WHERE employee_id=%s AND status=%s", [employee_id, "unsuccessful"])
            db.connection.commit()
            cur.close()
            return redirect(url_for('employee.chooseEditShiftAndOff'))

        elif request.form['choose'] == "confirm":
            current_time = datetime.datetime.now()
            TimeStamp = current_time.strftime("%Y-%m-%d %H:%M:%S")

            cur = db.connection.cursor()
            cur.execute("UPDATE transactionChangeWork SET status=%s, TimeStamp=%s  WHERE  employee_id=%s AND status=%s", ("waiting", TimeStamp, employee_id, "unsuccessful"))
            db.connection.commit()
            cur.close()
            return redirect(url_for('employee.employeeShiftAndOffTransactionEnd'))

    else:
        cur = db.connection.cursor()
        transactionChangeWork_element = cur.execute(" SELECT * FROM transactionChangeWork WHERE employee_id=%s AND status=%s", (employee_id, "unsuccessful"))
        transactionChangeWork = cur.fetchall()
        cur.close()

        return render_template('employee/shiftAndOffEditListSummary.html', first_name=session.get("first_name"), last_name=session.get("last_name"),
                        transactionChangeWork_element=transactionChangeWork_element, transactionChangeWork=transactionChangeWork)


@employee.route('/employee/edit/addemployee/addemployeesummary', methods=['POST','GET'])
def employeeAddTransaction():
    line_id = session.get("line_id") # in case for query
        
    if line_id is None or session.get("first_name") == "userNotFound":
        return render_template('employee/warning.html')
    else:
        return render_template('employee/addEmployeeEditListSummary.html', first_name=session.get("first_name"), last_name=session.get("last_name"))
    # return render_template('employee/addEmployeeEditListSummary.html')

####################################################################################################

@employee.route('/employee/edit/shift/self/selflist/selflistsummary/selftransactionend', methods=['POST','GET'])
def employeeSelfTransactionEnd():
    line_id = session.get("line_id") # in case for query
        
    if line_id is None or session.get("first_name") == "userNotFound":
        return render_template('employee/warning.html')
    else:
        return render_template('employee/selfTransactionEnd.html', first_name=session.get("first_name"), last_name=session.get("last_name"))
    # return render_template('employee/selfTransactionEnd.html')
    # บันทึกลง table transaction

@employee.route('/employee/edit/shift/cowork/coworksummary/coworktransactionend', methods=['POST','GET'])
def employeeCoworkTransactionEnd():
    line_id = session.get("line_id") # in case for query
        
    if line_id is None or session.get("first_name") == "userNotFound":
        return render_template('employee/warning.html')
    else:
        return render_template('employee/coworkTransactionEnd.html', first_name=session.get("first_name"), last_name=session.get("last_name"))
    # return render_template('employee/coworkTransactionEnd.html')
    # บันทึกลง table transaction

@employee.route('/employee/edit/shift/addshift/addshiftsummary/addshifttransactionend', methods=['POST','GET'])
def employeeAddShiftTransactionEnd():
    line_id = session.get("line_id") # in case for query
        
    if line_id is None or session.get("first_name") == "userNotFound":
        return render_template('employee/warning.html')
    else:
        return render_template('employee/addShiftTransactionEnd.html', first_name=session.get("first_name"), last_name=session.get("last_name"))
    # return render_template('employee/addShiftTransactionEnd.html')
    # บันทึกลง table transaction

@employee.route('/employee/edit/shiftandoff/shiftandoffsummary/shiftandofftransactionend', methods=['POST','GET'])
def employeeShiftAndOffTransactionEnd():
    line_id = session.get("line_id") # in case for query
        
    if line_id is None or session.get("first_name") == "userNotFound":
        return render_template('employee/warning.html')
    else:
        return render_template('employee/shiftAndOffTransactionEnd.html', first_name=session.get("first_name"), last_name=session.get("last_name"))
    # return render_template('employee/shiftAndOffTransactionEnd.html')
    # บันทึกลง table transaction

@employee.route('/employee/edit/addemployee/addemployeesummary/addemployeetransactionend', methods=['POST','GET'])
def employeeAddEmployeeTransactionEnd():
    line_id = session.get("line_id") # in case for query
        
    if line_id is None or session.get("first_name") == "userNotFound":
        return render_template('employee/warning.html')
    else:
        return render_template('employee/addEmployeeTransactionEnd.html', first_name=session.get("first_name"), last_name=session.get("last_name"))
    # return render_template('employee/addEmployeeTransactionEnd.html')
    # บันทึกลง table transaction
