from .__init__ import director
from ..extensions import db, yag
from flask import render_template, redirect, url_for, request, session
import datetime;

# Director start page
@director.route('/director')
def directorLoginPage():
    line_id = request.args.get("userId")

    if line_id is None:
        session['line_id'] = None
        return render_template('director/welcome.html')

    toString = str(line_id)
    session['line_id'] = toString # send line_id to other page
    
    cur = db.connection.cursor()
    query = "SELECT director_name FROM director inner join directorInfo on director.director_id = directorInfo.director_id WHERE line_id = " + "'" + toString + "'"
    cur.execute(query)
    first_name = cur.fetchall()
    query = "SELECT director_lastname FROM director inner join directorInfo on director.director_id = directorInfo.director_id WHERE line_id = " + "'" + toString + "'"
    cur.execute(query)
    last_name = cur.fetchall()
    query = "SELECT director_id FROM director WHERE line_id = " + "'" + toString + "'"
    cur.execute(query)
    director_id = cur.fetchall() 
    cur.execute("SELECT director_section FROM directorInfo WHERE director_id=%s", [director_id[0][0]])
    director_section = cur.fetchall()

    cur.close()

    if bool(first_name) == False and bool(last_name) == False:
        session['first_name'] = "userNotFound" # send first_name to other page
        return render_template('director/welcome.html')

    session['first_name'] = first_name # send first_name to other page
    session['last_name'] = last_name # send last_name to other page
    session['director_id'] = director_id[0][0] # send last_name to other page
    session['director_section'] = director_section[0][0]

    return render_template('director/welcome.html')


# Director home page
@director.route('/director/home', methods=['POST','GET'])
def directorPage():
    line_id = session.get("line_id") # in case for query
        
    if line_id is None or session.get("first_name") == "userNotFound":
        return render_template('director/warning.html')
    else:
        return render_template('director/director.html', first_name=session.get("first_name"), last_name=session.get("last_name"))
    # return render_template('director/director.html')


# Director see pending shift and off work transaction
@director.route('/director/status/pending', methods=['POST','GET'])
def pending():
    line_id = session.get("line_id") # in case for query
    director_id = session.get("director_id")
        
    if line_id is None or session.get("first_name") == "userNotFound":
        return render_template('director/warning.html')
        
    elif request.method == 'POST':
        if request.form['select'] == "ChangeWork":
            if request.form['choose'] == "update":
                transactionChangeWork_id = request.form['transactionChangeWork_id']
                transactionChangeWork_TimeStamp = request.form['transactionChangeWork_TimeStamp']
                
                cur = db.connection.cursor()
                cur.execute("SELECT requestId FROM transactionChangeWork WHERE transactionChangeWork_id=%s",[transactionChangeWork_id])
                request_data = cur.fetchall()
                request_id = request_data[0][0]

                cur.execute("SELECT employee_name, employee_lastname, employee_email FROM employeeInfo WHERE employee_id=%s",[request_id])
                employee_data = cur.fetchall()
                employee_name = employee_data[0][0]
                employee_lastname = employee_data[0][1]
                employee_email = employee_data[0][2]

                cur.execute("SELECT director_name, director_lastname FROM directorInfo WHERE director_id=%s",[director_id])
                director_data = cur.fetchall()
                director_name = director_data[0][0]
                director_lastname = director_data[0][1]
                cur.close()

                current_time = datetime.datetime.now()
                TimeStamp = current_time.strftime("%Y-%m-%d")

                recipients = [employee_email]
                subject = 'ระบบมีการอนุมัติรายการเปลี่ยนรูปแบบการทำงานและวันหยุด'
                body = f'เรียน {employee_name} {employee_lastname},\n\nอีเมล์นี้เป็นอีเมล์อัตโนมัติทีส่งจากระบบ SCG-Schedule โปรดตรวจสอบรายการอนุมัติเปลี่ยนรูปแบบการทำงานและวันหยุด (จากคุณ {director_name} {director_lastname} เมื่อวันที่ {TimeStamp} กรุณาพิจารณารายการผ่านทางลิงก์ด้านล่าง http://127.0.0.1:5000\n\nด้วยความเคารพ,\n'
                yag.useralias = 'testbyNamhvam'
                yag.send(to=recipients,subject=subject,contents=[body])
                print ('ส่ง Email สำเร็จ')

                current_time = datetime.datetime.now()
                TimeStamp = current_time.strftime("%Y-%m-%d %H:%M:%S")
                status = "approve"

                cur = db.connection.cursor()
                cur.execute("UPDATE transactionChangeWork SET status2=%s, consider_time2=%s, TimeStamp=%s WHERE transactionChangeWork_id=%s",(status, TimeStamp, transactionChangeWork_TimeStamp, transactionChangeWork_id))
                db.connection.commit()
                cur.close()
                return redirect(url_for('director.pending'))

            elif request.form['choose'] == "delete":
                transactionChangeWork_id = request.form['transactionChangeWork_id']
                transactionChangeWork_TimeStamp = request.form['transactionChangeWork_TimeStamp']
                
                cur = db.connection.cursor()
                cur.execute("SELECT requestId FROM transactionChangeWork WHERE transactionChangeWork_id=%s",[transactionChangeWork_id])
                request_data = cur.fetchall()
                request_id = request_data[0][0]

                cur.execute("SELECT employee_name, employee_lastname, employee_email FROM employeeInfo WHERE employee_id=%s",[request_id])
                employee_data = cur.fetchall()
                employee_name = employee_data[0][0]
                employee_lastname = employee_data[0][1]
                employee_email = employee_data[0][2]

                cur.execute("SELECT director_name, director_lastname FROM directorInfo WHERE director_id=%s",[director_id])
                director_data = cur.fetchall()
                director_name = director_data[0][0]
                director_lastname = director_data[0][1]
                cur.close()

                current_time = datetime.datetime.now()
                TimeStamp = current_time.strftime("%Y-%m-%d")

                recipients = [employee_email]
                subject = 'ระบบมีการปฏิเสธรายการเปลี่ยนรูปแบบการทำงานและวันหยุด'
                body = f'เรียน {employee_name} {employee_lastname},\n\nอีเมล์นี้เป็นอีเมล์อัตโนมัติทีส่งจากระบบ SCG-Schedule โปรดตรวจสอบรายการปฏิเสธเปลี่ยนรูปแบบการทำงานและวันหยุด (จากคุณ {director_name} {director_lastname} เมื่อวันที่ {TimeStamp} กรุณาพิจารณารายการผ่านทางลิงก์ด้านล่าง http://127.0.0.1:5000\n\nด้วยความเคารพ,\n'
                yag.useralias = 'testbyNamhvam'
                yag.send(to=recipients,subject=subject,contents=[body])
                print ('ส่ง Email สำเร็จ')

                current_time = datetime.datetime.now()
                TimeStamp = current_time.strftime("%Y-%m-%d %H:%M:%S")
                status = "reject"

                cur = db.connection.cursor()
                cur.execute("UPDATE transactionChangeWork SET status2=%s, consider_time2=%s, TimeStamp=%s WHERE transactionChangeWork_id=%s",(status, TimeStamp, transactionChangeWork_TimeStamp, transactionChangeWork_id))
                db.connection.commit()
                cur.close()
                return redirect(url_for('director.pending'))

    else:
        cur = db.connection.cursor()
        transactionChangeWork_element = cur.execute("SELECT * FROM transactionChangeWork WHERE director_id=%s AND status2 IS NULL",[director_id])
        transactionChangeWork = cur.fetchall()

        return render_template('director/pending.html', first_name=session.get("first_name"), last_name=session.get("last_name"),
                    transactionChangeWork=transactionChangeWork,transactionChangeWork_element=transactionChangeWork_element)


# Director see approve transaction of themself
@director.route('/director/status/approve', methods=['POST','GET'])
def approve():
    line_id = session.get("line_id") # in case for query
    director_id = session.get("director_id")
        
    if line_id is None or session.get("first_name") == "userNotFound":
        return render_template('director/warning.html')
    else:
        cur = db.connection.cursor()
        transactionChangeWork_element = cur.execute("SELECT transactionChangeWork_id ,employee_id,employee_name ,employee_lastname ,date ,TimeStamp ,reason ,Status ,transactionChangeWork.approver_id ,consider_time1 ,consider_time2 ,transactionChangeWork.director_id ,Oldwork_type ,Newwork_type ,Oldoff_code ,Newoff_code ,section_code ,requestId ,status2, approver_name, approver_lastname, director_name, director_lastname FROM transactionChangeWork INNER JOIN approverInfo on transactionChangeWork.approver_id = approverInfo.approver_id INNER JOIN directorInfo on transactionChangeWork.director_id = directorInfo.director_id WHERE transactionChangeWork.director_id = " + "'" + director_id + "'" + " AND status2='approve'")
        transactionChangeWork = cur.fetchall()

        return render_template('director/approve.html', first_name=session.get("first_name"), last_name=session.get("last_name"),
                    transactionChangeWork=transactionChangeWork,transactionChangeWork_element=transactionChangeWork_element)
