import sqlite3
import os

import os

class Database:
    def __init__(self, db_path=None):
        # 使用绝对路径，确保数据库文件位置正确
        if db_path is None:
            # 获取当前文件所在目录的绝对路径
            current_dir = os.path.dirname(os.path.abspath(__file__))
            # 数据库文件放在backend目录下
            self.db_path = os.path.join(current_dir, '..', '..', 'daat_seeker.db')
        else:
            self.db_path = db_path
        # 确保目录存在
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        self.conn = None
        self.cursor = None

    def connect(self):
        """连接数据库"""
        try:
            print(f"正在连接数据库: {self.db_path}")
            self.conn = sqlite3.connect(self.db_path)
            self.cursor = self.conn.cursor()
            print("数据库连接成功")
            return True
        except Exception as e:
            print(f"Failed to connect to database: {e}")
            return False

    def close(self):
        """关闭数据库连接"""
        if self.conn:
            self.conn.close()

    def create_tables(self):
        """创建表"""
        try:
            # 创建内容表
            self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS contents (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT NOT NULL,
                interface TEXT,
                subject TEXT NOT NULL,
                tags TEXT NOT NULL,
                type TEXT NOT NULL DEFAULT 'question'
            )
            ''')

            # 创建标签表
            self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS tags (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                color TEXT NOT NULL
            )
            ''')

            # 创建学科表
            self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS subjects (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE
            )
            ''')

            self.conn.commit()
            return True
        except Exception as e:
            print(f"Failed to create tables: {e}")
            return False

    def insert_initial_data(self):
        """插入初始数据"""
        try:
            print("开始插入初始数据...")
            
            # 检查标签表是否为空
            self.cursor.execute("SELECT COUNT(*) FROM tags")
            count = self.cursor.fetchone()[0]
            print(f"标签表行数: {count}")

            # 如果标签表为空，插入初始标签
            if count == 0:
                print("插入初始标签...")
                self.cursor.executemany('''
                INSERT INTO tags (name, color) VALUES (?, ?)
                ''', [
                    ('数学', '#4CAF50'),
                    ('物理学', '#2196F3'),
                    ('计算机科学', '#FF9800')
                    #('调和级数', '#9C27B0'),
                    #('洛伦兹变换', '#F44336')
                ])
                print("标签插入完成")

            # 检查学科表是否为空
            self.cursor.execute("SELECT COUNT(*) FROM subjects")
            count = self.cursor.fetchone()[0]
            print(f"学科表行数: {count}")

            # 如果学科表为空，插入初始学科
            if count == 0:
                print("插入初始学科...")
                self.cursor.executemany('''
                INSERT INTO subjects (name) VALUES (?)
                ''', [
                    ('数学',),
                    ('物理学',),
                    ('化学',),
                    ('生物学',),
                    ('计算机科学',),
                    ('地理学',),
                    ('逻辑学',)
                ])
                print("学科插入完成")

            # 清空内容表并重新插入初始内容
            print("清空内容表...")
            self.cursor.execute("DELETE FROM contents")
            print("插入初始内容...")
            self.cursor.executemany('''
            INSERT INTO contents (title, description, interface, subject, tags, type) VALUES (?, ?, ?, ?, ?, ?)
            ''', [
                ('计算调和级数', '调和级数是发散的。虽然其增长速度非常缓慢（近似于ln(n)+γ，其中γ≈0.5772是欧拉-马歇罗尼常数），但随着n增大，其和会无限增大。这是数学分析中的经典结论，由中世纪数学家尼克尔·奥雷姆（Nicole Oresme）首次证明。', 'harmonic', '数学', '数学,调和级数', 'question'),
                ('洛伦兹变换', '洛伦兹变换是狭义相对论的核心，描述了两个惯性参考系之间的时空坐标转换。它基于两个基本假设：相对性原理和光速不变原理。洛伦兹变换已被无数实验验证，包括粒子加速器中的时间膨胀效应、GPS卫星的时间校正等。', 'lorentz', '物理学', '物理学,洛伦兹变换', 'question'),
                ('计算1~n的和', '计算1~n的和是一个简单的数学问题，它等于n的前n个自然数的和。例如，1+2+3+...+n=n(n+1)/2。当n趋于无穷时，此求和也趋于无穷，并不收敛至-1/12。', 'sum', '数学', '数学,1~n的和', 'question')   
            ])
            print("内容插入完成")

            self.conn.commit()
            print("初始数据插入成功")
            return True
        except Exception as e:
            print(f"Failed to insert initial data: {e}")
            return False

    def _ensure_connection(self):
        """确保数据库连接正常"""
        if not self.conn:
            return self.connect()
        try:
            # 通过执行一个简单的查询来检查连接是否正常
            self.cursor.execute("SELECT 1")
            return True
        except:
            # 如果查询失败，重新连接
            return self.connect()

    def get_all_contents(self):
        """获取所有内容"""
        try:
            print("开始获取所有内容...")
            if not self._ensure_connection():
                print("连接失败，返回空列表")
                return []
            print("执行查询: SELECT id, title, description, interface, subject, tags, type FROM contents")
            self.cursor.execute("SELECT id, title, description, interface, subject, tags, type FROM contents")
            rows = self.cursor.fetchall()
            print(f"获取到 {len(rows)} 条内容")
            for row in rows:
                print(f"内容: {row[1]}")
            contents = []
            for row in rows:
                contents.append({
                    'id': row[0],
                    'title': row[1],
                    'description': row[2],
                    'interface': row[3],
                    'subject': row[4],
                    'tags': row[5],
                    'type': row[6]
                })
            print(f"返回 {len(contents)} 条内容")
            return contents
        except Exception as e:
            print(f"Failed to get all contents: {e}")
            import traceback
            traceback.print_exc()
            return []

    def get_content_by_id(self, id):
        """根据ID获取内容"""
        try:
            if not self._ensure_connection():
                return None
            self.cursor.execute("SELECT id, title, description, interface, subject, tags, type FROM contents WHERE id = ?", (id,))
            row = self.cursor.fetchone()
            if row:
                return {
                    'id': row[0],
                    'title': row[1],
                    'description': row[2],
                    'interface': row[3],
                    'subject': row[4],
                    'tags': row[5],
                    'type': row[6]
                }
            return None
        except Exception as e:
            print(f"Failed to get content by id: {e}")
            return None

    def get_all_subjects(self):
        """获取所有学科"""
        try:
            if not self._ensure_connection():
                return []
            self.cursor.execute("SELECT name FROM subjects")
            rows = self.cursor.fetchall()
            subjects = [row[0] for row in rows]
            return subjects
        except Exception as e:
            print(f"Failed to get all subjects: {e}")
            return []

    def get_contents_by_subject(self, subject):
        """根据学科获取内容"""
        try:
            if not self._ensure_connection():
                return []
            self.cursor.execute("SELECT id, title, description, interface, subject, tags, type FROM contents WHERE subject = ?", (subject,))
            rows = self.cursor.fetchall()
            contents = []
            for row in rows:
                contents.append({
                    'id': row[0],
                    'title': row[1],
                    'description': row[2],
                    'interface': row[3],
                    'subject': row[4],
                    'tags': row[5],
                    'type': row[6]
                })
            return contents
        except Exception as e:
            print(f"Failed to get contents by subject: {e}")
            return []

    def get_all_tags(self):
        """获取所有标签"""
        try:
            if not self._ensure_connection():
                return []
            self.cursor.execute("SELECT id, name, color FROM tags")
            rows = self.cursor.fetchall()
            tags = []
            for row in rows:
                tags.append({
                    'id': row[0],
                    'name': row[1],
                    'color': row[2]
                })
            return tags
        except Exception as e:
            print(f"Failed to get all tags: {e}")
            return []

    def init_db(self):
        """初始化数据库"""
        if self.connect():
            if self.create_tables():
                if self.insert_initial_data():
                    print("Database initialized successfully")
                    return True
        return False

# 全局数据库实例
db_instance = None

def get_db():
    """获取数据库实例"""
    global db_instance
    if db_instance is None:
        db_instance = Database()
        db_instance.connect()
        # 确保数据库已初始化
        db_instance.init_db()
    else:
        # 确保连接正常
        db_instance._ensure_connection()
    return db_instance
