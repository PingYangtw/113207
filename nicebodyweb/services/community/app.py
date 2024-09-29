# 匯入Blueprint模組
from datetime import datetime
import os
import random
import string
from urllib import response
from flask import render_template, session, Blueprint, request, jsonify
from utils import db

# 產生目標服務藍圖
community_bp = Blueprint('community_bp', __name__)

#--------------------------
# 在目標服務藍圖加入路由
#--------------------------

#社群主頁(母畫面)
@community_bp.route('/communityMain')
def community_Main(): 
    if "google_id" in session:
        name=session['name']
        userImage=session['user_image']
        uid=session['uid']
        is_nutritionist=session['is_nutritionist']
    else:
        name='0'
        userImage='0'
        uid='0'
        is_nutritionist='0'

    connection = db.get_connection()
    cursor = connection.cursor()

    cursor.execute('''
        SELECT a.*, 
            b."userImage" AS userProfileImage, 
            b.username, 
            c.message, 
            c.update_time, 
            c."Uid" AS answerUid,
            d."userImage" AS answerUserImage
        FROM body.question AS a
        LEFT JOIN body.user_profile AS b ON a."Uid" = b."Uid"
        LEFT JOIN body.answer AS c ON a."BestAid" = c."Aid"
        LEFT JOIN body.user_profile AS d ON c."Uid" = d."Uid"
        ORDER BY a.create_time DESC;
        '''
    )

    question = cursor.fetchall()

    cursor.execute('''
        select a."QKid", a."categoryName", b."Qid", COALESCE(keepCount, 0) from body."QnAKeepCategory" as a
        left join (select "QKid", STRING_AGG("Qid"::TEXT, ',') as"Qid", count(*) as keepCount from body."QnAKeep" group by "QKid" ) as b on a."QKid" = b."QKid" 
        where "Uid" = %s
        order by a.create_time''', (uid, )           
        )
    
    keep = cursor.fetchall()
    connection.close()

    for i, q in enumerate(question):
        # 構建資料夾的完整路徑
        if q[4]:
            base_folder = os.path.join('static/images/community', str(q[1]), q[4]) 
        
            # 如果資料夾存在，獲取所有的檔案名稱
            if os.path.exists(base_folder):
                image_files = os.listdir(base_folder)
                # 將檔案名稱清單加入到 question 中
                question[i] = q + (image_files,)
            else:
                # 資料夾不存在，則附加空清單
                question[i] = q + ([],)

    combined = []
    for _, _, numbers, _, in keep:
        if numbers:
            combined.extend(numbers.split(','))
    
    combined = list(dict.fromkeys(combined))

    keepCombined = ','.join(combined)

    return render_template('/community/communityMain.html', name=name, userImage=userImage, uid=uid, question=question, is_nutritionist=is_nutritionist, keep=keep, keepCombined=keepCombined)


#單一貼文(子畫面)
@community_bp.route('/detailedPost', methods=['GET'])
def detailed_post(): 
    if "google_id" in session:
        name=session['name']
        userImage=session['user_image']
        uid=session['uid']
        is_nutritionist=session['is_nutritionist']
    else:
        name='0'
        userImage='0'
        uid='0'
        is_nutritionist='0'
    
    connection = db.get_connection() 
    
    cursor = connection.cursor()     

    question_id = request.args.get('question_id')

    cursor.execute('''
        SELECT a.*, 
            b."userImage" AS userProfileImage, 
            b.username
        FROM body.question AS a
        LEFT JOIN body.user_profile AS b ON a."Uid" = b."Uid"
        WHERE a."Qid" = %s;
        ''', (question_id, )
    )

    question = cursor.fetchone()

    cursor.execute('''
        select a.*, b."userImage" from body.answer as a
        LEFT JOIN body.user_profile AS b ON a."Uid" = b."Uid"
        where a."Qid" = %s
        order by a.update_time desc;
        ''', (question_id, )
    )

    answer = cursor.fetchall()

    cursor.execute('''
        select a."QKid" , a."categoryName" , COALESCE(b."Qid", 0), COALESCE(keepCount, 0) from body."QnAKeepCategory" as a
        left join body."QnAKeep" as b
        on a."QKid"  = b."QKid" and b."Qid" = %s
        left join (select "QKid", count(*) as keepCount from body."QnAKeep" group by "QKid" ) as c on a."QKid"  = c."QKid" 
        where a."Uid" = %s
        order by a.create_time 
                   ''', (question_id, uid))
    
    keep = cursor.fetchall()

    connection.close()

    if question[4]:
        base_folder = os.path.join('static/images/community', str(question[1])) + '/' + question[4]
    
        # 如果資料夾存在，獲取所有的檔案名稱
        if os.path.exists(base_folder):
            image_files = os.listdir(base_folder)
            # 將檔案名稱清單加入到 question 中
            question = question + (image_files,)
        else:
            # 資料夾不存在，則附加空清單
            question = question + ([],)

    # 將 BestAid 放置在 answer 的第一個位置
    if question[5]:
        for i, ans in enumerate(answer):
            if str(ans[0]) == str(question[5]):
                best_answer = answer.pop(i)
                answer.insert(0, best_answer)
                break

    return render_template('/community/detailedPost.html', name=name, userImage=userImage, uid=uid, question=question, answer=answer, is_nutritionist=is_nutritionist, keep=keep)

#提問
@community_bp.route('/airecipePost', methods=['GET'])
def airecipe_post(): 
    if "google_id" in session:
        name=session['name']
        userImage=session['user_image']
        uid=session['uid']
    else:
        name='0'
        userImage='0'
        uid='0'

    return render_template('/community/airecipePost.html', name=name, userImage=userImage, uid=uid)

#提問編輯
@community_bp.route('/updatePost', methods=['GET'])
def update_post(): 
    if "google_id" in session:
        name=session['name']
        userImage=session['user_image']
        uid=session['uid']
    else:
        name='0'
        userImage='0'
        uid='0'
    
    connection = db.get_connection() 
    
    cursor = connection.cursor()     

    question_id = request.args.get('question_id')

    cursor.execute('''
        select a.* from body.question as a
        where a."Qid" = %s and a."Uid" = %s;
        ''', (question_id, uid)
    )

    question = cursor.fetchone()

    if question[4]:
        base_folder = os.path.join('static/images/community', str(question[1])) + '/' + question[4]
    
        # 如果資料夾存在，獲取所有的檔案名稱
        if os.path.exists(base_folder):
            image_files = os.listdir(base_folder)
            # 將檔案名稱清單加入到 question 中
            question = question + (image_files,)
        else:
            # 資料夾不存在，則附加空清單
            question = question + ([],)
    else:
        # 資料夾不存在，則附加空清單
        question = question + ([],)

    connection.close()
                   
    return render_template('/community/updatePost.html', name=name, userImage=userImage, uid=uid, question=question)

#檢舉
@community_bp.route('/report', methods=['POST'])
def report(): 
    uid=session['uid']

    if request.method == 'POST':
        try:
            connection = db.get_connection()
            cursor = connection.cursor()

            report_type = request.form.get('reasons')
            otherType = request.form.get('otherReason')
            qid = request.form.get('question_id')

            # 如果report_content是空的，則將其設為NULL
            if not otherType:
                otherType = None


            cursor.execute('''
                    INSERT INTO body.question_report ("Uid", "Qid", "reportType", "otherType", create_time)
                    VALUES (%s, %s, %s, %s, now());
                    ''', (uid, qid, report_type, otherType)
                )

            response = {'message': 'Reported successfully'}

            connection.commit()
            connection.close()

            return jsonify(response)
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return jsonify({'error': str(e)}), 500
        
# 收藏
@community_bp.route('/addCollect', methods=['POST'])
def add_collect(): 
    uid=session['uid']

    if request.method == 'POST':
        try:
            connection = db.get_connection()
            cursor = connection.cursor()

            qid = request.form.get('question_id')
            category_id = request.form.get('category_id')

            cursor.execute('INSERT INTO body."QnAKeep" ("Qid", "QKid", create_time, update_time) VALUES (%s, %s, now(), now());', (qid, category_id))
            response = {'message': f'addCollect successfully.'}

            response = {'message': 'Collected successfully'}

            connection.commit()
            connection.close()

            return jsonify(response)
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return jsonify({'error': str(e)}), 500
        
# 取消收藏
@community_bp.route('/subCollect', methods=['POST'])
def sub_collect(): 
    uid=session['uid']

    if request.method == 'POST':
        try:
            connection = db.get_connection()
            cursor = connection.cursor()

            qid = request.form.get('question_id')
            category_id = request.form.get('category_id')

            cursor.execute('DELETE FROM body."QnAKeep" WHERE "Qid" = %s AND "QKid" = %s;', (qid, category_id))
            response = {'message': f'subCollect successfully.'}

            response = {'message': 'UnCollected successfully'}

            connection.commit()
            connection.close()

            return jsonify(response)
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return jsonify({'error': str(e)}), 500
        
# 發佈
@community_bp.route('/postQuestion', methods=['POST'])
def post_question():
    uid=session['uid']

    if request.method == 'POST':
        try:
            title = request.form.get('title')
            content = request.form.get('content')
            files = request.files.getlist('files[]')

            nowtime = datetime.now()
            create_time = nowtime.strftime("%Y-%m-%d %H:%M:%S")
            create_time_str = create_time.replace(" ", "_").replace(":", "-")

            if files != []:
                # 檢查資料夾是否存在，若不存在則創建
                base_path = "static/images/community/"
                uid_folders = [d for d in os.listdir(base_path) if d.startswith(str(uid))]
                
                if uid_folders:
                    folder_path_uid = os.path.join(base_path, uid_folders[0])  # 返回找到的第一個資料夾
                    folder_name = uid_folders[0]
                else:
                    # 創建唯一的資料夾
                    folder_path_uid = os.path.join(base_path, str(uid))
                    os.makedirs(folder_path_uid)

                nowtime = datetime.now()
                create_time = nowtime.strftime("%Y-%m-%d %H:%M:%S")
                create_time_str = create_time.replace(" ", "_").replace(":", "-")
                    
                random_str = ''.join(random.choices(string.ascii_letters + string.digits, k=16))
                folder_name = f"{uid}_{create_time_str}_{random_str}"
                folder_path = os.path.join(base_path, str(uid), folder_name)
                os.makedirs(folder_path)

                for index, file in enumerate(files, start=1):
                    if file and file.filename:
                        # 在檔案名稱前面加上迴圈數，並用 "_" 分隔
                        new_filename = f"{index}_{file.filename}"
                        file.save(os.path.join(folder_path, new_filename))
            else:
                folder_name = None

            connection = db.get_connection()
            cursor = connection.cursor()

            cursor.execute('''
                INSERT INTO body.question
                ("Uid", title, "content", question_image, "BestAid", create_time, update_time)
                VALUES(%s, %s, %s, %s, null, %s, %s);
                ''', (uid, title, content, folder_name, create_time, create_time))
            
            # cursor.execute('''
            #     SELECT "Qid" FROM body.question 
            #     where "Uid" = %s and create_time = %s
            #     LIMIT 1;''', (uid, create_time))
            
            # Qid = cursor.fetchone()[0]

            response = {'message': 'Question posted successfully.'}
            connection.commit()
            connection.close()

            return jsonify(response)
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return jsonify({'error': str(e)}), 500

#編輯發佈
@community_bp.route('/updateQuestion', methods=['POST'])
def update_question():
    uid=session['uid']

    if request.method == 'POST':
        try:
            title = request.form.get('title')
            content = request.form.get('content')
            qid = request.form.get('Qid')
            folderName = request.form.get('folderName')
            files = request.files.getlist('files[]')

            base_path = "static/images/community/"

            print(folderName, files)

            if folderName=='None' and files:
                # 檢查資料夾是否存在，若不存在則創建
                base_path = "static/images/community/"
                uid_folders = [d for d in os.listdir(base_path) if d.startswith(str(uid))]
                
                if uid_folders:
                    folder_path_uid = os.path.join(base_path, uid_folders[0])  # 返回找到的第一個資料夾
                    folder_name = uid_folders[0]
                else:
                    # 創建唯一的資料夾
                    folder_path_uid = os.path.join(base_path, str(uid))
                    os.makedirs(folder_path_uid)

                nowtime = datetime.now()
                create_time = nowtime.strftime("%Y-%m-%d %H:%M:%S")
                create_time_str = create_time.replace(" ", "_").replace(":", "-")
                
                random_str = ''.join(random.choices(string.ascii_letters + string.digits, k=16))
                folderName = f"{uid}_{create_time_str}_{random_str}"
                folder_path = os.path.join(base_path, str(uid), folderName)
                os.makedirs(folder_path)

            if folderName!='None': 
                folder_path = os.path.join(base_path, str(uid), folderName)

                # 清空檔案，但是保留跟files裡面的檔案名稱一樣的檔案
                for file in os.listdir(folder_path):
                    if file not in [f.filename for f in files]:
                        os.remove(os.path.join(folder_path, file))

                # 取得資料夾中的所有檔案名稱
                existing_files = set(os.listdir(folder_path))
                
                print(existing_files)

                # 新增新的檔案
                for index, file in enumerate(files, start=1):

                    random_str = ''.join(random.choices(string.ascii_letters + string.digits, k=16))

                    new_filename = f"{index}_{random_str}.jpg"

                    if file.filename not in existing_files:  # 檢查檔案是否已存在
                        print(file.filename)
                        file.save(os.path.join(folder_path, new_filename))
                        existing_files.add(new_filename)  # 更新存在的檔案列表

            connection = db.get_connection()
            cursor = connection.cursor()

            cursor.execute('''
                UPDATE body.question 
                SET title = %s, "content" = %s, update_time = now(), question_image = %s
                WHERE "Qid" = %s and "Uid" = %s;
                ''', (title, content, folderName, qid, uid))

            response = {'message': 'Question posted successfully.'}
            connection.commit()
            connection.close()

            return jsonify(response)
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return jsonify({'error': str(e)}), 500


# 刪除
@community_bp.route('/deleteQuestion', methods=['POST'])
def delete_question():
    uid=session['uid']

    if request.method == 'POST':
        try:
            connection = db.get_connection()
            cursor = connection.cursor()

            qid = request.form.get('question_id')

            cursor.execute('''
                DELETE FROM body.question
                WHERE "Qid" = %s;
                ''', (qid, ))
            
            response = {'message': 'Question deleted successfully.'}
            connection.commit()
            connection.close()

            return jsonify(response)
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return jsonify({'error': str(e)}), 500

# 收藏
@community_bp.route('addCollect', methods=['POST'])
def robott_addCollect():
    uid=session['uid']

    if request.method == 'POST':
        try:
            question_id = request.form.get('question_id')
            category_id = request.form.get('category_id')

            connection = db.get_connection() 
            cursor = connection.cursor()

            cursor.execute('INSERT INTO body."QnAKeep" ("Qid", "QKid", create_time, update_time) VALUES (%s, %s, now(), now());', (question_id, category_id))
            response = {'message': f'addCollect successfully.'}

            connection.commit()
            connection.close()

            return jsonify(response)
        except Exception as e:
            return jsonify({'error': str(e)}), 500
        
# 取消收藏
@community_bp.route('subCollect', methods=['POST'])
def robott_subCollect():
    uid=session['uid']

    if request.method == 'POST':
        try:
            question_id = request.form.get('question_id')
            category_id = request.form.get('category_id')

            connection = db.get_connection() 
            cursor = connection.cursor()

            cursor.execute('DELETE FROM body."QnAKeep" WHERE "Qid"=%s and "QKid"=%s;', (question_id, category_id))
            response = {'message': f'subCollect successfully.'}

            connection.commit()
            connection.close()

            return jsonify(response)
        except Exception as e:
            return jsonify({'error': str(e)}), 500
        
# 留言
@community_bp.route('addAnswer', methods=['POST'])
def robott_addAnswer():
    uid=session['uid']

    if request.method == 'POST':
        try:
            question_id = request.form.get('question_id')
            content = request.form.get('message')

            connection = db.get_connection() 
            cursor = connection.cursor()

            cursor.execute('INSERT INTO body.answer ("Qid", "Uid", message, create_time, update_time) VALUES (%s, %s, %s, now(), now());', (question_id, uid, content))
            response = {'message': f'addAnswer successfully.'}

            connection.commit()
            connection.close()

            return jsonify(response)
        except Exception as e:
            return jsonify({'error': str(e)}), 500
        
# 設為最佳解
@community_bp.route('setBestAnswer', methods=['POST'])
def robott_setBestAnswer():
    uid=session['uid']

    if request.method == 'POST':
        try:
            question_id = request.form.get('question_id')
            answer_id = request.form.get('answer_id')

            connection = db.get_connection() 
            cursor = connection.cursor()

            cursor.execute('UPDATE body.question SET "BestAid"=%s WHERE "Qid"=%s;', (answer_id, question_id))
            response = {'message': f'setBestAnswer successfully.'}

            connection.commit()
            connection.close()

            return jsonify(response)
        except Exception as e:
            return jsonify({'error': str(e)}), 500