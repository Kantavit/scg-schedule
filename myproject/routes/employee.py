from .__init__ import employee
from ..extensions import db
from flask import render_template, redirect, url_for, request



@employee.route('/', methods=['POST','GET'])
def index():
    if request.method == 'POST':
        return redirect(url_for('employee.employeePage')) # redirect to employeePage()
    else:
        return redirect(url_for('employee.employeePage'))

@employee.route('/employee', methods=['POST','GET'])
def employeePage():
    if request.method == 'POST':
        task_content = request.form['content']
        userid = request.form['userId']
        return render_template('employee/employee.html',content=task_content, userid=userid)
    
    elif request.method == 'GET':
        # cur = db.connection.cursor()
        # users = cur.execute("SELECT * FROM users")

        # if users > 0:
        #     userDetails = cur.fetchall()
        #     cur.close()
        #     return render_template('employee/employee.html',userDetails=userDetails)

        line_userid = request.args.get("userId")
        toString = str(line_userid)
        
        cur = db.connection.cursor()
        query = "SELECT employee_name FROM employee inner join employeeInfo on employee.employee_id = employeeInfo.employee_id WHERE line_id = " + "'" + toString + "'"
        user_name = cur.execute(query)
        userDetails = cur.fetchall()
        cur.close()

        return render_template('employee/employee.html', user_name=userDetails)
        

@employee.route('/employee/edit', methods=['POST','GET'])
def chooseEdit():
    if request.method == 'POST':
        return render_template('employee/employeeEdit.html')
    else:
        return render_template('employee/employeeEdit.html')

####################################################################################################

@employee.route('/employee/edit/shift')
def chooseEditShift():
    return render_template('employee/editShift.html')

@employee.route('/employee/edit/shift/self', methods=['POST','GET'])
def editYourself():
    return render_template('employee/selfEdit.html')

@employee.route('/employee/edit/shift/cowork', methods=['POST','GET'])
def editCowork():
    return render_template('employee/coworkEdit.html')
    # ถ้าคนเป็น 2 ให้รับค่าแค่ 2 แถวแรก ถ้า 3 คนให้เอาทั้ง 3 แถว ถ้าเลือก 2 คนใส่มาคนเดียวให้ซ้ำหน้าเดิม

@employee.route('/employee/edit/shift/addshift', methods=['POST','GET'])
def editAddShift():
    return render_template('employee/addshiftEdit.html')

####################################################################################################

@employee.route('/employee/edit/shiftandoff', methods=['POST','GET'])
def chooseEditShiftAndOff():
    return render_template('employee/editShiftAndOff.html')

@employee.route('/employee/edit/shiftandoff/viewshift', methods=['POST','GET']) # แก้เป็นให้เข้าไปแก้ตาม <int:id> 
def viewShift():
    return render_template('employee/viewShift.html')

@employee.route('/employee/edit/shiftandoff/viewshiftonly', methods=['POST','GET']) 
def viewShiftOnly():
    return render_template('employee/viewShiftOnly.html')

####################################################################################################

@employee.route('/employee/edit/status')
def chooseCheckStatus():
    return render_template('employee/checkStatus.html')

@employee.route('/employee/edit/status/pending')
def pending():
    return render_template('employee/pending.html')

@employee.route('/employee/edit/status/approve')
def approve():
    return render_template('employee/approve.html')

@employee.route('/employee/edit/status/reject')
def reject():
    return render_template('employee/reject.html')

####################################################################################################

@employee.route('/employee/edit/addemployee', methods=['POST','GET'])
def addEmployee():
    return render_template('employee/addEmployee.html')

####################################################################################################

@employee.route('/employee/edit/shift/self/selflist', methods=['POST','GET'])
def editYourselfList():
    return render_template('employee/selfEditList.html')


@employee.route('/employee/edit/shift/self/selflist/selflistsummary', methods=['POST','GET'])
def employeeSelfTransaction():
    return render_template('employee/selfEditListSummary.html')


@employee.route('/employee/edit/shift/cowork/coworksummary', methods=['POST','GET'])
def employeeCoworkTransaction():
    return render_template('employee/coworkEditListSummary.html')


@employee.route('/employee/edit/shift/addshift/addshiftsummary', methods=['POST','GET'])
def employeeAddShiftTransaction():
    return render_template('employee/addShiftEditListSummary.html')


@employee.route('/employee/edit/shiftandoff/shiftandoffsummary', methods=['POST','GET'])
def employeeShiftAndOffTransaction():
    return render_template('employee/shiftAndOffEditListSummary.html')


@employee.route('/employee/edit/addemployee/addemployeesummary', methods=['POST','GET'])
def employeeAddTransaction():
    return render_template('employee/addEmployeeEditListSummary.html')

####################################################################################################

@employee.route('/employee/edit/shift/self/selflist/selflistsummary/selftransactionend', methods=['POST','GET'])
def employeeSelfTransactionEnd():
    return render_template('employee/selfTransactionEnd.html')
    # บันทึกลง table transaction

@employee.route('/employee/edit/shift/cowork/coworksummary/coworktransactionend', methods=['POST','GET'])
def employeeCoworkTransactionEnd():
    return render_template('employee/coworkTransactionEnd.html')
    # บันทึกลง table transaction

@employee.route('/employee/edit/shift/addshift/addshiftsummary/addshifttransactionend', methods=['POST','GET'])
def employeeAddShiftTransactionEnd():
    return render_template('employee/addShiftTransactionEnd.html')
    # บันทึกลง table transaction

@employee.route('/employee/edit/shiftandoff/shiftandoffsummary/shiftandofftransactionend', methods=['POST','GET'])
def employeeShiftAndOffTransactionEnd():
    return render_template('employee/shiftAndOffTransactionEnd.html')
    # บันทึกลง table transaction

@employee.route('/employee/edit/addemployee/addemployeesummary/addemployeetransactionend', methods=['POST','GET'])
def employeeAddEmployeeTransactionEnd():
    return render_template('employee/addEmployeeTransactionEnd.html')
    # บันทึกลง table transaction


# @employee.route('/user/<name>')
# def create_user(name):
#     user = User(name=name)
#     db.session.add(user)
#     db.session.commit()

#     return 'User created !!'
