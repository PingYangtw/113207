# 匯入Blueprint模組
from flask import render_template
from flask import Blueprint

# 產生目標服務藍圖
task_bp = Blueprint('task_bp', __name__)

#--------------------------
# 在目標服務藍圖加入路由
#--------------------------

#任務頁面
@task_bp.route('/taskPage')
def task_page(): 
    return render_template('/task/taskPage.html', data='王小明')