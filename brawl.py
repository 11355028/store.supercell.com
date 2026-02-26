from flask import Flask, render_template_string, request, jsonify

app = Flask(__name__)

# 單頁 HTML 模板 (包含 CSS 與 JavaScript)
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="zh-TW">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>荒野亂鬥 - 測試商城</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background-color: #f4f4f9;
            color: #333;
            margin: 0;
            padding: 20px;
        }
        h1, h2 {
            text-align: center;
            color: #2c3e50;
        }
        .container {
            max-width: 800px;
            margin: 0 auto;
            background: #fff;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        }
        .section {
            margin-bottom: 30px;
            padding-bottom: 20px;
            border-bottom: 1px solid #eee;
        }
        .product {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 10px;
            background: #fdfdfd;
            border: 1px solid #ddd;
            margin-bottom: 10px;
            border-radius: 5px;
        }
        .product-name {
            font-weight: bold;
            flex-grow: 1;
        }
        .product-price {
            color: #e74c3c;
            margin-right: 20px;
            font-weight: bold;
            width: 100px;
            text-align: right;
        }
        input[type="number"] {
            width: 60px;
            padding: 5px;
            border: 1px solid #ccc;
            border-radius: 4px;
        }
        .checkout-section {
            text-align: center;
            margin-top: 20px;
            background: #ecf0f1;
            padding: 20px;
            border-radius: 10px;
        }
        .total-price {
            font-size: 1.5em;
            color: #d35400;
            margin-bottom: 15px;
        }
        button {
            background-color: #27ae60;
            color: white;
            border: none;
            padding: 10px 30px;
            font-size: 1.2em;
            border-radius: 5px;
            cursor: pointer;
            transition: background 0.3s;
        }
        button:hover {
            background-color: #2ecc71;
        }
        .disclaimer {
            font-size: 0.85em;
            color: #7f8c8d;
            margin-top: 10px;
        }
    </style>
</head>
<body>

<div class="container">
    <h1>荒野亂鬥 特約商城 (測試版)</h1>
    
    <div id="store-items">
        </div>

    <div class="checkout-section">
        <div class="total-price">總計: NT$ <span id="total-amount">0</span></div>
        <button onclick="checkout()">模擬信用卡結帳</button>
        <div class="disclaimer">
            * 每個商品單次最多限購 5 個。<br>
            * 本網站僅供測試，不收集真實信用卡資料，點擊結帳將模擬成功。
        </div>
    </div>
</div>

<script>
    // 商品資料
    const products = {
        "通行券專區": [
            { id: "p1", name: "亂鬥通行券", price: 290 },
            { id: "p2", name: "高級通行券", price: 430 },
            { id: "p3", name: "Pro通行券", price: 780 }
        ],
        "寶石專區": [
            { id: "g1", name: "30寶石", price: 70 },
            { id: "g2", name: "80寶石", price: 170 },
            { id: "g3", name: "170寶石", price: 330 },
            { id: "g4", name: "360寶石", price: 670 },
            { id: "g5", name: "950寶石", price: 1690 },
            { id: "g6", name: "2000寶石", price: 3290 }
        ],
        "代打專區": [
            { id: "b1", name: "總盃100", price: 250 },
            { id: "b2", name: "總盃500", price: 1250 },
            { id: "b3", name: "總盃1000", price: 2400 },
            { id: "b4", name: "單角100", price: 600 },
            { id: "b5", name: "單角200", price: 1100 },
            { id: "b6", name: "單角500", price: 1750 },
            { id: "b7", name: "單角衝巔峰威望一", price: 2250 },
            { id: "b8", name: "單角衝巔峰威望二 (若無1000盃則衝至威望一)", price: 2500 },
            { id: "b9", name: "單角衝巔峰威望三以上 (未達威望二則衝至下個里程碑)", price: 3000 }
        ]
    };

    const storeContainer = document.getElementById('store-items');
    
    // 渲染商品列表
    for (const [category, items] of Object.entries(products)) {
        let sectionHTML = `<div class="section"><h2>${category}</h2>`;
        items.forEach(item => {
            sectionHTML += `
                <div class="product">
                    <span class="product-name">${item.name}</span>
                    <span class="product-price">NT$ ${item.price}</span>
                    <input type="number" id="${item.id}" data-price="${item.price}" data-name="${item.name}" value="0" min="0" max="5" onchange="calculateTotal()">
                </div>
            `;
        });
        sectionHTML += `</div>`;
        storeContainer.innerHTML += sectionHTML;
    }

    // 計算總金額
    function calculateTotal() {
        let total = 0;
        const inputs = document.querySelectorAll('input[type="number"]');
        inputs.forEach(input => {
            let qty = parseInt(input.value);
            // 強制檢查不能超過 5 個
            if (qty > 5) {
                input.value = 5;
                qty = 5;
                alert("一個商品最多只能下單 5 個！");
            }
            if (qty < 0) {
                input.value = 0;
                qty = 0;
            }
            let price = parseInt(input.getAttribute('data-price'));
            total += qty * price;
        });
        document.getElementById('total-amount').innerText = total;
    }

    // 送出結帳
    function checkout() {
        let orderDetails = [];
        const inputs = document.querySelectorAll('input[type="number"]');
        inputs.forEach(input => {
            let qty = parseInt(input.value);
            if (qty > 0) {
                orderDetails.push({
                    name: input.getAttribute('data-name'),
                    price: input.getAttribute('data-price'),
                    quantity: qty
                });
            }
        });

        if (orderDetails.length === 0) {
            alert("購物車是空的，請先選擇商品！");
            return;
        }

        // 發送 POST 請求至 Python 後端
        fetch('/checkout', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ items: orderDetails })
        })
        .then(response => response.json())
        .then(data => {
            alert(data.message + "\\n\\n訂單總額: NT$" + document.getElementById('total-amount').innerText);
            // 結帳後清空購物車
            inputs.forEach(input => input.value = 0);
            calculateTotal();
        })
        .catch(error => {
            console.error('Error:', error);
            alert("結帳系統發生錯誤！");
        });
    }
</script>

</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/checkout', methods=['POST'])
def process_checkout():
    data = request.json
    # 在終端機印出訂單資訊供測試確認
    print("--- 收到新訂單 ---")
    for item in data.get('items', []):
        print(f"商品: {item['name']}, 數量: {item['quantity']}, 單價: {item['price']}")
    print("------------------")
    
    return jsonify({
        "status": "success",
        "message": "信用卡測試付款成功！訂單已傳送至後端。"
    })

if __name__ == '__main__':
    # 啟動測試伺服器
    app.run(host='0.0.0.0', port=5000, debug=True)
