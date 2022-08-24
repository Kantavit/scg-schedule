from .__init__ import employee
from ..extensions import db, yag
from flask import render_template, redirect, url_for, request, session
import datetime;
import pendulum

# Employee start page
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

    # update employee_section from approver
    cur.execute("SELECT approver_section FROM employeeInfo INNER JOIN approverInfo on approverInfo.approver_id = employeeInfo.approver_id WHERE employee_id=%s", [employee_id])
    approver_section = cur.fetchall()
    cur.execute("UPDATE employeeInfo SET employee_section=%s WHERE employee_id=%s",(approver_section, employee_id))
    db.connection.commit()

    cur.close()

    if bool(first_name) == False and bool(last_name) == False:
        session['first_name'] = "userNotFound" # send first_name to other page
        return render_template('employee/welcome.html')

    session['first_name'] = first_name # send first_name to other page
    session['last_name'] = last_name # send last_name to other page
    session['employee_id'] = employee_id[0][0] # send last_name to other page
    session['sub_team'] = sub_team[0][0]

    return render_template('employee/welcome.html')


# Employee date range
@employee.route('/employee', methods=['POST','GET'])
def employeePage():
    line_id = session.get("line_id") # in case for query

    if line_id is None or session.get("first_name") == "userNotFound":
        return render_template('employee/warning.html')
    else:
        return render_template('employee/employee.html', first_name=session.get("first_name"), last_name=session.get("last_name"))
        

# Employee select to edit 
@employee.route('/employee/edit')
def chooseEdit():
    line_id = session.get("line_id") # in case for query
        
    if line_id is None or session.get("first_name") == "userNotFound":
        return render_template('employee/warning.html')
    else:
        return render_template('employee/employeeEdit.html', first_name=session.get("first_name"), last_name=session.get("last_name"))

####################################################################################################

# Employee see yourself shift date range
@employee.route('/employee/edit/shift')
def chooseEditShift():
    line_id = session.get("line_id") # in case for query
        
    if line_id is None or session.get("first_name") == "userNotFound":
        return render_template('employee/warning.html')
    else:
        return render_template('employee/editShift.html', first_name=session.get("first_name"), last_name=session.get("last_name"))
    # return render_template('employee/editShift.html')


# Employee edit shift themself
@employee.route('/employee/edit/shift/self', methods=['POST','GET'])
def editYourself():
    line_id = session.get("line_id") # in case for query
        
    if line_id is None or session.get("first_name") == "userNotFound":
        return render_template('employee/warning.html')
    else:
        return render_template('employee/selfEdit.html', first_name=session.get("first_name"), last_name=session.get("last_name"))
    # return render_template('employee/selfEdit.html')


# Employee edit shift cowork
@employee.route('/employee/edit/shift/cowork', methods=['POST','GET'])
def editCowork():
    line_id = session.get("line_id") # in case for query
    employee_id = session.get("employee_id")

    # query sub_team
    cur = db.connection.cursor()
    cur.execute("SELECT sub_team FROM employeeInfo WHERE employee_id=%s",[employee_id])
    sub_team = cur.fetchall()
    cur.close()
    
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

    else:
        cur = db.connection.cursor()

        # query sub_team
        cur.execute("SELECT sub_team FROM employeeInfo WHERE employee_id=%s",[employee_id])
        sub_team = cur.fetchall()
        
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

        if count == 1:
            cur.execute("SELECT * FROM employeeShift WHERE employeeShift_id=%s ",[otherEmployee[0]])
            shifts2 = cur.fetchall()
            cur.close()
            return render_template('employee/coworkEdit.html', first_name=session.get("first_name"), last_name=session.get("last_name"),
                                idSub_team=idSub_team, shifts=shifts, shifts2=shifts2)
        elif count == 2:
            cur.execute("SELECT * FROM employeeShift WHERE employeeShift_id=%s ",[otherEmployee[0]])
            shifts2 = cur.fetchall()
            cur.execute("SELECT * FROM employeeShift WHERE employeeShift_id=%s ",[otherEmployee[1]])
            shifts3 = cur.fetchall()
            cur.close()
            return render_template('employee/coworkEdit.html', first_name=session.get("first_name"), last_name=session.get("last_name"),
                                idSub_team=idSub_team, shifts=shifts, shifts2=shifts2, shifts3=shifts3 )
        elif count == 3:
            cur.execute("SELECT * FROM employeeShift WHERE employeeShift_id=%s ",[otherEmployee[0]])
            shifts2 = cur.fetchall()
            cur.execute("SELECT * FROM employeeShift WHERE employeeShift_id=%s ",[otherEmployee[1]])
            shifts3 = cur.fetchall()
            cur.execute("SELECT * FROM employeeShift WHERE employeeShift_id=%s ",[otherEmployee[2]])
            shifts4 = cur.fetchall()
            cur.close()
            return render_template('employee/coworkEdit.html', first_name=session.get("first_name"), last_name=session.get("last_name"),
                                idSub_team=idSub_team, shifts=shifts, shifts2=shifts2, shifts3=shifts3, shifts4=shifts4 )
        elif count == 4:
            cur.execute("SELECT * FROM employeeShift WHERE employeeShift_id=%s ",[otherEmployee[0]])
            shifts2 = cur.fetchall()
            cur.execute("SELECT * FROM employeeShift WHERE employeeShift_id=%s ",[otherEmployee[1]])
            shifts3 = cur.fetchall()
            cur.execute("SELECT * FROM employeeShift WHERE employeeShift_id=%s ",[otherEmployee[2]])
            shifts4 = cur.fetchall()
            cur.execute("SELECT * FROM employeeShift WHERE employeeShift_id=%s ",[otherEmployee[3]])
            shifts5 = cur.fetchall()
            cur.close()
            return render_template('employee/coworkEdit.html', first_name=session.get("first_name"), last_name=session.get("last_name"),
                                idSub_team=idSub_team, shifts=shifts, shifts2=shifts2, shifts3=shifts3, shifts4=shifts4, shifts5=shifts5 )
        else:
            return render_template('employee/coworkEdit.html', first_name=session.get("first_name"), last_name=session.get("last_name"),
                                idSub_team=idSub_team, shifts=shifts )


# Employee add shift in the same day
@employee.route('/employee/edit/shift/addshift', methods=['POST','GET'])
def editAddShift():
    line_id = session.get("line_id") # in case for query
    employee_id = session.get("employee_id")
    requestId = employee_id
        
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

            cur.execute("INSERT INTO transactionaddShift (requestId, employee_id , date , OldShift , addShift , TimeStamp ,  reason , status , approver_id ) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)",(requestId, employee_id , date , OldShift , addShift , TimeStamp ,  reason , status , approver_id))
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
            cur.execute("UPDATE transactionaddShift SET requestId=%s, date=%s , OldShift=%s , addShift=%s , reason=%s , TimeStamp=%s WHERE transactionaddShift_id=%s",(requestId, date , OldShift , addShift , reason, TimeStamp, transactionaddShift_id))
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
        transactionaddShift_element = cur.execute(" SELECT * FROM transactionaddShift WHERE requestId=%s AND status=%s", (employee_id, "unsuccessful"))
        transactionaddShift = cur.fetchall()
        query = "SELECT * FROM employeeShift WHERE employeeShift_id = " + "'" + employee_id + "'"
        cur.execute(query)
        shifts = cur.fetchall()
        cur.close()

        return render_template('employee/addshiftEdit.html', first_name=session.get("first_name"), last_name=session.get("last_name"),
                        transactionaddShift_element=transactionaddShift_element, transactionaddShift=transactionaddShift, shifts=shifts)


####################################################################################################

# Employee edit shift and off work
@employee.route('/employee/edit/shiftandoff', methods=['POST','GET'])
def chooseEditShiftAndOff():
    line_id = session.get("line_id") # in case for query
    employee_id = session.get("employee_id")
    requestId = employee_id
    
    # query sub_team
    cur = db.connection.cursor()
    cur.execute("SELECT sub_team FROM employeeInfo WHERE employee_id=%s",[employee_id])
    sub_team = cur.fetchall()
    cur.close()
        
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

            cur.execute("INSERT INTO transactionChangeWork (requestId, employee_id , employee_name , employee_lastname, date, Oldwork_type, Newwork_type, Oldoff_code, Newoff_code, section_code, reason, TimeStamp, status, approver_id, director_id ) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(requestId, employee_id , employee_name , employee_lastname, date, Oldwork_type, Newwork_type, Oldoff_code, Newoff_code, section_code, reason, TimeStamp, status, approver_id, director_id))
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

            cur.execute("UPDATE transactionChangeWork SET requestId=%s, employee_id=%s , employee_name=%s , employee_lastname=%s, date=%s, Oldwork_type=%s, Newwork_type=%s, Oldoff_code=%s, Newoff_code=%s, section_code=%s, reason=%s, TimeStamp=%s, status=%s, approver_id=%s, director_id=%s WHERE transactionChangeWork_id=%s",(requestId, employee_id , employee_name , employee_lastname, date, Oldwork_type, Newwork_type, Oldoff_code, Newoff_code, section_code, reason, TimeStamp, status, approver_id, director_id, transactionChangeWork_id))
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

        # get all section_code
        section_code_element = cur.execute("SELECT Remark, dayoff, section_code FROM filtershift")
        section_code_data = cur.fetchall()
        
        transactionChangeWork_element = cur.execute(" SELECT * FROM transactionChangeWork WHERE requestId=%s AND status=%s", (employee_id, "unsuccessful"))
        transactionChangeWork = cur.fetchall()

        otherEmployee = [0]*count
        for i in range(count):
            otherEmployee[i] = idSub_team[i][0]


        cur.execute("SELECT employee_id,Remark , dayoff FROM filtershift INNER JOIN employeeInfo ON filtershift.section_code = employeeInfo.section_code WHERE employee_id=%s",[employee_id])
        workData1 = cur.fetchall()

        if count == 1:
            cur.execute("SELECT employee_id,Remark , dayoff FROM filtershift INNER JOIN employeeInfo ON filtershift.section_code = employeeInfo.section_code WHERE employee_id=%s",[otherEmployee[0]])
            workData2 = cur.fetchall()
            cur.close()
            return render_template('employee/editShiftAndOff.html', first_name=session.get("first_name"), last_name=session.get("last_name"),
                                idSub_teamAll=idSub_teamAll, workData1=workData1, workData2=workData2, section_code_element=section_code_element,
                                section_code_data=section_code_data, transactionChangeWork_element=transactionChangeWork_element, transactionChangeWork=transactionChangeWork )
        elif count == 2:
            cur.execute("SELECT employee_id,Remark , dayoff FROM filtershift INNER JOIN employeeInfo ON filtershift.section_code = employeeInfo.section_code WHERE employee_id=%s",[otherEmployee[0]])
            workData2 = cur.fetchall()
            cur.execute("SELECT employee_id,Remark , dayoff FROM filtershift INNER JOIN employeeInfo ON filtershift.section_code = employeeInfo.section_code WHERE employee_id=%s",[otherEmployee[1]])
            workData3 = cur.fetchall()
            cur.close()
            return render_template('employee/editShiftAndOff.html', first_name=session.get("first_name"), last_name=session.get("last_name"),
                                idSub_teamAll=idSub_teamAll, workData1=workData1, workData2=workData2, workData3=workData3, section_code_element=section_code_element,
                                section_code_data=section_code_data, transactionChangeWork_element=transactionChangeWork_element, transactionChangeWork=transactionChangeWork )
        elif count == 3:
            cur.execute("SELECT employee_id,Remark , dayoff FROM filtershift INNER JOIN employeeInfo ON filtershift.section_code = employeeInfo.section_code WHERE employee_id=%s",[otherEmployee[0]])
            workData2 = cur.fetchall()
            cur.execute("SELECT employee_id,Remark , dayoff FROM filtershift INNER JOIN employeeInfo ON filtershift.section_code = employeeInfo.section_code WHERE employee_id=%s",[otherEmployee[1]])
            workData3 = cur.fetchall()
            cur.execute("SELECT employee_id,Remark , dayoff FROM filtershift INNER JOIN employeeInfo ON filtershift.section_code = employeeInfo.section_code WHERE employee_id=%s",[otherEmployee[2]])
            workData4 = cur.fetchall()
            cur.close()
            return render_template('employee/editShiftAndOff.html', first_name=session.get("first_name"), last_name=session.get("last_name"),
                                idSub_teamAll=idSub_teamAll, workData1=workData1, workData2=workData2, workData3=workData3, workData4=workData4, section_code_element=section_code_element,
                                section_code_data=section_code_data, transactionChangeWork_element=transactionChangeWork_element, transactionChangeWork=transactionChangeWork )
        elif count == 4:
            cur.execute("SELECT employee_id,Remark , dayoff FROM filtershift INNER JOIN employeeInfo ON filtershift.section_code = employeeInfo.section_code WHERE employee_id=%s",[otherEmployee[0]])
            workData2 = cur.fetchall()
            cur.execute("SELECT employee_id,Remark , dayoff FROM filtershift INNER JOIN employeeInfo ON filtershift.section_code = employeeInfo.section_code WHERE employee_id=%s",[otherEmployee[1]])
            workData3 = cur.fetchall()
            cur.execute("SELECT employee_id,Remark , dayoff FROM filtershift INNER JOIN employeeInfo ON filtershift.section_code = employeeInfo.section_code WHERE employee_id=%s",[otherEmployee[2]])
            workData4 = cur.fetchall()
            cur.execute("SELECT employee_id,Remark , dayoff FROM filtershift INNER JOIN employeeInfo ON filtershift.section_code = employeeInfo.section_code WHERE employee_id=%s",[otherEmployee[3]])
            workData5 = cur.fetchall()
            cur.close()
            return render_template('employee/editShiftAndOff.html', first_name=session.get("first_name"), last_name=session.get("last_name"),
                                idSub_teamAll=idSub_teamAll, workData1=workData1, workData2=workData2, workData3=workData3, workData4=workData4, workData5=workData5, section_code_element=section_code_element,
                                section_code_data=section_code_data, transactionChangeWork_element=transactionChangeWork_element, transactionChangeWork=transactionChangeWork )
        else:
            return render_template('employee/editShiftAndOff.html', first_name=session.get("first_name"), last_name=session.get("last_name"),
                                idSub_teamAll=idSub_teamAll, workData1=workData1, section_code_element=section_code_element,
                                section_code_data=section_code_data, transactionChangeWork_element=transactionChangeWork_element, transactionChangeWork=transactionChangeWork )


####################################################################################################

# Employee check transaction status
@employee.route('/employee/edit/status')
def chooseCheckStatus():
    line_id = session.get("line_id") # in case for query
    employee_id = session.get("employee_id")

    waitCount = 0
    cur = db.connection.cursor()
    cur.execute("SELECT COUNT(transactionaddemployee_id) FROM transactionaddemployee WHERE requestId=%s AND status=%s",(employee_id, "waiting"))
    transactionaddemployee_count = cur.fetchall()
    waitCount = waitCount + transactionaddemployee_count[0][0]

    cur.execute("SELECT COUNT(transactionaddShift_id) FROM transactionaddShift WHERE requestId=%s AND status=%s",(employee_id, "waiting"))
    transactionaddShift_count = cur.fetchall()
    waitCount = waitCount + transactionaddShift_count[0][0]

    cur.execute("SELECT COUNT(transactionChangeShift_id) FROM transactionChangeShift WHERE requestId=%s AND status=%s",(employee_id, "waiting"))
    transactionChangeShift_count = cur.fetchall()
    waitCount = waitCount + transactionChangeShift_count[0][0]

    cur.execute("SELECT COUNT(transactionChangeWork_id) FROM transactionChangeWork WHERE requestId=%s AND status=%s AND status2 IS NULL",(employee_id, "waiting"))
    transactionChangeWork_count = cur.fetchall()
    waitCount = waitCount + transactionChangeWork_count[0][0]

    cur.execute("SELECT COUNT(transactionCoworkShift_id) FROM transactionCoworkShift WHERE requestId=%s AND status=%s",(employee_id, "waiting"))
    transactionCoworkShift_count = cur.fetchall()
    waitCount = waitCount + transactionCoworkShift_count[0][0]

    approveCount = 0
    cur = db.connection.cursor()
    cur.execute("SELECT COUNT(transactionaddemployee_id) FROM transactionaddemployee WHERE requestId=%s AND status=%s",(employee_id, "approve"))
    transactionaddemployee_count = cur.fetchall()
    approveCount = approveCount + transactionaddemployee_count[0][0]

    cur.execute("SELECT COUNT(transactionaddShift_id) FROM transactionaddShift WHERE requestId=%s AND status=%s",(employee_id, "approve"))
    transactionaddShift_count = cur.fetchall()
    approveCount = approveCount + transactionaddShift_count[0][0]

    cur.execute("SELECT COUNT(transactionChangeShift_id) FROM transactionChangeShift WHERE requestId=%s AND status=%s",(employee_id, "approve"))
    transactionChangeShift_count = cur.fetchall()
    approveCount = approveCount + transactionChangeShift_count[0][0]

    cur.execute("SELECT COUNT(transactionChangeWork_id) FROM transactionChangeWork WHERE requestId=%s AND status=%s AND status2=%s",(employee_id, "approve", "approve"))
    transactionChangeWork_count = cur.fetchall()
    approveCount = approveCount + transactionChangeWork_count[0][0]

    cur.execute("SELECT COUNT(transactionCoworkShift_id) FROM transactionCoworkShift WHERE requestId=%s AND status=%s",(employee_id, "approve"))
    transactionCoworkShift_count = cur.fetchall()
    approveCount = approveCount + transactionCoworkShift_count[0][0]

    rejectCount = 0
    cur = db.connection.cursor()
    cur.execute("SELECT COUNT(transactionaddemployee_id) FROM transactionaddemployee WHERE requestId=%s AND status=%s",(employee_id, "reject"))
    transactionaddemployee_count = cur.fetchall()
    rejectCount = rejectCount + transactionaddemployee_count[0][0]

    cur.execute("SELECT COUNT(transactionaddShift_id) FROM transactionaddShift WHERE requestId=%s AND status=%s",(employee_id, "reject"))
    transactionaddShift_count = cur.fetchall()
    rejectCount = rejectCount + transactionaddShift_count[0][0]

    cur.execute("SELECT COUNT(transactionChangeShift_id) FROM transactionChangeShift WHERE requestId=%s AND status=%s",(employee_id, "reject"))
    transactionChangeShift_count = cur.fetchall()
    rejectCount = rejectCount + transactionChangeShift_count[0][0]

    cur.execute("SELECT COUNT(transactionChangeWork_id) FROM transactionChangeWork WHERE requestId=%s AND status=%s AND status2=%s",(employee_id, "reject", "reject"))
    transactionChangeWork_count = cur.fetchall()
    rejectCount = rejectCount + transactionChangeWork_count[0][0]

    cur.execute("SELECT COUNT(transactionCoworkShift_id) FROM transactionCoworkShift WHERE requestId=%s AND status=%s",(employee_id, "reject"))
    transactionCoworkShift_count = cur.fetchall()
    rejectCount = rejectCount + transactionCoworkShift_count[0][0]


    if line_id is None or session.get("first_name") == "userNotFound":
        return render_template('employee/warning.html')
    else:

        return render_template('employee/checkStatus.html', first_name=session.get("first_name"), last_name=session.get("last_name"), waitCount=waitCount, approveCount=approveCount, rejectCount=rejectCount)


# Employee check pending transaction
@employee.route('/employee/edit/status/pending', methods=['POST','GET'])
def pending():
    line_id = session.get("line_id") # in case for query
    employee_id = session.get("employee_id")
        
    if line_id is None or session.get("first_name") == "userNotFound":
        return render_template('employee/warning.html')
        
    elif request.method == 'POST':
        if request.form['select'] == "addemployee":
            if request.form['choose'] == "update":
                transactionaddemployee_id = request.form['transactionaddemployee_id']
                status = "unsuccessful"

                cur = db.connection.cursor()
                cur.execute("UPDATE transactionaddemployee SET status=%s, requestId=%s WHERE transactionaddemployee_id=%s",(status, employee_id, transactionaddemployee_id))
                db.connection.commit()
                cur.close()
                return redirect(url_for('employee.addEmployee'))

            elif request.form['choose'] == "delete":
                transactionaddemployee_id = request.form['transactionaddemployee_id']

                cur = db.connection.cursor()
                cur.execute("DELETE FROM transactionaddemployee WHERE transactionaddemployee_id=%s",[transactionaddemployee_id])
                db.connection.commit()
                cur.close()
                return redirect(url_for('employee.pending'))

        elif request.form['select'] == "addShift":
            if request.form['choose'] == "update":
                transactionaddShift_id = request.form['transactionaddShift_id']
                status = "unsuccessful"

                cur = db.connection.cursor()
                cur.execute("UPDATE transactionaddShift SET status=%s, requestId=%s WHERE transactionaddShift_id=%s",(status, employee_id, transactionaddShift_id))
                db.connection.commit()
                cur.close()
                return redirect(url_for('employee.editAddShift'))

            elif request.form['choose'] == "delete":
                transactionaddShift_id = request.form['transactionaddShift_id']

                cur = db.connection.cursor()
                cur.execute("DELETE FROM transactionaddShift WHERE transactionaddShift_id=%s",[transactionaddShift_id])
                db.connection.commit()
                cur.close()
                return redirect(url_for('employee.pending'))

        elif request.form['select'] == "ChangeShift":
            if request.form['choose'] == "update":
                transactionChangeShift_id = request.form['transactionChangeShift_id']
                status = "unsuccessful"

                cur = db.connection.cursor()
                cur.execute("UPDATE transactionChangeShift SET status=%s, requestId=%s WHERE transactionChangeShift_id=%s",(status, employee_id, transactionChangeShift_id))
                db.connection.commit()
                cur.close()
                return redirect(url_for('employee.editYourselfList'))

            elif request.form['choose'] == "delete":
                transactionChangeShift_id = request.form['transactionChangeShift_id']

                cur = db.connection.cursor()
                cur.execute("DELETE FROM transactionChangeShift WHERE transactionChangeShift_id=%s",[transactionChangeShift_id])
                db.connection.commit()
                cur.close()
                return redirect(url_for('employee.pending'))

        elif request.form['select'] == "ChangeWork":
            if request.form['choose'] == "update":
                transactionChangeWork_id = request.form['transactionChangeWork_id']
                status = "unsuccessful"

                cur = db.connection.cursor()
                cur.execute("UPDATE transactionChangeWork SET status=%s, requestId=%s WHERE transactionChangeWork_id=%s",(status, employee_id, transactionChangeWork_id))
                db.connection.commit()
                cur.close()
                return redirect(url_for('employee.chooseEditShiftAndOff'))

            elif request.form['choose'] == "delete":
                transactionChangeWork_id = request.form['transactionChangeWork_id']

                cur = db.connection.cursor()
                cur.execute("DELETE FROM transactionChangeWork WHERE transactionChangeWork_id=%s",[transactionChangeWork_id])
                db.connection.commit()
                cur.close()
                return redirect(url_for('employee.pending'))

        elif request.form['select'] == "CoworkShift":
            if request.form['choose'] == "delete":
                transactionCoworkShift_id = request.form['transactionCoworkShift_id']

                cur = db.connection.cursor()
                cur.execute("DELETE FROM transactionCoworkShift WHERE transactionCoworkShift_id=%s",[transactionCoworkShift_id])
                db.connection.commit()
                cur.close()
                return redirect(url_for('employee.pending'))

    else:
        cur = db.connection.cursor()
        transactionaddemployee_element = cur.execute("SELECT transactionaddemployee_id, employee_id, employee_name,employee_lastname, date_start, date_end, Oldsection, Newsection, TimeStamp, reason, transactionaddemployee.approver_id, consider_time, status, requestId, approver_name, approver_lastname FROM transactionaddemployee INNER JOIN approverInfo on transactionaddemployee.approver_id = approverInfo.approver_id WHERE requestId = " + "'" + employee_id + "'" + " AND status='waiting'")
        transactionaddemployee = cur.fetchall()

        transactionaddShift_element = cur.execute("SELECT * FROM transactionaddShift WHERE requestId=%s AND status=%s",(employee_id, "waiting"))
        transactionaddShift = cur.fetchall()

        transactionChangeShift_element = cur.execute("SELECT * FROM transactionChangeShift WHERE requestId=%s AND status=%s",(employee_id, "waiting"))
        transactionChangeShift = cur.fetchall()

        transactionChangeWork_element = cur.execute("SELECT * FROM transactionChangeWork WHERE requestId=%s AND status=%s AND status2 IS NULL",(employee_id, "waiting"))
        transactionChangeWork = cur.fetchall()

        transactionCoworkShift_element = cur.execute("SELECT * FROM transactionCoworkShift WHERE requestId=%s AND status=%s",(employee_id, "waiting"))
        transactionCoworkShift = cur.fetchall()

        return render_template('employee/pending.html', first_name=session.get("first_name"), last_name=session.get("last_name"), 
                    transactionaddemployee=transactionaddemployee,transactionaddemployee_element=transactionaddemployee_element,
                    transactionaddShift=transactionaddShift,transactionaddShift_element=transactionaddShift_element,
                    transactionChangeShift=transactionChangeShift,transactionChangeShift_element=transactionChangeShift_element,
                    transactionChangeWork=transactionChangeWork,transactionChangeWork_element=transactionChangeWork_element,
                    transactionCoworkShift=transactionCoworkShift,transactionCoworkShift_element=transactionCoworkShift_element)


# Employee check approved transaction
@employee.route('/employee/edit/status/approve')
def approve():
    line_id = session.get("line_id") # in case for query
    employee_id = session.get("employee_id")
        
    if line_id is None or session.get("first_name") == "userNotFound":
        return render_template('employee/warning.html')
    else:
        cur = db.connection.cursor()
        transactionaddemployee_element = cur.execute("SELECT transactionaddemployee_id, employee_id, employee_name,employee_lastname, date_start, date_end, Oldsection, Newsection, TimeStamp, reason, transactionaddemployee.approver_id, consider_time, status, requestId, approver_name, approver_lastname FROM transactionaddemployee INNER JOIN approverInfo on transactionaddemployee.approver_id = approverInfo.approver_id WHERE requestId = " + "'" + employee_id + "'" + " AND status='approve'")
        transactionaddemployee = cur.fetchall()

        transactionaddShift_element = cur.execute("SELECT transactionaddShift_id ,transactionaddShift.employee_id ,date ,OldShift ,addShift ,TimeStamp ,reason ,Status ,transactionaddShift.approver_id ,consider_time ,requestId , employee_name , employee_lastname , approver_name, approver_lastname FROM transactionaddShift INNER JOIN employeeInfo on transactionaddShift.employee_id = employeeInfo.employee_id INNER JOIN approverInfo on transactionaddShift.approver_id = approverInfo.approver_id WHERE requestId = " + "'" + employee_id + "'" + " AND status='approve'")
        transactionaddShift = cur.fetchall()

        transactionChangeShift_element = cur.execute("SELECT transactionChangeShift_id,transactionChangeShift.employee_id,date,OldShift,NewShift,TimeStamp,reason , Status ,transactionChangeShift.approver_id,consider_time, requestId, employee_name , employee_lastname, approver_name, approver_lastname FROM `transactionChangeShift` INNER JOIN employeeInfo on transactionChangeShift.employee_id = employeeInfo.employee_id INNER JOIN approverInfo on transactionChangeShift.approver_id = approverInfo.approver_id WHERE requestId = " + "'" + employee_id + "'" + " AND status='approve'")
        transactionChangeShift = cur.fetchall()

        transactionChangeWork_element = cur.execute("SELECT transactionChangeWork_id ,employee_id,employee_name ,employee_lastname ,date ,TimeStamp ,reason ,Status ,transactionChangeWork.approver_id ,consider_time1 ,consider_time2 ,transactionChangeWork.director_id ,Oldwork_type ,Newwork_type ,Oldoff_code ,Newoff_code ,section_code ,requestId ,status2, approver_name, approver_lastname, director_name, director_lastname FROM transactionChangeWork INNER JOIN approverInfo on transactionChangeWork.approver_id = approverInfo.approver_id INNER JOIN directorInfo on transactionChangeWork.director_id = directorInfo.director_id WHERE requestId = " + "'" + employee_id + "'" + " AND status='approve' AND status2='approve'")
        transactionChangeWork = cur.fetchall()

        transactionCoworkShift_element = cur.execute("SELECT transactionCoworkShift_id,transactionCoworkShift.employee_id,date,OldShift,NewShift,TimeStamp,reason,Status,transactionCoworkShift.approver_id,consider_time ,employee_id2 ,employee_name2 ,employee_lastname2 ,OldShift2 ,NewShift2 ,employee_id3 ,employee_name3 ,employee_lastname3 ,OldShift3 ,NewShift3 ,requestId ,employee_name , employee_lastname, approver_name , approver_lastname FROM `transactionCoworkShift` INNER JOIN employeeInfo on transactionCoworkShift.employee_id = employeeInfo.employee_id INNER JOIN approverInfo on transactionCoworkShift.approver_id = approverInfo.approver_id WHERE requestId = " + "'" + employee_id + "'" + " AND status='approve'")
        transactionCoworkShift = cur.fetchall()

        return render_template('employee/approve.html', first_name=session.get("first_name"), last_name=session.get("last_name"), 
                    transactionaddemployee=transactionaddemployee,transactionaddemployee_element=transactionaddemployee_element,
                    transactionaddShift=transactionaddShift,transactionaddShift_element=transactionaddShift_element,
                    transactionChangeShift=transactionChangeShift,transactionChangeShift_element=transactionChangeShift_element,
                    transactionChangeWork=transactionChangeWork,transactionChangeWork_element=transactionChangeWork_element,
                    transactionCoworkShift=transactionCoworkShift,transactionCoworkShift_element=transactionCoworkShift_element)


# Employee check rejected transaction
@employee.route('/employee/edit/status/reject')
def reject():
    line_id = session.get("line_id") # in case for query
    employee_id = session.get("employee_id")
        
    if line_id is None or session.get("first_name") == "userNotFound":
        return render_template('employee/warning.html')
    else:
        cur = db.connection.cursor()
        transactionaddemployee_element = cur.execute("SELECT transactionaddemployee_id, employee_id, employee_name,employee_lastname, date_start, date_end, Oldsection, Newsection, TimeStamp, reason, transactionaddemployee.approver_id, consider_time, status, requestId, approver_name, approver_lastname FROM transactionaddemployee INNER JOIN approverInfo on transactionaddemployee.approver_id = approverInfo.approver_id WHERE requestId = " + "'" + employee_id + "'" + " AND status='reject'")
        transactionaddemployee = cur.fetchall()

        transactionaddShift_element = cur.execute("SELECT transactionaddShift_id ,transactionaddShift.employee_id ,date ,OldShift ,addShift ,TimeStamp ,reason ,Status ,transactionaddShift.approver_id ,consider_time ,requestId , employee_name , employee_lastname , approver_name, approver_lastname FROM transactionaddShift INNER JOIN employeeInfo on transactionaddShift.employee_id = employeeInfo.employee_id INNER JOIN approverInfo on transactionaddShift.approver_id = approverInfo.approver_id WHERE requestId = " + "'" + employee_id + "'" + " AND status='reject'")
        transactionaddShift = cur.fetchall()

        transactionChangeShift_element = cur.execute("SELECT transactionChangeShift_id,transactionChangeShift.employee_id,date,OldShift,NewShift,TimeStamp,reason , Status ,transactionChangeShift.approver_id,consider_time, requestId, employee_name , employee_lastname, approver_name, approver_lastname FROM `transactionChangeShift` INNER JOIN employeeInfo on transactionChangeShift.employee_id = employeeInfo.employee_id INNER JOIN approverInfo on transactionChangeShift.approver_id = approverInfo.approver_id WHERE requestId = " + "'" + employee_id + "'" + " AND status='reject'")
        transactionChangeShift = cur.fetchall()

        transactionChangeWork_element = cur.execute("SELECT transactionChangeWork_id ,employee_id,employee_name ,employee_lastname ,date ,TimeStamp ,reason ,Status ,transactionChangeWork.approver_id ,consider_time1 ,consider_time2 ,transactionChangeWork.director_id ,Oldwork_type ,Newwork_type ,Oldoff_code ,Newoff_code ,section_code ,requestId ,status2, approver_name, approver_lastname, director_name, director_lastname FROM transactionChangeWork INNER JOIN approverInfo on transactionChangeWork.approver_id = approverInfo.approver_id INNER JOIN directorInfo on transactionChangeWork.director_id = directorInfo.director_id WHERE requestId = " + "'" + employee_id + "'" + " AND status='reject' AND status2='reject'")
        transactionChangeWork = cur.fetchall()

        transactionCoworkShift_element = cur.execute("SELECT transactionCoworkShift_id,transactionCoworkShift.employee_id,date,OldShift,NewShift,TimeStamp,reason,Status,transactionCoworkShift.approver_id,consider_time ,employee_id2 ,employee_name2 ,employee_lastname2 ,OldShift2 ,NewShift2 ,employee_id3 ,employee_name3 ,employee_lastname3 ,OldShift3 ,NewShift3 ,requestId ,employee_name , employee_lastname, approver_name , approver_lastname FROM `transactionCoworkShift` INNER JOIN employeeInfo on transactionCoworkShift.employee_id = employeeInfo.employee_id INNER JOIN approverInfo on transactionCoworkShift.approver_id = approverInfo.approver_id WHERE requestId = " + "'" + employee_id + "'" + " AND status='reject'")
        transactionCoworkShift = cur.fetchall()

        return render_template('employee/reject.html', first_name=session.get("first_name"), last_name=session.get("last_name"), 
                    transactionaddemployee=transactionaddemployee,transactionaddemployee_element=transactionaddemployee_element,
                    transactionaddShift=transactionaddShift,transactionaddShift_element=transactionaddShift_element,
                    transactionChangeShift=transactionChangeShift,transactionChangeShift_element=transactionChangeShift_element,
                    transactionChangeWork=transactionChangeWork,transactionChangeWork_element=transactionChangeWork_element,
                    transactionCoworkShift=transactionCoworkShift,transactionCoworkShift_element=transactionCoworkShift_element)


####################################################################################################

# Employee add employee in new section or edit sub team
@employee.route('/employee/edit/addemployee', methods=['POST','GET'])
def addEmployee():
    line_id = session.get("line_id") # in case for query
    employee_id = session.get("employee_id")
    sub_team = session.get("sub_team")
    requestId = employee_id
        
    if line_id is None or session.get("first_name") == "userNotFound":
        return render_template('employee/warning.html')
    
    elif request.method == 'POST':
        if request.form['select'] == "sub_team":
            if request.form['choose'] == "add":
                addToTeam = request.form['addToTeam']
                createTeam = request.form['createTeam']
                name1 = request.form['name-team1']
                name2 = request.form['name-team2']
                name3 = request.form['name-team3']
                name4 = request.form['name-team4']
                name5 = request.form['name-team5']

                cur = db.connection.cursor()

                if request.form['choose2'] == "เพิ่มสมาชิก":  
                    if name1 != "none":
                        cur.execute("UPDATE employeeInfo SET sub_team=%s WHERE employee_id=%s",(addToTeam, name1))
                        try:
                            cur.execute("SELECT employee_name, employee_lastname, employee_email FROM employeeInfo WHERE employee_id=%s",[name1])
                            employee_data = cur.fetchall()
                            employee_name = employee_data[0][0]
                            employee_lastname = employee_data[0][1]
                            employee_email = employee_data[0][2]

                            current_time = datetime.datetime.now()
                            TimeStamp = current_time.strftime("%Y-%m-%d")

                            recipients = [employee_email]
                            subject = 'ระบบมีรายการเปลี่ยนทีมย่อย'
                            body = f'เรียน {employee_name} {employee_lastname},\n\nอีเมล์นี้เป็นอีเมล์อัตโนมัติทีส่งจากระบบ SCG-Schedule\n\nด้วยความเคารพ,\nระบบมีรายการเปลี่ยนทีมย่อยของท่านให้อยู่ในทีม {addToTeam} เรียบร้อยแล้ว (เมื่อวันที่ {TimeStamp} ท่านสามารถตรวจสอบผ่านลิงก์ด้านล่าง http://127.0.0.1:5000'
                            yag.useralias = 'testbyNamhvam'
                            yag.send(to=recipients,subject=subject,contents=[body])
                            print ('ส่ง Email สำเร็จ')
                        except IndexError:
                            pass
                    if name2 != "none":
                        cur.execute("UPDATE employeeInfo SET sub_team=%s WHERE employee_id=%s",(addToTeam, name2))
                        try:
                            cur.execute("SELECT employee_name, employee_lastname, employee_email FROM employeeInfo WHERE employee_id=%s",[name2])
                            employee_data = cur.fetchall()
                            employee_name = employee_data[0][0]
                            employee_lastname = employee_data[0][1]
                            employee_email = employee_data[0][2]

                            current_time = datetime.datetime.now()
                            TimeStamp = current_time.strftime("%Y-%m-%d")

                            recipients = [employee_email]
                            subject = 'ระบบมีรายการเปลี่ยนทีมย่อย'
                            body = f'เรียน {employee_name} {employee_lastname},\n\nอีเมล์นี้เป็นอีเมล์อัตโนมัติทีส่งจากระบบ SCG-Schedule\n\nด้วยความเคารพ,\nระบบมีรายการเปลี่ยนทีมย่อยของท่านให้อยู่ในทีม {addToTeam} เรียบร้อยแล้ว (เมื่อวันที่ {TimeStamp} ท่านสามารถตรวจสอบผ่านลิงก์ด้านล่าง http://127.0.0.1:5000'
                            yag.useralias = 'testbyNamhvam'
                            yag.send(to=recipients,subject=subject,contents=[body])
                            print ('ส่ง Email สำเร็จ')
                        except IndexError:
                            pass
                    if name3 != "none":
                        cur.execute("UPDATE employeeInfo SET sub_team=%s WHERE employee_id=%s",(addToTeam, name3))
                        try:
                            cur.execute("SELECT employee_name, employee_lastname, employee_email FROM employeeInfo WHERE employee_id=%s",[name3])
                            employee_data = cur.fetchall()
                            employee_name = employee_data[0][0]
                            employee_lastname = employee_data[0][1]
                            employee_email = employee_data[0][2]

                            current_time = datetime.datetime.now()
                            TimeStamp = current_time.strftime("%Y-%m-%d")

                            recipients = [employee_email]
                            subject = 'ระบบมีรายการเปลี่ยนทีมย่อย'
                            body = f'เรียน {employee_name} {employee_lastname},\n\nอีเมล์นี้เป็นอีเมล์อัตโนมัติทีส่งจากระบบ SCG-Schedule\n\nด้วยความเคารพ,\nระบบมีรายการเปลี่ยนทีมย่อยของท่านให้อยู่ในทีม {addToTeam} เรียบร้อยแล้ว (เมื่อวันที่ {TimeStamp} ท่านสามารถตรวจสอบผ่านลิงก์ด้านล่าง http://127.0.0.1:5000'
                            yag.useralias = 'testbyNamhvam'
                            yag.send(to=recipients,subject=subject,contents=[body])
                            print ('ส่ง Email สำเร็จ')
                        except IndexError:
                            pass
                    if name4 != "none":
                        cur.execute("UPDATE employeeInfo SET sub_team=%s WHERE employee_id=%s",(addToTeam, name4))
                        try:
                            cur.execute("SELECT employee_name, employee_lastname, employee_email FROM employeeInfo WHERE employee_id=%s",[name4])
                            employee_data = cur.fetchall()
                            employee_name = employee_data[0][0]
                            employee_lastname = employee_data[0][1]
                            employee_email = employee_data[0][2]

                            current_time = datetime.datetime.now()
                            TimeStamp = current_time.strftime("%Y-%m-%d")

                            recipients = [employee_email]
                            subject = 'ระบบมีรายการเปลี่ยนทีมย่อย'
                            body = f'เรียน {employee_name} {employee_lastname},\n\nอีเมล์นี้เป็นอีเมล์อัตโนมัติทีส่งจากระบบ SCG-Schedule\n\nด้วยความเคารพ,\nระบบมีรายการเปลี่ยนทีมย่อยของท่านให้อยู่ในทีม {addToTeam} เรียบร้อยแล้ว (เมื่อวันที่ {TimeStamp} ท่านสามารถตรวจสอบผ่านลิงก์ด้านล่าง http://127.0.0.1:5000'
                            yag.useralias = 'testbyNamhvam'
                            yag.send(to=recipients,subject=subject,contents=[body])
                            print ('ส่ง Email สำเร็จ')
                        except IndexError:
                            pass
                    if name5 != "none":
                        cur.execute("UPDATE employeeInfo SET sub_team=%s WHERE employee_id=%s",(addToTeam, name5))
                        try:
                            cur.execute("SELECT employee_name, employee_lastname, employee_email FROM employeeInfo WHERE employee_id=%s",[name5])
                            employee_data = cur.fetchall()
                            employee_name = employee_data[0][0]
                            employee_lastname = employee_data[0][1]
                            employee_email = employee_data[0][2]

                            current_time = datetime.datetime.now()
                            TimeStamp = current_time.strftime("%Y-%m-%d")

                            recipients = [employee_email]
                            subject = 'ระบบมีรายการเปลี่ยนทีมย่อย'
                            body = f'เรียน {employee_name} {employee_lastname},\n\nอีเมล์นี้เป็นอีเมล์อัตโนมัติทีส่งจากระบบ SCG-Schedule\n\nด้วยความเคารพ,\nระบบมีรายการเปลี่ยนทีมย่อยของท่านให้อยู่ในทีม {addToTeam} เรียบร้อยแล้ว (เมื่อวันที่ {TimeStamp} ท่านสามารถตรวจสอบผ่านลิงก์ด้านล่าง http://127.0.0.1:5000'
                            yag.useralias = 'testbyNamhvam'
                            yag.send(to=recipients,subject=subject,contents=[body])
                            print ('ส่ง Email สำเร็จ')
                        except IndexError:
                            pass
                elif request.form['choose2'] == "สร้างทีม":
                    if name1 != "none":
                        cur.execute("UPDATE employeeInfo SET sub_team=%s WHERE employee_id=%s",(createTeam, name1))
                        try:
                            cur.execute("SELECT employee_name, employee_lastname, employee_email FROM employeeInfo WHERE employee_id=%s",[name1])
                            employee_data = cur.fetchall()
                            employee_name = employee_data[0][0]
                            employee_lastname = employee_data[0][1]
                            employee_email = employee_data[0][2]

                            current_time = datetime.datetime.now()
                            TimeStamp = current_time.strftime("%Y-%m-%d")

                            recipients = [employee_email]
                            subject = 'ระบบมีรายการสร้างทีมย่อยใหม่'
                            body = f'เรียน {employee_name} {employee_lastname},\n\nอีเมล์นี้เป็นอีเมล์อัตโนมัติทีส่งจากระบบ SCG-Schedule\n\nด้วยความเคารพ,\nระบบมีรายการสร้างทีมย่อยใหม่ของท่านให้อยู่ในทีม {createTeam} เรียบร้อยแล้ว (เมื่อวันที่ {TimeStamp} ท่านสามารถตรวจสอบผ่านลิงก์ด้านล่าง http://127.0.0.1:5000'
                            yag.useralias = 'testbyNamhvam'
                            yag.send(to=recipients,subject=subject,contents=[body])
                            print ('ส่ง Email สำเร็จ')
                        except IndexError:
                            pass
                    if name2 != "none":
                        cur.execute("UPDATE employeeInfo SET sub_team=%s WHERE employee_id=%s",(createTeam, name2))
                        try:
                            cur.execute("SELECT employee_name, employee_lastname, employee_email FROM employeeInfo WHERE employee_id=%s",[name2])
                            employee_data = cur.fetchall()
                            employee_name = employee_data[0][0]
                            employee_lastname = employee_data[0][1]
                            employee_email = employee_data[0][2]

                            current_time = datetime.datetime.now()
                            TimeStamp = current_time.strftime("%Y-%m-%d")

                            recipients = [employee_email]
                            subject = 'ระบบมีรายการสร้างทีมย่อยใหม่'
                            body = f'เรียน {employee_name} {employee_lastname},\n\nอีเมล์นี้เป็นอีเมล์อัตโนมัติทีส่งจากระบบ SCG-Schedule\n\nด้วยความเคารพ,\nระบบมีรายการสร้างทีมย่อยใหม่ของท่านให้อยู่ในทีม {createTeam} เรียบร้อยแล้ว (เมื่อวันที่ {TimeStamp} ท่านสามารถตรวจสอบผ่านลิงก์ด้านล่าง http://127.0.0.1:5000'
                            yag.useralias = 'testbyNamhvam'
                            yag.send(to=recipients,subject=subject,contents=[body])
                            print ('ส่ง Email สำเร็จ')
                        except IndexError:
                            pass
                    if name3 != "none":
                        cur.execute("UPDATE employeeInfo SET sub_team=%s WHERE employee_id=%s",(createTeam, name3))
                        try:
                            cur.execute("SELECT employee_name, employee_lastname, employee_email FROM employeeInfo WHERE employee_id=%s",[name3])
                            employee_data = cur.fetchall()
                            employee_name = employee_data[0][0]
                            employee_lastname = employee_data[0][1]
                            employee_email = employee_data[0][2]

                            current_time = datetime.datetime.now()
                            TimeStamp = current_time.strftime("%Y-%m-%d")

                            recipients = [employee_email]
                            subject = 'ระบบมีรายการสร้างทีมย่อยใหม่'
                            body = f'เรียน {employee_name} {employee_lastname},\n\nอีเมล์นี้เป็นอีเมล์อัตโนมัติทีส่งจากระบบ SCG-Schedule\n\nด้วยความเคารพ,\nระบบมีรายการสร้างทีมย่อยใหม่ของท่านให้อยู่ในทีม {createTeam} เรียบร้อยแล้ว (เมื่อวันที่ {TimeStamp} ท่านสามารถตรวจสอบผ่านลิงก์ด้านล่าง http://127.0.0.1:5000'
                            yag.useralias = 'testbyNamhvam'
                            yag.send(to=recipients,subject=subject,contents=[body])
                            print ('ส่ง Email สำเร็จ')
                        except IndexError:
                            pass
                    if name4 != "none":
                        cur.execute("UPDATE employeeInfo SET sub_team=%s WHERE employee_id=%s",(createTeam, name4))
                        try:
                            cur.execute("SELECT employee_name, employee_lastname, employee_email FROM employeeInfo WHERE employee_id=%s",[name4])
                            employee_data = cur.fetchall()
                            employee_name = employee_data[0][0]
                            employee_lastname = employee_data[0][1]
                            employee_email = employee_data[0][2]

                            current_time = datetime.datetime.now()
                            TimeStamp = current_time.strftime("%Y-%m-%d")

                            recipients = [employee_email]
                            subject = 'ระบบมีรายการสร้างทีมย่อยใหม่'
                            body = f'เรียน {employee_name} {employee_lastname},\n\nอีเมล์นี้เป็นอีเมล์อัตโนมัติทีส่งจากระบบ SCG-Schedule\n\nด้วยความเคารพ,\nระบบมีรายการสร้างทีมย่อยใหม่ของท่านให้อยู่ในทีม {createTeam} เรียบร้อยแล้ว (เมื่อวันที่ {TimeStamp} ท่านสามารถตรวจสอบผ่านลิงก์ด้านล่าง http://127.0.0.1:5000'
                            yag.useralias = 'testbyNamhvam'
                            yag.send(to=recipients,subject=subject,contents=[body])
                            print ('ส่ง Email สำเร็จ')
                        except IndexError:
                            pass
                    if name5 != "none":
                        cur.execute("UPDATE employeeInfo SET sub_team=%s WHERE employee_id=%s",(createTeam, name5))
                        try:
                            cur.execute("SELECT employee_name, employee_lastname, employee_email FROM employeeInfo WHERE employee_id=%s",[name5])
                            employee_data = cur.fetchall()
                            employee_name = employee_data[0][0]
                            employee_lastname = employee_data[0][1]
                            employee_email = employee_data[0][2]

                            current_time = datetime.datetime.now()
                            TimeStamp = current_time.strftime("%Y-%m-%d")

                            recipients = [employee_email]
                            subject = 'ระบบมีรายการสร้างทีมย่อยใหม่'
                            body = f'เรียน {employee_name} {employee_lastname},\n\nอีเมล์นี้เป็นอีเมล์อัตโนมัติทีส่งจากระบบ SCG-Schedule\n\nด้วยความเคารพ,\nระบบมีรายการสร้างทีมย่อยใหม่ของท่านให้อยู่ในทีม {createTeam} เรียบร้อยแล้ว (เมื่อวันที่ {TimeStamp} ท่านสามารถตรวจสอบผ่านลิงก์ด้านล่าง http://127.0.0.1:5000'
                            yag.useralias = 'testbyNamhvam'
                            yag.send(to=recipients,subject=subject,contents=[body])
                            print ('ส่ง Email สำเร็จ')
                        except IndexError:
                            pass
                
                db.connection.commit()
                cur.close()
                return redirect(url_for('employee.addEmployee'))

            elif request.form['choose'] == "update":
                employeeToDelete = request.form['employeeToDelete']

                cur = db.connection.cursor()
                cur.execute("UPDATE employeeInfo SET sub_team=%s WHERE employee_id=%s",(" ", employeeToDelete))
                db.connection.commit()
                cur.close()
                return redirect(url_for('employee.addEmployee'))

            elif request.form['choose'] == "delete":
                sub_team = request.form['sub_team']

                cur = db.connection.cursor()
                cur.execute("UPDATE employeeInfo SET sub_team=%s WHERE sub_team=%s",(" ", sub_team))
                db.connection.commit()
                cur.close()
                return redirect(url_for('employee.addEmployee'))

        elif request.form['select'] == "section":
            if request.form['choose'] == "add":
                employee_id = request.form['name-section']
                employee_name = employee_id.split()[1]
                employee_lastname = employee_id.split()[2]
                employee_id = employee_id.split()[0]
                date_start = request.form['date_start']
                date_end = request.form['date_end']

                cur = db.connection.cursor()
                cur.execute("SELECT employee_section FROM employeeInfo WHERE employee_id=%s",[employee_id])
                Oldsection = cur.fetchall()
                Oldsection = Oldsection[0][0]
                NewApprover = request.form['NewApprover']
                NewApprover = NewApprover.split()[0]
                cur.execute("SELECT approver_section FROM approverInfo WHERE approver_id=%s",[NewApprover])
                Newsection = cur.fetchall()
                Newsection = Newsection[0][0]
                cur.execute("SELECT director_id FROM approverInfo WHERE approver_id=%s",[NewApprover])
                NewDirector = cur.fetchall()
                NewDirector = NewDirector[0][0]
                cur.close()

                current_time = datetime.datetime.now()
                TimeStamp = current_time.strftime("%Y-%m-%d %H:%M:%S")
                
                status = "unsuccessful"
                
                cur = db.connection.cursor()
                cur.execute("INSERT INTO transactionaddemployee (requestId, employee_id, employee_name, employee_lastname, date_start, date_end, Oldsection, Newsection, TimeStamp, status, approver_id, director_id) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(requestId, employee_id, employee_name, employee_lastname, date_start, date_end, Oldsection, Newsection, TimeStamp, status, NewApprover, NewDirector))
                db.connection.commit()
                cur.close()
                return redirect(url_for('employee.addEmployee'))

            elif request.form['choose'] == "update":
                transactionaddemployee_id = request.form['transactionaddemployee_id']
                employee_id = request.form['name-section']
                employee_name = employee_id.split()[1]
                employee_lastname = employee_id.split()[2]
                employee_id = employee_id.split()[0]
                date_start = request.form['date_start']
                date_end = request.form['date_end']

                cur = db.connection.cursor()
                cur.execute("SELECT employee_section FROM employeeInfo WHERE employee_id=%s",[employee_id])
                Oldsection = cur.fetchall()
                Oldsection = Oldsection[0][0]
                NewApprover = request.form['NewApprover']
                NewApprover = NewApprover.split()[0]
                cur.execute("SELECT approver_section FROM approverInfo WHERE approver_id=%s",[NewApprover])
                Newsection = cur.fetchall()
                Newsection = Newsection[0][0]
                cur.execute("SELECT director_id FROM approverInfo WHERE approver_id=%s",[NewApprover])
                NewDirector = cur.fetchall()
                NewDirector = NewDirector[0][0]
                cur.close()

                current_time = datetime.datetime.now()
                TimeStamp = current_time.strftime("%Y-%m-%d %H:%M:%S")
                
                status = "unsuccessful"

                cur = db.connection.cursor()
                cur.execute("UPDATE transactionaddemployee SET requestId=%s, employee_id=%s, employee_name=%s, employee_lastname=%s, date_start=%s, date_end=%s, Oldsection=%s, Newsection=%s, TimeStamp=%s, status=%s, approver_id=%s, director_id=%s WHERE transactionaddemployee_id=%s",(requestId, employee_id, employee_name, employee_lastname, date_start, date_end, Oldsection, Newsection, TimeStamp, status, NewApprover, NewDirector, transactionaddemployee_id))
                db.connection.commit()
                cur.close()
                return redirect(url_for('employee.addEmployee'))

            elif request.form['choose'] == "delete":
                transactionaddemployee_id = request.form['transactionaddemployee_id']

                cur = db.connection.cursor()
                cur.execute("DELETE FROM transactionaddemployee WHERE transactionaddemployee_id=%s",[transactionaddemployee_id])
                db.connection.commit()
                cur.close()
                return redirect(url_for('employee.addEmployee'))

    else:
        cur = db.connection.cursor()
        transactionaddemployee_element = cur.execute(" SELECT * FROM transactionaddemployee INNER JOIN approverInfo on transactionaddemployee.approver_id = approverInfo.approver_id  WHERE requestId=%s AND status=%s", (employee_id, "unsuccessful"))
        transactionaddemployee = cur.fetchall()
        cur.execute("SELECT * FROM employeeInfo")
        allEmployee = cur.fetchall()
        cur.execute("SELECT * FROM approverInfo")
        allApprover = cur.fetchall()
        cur.execute("SELECT employee_section FROM employeeInfo WHERE employee_id=%s", [employee_id])
        user_section = cur.fetchall()
        user_section = user_section[0][0]
        cur.execute("SELECT employee_id , employee_name , employee_lastname from employeeInfo WHERE employee_section=%s",[user_section])
        employeeInsection = cur.fetchall()
        teamInSection_element = cur.execute("SELECT sub_team, COUNT(employee_id) as num FROM employeeInfo WHERE employee_section=%s AND sub_team!=%s GROUP BY sub_team",(user_section, " "))
        teamInSection = cur.fetchall()
        employeeInTeam_element = cur.execute("SELECT sub_team , employee_id, employee_name, employee_lastname  FROM employeeInfo WHERE employee_section=%s",[user_section])
        employeeInTeam = cur.fetchall()
        cur.close()

        return render_template('employee/addEmployee.html', first_name=session.get("first_name"), last_name=session.get("last_name"),
                        transactionaddemployee_element=transactionaddemployee_element, transactionaddemployee=transactionaddemployee,
                        allEmployee=allEmployee, allApprover=allApprover, employeeInsection=employeeInsection,
                        teamInSection_element=teamInSection_element, teamInSection=teamInSection, employeeInTeam_element=employeeInTeam_element,
                        employeeInTeam=employeeInTeam)

####################################################################################################

# Employee add edit shift themself transaction
@employee.route('/employee/edit/shift/self/selflist', methods=['POST','GET'])
def editYourselfList():
    line_id = session.get("line_id") # in case for query
    employee_id = session.get("employee_id")
    requestId = employee_id
        
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

            cur.execute("INSERT INTO transactionChangeShift (requestId, employee_id , date , OldShift , NewShift , TimeStamp ,  reason , status , approver_id ) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)",(requestId, employee_id , date , OldShift , NewShift , TimeStamp ,  reason , status , approver_id))
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
            cur.execute("UPDATE transactionChangeShift SET requestId=%s, date=%s , OldShift=%s , NewShift=%s , reason=%s , TimeStamp=%s WHERE transactionChangeShift_id=%s",(requestId, date , OldShift , NewShift , reason, TimeStamp, transactionChangeShift_id))
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
        transactionChangeShift_element = cur.execute(" SELECT * FROM transactionChangeShift WHERE requestId=%s AND status=%s", (employee_id, "unsuccessful"))
        transactionChangeShift = cur.fetchall()
        query = "SELECT * FROM employeeShift WHERE employeeShift_id = " + "'" + employee_id + "'"
        cur.execute(query)
        shifts = cur.fetchall()
        cur.close()

        return render_template('employee/selfEditList.html', first_name=session.get("first_name"), last_name=session.get("last_name"),
                        transactionChangeShift_element=transactionChangeShift_element, transactionChangeShift=transactionChangeShift, shifts=shifts)


# Employee see edit shift themself summary transaction
@employee.route('/employee/edit/shift/self/selflist/selflistsummary', methods=['POST','GET'])
def employeeSelfTransaction():
    line_id = session.get("line_id") # in case for query
    employee_id = session.get("employee_id")
        
    if line_id is None or session.get("first_name") == "userNotFound":
        return render_template('employee/warning.html')

    elif request.method == 'POST':
        if request.form['choose'] == "cancel":
            cur = db.connection.cursor()
            cur.execute("DELETE FROM transactionChangeShift WHERE requestId=%s AND status=%s", [employee_id, "unsuccessful"])
            db.connection.commit()
            cur.close()
            return redirect(url_for('employee.editYourselfList'))

        elif request.form['choose'] == "confirm":
            current_time = datetime.datetime.now()
            TimeStamp = current_time.strftime("%Y-%m-%d %H:%M:%S")

            cur = db.connection.cursor()
            cur.execute("UPDATE transactionChangeShift SET status=%s, TimeStamp=%s  WHERE  requestId=%s AND status=%s", ("waiting", TimeStamp, employee_id, "unsuccessful"))
            db.connection.commit()
            cur.close()
            return redirect(url_for('employee.employeeSelfTransactionEnd'))

    else:
        cur = db.connection.cursor()
        transactionChangeShift_element = cur.execute(" SELECT * FROM transactionChangeShift WHERE requestId=%s AND status=%s", (employee_id, "unsuccessful"))
        transactionChangeShift = cur.fetchall()
        query = "SELECT * FROM employeeShift WHERE employeeShift_id = " + "'" + employee_id + "'"
        cur.execute(query)
        shifts = cur.fetchall()
        cur.close()

        return render_template('employee/selfEditListSummary.html', first_name=session.get("first_name"), last_name=session.get("last_name"),
                        transactionChangeShift_element=transactionChangeShift_element, transactionChangeShift=transactionChangeShift, shifts=shifts)


# Employee add change cowork shift transaction
@employee.route('/employee/edit/shift/cowork/coworksummary', methods=['POST','GET'])
def employeeCoworkTransaction():
    line_id = session.get("line_id") # in case for query
    employee_id = session.get("employee_id")
    requestId = employee_id

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

        cur = db.connection.cursor()
        email_list = []
        cur.execute("SELECT employee_email FROM employeeInfo WHERE employee_id=%s",[name2])
        email_query = cur.fetchall()
        email_query = email_query[0][0]
        email_list.append(email_query)
        cur.close()

        session['email_list'] = email_list
        
        if request.method == 'POST':
            if request.form['choose'] == "cancel":
                return redirect(url_for('employee.editCowork'))

            elif request.form['choose'] == "confirm":
                current_time = datetime.datetime.now()
                TimeStamp = current_time.strftime("%Y-%m-%d %H:%M:%S")

                cur = db.connection.cursor()
                cur.execute("INSERT INTO transactionCoworkShift (requestId, employee_id , date , OldShift , NewShift , TimeStamp ,  reason , status , approver_id, employee_id2, employee_name2, employee_lastname2, OldShift2, NewShift2 ) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(requestId, name1 , date1 , OldShift1 , NewShift1 , TimeStamp ,  reason , status , approver_id, name2, employee_name2, employee_lastname2, OldShift2, NewShift2))
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
        
        cur = db.connection.cursor()
        email_list = []
        cur.execute("SELECT employee_email FROM employeeInfo WHERE employee_id=%s",[name2])
        email_query = cur.fetchall()
        email_query = email_query[0][0]
        email_list.append(email_query)
        cur.execute("SELECT employee_email FROM employeeInfo WHERE employee_id=%s",[name3])
        email_query = cur.fetchall()
        email_query = email_query[0][0]
        email_list.append(email_query)
        cur.close()
        
        session['email_list'] = email_list

        if request.method == 'POST':
            if request.form['choose'] == "cancel":
                return redirect(url_for('employee.editCowork'))

            elif request.form['choose'] == "confirm":
                current_time = datetime.datetime.now()
                TimeStamp = current_time.strftime("%Y-%m-%d %H:%M:%S")

                cur = db.connection.cursor()
                cur.execute("INSERT INTO transactionCoworkShift (requestId, employee_id , date , OldShift , NewShift , TimeStamp ,  reason , status , approver_id, employee_id2, employee_name2, employee_lastname2, OldShift2, NewShift2, employee_id3, employee_name3, employee_lastname3, OldShift3, NewShift3 ) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(requestId, employee_id , date1 , OldShift1 , NewShift1 , TimeStamp ,  reason , status , approver_id, name2, employee_name2, employee_lastname2, OldShift2, NewShift2, name3, employee_name3, employee_lastname3, OldShift3, NewShift3))
                db.connection.commit()
                cur.close()
                return redirect(url_for('employee.employeeCoworkTransactionEnd'))

        return render_template('employee/coworkEditListSummary.html', first_name=session.get("first_name"), last_name=session.get("last_name"),
                    date1=date1,employee_name1=employee_name1,employee_lastname1=employee_lastname1,OldShift1=OldShift1,NewShift1=NewShift1,
                    employee_name2=employee_name2,employee_lastname2=employee_lastname2,OldShift2=OldShift2,NewShift2=NewShift2,employee_name3=employee_name3,
                    employee_lastname3=employee_lastname3,OldShift3=OldShift3,NewShift3=NewShift3,reason=reason)
        

    else:
        return render_template('employee/coworkEditListSummary.html', first_name=session.get("first_name"), last_name=session.get("last_name"))


# Employee see add shift in same day summary transaction
@employee.route('/employee/edit/shift/addshift/addshiftsummary', methods=['POST','GET'])
def employeeAddShiftTransaction():
    line_id = session.get("line_id") # in case for query
    employee_id = session.get("employee_id")
        
    if line_id is None or session.get("first_name") == "userNotFound":
        return render_template('employee/warning.html')

    elif request.method == 'POST':
        if request.form['choose'] == "cancel":
            cur = db.connection.cursor()
            cur.execute("DELETE FROM transactionaddShift WHERE requestId=%s AND status=%s", [employee_id, "unsuccessful"])
            db.connection.commit()
            cur.close()
            return redirect(url_for('employee.editAddShift'))

        elif request.form['choose'] == "confirm":
            current_time = datetime.datetime.now()
            TimeStamp = current_time.strftime("%Y-%m-%d %H:%M:%S")

            cur = db.connection.cursor()
            cur.execute("UPDATE transactionaddShift SET status=%s, TimeStamp=%s  WHERE  requestId=%s AND status=%s", ("waiting", TimeStamp, employee_id, "unsuccessful"))
            db.connection.commit()
            cur.close()
            return redirect(url_for('employee.employeeAddShiftTransactionEnd'))

    else:
        cur = db.connection.cursor()
        transactionaddShift_element = cur.execute(" SELECT * FROM transactionaddShift WHERE requestId=%s AND status=%s", (employee_id, "unsuccessful"))
        transactionaddShift = cur.fetchall()
        query = "SELECT * FROM employeeShift WHERE employeeShift_id = " + "'" + employee_id + "'"
        cur.execute(query)
        shifts = cur.fetchall()
        cur.close()

        return render_template('employee/addShiftEditListSummary.html', first_name=session.get("first_name"), last_name=session.get("last_name"),
                        transactionaddShift_element=transactionaddShift_element, transactionaddShift=transactionaddShift, shifts=shifts)


# Employee see add shift and off work summary transaction
@employee.route('/employee/edit/shiftandoff/shiftandoffsummary', methods=['POST','GET'])
def employeeShiftAndOffTransaction():
    line_id = session.get("line_id") # in case for query
    employee_id = session.get("employee_id")
        
    if line_id is None or session.get("first_name") == "userNotFound":
        return render_template('employee/warning.html')

    elif request.method == 'POST':
        if request.form['choose'] == "cancel":
            cur = db.connection.cursor()
            cur.execute("DELETE FROM transactionChangeWork WHERE requestId=%s AND status=%s", [employee_id, "unsuccessful"])
            db.connection.commit()
            cur.close()
            return redirect(url_for('employee.chooseEditShiftAndOff'))

        elif request.form['choose'] == "confirm":
            current_time = datetime.datetime.now()
            TimeStamp = current_time.strftime("%Y-%m-%d %H:%M:%S")

            cur = db.connection.cursor()
            cur.execute("UPDATE transactionChangeWork SET status=%s, TimeStamp=%s  WHERE  requestId=%s AND status=%s", ("waiting", TimeStamp, employee_id, "unsuccessful"))
            db.connection.commit()
            cur.close()
            return redirect(url_for('employee.employeeShiftAndOffTransactionEnd'))

    else:
        cur = db.connection.cursor()
        transactionChangeWork_element = cur.execute(" SELECT * FROM transactionChangeWork WHERE requestId=%s AND status=%s", (employee_id, "unsuccessful"))
        transactionChangeWork = cur.fetchall()
        
        email_count = cur.execute("SELECT DISTINCT employee_email FROM `transactionChangeWork` INNER JOIN employeeInfo on transactionChangeWork.employee_id = employeeInfo.employee_id WHERE transactionChangeWork.requestId=%s and transactionChangeWork.employee_id!=%s and status=%s",(employee_id, employee_id, 'unsuccessful'))
        email_query = cur.fetchall()
        cur.close()
        
        email_list = []
        for i in range(email_count):
            email_list.append(email_query[i][0])
        
        session['email_list'] = email_list

        return render_template('employee/shiftAndOffEditListSummary.html', first_name=session.get("first_name"), last_name=session.get("last_name"),
                        transactionChangeWork_element=transactionChangeWork_element, transactionChangeWork=transactionChangeWork)


# Employee see employee in new section summary transaction
@employee.route('/employee/edit/addemployee/addemployeesummary', methods=['POST','GET'])
def employeeAddTransaction():
    line_id = session.get("line_id") # in case for query
    employee_id = session.get("employee_id")
        
    if line_id is None or session.get("first_name") == "userNotFound":
        return render_template('employee/warning.html')

    elif request.method == 'POST':
        if request.form['choose'] == "cancel":
            cur = db.connection.cursor()
            cur.execute("DELETE FROM transactionaddemployee WHERE requestId=%s AND status=%s", [employee_id, "unsuccessful"])
            db.connection.commit()
            cur.close()
            return redirect(url_for('employee.addEmployee'))

        elif request.form['choose'] == "confirm":
            current_time = datetime.datetime.now()
            TimeStamp = current_time.strftime("%Y-%m-%d %H:%M:%S")

            cur = db.connection.cursor()
            cur.execute("UPDATE transactionaddemployee SET status=%s, TimeStamp=%s  WHERE  requestId=%s AND status=%s", ("waiting", TimeStamp, employee_id, "unsuccessful"))
            db.connection.commit()
            cur.close()
            return redirect(url_for('employee.employeeAddEmployeeTransactionEnd'))

    else:
        cur = db.connection.cursor()
        transactionaddemployee_element = cur.execute(" SELECT * FROM transactionaddemployee INNER JOIN approverInfo on transactionaddemployee.approver_id = approverInfo.approver_id  WHERE requestId=%s AND status=%s", (employee_id, "unsuccessful"))
        transactionaddemployee = cur.fetchall()
        
        email_count = cur.execute("SELECT DISTINCT employee_email FROM `transactionaddemployee` INNER JOIN employeeInfo on transactionaddemployee.employee_id = employeeInfo.employee_id WHERE transactionaddemployee.requestId=%s and transactionaddemployee.employee_id!=%s and status=%s",(employee_id, employee_id, 'unsuccessful'))
        email_query = cur.fetchall()

        approver_email_count = cur.execute("SELECT DISTINCT approver_email FROM `transactionaddemployee` INNER JOIN approverInfo on transactionaddemployee.approver_id = approverInfo.approver_id WHERE transactionaddemployee.requestId=%s and status=%s",(employee_id, "unsuccessful"))
        approver_email_query = cur.fetchall()
        cur.close()
        
        email_list = []
        for i in range(email_count):
            email_list.append(email_query[i][0])
        
        session['email_list'] = email_list

        approver_email_list = []
        for i in range(approver_email_count):
            approver_email_list.append(approver_email_query[i][0])

        session['approver_email_list'] = approver_email_list

        return render_template('employee/addEmployeeEditListSummary.html', first_name=session.get("first_name"), last_name=session.get("last_name"),
                        transactionaddemployee_element=transactionaddemployee_element, transactionaddemployee=transactionaddemployee)

####################################################################################################

# Employee edit shift themself transaction ended
@employee.route('/employee/edit/shift/self/selflist/selflistsummary/selftransactionend', methods=['POST','GET'])
def employeeSelfTransactionEnd():
    line_id = session.get("line_id") # in case for query
    employee_id = session.get("employee_id")
        
    if line_id is None or session.get("first_name") == "userNotFound":
        return render_template('employee/warning.html')
    else:
        cur = db.connection.cursor()
        cur.execute("SELECT approver_name,approver_lastname,approver_email FROM `approverInfo` INNER JOIN employeeInfo ON approverInfo.approver_id = employeeInfo.approver_id WHERE employeeInfo.employee_id=%s",[employee_id])
        approver_data = cur.fetchall()
        approver_name = approver_data[0][0]
        approver_lastname = approver_data[0][1]
        approver_email = approver_data[0][2]

        cur.execute("SELECT employee_name, employee_lastname FROM employeeInfo WHERE employee_id=%s",[employee_id])
        employee_data = cur.fetchall()
        employee_name = employee_data[0][0]
        employee_lastname = employee_data[0][1]
        cur.close()

        current_time = datetime.datetime.now()
        TimeStamp = current_time.strftime("%Y-%m-%d")

        recipients = [approver_email]
        subject = 'ระบบมีการรออนุมัติรายการเปลี่ยนกะตนเองจากพนักงาน'
        body = f'เรียน {approver_name} {approver_lastname},\n\nอีเมล์นี้เป็นอีเมล์อัตโนมัติทีส่งจากระบบ SCG-Schedule\n\nด้วยความเคารพ,\nโปรดตรวจสอบรายการขออนุมัติเปลี่ยนกะตนเอง (จากคุณ {employee_name} {employee_lastname} เมื่อวันที่ {TimeStamp} กรุณาพิจารณารายการผ่านทางลิงก์ด้านล่าง http://127.0.0.1:5000/manager'
        yag.useralias = 'testbyNamhvam'
        yag.send(to=recipients,subject=subject,contents=[body])
        print ('ส่ง Email สำเร็จ')

        return render_template('employee/selfTransactionEnd.html', first_name=session.get("first_name"), last_name=session.get("last_name"))


# Employee edit cowork shift transaction ended
@employee.route('/employee/edit/shift/cowork/coworksummary/coworktransactionend', methods=['POST','GET'])
def employeeCoworkTransactionEnd():
    line_id = session.get("line_id") # in case for query
    employee_id = session.get("employee_id")
    email_list = session.get("email_list")
        
    if line_id is None or session.get("first_name") == "userNotFound":
        return render_template('employee/warning.html')
    else:
        cur = db.connection.cursor()

        cur.execute("SELECT employee_name, employee_lastname FROM employeeInfo WHERE employee_id=%s",[employee_id])
        request_data = cur.fetchall()
        request_name = request_data[0][0]
        request_lastname = request_data[0][1]

        for email in email_list:
            cur.execute("SELECT employee_name, employee_lastname FROM employeeInfo WHERE employee_email=%s",[email])
            employee_data = cur.fetchall()
            employee_name = employee_data[0][0]
            employee_lastname = employee_data[0][1]

            current_time = datetime.datetime.now()
            TimeStamp = current_time.strftime("%Y-%m-%d")

            recipients = [email]
            subject = 'ระบบมีการรออนุมัติรายการสลับกะกับเพื่อนจากเพื่อนร่วมงาน'
            body = f'เรียน {employee_name} {employee_lastname},\n\nอีเมล์นี้เป็นอีเมล์อัตโนมัติทีส่งจากระบบ SCG-Schedule\n\nด้วยความเคารพ,\nระบบมีรายการสลับกะกับเพื่อนซึ่งเกี่ยวข้องกับท่าน \nโปรดสอบถามเพื่อนร่วมงานหากเกิดข้อสงสัย (จากคุณ {request_name} {request_lastname} เมื่อวันที่ {TimeStamp} กรุณาพิจารณารายการผ่านทางลิงก์ด้านล่าง http://127.0.0.1:5000'
            yag.useralias = 'testbyNamhvam'
            yag.send(to=recipients,subject=subject,contents=[body])
            print ('ส่ง Email สำเร็จ')

        cur.execute("SELECT approver_name,approver_lastname,approver_email FROM `approverInfo` INNER JOIN employeeInfo ON approverInfo.approver_id = employeeInfo.approver_id WHERE employeeInfo.employee_id=%s",[employee_id])
        approver_data = cur.fetchall()
        approver_name = approver_data[0][0]
        approver_lastname = approver_data[0][1]
        approver_email = approver_data[0][2]

        cur.execute("SELECT employee_name, employee_lastname FROM employeeInfo WHERE employee_id=%s",[employee_id])
        employee_data = cur.fetchall()
        employee_name = employee_data[0][0]
        employee_lastname = employee_data[0][1]
        cur.close()

        current_time = datetime.datetime.now()
        TimeStamp = current_time.strftime("%Y-%m-%d")

        recipients = [approver_email]
        subject = 'ระบบมีการรออนุมัติรายการสลับกะกับเพื่อนจากพนักงาน'
        body = f'เรียน {approver_name} {approver_lastname},\n\nอีเมล์นี้เป็นอีเมล์อัตโนมัติทีส่งจากระบบ SCG-Schedule\n\nด้วยความเคารพ,\nโปรดตรวจสอบรายการขออนุมัติสลับกะกับเพื่อน (จากคุณ {employee_name} {employee_lastname} เมื่อวันที่ {TimeStamp} กรุณาพิจารณารายการผ่านทางลิงก์ด้านล่าง http://127.0.0.1:5000/manager'
        yag.useralias = 'testbyNamhvam'
        yag.send(to=recipients,subject=subject,contents=[body])
        print ('ส่ง Email สำเร็จ')

        return render_template('employee/coworkTransactionEnd.html', first_name=session.get("first_name"), last_name=session.get("last_name"))


# Employee add shift in the same day transaction ended
@employee.route('/employee/edit/shift/addshift/addshiftsummary/addshifttransactionend', methods=['POST','GET'])
def employeeAddShiftTransactionEnd():
    line_id = session.get("line_id") # in case for query
    employee_id = session.get("employee_id")
        
    if line_id is None or session.get("first_name") == "userNotFound":
        return render_template('employee/warning.html')
    else:
        cur = db.connection.cursor()
        cur.execute("SELECT approver_name,approver_lastname,approver_email FROM `approverInfo` INNER JOIN employeeInfo ON approverInfo.approver_id = employeeInfo.approver_id WHERE employeeInfo.employee_id=%s",[employee_id])
        approver_data = cur.fetchall()
        approver_name = approver_data[0][0]
        approver_lastname = approver_data[0][1]
        approver_email = approver_data[0][2]

        cur.execute("SELECT employee_name, employee_lastname FROM employeeInfo WHERE employee_id=%s",[employee_id])
        employee_data = cur.fetchall()
        employee_name = employee_data[0][0]
        employee_lastname = employee_data[0][1]
        cur.close()

        current_time = datetime.datetime.now()
        TimeStamp = current_time.strftime("%Y-%m-%d")

        recipients = [approver_email]
        subject = 'ระบบมีการรออนุมัติรายการเพิ่มกะในวันเดียวกันจากพนักงาน'
        body = f'เรียน {approver_name} {approver_lastname},\n\nอีเมล์นี้เป็นอีเมล์อัตโนมัติทีส่งจากระบบ SCG-Schedule\n\nด้วยความเคารพ,\nโปรดตรวจสอบรายการเพิ่มกะในวันเดียวกัน (จากคุณ {employee_name} {employee_lastname} เมื่อวันที่ {TimeStamp} กรุณาพิจารณารายการผ่านทางลิงก์ด้านล่าง http://127.0.0.1:5000/manager'
        yag.useralias = 'testbyNamhvam'
        yag.send(to=recipients,subject=subject,contents=[body])
        print ('ส่ง Email สำเร็จ')

        return render_template('employee/addShiftTransactionEnd.html', first_name=session.get("first_name"), last_name=session.get("last_name"))


# Employee edit shift and off work transaction ended
@employee.route('/employee/edit/shiftandoff/shiftandoffsummary/shiftandofftransactionend', methods=['POST','GET'])
def employeeShiftAndOffTransactionEnd():
    line_id = session.get("line_id") # in case for query
    employee_id = session.get("employee_id")
    email_list = session.get("email_list")
        
    if line_id is None or session.get("first_name") == "userNotFound":
        return render_template('employee/warning.html')
    else:
        cur = db.connection.cursor()

        cur.execute("SELECT employee_name, employee_lastname FROM employeeInfo WHERE employee_id=%s",[employee_id])
        request_data = cur.fetchall()
        request_name = request_data[0][0]
        request_lastname = request_data[0][1]

        for email in email_list:
            cur.execute("SELECT employee_name, employee_lastname FROM employeeInfo WHERE employee_email=%s",[email])
            employee_data = cur.fetchall()
            employee_name = employee_data[0][0]
            employee_lastname = employee_data[0][1]

            current_time = datetime.datetime.now()
            TimeStamp = current_time.strftime("%Y-%m-%d")

            recipients = [email]
            subject = 'ระบบมีการรออนุมัติรายการเปลี่ยนรูปแบบการทำงานและวันหยุดจากเพื่อนร่วมงาน'
            body = f'เรียน {employee_name} {employee_lastname},\n\nอีเมล์นี้เป็นอีเมล์อัตโนมัติทีส่งจากระบบ SCG-Schedule\n\nด้วยความเคารพ,\nระบบมีรายการเปลี่ยนรูปแบบการทำงานและวันหยุดซึ่งเกี่ยวข้องกับท่าน \nโปรดสอบถามเพื่อนร่วมงานหากเกิดข้อสงสัย (จากคุณ {request_name} {request_lastname} เมื่อวันที่ {TimeStamp} กรุณาพิจารณารายการผ่านทางลิงก์ด้านล่าง http://127.0.0.1:5000'
            yag.useralias = 'testbyNamhvam'
            yag.send(to=recipients,subject=subject,contents=[body])
            print ('ส่ง Email สำเร็จ')

        cur.execute("SELECT approver_name,approver_lastname,approver_email FROM `approverInfo` INNER JOIN employeeInfo ON approverInfo.approver_id = employeeInfo.approver_id WHERE employeeInfo.employee_id=%s",[employee_id])
        approver_data = cur.fetchall()
        approver_name = approver_data[0][0]
        approver_lastname = approver_data[0][1]
        approver_email = approver_data[0][2]

        cur.execute("SELECT employee_name, employee_lastname FROM employeeInfo WHERE employee_id=%s",[employee_id])
        employee_data = cur.fetchall()
        employee_name = employee_data[0][0]
        employee_lastname = employee_data[0][1]
        cur.close()

        current_time = datetime.datetime.now()
        TimeStamp = current_time.strftime("%Y-%m-%d")

        recipients = [approver_email]
        subject = 'ระบบมีการรออนุมัติรายการเปลี่ยนรูปแบบการทำงานและวันหยุดจากพนักงาน'
        body = f'เรียน {approver_name} {approver_lastname},\n\nอีเมล์นี้เป็นอีเมล์อัตโนมัติทีส่งจากระบบ SCG-Schedule\n\nด้วยความเคารพ,\nโปรดตรวจสอบรายการเปลี่ยนรูปแบบการทำงานและวันหยุด (จากคุณ {employee_name} {employee_lastname} เมื่อวันที่ {TimeStamp} กรุณาพิจารณารายการผ่านทางลิงก์ด้านล่าง http://127.0.0.1:5000/manager'
        yag.useralias = 'testbyNamhvam'
        yag.send(to=recipients,subject=subject,contents=[body])
        print ('ส่ง Email สำเร็จ')

        return render_template('employee/shiftAndOffTransactionEnd.html', first_name=session.get("first_name"), last_name=session.get("last_name"))


# Employee add employee in new section transaction ended
@employee.route('/employee/edit/addemployee/addemployeesummary/addemployeetransactionend', methods=['POST','GET'])
def employeeAddEmployeeTransactionEnd():
    line_id = session.get("line_id") # in case for query
    employee_id = session.get("employee_id")
    email_list = session.get("email_list")
    approver_email_list = session.get("approver_email_list")
        
    if line_id is None or session.get("first_name") == "userNotFound":
        return render_template('employee/warning.html')
    else:
        cur = db.connection.cursor()

        cur.execute("SELECT employee_name, employee_lastname FROM employeeInfo WHERE employee_id=%s",[employee_id])
        request_data = cur.fetchall()
        request_name = request_data[0][0]
        request_lastname = request_data[0][1]

        for email in email_list:
            cur.execute("SELECT employee_name, employee_lastname FROM employeeInfo WHERE employee_email=%s",[email])
            employee_data = cur.fetchall()
            employee_name = employee_data[0][0]
            employee_lastname = employee_data[0][1]

            current_time = datetime.datetime.now()
            TimeStamp = current_time.strftime("%Y-%m-%d")

            recipients = [email]
            subject = 'ระบบมีการรออนุมัติรายการเปลี่ยนหน่วยงานใหม่จากเพื่อนร่วมงาน'
            body = f'เรียน {employee_name} {employee_lastname},\n\nอีเมล์นี้เป็นอีเมล์อัตโนมัติทีส่งจากระบบ SCG-Schedule\n\nด้วยความเคารพ,\nระบบมีรายการเปลี่ยนหน่วยงานใหม่ซึ่งเกี่ยวข้องกับท่าน \nโปรดสอบถามเพื่อนร่วมงานหากเกิดข้อสงสัย (จากคุณ {request_name} {request_lastname} เมื่อวันที่ {TimeStamp} กรุณาพิจารณารายการผ่านทางลิงก์ด้านล่าง http://127.0.0.1:5000'
            yag.useralias = 'testbyNamhvam'
            yag.send(to=recipients,subject=subject,contents=[body])
            print ('ส่ง Email สำเร็จ')

        for approver_email in approver_email_list:
            cur.execute("SELECT approver_name, approver_lastname FROM approverInfo WHERE approver_email=%s",[approver_email])
            approver_data = cur.fetchall()
            approver_name = approver_data[0][0]
            approver_lastname = approver_data[0][1]

            current_time = datetime.datetime.now()
            TimeStamp = current_time.strftime("%Y-%m-%d")

            recipients = [approver_email]
            subject = 'ระบบมีการรออนุมัติรายการเปลี่ยนหน่วยงานใหม่จากพนักงาน'
            body = f'เรียน {approver_name} {approver_lastname},\n\nอีเมล์นี้เป็นอีเมล์อัตโนมัติทีส่งจากระบบ SCG-Schedule\n\nด้วยความเคารพ,\nโปรดตรวจสอบรายการเปลี่ยนหน่วยงานใหม่ (จากคุณ {request_name} {request_lastname} เมื่อวันที่ {TimeStamp} กรุณาพิจารณารายการผ่านทางลิงก์ด้านล่าง http://127.0.0.1:5000/manager'
            yag.useralias = 'testbyNamhvam'
            yag.send(to=recipients,subject=subject,contents=[body])
            print ('ส่ง Email สำเร็จ')

        cur.close()
        return render_template('employee/addEmployeeTransactionEnd.html', first_name=session.get("first_name"), last_name=session.get("last_name"))


# NOT FINISHED YET
@employee.route('/employee/generate', methods=['POST','GET'])
def generate():
    line_id = session.get("line_id") # in case for query
    employee_id = session.get("employee_id")
    LV = 3
    start = '0000-00-00'
    end = '0000-00-00'
    cur = db.connection.cursor()
    cur.execute(" SELECT * FROM shiftformat " )
    formatdata = cur.fetchall()
    cur.execute(" SELECT section_code FROM employeeInfo  WHERE employee_id=%s",[employee_id])
    section_code = cur.fetchall()
    section_code =  section_code[0][0]

    cur.execute(" SELECT LV	 FROM filtershift  WHERE section_code =%s",[section_code])
    LV = cur.fetchall()
    LV =  LV[0][0]
    #print (section_code)

    if request.method == 'POST':
        start = request.form['start']
        end = request.form['end']
 
        #วันเริ่ม - จบ
        start = pendulum.from_format(start,'YYYY-MM-DD')
        #print (start)
        end = pendulum.from_format(end,'YYYY-MM-DD')
        #print (end)
        # เก็บวันเริ่มเเละจบ
        period = pendulum.period(start,end)
        #print (period)
        for dt in period:
            date = dt.to_date_string()
            print(date)
            d = datetime.datetime.strptime(date ,'%Y-%m-%d')
            x = datetime.datetime.strftime(d,'%W') 
            intweek = int(x) 
            modweek = intweek % LV
            strmodweek = str(modweek)
            # print(strmodweek)
            day = d.strftime("%a")
            # print (day)
            for i in range(len(formatdata)): 
                if (section_code == formatdata[i][2] and day == formatdata[i][1] and modweek == formatdata[i][6] ):
                    print ( date)
                    print ( formatdata[i][3])
                    # formatdata[i][3]
                    print ('if2')
                    
                    try:
                        cur.execute("INSERT INTO employeeShift (employeeShift_id, section_code , date , day , Shift , start_time , stop_time ) VALUES (%s,%s,%s,%s,%s,%s,%s)",(employee_id,section_code,date,day,formatdata[i][3],formatdata[i][4],formatdata[i][5]))
                        db.connection.commit()
                    #ถ้า error ให้หยุดใส่ข้อมูลแล้วแสดงใน terminal ว่า ERROR
                    except (cur.Error, cur.Warning) as e:
                        print(e)
                        print("ERROR IS HERE")
                        

    cur.close()    

    cur = db.connection.cursor()
    cur.execute("SELECT * FROM employeeShift WHERE employeeShift_id=%s",[employee_id])
    argsssssss = cur.fetchall()
    cur.close()

    # ตัวคือที่จะเอาไปแสดง = ชื่อที่ใส่ให้มัน
    return render_template('employee/generatedateAuto.html' , formatdata = formatdata, argsssssss=argsssssss )    
