# 匯入Blueprint模組
import logging
from flask import render_template
from flask import Blueprint
from flask import request

from utils import db

#檢查上傳檔案類型
# def allowed_file(filename):
#     return '.' in filename and filename.rsplit('.', 1)[1].lower() in ('png', 'jpg', 'jpeg', 'gif')

# 產生機器人服務藍圖
robott_bp = Blueprint('robott_bp', __name__)

#--------------------------
# 在機器人服務藍圖加入路由
#--------------------------

Recipes_image_path = "http://127.0.0.1:5000/static/images/openai"
user_image_path = "http://127.0.0.1:5000/static/images/userImage"

logging.basicConfig(level=logging.DEBUG)

#生成食譜
@robott_bp.route('/generateRecipes')
def robott_selfList():
    connection = db.get_connection() 

    cursor = connection.cursor()     
    cursor.execute('SELECT title, TO_CHAR(create_time, \'MM.DD.YYYY\') as "create_time", summary, "cookImage", "isPublish", diet, "Cookid" FROM body."cookbook" where "Uid" =1 order by "Cookid" desc;')

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
@robott_bp.route('/detailedRecipe', methods=['GET'])
def robott_selfList_more(): 
    #取得資料庫連線 
    connection = db.get_connection() 
    
    #產生執行sql命令的物件, 再執行sql   
    cursor = connection.cursor()     

    recipe_id = request.args.get('recipe_id')

    cursor.execute('SELECT title, TO_CHAR(create_time, \'MM.DD.YYYY\'), summary, "prepare", "cookTime", "cookStep", nutrition, "cookImage", "isPublish", diet, "prepareMoney" FROM body."cookbook" where "Cookid" =%s', (recipe_id,))
    
    #取出資料
    data = cursor.fetchone()
    #關閉資料庫連線    
    connection.close()

    return render_template('/robott/detailedRecipe.html', data=data, Recipes_image_path=Recipes_image_path)

#發佈食譜
@robott_bp.route('/shareResults', methods=['GET'])
def robott_share():
    connection = db.get_connection() 
    
    cursor = connection.cursor()     

    recipe_id = request.args.get('recipe_id')
    likecount = request.args.get('likecount')
    messagecount = request.args.get('messagecount')

    cursor.execute('SELECT title, TO_CHAR(create_time, \'MM.DD.YYYY\'), summary, "prepare", "cookTime", "cookStep", nutrition, "cookImage", diet, "prepareMoney" FROM body."cookbook" where "Cookid" =%s', (recipe_id,))

    data = cursor.fetchone()

    cursor.execute('select * from body."v_shareResults" where "Cookid" =%s order by create_time desc;', (recipe_id,))

    data2 = cursor.fetchall()

    connection.close()

    return render_template('/robott/shareResults.html', data=data, data2=data2, Recipes_image_path=Recipes_image_path, user_image_path=user_image_path, likecount=likecount, messagecount=messagecount)