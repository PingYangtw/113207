# 匯入Blueprint模組
from flask import jsonify, render_template
from flask import Blueprint
from flask import request


from utils import db

# 產生目標服務藍圖
goal_bp = Blueprint('goal_bp', __name__)

#--------------------------
# 在目標服務藍圖加入路由
#--------------------------

from flask import request, jsonify

@goal_bp.route('/goalMain', methods=['GET', 'POST'])
def goal_main(): 
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
            cursor.execute('SELECT "ChCategoryid", "checkName", "Iconid", "isCheck"  FROM body.v_check where "Uid" = 1 order by create_time;')
            data = cursor.fetchall()
            connection.close()
            return render_template('/goal/goalMain.html', data=data)
        except Exception as e:
            return jsonify({'error': str(e)}), 500

#打卡目標新增
@goal_bp.route('/saveCheckbox', methods=['POST'])
def save_goal():
    if request.method == 'POST':
        try:
            data = request.get_json()

            icon_id = data['iconId']
            text = data['text']

            connection = db.get_connection() 
            cursor = connection.cursor()

            cursor.execute('INSERT INTO body."checkCategory"("checkName", "Uid", "Iconid", create_time, update_time) VALUES(%s, 1, %s, now(), now())', (text, icon_id))
            response = {'message': f'saveCheckbox inserted successfully.'}

            connection.commit()
            connection.close()

            return jsonify(response)
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return jsonify({'error': str(e)}), 500

#打卡目標列表
@goal_bp.route('/checkList')
def check_list(): 
    connection = db.get_connection() 
    cursor = connection.cursor()     
    cursor.execute('SELECT "ChCategoryid", "checkName", "Iconid" FROM body."checkCategory" where "Uid" = 1 order by create_time;')
    data = cursor.fetchall()
    connection.close()   
    return render_template('/goal/checkList.html', data=data)

#體重紀錄列表
@goal_bp.route('/weightList')
def weight_list(): 
    return render_template('/goal/weightList.html', data='王小明')