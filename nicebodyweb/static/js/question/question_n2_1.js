window.onload = function () {
    // Navbar
    renderNav();

    if (messageText == "0") {
        document.getElementById("loginDialog").showModal();
        document.getElementById('loginDialog').scrollTop = 0;
    }

    // 解析 URL 中的 `category` 參數來決定標籤顯示
    const urlParams = new URLSearchParams(window.location.search);
    const category = urlParams.get('category') || 'main_food'; // 默認類別為 'main_food'

    // 定義不同類別對應的標籤
    const tagData = {
        main_food: ["白米", "糙米", "黑米", "紅米", "糯米", "香米", "小米",
                    "寬麵", "細麵", "刀削麵", "拉麵", "義大利麵",
                    "餃子", "餛飩", "麵包",
                    "馬鈴薯", "玉米", "地瓜", "紅薯"],
        meat: ["牛肉", "豬肉", "雞肉", "雞胸肉", "雞腿肉", "羊肉", "鴨肉", "魚肉", "蝦仁", "蛤蜊", "鮭魚", "鱈魚", "魷魚", "章魚", "螃蟹", "培根", "火腿", "香腸", "熱狗"],
        vegetable: ["菠菜", "青江菜", "空心菜", "大白菜", "高麗菜", "胡蘿蔔", "馬鈴薯", "芋頭", "白花菜", "青菜花", "青椒", "苦瓜", "高麗菜", "茄子", "金針菇", "洋蔥", "青椒", "金針菇", "洋蔥"],
        fruit: ["香蕉", "芭樂", "番茄", "草莓", "蓮霧", "枇杷", "桃子", "櫻桃", "西瓜", "釋迦", "百香果", "鳳梨", "芒果", "柚子", "柿子", "火龍果", "楊桃", "梨子", "柳丁", "蘋果", "葡萄", "橘子","荔枝", "龍眼"],
        egg: ["班尼迪克蛋 ", "歐姆蛋", "玉子燒 ", "溏心蛋", "滷蛋", "鐵蛋", "太陽蛋", "荷包蛋", "炒蛋", "鹹蛋", "皮蛋", "茶葉蛋", "糖心蛋", "水煮蛋", "炸蛋", "蛋餅", "蛋捲"],
        nut: ["杏仁", "核桃", "腰果", "榛果", "開心果", "南瓜子", "花生", "松子", "蓮子", "巴西堅果", "夏威夷果", "胡桃", "黑芝麻", "白芝麻", "葵花子"],
        dairy: ["鮮乳", "低脂乳", "植物奶", "燕麥奶", "脫脂乳", "保久乳", "奶粉", "優酪乳", "優格", "乳酪", "起司", "奶油", "乳清蛋白", "煉乳", "奶昔"],
        seasoning: ["醬油", "醋", "糖", "鹽", "胡椒", "辣椒", "香料", "調味料", "油", "香油", "辣醬", "蒜", "番茄醬", "沙拉醬", "蜂蜜芥末醬", "和風醬", "泰式酸辣醬"],
        drink: ["水", "紅茶", "抹茶", "烏龍茶", "綠茶", "包種茶", "普洱茶", "咖啡", "奶茶", "珍珠奶茶", "果汁", "汽水", "啤酒", "紅酒", "白酒", "威士忌", "伏特加", "龍舌蘭"],
        other: ["餅乾", "蛋糕", "巧克力", "糖果", "冰淇淋", "壽司", "豆花", "滷味", "沙拉", "湯", "臭豆腐", "滷肉飯", "健康餐盒", "可愛造型便當", "月餅"]
    };

    // 根據類別來選擇標籤
    const defaultTags = tagData[category] || tagData['main_food'];

    // 變數
    let tags = [];
    let selectedTagCounts = JSON.parse(sessionStorage.getItem('selectedTagCounts')) || {};

    const tagListContainer1 = document.querySelector('.tag-list-item');
    const tagListContainer2 = document.querySelector('.tag-list-item2');
    const tagListContainer3 = document.querySelector('.tag-list-item3');

    const continueBtn = document.getElementById('continue-btn');

    const inputField = document.getElementById('tag-ip');

    const savedValue = sessionStorage.getItem('tagInputValue2');

    console.log(savedValue);

    // 初始化標籤
    defaultTags.forEach((tag, index) => {
        const tagButton = document.createElement("button");
        tagButton.classList.add("item");
        tagButton.textContent = tag;
        tagButton.id = tag;
        tagButton.addEventListener("click", function () {
            const isSelected = tagButton.classList.contains("item-select");
            if (!isSelected) {
                addTagToInput(tag); // 使用按鈕上存儲的標籤值
                tagButton.classList.add("item-select");
                selectedTagCounts[category] = (selectedTagCounts[category] || 0) + 1;
            } else {
                removeTagFromInput(tag); // 使用按鈕上存儲的標籤值
                tagButton.classList.remove("item-select");
                selectedTagCounts[tacategoryg]--;
            }

            sessionStorage.setItem('selectedTagCounts', JSON.stringify(selectedTagCounts));
            console.log('selectedTagCounts 的值為：', selectedTagCounts);

            
            // 每次点击标签后检查输入框
            checkInput();
        });

        if (index <= 7 ) {
            tagListContainer1.appendChild(tagButton);
        } else if (index <= 12) {
            tagListContainer2.appendChild(tagButton);
        } else {
            tagListContainer3.appendChild(tagButton);
        }
    });

    function addTagToInput(tag) {
        tags.push(tag);

        // 將標籤文字添加到輸入框中
        const tagInput = document.getElementById('tag-ip');
        if (tagInput.value.trim() === "") {
            tagInput.value = tag;
        } else {
            tagInput.value += `、 ${tag}`;
        }
    }

    // 從輸入框中移除指定的標籤文字
    function removeTagFromInput(tagToRemove) {
        tags = tags.filter(tag => tag !== tagToRemove);

        const tagInput = document.getElementById('tag-ip');
        const currentTags = tagInput.value.split('、').map(tag => tag.trim());
        const updatedTags = currentTags.filter(tag => tag !== tagToRemove);
        tagInput.value = updatedTags.join('、');
    }

    // 检查输入框中是否有文本，并根据情况更新按钮状态和样式
    function checkInput() {
        if (inputField.value.trim() !== '' || tags.length > 0) {
            continueBtn.classList.add('button-brwon');
            continueBtn.setAttribute('href', '/question/question_n3');
        } else {
            continueBtn.classList.remove('button-brwon');
            continueBtn.removeAttribute('href');
        }
    }

    // 点击按钮时跳转到question_second.html页面
    continueBtn.addEventListener('click', function () {
        const tagInput = document.getElementById('tag-ip');
        sessionStorage.setItem('tagInputValue2', tagInput.value);
        sessionStorage.removeItem('tagInputValue3');
    });

    inputField.addEventListener('input', function() {
        const inputValue = inputField.value.trim(); // 獲取去除兩端空格的輸入值
        if (inputValue !== '') {
            continueBtn.classList.add('button-brwon');
            continueBtn.setAttribute('href', '/question/question_n3');
        } else {
            continueBtn.classList.remove('button-brwon');
            continueBtn.removeAttribute('href');
        }
    });

    continueBtn.addEventListener('click', function() {
        const inputValue = inputField.value.trim(); // 獲取去除兩端空格的輸入值
        if (inputValue === '') {
            alert('請輸入內容');
        } 
    });

    // 點擊返回按鈕時返回到前一頁
    document.getElementById('back').addEventListener('click', function () {
        const tagInput = document.getElementById('tag-ip');
        sessionStorage.setItem('tagInputValue2', tagInput.value);
        sessionStorage.setItem()
    });

   if (savedValue !== null) {
    inputField.value = savedValue;
    checkInput();
    const selectedTags = savedValue.split('、').map(tag => tag.trim());
    selectedTags.forEach(tag => {
        const tagButton = document.getElementById(tag);
        if (tagButton !== null) {
            tagButton.classList.add('item-select');
        }
    });
    
    }
    
};