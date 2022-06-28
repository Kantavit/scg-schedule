from .__init__ import employee
from ..extensions import db
from flask import render_template, redirect, url_for, request, session



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
    justQuery = cur.execute(query)
    first_name = cur.fetchall()
    query = "SELECT employee_lastname FROM employee inner join employeeInfo on employee.employee_id = employeeInfo.employee_id WHERE line_id = " + "'" + toString + "'"
    justQuery = cur.execute(query)
    last_name = cur.fetchall()
    cur.close()

    if bool(first_name) == False and bool(last_name) == False:
        session['first_name'] = "userNotFound" # send first_name to other page
        return render_template('employee/welcome.html')

    session['first_name'] = first_name # send first_name to other page
    session['last_name'] = last_name # send last_name to other page

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
        
    if line_id is None or session.get("first_name") == "userNotFound":
        return render_template('employee/warning.html')
    else:
        return render_template('employee/coworkEdit.html', first_name=session.get("first_name"), last_name=session.get("last_name"))
    # return render_template('employee/coworkEdit.html')
    # ถ้าคนเป็น 2 ให้รับค่าแค่ 2 แถวแรก ถ้า 3 คนให้เอาทั้ง 3 แถว ถ้าเลือก 2 คนใส่มาคนเดียวให้ซ้ำหน้าเดิม

@employee.route('/employee/edit/shift/addshift', methods=['POST','GET'])
def editAddShift():
    line_id = session.get("line_id") # in case for query
        
    if line_id is None or session.get("first_name") == "userNotFound":
        return render_template('employee/warning.html')
    else:
        return render_template('employee/addshiftEdit.html', first_name=session.get("first_name"), last_name=session.get("last_name"))
    # return render_template('employee/addshiftEdit.html')

####################################################################################################

@employee.route('/employee/edit/shiftandoff', methods=['POST','GET'])
def chooseEditShiftAndOff():
    line_id = session.get("line_id") # in case for query
        
    if line_id is None or session.get("first_name") == "userNotFound":
        return render_template('employee/warning.html')
    else:
        return render_template('employee/editShiftAndOff.html', first_name=session.get("first_name"), last_name=session.get("last_name"))
    # return render_template('employee/editShiftAndOff.html')

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
        
    if line_id is None or session.get("first_name") == "userNotFound":
        return render_template('employee/warning.html')
    else:
        return render_template('employee/selfEditList.html', first_name=session.get("first_name"), last_name=session.get("last_name"))
    # return render_template('employee/selfEditList.html')


@employee.route('/employee/edit/shift/self/selflist/selflistsummary', methods=['POST','GET'])
def employeeSelfTransaction():
    line_id = session.get("line_id") # in case for query
        
    if line_id is None or session.get("first_name") == "userNotFound":
        return render_template('employee/warning.html')
    else:
        return render_template('employee/selfEditListSummary.html', first_name=session.get("first_name"), last_name=session.get("last_name"))
    # return render_template('employee/selfEditListSummary.html')


@employee.route('/employee/edit/shift/cowork/coworksummary', methods=['POST','GET'])
def employeeCoworkTransaction():
    line_id = session.get("line_id") # in case for query
        
    if line_id is None or session.get("first_name") == "userNotFound":
        return render_template('employee/warning.html')
    else:
        return render_template('employee/coworkEditListSummary.html', first_name=session.get("first_name"), last_name=session.get("last_name"))
    # return render_template('employee/coworkEditListSummary.html')


@employee.route('/employee/edit/shift/addshift/addshiftsummary', methods=['POST','GET'])
def employeeAddShiftTransaction():
    line_id = session.get("line_id") # in case for query
        
    if line_id is None or session.get("first_name") == "userNotFound":
        return render_template('employee/warning.html')
    else:
        return render_template('employee/addShiftEditListSummary.html', first_name=session.get("first_name"), last_name=session.get("last_name"))
    # return render_template('employee/addShiftEditListSummary.html')


@employee.route('/employee/edit/shiftandoff/shiftandoffsummary', methods=['POST','GET'])
def employeeShiftAndOffTransaction():
    line_id = session.get("line_id") # in case for query
        
    if line_id is None or session.get("first_name") == "userNotFound":
        return render_template('employee/warning.html')
    else:
        return render_template('employee/shiftAndOffEditListSummary.html', first_name=session.get("first_name"), last_name=session.get("last_name"))
    # return render_template('employee/shiftAndOffEditListSummary.html')


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
