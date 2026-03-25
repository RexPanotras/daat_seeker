import sys
import os

# 添加src目录到Python路径
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from daat_seeker.database import get_db

def test_database():
    print("开始测试数据库...")
    
    # 获取数据库实例
    db = get_db()
    
    # 测试获取所有内容
    print("测试获取所有内容...")
    contents = db.get_all_contents()
    print(f"获取到 {len(contents)} 条内容")
    for content in contents:
        print(f"内容: {content['title']}")
    
    # 测试获取所有学科
    print("测试获取所有学科...")
    subjects = db.get_all_subjects()
    print(f"获取到 {len(subjects)} 个学科")
    for subject in subjects:
        print(f"学科: {subject}")
    
    print("数据库测试完成")

if __name__ == "__main__":
    test_database()
