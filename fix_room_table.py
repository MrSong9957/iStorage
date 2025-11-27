import os
import sqlite3
from django.conf import settings

def fix_room_table():
    """
    检查并修复items_room表中缺失的room_name列
    """
    # 获取数据库路径
    db_path = os.path.join(settings.BASE_DIR, 'db.sqlite3')
    
    # 连接到数据库
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # 检查items_room表中是否存在room_name列
        cursor.execute("PRAGMA table_info(items_room)")
        columns = [column[1] for column in cursor.fetchall()]
        
        print(f"当前items_room表的列: {columns}")
        
        # 如果room_name列不存在，则添加该列
        if 'room_name' not in columns:
            print("发现room_name列缺失，正在添加...")
            # 添加room_name列
            cursor.execute("ALTER TABLE items_room ADD COLUMN room_name TEXT NOT NULL DEFAULT ''")
            conn.commit()
            print("成功添加room_name列")
            
            # 可选：如果需要为现有记录设置默认值，使用现有的'name'列值
            print("正在为现有记录设置默认room_name值...")
            cursor.execute("SELECT id, name FROM items_room WHERE room_name = ''")
            rooms = cursor.fetchall()
            
            for room_id, room_name_value in rooms:
                # 使用现有的'name'列值作为room_name的默认值
                cursor.execute("UPDATE items_room SET room_name = ? WHERE id = ?", (room_name_value, room_id))
            
            conn.commit()
            print(f"已更新{len(rooms)}条记录的room_name值")
        else:
            print("room_name列已存在，无需修复")
            
    except Exception as e:
        print(f"修复过程中发生错误: {str(e)}")
        conn.rollback()
    finally:
        # 关闭连接
        conn.close()

if __name__ == "__main__":
    # 设置Django环境
    import django
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
    django.setup()
    
    # 执行修复
    fix_room_table()
