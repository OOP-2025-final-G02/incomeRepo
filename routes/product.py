from flask import Blueprint, render_template, request, redirect, url_for
from models import Product, User

# Blueprintの作成
product_bp = Blueprint('product', __name__, url_prefix='/products')


@product_bp.route('/')
def list():
    products = Product.select()
    return render_template('product_list.html', title='月収一覧', items=products)


@product_bp.route('/add', methods=['GET', 'POST'])
def add():

    # POSTで送られてきたデータは登録
    if request.method == 'POST':
        user_id = request.form['user_id']
        income = request.form['income']
        Product.create(user=user_id, income=income)
        return redirect(url_for('product.list'))

    # ユーザー一覧を取得してテンプレートに渡す
    users = User.select()
    return render_template('product_add.html', users=users)