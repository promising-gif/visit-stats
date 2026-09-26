from openai import OpenAI
from fastapi import FastAPI, Body
from fastapi import Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from sqlalchemy import create_engine, text
from sqlalchemy.exc import IntegrityError
import os                # 新增：用来读取环境变量
from dotenv import load_dotenv  # 新增：用来加载 .env 文件



load_dotenv()            # 新增：加载 .env 文件里的配置

# 现在密码不再写在代码里，而是从 .env 文件里读取
DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)
client = OpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com"
)
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],          # 允许所有来源（测试阶段够用）
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/test", response_class=HTMLResponse)
async def test_page():
    return """
    <!DOCTYPE html>
    <html>
    <head><meta charset="UTF-8"><title>测试埋点</title></head>
    <body>
        <h1>欢迎来到测试页面</h1>
        <p>自动上报中...</p>
        <script>
            fetch('/pages/', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ page_url: '/test' })
            })
            .then(res => res.json())
            .then(data => console.log('✅ 上报成功:', data))
            .catch(err => console.warn('⚠️ 上报失败:', err));
        </script>
    </body>
    </html>
    """

# 下面的代码保持不变...

@app.get("/", response_class=HTMLResponse)
async def root():
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>网站访问统计看板</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 30px; background: #f5f7fa; }
            .container { max-width: 1000px; margin: auto; background: white; padding: 30px; border-radius: 12px; box-shadow: 0 4px 12px rgba(0,0,0,0.1); }
            h1 { color: #2c3e50; }
            .stats-grid { display: flex; gap: 20px; margin-bottom: 30px; }
            .stat-card { background: #ecf0f1; padding: 20px; border-radius: 10px; flex: 1; text-align: center; }
            .stat-card .number { font-size: 32px; font-weight: bold; color: #2980b9; }
            .section { border: 1px solid #ddd; padding: 20px; margin-bottom: 20px; border-radius: 8px; background: #fafbfc; }
            .section h3 { margin-top: 0; }
            table { width: 100%; border-collapse: collapse; margin-top: 12px; }
            th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
            th { background: #f2f2f2; }
            button { padding: 8px 16px; background: #3498db; color: white; border: none; border-radius: 6px; cursor: pointer; }
            button:hover { background: #2980b9; }
            input { padding: 8px; border-radius: 6px; border: 1px solid #ccc; width: 250px; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>📊 网站访问统计看板</h1>
            
            <div class="stats-grid">
                <div class="stat-card"><div>今日访问</div><div class="number" id="todayCount">-</div></div>
                <div class="stat-card"><div>总访问量</div><div class="number" id="totalCount">-</div></div>
            </div>

            <div class="section">
                <h3>🔥 热门页面排行 TOP 5</h3>
                <button onclick="loadHotPages()">刷新排行</button>
                <div id="hotResult">点击按钮加载数据...</div>
            </div>

            <div class="section">
                <h3>📋 全部访问记录</h3>
                <button onclick="loadAllPages()">刷新列表</button>
                <div id="listResult">点击按钮加载数据...</div>
            </div>
            <div class="section">
                <h3>🤖 AI 智能分析</h3>
                <button onclick="analyzeData()">生成分析</button>
                <div id="aiResult">点击按钮生成 AI 分析...</div>
            </div>



            <div class="section">
                <h3>📅 按日期筛选</h3>
                <input type="date" id="dateInput">
                <button onclick="filterByDate()">查询</button>
                <div id="dateResult">等待查询...</div>
            </div>

            <div class="section">
                <h3>➕ 模拟访问（测试用）</h3>
                <input type="text" id="pageUrlInput" placeholder="输入页面路径，如 /blog/1" value="/test">
                <button onclick="simulateVisit()">记录访问</button>
                <div id="createResult">等待操作...</div>
            </div>

        </div>

        <script>
            async function loadHotPages() {
                const resp = await fetch('/pages/hot');
                const data = await resp.json();
                let html = '<table><tr><th>页面路径</th><th>访问次数</th></tr>';
                data.data.forEach(row => {
                    html += `<tr><td>${row.page_url}</td><td>${row.visit_count}</td></tr>`;
                });
                html += '</table>';
                document.getElementById('hotResult').innerHTML = html;
            }

            async function loadAllPages() {
                const resp = await fetch('/pages');
                const data = await resp.json();
                let html = `<div>共 ${data.count} 条记录</div><table><tr><th>ID</th><th>页面路径</th><th>访客IP</th><th>访问时间</th></tr>`;
                data.data.forEach(row => {
                    html += `<tr><td>${row.id}</td><td>${row.page_url}</td><td>${row.visitor_ip}</td><td>${row.visit_time}</td></tr>`;
                });
                html += '</table>';
                document.getElementById('listResult').innerHTML = html;
            }

            async function simulateVisit() {
                const page_url = document.getElementById('pageUrlInput').value;
                const resultDiv = document.getElementById('createResult');
                const resp = await fetch('/pages/', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ page_url, visitor_ip: '模拟访客' })
                });
                const data = await resp.json();
                resultDiv.innerHTML = `✅ ${data.message}`;
                loadAllPages();
                loadHotPages();
            }

            
            

            
            

            async function filterByDate() {
                const date = document.getElementById('dateInput').value;
                if (!date) {
                    document.getElementById('dateResult').innerHTML = '<div class="error">请先选择日期</div>';
                    return;
                }
                const resp = await fetch(`/pages/date/${date}`);
                const data = await resp.json();
                if (data.count === 0) {
                    document.getElementById('dateResult').innerHTML = '<div>这一天没有访问记录</div>';
                return;
                }
                let html = `<div>共 ${data.count} 条记录</div><table><tr><th>ID</th><th>页面</th><th>访客IP</th><th>时间</th></tr>`;
                data.data.forEach(row => {
                    html += `<tr><td>${row.id}</td><td>${row.page_url}</td><td>${row.visitor_ip}</td><td>${row.visit_time}</td></tr>`;
                });
                html += '</table>';
                document.getElementById('dateResult').innerHTML = html;
            }


            async function loadStats() {
                const resp = await fetch('/pages');
                const data = await resp.json();
                document.getElementById('totalCount').innerText = data.count || 0;
    
                // 今日访问量：只统计今天的记录
                const today = new Date().toISOString().split('T')[0];
                const todayRows = data.data.filter(row => row.visit_time && row.visit_time.startsWith(today));
                document.getElementById('todayCount').innerText = todayRows.length || 0;
            }
            async function analyzeData() {
                const resultDiv = document.getElementById('aiResult');
                resultDiv.innerHTML = '⏳ AI 分析中，请稍候...';
                try {
                    const resp = await fetch('/analyze');
                    const data = await resp.json();
                    // 把换行符转换成 HTML 换行
                    const formatted = data.analysis.replace(/\\n/g, '<br>');
                    resultDiv.innerHTML = `<div style="line-height: 1.8;">${formatted}</div>`;
                } catch (e) {
                    resultDiv.innerHTML = `<div class="error">❌ 分析失败: ${e.message}</div>`;
                }
            }


            window.onload = function() {
                loadStats();
                loadAllPages();
                loadHotPages();
            };
        </script>
    </body>
    </html>
    """
    return html_content

# 这个接口会去数据库里查 user_id 对应的 pv 值
@app.get("/data/{user_id}")
async def get_user(user_id: int):
    with engine.connect() as conn:
        # 1. 核心业务：查数据（SELECT，不需要 commit）
        sql_select = text("SELECT pv FROM user_actions WHERE user_id = :uid LIMIT 1")
        result = conn.execute(sql_select, {"uid": user_id}).fetchone()
        
        # 2. 附加功能：记录查询日志（INSERT，必须 commit！）
        sql_log = text("INSERT INTO query_log (queried_user_id, action_type) VALUES (:uid, 'query')")
        conn.execute(sql_log, {"uid": user_id})
        conn.commit()  # ⚠️ 关键！日志是新增数据，必须提交
        
        # 3. 返回结果
        if result:
            return {"user_id": user_id, "pv": result[0], "status": "查询成功，已记录日志"}
        else:
            return {"user_id": user_id, "pv": 0, "status": "该用户暂无记录，已记录日志"}

#列表查询
@app.get("/pages")
async def get_all_pages():
    with engine.connect() as conn:
        sql = text("SELECT id, page_url, visitor_ip, visit_time FROM page_views ORDER BY id DESC")
        result = conn.execute(sql).fetchall()
        
        pages_list = []
        for row in result:
            pages_list.append({
                "id": row[0],
                "page_url": row[1],
                "visitor_ip": row[2],
                "visit_time": row[3]
            })
        return {"count": len(pages_list), "data": pages_list}

#接口-增
from sqlalchemy.exc import IntegrityError  # 在文件顶部导入

@app.post("/users/")
async def create_user(user_id: int = Body(), action_type: str = Body(), pv: int = Body()):
    try:
        with engine.connect() as conn:
            sql = text("INSERT INTO user_actions (user_id, action_type, pv) VALUES (:uid, :action, :pv)")
            conn.execute(sql, {"uid": user_id, "action": action_type, "pv": pv})
            conn.commit()
            return {"message": "用户数据创建成功!", "user_id": user_id}
    except IntegrityError:
        # 如果数据库报唯一约束冲突，返回 400（Bad Request）而不是 500
        return {"message": f"用户 {user_id} 已存在，请勿重复插入"}, 400


#接口-查询记录
@app.get("/users/recent")
async def get_recent():
    with engine.connect() as conn:
        sql=text("SELECT user_id,action_type,pv FROM user_actions ORDER BY id DESC LIMIT 3")
        result=conn.execute(sql).fetchall()

        users_list=[]
        for row in result:
            users_list.append({"users_id":row[0],"action_type":row[1],"pv":row[2]})
        return {"count":len(users_list),"data":users_list}

#接口-改
@app.put("/users/{user_id}")
async def update_user(user_id: int, action_type: str = Body(), pv: int = Body()):
    with engine.connect() as conn:
        # 1. 执行更新操作
        sql_update = text("UPDATE user_actions SET action_type = :action, pv = :pv WHERE user_id = :uid")
        result = conn.execute(sql_update, {"action": action_type, "pv": pv, "uid": user_id})
        
        # 2. 记录操作日志（INSERT）
        sql_log = text("INSERT INTO query_log (queried_user_id, action_type) VALUES (:uid, 'update')")
        conn.execute(sql_log, {"uid": user_id})
        
        # 3. 一起提交（要么全成功，要么全失败）
        conn.commit()
        
        if result.rowcount > 0:
            return {"message": f"用户 {user_id} 更新成功，已记录日志"}
        else:
            return {"message": f"用户 {user_id} 不存在，更新失败"}


@app.delete("/users/{user_id}")
async def delete_user(user_id: int):
    with engine.connect() as conn:
        # 1. 执行删除操作
        sql_delete = text("DELETE FROM user_actions WHERE user_id = :uid")
        result = conn.execute(sql_delete, {"uid": user_id})
        
        # 2. 记录操作日志（INSERT）
        sql_log = text("INSERT INTO query_log (queried_user_id, action_type) VALUES (:uid, 'delete')")
        conn.execute(sql_log, {"uid": user_id})
        
        # 3. 一起提交
        conn.commit()
        
        if result.rowcount > 0:
            return {"message": f"用户 {user_id} 已删除，已记录日志"}
        else:
            return {"message": f"用户 {user_id} 不存在"}


@app.get("/pages/hot")
async def get_hot_pages():
    with engine.connect() as conn:
        sql = text("""
            SELECT page_url, COUNT(*) as visit_count 
            FROM page_views 
            GROUP BY page_url 
            ORDER BY visit_count DESC 
            LIMIT 5
        """)
        result = conn.execute(sql).fetchall()
        
        hot_list = []
        for row in result:
            hot_list.append({
                "page_url": row[0],
                "visit_count": row[1]
            })
        return {"data": hot_list}

@app.get("/analyze")
async def analyze_visits():
    # 1. 从数据库查出最近的访问数据
    with engine.connect() as conn:
        sql = text("""
            SELECT page_url, COUNT(*) as visit_count 
            FROM page_views 
            GROUP BY page_url 
            ORDER BY visit_count DESC 
            LIMIT 10
        """)
        result = conn.execute(sql).fetchall()
        
        # 2. 把数据整理成文字
        data_text = "网站访问数据如下：\n"
        for row in result:
            data_text += f"- 页面 {row[0]}：被访问 {row[1]} 次\n"
        
        # 3. 调用 DeepSeek API 生成分析
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": "你是一个数据分析助手，请用简洁的中文分析以下网站访问数据，给出2-3条建议。"},
                {"role": "user", "content": data_text}
            ]
        )
        
        analysis = response.choices[0].message.content
        return {"analysis": analysis}


@app.get("/pages/date/{date_str}")
async def get_pages_by_date(date_str: str):
    with engine.connect() as conn:
        sql = text("SELECT id, page_url, visitor_ip, visit_time FROM page_views WHERE DATE(visit_time) = :date ORDER BY id DESC")
        result = conn.execute(sql, {"date": date_str}).fetchall()
        pages_list = []
        for row in result:
            pages_list.append({
                "id": row[0],
                "page_url": row[1],
                "visitor_ip": row[2],
                "visit_time": row[3]
            })
        return {"count": len(pages_list), "data": pages_list}





@app.post("/pages/")
async def create_page_view(request: Request):
    try:
        data = await request.json()
    except Exception:
        return {"error": "无效的 JSON 格式"}, 400

    page_url = data.get("page_url", "/unknown")
    visitor_ip = data.get("visitor_ip", None)
    # 👇 过滤本地路径
    if page_url.startswith("C:") or page_url.startswith("file://") or page_url.startswith("/C:"):
        return {"message": "本地路径已忽略", "page_url": page_url}
    
    # 如果没有传 visitor_ip，就从请求头中获取真实 IP
    if not visitor_ip:
        forwarded = request.headers.get("X-Forwarded-For")
        if forwarded:
            visitor_ip = forwarded.split(",")[0].strip()
        else:
            visitor_ip = request.client.host


    with engine.connect() as conn:
        sql = text("INSERT INTO page_views (page_url, visitor_ip) VALUES (:url, :ip)")
        conn.execute(sql, {"url": page_url, "ip": visitor_ip})
        conn.commit()
        return {"message": "访问记录已保存!", "page_url": page_url, "visitor_ip": visitor_ip}


@app.get("/pages/{page_url}")
async def get_page_stats(page_url: str):
    with engine.connect() as conn:
        sql = text("SELECT COUNT(*) FROM page_views WHERE page_url = :url")
        result = conn.execute(sql, {"url": page_url}).fetchone()
        return {"page_url": page_url, "visit_count": result[0] if result else 0}


@app.get("/pages/date/{date_str}")
async def get_pages_by_date(date_str: str):
    with engine.connect() as conn:
        sql = text("SELECT id, page_url, visitor_ip, visit_time FROM page_views WHERE DATE(visit_time) = :date ORDER BY id DESC")
        result = conn.execute(sql, {"date": date_str}).fetchall()
        pages_list = []
        for row in result:
            pages_list.append({
                "id": row[0], "page_url": row[1],
                "visitor_ip": row[2], "visit_time": row[3]
            })
        return {"count": len(pages_list), "data": pages_list}


