# 匯入Blueprint模組
from flask import render_template
from flask import Blueprint

from utils import db

#檢查上傳檔案類型
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ('png', 'jpg', 'jpeg', 'gif')

# 產生營養師服務藍圖
robott_bp = Blueprint('robott_bp', __name__)

#--------------------------
# 在營養師服務藍圖加入路由
#--------------------------
#生成食譜
@robott_bp.route('/selfList')
def robott_selfList(): 
    #取得資料庫連線 
    connection = db.get_connection() 
    
    #產生執行sql命令的物件, 再執行sql   
    cursor = connection.cursor()     
    cursor.execute('SELECT cusno FROM public.customer limit 1;')
    
    #取出資料
    data = cursor.fetchall()    
    print(data)
    #關閉資料庫連線    
    connection.close()
    
    #渲染網頁  
    return render_template('/robott/generateRecipes.html', data=data)


#食譜天地
@robott_bp.route('/everyList')
def robott_everyList(): 
    #取得資料庫連線 
    connection = db.get_connection() 
    
    #產生執行sql命令的物件, 再執行sql   
    cursor = connection.cursor()     
    cursor.execute('SELECT cusno FROM public.customer limit 1;')
    
    #取出資料
    data = cursor.fetchall()    
    print(data)
    #關閉資料庫連線    
    connection.close()
    
    #渲染網頁  
    return render_template('/robott/recipeWorld.html', data=data)


#生成食譜 > 詳細食譜
@robott_bp.route('/selfList/more')
def robott_selfList_more(): 
    #取得資料庫連線 
    connection = db.get_connection() 
    
    #產生執行sql命令的物件, 再執行sql   
    cursor = connection.cursor()     
    cursor.execute('SELECT cusno FROM public.customer limit 1;')
    
    #取出資料
    data = cursor.fetchall()    
    print(data)
    #關閉資料庫連線    
    connection.close()
    
    #渲染網頁  
    return render_template('/robott/detailedRecipe.html', data=data)


#食譜天地 > 詳細食譜
@robott_bp.route('/everyList/more')
def robott_everyList_more(): 
    #取得資料庫連線 
    connection = db.get_connection() 
    
    #產生執行sql命令的物件, 再執行sql   
    cursor = connection.cursor()     
    cursor.execute('SELECT cusno FROM public.customer limit 1;')
    
    #取出資料
    data = cursor.fetchall()    
    print(data)
    #關閉資料庫連線    
    connection.close()
    
    #渲染網頁  
    return render_template('/robott/detailedRecipe.html', data=data)


#發佈食譜
@robott_bp.route('/selfList/share')
def robott_share(): 
    #取得資料庫連線 
    connection = db.get_connection() 
    
    #產生執行sql命令的物件, 再執行sql   
    cursor = connection.cursor()     
    cursor.execute('SELECT cusno FROM public.customer limit 1;')
    
    #取出資料
    data = cursor.fetchall()    
    print(data)
    #關閉資料庫連線    
    connection.close()
    
    #渲染網頁  
    return render_template('/robott/shareResults.html', data=data)