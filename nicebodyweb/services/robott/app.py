# 匯入Blueprint模組
from flask import render_template
from flask import Blueprint

from utils import db

#檢查上傳檔案類型
# def allowed_file(filename):
#     return '.' in filename and filename.rsplit('.', 1)[1].lower() in ('png', 'jpg', 'jpeg', 'gif')

# 產生機器人服務藍圖
robott_bp = Blueprint('robott_bp', __name__)

#--------------------------
# 在機器人服務藍圖加入路由
#--------------------------

#生成食譜
@robott_bp.route('/generateRecipes')
def robott_selfList(): 
    return render_template('/robott/generateRecipes.html')


#食譜天地
@robott_bp.route('/recipeWorld')
def robott_everyList(): 
    return render_template('/robott/recipeWorld.html')


#生成食譜 > 了解更多 & 食譜天地 > 了解更多
@robott_bp.route('/detailedRecipe')
def robott_selfList_more(): 
    #取得資料庫連線 
    connection = db.get_connection() 
    
    #產生執行sql命令的物件, 再執行sql   
    cursor = connection.cursor()     
    cursor.execute('SELECT cusno FROM public.customer limit 1;')
    
    #取出資料
    data = cursor.fetchall()
    #關閉資料庫連線    
    connection.close()

    return render_template('/robott/detailedRecipe.html', data=data)

#發佈食譜
@robott_bp.route('/shareResults')
def robott_share(): 
    return render_template('/robott/shareResults.html')