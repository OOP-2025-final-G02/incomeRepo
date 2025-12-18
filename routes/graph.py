from flask import Blueprint, render_template
from models import Order, User, Product
from datetime import datetime
from collections import defaultdict

# Blueprintの作成
graph_bp = Blueprint('graph', __name__, url_prefix='/graph')


@graph_bp.route('/')
def index():
    # グラフ表示に必要なデータを取得
    orders = Order.select()
    users = User.select()
    products = Product.select()
    
    # グラフ4: ユーザーが登録した月収を年ごとに集計
    yearly_income = defaultdict(float)
    for product in products:
        year = product.created_at.year
        yearly_income[year] += float(product.income)
    
    # ソート済みの年と月収を取得
    sorted_years = sorted(yearly_income.keys()) if yearly_income else []
    yearly_data = {
        'years': sorted_years,
        'counts': [yearly_income[year] for year in sorted_years] if sorted_years else []
    }

    return render_template('graph.html',
                         title='グラフ',
                         orders=orders,
                         users=users,
                         products=products,
                         yearly_data=yearly_data)
