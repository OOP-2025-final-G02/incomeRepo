"""
グラフ生成モジュール
外部ライブラリ: matplotlib, pandas を使用
"""
import matplotlib # グラフ生成用
matplotlib.use('Agg')  # GUI不要の場合はAggバックエンドを使用
import matplotlib.pyplot as plt
import pandas as pd
from models.product import Product
import io
import base64

def generate_monthly_summary_graph():
    """
    月ごとの合計金額を表示する円グラフ
    
    Returns:
        str: Base64エンコードされた円グラフ画像、またはNone（データがない場合）
    """
    # データベースから全データを取得
    products = Product.select().order_by(Product.created_at)
    
    if not products:
        return None
    
    # DataFrameに変換
    data = []
    for product in products:
        data.append({
            'date': product.created_at,
            'income': float(product.income)
        })
    
    df = pd.DataFrame(data)
    df['date'] = pd.to_datetime(df['date'])
    
    # 月ごとにグループ化
    df['year_month'] = df['date'].dt.to_period('M')
    df_monthly = df.groupby('year_month')['income'].sum().reset_index()
    df_monthly['year_month'] = df_monthly['year_month'].astype(str)
    
    # グラフの作成
    fig, ax = plt.subplots(figsize=(10, 8))
    
    # ラベルを月と金額で作成
    labels = [f"{month}\n¥{income:,.0f}" for month, income in zip(df_monthly['year_month'], df_monthly['income'])]
    
    # 円グラフの作成
    # 12ヶ月以上に対応した色を生成（HSVカラーマップで色を均等に分配）
    num_months = len(df_monthly)
    colors = plt.cm.hsv([i / num_months for i in range(num_months)])
    
    ax.pie(df_monthly['income'], 
           labels=labels, 
           autopct='%1.1f%%',
           startangle=90,
           counterclock=False,  # 時計回り方向で表示
           colors=colors,
           textprops={'fontsize': 9})
    
    # タイトル
    ax.set_title('月別収入割合', fontsize=14, fontweight='bold')
    ax.axis('equal')  # 円を正円にする
    
    # レイアウト調整
    plt.tight_layout()
    
    # 画像をバイナリに変換してBase64エンコード
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png', dpi=100, bbox_inches='tight')
    buffer.seek(0)
    image_base64 = base64.b64encode(buffer.getvalue()).decode()
    plt.close()
    
    return image_base64
