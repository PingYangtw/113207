import os
import requests
import pathlib
import shutil
from flask import Flask, session, abort, redirect, request, url_for, Blueprint, render_template, current_app
from google.oauth2 import id_token
from google_auth_oauthlib.flow import Flow
from pip._vendor import cachecontrol
import google.auth.transport.requests
from utils import db

# 配置 Google OAuth 2.0 憑證
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
secret_key = os.environ.get("APP_SECRET")
GOOGLE_CLIENT_ID = "971262403572-9oh6v76h7plj7asdpj7bj5hnvroj2q7h.apps.googleusercontent.com"
# client_secrets_file = os.path.join(pathlib.Path(__file__).parent, "client_secret.json")
client_secrets_file = "/etc/secrets/client_secret.json"

# 產生目標服務藍圖
login_bp = Blueprint('login_bp', __name__)

# 設置 Flow 物件
flow = Flow.from_client_secrets_file(
    client_secrets_file=client_secrets_file,
    scopes=["https://www.googleapis.com/auth/userinfo.profile", "https://www.googleapis.com/auth/userinfo.email", "openid"],
    # redirect_uri="http://127.0.0.1:5000/login/callback"
    redirect_uri="https://one13207.onrender.com/login/callback"
)

def login_is_required(function):
    def wrapper(*args, **kwargs):
        if "google_id" not in session:
            return abort(401)  # Authorization required
        else:
            return function()

    return wrapper

# 登入頁面
@login_bp.route('/loginPage')
def login_page(): 
    if "google_id" in session:
        return render_template('/home/login.html', name=session['name'], userImage=session['user_image'], uid=session['uid'], logged_in=True)
    else: 
        return render_template('/home/login.html', name='0', uid='0', logged_in=False)

# Google 登入
@login_bp.route('/googlelogin')
def google_login():
    authorization_url, state = flow.authorization_url(prompt='select_account')
    session["state"] = state
    return redirect(authorization_url)

# 回調函數
@login_bp.route('/callback')
def callback():
    if "google_id" not in session:
        flow.fetch_token(authorization_response=request.url)

        if not session["state"] == request.args["state"]:
            abort(500)  # State does not match!
       
        credentials = flow.credentials
        request_session = requests.session()
        cached_session = cachecontrol.CacheControl(request_session)
        token_request = google.auth.transport.requests.Request(session=cached_session)

        id_info = id_token.verify_oauth2_token(
            id_token=credentials._id_token,
            request=token_request,
            audience=GOOGLE_CLIENT_ID,
            clock_skew_in_seconds=60
        )
        
        connection = db.get_connection()
        cursor = connection.cursor()

        # 檢查googleId是否存在
        cursor.execute(
            """
            SELECT COUNT(*) FROM body.user_profile WHERE "googleId" = %s
            """,
            (id_info.get("sub"),)
        )
        count = cursor.fetchone()[0]

        if count == 0:
            # googleId不存在，插入新記錄
            cursor.execute(
                """
                INSERT INTO body.user_profile (username, email, "googleId", last_login_time, create_time, update_time)
                VALUES (%s, %s, %s, now(), now(), now())
                """,
                (id_info.get("name"), id_info.get("email"), id_info.get("sub"))
            )

            cursor.execute(
                """
                SELECT "Uid", "userImage", "isNutritionist", username FROM body.user_profile WHERE "googleId" = %s
                """,
                (id_info.get("sub"),)
            )

            result = cursor.fetchone()
            uid = result[0]
            user_image = result[1]
            is_nutritionist = result[2]
            username = result[3]

            # 獲取應用程序的根目錄
            app_root = current_app.root_path

            # 設置用戶圖片資料夾的絕對路徑
            user_image_folder = os.path.join(app_root, 'static', 'images', 'userImage', str(uid))
            default_image_path = os.path.join(app_root, 'static', 'images', 'userImage', 'default.jpg')

            # 檢查資料夾是否存在
            if not os.path.exists(user_image_folder):
                # 如果不存在，則創建資料夾
                os.makedirs(user_image_folder)
                
                # 複製預設圖片到新創建的資料夾
                shutil.copy(default_image_path, os.path.join(user_image_folder, 'default.jpg'))

            cursor.execute(
                """
                    INSERT INTO body."checkCategory" ("checkName", "Uid", "Iconid", create_time, update_time)
                    VALUES
                    ('吃蔬菜', %s, '2', now(), now()),
                    ('沒有吃零食', %s, '4', now(), now()),
                    ('喝水1公升', %s, '1', now(), now()),
                    ('沒有吃消夜', %s, '4', now(), now()),
                    ('吃2種水果', %s, '5', now(), now()),
                    ('有氧運動15分鐘', %s, '2', now(), now());
                """,
                (uid, uid, uid, uid, uid, uid)
            )

            username = id_info.get("name")
        else:
            # googleId存在，更新last_login_time
            cursor.execute(
                """
                UPDATE body.user_profile
                SET last_login_time = now()
                WHERE "googleId" = %s
                """,
                (id_info.get("sub"),)
            )
        
            cursor.execute(
                """
                SELECT "Uid", "userImage", "isNutritionist", username FROM body.user_profile WHERE "googleId" = %s
                """,
                (id_info.get("sub"),)
            )

            result = cursor.fetchone()
            uid = result[0]
            user_image = result[1]
            is_nutritionist = result[2]
            username = result[3]
        

        connection.commit()
        connection.close()

        # 保存用戶資訊到session
        session["google_id"] = id_info.get("sub")
        session["name"] = username
        session["email"] = id_info.get("email")
        session["uid"] = uid
        session["user_image"] = user_image
        session["is_nutritionist"] = is_nutritionist
        
        return redirect('/')
    else:
        return redirect('/')


# 登出
@login_bp.route('/logout')
def logout():
    if "google_id" in session:
        session.clear()
    return redirect('/login/loginPage')
