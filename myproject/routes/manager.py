from .__init__ import manager
from ..extensions import db
from flask import render_template, redirect, url_for, request, session



@manager.route('/manager')
def managerPage():
    return render_template('manager/manager.html')

@manager.route('/manager/status/pending', methods=['POST','GET'])
def pending():
    return render_template('manager/pending.html')

@manager.route('/manager/status/approve', methods=['POST','GET'])
def approve():
    return render_template('manager/approve.html')

@manager.route('/manager/shift')
def chooseEditShift():
    return render_template('manager/editShift.html')

####################################################################################################

@manager.route('/manager/edit', methods=['POST','GET'])
def employeeShift():
    return render_template('manager/managerEdit.html')


@manager.route('/manager/edit/selflist', methods=['POST','GET'])
def editYourselfList():
    return render_template('manager/selfEditList.html')


@manager.route('/manager/edit/cowork', methods=['POST','GET'])
def editCowork():
    return render_template('manager/coworkEdit.html')
    # ถ้าคนเป็น 2 ให้รับค่าแค่ 2 แถวแรก ถ้า 3 คนให้เอาทั้ง 3 แถว ถ้าเลือก 2 คนใส่มาคนเดียวให้ซ้ำหน้าเดิม


@manager.route('/manager/edit/addshift', methods=['POST','GET'])
def editAddShift():
    return render_template('manager/addshiftEdit.html')


@manager.route('/manager/edit/shiftandoff', methods=['POST','GET'])
def chooseEditShiftAndOff():
    return render_template('manager/editShiftAndOff.html')


@manager.route('/manager/edit/shiftandoff/viewshift', methods=['POST','GET']) # แก้เป็นให้เข้าไปแก้ตาม <int:id> 
def viewShift():
    return render_template('manager/viewShift.html')


@manager.route('/manager/edit/shiftandoff/viewshiftonly', methods=['POST','GET']) 
def viewShiftOnly():
    return render_template('manager/viewShiftOnly.html')


@manager.route('/manager/edit/addemployee', methods=['POST','GET'])
def addEmployee():
    return render_template('manager/addEmployee.html')


####################################################################################################

@manager.route('/manager/edit/selflist/selflistsummary', methods=['POST','GET'])
def employeeSelfTransaction():
    return render_template('manager/selfEditListSummary.html')


@manager.route('/manager/edit/cowork/coworksummary', methods=['POST','GET'])
def employeeCoworkTransaction():
    return render_template('manager/coworkEditListSummary.html')


@manager.route('/manager/edit/addshift/addshiftsummary', methods=['POST','GET'])
def employeeAddShiftTransaction():
    return render_template('manager/addShiftEditListSummary.html')


@manager.route('/manager/edit/shiftandoff/shiftandoffsummary', methods=['POST','GET'])
def employeeShiftAndOffTransaction():
    return render_template('manager/shiftAndOffEditListSummary.html')


@manager.route('/manager/edit/addemployee/addemployeesummary', methods=['POST','GET'])
def employeeAddTransaction():
    return render_template('manager/addEmployeeEditListSummary.html')


####################################################################################################

@manager.route('/manager/status/pending/approvetransactionend', methods=['POST','GET'])
def managerApproveTransactionEnd():
    return render_template('manager/approveTransactionEnd.html')


@manager.route('/manager/edit/selflist/selflistsummary/selftransactionend', methods=['POST','GET'])
def employeeSelfTransactionEnd():
    return render_template('manager/selfTransactionEnd.html')


@manager.route('/manager/edit/cowork/coworksummary/coworktransactionend', methods=['POST','GET'])
def employeeCoworkTransactionEnd():
    return render_template('manager/coworkTransactionEnd.html')


@manager.route('/manager/edit/addshift/addshiftsummary/addshifttransactionend', methods=['POST','GET'])
def employeeAddShiftTransactionEnd():
    return render_template('manager/addShiftTransactionEnd.html')


@manager.route('/manager/edit/shiftandoff/shiftandoffsummary/shiftandofftransactionend', methods=['POST','GET'])
def employeeShiftAndOffTransactionEnd():
    return render_template('manager/shiftAndOffTransactionEnd.html')


@manager.route('/manager/edit/addemployee/addemployeesummary/addemployeetransactionend', methods=['POST','GET'])
def employeeAddEmployeeTransactionEnd():
    return render_template('manager/addEmployeeTransactionEnd.html')






# ทดลอง query ข้อมูล
@manager.route('/user/find/<int:id>')
def create_user(id):
    user = User.query.filter_by(id=id).first()
    name = user.name
    return name + " " + "จ้า"

# ทดลอง redirect ไปยังส่วน employee
@manager.route('/testjar')
def gojar():
    return redirect(url_for('employee.chooseEdit'))