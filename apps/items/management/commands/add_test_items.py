# -*- coding: utf-8 -*-
"""添加测试物品数据的管理命令"""

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.utils import timezone
import random

from apps.items.models import Item, Category


class Command(BaseCommand):
    """添加测试物品数据的命令"""
    help = 'Adds 50 test items with random data to the database'
    
    def handle(self, *args, **kwargs):
        """处理命令"""
        # 获取用户模型
        User = get_user_model()
        
        # 获取所有用户
        users = User.objects.all()
        if not users:
            self.stdout.write(self.style.ERROR('No users found. Please create a user first.'))
            return
        
        # 预定义物品名称前缀
        item_prefixes = ['手机', '电脑', '桌子', '椅子', '电视', '冰箱', '洗衣机', '空调', '书', '笔', '杯子', '盘子', '刀', '叉', '勺子', '毛巾', '衣服', '裤子', '鞋子', '帽子', '手套', '围巾', '眼镜', '手表', '钱包', '钥匙', '雨伞', '背包', '行李箱', '玩具', '球', '球拍', '哑铃', '跑步机', '自行车', '汽车', '飞机', '火车', '船', '相机', '镜头', '三脚架', '麦克风', '音响', '耳机', '键盘', '鼠标', '显示器', '打印机', '扫描仪', '路由器', '交换机', '服务器', '硬盘', 'U盘', '光盘', '磁带', '电池', '充电器', '数据线', '插座', '开关', '灯泡', '风扇', '电暖器', '电饭煲', '电磁炉', '微波炉', '烤箱', '洗碗机', '消毒柜', '抽油烟机', '燃气灶', '热水器', '太阳能', '净水器', '空气净化器', '加湿器', '除湿器', '吸尘器', '扫地机器人', '拖把', '扫帚', '簸箕', '垃圾桶', '垃圾袋', '纸巾', '毛巾', '牙刷', '牙膏', '洗发水', '沐浴露', '护发素', '洗面奶', '面霜', '爽肤水', '乳液', '防晒霜', '口红', '眼影', '腮红', '粉底', '遮瑕', '眉笔', '睫毛膏', '眼线笔', '香水', '指甲油', '卸妆水', '面膜', '护手霜', '身体乳', '润唇膏', '香皂', '肥皂', '洗衣粉', '洗衣液', '柔顺剂', '洗洁精', '消毒液', '漂白剂', '除臭剂', '杀虫剂', '蚊香', '花露水', '创可贴', '消毒液', '感冒药', '退烧药', '消炎药', '止痛药', '胃药', '眼药水', '药膏', '绷带', '体温计', '血压计', '血糖仪', '听诊器', '口罩', '手套', '护目镜', '防护服', '鞋套', '帽子', '围巾', '手套', '口罩', '护膝', '护肘', '护腕', '头盔', '安全带', '救生衣', '灭火器', '消防栓', '烟雾报警器', '温度计', '湿度计', '气压计', '风速计', '雨量计', '指南针', '地图', 'GPS', '望远镜', '显微镜', '放大镜', '眼镜', '隐形眼镜', '老花镜', '太阳镜', '游泳镜', '滑雪镜', '潜水镜', '护目镜', '安全帽', '安全鞋', '安全手套', '安全腰带', '安全网', '防护栏', '防护门', '防护窗', '防护栏', '防护网', '防护门', '防护窗', '防护栏', '防护网', '防护门', '防护窗']
        
        # 预定义房间列表
        rooms = ['客厅', '卧室', '厨房', '卫生间', '书房', '阳台', '储物间', '车库', '阁楼', '地下室']
        
        # 预定义分类列表
        categories = ['电子设备', '家具', '衣物', '书籍', '厨房用品', '装饰品', '运动器材', '工具', '玩具', '其他']
        
        # 为每个用户添加测试物品
        for user in users:
            # 为当前用户创建分类
            for category_name in categories:
                Category.objects.get_or_create(name=category_name, user=user)
            
            # 生成并添加50个物品
            for i in range(50):
                # 生成随机物品名称
                item_name = random.choice(item_prefixes) + random.choice(['', ' 1', ' 2', ' 3', ' Pro', ' Air', ' Mini', ' Max'])
                
                # 随机选择房间
                room = random.choice(rooms)
                
                # 创建物品
                try:
                    # 使用原始SQL直接插入数据，避免Django ORM的类型检查
                    from django.db import connection
                    
                    # 生成唯一的item_code和当前时间
                    import time
                    new_item_code = int(time.time() * 1000000) + i
                    current_time = timezone.now()
                    
                    # 执行原始SQL插入
                    with connection.cursor() as cursor:
                        cursor.execute(
                            "INSERT INTO items_item (item_code, name, location, storage_time, user_id) VALUES (%s, %s, %s, %s, %s)",
                            [new_item_code, item_name, room, current_time, user.id]
                        )
                    
                    self.stdout.write(self.style.SUCCESS(f'Added item: {item_name} (Room: {room}, Code: {new_item_code}, User: {user.username})'))
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f'Error adding item for user {user.username}: {e}'))
        
        self.stdout.write(self.style.SUCCESS(f'Successfully added 50 test items for all users'))
