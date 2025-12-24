from flask import Blueprint, render_template
from models.graph_generator import generate_monthly_summary_graph
from models import Product, User

# Blueprintの作成
graph_bp = Blueprint('graph', __name__, url_prefix='/graph')


@graph_bp.route('/')
def index():
    """グラフ表示ページ"""
    monthly_graph = generate_monthly_summary_graph()
    products = Product.select()
    users = User.select()

    return render_template('graph.html',
                         monthly_graph=monthly_graph,
                         products=products,
                         users=users)
