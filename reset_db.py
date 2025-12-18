from models import db, MODELS

# データベースに接続
db.connect()

# 既存のテーブルを削除
db.drop_tables(MODELS, safe=True)

# テーブルを再作成
db.create_tables(MODELS)

print("データベースをリセットしました。")

db.close()
