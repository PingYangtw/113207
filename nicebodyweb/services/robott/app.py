# 匯入Blueprint模組
import logging
from flask import jsonify, render_template, session, Blueprint, request

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


#生成食譜
@robott_bp.route('/generateRecipes')
def robott_selfList():
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
    cursor.execute('SELECT title, TO_CHAR(create_time, \'MM.DD.YYYY\') as "create_time", summary, "cookImage", "isPublish", diet, "Cookid" FROM body."cookbook" where "Uid" =%s order by "Cookid" desc;', (uid,))

    data = cursor.fetchall()

    connection.close()
    return render_template('/robott/generateRecipes.html', data=data, Recipes_image_path=Recipes_image_path, name=name, userImage=userImage, uid=uid)



#食譜天地
@robott_bp.route('/recipeWorld')
def robott_everyList():
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
    cursor.execute('select title, a.update_time, summary, "cookImage", likecount, messagecount, "userImage", diet, a."Cookid", "cookTime", "prepareMoney", a."Uid", COALESCE(b."Uid", 0) as cookbookLike, cookbookStar from body."v_recipeWorld" as a left join (SELECT * FROM body."cookbookLike" where "Uid"=%s) as b on a."Cookid" = b."Cookid" order by a.update_time desc, a."Cookid" desc;', (uid,))

    data = cursor.fetchall()

    connection.close()
    return render_template('/robott/recipeWorld.html', data=data, Recipes_image_path=Recipes_image_path, user_image_path = user_image_path, name=name, userImage=userImage, uid=uid)


#生成食譜 > 了解更多 & 食譜天地 > 了解更多
@robott_bp.route('/detailedRecipe', methods=['GET', 'POST'])
def robott_selfList_more(): 
    if "google_id" in session:
        name=session['name']
        userImage=session['user_image']
        uid=session['uid']
    else:
        name='0'
        userImage='0'
        uid='0'

    if request.method == 'POST':
        try:
            data = request.get_json()

            recipe_id = data['id']
            connection = db.get_connection() 
            cursor = connection.cursor()

            cursor.execute('UPDATE body."cookbook" SET "isPublish"=1, update_time=now() WHERE "Cookid"=%s;', (recipe_id,))
            response = {'message': f'update successfully.'}

            connection.commit()
            connection.close()

            return jsonify(response)
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    else:
        try:    
            connection = db.get_connection() 
            cursor = connection.cursor()     
            recipe_id = request.args.get('recipe_id')
            cursor.execute('SELECT title, TO_CHAR(create_time, \'MM.DD.YYYY\'), summary, "prepare", "cookTime", "cookStep", nutrition, "cookImage", "isPublish", diet, "prepareMoney", "Cookid" FROM body."cookbook" where "Cookid" =%s', (recipe_id,))
            data = cursor.fetchone()
            connection.close()

            return render_template('/robott/detailedRecipe.html', data=data, Recipes_image_path=Recipes_image_path, name=name, userImage=userImage, uid=uid)
        except Exception as e:
            return jsonify({'error': str(e)}), 500
        
#發佈食譜
@robott_bp.route('/shareResults', methods=['GET'])
def robott_share():
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

    recipe_id = request.args.get('recipe_id')

    cursor.execute('select title, a.create_time, summary, "prepare", "cookTime", "cookStep", nutrition, "cookImage", diet, "prepareMoney", a."Cookid", a."Uid", COALESCE(b."Uid", 0) as cookbookLike, likecount, messagecount, cookbookStar from (SELECT title, create_time, summary, "prepare", "cookTime", "cookStep", nutrition, "cookImage", diet, "prepareMoney", "Cookid", "Uid", likecount, messagecount, cookbookStar FROM body."v_recipeWorld" where "Cookid" = %s) as a left join (SELECT * FROM body."cookbookLike" where "Uid" = %s) as b on a."Cookid" = b."Cookid"', (recipe_id, uid))

    data = cursor.fetchone()

    cursor.execute('select * from body."v_shareResults" where "Cookid" =%s;', (recipe_id,))

    data2 = cursor.fetchall()

    cursor.execute('''
        select a."CKid" , a."categoryName" , COALESCE(b."Cookid", 0), COALESCE(keepCount, 0) from body."CookKeepCategory" as a
        left join body."CookKeep" as b
        on a."CKid"  = b."CKid" and b."Cookid" = %s
        left join (select "CKid", count(*) as keepCount from body."CookKeep" group by "CKid" ) as c on a."CKid"  = c."CKid" 
        where a."Uid" = %s
        order by a.create_time 
                   ''', (recipe_id, uid))
    
    data3 = cursor.fetchall()

    connection.close()

    has_non_zero = any(d[2] != 0 for d in data3)

    return render_template('/robott/shareResults.html', data=data, data2=data2, data3=data3, Recipes_image_path=Recipes_image_path, user_image_path=user_image_path, name=name, userImage=userImage, has_non_zero=has_non_zero, uid=uid)

#發佈食譜 - 按讚
@robott_bp.route('/likeAdd', methods=['POST'])
def robott_likeAdd():
    uid=session['uid']

    if request.method == 'POST':
        try:
            recipe_id = request.form.get('recipe_id')

            connection = db.get_connection() 
            cursor = connection.cursor()

            cursor.execute('INSERT INTO body."cookbookLike" ("Cookid", "Uid", create_time) VALUES (%s, %s, now());', (recipe_id, uid))
            response = {'message': f'likeAdd successfully.'}

            connection.commit()
            connection.close()

            return jsonify(response)
        except Exception as e:
            return jsonify({'error': str(e)}), 500
        
#發佈食譜 - 取消讚
@robott_bp.route('/likeSub', methods=['POST'])
def robott_likeSub():
    uid=session['uid']

    if request.method == 'POST':
        try:
            recipe_id = request.form.get('recipe_id')

            connection = db.get_connection() 
            cursor = connection.cursor()

            cursor.execute('DELETE FROM body."cookbookLike" WHERE "Cookid"=%s and "Uid"=%s;', (recipe_id, uid))
            response = {'message': f'likeSub successfully.'}

            connection.commit()
            connection.close()

            return jsonify(response)
        except Exception as e:
            return jsonify({'error': str(e)}), 500
        
#發佈食譜 - 收藏
@robott_bp.route('addCollect', methods=['POST'])
def robott_addCollect():
    uid=session['uid']

    if request.method == 'POST':
        try:
            recipe_id = request.form.get('recipe_id')
            category_id = request.form.get('category_id')

            connection = db.get_connection() 
            cursor = connection.cursor()

            print(recipe_id, category_id)
            cursor.execute('INSERT INTO body."CookKeep" ("Cookid", "CKid", create_time, update_time) VALUES (%s, %s, now(), now());', (recipe_id, category_id))
            response = {'message': f'addCollect successfully.'}

            connection.commit()
            connection.close()

            return jsonify(response)
        except Exception as e:
            return jsonify({'error': str(e)}), 500
        
#發佈食譜 - 取消收藏
@robott_bp.route('subCollect', methods=['POST'])
def robott_subCollect():
    uid=session['uid']

    if request.method == 'POST':
        try:
            recipe_id = request.form.get('recipe_id')
            category_id = request.form.get('category_id')

            connection = db.get_connection() 
            cursor = connection.cursor()

            cursor.execute('DELETE FROM body."CookKeep" WHERE "Cookid"=%s and "CKid"=%s;', (recipe_id, category_id))
            response = {'message': f'subCollect successfully.'}

            connection.commit()
            connection.close()

            return jsonify(response)
        except Exception as e:
            return jsonify({'error': str(e)}), 500
        
#發佈食譜 - 食譜品質
@robott_bp.route('/comment', methods=['POST'])
def robott_comment():
    uid=session['uid']

    if request.method == 'POST':
        try:
            recipe_id = request.form.get('recipe_id')
            message = request.form.get('message')
            star = request.form.get('star')


            connection = db.get_connection() 
            cursor = connection.cursor()

            cursor.execute('INSERT INTO body."cookbookMessage" ("Cookid", "Uid", "message", star, create_time, update_time) VALUES (%s, %s, %s, %s, now(), now());', (recipe_id, uid, message, star))
            response = {'message': f'comment successfully.'}

            connection.commit()
            connection.close()

            return jsonify(1)
        except Exception as e:
            return jsonify({'error': str(e)}), 500