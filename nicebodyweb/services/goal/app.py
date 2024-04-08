# 匯入Blueprint模組
from flask import render_template
from flask import Blueprint

# 產生目標服務藍圖
goal_bp = Blueprint('goal_bp', __name__)

#--------------------------
# 在目標服務藍圖加入路由
#--------------------------

#目標主頁
@goal_bp.route('/goalMain')
def goal_main(): 
    return render_template('/goal/goalMain.html', data='王小明')


#打卡目標列表
@goal_bp.route('/checkList')
def check_list(): 
    return render_template('/goal/checkList.html', data='王小明')


#體重紀錄列表
@goal_bp.route('/weightList')
def weight_list(): 
    return render_template('/goal/weightList.html', data='王小明')