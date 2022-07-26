from .__init__ import manager
from ..extensions import db
from flask import render_template, redirect, url_for, request, session
import datetime;


@manager.route('/manager')
def managerLoginPage():
    line_id = request.args.get("userId")

    if line_id is None:
        session['line_id'] = None
        return render_template('manager/welcome.html')

    toString = str(line_id)
    session['line_id'] = toString # send line_id to other page
    
    cur = db.connection.cursor()
    query = "SELECT approver_name FROM approver inner join approverInfo on approver.approver_id = approverInfo.approver_id WHERE line_id = " + "'" + toString + "'"
    cur.execute(query)
    first_name = cur.fetchall()
    query = "SELECT approver_lastname FROM approver inner join approverInfo on approver.approver_id = approverInfo.approver_id WHERE line_id = " + "'" + toString + "'"
    cur.execute(query)
    last_name = cur.fetchall()
    query = "SELECT approver_id FROM approver WHERE line_id = " + "'" + toString + "'"
    cur.execute(query)
    approver_id = cur.fetchall() 
    cur.execute("SELECT approver_section FROM approverInfo WHERE approver_id=%s", [approver_id[0][0]])
    approver_section = cur.fetchall()

    cur.close()

    if bool(first_name) == False and bool(last_name) == False:
        session['first_name'] = "userNotFound" # send first_name to other page
        return render_template('manager/welcome.html')

    session['first_name'] = first_name # send first_name to other page
    session['last_name'] = last_name # send last_name to other page
    session['approver_id'] = approver_id[0][0] # send last_name to other page
    session['approver_section'] = approver_section[0][0]

    return render_template('manager/welcome.html')

@manager.route('/manager/home', methods=['POST','GET'])
def managerPage():
    line_id = session.get("line_id") # in case for query
        
    if line_id is None or session.get("first_name") == "userNotFound":
        return render_template('manager/warning.html')
    else:
        return render_template('manager/manager.html', first_name=session.get("first_name"), last_name=session.get("last_name"))
    # return render_template('manager/manager.html')

@manager.route('/manager/status/pending', methods=['POST','GET'])
def pending():
    line_id = session.get("line_id") # in case for query
    approver_id = session.get("approver_id")
        
    if line_id is None or session.get("first_name") == "userNotFound":
        return render_template('manager/warning.html')
        
    elif request.method == 'POST':
        if request.form['select'] == "addemployee":
            if request.form['choose'] == "update":
                transactionaddemployee_id = request.form['transactionaddemployee_id']
                current_time = datetime.datetime.now()
                TimeStamp = current_time.strftime("%Y-%m-%d %H:%M:%S")
                status = "approve"

                cur = db.connection.cursor()
                cur.execute("UPDATE transactionaddemployee SET status=%s, TimeStamp=%s WHERE transactionaddemployee_id=%s",(status, TimeStamp, transactionaddemployee_id))
                db.connection.commit()
                cur.close()
                return redirect(url_for('manager.pending'))

            elif request.form['choose'] == "delete":
                transactionaddemployee_id = request.form['transactionaddemployee_id']

                cur = db.connection.cursor()
                cur.execute("DELETE FROM transactionaddemployee WHERE transactionaddemployee_id=%s",[transactionaddemployee_id])
                db.connection.commit()
                cur.close()
                return redirect(url_for('manager.pending'))

        elif request.form['select'] == "addShift":
            if request.form['choose'] == "update":
                transactionaddShift_id = request.form['transactionaddShift_id']
                current_time = datetime.datetime.now()
                TimeStamp = current_time.strftime("%Y-%m-%d %H:%M:%S")
                status = "approve"

                cur = db.connection.cursor()
                cur.execute("UPDATE transactionaddShift SET status=%s, TimeStamp=%s WHERE transactionaddShift_id=%s",(status, TimeStamp, transactionaddShift_id))
                db.connection.commit()
                cur.close()
                return redirect(url_for('manager.pending'))

            elif request.form['choose'] == "delete":
                transactionaddShift_id = request.form['transactionaddShift_id']

                cur = db.connection.cursor()
                cur.execute("DELETE FROM transactionaddShift WHERE transactionaddShift_id=%s",[transactionaddShift_id])
                db.connection.commit()
                cur.close()
                return redirect(url_for('manager.pending'))

        elif request.form['select'] == "ChangeShift":
            if request.form['choose'] == "update":
                transactionChangeShift_id = request.form['transactionChangeShift_id']
                current_time = datetime.datetime.now()
                TimeStamp = current_time.strftime("%Y-%m-%d %H:%M:%S")
                status = "approve"

                cur = db.connection.cursor()
                cur.execute("UPDATE transactionChangeShift SET status=%s, TimeStamp=%s WHERE transactionChangeShift_id=%s",(status, TimeStamp, transactionChangeShift_id))
                db.connection.commit()
                cur.close()
                return redirect(url_for('manager.pending'))

            elif request.form['choose'] == "delete":
                transactionChangeShift_id = request.form['transactionChangeShift_id']

                cur = db.connection.cursor()
                cur.execute("DELETE FROM transactionChangeShift WHERE transactionChangeShift_id=%s",[transactionChangeShift_id])
                db.connection.commit()
                cur.close()
                return redirect(url_for('manager.pending'))

        elif request.form['select'] == "ChangeWork":
            if request.form['choose'] == "update":
                transactionChangeWork_id = request.form['transactionChangeWork_id']
                current_time = datetime.datetime.now()
                TimeStamp = current_time.strftime("%Y-%m-%d %H:%M:%S")
                status = "approve"

                cur = db.connection.cursor()
                cur.execute("UPDATE transactionChangeWork SET status=%s, TimeStamp=%s WHERE transactionChangeWork_id=%s",(status, TimeStamp, transactionChangeWork_id))
                db.connection.commit()
                cur.close()
                return redirect(url_for('manager.pending'))

            elif request.form['choose'] == "delete":
                transactionChangeWork_id = request.form['transactionChangeWork_id']

                cur = db.connection.cursor()
                cur.execute("DELETE FROM transactionChangeWork WHERE transactionChangeWork_id=%s",[transactionChangeWork_id])
                db.connection.commit()
                cur.close()
                return redirect(url_for('manager.pending'))

        elif request.form['select'] == "CoworkShift":
            if request.form['choose'] == "update":
                transactionCoworkShift_id = request.form['transactionCoworkShift_id']
                current_time = datetime.datetime.now()
                TimeStamp = current_time.strftime("%Y-%m-%d %H:%M:%S")
                status = "approve"

                cur = db.connection.cursor()
                cur.execute("UPDATE transactionCoworkShift SET status=%s, TimeStamp=%s WHERE transactionCoworkShift_id=%s",(status, TimeStamp, transactionCoworkShift_id))
                db.connection.commit()
                cur.close()
                return redirect(url_for('manager.pending'))

            elif request.form['choose'] == "delete":
                transactionCoworkShift_id = request.form['transactionCoworkShift_id']

                cur = db.connection.cursor()
                cur.execute("DELETE FROM transactionCoworkShift WHERE transactionCoworkShift_id=%s",[transactionCoworkShift_id])
                db.connection.commit()
                cur.close()
                return redirect(url_for('manager.pending'))

    else:
        cur = db.connection.cursor()
        transactionaddemployee_element = cur.execute("SELECT * FROM transactionaddemployee WHERE approver_id=%s AND status=%s",(approver_id, "waiting"))
        transactionaddemployee = cur.fetchall()

        transactionaddShift_element = cur.execute("SELECT * FROM transactionaddShift WHERE approver_id=%s AND status=%s",(approver_id, "waiting"))
        transactionaddShift = cur.fetchall()

        transactionChangeShift_element = cur.execute("SELECT * FROM transactionChangeShift WHERE approver_id=%s AND status=%s",(approver_id, "waiting"))
        transactionChangeShift = cur.fetchall()

        transactionChangeWork_element = cur.execute("SELECT * FROM transactionChangeWork WHERE approver_id=%s AND status=%s",(approver_id, "waiting"))
        transactionChangeWork = cur.fetchall()

        transactionCoworkShift_element = cur.execute("SELECT * FROM transactionCoworkShift WHERE approver_id=%s AND status=%s",(approver_id, "waiting"))
        transactionCoworkShift = cur.fetchall()

        return render_template('manager/pending.html', first_name=session.get("first_name"), last_name=session.get("last_name"), 
                    transactionaddemployee=transactionaddemployee,transactionaddemployee_element=transactionaddemployee_element,
                    transactionaddShift=transactionaddShift,transactionaddShift_element=transactionaddShift_element,
                    transactionChangeShift=transactionChangeShift,transactionChangeShift_element=transactionChangeShift_element,
                    transactionChangeWork=transactionChangeWork,transactionChangeWork_element=transactionChangeWork_element,
                    transactionCoworkShift=transactionCoworkShift,transactionCoworkShift_element=transactionCoworkShift_element)


@manager.route('/manager/status/approve', methods=['POST','GET'])
def approve():
    line_id = session.get("line_id") # in case for query
    approver_id = session.get("approver_id")
        
    if line_id is None or session.get("first_name") == "userNotFound":
        return render_template('manager/warning.html')
    else:
        cur = db.connection.cursor()
        transactionaddemployee_element = cur.execute("SELECT * FROM transactionaddemployee WHERE approver_id=%s AND status=%s",(approver_id, "approve"))
        transactionaddemployee = cur.fetchall()

        transactionaddShift_element = cur.execute("SELECT * FROM transactionaddShift WHERE approver_id=%s AND status=%s",(approver_id, "approve"))
        transactionaddShift = cur.fetchall()

        transactionChangeShift_element = cur.execute("SELECT * FROM transactionChangeShift WHERE approver_id=%s AND status=%s",(approver_id, "approve"))
        transactionChangeShift = cur.fetchall()

        transactionChangeWork_element = cur.execute("SELECT * FROM transactionChangeWork WHERE approver_id=%s AND status=%s",(approver_id, "approve"))
        transactionChangeWork = cur.fetchall()

        transactionCoworkShift_element = cur.execute("SELECT * FROM transactionCoworkShift WHERE approver_id=%s AND status=%s",(approver_id, "approve"))
        transactionCoworkShift = cur.fetchall()

        return render_template('manager/approve.html', first_name=session.get("first_name"), last_name=session.get("last_name"), 
                    transactionaddemployee=transactionaddemployee,transactionaddemployee_element=transactionaddemployee_element,
                    transactionaddShift=transactionaddShift,transactionaddShift_element=transactionaddShift_element,
                    transactionChangeShift=transactionChangeShift,transactionChangeShift_element=transactionChangeShift_element,
                    transactionChangeWork=transactionChangeWork,transactionChangeWork_element=transactionChangeWork_element,
                    transactionCoworkShift=transactionCoworkShift,transactionCoworkShift_element=transactionCoworkShift_element)
                    

@manager.route('/manager/shift', methods=['POST','GET'])
def chooseEditShift():
    line_id = session.get("line_id") # in case for query
        
    if line_id is None or session.get("first_name") == "userNotFound":
        return render_template('manager/warning.html')
    else:
        return render_template('manager/editShift.html', first_name=session.get("first_name"), last_name=session.get("last_name"))


####################################################################################################

@manager.route('/manager/edit', methods=['POST','GET'])
def employeeShift():
    line_id = session.get("line_id") # in case for query
    approver_section = session.get("approver_section")
        
    if line_id is None or session.get("first_name") == "userNotFound":
        return render_template('manager/warning.html')

    elif request.method == 'POST':
        session['sub_team'] = request.form['sub_team']
        return render_template('manager/managerEdit.html', first_name=session.get("first_name"), last_name=session.get("last_name"))

    else:
        cur = db.connection.cursor()
        teamInSection_element = cur.execute("SELECT sub_team, COUNT(employee_id) as num FROM employeeInfo WHERE employee_section=%s AND sub_team!=%s GROUP BY sub_team",(approver_section, " "))
        teamInSection = cur.fetchall()
    
        cur.close()
        
        return render_template('manager/selectSubteam.html', first_name=session.get("first_name"), last_name=session.get("last_name"),
                    teamInSection_element=teamInSection_element, teamInSection=teamInSection)


@manager.route('/manager/edit/selflist', methods=['POST','GET'])
def editYourselfList():
    line_id = session.get("line_id") # in case for query
    sub_team = session.get("sub_team")
    approver_id = session.get("approver_id")
    requestId = approver_id
        
    if line_id is None or session.get("first_name") == "userNotFound":
        return render_template('manager/warning.html')
    
    elif request.method == 'POST':
        if request.form['choose'] == "add":
            employee_id = request.form['name']
            date = request.form['date']
            OldShift = request.form['OldShift']
            NewShift = request.form['NewShift']
            reason = request.form['reason']
            current_time = datetime.datetime.now()
            TimeStamp = current_time.strftime("%Y-%m-%d %H:%M:%S")
            
            status = "unsuccessful"
              
            cur = db.connection.cursor()
            cur.execute("INSERT INTO transactionChangeShift (requestId, employee_id , date , OldShift , NewShift , TimeStamp ,  reason , status , approver_id ) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)",(requestId, employee_id , date , OldShift , NewShift , TimeStamp ,  reason , status , approver_id))
            db.connection.commit()
            cur.close()
            return redirect(url_for('manager.editYourselfList'))

        elif request.form['choose'] == "update":
            transactionChangeShift_id = request.form['transactionChangeShift_id']
            employee_id = request.form['name']
            date = request.form['date']
            OldShift = request.form['OldShift']
            NewShift = request.form['NewShift']
            reason = request.form['reason']
            current_time = datetime.datetime.now()
            TimeStamp = current_time.strftime("%Y-%m-%d %H:%M:%S")

            cur = db.connection.cursor()
            cur.execute("UPDATE transactionChangeShift SET requestId=%s, employee_id=%s, date=%s , OldShift=%s , NewShift=%s , reason=%s , TimeStamp=%s WHERE transactionChangeShift_id=%s",(requestId, employee_id, date , OldShift , NewShift , reason, TimeStamp, transactionChangeShift_id))
            db.connection.commit()
            cur.close()
            return redirect(url_for('manager.editYourselfList'))

        elif request.form['choose'] == "delete":
            transactionChangeShift_id = request.form['transactionChangeShift_id']

            cur = db.connection.cursor()
            cur.execute("DELETE FROM transactionChangeShift WHERE transactionChangeShift_id=%s",[transactionChangeShift_id])
            db.connection.commit()
            cur.close()
            return redirect(url_for('manager.editYourselfList'))

    else:     
        cur = db.connection.cursor()

        # count employee
        cur.execute("SELECT COUNT(employee_id) FROM employeeInfo WHERE sub_team=%s",[sub_team])
        employee_count = cur.fetchall()
        count = employee_count[0][0]

        # get all employee in same team 
        cur.execute("SELECT employee_id, employee_name, employee_lastname FROM employeeInfo WHERE sub_team=%s",[sub_team])
        idSub_teamAll = cur.fetchall()
        
        transactionChangeShift_element = cur.execute("SELECT * FROM transactionChangeShift WHERE requestId=%s AND status=%s", (approver_id, "unsuccessful"))
        transactionChangeShift = cur.fetchall()

        otherEmployee = [0]*count
        for i in range(count):
            otherEmployee[i] = idSub_teamAll[i][0]

        if count == 1:
            cur.execute("SELECT employee_id,Remark , dayoff FROM filtershift INNER JOIN employeeInfo ON filtershift.section_code = employeeInfo.section_code WHERE employee_id=%s",[otherEmployee[0]])
            workData1 = cur.fetchall()
            cur.close()
            return render_template('manager/selfEditList.html', first_name=session.get("first_name"), last_name=session.get("last_name"),
                                idSub_teamAll=idSub_teamAll, workData1=workData1,
                                transactionChangeShift_element=transactionChangeShift_element, transactionChangeShift=transactionChangeShift)
        elif count == 2:
            cur.execute("SELECT employee_id,Remark , dayoff FROM filtershift INNER JOIN employeeInfo ON filtershift.section_code = employeeInfo.section_code WHERE employee_id=%s",[otherEmployee[0]])
            workData1 = cur.fetchall()
            cur.execute("SELECT employee_id,Remark , dayoff FROM filtershift INNER JOIN employeeInfo ON filtershift.section_code = employeeInfo.section_code WHERE employee_id=%s",[otherEmployee[1]])
            workData2 = cur.fetchall()
            cur.close()
            return render_template('manager/selfEditList.html', first_name=session.get("first_name"), last_name=session.get("last_name"),
                                idSub_teamAll=idSub_teamAll, workData1=workData1, workData2=workData2, 
                                transactionChangeShift_element=transactionChangeShift_element, transactionChangeShift=transactionChangeShift)
        elif count == 3:
            cur.execute("SELECT employee_id,Remark , dayoff FROM filtershift INNER JOIN employeeInfo ON filtershift.section_code = employeeInfo.section_code WHERE employee_id=%s",[otherEmployee[0]])
            workData1 = cur.fetchall()
            cur.execute("SELECT employee_id,Remark , dayoff FROM filtershift INNER JOIN employeeInfo ON filtershift.section_code = employeeInfo.section_code WHERE employee_id=%s",[otherEmployee[1]])
            workData2 = cur.fetchall()
            cur.execute("SELECT employee_id,Remark , dayoff FROM filtershift INNER JOIN employeeInfo ON filtershift.section_code = employeeInfo.section_code WHERE employee_id=%s",[otherEmployee[2]])
            workData3 = cur.fetchall()
            cur.close()
            return render_template('manager/selfEditList.html', first_name=session.get("first_name"), last_name=session.get("last_name"),
                                idSub_teamAll=idSub_teamAll, workData1=workData1, workData2=workData2, workData3=workData3, 
                                transactionChangeShift_element=transactionChangeShift_element, transactionChangeShift=transactionChangeShift)
        elif count == 4:
            cur.execute("SELECT employee_id,Remark , dayoff FROM filtershift INNER JOIN employeeInfo ON filtershift.section_code = employeeInfo.section_code WHERE employee_id=%s",[otherEmployee[0]])
            workData1 = cur.fetchall()
            cur.execute("SELECT employee_id,Remark , dayoff FROM filtershift INNER JOIN employeeInfo ON filtershift.section_code = employeeInfo.section_code WHERE employee_id=%s",[otherEmployee[1]])
            workData2 = cur.fetchall()
            cur.execute("SELECT employee_id,Remark , dayoff FROM filtershift INNER JOIN employeeInfo ON filtershift.section_code = employeeInfo.section_code WHERE employee_id=%s",[otherEmployee[2]])
            workData3 = cur.fetchall()
            cur.execute("SELECT employee_id,Remark , dayoff FROM filtershift INNER JOIN employeeInfo ON filtershift.section_code = employeeInfo.section_code WHERE employee_id=%s",[otherEmployee[3]])
            workData4 = cur.fetchall()
            cur.close()
            return render_template('manager/selfEditList.html', first_name=session.get("first_name"), last_name=session.get("last_name"),
                                idSub_teamAll=idSub_teamAll, workData1=workData1, workData2=workData2, workData3=workData3, workData4=workData4,
                                transactionChangeShift_element=transactionChangeShift_element, transactionChangeShift=transactionChangeShift)
        elif count == 5:
            cur.execute("SELECT employee_id,Remark , dayoff FROM filtershift INNER JOIN employeeInfo ON filtershift.section_code = employeeInfo.section_code WHERE employee_id=%s",[otherEmployee[0]])
            workData1 = cur.fetchall()
            cur.execute("SELECT employee_id,Remark , dayoff FROM filtershift INNER JOIN employeeInfo ON filtershift.section_code = employeeInfo.section_code WHERE employee_id=%s",[otherEmployee[1]])
            workData2 = cur.fetchall()
            cur.execute("SELECT employee_id,Remark , dayoff FROM filtershift INNER JOIN employeeInfo ON filtershift.section_code = employeeInfo.section_code WHERE employee_id=%s",[otherEmployee[2]])
            workData3 = cur.fetchall()
            cur.execute("SELECT employee_id,Remark , dayoff FROM filtershift INNER JOIN employeeInfo ON filtershift.section_code = employeeInfo.section_code WHERE employee_id=%s",[otherEmployee[3]])
            workData4 = cur.fetchall()
            cur.execute("SELECT employee_id,Remark , dayoff FROM filtershift INNER JOIN employeeInfo ON filtershift.section_code = employeeInfo.section_code WHERE employee_id=%s",[otherEmployee[4]])
            workData5 = cur.fetchall()
            return render_template('manager/selfEditList.html', first_name=session.get("first_name"), last_name=session.get("last_name"),
                                idSub_teamAll=idSub_teamAll, workData1=workData1, workData2=workData2, workData3=workData3, workData4=workData4, workData5=workData5,
                                transactionChangeShift_element=transactionChangeShift_element, transactionChangeShift=transactionChangeShift)


@manager.route('/manager/edit/cowork', methods=['POST','GET'])
def editCowork():
    line_id = session.get("line_id") # in case for query
    sub_team = session.get("sub_team")
    approver_id = session.get("approver_id")
    
    if line_id is None or session.get("first_name") == "userNotFound":
        return render_template('manager/warning.html')
    
    elif request.method == 'POST':
        if request.form['choose'] == "สองคน":
            cur = db.connection.cursor()

            # count employee
            cur.execute("SELECT COUNT(employee_id) FROM employeeInfo WHERE sub_team=%s",[sub_team])
            employee_count = cur.fetchall()
            count = employee_count[0][0]

            # get employee in same team
            cur.execute("SELECT employee_id, employee_name, employee_lastname FROM employeeInfo WHERE sub_team=%s",[sub_team])
            idSub_team = cur.fetchall()
            
            employee_id1 = request.form['name2-1']

            for i in range(count):
                if idSub_team[i][0] == employee_id1:
                    employee_name1 = idSub_team[i][1] 
                    employee_lastname1 = idSub_team[i][2]
                    break

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

            session['date2-1'] = date

            session['name2-1'] = employee_id1
            session['employee_name1'] = employee_name1
            session['employee_lastname1'] = employee_lastname1
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
            session['status2p'] = "approve"
            session['choose'] = "สองคน"

            cur.close()
            return redirect(url_for('manager.employeeCoworkTransaction'))

        elif request.form['choose'] == "สามคน":
            cur = db.connection.cursor()

            # count employee
            cur.execute("SELECT COUNT(employee_id) FROM employeeInfo WHERE sub_team=%s",[sub_team])
            employee_count = cur.fetchall()
            count = employee_count[0][0]

            # get employee in same team
            cur.execute("SELECT employee_id, employee_name, employee_lastname FROM employeeInfo WHERE sub_team=%s",[sub_team])
            idSub_team = cur.fetchall()

            employee_id1 = request.form['name3-1']

            for i in range(count):
                if idSub_team[i][0] == employee_id1:
                    employee_name1 = idSub_team[i][1] 
                    employee_lastname1 = idSub_team[i][2]
                    break

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

            session['date3-1'] = date

            session['name3-1'] = employee_id1
            session['employee_name1'] = employee_name1
            session['employee_lastname1'] = employee_lastname1
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
            session['status3p'] = "approve"
            session['choose'] = "สามคน"

            cur.close()
            return redirect(url_for('manager.employeeCoworkTransaction'))

    else:
        cur = db.connection.cursor()
        
        # count employee
        cur.execute("SELECT COUNT(employee_id) FROM employeeInfo WHERE sub_team=%s",[sub_team])
        employee_count = cur.fetchall()
        count = employee_count[0][0]

        # get employee in same team
        cur.execute("SELECT employee_id, employee_name, employee_lastname FROM employeeInfo WHERE sub_team=%s",[sub_team])
        idSub_team = cur.fetchall()

        otherEmployee = [0]*count
        for i in range(count):
            otherEmployee[i] = idSub_team[i][0]
        
        if count == 1:
            cur.execute("SELECT employee_id,Remark , dayoff FROM filtershift INNER JOIN employeeInfo ON filtershift.section_code = employeeInfo.section_code WHERE employee_id=%s",[otherEmployee[0]])
            workData1 = cur.fetchall()
            cur.close()
            return render_template('manager/coworkEdit.html', first_name=session.get("first_name"), last_name=session.get("last_name"),
                                idSub_team=idSub_team, workData1=workData1)
        elif count == 2:
            cur.execute("SELECT employee_id,Remark , dayoff FROM filtershift INNER JOIN employeeInfo ON filtershift.section_code = employeeInfo.section_code WHERE employee_id=%s",[otherEmployee[0]])
            workData1 = cur.fetchall()
            cur.execute("SELECT employee_id,Remark , dayoff FROM filtershift INNER JOIN employeeInfo ON filtershift.section_code = employeeInfo.section_code WHERE employee_id=%s",[otherEmployee[1]])
            workData2 = cur.fetchall()
            cur.close()
            return render_template('manager/coworkEdit.html', first_name=session.get("first_name"), last_name=session.get("last_name"),
                                idSub_team=idSub_team, workData1=workData1, workData2=workData2)
        elif count == 3:
            cur.execute("SELECT employee_id,Remark , dayoff FROM filtershift INNER JOIN employeeInfo ON filtershift.section_code = employeeInfo.section_code WHERE employee_id=%s",[otherEmployee[0]])
            workData1 = cur.fetchall()
            cur.execute("SELECT employee_id,Remark , dayoff FROM filtershift INNER JOIN employeeInfo ON filtershift.section_code = employeeInfo.section_code WHERE employee_id=%s",[otherEmployee[1]])
            workData2 = cur.fetchall()
            cur.execute("SELECT employee_id,Remark , dayoff FROM filtershift INNER JOIN employeeInfo ON filtershift.section_code = employeeInfo.section_code WHERE employee_id=%s",[otherEmployee[2]])
            workData3 = cur.fetchall()
            cur.close()
            return render_template('manager/coworkEdit.html', first_name=session.get("first_name"), last_name=session.get("last_name"),
                                idSub_team=idSub_team, workData1=workData1, workData2=workData2, workData3=workData3)
        elif count == 4:
            cur.execute("SELECT employee_id,Remark , dayoff FROM filtershift INNER JOIN employeeInfo ON filtershift.section_code = employeeInfo.section_code WHERE employee_id=%s",[otherEmployee[0]])
            workData1 = cur.fetchall()
            cur.execute("SELECT employee_id,Remark , dayoff FROM filtershift INNER JOIN employeeInfo ON filtershift.section_code = employeeInfo.section_code WHERE employee_id=%s",[otherEmployee[1]])
            workData2 = cur.fetchall()
            cur.execute("SELECT employee_id,Remark , dayoff FROM filtershift INNER JOIN employeeInfo ON filtershift.section_code = employeeInfo.section_code WHERE employee_id=%s",[otherEmployee[2]])
            workData3 = cur.fetchall()
            cur.execute("SELECT employee_id,Remark , dayoff FROM filtershift INNER JOIN employeeInfo ON filtershift.section_code = employeeInfo.section_code WHERE employee_id=%s",[otherEmployee[3]])
            workData4 = cur.fetchall()
            cur.close()
            return render_template('manager/coworkEdit.html', first_name=session.get("first_name"), last_name=session.get("last_name"),
                                idSub_team=idSub_team, workData1=workData1, workData2=workData2, workData3=workData3, workData4=workData4)
        elif count == 5:
            cur.execute("SELECT employee_id,Remark , dayoff FROM filtershift INNER JOIN employeeInfo ON filtershift.section_code = employeeInfo.section_code WHERE employee_id=%s",[otherEmployee[0]])
            workData1 = cur.fetchall()
            cur.execute("SELECT employee_id,Remark , dayoff FROM filtershift INNER JOIN employeeInfo ON filtershift.section_code = employeeInfo.section_code WHERE employee_id=%s",[otherEmployee[1]])
            workData2 = cur.fetchall()
            cur.execute("SELECT employee_id,Remark , dayoff FROM filtershift INNER JOIN employeeInfo ON filtershift.section_code = employeeInfo.section_code WHERE employee_id=%s",[otherEmployee[2]])
            workData3 = cur.fetchall()
            cur.execute("SELECT employee_id,Remark , dayoff FROM filtershift INNER JOIN employeeInfo ON filtershift.section_code = employeeInfo.section_code WHERE employee_id=%s",[otherEmployee[3]])
            workData4 = cur.fetchall()
            cur.execute("SELECT employee_id,Remark , dayoff FROM filtershift INNER JOIN employeeInfo ON filtershift.section_code = employeeInfo.section_code WHERE employee_id=%s",[otherEmployee[4]])
            workData5 = cur.fetchall()
            return render_template('manager/coworkEdit.html', first_name=session.get("first_name"), last_name=session.get("last_name"),
                                idSub_team=idSub_team, workData1=workData1, workData2=workData2, workData3=workData3, workData4=workData4, workData5=workData5)


@manager.route('/manager/edit/addshift', methods=['POST','GET'])
def editAddShift():
    line_id = session.get("line_id") # in case for query
    sub_team = session.get("sub_team")
    approver_id = session.get("approver_id")
    requestId = approver_id
        
    if line_id is None or session.get("first_name") == "userNotFound":
        return render_template('manager/warning.html')
    
    elif request.method == 'POST':
        if request.form['choose'] == "add":
            employee_id = request.form['name']
            date = request.form['date']
            OldShift = request.form['OldShift']
            addShift = request.form['addShift']
            reason = request.form['reason']
            current_time = datetime.datetime.now()
            TimeStamp = current_time.strftime("%Y-%m-%d %H:%M:%S")
            
            status = "unsuccessful"
              
            cur = db.connection.cursor()
            cur.execute("INSERT INTO transactionaddShift (requestId, employee_id , date , OldShift , addShift , TimeStamp ,  reason , status , approver_id ) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)",(requestId, employee_id , date , OldShift , addShift , TimeStamp ,  reason , status , approver_id))
            db.connection.commit()
            cur.close()
            return redirect(url_for('manager.editAddShift'))

        elif request.form['choose'] == "update":
            transactionaddShift_id = request.form['transactionaddShift_id']
            employee_id = request.form['name']
            date = request.form['date']
            OldShift = request.form['OldShift']
            addShift = request.form['addShift']
            reason = request.form['reason']
            current_time = datetime.datetime.now()
            TimeStamp = current_time.strftime("%Y-%m-%d %H:%M:%S")

            cur = db.connection.cursor()
            cur.execute("UPDATE transactionaddShift SET requestId=%s, employee_id=%s, date=%s , OldShift=%s , addShift=%s , reason=%s , TimeStamp=%s WHERE transactionaddShift_id=%s",(requestId, employee_id, date , OldShift , addShift , reason, TimeStamp, transactionaddShift_id))
            db.connection.commit()
            cur.close()
            return redirect(url_for('manager.editAddShift'))

        elif request.form['choose'] == "delete":
            transactionaddShift_id = request.form['transactionaddShift_id']

            cur = db.connection.cursor()
            cur.execute("DELETE FROM transactionaddShift WHERE transactionaddShift_id=%s",[transactionaddShift_id])
            db.connection.commit()
            cur.close()
            return redirect(url_for('manager.editAddShift'))

    else:     
        cur = db.connection.cursor()

        # count employee
        cur.execute("SELECT COUNT(employee_id) FROM employeeInfo WHERE sub_team=%s",[sub_team])
        employee_count = cur.fetchall()
        count = employee_count[0][0]

        # get all employee in same team 
        cur.execute("SELECT employee_id, employee_name, employee_lastname FROM employeeInfo WHERE sub_team=%s",[sub_team])
        idSub_teamAll = cur.fetchall()
        
        transactionaddShift_element = cur.execute("SELECT * FROM transactionaddShift WHERE requestId=%s AND status=%s", (approver_id, "unsuccessful"))
        transactionaddShift = cur.fetchall()

        otherEmployee = [0]*count
        for i in range(count):
            otherEmployee[i] = idSub_teamAll[i][0]

        if count == 1:
            cur.execute("SELECT employee_id,Remark , dayoff FROM filtershift INNER JOIN employeeInfo ON filtershift.section_code = employeeInfo.section_code WHERE employee_id=%s",[otherEmployee[0]])
            workData1 = cur.fetchall()
            cur.close()
            return render_template('manager/addshiftEdit.html', first_name=session.get("first_name"), last_name=session.get("last_name"),
                                idSub_teamAll=idSub_teamAll, workData1=workData1,
                                transactionaddShift_element=transactionaddShift_element, transactionaddShift=transactionaddShift)
        elif count == 2:
            cur.execute("SELECT employee_id,Remark , dayoff FROM filtershift INNER JOIN employeeInfo ON filtershift.section_code = employeeInfo.section_code WHERE employee_id=%s",[otherEmployee[0]])
            workData1 = cur.fetchall()
            cur.execute("SELECT employee_id,Remark , dayoff FROM filtershift INNER JOIN employeeInfo ON filtershift.section_code = employeeInfo.section_code WHERE employee_id=%s",[otherEmployee[1]])
            workData2 = cur.fetchall()
            cur.close()
            return render_template('manager/addshiftEdit.html', first_name=session.get("first_name"), last_name=session.get("last_name"),
                                idSub_teamAll=idSub_teamAll, workData1=workData1, workData2=workData2, 
                                transactionaddShift_element=transactionaddShift_element, transactionaddShift=transactionaddShift)
        elif count == 3:
            cur.execute("SELECT employee_id,Remark , dayoff FROM filtershift INNER JOIN employeeInfo ON filtershift.section_code = employeeInfo.section_code WHERE employee_id=%s",[otherEmployee[0]])
            workData1 = cur.fetchall()
            cur.execute("SELECT employee_id,Remark , dayoff FROM filtershift INNER JOIN employeeInfo ON filtershift.section_code = employeeInfo.section_code WHERE employee_id=%s",[otherEmployee[1]])
            workData2 = cur.fetchall()
            cur.execute("SELECT employee_id,Remark , dayoff FROM filtershift INNER JOIN employeeInfo ON filtershift.section_code = employeeInfo.section_code WHERE employee_id=%s",[otherEmployee[2]])
            workData3 = cur.fetchall()
            cur.close()
            return render_template('manager/addshiftEdit.html', first_name=session.get("first_name"), last_name=session.get("last_name"),
                                idSub_teamAll=idSub_teamAll, workData1=workData1, workData2=workData2, workData3=workData3, 
                                transactionaddShift_element=transactionaddShift_element, transactionaddShift=transactionaddShift)
        elif count == 4:
            cur.execute("SELECT employee_id,Remark , dayoff FROM filtershift INNER JOIN employeeInfo ON filtershift.section_code = employeeInfo.section_code WHERE employee_id=%s",[otherEmployee[0]])
            workData1 = cur.fetchall()
            cur.execute("SELECT employee_id,Remark , dayoff FROM filtershift INNER JOIN employeeInfo ON filtershift.section_code = employeeInfo.section_code WHERE employee_id=%s",[otherEmployee[1]])
            workData2 = cur.fetchall()
            cur.execute("SELECT employee_id,Remark , dayoff FROM filtershift INNER JOIN employeeInfo ON filtershift.section_code = employeeInfo.section_code WHERE employee_id=%s",[otherEmployee[2]])
            workData3 = cur.fetchall()
            cur.execute("SELECT employee_id,Remark , dayoff FROM filtershift INNER JOIN employeeInfo ON filtershift.section_code = employeeInfo.section_code WHERE employee_id=%s",[otherEmployee[3]])
            workData4 = cur.fetchall()
            cur.close()
            return render_template('manager/addshiftEdit.html', first_name=session.get("first_name"), last_name=session.get("last_name"),
                                idSub_teamAll=idSub_teamAll, workData1=workData1, workData2=workData2, workData3=workData3, workData4=workData4,
                                transactionaddShift_element=transactionaddShift_element, transactionaddShift=transactionaddShift)
        elif count == 5:
            cur.execute("SELECT employee_id,Remark , dayoff FROM filtershift INNER JOIN employeeInfo ON filtershift.section_code = employeeInfo.section_code WHERE employee_id=%s",[otherEmployee[0]])
            workData1 = cur.fetchall()
            cur.execute("SELECT employee_id,Remark , dayoff FROM filtershift INNER JOIN employeeInfo ON filtershift.section_code = employeeInfo.section_code WHERE employee_id=%s",[otherEmployee[1]])
            workData2 = cur.fetchall()
            cur.execute("SELECT employee_id,Remark , dayoff FROM filtershift INNER JOIN employeeInfo ON filtershift.section_code = employeeInfo.section_code WHERE employee_id=%s",[otherEmployee[2]])
            workData3 = cur.fetchall()
            cur.execute("SELECT employee_id,Remark , dayoff FROM filtershift INNER JOIN employeeInfo ON filtershift.section_code = employeeInfo.section_code WHERE employee_id=%s",[otherEmployee[3]])
            workData4 = cur.fetchall()
            cur.execute("SELECT employee_id,Remark , dayoff FROM filtershift INNER JOIN employeeInfo ON filtershift.section_code = employeeInfo.section_code WHERE employee_id=%s",[otherEmployee[4]])
            workData5 = cur.fetchall()
            return render_template('manager/addshiftEdit.html', first_name=session.get("first_name"), last_name=session.get("last_name"),
                                idSub_teamAll=idSub_teamAll, workData1=workData1, workData2=workData2, workData3=workData3, workData4=workData4, workData5=workData5,
                                transactionaddShift_element=transactionaddShift_element, transactionaddShift=transactionaddShift)


@manager.route('/manager/edit/shiftandoff', methods=['POST','GET'])
def chooseEditShiftAndOff():
    line_id = session.get("line_id") # in case for query
    sub_team = session.get("sub_team")
    approver_id = session.get("approver_id")
    requestId = approver_id
        
    if line_id is None or session.get("first_name") == "userNotFound":
        return render_template('manager/warning.html')
    
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
            return redirect(url_for('manager.chooseEditShiftAndOff'))

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
            return redirect(url_for('manager.chooseEditShiftAndOff'))

        elif request.form['choose'] == "delete":
            transactionChangeWork_id = request.form['transactionChangeWork_id']

            cur = db.connection.cursor()
            cur.execute("DELETE FROM transactionChangeWork WHERE transactionChangeWork_id=%s",[transactionChangeWork_id])
            db.connection.commit()
            cur.close()
            return redirect(url_for('manager.chooseEditShiftAndOff'))

    else:
        cur = db.connection.cursor()

        # count employee
        cur.execute("SELECT COUNT(employee_id) FROM employeeInfo WHERE sub_team=%s",[sub_team])
        employee_count = cur.fetchall()
        count = employee_count[0][0]

        # get all employee in same team 
        cur.execute("SELECT employee_id, employee_name, employee_lastname FROM employeeInfo WHERE sub_team=%s",[sub_team])
        idSub_teamAll = cur.fetchall()

        # get all section_code
        section_code_element = cur.execute("SELECT Remark, dayoff, section_code FROM filtershift")
        section_code_data = cur.fetchall()
        
        transactionChangeWork_element = cur.execute(" SELECT * FROM transactionChangeWork WHERE requestId=%s AND status=%s", (approver_id, "unsuccessful"))
        transactionChangeWork = cur.fetchall()

        otherEmployee = [0]*count
        for i in range(count):
            otherEmployee[i] = idSub_teamAll[i][0]

        if count == 1:
            cur.execute("SELECT employee_id,Remark , dayoff FROM filtershift INNER JOIN employeeInfo ON filtershift.section_code = employeeInfo.section_code WHERE employee_id=%s",[otherEmployee[0]])
            workData1 = cur.fetchall()
            cur.close()
            return render_template('manager/editShiftAndOff.html', first_name=session.get("first_name"), last_name=session.get("last_name"),
                                idSub_teamAll=idSub_teamAll, workData1=workData1, section_code_element=section_code_element,
                                section_code_data=section_code_data, transactionChangeWork_element=transactionChangeWork_element, transactionChangeWork=transactionChangeWork )
        elif count == 2:
            cur.execute("SELECT employee_id,Remark , dayoff FROM filtershift INNER JOIN employeeInfo ON filtershift.section_code = employeeInfo.section_code WHERE employee_id=%s",[otherEmployee[0]])
            workData1 = cur.fetchall()
            cur.execute("SELECT employee_id,Remark , dayoff FROM filtershift INNER JOIN employeeInfo ON filtershift.section_code = employeeInfo.section_code WHERE employee_id=%s",[otherEmployee[1]])
            workData2 = cur.fetchall()
            cur.close()
            return render_template('manager/editShiftAndOff.html', first_name=session.get("first_name"), last_name=session.get("last_name"),
                                idSub_teamAll=idSub_teamAll, workData1=workData1, workData2=workData2, section_code_element=section_code_element,
                                section_code_data=section_code_data, transactionChangeWork_element=transactionChangeWork_element, transactionChangeWork=transactionChangeWork )
        elif count == 3:
            cur.execute("SELECT employee_id,Remark , dayoff FROM filtershift INNER JOIN employeeInfo ON filtershift.section_code = employeeInfo.section_code WHERE employee_id=%s",[otherEmployee[0]])
            workData1 = cur.fetchall()
            cur.execute("SELECT employee_id,Remark , dayoff FROM filtershift INNER JOIN employeeInfo ON filtershift.section_code = employeeInfo.section_code WHERE employee_id=%s",[otherEmployee[1]])
            workData2 = cur.fetchall()
            cur.execute("SELECT employee_id,Remark , dayoff FROM filtershift INNER JOIN employeeInfo ON filtershift.section_code = employeeInfo.section_code WHERE employee_id=%s",[otherEmployee[2]])
            workData3 = cur.fetchall()
            cur.close()
            return render_template('manager/editShiftAndOff.html', first_name=session.get("first_name"), last_name=session.get("last_name"),
                                idSub_teamAll=idSub_teamAll, workData1=workData1, workData2=workData2, workData3=workData3, section_code_element=section_code_element,
                                section_code_data=section_code_data, transactionChangeWork_element=transactionChangeWork_element, transactionChangeWork=transactionChangeWork )
        elif count == 4:
            cur.execute("SELECT employee_id,Remark , dayoff FROM filtershift INNER JOIN employeeInfo ON filtershift.section_code = employeeInfo.section_code WHERE employee_id=%s",[otherEmployee[0]])
            workData1 = cur.fetchall()
            cur.execute("SELECT employee_id,Remark , dayoff FROM filtershift INNER JOIN employeeInfo ON filtershift.section_code = employeeInfo.section_code WHERE employee_id=%s",[otherEmployee[1]])
            workData2 = cur.fetchall()
            cur.execute("SELECT employee_id,Remark , dayoff FROM filtershift INNER JOIN employeeInfo ON filtershift.section_code = employeeInfo.section_code WHERE employee_id=%s",[otherEmployee[2]])
            workData3 = cur.fetchall()
            cur.execute("SELECT employee_id,Remark , dayoff FROM filtershift INNER JOIN employeeInfo ON filtershift.section_code = employeeInfo.section_code WHERE employee_id=%s",[otherEmployee[3]])
            workData4 = cur.fetchall()
            cur.close()
            return render_template('manager/editShiftAndOff.html', first_name=session.get("first_name"), last_name=session.get("last_name"),
                                idSub_teamAll=idSub_teamAll, workData1=workData1, workData2=workData2, workData3=workData3, workData4=workData4, section_code_element=section_code_element,
                                section_code_data=section_code_data, transactionChangeWork_element=transactionChangeWork_element, transactionChangeWork=transactionChangeWork )
        elif count == 5:
            cur.execute("SELECT employee_id,Remark , dayoff FROM filtershift INNER JOIN employeeInfo ON filtershift.section_code = employeeInfo.section_code WHERE employee_id=%s",[otherEmployee[0]])
            workData1 = cur.fetchall()
            cur.execute("SELECT employee_id,Remark , dayoff FROM filtershift INNER JOIN employeeInfo ON filtershift.section_code = employeeInfo.section_code WHERE employee_id=%s",[otherEmployee[1]])
            workData2 = cur.fetchall()
            cur.execute("SELECT employee_id,Remark , dayoff FROM filtershift INNER JOIN employeeInfo ON filtershift.section_code = employeeInfo.section_code WHERE employee_id=%s",[otherEmployee[2]])
            workData3 = cur.fetchall()
            cur.execute("SELECT employee_id,Remark , dayoff FROM filtershift INNER JOIN employeeInfo ON filtershift.section_code = employeeInfo.section_code WHERE employee_id=%s",[otherEmployee[3]])
            workData4 = cur.fetchall()
            cur.execute("SELECT employee_id,Remark , dayoff FROM filtershift INNER JOIN employeeInfo ON filtershift.section_code = employeeInfo.section_code WHERE employee_id=%s",[otherEmployee[4]])
            workData5 = cur.fetchall()
            return render_template('manager/editShiftAndOff.html', first_name=session.get("first_name"), last_name=session.get("last_name"),
                                idSub_teamAll=idSub_teamAll, workData1=workData1, workData2=workData2, workData3=workData3, workData4=workData4, workData5=workData5, section_code_element=section_code_element,
                                section_code_data=section_code_data, transactionChangeWork_element=transactionChangeWork_element, transactionChangeWork=transactionChangeWork )


@manager.route('/manager/edit/shiftandoff/viewshift', methods=['POST','GET']) # แก้เป็นให้เข้าไปแก้ตาม <int:id> 
def viewShift():
    line_id = session.get("line_id") # in case for query
        
    if line_id is None or session.get("first_name") == "userNotFound":
        return render_template('manager/warning.html')
    else:
        return render_template('manager/viewShift.html', first_name=session.get("first_name"), last_name=session.get("last_name"))
    # return render_template('manager/viewShift.html')


@manager.route('/manager/edit/shiftandoff/viewshiftonly', methods=['POST','GET']) 
def viewShiftOnly():
    line_id = session.get("line_id") # in case for query
        
    if line_id is None or session.get("first_name") == "userNotFound":
        return render_template('manager/warning.html')
    else:
        return render_template('manager/viewShiftOnly.html', first_name=session.get("first_name"), last_name=session.get("last_name"))
    # return render_template('manager/viewShiftOnly.html')


@manager.route('/manager/edit/addemployee', methods=['POST','GET'])
def addEmployee():
    line_id = session.get("line_id") # in case for query
    sub_team = session.get("sub_team")
    approver_id = session.get("approver_id")
    approver_section = session.get("approver_section")
    requestId = approver_id
        
    if line_id is None or session.get("first_name") == "userNotFound":
        return render_template('manager/warning.html')
    
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
                    if name2 != "none":
                        cur.execute("UPDATE employeeInfo SET sub_team=%s WHERE employee_id=%s",(addToTeam, name2))
                    if name3 != "none":
                        cur.execute("UPDATE employeeInfo SET sub_team=%s WHERE employee_id=%s",(addToTeam, name3))
                    if name4 != "none":
                        cur.execute("UPDATE employeeInfo SET sub_team=%s WHERE employee_id=%s",(addToTeam, name4))
                    if name5 != "none":
                        cur.execute("UPDATE employeeInfo SET sub_team=%s WHERE employee_id=%s",(addToTeam, name5))
                elif request.form['choose2'] == "สร้างทีม":
                    if name1 != "none":
                        cur.execute("UPDATE employeeInfo SET sub_team=%s WHERE employee_id=%s",(createTeam, name1))
                    if name2 != "none":
                        cur.execute("UPDATE employeeInfo SET sub_team=%s WHERE employee_id=%s",(createTeam, name2))
                    if name3 != "none":
                        cur.execute("UPDATE employeeInfo SET sub_team=%s WHERE employee_id=%s",(createTeam, name3))
                    if name4 != "none":
                        cur.execute("UPDATE employeeInfo SET sub_team=%s WHERE employee_id=%s",(createTeam, name4))
                    if name5 != "none":
                        cur.execute("UPDATE employeeInfo SET sub_team=%s WHERE employee_id=%s",(createTeam, name5))
                
                db.connection.commit()
                cur.close()
                return redirect(url_for('manager.addEmployee'))

            elif request.form['choose'] == "update":
                employeeToDelete = request.form['employeeToDelete']

                cur = db.connection.cursor()
                cur.execute("UPDATE employeeInfo SET sub_team=%s WHERE employee_id=%s",(" ", employeeToDelete))
                db.connection.commit()
                cur.close()
                return redirect(url_for('manager.addEmployee'))

            elif request.form['choose'] == "delete":
                sub_team = request.form['sub_team']

                cur = db.connection.cursor()
                cur.execute("UPDATE employeeInfo SET sub_team=%s WHERE sub_team=%s",(" ", sub_team))
                db.connection.commit()
                cur.close()
                return redirect(url_for('manager.addEmployee'))

        elif request.form['select'] == "section":
            if request.form['choose'] == "add":
                employee_id = request.form['name-section']
                employee_name = employee_id.split()[1]
                employee_lastname = employee_id.split()[2]
                employee_id = employee_id.split()[0]
                date_start = request.form['date_start']
                date_end = request.form['date_end']
                Oldsection = request.form['Oldsection']
                Newsection = request.form['Newsection']
                current_time = datetime.datetime.now()
                TimeStamp = current_time.strftime("%Y-%m-%d %H:%M:%S")
                
                status = "unsuccessful"
                
                cur = db.connection.cursor()
                cur.execute("SELECT approver_id FROM employeeInfo WHERE employee_section=%s",[Newsection])
                approver_id = cur.fetchall()
                approver_id = approver_id[0][0]

                cur.execute("INSERT INTO transactionaddemployee (requestId, employee_id, employee_name, employee_lastname, date_start, date_end, Oldsection, Newsection, TimeStamp, status, approver_id) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(requestId, employee_id, employee_name, employee_lastname, date_start, date_end, Oldsection, Newsection, TimeStamp, status, approver_id))
                db.connection.commit()
                cur.close()
                return redirect(url_for('manager.addEmployee'))

            elif request.form['choose'] == "update":
                transactionaddemployee_id = request.form['transactionaddemployee_id']
                employee_id = request.form['name-section']
                employee_name = employee_id.split()[1]
                employee_lastname = employee_id.split()[2]
                employee_id = employee_id.split()[0]
                date_start = request.form['date_start']
                date_end = request.form['date_end']
                Oldsection = request.form['Oldsection']
                Newsection = request.form['Newsection']
                current_time = datetime.datetime.now()
                TimeStamp = current_time.strftime("%Y-%m-%d %H:%M:%S")
                
                status = "unsuccessful"

                cur = db.connection.cursor()
                cur.execute("SELECT approver_id FROM employeeInfo WHERE employee_section=%s",[Newsection])
                approver_id = cur.fetchall()
                approver_id = approver_id[0][0]

                cur.execute("UPDATE transactionaddemployee SET requestId=%s, employee_id=%s, employee_name=%s, employee_lastname=%s, date_start=%s, date_end=%s, Oldsection=%s, Newsection=%s, TimeStamp=%s, status=%s, approver_id=%s WHERE transactionaddemployee_id=%s",(requestId, employee_id, employee_name, employee_lastname, date_start, date_end, Oldsection, Newsection, TimeStamp, status, approver_id, transactionaddemployee_id))
                db.connection.commit()
                cur.close()
                return redirect(url_for('manager.addEmployee'))

            elif request.form['choose'] == "delete":
                transactionaddemployee_id = request.form['transactionaddemployee_id']

                cur = db.connection.cursor()
                cur.execute("DELETE FROM transactionaddemployee WHERE transactionaddemployee_id=%s",[transactionaddemployee_id])
                db.connection.commit()
                cur.close()
                return redirect(url_for('manager.addEmployee'))

    else:
        cur = db.connection.cursor()
        transactionaddemployee_element = cur.execute(" SELECT * FROM transactionaddemployee WHERE requestId=%s AND status=%s", (approver_id, "unsuccessful"))
        transactionaddemployee = cur.fetchall()
        cur.execute("SELECT * FROM employeeInfo")
        allEmployee = cur.fetchall()
        cur.execute("SELECT DISTINCT employee_section FROM employeeInfo")
        employee_section = cur.fetchall()
        user_section = approver_section
        cur.execute("SELECT employee_id , employee_name , employee_lastname FROM employeeInfo WHERE employee_section=%s",[user_section])
        employeeInsection = cur.fetchall()
        teamInSection_element = cur.execute("SELECT sub_team, COUNT(employee_id) as num FROM employeeInfo WHERE employee_section=%s AND sub_team!=%s GROUP BY sub_team",(user_section, " "))
        teamInSection = cur.fetchall()
        employeeInTeam_element = cur.execute("SELECT sub_team , employee_id, employee_name, employee_lastname  FROM employeeInfo WHERE employee_section=%s",[user_section])
        employeeInTeam = cur.fetchall()
        cur.close()

        return render_template('manager/addEmployee.html', first_name=session.get("first_name"), last_name=session.get("last_name"),
                        transactionaddemployee_element=transactionaddemployee_element, transactionaddemployee=transactionaddemployee,
                        allEmployee=allEmployee, employeeInsection=employeeInsection, employee_section=employee_section,
                        teamInSection_element=teamInSection_element, teamInSection=teamInSection, employeeInTeam_element=employeeInTeam_element,
                        employeeInTeam=employeeInTeam)


####################################################################################################

@manager.route('/manager/edit/selflist/selflistsummary', methods=['POST','GET'])
def employeeSelfTransaction():
    line_id = session.get("line_id") # in case for query
    approver_id = session.get("approver_id")
        
    if line_id is None or session.get("first_name") == "userNotFound":
        return render_template('manager/warning.html')

    elif request.method == 'POST':
        if request.form['choose'] == "cancel":
            cur = db.connection.cursor()
            cur.execute("DELETE FROM transactionChangeShift WHERE requestId=%s AND status=%s", [approver_id, "unsuccessful"])
            db.connection.commit()
            cur.close()
            return redirect(url_for('manager.editYourselfList'))

        elif request.form['choose'] == "confirm":
            current_time = datetime.datetime.now()
            TimeStamp = current_time.strftime("%Y-%m-%d %H:%M:%S")

            cur = db.connection.cursor()
            cur.execute("UPDATE transactionChangeShift SET status=%s, TimeStamp=%s  WHERE  requestId=%s AND status=%s", ("approve", TimeStamp, approver_id, "unsuccessful"))
            db.connection.commit()
            cur.close()
            return redirect(url_for('manager.employeeSelfTransactionEnd'))

    else:
        cur = db.connection.cursor()
        transactionChangeShift_element = cur.execute(" SELECT * FROM transactionChangeShift WHERE requestId=%s AND status=%s", (approver_id, "unsuccessful"))
        transactionChangeShift = cur.fetchall()
        cur.close()

        return render_template('manager/selfEditListSummary.html', first_name=session.get("first_name"), last_name=session.get("last_name"),
                        transactionChangeShift_element=transactionChangeShift_element, transactionChangeShift=transactionChangeShift)


@manager.route('/manager/edit/cowork/coworksummary', methods=['POST','GET'])
def employeeCoworkTransaction():
    line_id = session.get("line_id") # in case for query
    approver_id = session.get("approver_id")
    requestId = approver_id

    if line_id is None or session.get("first_name") == "userNotFound":
        return render_template('manager/warning.html')

    elif session.get("choose") == "สองคน":
        date1 = session.get("date2-1")

        name1 = session.get("name2-1")
        employee_name1 = session.get("employee_name1")
        employee_lastname1 = session.get("employee_lastname1")
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
        status = "approve"
        
        if request.method == 'POST':
            if request.form['choose'] == "cancel":
                return redirect(url_for('manager.editCowork'))

            elif request.form['choose'] == "confirm":
                current_time = datetime.datetime.now()
                TimeStamp = current_time.strftime("%Y-%m-%d %H:%M:%S")

                cur = db.connection.cursor()
                cur.execute("INSERT INTO transactionCoworkShift (requestId, employee_id , date , OldShift , NewShift , TimeStamp ,  reason , status , approver_id, employee_id2, employee_name2, employee_lastname2, OldShift2, NewShift2 ) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(requestId, name1 , date1 , OldShift1 , NewShift1 , TimeStamp ,  reason , status , approver_id, name2, employee_name2, employee_lastname2, OldShift2, NewShift2))
                db.connection.commit()
                cur.close()
                return redirect(url_for('manager.employeeCoworkTransactionEnd'))

        return render_template('manager/coworkEditListSummary.html', first_name=session.get("first_name"), last_name=session.get("last_name"),
                    date1=date1,name1=name1,employee_name1=employee_name1,employee_lastname1=employee_lastname1,OldShift1=OldShift1,NewShift1=NewShift1,
                    employee_name2=employee_name2,employee_lastname2=employee_lastname2,OldShift2=OldShift2,NewShift2=NewShift2,reason=reason, employee_name3=employee_name3)

    elif session.get("choose") == "สามคน":
        date1 = session.get("date3-1")

        name1 = session.get("name2-1")
        employee_name1 = session.get("employee_name1")
        employee_lastname1 = session.get("employee_lastname1")
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
        status = "approve"
        
        if request.method == 'POST':
            if request.form['choose'] == "cancel":
                return redirect(url_for('manager.editCowork'))

            elif request.form['choose'] == "confirm":
                current_time = datetime.datetime.now()
                TimeStamp = current_time.strftime("%Y-%m-%d %H:%M:%S")

                cur = db.connection.cursor()
                cur.execute("INSERT INTO transactionCoworkShift (requestId, employee_id , date , OldShift , NewShift , TimeStamp ,  reason , status , approver_id, employee_id2, employee_name2, employee_lastname2, OldShift2, NewShift2, employee_id3, employee_name3, employee_lastname3, OldShift3, NewShift3 ) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(requestId, name1 , date1 , OldShift1 , NewShift1 , TimeStamp ,  reason , status , approver_id, name2, employee_name2, employee_lastname2, OldShift2, NewShift2, name3, employee_name3, employee_lastname3, OldShift3, NewShift3))
                db.connection.commit()
                cur.close()
                return redirect(url_for('manager.employeeCoworkTransactionEnd'))

        return render_template('manager/coworkEditListSummary.html', first_name=session.get("first_name"), last_name=session.get("last_name"),
                    date1=date1,name1=name1,employee_name1=employee_name1,employee_lastname1=employee_lastname1,OldShift1=OldShift1,NewShift1=NewShift1,
                    employee_name2=employee_name2,employee_lastname2=employee_lastname2,OldShift2=OldShift2,NewShift2=NewShift2,employee_name3=employee_name3,
                    employee_lastname3=employee_lastname3,OldShift3=OldShift3,NewShift3=NewShift3,reason=reason)
        
    else:
        return render_template('manager/coworkEditListSummary.html', first_name=session.get("first_name"), last_name=session.get("last_name"))


@manager.route('/manager/edit/addshift/addshiftsummary', methods=['POST','GET'])
def employeeAddShiftTransaction():
    line_id = session.get("line_id") # in case for query
    approver_id = session.get("approver_id")
        
    if line_id is None or session.get("first_name") == "userNotFound":
        return render_template('manager/warning.html')

    elif request.method == 'POST':
        if request.form['choose'] == "cancel":
            cur = db.connection.cursor()
            cur.execute("DELETE FROM transactionaddShift WHERE requestId=%s AND status=%s", [approver_id, "unsuccessful"])
            db.connection.commit()
            cur.close()
            return redirect(url_for('manager.editAddShift'))

        elif request.form['choose'] == "confirm":
            current_time = datetime.datetime.now()
            TimeStamp = current_time.strftime("%Y-%m-%d %H:%M:%S")

            cur = db.connection.cursor()
            cur.execute("UPDATE transactionaddShift SET status=%s, TimeStamp=%s  WHERE  requestId=%s AND status=%s", ("approve", TimeStamp, approver_id, "unsuccessful"))
            db.connection.commit()
            cur.close()
            return redirect(url_for('manager.employeeAddShiftTransactionEnd'))

    else:
        cur = db.connection.cursor()
        transactionaddShift_element = cur.execute(" SELECT * FROM transactionaddShift WHERE requestId=%s AND status=%s", (approver_id, "unsuccessful"))
        transactionaddShift = cur.fetchall()
        cur.close()

        return render_template('manager/addShiftEditListSummary.html', first_name=session.get("first_name"), last_name=session.get("last_name"),
                        transactionaddShift_element=transactionaddShift_element, transactionaddShift=transactionaddShift)


@manager.route('/manager/edit/shiftandoff/shiftandoffsummary', methods=['POST','GET'])
def employeeShiftAndOffTransaction():
    line_id = session.get("line_id") # in case for query
    approver_id = session.get("approver_id")
        
    if line_id is None or session.get("first_name") == "userNotFound":
        return render_template('manager/warning.html')

    elif request.method == 'POST':
        if request.form['choose'] == "cancel":
            cur = db.connection.cursor()
            cur.execute("DELETE FROM transactionChangeWork WHERE requestId=%s AND status=%s", [approver_id, "unsuccessful"])
            db.connection.commit()
            cur.close()
            return redirect(url_for('manager.chooseEditShiftAndOff'))

        elif request.form['choose'] == "confirm":
            current_time = datetime.datetime.now()
            TimeStamp = current_time.strftime("%Y-%m-%d %H:%M:%S")

            cur = db.connection.cursor()
            cur.execute("UPDATE transactionChangeWork SET status=%s, TimeStamp=%s  WHERE  requestId=%s AND status=%s", ("approve", TimeStamp, approver_id, "unsuccessful"))
            db.connection.commit()
            cur.close()
            return redirect(url_for('manager.employeeShiftAndOffTransactionEnd'))

    else:
        cur = db.connection.cursor()
        transactionChangeWork_element = cur.execute(" SELECT * FROM transactionChangeWork WHERE requestId=%s AND status=%s", (approver_id, "unsuccessful"))
        transactionChangeWork = cur.fetchall()
        cur.close()

        return render_template('manager/shiftAndOffEditListSummary.html', first_name=session.get("first_name"), last_name=session.get("last_name"),
                        transactionChangeWork_element=transactionChangeWork_element, transactionChangeWork=transactionChangeWork)


@manager.route('/manager/edit/addemployee/addemployeesummary', methods=['POST','GET'])
def employeeAddTransaction():
    line_id = session.get("line_id") # in case for query
    approver_id = session.get("approver_id")
        
    if line_id is None or session.get("first_name") == "userNotFound":
        return render_template('manager/warning.html')

    elif request.method == 'POST':
        if request.form['choose'] == "cancel":
            cur = db.connection.cursor()
            cur.execute("DELETE FROM transactionaddemployee WHERE requestId=%s AND status=%s", [approver_id, "unsuccessful"])
            db.connection.commit()
            cur.close()
            return redirect(url_for('manager.addEmployee'))

        elif request.form['choose'] == "confirm":
            current_time = datetime.datetime.now()
            TimeStamp = current_time.strftime("%Y-%m-%d %H:%M:%S")

            cur = db.connection.cursor()
            cur.execute("UPDATE transactionaddemployee SET status=%s, TimeStamp=%s  WHERE  requestId=%s AND status=%s", ("approve", TimeStamp, approver_id, "unsuccessful"))
            db.connection.commit()
            cur.close()
            return redirect(url_for('manager.employeeAddEmployeeTransactionEnd'))

    else:
        cur = db.connection.cursor()
        transactionaddemployee_element = cur.execute(" SELECT * FROM transactionaddemployee WHERE requestId=%s AND status=%s", (approver_id, "unsuccessful"))
        transactionaddemployee = cur.fetchall()
        cur.close()

        return render_template('manager/addEmployeeEditListSummary.html', first_name=session.get("first_name"), last_name=session.get("last_name"),
                        transactionaddemployee_element=transactionaddemployee_element, transactionaddemployee=transactionaddemployee)


####################################################################################################

@manager.route('/manager/status/pending/approvetransactionend', methods=['POST','GET'])
def managerApproveTransactionEnd():
    line_id = session.get("line_id") # in case for query
        
    if line_id is None or session.get("first_name") == "userNotFound":
        render_template('manager/warning.html')
    else:
        return render_template('manager/approveTransactionEnd.html', first_name=session.get("first_name"), last_name=session.get("last_name"))
    # return render_template('manager/approveTransactionEnd.html')


@manager.route('/manager/edit/selflist/selflistsummary/selftransactionend', methods=['POST','GET'])
def employeeSelfTransactionEnd():
    line_id = session.get("line_id") # in case for query
        
    if line_id is None or session.get("first_name") == "userNotFound":
        return render_template('manager/warning.html')
    else:
        return render_template('manager/selfTransactionEnd.html', first_name=session.get("first_name"), last_name=session.get("last_name"))
    # return render_template('manager/selfTransactionEnd.html')


@manager.route('/manager/edit/cowork/coworksummary/coworktransactionend', methods=['POST','GET'])
def employeeCoworkTransactionEnd():
    line_id = session.get("line_id") # in case for query
        
    if line_id is None or session.get("first_name") == "userNotFound":
        return render_template('manager/warning.html')
    else:
        return render_template('manager/coworkTransactionEnd.html', first_name=session.get("first_name"), last_name=session.get("last_name"))
    # return render_template('manager/coworkTransactionEnd.html')


@manager.route('/manager/edit/addshift/addshiftsummary/addshifttransactionend', methods=['POST','GET'])
def employeeAddShiftTransactionEnd():
    line_id = session.get("line_id") # in case for query
        
    if line_id is None or session.get("first_name") == "userNotFound":
        return render_template('manager/warning.html')
    else:
        return render_template('manager/addShiftTransactionEnd.html', first_name=session.get("first_name"), last_name=session.get("last_name"))
    # return render_template('manager/addShiftTransactionEnd.html')


@manager.route('/manager/edit/shiftandoff/shiftandoffsummary/shiftandofftransactionend', methods=['POST','GET'])
def employeeShiftAndOffTransactionEnd():
    line_id = session.get("line_id") # in case for query
        
    if line_id is None or session.get("first_name") == "userNotFound":
        return render_template('manager/warning.html')
    else:
        return render_template('manager/shiftAndOffTransactionEnd.html', first_name=session.get("first_name"), last_name=session.get("last_name"))
    # return render_template('manager/shiftAndOffTransactionEnd.html')


@manager.route('/manager/edit/addemployee/addemployeesummary/addemployeetransactionend', methods=['POST','GET'])
def employeeAddEmployeeTransactionEnd():
    line_id = session.get("line_id") # in case for query
        
    if line_id is None or session.get("first_name") == "userNotFound":
        return render_template('manager/warning.html')
    else:
        return render_template('manager/addEmployeeTransactionEnd.html', first_name=session.get("first_name"), last_name=session.get("last_name"))
    # return render_template('manager/addEmployeeTransactionEnd.html')

