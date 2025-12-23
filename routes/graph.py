from flask import Blueprint, render_template
from models.graph_generator import generate_monthly_summary_graph
from models.graph_circle import generate_monthly_summary_graph as generate_pie_graph 

# Blueprintの作成
graph_bp = Blueprint('graph', __name__, url_prefix='/graph')


@graph_bp.route('/')
def index():
    """グラフ表示ページ"""
    monthly_graph = generate_monthly_summary_graph()

    pie_graph = generate_pie_graph()  # 円グラフを生成(幅:pie_graph)

    return render_template('graph.html',
                         monthly_graph=monthly_graph,

                         pie_graph=pie_graph)
