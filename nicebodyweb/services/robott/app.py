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

# Recipes_image_path = ""
# user_image_path = ""
# Recipes_image_path = "http://127.0.0.1:5000/static/images/openai"
# user_image_path = "http://127.0.0.1:5000/static/images/userImage"

#生成食譜
@robott_bp.route('/generateRecipes')
def robott_selfList():
    connection = db.get_connection() 

    cursor = connection.cursor()     
    cursor.execute('SELECT title, TO_CHAR(create_time, \'MM.DD.YYYY\') as "create_time", summary, "cookImage", "isPublish" FROM body."Cookbook" where "Uid" =1 order by "Cookid" desc;')

    data = cursor.fetchall()

    connection.close()
    return render_template('/robott/generateRecipes.html', data=data, Recipes_image_path=Recipes_image_path)



#食譜天地
@robott_bp.route('/recipeWorld')
def robott_everyList():
    connection = db.get_connection() 

    cursor = connection.cursor()     
    cursor.execute('select * from body."v_recipeWorld" order by create_time desc;')

    data = cursor.fetchall()

    connection.close()
    return render_template('/robott/recipeWorld.html', data=data, Recipes_image_path=Recipes_image_path, user_image_path = user_image_path)


#生成食譜 > 了解更多 & 食譜天地 > 了解更多
@robott_bp.route('/detailedRecipe')
def robott_selfList_more(): 
    #取得資料庫連線 
    connection = db.get_connection() 
    
    #產生執行sql命令的物件, 再執行sql   
    cursor = connection.cursor()     
    cursor.execute('SELECT title, TO_CHAR(create_time, \'MM.DD.YYYY\'), summary, "prepare", "cookTime", "cookStep", nutrition, "cookImage", "isPublish" FROM body."Cookbook" where "Cookid" =1;')
    
    #取出資料
    data = cursor.fetchone()
    #關閉資料庫連線    
    connection.close()

    return render_template('/robott/detailedRecipe.html', data=data)

#發佈食譜
@robott_bp.route('/shareResults')
def robott_share():
    return render_template('/robott/shareResults.html', data='王小明')