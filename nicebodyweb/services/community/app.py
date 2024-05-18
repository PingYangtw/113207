# 匯入Blueprint模組
from flask import render_template
from flask import Blueprint

# 產生目標服務藍圖
community_bp = Blueprint('community_bp', __name__)

#--------------------------
# 在目標服務藍圖加入路由
#--------------------------

#社群主頁(母畫面)
@community_bp.route('/communityMain')
def community_Main(): 
    return render_template('/community/communityMain.html', data='王小明')


#單一貼文(子畫面)
@community_bp.route('/detailedPost')
def detailed_post(): 
    return render_template('/community/detailedPost.html', data='王小明')


#AI食譜發布
@community_bp.route('/airecipePost')
def airecipe_post(): 
    return render_template('/community/airecipePost.html', data='王小明')