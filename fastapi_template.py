# ==========================================
# 1. 导入所需工具（需要什么就加什么）
# ==========================================
from fastapi import FastAPI, Request, Body, HTTPException
from fastapi.responses import HTMLResponse
from sqlalchemy import create_engine, text
from sqlalchemy.exc import IntegrityError
import os
from dotenv import load_dotenv

# ==========================================
# 2. 创建 app 实例和数据库连接
# ==========================================
load_dotenv()
app = FastAPI()

DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)

# ==========================================
# 3. 基础路由（示例：首页）
# ==========================================
@app.get("/")
async def root():
    return {"message": "Hello World"}

# ==========================================
# 4. GET 接口（查询数据）
# ==========================================
@app.get("/items")
async def get_items():
    with engine.connect() as conn:
        sql = text("SELECT * FROM your_table")
        result = conn.execute(sql).fetchall()
        # 将结果转换为字典列表
        data = [{"id": row[0], "name": row[1]} for row in result]
        return {"data": data}

# ==========================================
# 5. GET 接口（根据ID查询）
# ==========================================
@app.get("/items/{item_id}")
async def get_item(item_id: int):
    with engine.connect() as conn:
        sql = text("SELECT * FROM your_table WHERE id = :id")
        result = conn.execute(sql, {"id": item_id}).fetchone()
        if not result:
            raise HTTPException(status_code=404, detail="未找到")
        return {"id": result[0], "name": result[1]}

# ==========================================
# 6. POST 接口（新增数据）
# ==========================================
@app.post("/items")
async def create_item(request: Request):
    data = await request.json()
    name = data.get("name")

    with engine.connect() as conn:
        sql = text("INSERT INTO your_table (name) VALUES (:name)")
        conn.execute(sql, {"name": name})
        conn.commit()
        return {"message": "创建成功", "name": name}

# ==========================================
# 7. PUT 接口（更新数据）
# ==========================================
@app.put("/items/{item_id}")
async def update_item(item_id: int, request: Request):
    data = await request.json()
    name = data.get("name")

    with engine.connect() as conn:
        sql = text("UPDATE your_table SET name = :name WHERE id = :id")
        result = conn.execute(sql, {"name": name, "id": item_id})
        conn.commit()
        if result.rowcount == 0:
            raise HTTPException(status_code=404, detail="未找到")
        return {"message": "更新成功"}

# ==========================================
# 8. DELETE 接口（删除数据）
# ==========================================
@app.delete("/items/{item_id}")
async def delete_item(item_id: int):
    with engine.connect() as conn:
        sql = text("DELETE FROM your_table WHERE id = :id")
        result = conn.execute(sql, {"id": item_id})
        conn.commit()
        if result.rowcount == 0:
            raise HTTPException(status_code=404, detail="未找到")
        return {"message": "删除成功"}

# ==========================================
# 9. 启动入口（本地调试用）
# ==========================================
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)



# 启动后端服务
##uvicorn main:app --reload

# 启动 ngrok 公网隧道（需要先 cd 到桌面）
##ngrok http 8000   