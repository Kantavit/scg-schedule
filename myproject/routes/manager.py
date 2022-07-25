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
        
    if line_id is None or session.get("first_name") == "userNotFound":
        return render_template('manager/warning.html')
    else:
        return render_template('manager/pending.html', first_name=session.get("first_name"), last_name=session.get("last_name"))
    # return render_template('manager/pending.html')

@manager.route('/manager/status/approve', methods=['POST','GET'])
def approve():
    line_id = session.get("line_id") # in case for query
        
    if line_id is None or session.get("first_name") == "userNotFound":
        return render_template('manager/warning.html')
    else:
        return render_template('manager/approve.html', first_name=session.get("first_name"), last_name=session.get("last_name"))
    # return render_template('manager/approve.html')

@manager.route('/manager/shift')
def chooseEditShift():
    line_id = session.get("line_id") # in case for query
        
    if line_id is None or session.get("first_name") == "userNotFound":
        return render_template('manager/warning.html')
    else:
        return render_template('manager/editShift.html', first_name=session.get("first_name"), last_name=session.get("last_name"))
    # return render_template('manager/editShift.html')

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
        
    if line_id is None or session.get("first_name") == "userNotFound":
        return render_template('manager/warning.html')
    else:
        return render_template('manager/selfEditList.html', first_name=session.get("first_name"), last_name=session.get("last_name"))
    # return render_template('manager/selfEditList.html')


@manager.route('/manager/edit/cowork', methods=['POST','GET'])
def editCowork():
    line_id = session.get("line_id") # in case for query
        
    if line_id is None or session.get("first_name") == "userNotFound":
        return render_template('manager/warning.html')
    else:
        return render_template('manager/coworkEdit.html', first_name=session.get("first_name"), last_name=session.get("last_name"))
    # return render_template('manager/coworkEdit.html')
    # ถ้าคนเป็น 2 ให้รับค่าแค่ 2 แถวแรก ถ้า 3 คนให้เอาทั้ง 3 แถว ถ้าเลือก 2 คนใส่มาคนเดียวให้ซ้ำหน้าเดิม


@manager.route('/manager/edit/addshift', methods=['POST','GET'])
def editAddShift():
    line_id = session.get("line_id") # in case for query
        
    if line_id is None or session.get("first_name") == "userNotFound":
        return render_template('manager/warning.html')
    else:
        return render_template('manager/addshiftEdit.html', first_name=session.get("first_name"), last_name=session.get("last_name"))
    # return render_template('manager/addshiftEdit.html')


@manager.route('/manager/edit/shiftandoff', methods=['POST','GET'])
def chooseEditShiftAndOff():
    line_id = session.get("line_id") # in case for query
        
    if line_id is None or session.get("first_name") == "userNotFound":
        return render_template('manager/warning.html')
    else:
        return render_template('manager/editShiftAndOff.html', first_name=session.get("first_name"), last_name=session.get("last_name"))
    # return render_template('manager/editShiftAndOff.html')


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
        
    if line_id is None or session.get("first_name") == "userNotFound":
        return render_template('manager/warning.html')
    else:
        return render_template('manager/addEmployee.html', first_name=session.get("first_name"), last_name=session.get("last_name"))
    # return render_template('manager/addEmployee.html')


####################################################################################################

@manager.route('/manager/edit/selflist/selflistsummary', methods=['POST','GET'])
def employeeSelfTransaction():
    line_id = session.get("line_id") # in case for query
        
    if line_id is None or session.get("first_name") == "userNotFound":
        return render_template('manager/warning.html')
    else:
        return render_template('manager/selfEditListSummary.html', first_name=session.get("first_name"), last_name=session.get("last_name"))
    # return render_template('manager/selfEditListSummary.html')


@manager.route('/manager/edit/cowork/coworksummary', methods=['POST','GET'])
def employeeCoworkTransaction():
    line_id = session.get("line_id") # in case for query
        
    if line_id is None or session.get("first_name") == "userNotFound":
        return render_template('manager/warning.html')
    else:
        return render_template('manager/coworkEditListSummary.html', first_name=session.get("first_name"), last_name=session.get("last_name"))
    # return render_template('manager/coworkEditListSummary.html')


@manager.route('/manager/edit/addshift/addshiftsummary', methods=['POST','GET'])
def employeeAddShiftTransaction():
    line_id = session.get("line_id") # in case for query
        
    if line_id is None or session.get("first_name") == "userNotFound":
        return render_template('manager/warning.html')
    else:
        return render_template('manager/addShiftEditListSummary.html', first_name=session.get("first_name"), last_name=session.get("last_name"))
    # return render_template('manager/addShiftEditListSummary.html')


@manager.route('/manager/edit/shiftandoff/shiftandoffsummary', methods=['POST','GET'])
def employeeShiftAndOffTransaction():
    line_id = session.get("line_id") # in case for query
        
    if line_id is None or session.get("first_name") == "userNotFound":
        return render_template('manager/warning.html')
    else:
        return render_template('manager/shiftAndOffEditListSummary.html', first_name=session.get("first_name"), last_name=session.get("last_name"))
    # return render_template('manager/shiftAndOffEditListSummary.html')


@manager.route('/manager/edit/addemployee/addemployeesummary', methods=['POST','GET'])
def employeeAddTransaction():
    line_id = session.get("line_id") # in case for query
        
    if line_id is None or session.get("first_name") == "userNotFound":
        return render_template('manager/warning.html')
    else:
        return render_template('manager/addEmployeeEditListSummary.html', first_name=session.get("first_name"), last_name=session.get("last_name"))
    # return render_template('manager/addEmployeeEditListSummary.html')


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
        render_template('manager/warning.html')
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

