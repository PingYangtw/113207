# 匯入Blueprint模組
import os
import threading
import time
import json
import urllib.request
import azure.cognitiveservices.speech as speechsdk
from flask import jsonify, render_template, session, Blueprint, request
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from openai import OpenAI
from utils import db

#檢查上傳檔案類型
# def allowed_file(filename):
#     return '.' in filename and filename.rsplit('.', 1)[1].lower() in ('png', 'jpg', 'jpeg', 'gif')

# 產生機器人服務藍圖
robott_bp = Blueprint('robott_bp', __name__)

#--------------------------
# 在機器人服務藍圖加入路由
#--------------------------

Recipes_image_path = "/static/images/openai"
user_image_path = "/static/images/userImage"


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
    cursor.execute('''
        SELECT title, TO_CHAR(a.create_time, \'MM.DD.YYYY\') as "create_time", summary, "cookImage", "isPublish", a.diet, "Cookid", b."isNutritionist" 
        FROM body."cookbook" as a
        left join body.user_profile as b 
        on a."Uid"  = b."Uid" 
        where a."Uid" =%s order by "Cookid" desc;
        ''', (uid,))

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
    cursor.execute('select title, a.update_time, summary, "cookImage", likecount, messagecount, "userImage", diet, a."Cookid", "cookTime", "prepareMoney", a."Uid", COALESCE(b."Uid", 0) as cookbookLike, cookbookStar, "isNutritionist" from body."v_recipeWorld" as a left join (SELECT * FROM body."cookbookLike" where "Uid"=%s) as b on a."Cookid" = b."Cookid" order by a.update_time desc, a."Cookid" desc;', (uid,))

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
            cursor.execute('SELECT title, TO_CHAR(create_time, \'MM.DD.YYYY\'), summary, "prepare", "cookTime", "cookStep", nutrition, "cookImage", "isPublish", diet, "prepareMoney", "Cookid", "cookStep_mp3" FROM body."cookbook" where "Cookid" =%s', (recipe_id,))
            data = cursor.fetchone()

            # 獲取前 7 個最喜歡的食譜
            cursor.execute('''
                WITH first_query AS (
                    SELECT "cookImage", title, "Cookid" 
                    FROM body."v_recipeWorld" 
                    WHERE main_req = (SELECT main_req FROM body.cookbook WHERE "Cookid" = %s) 
                    AND "Cookid" != %s
                    ORDER BY likecount DESC
                    LIMIT 7
                )

                SELECT * FROM first_query

                UNION ALL

                -- 只在 first_query 的結果少於 7 筆時從這裡補足
                select "cookImage", title, "Cookid" from (
                SELECT "cookImage", title, "Cookid", likecount 
                FROM body."v_recipeWorld"
                WHERE "Cookid" NOT IN (SELECT "Cookid" FROM first_query) -- 避免重複
                ORDER BY likecount DESC
                LIMIT 7 - (SELECT COUNT(*) FROM first_query)) as a;
            ''', (recipe_id, recipe_id))
            recipe_data = cursor.fetchall()

            connection.close()

            return render_template('/robott/detailedRecipe.html', data=data, Recipes_image_path=Recipes_image_path, name=name, userImage=userImage, uid=uid, recipe_data=recipe_data)
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

    cursor.execute('select title, a.create_time, summary, "prepare", "cookTime", "cookStep", nutrition, "cookImage", diet, "prepareMoney", a."Cookid", a."Uid", COALESCE(b."Uid", 0) as cookbookLike, likecount, messagecount, cookbookStar, "cookStep_mp3" from (SELECT title, create_time, summary, "prepare", "cookTime", "cookStep", nutrition, "cookImage", diet, "prepareMoney", "Cookid", "Uid", likecount, messagecount, cookbookStar, "cookStep_mp3" FROM body."v_recipeWorld" where "Cookid" = %s) as a left join (SELECT * FROM body."cookbookLike" where "Uid" = %s) as b on a."Cookid" = b."Cookid"', (recipe_id, uid))

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

    # 獲取前 7 個最喜歡的食譜
    cursor.execute('''
        WITH first_query AS (
            SELECT "cookImage", title, "Cookid" 
            FROM body."v_recipeWorld" 
            WHERE main_req = (SELECT main_req FROM body.cookbook WHERE "Cookid" = %s) 
            AND "Cookid" != %s
            ORDER BY likecount DESC
            LIMIT 7
        )

        SELECT * FROM first_query

        UNION ALL

        -- 只在 first_query 的結果少於 7 筆時從這裡補足
        select "cookImage", title, "Cookid" from (
        SELECT "cookImage", title, "Cookid", likecount 
        FROM body."v_recipeWorld"
        WHERE "Cookid" NOT IN (SELECT "Cookid" FROM first_query) -- 避免重複
        ORDER BY likecount DESC
        LIMIT 7 - (SELECT COUNT(*) FROM first_query)) as a;
    ''', (recipe_id, recipe_id))
    recipe_data = cursor.fetchall()

    connection.close()

    has_non_zero = any(d[2] != 0 for d in data3)

    return render_template('/robott/shareResults.html', data=data, data2=data2, data3=data3, Recipes_image_path=Recipes_image_path, user_image_path=user_image_path, name=name, userImage=userImage, has_non_zero=has_non_zero, uid=uid, recipe_data=recipe_data)

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
        
#生成食譜 - 隨機生成
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY", "OPENAI_API_KEY"))

speech_config = speechsdk.SpeechConfig(
    subscription=os.environ.get("SPEECH_KEY", "SPEECH_KEY"),
    region="southeastasia"  # 區域
)

speech_config.speech_synthesis_voice_name = "zh-TW-HsiaoChenNeural"

@robott_bp.route('/randomRecipe', methods=['POST'])
def robott_randomRecipe():
    name=session['name']
    uid=session['uid']
    userImage=session['user_image']

    if request.method == 'POST':
        try:
            content = f"飲食法:隨機; 主要食材:隨機; 營養需求:隨機; 烹調時間:隨機; 過敏成分或不吃的食物:隨機"

            def wait_on_run(run, thread):
                while run.status == "queued" or run.status == "in_progress":
                    run = client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)
                    time.sleep(0.5)
                return run
            
            # 食譜助理執行緒
            def recipe_assistant():
                thread = client.beta.threads.create()
                message = client.beta.threads.messages.create(thread_id=thread.id, role="user", content=content)
                run = client.beta.threads.runs.create(thread_id=thread.id, assistant_id='asst_uq2gPIFYGBn1gCda10ExVyj1')
                run = wait_on_run(run, thread)
                messages = client.beta.threads.messages.list(thread_id=thread.id)
                for message in reversed(messages.data):
                    data = message.content[0].text.value
                print(json.loads(data))
                return json.loads(data)

            # 估價助理執行緒
            def pricing_assistant(prepare_str):
                thread = client.beta.threads.create()
                message = client.beta.threads.messages.create(thread_id=thread.id, role="user", content=prepare_str)
                run = client.beta.threads.runs.create(thread_id=thread.id, assistant_id='asst_g2WebXcfXJBxfFP9VzMbBKQd')
                run = wait_on_run(run, thread)
                messages = client.beta.threads.messages.list(thread_id=thread.id)
                for message in reversed(messages.data):
                    data2 = message.content[0].text.value
                print(json.loads(data2))
                return json.loads(data2)

            # 生成圖片執行緒
            def generate_image(imagedescribe):
                response = client.images.generate(
                    model="dall-e-3",
                    prompt="食物在畫面的正中心，不能出現未說明的食材" + imagedescribe,
                    n=1,
                    quality="standard",
                    size="1024x1024",
                )
                image_url = response.data[0].url
                current_time = datetime.now()
                image_name = "image" + current_time.strftime('%Y-%m-%d-%H-%M-%S') + ".png"
                file_name = "static/images/openai/" + image_name
                urllib.request.urlretrieve(image_url, file_name)
                return image_name
            
            # 生成音檔執行緒
            def generate_audio(text):
                # 在/static/mp3/uid資料夾下生成音檔
                audio_path = f"static/mp3/{uid}"

                if not os.path.exists(audio_path):
                    os.makedirs(audio_path)

                # 檔案名稱，uid+時間戳
                current_time = datetime.now()
                filename = f"{uid}-{current_time.strftime('%Y-%m-%d-%H-%M-%S')}.mp3"
                file_path = f"{audio_path}/{filename}"

                # 在每個句號後面加入 3 秒的停頓
                text_with_pause = text.replace('。', '。<break time="3000ms"/>')

                # 將文本轉換為 SSML 格式
                ssml_text = f"""
                <speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" xml:lang="zh-TW">
                    <voice name="zh-TW-HsiaoChenNeural">
                        {text_with_pause}
                    </voice>
                </speak>
                """

                # 輸出配置
                audio_config = speechsdk.audio.AudioOutputConfig(filename=file_path)
                synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)

                # 生成
                result = synthesizer.speak_ssml_async(ssml_text).get()

                if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
                    return filename
                else:
                    error_message = f"Error synthesizing speech: {result.error_details}"
                    print(error_message)
                    if result.cancellation_details.reason == speechsdk.CancellationReason.Error:
                        print(f"Error details: {result.cancellation_details.error_details}")
                    raise Exception(error_message)

            with ThreadPoolExecutor() as executor:
                # 同時執行多個任務
                recipe_future = executor.submit(recipe_assistant)
                recipe_data = recipe_future.result()

                title = recipe_data["recipe"]["title"]
                summary = recipe_data["recipe"]["summary"]
                prepare = recipe_data["recipe"]["prepare"]
                cookTime = recipe_data["recipe"]["cookTime"]
                cookStep = recipe_data["recipe"]["cookStep"]
                nutrition = recipe_data["recipe"]["nutrition"]
                diet = recipe_data["recipe"]["diet"]
                imagedescribe = recipe_data["imagedescribe"]

                # print(cookStep)

                cookStep = [step.replace("瀝乾", "瀝掉").replace("盛盤", "裝盤") for step in cookStep]


                prepare_str = ', '.join(prepare)
                cookStep_str = ', '.join(cookStep)
                nutrition_str = ', '.join(nutrition)
                diet_str = ', '.join(diet)

                pricing_future = executor.submit(pricing_assistant, prepare_str)
                pricing_data = pricing_future.result()

                prepareMoney = pricing_data["prepareMoney"]
                prepareMoney_str = ', '.join(prepareMoney)
                total = pricing_data["total"]

                image_future = executor.submit(generate_image, imagedescribe)
                image_name = image_future.result()

                # 在每一個cookStep開頭加上步驟編號
                cookStep_audiostr = ''
                for i, step in enumerate(cookStep, 1):
                    cookStep_audiostr += f"步驟{i}, {step}。"

                audio_future = executor.submit(generate_audio, cookStep_audiostr)
                audio_name = audio_future.result()


            current_date = datetime.now().strftime("%Y-%m-%d")
            

            # DB
            def db_insert():
                conn = db.get_connection()
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO body.cookbook (\"Uid\", title, summary, \"prepare\", \"prepareMoney\", \"cookTime\", \"cookStep\", \"cookStep_mp3\", 
                    nutrition, diet, \"cookImage\", \"cookImageDescribe\", \"isPublish\", diet_req, main_req, nutrition_req, cook_time_req, 
                    special_diet_req, create_time, update_time) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, '0', %s, %s, %s, %s, %s, now(), now())
                    ''',
                    (uid, title, summary, prepareMoney_str, total, cookTime, cookStep_str, audio_name, nutrition_str, diet_str, image_name, imagedescribe, '隨機', '隨機', '隨機', '隨機', '隨機'))
                
                cursor.execute('''
                    SELECT "Cookid" 
                    FROM body.cookbook 
                    WHERE title = %s AND "Uid" = %s 
                    ORDER BY "Cookid" DESC 
                    LIMIT 1;
                               ''', (title, uid))
                
                recipe_id = cursor.fetchone()[0]

                conn.commit()
                conn.close()

                return recipe_id
            
            recipe_id = db_insert()

            return jsonify({'recipe_id': recipe_id})
        except Exception as e:
            # 印出錯誤原因
            print('-'*30)
            print(e)
            print('-'*30)
            # 渲染失敗畫面
            # logging.error("Error occurred", exc_info=True)
            # logging.basicConfig(filename='../error.log', level=logging.ERROR)
            # 渲染錯誤畫面並返回錯誤信息
            return render_template('/question/error.html', error_message=str(e))

