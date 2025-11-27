from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from functools import wraps
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your-secret-key-here-change-in-production')

# 使用環境變數中的資料庫 URL（Render 會自動設定 DATABASE_URL）
# 如果沒有設定環境變數，則使用本地 SQLite 資料庫
database_url = os.environ.get('DATABASE_URL')
if database_url:
    # 將 postgres:// 轉換為 postgresql://（SQLAlchemy 使用 psycopg2 驅動）
    if database_url.startswith('postgres://'):
        database_url = database_url.replace('postgres://', 'postgresql://', 1)
    app.config['SQLALCHEMY_DATABASE_URI'] = database_url
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///expense_tracker.db'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    account = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    expenses = db.relationship('Expense', backref='user', lazy=True, cascade='all, delete-orphan')
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    category = db.Column(db.String(100), nullable=False)
    item = db.Column(db.String(200), nullable=False)
    price = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'date': self.date.strftime('%Y-%m-%d'),
            'category': self.category,
            'item': self.item,
            'price': self.price,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S')
        }

# Login required decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('請先登入', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# Authentication Routes
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        account = request.form.get('account')
        password = request.form.get('password')
        
        if not username or not account or not password:
            flash('所有欄位都必須填寫', 'danger')
            return redirect(url_for('register'))
        
        if User.query.filter_by(account=account).first():
            flash('帳號已存在', 'danger')
            return redirect(url_for('register'))
        
        user = User(username=username, account=account)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        
        flash('註冊成功！請登入', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        account = request.form.get('account')
        password = request.form.get('password')
        
        user = User.query.filter_by(account=account).first()
        
        if user and user.check_password(password):
            session['user_id'] = user.id
            session['username'] = user.username
            flash(f'歡迎回來，{user.username}！', 'success')
            return redirect(url_for('index'))
        else:
            flash('帳號或密碼錯誤', 'danger')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('已登出', 'info')
    return redirect(url_for('login'))

# Web Routes
@app.route('/')
@login_required
def index():
    user_id = session['user_id']
    expenses = Expense.query.filter_by(user_id=user_id).order_by(Expense.date.desc()).all()
    
    # Calculate total
    total = sum(expense.price for expense in expenses)
    
    return render_template('index.html', expenses=expenses, total=total)

@app.route('/expense/<int:id>')
@login_required
def view_expense(id):
    expense = Expense.query.get_or_404(id)
    
    # Check if expense belongs to current user
    if expense.user_id != session['user_id']:
        flash('無權限查看此紀錄', 'danger')
        return redirect(url_for('index'))
    
    return render_template('view_expense.html', expense=expense)

@app.route('/expense/new', methods=['GET', 'POST'])
@login_required
def new_expense():
    if request.method == 'POST':
        date_str = request.form.get('date')
        category = request.form.get('category')
        custom_category = request.form.get('custom_category')
        item = request.form.get('item')
        price = request.form.get('price')
        
        # Use custom category if provided
        if custom_category:
            category = custom_category
        
        try:
            date = datetime.strptime(date_str, '%Y-%m-%d').date()
            price = float(price)
            
            expense = Expense(
                user_id=session['user_id'],
                date=date,
                category=category,
                item=item,
                price=price
            )
            db.session.add(expense)
            db.session.commit()
            
            flash('花費紀錄新增成功！', 'success')
            return redirect(url_for('index'))
        except ValueError:
            flash('日期或價格格式錯誤', 'danger')
    
    return render_template('new_expense.html')

@app.route('/expense/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit_expense(id):
    expense = Expense.query.get_or_404(id)
    
    # Check if expense belongs to current user
    if expense.user_id != session['user_id']:
        flash('無權限編輯此紀錄', 'danger')
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        date_str = request.form.get('date')
        category = request.form.get('category')
        custom_category = request.form.get('custom_category')
        item = request.form.get('item')
        price = request.form.get('price')
        
        # Use custom category if provided
        if custom_category:
            category = custom_category
        
        try:
            expense.date = datetime.strptime(date_str, '%Y-%m-%d').date()
            expense.category = category
            expense.item = item
            expense.price = float(price)
            
            db.session.commit()
            
            flash('花費紀錄更新成功！', 'success')
            return redirect(url_for('view_expense', id=id))
        except ValueError:
            flash('日期或價格格式錯誤', 'danger')
    
    return render_template('edit_expense.html', expense=expense)

# RESTful API Routes
@app.route('/api/expenses', methods=['GET'])
@login_required
def api_get_expenses():
    user_id = session['user_id']
    expenses = Expense.query.filter_by(user_id=user_id).order_by(Expense.date.desc()).all()
    return jsonify([expense.to_dict() for expense in expenses])

@app.route('/api/expenses/<int:id>', methods=['GET'])
@login_required
def api_get_expense(id):
    expense = Expense.query.get_or_404(id)
    
    if expense.user_id != session['user_id']:
        return jsonify({'error': 'Unauthorized'}), 403
    
    return jsonify(expense.to_dict())

@app.route('/api/expenses', methods=['POST'])
@login_required
def api_create_expense():
    data = request.get_json()
    
    if not all(k in data for k in ('date', 'category', 'item', 'price')):
        return jsonify({'error': 'Missing required fields'}), 400
    
    try:
        expense = Expense(
            user_id=session['user_id'],
            date=datetime.strptime(data['date'], '%Y-%m-%d').date(),
            category=data['category'],
            item=data['item'],
            price=float(data['price'])
        )
        db.session.add(expense)
        db.session.commit()
        
        return jsonify(expense.to_dict()), 201
    except (ValueError, KeyError) as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/expenses/<int:id>', methods=['PUT'])
@login_required
def api_update_expense(id):
    expense = Expense.query.get_or_404(id)
    
    if expense.user_id != session['user_id']:
        return jsonify({'error': 'Unauthorized'}), 403
    
    data = request.get_json()
    
    try:
        if 'date' in data:
            expense.date = datetime.strptime(data['date'], '%Y-%m-%d').date()
        if 'category' in data:
            expense.category = data['category']
        if 'item' in data:
            expense.item = data['item']
        if 'price' in data:
            expense.price = float(data['price'])
        
        db.session.commit()
        
        return jsonify(expense.to_dict())
    except (ValueError, KeyError) as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/expenses/<int:id>', methods=['DELETE'])
@login_required
def api_delete_expense(id):
    expense = Expense.query.get_or_404(id)
    
    if expense.user_id != session['user_id']:
        return jsonify({'error': 'Unauthorized'}), 403
    
    db.session.delete(expense)
    db.session.commit()
    
    return jsonify({'message': 'Expense deleted successfully'}), 200

# Delete expense from web interface
@app.route('/expense/<int:id>/delete', methods=['POST'])
@login_required
def delete_expense(id):
    expense = Expense.query.get_or_404(id)
    
    if expense.user_id != session['user_id']:
        flash('無權限刪除此紀錄', 'danger')
        return redirect(url_for('index'))
    
    db.session.delete(expense)
    db.session.commit()
    
    flash('花費紀錄已刪除', 'success')
    return redirect(url_for('index'))

# Initialize database
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port, debug=False)
