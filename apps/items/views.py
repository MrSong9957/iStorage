# -*- coding: utf-8 -*-
"""物品应用视图"""

from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView
from django.http import JsonResponse
from django.contrib import messages
from collections import defaultdict
import os

from .models import Item, Category, Navigation
from .forms import ItemForm


@login_required
def deposit_item(request):
    """物品存放视图"""
    if request.method == 'POST':
        form = ItemForm(request.POST, request.FILES)
        if form.is_valid():
            item = form.save(commit=False)
            item.user = request.user
            # 自动生成物品编号（在模型的save方法中实现）
            item.save()
            messages.success(request, '物品已成功存放！')
            return redirect('items:success')
    else:
        form = ItemForm()
    return render(request, 'items/deposit_item.html', {'form': form})


class ItemCreateView(CreateView):
    """物品创建视图（基于类）"""
    model = Item
    form_class = ItemForm
    template_name = 'items/deposit_item.html'  # 使用现有的deposit_item.html模板，避免创建新文件
    success_url = reverse_lazy('items:success')

    def form_valid(self, form):
        """验证表单并保存物品"""
        item = form.save(commit=False)
        item.user = self.request.user
        # 自动生成物品编号（在模型的save方法中实现）
        item.save()
        messages.success(self.request, '物品已成功创建！')
        return super().form_valid(form)


@login_required
def success(request):
    """成功页面视图"""
    return render(request, 'items/success.html')


@login_required
def tag_view(request):
    """标签视图"""
    # 这里可以添加标签相关的功能
    return render(request, 'items/tag_view.html')


def generate_recommendations(user, limit=5):
    """生成推荐的房间和分类"""
    from collections import Counter
    
    # 获取用户的物品
    items = Item.objects.filter(user=user)
    
    # 生成推荐房间
    room_counter = Counter(item.location for item in items if item.location)
    recommended_rooms = [room for room, count in room_counter.most_common(limit)]
    
    # 生成推荐分类
    category_counter = Counter(item.category.name for item in items if item.category)
    recommended_categories = [category for category, count in category_counter.most_common(limit)]
    
    return {
        'rooms': recommended_rooms,
        'categories': recommended_categories
    }


@login_required
def find_items(request):
    """查找物品页面视图"""
    # 处理筛选条件
    filter_type = request.GET.get('filter', 'room')
    # 获取分类筛选参数
    category_filter = request.GET.get('category', None)
    
    # 获取用户的物品
    items = Item.objects.filter(user=request.user).select_related('category')
    
    # 应用分类筛选
    if category_filter:
        if filter_type == 'room':
            # 按房间筛选
            items = items.filter(location=category_filter)
        else:
            # 按分类筛选
            if category_filter == '未分类':
                items = items.filter(category__isnull=True)
            else:
                items = items.filter(category__name=category_filter)
    
    # 按房间或分类分组
    grouped_items = defaultdict(list)
    
    if filter_type == 'category':
        # 按分类分组
        for item in items:
            category = item.category.name if item.category else "未分类"
            grouped_items[category].append(item)
    elif filter_type == 'room':
        # 按房间分组
        for item in items:
            room = item.location or "未指定"
            grouped_items[room].append(item)
    
    # 转换为普通字典，确保模板能够正确判断是否为空
    grouped_items = dict(grouped_items)
    
    # 统计数据
    total_items = items.count()
    categories = Category.objects.filter(user=request.user)
    category_count = categories.count()
    
    # 统计房间数 - 直接从所有物品中获取唯一房间列表
    # 先获取所有物品的房间名称，然后进行彻底的清理和去重
    all_rooms = Item.objects.filter(user=request.user).values_list('location', flat=True).exclude(location__isnull=True).exclude(location='')
    
    # 彻底清理和去重：
    # 1. 去除首尾空格
    # 2. 去除所有不可见字符
    # 3. 考虑大小写不敏感进行去重，但保留原始大小写
    cleaned_rooms_dict = {}
    for room in all_rooms:
        # 去除首尾空格
        cleaned_room = room.strip()
        # 去除所有不可见字符
        cleaned_room = cleaned_room.replace('\n', '').replace('\t', '').replace('\r', '')
        # 只处理非空值
        if cleaned_room:
            # 使用小写作为键进行去重，但保留原始值
            cleaned_rooms_dict[cleaned_room.lower()] = cleaned_room
    
    # 转换为列表并排序
    rooms = sorted(list(cleaned_rooms_dict.values()))
    room_count = len(rooms)
    
    # 生成推荐数据
    recommendations = generate_recommendations(request.user)
    
    # 获取导航数据
    main_navs = Navigation.objects.filter(user=request.user, type='main').order_by('order')
    
    # 获取当前活动的主导航
    active_main = None
    for nav in main_navs:
        if request.path == nav.url:
            active_main = nav
            break
    
    # 获取当前主导航的子标签
    sub_navs = []
    if active_main:
        sub_navs = active_main.children.filter(user=request.user).order_by('order')
    
    # 获取当前活动的子标签
    active_sub_tag = request.GET.get('sub_tag', '')
    
    return render(request, 'items/find_items_base.html', {
        'grouped_items': grouped_items,
        'items': items,
        'total_items': total_items,
        'categories': categories,
        'category_count': category_count,
        'room_count': room_count,
        'filter_type': filter_type,
        'category_filter': category_filter,
        'recommended_rooms': recommendations['rooms'],
        'recommended_categories': recommendations['categories'],
        'all_categories': categories,
        'all_rooms': rooms,
        'main_navs': main_navs,
        'sub_navs': sub_navs,
        'active_sub_tag': active_sub_tag
    })


@login_required
def add_category(request):
    """添加新分类API"""
    if request.method == 'POST':
        name = request.POST.get('name')
        if name:
            category, created = Category.objects.get_or_create(
                user=request.user,
                name=name
            )
            return JsonResponse({'success': True, 'category': {'id': category.id, 'name': category.name}})
    return JsonResponse({'success': False, 'error': 'Invalid request'})


@login_required
def add_room(request):
    """添加新房间API"""
    if request.method == 'POST':
        name = request.POST.get('name')
        if name:
            # 房间直接存储在物品的location字段中，不需要单独的模型
            return JsonResponse({'success': True, 'room': name})
    return JsonResponse({'success': False, 'error': 'Invalid request'})


@login_required
def test_find_items(request):
    """测试查找物品功能"""
    # 这里可以添加测试查找功能的代码
    return render(request, 'items/test_find_items.html')


@login_required
def item_detail(request, item_id):
    """物品详情页视图，支持返回模态框片段"""
    item = get_object_or_404(Item, id=item_id, user=request.user)
    
    # 如果是POST请求，处理物品更新
    if request.method == 'POST':
        # 处理表单数据
        item.name = request.POST.get('name', item.name)
        item.location = request.POST.get('location', item.location)
        
        # 处理图片上传
        if 'image' in request.FILES:
            # 删除旧图片
            if item.image and os.path.exists(item.image.path):
                os.remove(item.image.path)
            item.image = request.FILES['image']
        
        item.save()
        return JsonResponse({'success': True, 'item': {'id': item.id, 'name': item.name, 'location': item.location}})
    
    # 如果是GET请求，根据是否有modal参数决定渲染完整页面还是模态框片段
    if request.GET.get('modal') == '1':
        return render(request, 'items/_item_modal.html', {'item': item})
    else:
        return render(request, 'items/item_detail.html', {'item': item})


@login_required
def delete_item(request, item_id):
    """删除物品API"""
    item = get_object_or_404(Item, id=item_id, user=request.user)
    # 删除物品图片（如果存在）
    if item.image and os.path.exists(item.image.path):
        os.remove(item.image.path)
    item.delete()
    return JsonResponse({'success': True})


@login_required
def update_item_location(request, item_id):
    """更新物品位置API"""
    item = get_object_or_404(Item, id=item_id, user=request.user)
    if request.method == 'POST':
        new_location = request.POST.get('location', '')
        item.location = new_location
        item.save()
        return JsonResponse({'success': True, 'location': new_location})
    return JsonResponse({'success': False, 'error': 'Invalid request method'})


@login_required
def get_items_by_category(request):
    """根据分类获取物品API"""
    # 获取分类参数
    category = request.GET.get('category', '')
    # 获取过滤类型
    filter_type = request.GET.get('filter_type', 'room')
    
    # 参数校验
    if not category:
        return JsonResponse({'success': False, 'error': '分类参数不能为空'})
    
    try:
        # 根据过滤类型和分类参数查询数据
        if filter_type == 'room':
            # 按房间查询
            items = Item.objects.filter(user=request.user, location=category).select_related('category')
        else:
            # 按分类查询
            items = Item.objects.filter(user=request.user, category__name=category).select_related('category')
        
        # 构建返回数据
        item_list = []
        for item in items:
            item_list.append({
                'id': item.id,
                'name': item.name,
                'location': item.location,
                'category': item.category.name if item.category else '未分类',
                'item_code': item.item_code,
                'image': item.image.url if item.image else None
            })
        
        return JsonResponse({
            'success': True,
            'data': item_list,
            'category': category,
            'count': len(item_list)
        })
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})


@login_required
def manage_navigation(request):
    """管理导航项API"""
    if request.method == 'POST':
        action = request.POST.get('action')
        
        # 添加导航项
        if action == 'add':
            parent_id = request.POST.get('parent_id')
            name = request.POST.get('name')
            url = request.POST.get('url')
            icon = request.POST.get('icon')
            
            # 验证数据
            if not name or not url or not icon:
                return JsonResponse({'success': False, 'error': '缺少必填字段'})
            
            try:
                # 创建导航项
                nav = Navigation(
                    user=request.user,
                    name=name,
                    url=url,
                    icon=icon,
                    type='sub',
                    parent_id=parent_id if parent_id else None
                )
                nav.save()
                return JsonResponse({'success': True, 'nav': {
                    'id': nav.id,
                    'name': nav.name,
                    'url': nav.url,
                    'icon': nav.icon
                }})
            except Exception as e:
                return JsonResponse({'success': False, 'error': str(e)})
        
        # 编辑导航项
        elif action == 'edit':
            nav_id = request.POST.get('nav_id')
            name = request.POST.get('name')
            url = request.POST.get('url')
            icon = request.POST.get('icon')
            
            # 验证数据
            if not nav_id or not name or not url or not icon:
                return JsonResponse({'success': False, 'error': '缺少必填字段'})
            
            try:
                # 更新导航项
                nav = Navigation.objects.get(id=nav_id, user=request.user)
                nav.name = name
                nav.url = url
                nav.icon = icon
                nav.save()
                return JsonResponse({'success': True, 'nav': {
                    'id': nav.id,
                    'name': nav.name,
                    'url': nav.url,
                    'icon': nav.icon
                }})
            except Navigation.DoesNotExist:
                return JsonResponse({'success': False, 'error': '导航项不存在'})
            except Exception as e:
                return JsonResponse({'success': False, 'error': str(e)})
        
        # 删除导航项
        elif action == 'delete':
            nav_id = request.POST.get('nav_id')
            
            if not nav_id:
                return JsonResponse({'success': False, 'error': '缺少导航项ID'})
            
            try:
                nav = Navigation.objects.get(id=nav_id, user=request.user)
                nav.delete()
                return JsonResponse({'success': True})
            except Navigation.DoesNotExist:
                return JsonResponse({'success': False, 'error': '导航项不存在'})
            except Exception as e:
                return JsonResponse({'success': False, 'error': str(e)})
        
    return JsonResponse({'success': False, 'error': '无效的请求方法或操作'})


@login_required
def manage_categories(request):
    """管理分类和房间视图"""
    # 获取用户的所有分类
    categories = Category.objects.filter(user=request.user)
    
    # 获取用户的所有房间，去除空值并去重
    rooms = list(set(Item.objects.filter(user=request.user).values_list('location', flat=True).exclude(location__isnull=True).exclude(location='')))
    
    # 处理POST请求
    if request.method == 'POST':
        # 处理分类删除
        if 'delete_category' in request.POST:
            category_id = request.POST.get('category_id')
            if category_id:
                Category.objects.filter(id=category_id, user=request.user).delete()
        
        # 处理房间删除
        elif 'delete_room' in request.POST:
            room_name = request.POST.get('room_name')
            if room_name:
                # 将使用该房间的物品的location设为''
                Item.objects.filter(user=request.user, location=room_name).update(location='')
        
        # 处理分类更新
        elif 'update_category' in request.POST:
            category_id = request.POST.get('category_id')
            new_name = request.POST.get('new_name')
            if category_id and new_name:
                Category.objects.filter(id=category_id, user=request.user).update(name=new_name)
        
        # 处理房间更新
        elif 'update_room' in request.POST:
            old_name = request.POST.get('old_name')
            new_name = request.POST.get('new_name')
            if old_name and new_name:
                # 更新使用该房间的物品的location
                Item.objects.filter(user=request.user, location=old_name).update(location=new_name)
        
        # 重定向回管理分类页面
        return redirect('items:manage_categories')
    
    # 获取导航数据
    main_navs = Navigation.objects.filter(user=request.user, type='main').order_by('order')
    
    # 获取当前活动的主导航
    active_main = None
    for nav in main_navs:
        if request.path == nav.url:
            active_main = nav
            break
    
    # 获取当前主导航的子标签
    sub_navs = []
    if active_main:
        sub_navs = active_main.children.filter(user=request.user).order_by('order')
    
    # 获取当前活动的子标签
    active_sub_tag = request.GET.get('sub_tag', '')
    
    # 为find_items_base.html模板提供必要的上下文数据
    # 获取所有物品
    items = Item.objects.filter(user=request.user)
    # 物品总数
    total_items = items.count()
    # 分类数量
    category_count = categories.count()
    # 房间数量
    room_count = len(rooms)
    # 筛选类型 - 管理分类页面默认使用'category'
    filter_type = 'category'
    # 生成推荐数据
    recommendations = generate_recommendations(request.user)
    # 空的分组物品，因为管理分类页面不需要分组显示
    grouped_items = {}
    
    return render(request, 'items/manage_categories.html', {
        'categories': categories,
        'rooms': rooms,
        'main_navs': main_navs,
        'sub_navs': sub_navs,
        'active_sub_tag': active_sub_tag,
        # 以下是find_items_base.html模板所需的数据
        'grouped_items': grouped_items,
        'items': items,
        'total_items': total_items,
        'category_count': category_count,
        'room_count': room_count,
        'filter_type': filter_type,
        'recommended_rooms': recommendations['rooms'],
        'recommended_categories': recommendations['categories'],
        'all_categories': categories,
        'all_rooms': rooms
    })

