import pandas as pd
from sqlalchemy import create_engine
import os
from dotenv import load_dotenv

# 1. 连接数据库（复用你项目里的配置）
load_dotenv()
engine = create_engine(os.getenv("DATABASE_URL"))

# 2. 读取数据（把整张表变成一个 DataFrame）
df = pd.read_sql("SELECT * FROM page_views ORDER BY visit_time DESC", engine)

print("=" * 40)
print("【1】数据长什么样")
print("=" * 40)
print(f"总行数: {len(df)}, 总列数: {len(df.columns)}")
print(df.head(5))   # 看前5行

print("\n" + "=" * 40)
print("【2】基本统计")
print("=" * 40)
print(f"总访问量: {len(df)}")
print(f"独立页面数: {df['page_url'].nunique()}")
print(f"独立访客数: {df['visitor_ip'].nunique()}")

print("\n" + "=" * 40)
print("【3】热门页面 TOP 5（相当于 SQL 的 GROUP BY）")
print("=" * 40)
print(df['page_url'].value_counts().head(5))

print("\n" + "=" * 40)
print("【4】每日访问量（把时间戳拆成日期）")
print("=" * 40)
df['visit_date'] = pd.to_datetime(df['visit_time']).dt.date
print(df.groupby('visit_date').size())

print("\n" + "=" * 40)
print("【5】访客 IP 排行 TOP 5")
print("=" * 40)
print(df['visitor_ip'].value_counts().head(5))