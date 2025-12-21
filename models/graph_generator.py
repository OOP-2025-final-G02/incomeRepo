"""
グラフ生成モジュール
外部ライブラリ: matplotlib, pandas を使用
"""
import matplotlib
matplotlib.use('Agg')  # GUI不要の場合はAggバックエンドを使用
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd
from models.product import Product
import io
import base64

def generate_monthly_summary_graph():
    """
    月ごとの合計金額を表示する折れ線グラフ
    複数年の場合は複数年分データが表示される
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
    fig, ax = plt.subplots(figsize=(14, 6))
    
    ax.plot(range(len(df_monthly)), df_monthly['income'], 
            marker='s', linestyle='-', linewidth=2, markersize=6, color='#A23B72')
    
    # グリッドを追加
    ax.grid(True, alpha=0.3)
    
    # ラベルとタイトル
    ax.set_xlabel('年-月', fontsize=12, fontweight='bold')
    ax.set_ylabel('金額 (円)', fontsize=12, fontweight='bold')
    ax.set_title('月ごとの金額推移グラフ', fontsize=14, fontweight='bold')
    
    # x軸のラベルを年月に
    ax.set_xticks(range(len(df_monthly)))
    ax.set_xticklabels(df_monthly['year_month'], rotation=45, ha='right')
    
    # y軸を金額形式で表示
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'¥{x:,.0f}'))
    
    # レイアウト調整
    plt.tight_layout()
    
    # 画像をバイナリに変換してBase64エンコード
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png', dpi=100)
    buffer.seek(0)
    image_base64 = base64.b64encode(buffer.getvalue()).decode()
    plt.close()
    
    return image_base64
