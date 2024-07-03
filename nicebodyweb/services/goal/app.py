# 匯入Blueprint模組
import re
from flask import jsonify, render_template, session, request, jsonify, Blueprint
from utils import db

# 產生目標服務藍圖
goal_bp = Blueprint('goal_bp', __name__)

#--------------------------
# 在目標服務藍圖加入路由
#--------------------------

@goal_bp.route('/goalMain', methods=['GET', 'POST'])
def goal_main(): 
    if "google_id" in session:
        name=session['name']
        uid=session['uid']
        userImage=session['user_image']
    else:
        name='0'
        uid='1'
        userImage='0'

    if request.method == 'POST':
        try:
            data = request.json
            isChecked = data.get('checked')
            goalId = data.get('id')

            if isChecked is None or goalId is None:
                return jsonify({'error': 'Invalid request data.'}), 400

            connection = db.get_connection() 
            cursor = connection.cursor()

            if isChecked:
                cursor.execute("INSERT INTO body.\"checkIn\"(\"ChCategoryid\", create_time) VALUES(%s, now())", (goalId,))
                response = {'message': f'checkIn {goalId} inserted successfully.'}
            else:
                cursor.execute("DELETE FROM body.\"checkIn\" WHERE \"ChCategoryid\" = %s", (goalId,))
                response = {'message': f'checkIn {goalId} deleted successfully.'}

            connection.commit()
            connection.close()

            return jsonify(response)
        except Exception as e:
            return jsonify({'error': str(e)}), 500
        
    else:
        try:
            connection = db.get_connection() 
            cursor = connection.cursor()     
            cursor.execute('SELECT "ChCategoryid", "checkName", "Iconid", "isCheck"  FROM body.v_check where "Uid" = %s order by create_time;', (uid,))
            data = cursor.fetchall()

            cursor.execute('SELECT COALESCE(weight, \'0\') from ('
                           'select "Wid", weight , date(create_time) as create_time '
                           'FROM body.weight as a where "Uid" = %s) as a '
                           'RIGHT JOIN ('
                           '    SELECT current_date - i AS create_time '
                           '    FROM generate_series(0, 6) AS t(i) '
                           ') as b '
                           'ON a.create_time = b.create_time '
                           'order by b.create_time;'
                           ,(uid,))
            weight = cursor.fetchall()
            weight = [item[0] for item in weight]
            weight = [float(w) for w in weight]
            print(weight)

            connection.close()
            return render_template('/goal/goalMain.html', data=data, weight=weight, name=name, userImage=userImage)
        except Exception as e:
            return jsonify({'error': str(e)}), 500

#新增 - 打卡目標
@goal_bp.route('/saveCheckbox', methods=['POST'])
def save_goal():
    uid=session['uid']

    if request.method == 'POST':
        try:
            data = request.get_json()

            icon_id = data['iconId']
            text = data['text']

            connection = db.get_connection() 
            cursor = connection.cursor()

            cursor.execute('INSERT INTO body."checkCategory"("checkName", "Uid", "Iconid", create_time, update_time) VALUES(%s, %s, %s, now(), now())', (text, uid, icon_id))
            response = {'message': f'saveCheckbox inserted successfully.'}

            connection.commit()
            connection.close()

            return jsonify(response)
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return jsonify({'error': str(e)}), 500
        
#修改 - 打卡目標
@goal_bp.route('/updateCheckbox', methods=['POST'])
def update_goal():
    uid=session['uid']

    if request.method == 'POST':
        try:
            data = request.get_json()

            icon_id = data['iconId']
            text = data['text']
            goal_id = data['id']

            connection = db.get_connection() 
            cursor = connection.cursor()

            cursor.execute('UPDATE body."checkCategory" SET "checkName"=%s, "Iconid"=%s, update_time=now() WHERE "Uid"=%s and "ChCategoryid"=%s;', (text, icon_id, uid, goal_id))
            response = {'message': f'updateCheckbox successfully.'}

            connection.commit()
            connection.close()

            return jsonify(response)
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return jsonify({'error': str(e)}), 500

#刪除 - 打卡目標
@goal_bp.route('/deleteCheckbox', methods=['POST'])
def delete_goal():
    uid=session['uid']

    if request.method == 'POST':
        try:
            data = request.get_json()

            goal_id = data['id']

            connection = db.get_connection() 
            cursor = connection.cursor()

            cursor.execute('DELETE FROM body."checkCategory" WHERE "Uid"=%s and "ChCategoryid"=%s;', (uid, goal_id,))
            response = {'message': f'deleteCheckbox successfully.'}

            connection.commit()
            connection.close()

            return jsonify(response)
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return jsonify({'error': str(e)}), 500

#打卡目標列表
@goal_bp.route('/checkList')
def check_list(): 
    if "google_id" in session:
        name=session['name']
        uid=session['uid']
        userImage=session['user_image']
    else:
        name='0'
        uid='1'
        userImage='0'

    connection = db.get_connection() 
    cursor = connection.cursor()     
    cursor.execute('SELECT "ChCategoryid", "checkName", "Iconid" FROM body."checkCategory" where "Uid" = %s order by create_time;', (uid,))
    data = cursor.fetchall()
    connection.close()   
    return render_template('/goal/checkList.html', data=data, name=name, userImage=userImage)

#體重紀錄列表
@goal_bp.route('/weightList')
def weight_list(): 
    if "google_id" in session:
        name=session['name']
        uid=session['uid']
        userImage=session['user_image']
    else:
        name='0'
        uid='0'
        userImage='0'
        
    connection = db.get_connection() 
    cursor = connection.cursor()     
    cursor.execute('SELECT "Wid", weight, TO_CHAR(create_time, \'YYYY/MM/DD\') FROM body.weight where "Uid"  = %s;', (uid,))
    data = cursor.fetchall()
    connection.close() 
    return render_template('/goal/weightList.html', data=data, name=name, userImage=userImage)

#新增 - 今日體重
@goal_bp.route('/saveTodayWeight', methods=['POST'])
def save_todayWeight():
    uid=session['uid']

    if request.method == 'POST':
        try:
            weight = request.form.get('weight')

            connection = db.get_connection() 
            cursor = connection.cursor()

            cursor.execute('INSERT INTO body.weight(weight, "Uid", create_time, update_time) VALUES(%s, %s, now(), now())', (weight, uid))
            response = {'message': f'deleteCheckbox successfully.'}
            
            connection.commit()
            connection.close()

            return jsonify(response)
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return jsonify({'error': str(e)}), 500
