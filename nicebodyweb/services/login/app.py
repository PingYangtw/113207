# 匯入Blueprint模組
from flask import render_template
from flask import Blueprint

# 產生目標服務藍圖
login_bp = Blueprint('login_bp', __name__)

#--------------------------
# 在目標服務藍圖加入路由
#--------------------------

#任務頁面
@login_bp.route('/loginPage')
def login_page(): 
    return render_template('/home/login.html', data='王小明')