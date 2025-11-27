#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""创建缺失的数据库表"""

import os
import django

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.db import connection

# 要创建的表的SQL语句（SQLite兼容）
create_storagecell_table = """
CREATE TABLE IF NOT EXISTS `items_storagecell` (
    `id` INTEGER PRIMARY KEY AUTOINCREMENT,
    `cell_number` INTEGER NOT NULL,
    `cell_id` VARCHAR(7) NOT NULL,
    `qr_code` BLOB NOT NULL,
    `room_id` INTEGER NOT NULL,
    `furniture_id` INTEGER NOT NULL,
    `user_id` INTEGER NOT NULL,
    UNIQUE(`cell_id`),
    UNIQUE(`room_id`, `furniture_id`, `cell_number`),
    FOREIGN KEY (`room_id`) REFERENCES `items_room` (`id`),
    FOREIGN KEY (`furniture_id`) REFERENCES `items_furniture` (`id`),
    FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
);
"""

create_item_storagecells_table = """
CREATE TABLE IF NOT EXISTS `items_item_storage_cells` (
    `id` INTEGER PRIMARY KEY AUTOINCREMENT,
    `item_id` INTEGER NOT NULL,
    `storagecell_id` INTEGER NOT NULL,
    UNIQUE(`item_id`, `storagecell_id`),
    FOREIGN KEY (`item_id`) REFERENCES `items_item` (`id`),
    FOREIGN KEY (`storagecell_id`) REFERENCES `items_storagecell` (`id`)
);
"""

# 执行SQL命令
with connection.cursor() as cursor:
    try:
        # 创建StorageCell表
        cursor.execute(create_storagecell_table)
        print("StorageCell表创建成功")
        
        # 创建Item与StorageCell的多对多关联表
        cursor.execute(create_item_storagecells_table)
        print("Item与StorageCell的关联表创建成功")
        
        print("所有缺失的表已创建完成")
    except Exception as e:
        print(f"创建表时出错: {e}")
