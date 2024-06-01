# 匯入Blueprint模組
from flask import render_template
from flask import Blueprint

# 產生目標服務藍圖
profile_bp = Blueprint('profile_bp', __name__)

#--------------------------
# 在目標服務藍圖加入路由
#--------------------------

#個人檔案頁面
@profile_bp.route('/profile')
def profile_page(): 
    return render_template('/profile/profile.html', data='王小明')

#個人檔案詳細頁面
@profile_bp.route('/profilePage')
def detailed_profile_page(): 
    return render_template('/profile/profilePage.html', data='王小明')

@profile_bp.route('/login')
def login(): 
    return render_template('/profile/login.html', data='王小明')

#關注列表頁面
@profile_bp.route('/followList')
def follow_list(): 
    return render_template('/profile/followList.html', data='王小明')

#收藏列表頁面
@profile_bp.route('/collectionList')
def collection_list(): 
    return render_template('/profile/collectionList.html', data='王小明')
