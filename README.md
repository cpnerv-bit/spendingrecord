# 花費紀錄系統

一個使用 Flask 和 SQLAlchemy 建立的花費紀錄管理系統，具有完整的使用者認證和 RESTful API。

## 功能特色

### 使用者功能
- ✅ 使用者註冊與登入系統
- ✅ 密碼加密保護
- ✅ Session 管理

### 花費紀錄管理
- ✅ 新增花費紀錄（日期、類別、品項、價錢）
- ✅ 查看花費紀錄列表
- ✅ 查看單筆花費紀錄詳情
- ✅ 編輯花費紀錄
- ✅ 刪除花費紀錄
- ✅ 自動計算總花費
- ✅ 日期選擇器
- ✅ 預設類別（早餐、午餐、晚餐）
- ✅ 自訂類別功能

### RESTful API
- `GET /api/expenses` - 取得所有花費紀錄
- `GET /api/expenses/<id>` - 取得單筆花費紀錄
- `POST /api/expenses` - 新增花費紀錄
- `PUT /api/expenses/<id>` - 更新花費紀錄
- `DELETE /api/expenses/<id>` - 刪除花費紀錄

### UI/UX 設計
- 🎨 現代化漸層設計
- 📱 響應式設計（支援手機、平板、桌面）
- 🎯 直覺的使用者介面
- ⚡ 流暢的動畫效果
- 🌈 類別顏色標記
- 💫 卡片懸停效果
- ✨ Bootstrap 5 + Bootstrap Icons

## 安裝步驟

### 1. 安裝 Python 套件

```powershell
pip install -r requirements.txt
```

### 2. 執行應用程式

```powershell
python app.py
```

### 3. 開啟瀏覽器

訪問 `http://127.0.0.1:5000` 開始使用

## 使用說明

### 首次使用

1. **註冊帳號**
   - 點擊「註冊」連結
   - 填寫使用者名稱、帳號、密碼
   - 提交註冊表單

2. **登入系統**
   - 使用註冊的帳號和密碼登入
   - 成功登入後會跳轉到花費紀錄列表頁面

### 管理花費紀錄

#### 新增紀錄
1. 點擊「新增花費紀錄」按鈕
2. 選擇日期（點擊日曆圖示可選擇年、月、日）
3. 選擇類別（早餐、午餐、晚餐）或自訂類別
4. 輸入品項名稱
5. 輸入價錢
6. 點擊「儲存紀錄」

#### 查看紀錄
- 在列表頁面點擊任一筆紀錄即可查看詳情
- 或點擊「👁️」按鈕查看

#### 編輯紀錄
1. 在紀錄詳情頁面點擊「編輯」按鈕
2. 修改需要變更的欄位
3. 點擊「儲存變更」

#### 刪除紀錄
1. 在紀錄詳情頁面點擊「刪除」按鈕
2. 確認刪除操作

## API 使用範例

### 新增花費紀錄

```bash
curl -X POST http://127.0.0.1:5000/api/expenses \
  -H "Content-Type: application/json" \
  -d '{
    "date": "2025-11-25",
    "category": "午餐",
    "item": "便當",
    "price": 120
  }'
```

### 取得所有紀錄

```bash
curl http://127.0.0.1:5000/api/expenses
```

### 更新紀錄

```bash
curl -X PUT http://127.0.0.1:5000/api/expenses/1 \
  -H "Content-Type: application/json" \
  -d '{
    "price": 150
  }'
```

### 刪除紀錄

```bash
curl -X DELETE http://127.0.0.1:5000/api/expenses/1
```

## 資料庫結構

### User 資料表
- `id`: 主鍵
- `username`: 使用者名稱
- `account`: 帳號（唯一）
- `password_hash`: 密碼雜湊值

### Expense 資料表
- `id`: 主鍵
- `user_id`: 使用者 ID（外鍵）
- `date`: 日期
- `category`: 類別
- `item`: 品項
- `price`: 價錢
- `created_at`: 建立時間

## 技術架構

- **後端框架**: Flask 3.0.0
- **資料庫 ORM**: Flask-SQLAlchemy 3.1.1
- **密碼加密**: Werkzeug Security
- **前端框架**: Bootstrap 5.3.0
- **圖示**: Bootstrap Icons 1.11.0
- **資料庫**: SQLite

## 注意事項

1. **安全性**: 在生產環境中，請修改 `app.config['SECRET_KEY']` 為更安全的隨機字串
2. **資料庫**: 系統會自動建立 `expense_tracker.db` SQLite 資料庫
3. **Session**: 使用者登入後會保持登入狀態直到登出
4. **權限**: 使用者只能查看、編輯、刪除自己的花費紀錄

## 專案結構

```
花費紀錄/
├── app.py                      # 主程式
├── requirements.txt            # Python 套件清單
├── expense_tracker.db          # SQLite 資料庫（自動建立）
└── templates/                  # HTML 模板
    ├── base.html              # 基礎模板
    ├── login.html             # 登入頁面
    ├── register.html          # 註冊頁面
    ├── index.html             # 花費紀錄列表
    ├── new_expense.html       # 新增花費紀錄
    ├── edit_expense.html      # 編輯花費紀錄
    └── view_expense.html      # 查看花費紀錄詳情
```

## 授權

此專案為教學用途，可自由使用和修改。
