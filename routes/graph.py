from flask import Blueprint, render_template
from models import Order, User, Product

# Blueprintの作成
graph_bp = Blueprint('graph', __name__, url_prefix='/graph')


@graph_bp.route('/')
def index():
    # グラフ表示に必要なデータを取得
    orders = Order.select()
    users = User.select()
    products = Product.select()

    return render_template('graph.html',
                         title='グラフ',
                         orders=orders,
                         users=users,
                         products=products)
