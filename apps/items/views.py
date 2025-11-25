# -*- coding: utf-8 -*-
"""物品应用视图"""

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.http import JsonResponse
import qrcode
from PIL import Image
import datetime
import random
import base64
import io
import json
from .models import Item, Storage

def generate_item_code():
    """
    生成物品编号：前缀+时间戳+随机数
    格式：ITEM-20240520-10086
    """
    prefix = 'ITEM'
    timestamp = datetime.datetime.now().strftime('%Y%m%d')
    random_num = str(random.randint(10000, 99999))
    return f"{prefix}-{timestamp}-{random_num}"

@login_required
def deposit_item(request):
    """
    物品录入视图 - 极简化版本，仅处理物品名称和图片字段的录入（二选一）
    """
    if request.method == 'POST':
        # 简化处理：直接从请求中获取必要字段
        name = request.POST.get('name')
        image = request.FILES.get('image')
        
        # 二选一验证：名称或图片至少有一个不为空
        if not name and not image:
            return redirect('items:deposit')
        
        try:
            # 生成唯一的物品编号
            item_code = generate_item_code()
            
            # 直接创建物品实例
            item = Item(
                item_code=item_code,
                name=name or '未命名物品',
                description='',  # 简化版本，不使用描述
                category='others',  # 默认为其他类别
                value=0.0,  # 简化版本，不使用价值
                location='',  # 简化版本，不使用位置
                notes='',  # 简化版本，不使用备注
                image=image,
                user=request.user
            )
            
            # 生成二维码
            qr_data = json.dumps({
                'code': item.item_code,
                'name': item.name,
                'category': 'item'
            })
            
            # 创建二维码
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            qr.add_data(qr_data)
            qr.make(fit=True)
            
            # 生成二维码图片
            qr_image = qr.make_image(fill_color="black", back_color="white")
            
            # 将图片转换为base64编码
            buffer = io.BytesIO()
            qr_image.save(buffer, format="PNG")
            qr_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
            
            # 保存二维码到物品
            item.qr_code = qr_base64
            item.save()
            return redirect('items:deposit')
        except Exception as e:
            return redirect('items:deposit')
    else:
        # GET请求通常不会直接访问这个视图，因为表单在模态窗口中
        # 但如果直接访问，返回items:deposit
        return redirect('items:deposit')

class ItemCreateView(CreateView):
    """
    基于类的物品录入视图 - 独立页面版本
    """
    model = Item
    fields = ['name', 'description', 'category', 'value', 'location', 'notes', 'image']
    template_name = 'items/deposit_item.html'
    success_url = reverse_lazy('items:success')
    
    def form_valid(self, form):
        # 设置用户和生成物品编号
        item = form.save(commit=False)
        item.user = self.request.user
        item.item_code = generate_item_code()
        
        # 生成二维码
        qr_data = json.dumps({
            'code': item.item_code,
            'name': item.name,
            'category': 'item'
        })
        
        # 创建二维码
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(qr_data)
        qr.make(fit=True)
        
        # 生成二维码图片
        qr_image = qr.make_image(fill_color="black", back_color="white")
        
        # 将图片转换为base64编码
        buffer = io.BytesIO()
        qr_image.save(buffer, format="PNG")
        qr_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
        
        # 保存二维码到物品
        item.qr_code = qr_base64
        
        return super().form_valid(form)
    
    def get_form_kwargs(self):
        # 移除user参数，因为ItemForm不接受这个参数
        kwargs = super().get_form_kwargs()
        return kwargs

@login_required
def success(request):
    """
    物品录入成功页面
    """
    return render(request, 'items/success.html')

@login_required
def generate_tag(request):
    """
    生成标签数据的API接口
    返回物品信息和二维码的base64编码
    """
    if request.method == 'POST':
        try:
            # 生成新的物品编号
            item_code = generate_item_code()
            name = request.POST.get('name', '未命名物品')
            
            # 生成二维码数据（包含物品编号和名称信息）
            qr_data = json.dumps({
                'item_code': item_code,
                'name': name
            })
            
            # 创建二维码
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            qr.add_data(qr_data)
            qr.make(fit=True)
            
            # 生成二维码图片
            qr_image = qr.make_image(fill_color="black", back_color="white")
            
            # 将图片转换为base64编码
            buffer = io.BytesIO()
            qr_image.save(buffer, format="PNG")
            qr_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
            
            # 返回JSON响应
            return JsonResponse({
                'success': True,
                'item_code': item_code,
                'name': name,
                'qr_code': qr_base64
            })
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            })
    
    # 非POST请求返回错误
    return JsonResponse({
        'success': False,
        'error': '只支持POST请求'
    })

from .models import Item

@login_required
def tag_view(request):
    """
    标签展示和打印页面视图
    接收物品信息，展示标签并提供打印功能和标签录入功能
    """
    if request.method == 'POST':
        # 处理标签录入请求
        if request.POST.get('action') == 'save_tag':
            # 获取标签信息
            name = request.POST.get('name', '未命名物品')
            item_code = request.POST.get('item_code')
            category = request.POST.get('category', 'item')
            
            try:
                if category == 'storage':
                    # 检查储物格编号是否已存在
                    if Storage.objects.filter(storage_code=item_code).exists():
                        return JsonResponse({'success': False, 'message': '该储物格编号已存在！'})
                    
                    # 创建新储物格记录
                    storage_data = {
                        'name': name,
                        'storage_code': item_code,
                        'user': request.user
                    }
                    
                    new_storage = Storage.objects.create(**storage_data)
                    return JsonResponse({'success': True, 'message': '储物格标签录入成功！'})
                else:
                    # 检查物品编号是否已存在
                    if Item.objects.filter(item_code=item_code).exists():
                        return JsonResponse({'success': False, 'message': '该物品编号已存在！'})
                    
                    # 创建新物品记录
                    item_data = {
                        'name': name,
                        'item_code': item_code,
                        'category': 'others',  # 默认分类为'其他'
                        'location': '待分配',  # 默认位置
                        'user': request.user
                    }
                    
                    new_item = Item.objects.create(**item_data)
                    
                    # 生成二维码
                    qr_data = json.dumps({
                        'code': new_item.item_code,
                        'name': new_item.name,
                        'category': 'item'
                    })
                    
                    # 创建二维码
                    qr = qrcode.QRCode(
                        version=1,
                        error_correction=qrcode.constants.ERROR_CORRECT_L,
                        box_size=10,
                        border=4,
                    )
                    qr.add_data(qr_data)
                    qr.make(fit=True)
                    
                    # 生成二维码图片
                    qr_image = qr.make_image(fill_color="black", back_color="white")
                    
                    # 将图片转换为base64编码
                    buffer = io.BytesIO()
                    qr_image.save(buffer, format="PNG")
                    qr_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
                    
                    # 保存二维码到物品
                    new_item.qr_code = qr_base64
                    new_item.save()
                    
                    return JsonResponse({'success': True, 'message': '物品标签录入成功！'})
            except Exception as e:
                return JsonResponse({'success': False, 'message': str(e)})
        
        # 原有的标签展示逻辑
        # 获取物品信息
        name = request.POST.get('name', '未命名物品')
        item_code = request.POST.get('item_code')
        image = request.FILES.get('image')
        category = request.POST.get('category', 'item')
        
        # 为储物格生成特殊前缀的编号
        if not item_code:
            if category == 'storage':
                # 储物格编号：STORAGE-日期-随机数
                prefix = 'STORAGE'
                timestamp = datetime.datetime.now().strftime('%Y%m%d')
                random_num = str(random.randint(10000, 99999))
                item_code = f"{prefix}-{timestamp}-{random_num}"
            else:
                item_code = generate_item_code()
        
        # 生成二维码数据，根据类别包含不同信息
        qr_data = json.dumps({
            'code': item_code,
            'name': name,
            'category': category
        })
        
        # 创建二维码
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(qr_data)
        qr.make(fit=True)
        
        # 生成二维码图片
        qr_image = qr.make_image(fill_color="black", back_color="white")
        
        # 将图片转换为base64编码
        buffer = io.BytesIO()
        qr_image.save(buffer, format="PNG")
        qr_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
        
        # 获取来源信息，默认为item_create
        source = request.POST.get('source', 'item_create')
        
        # 准备上下文数据
        context = {
            'name': name,
            'item_code': item_code,
            'qr_code': qr_base64,
            'has_image': image is not None,
            'source': source,
            'category': category
        }
        
        return render(request, 'items/tag_view.html', context)
    
    # GET请求重定向到物品录入页面
    return redirect('items:item_create')

@login_required
def associate_item_storage(request):
    """
    关联物品和储物格视图
    用于通过扫描二维码建立物品与储物格之间的关联
    """
    if request.method == 'POST':
        try:
            # 获取扫描的二维码数据
            qr_data = json.loads(request.POST.get('qr_data', '{}'))
            code = qr_data.get('code')
            category = qr_data.get('category', 'item')
            
            # 获取当前会话中的临时数据
            session_data = request.session.get('association_data', {})
            
            if category == 'item':
                # 查找物品
                item = Item.objects.filter(item_code=code, user=request.user).first()
                if not item:
                    return JsonResponse({'success': False, 'message': '未找到该物品，请确认标签正确'})
                
                # 保存物品信息到会话
                session_data['item'] = {
                    'code': item.item_code,
                    'name': item.name
                }
                
                # 检查是否已有储物格信息
                if 'storage' in session_data:
                    # 找到储物格
                    storage = Storage.objects.filter(storage_code=session_data['storage']['code'], user=request.user).first()
                    if storage:
                        # 建立关联
                        item.storages.add(storage)
                        # 更新物品位置信息，确保格式为房间-家具-储物格
                        item.location = storage.name
                        item.save()
                        # 清空会话数据
                        request.session.pop('association_data', None)
                        return JsonResponse({
                            'success': True, 
                            'message': f'成功将物品「{item.name}」关联到储物格「{storage.name}」',
                            'complete': True
                        })
                
                request.session['association_data'] = session_data
                return JsonResponse({
                    'success': True, 
                    'message': f'物品「{item.name}」已识别，请扫描储物格标签',
                    'complete': False
                })
            
            else:  # category == 'storage'
                # 查找储物格
                storage = Storage.objects.filter(storage_code=code, user=request.user).first()
                if not storage:
                    return JsonResponse({'success': False, 'message': '未找到该储物格，请确认标签正确'})
                
                # 保存储物格信息到会话
                session_data['storage'] = {
                    'code': storage.storage_code,
                    'name': storage.name
                }
                
                # 检查是否已有物品信息
                if 'item' in session_data:
                    # 找到物品
                    item = Item.objects.filter(item_code=session_data['item']['code'], user=request.user).first()
                    if item:
                        # 建立关联
                        item.storages.add(storage)
                        # 更新物品位置信息，确保格式为房间-家具-储物格
                        item.location = storage.name
                        item.save()
                        # 清空会话数据
                        request.session.pop('association_data', None)
                        return JsonResponse({
                            'success': True, 
                            'message': f'成功将物品「{item.name}」关联到储物格「{storage.name}」',
                            'complete': True
                        })
                
                request.session['association_data'] = session_data
                return JsonResponse({
                    'success': True, 
                    'message': f'储物格「{storage.name}」已识别，请扫描物品标签',
                    'complete': False
                })
        
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})
    
    # GET请求，显示关联页面
    return render(request, 'items/associate_item_storage.html', {})

@login_required
def clear_association(request):
    """
    清除关联会话数据
    """
    request.session.pop('association_data', None)
    return JsonResponse({'success': True, 'message': '已清除关联状态'})

@login_required
def print_selector(request):
    """
    打印选择器中间页面视图
    提供打印物品标签和打印储物格标签两个选项
    """
    return render(request, 'items/print_selector.html')

@login_required
def deposit_storage(request):
    """
    储物格录入视图
    提供房间、家具和储物格信息的录入功能
    """
    if request.method == 'POST':
        # 获取表单数据
        room = request.POST.get('room', '')
        furniture = request.POST.get('furniture', '')
        unit = request.POST.get('unit', '')
        name = request.POST.get('name', '')  # 组合后的名称
        storage_code = request.POST.get('item_code', '')  # 从tag_view传来的储物格编号
        
        try:
            # 创建储物格记录
            storage = Storage.objects.create(
                storage_code=storage_code,
                name=name,
                room=room,
                furniture=furniture,
                unit=unit,
                user=request.user
            )
            return redirect('items:success')
        except Exception as e:
            # 如果出错，重新渲染表单并显示错误
            context = {
                'room': room,
                'furniture': furniture,
                'unit': unit,
                'error': str(e)
            }
            return render(request, 'items/deposit_storage.html', context)
    
    return render(request, 'items/deposit_storage.html')

@login_required
def find_items(request):
    """
    查找物品页面视图
    包含搜索框、最近的物品、分类物品和储物格四个模块
    """
    # 获取搜索关键词
    search_query = request.GET.get('q', '')
    
    # 搜索物品
    items = Item.objects.filter(user=request.user)
    if search_query:
        items = items.filter(
            models.Q(name__icontains=search_query) |
            models.Q(item_code__icontains=search_query) |
            models.Q(description__icontains=search_query) |
            models.Q(location__icontains=search_query) |
            models.Q(category__icontains=search_query)
        )
    
    # 获取最近的物品（最近5个）
    recent_items = Item.objects.filter(user=request.user).order_by('-storage_time')[:5]
    
    # 获取分类物品
    # 先获取所有物品种类
    categories = Item.CATEGORY_CHOICES
    # 为每个分类获取对应的物品
    category_items = {}
    for category, display_name in categories:
        category_items[display_name] = Item.objects.filter(user=request.user, category=category)[:3]
    
    # 获取储物格，按房间、家具、储物格排序
    storages = Storage.objects.filter(user=request.user).order_by('room', 'furniture', 'unit')
    
    # 获取所有房间，用于筛选
    rooms = Storage.objects.filter(user=request.user).values_list('room', flat=True).distinct()
    
    # 获取所有分类选项
    categories = Item.CATEGORY_CHOICES
    
    context = {
        'search_query': search_query,
        'items': items,
        'recent_items': recent_items,
        'category_items': category_items,
        'storages': storages,
        'rooms': rooms,
        'categories': json.dumps(categories),
    }
    
    return render(request, 'items/find_items.html', context)

@login_required
def save_description(request, item_id):
    """
    保存物品描述的API端点
    """
    if request.method == 'POST':
        try:
            # 获取物品
            item = Item.objects.get(id=item_id, user=request.user)
            
            # 解析请求数据
            data = json.loads(request.body)
            description = data.get('description', '')
            
            # 更新描述
            item.description = description
            item.save()
            
            return JsonResponse({'success': True, 'message': '描述保存成功'})
        except Item.DoesNotExist:
            return JsonResponse({'success': False, 'message': '物品不存在'}, status=404)
        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'message': '无效的请求数据'}, status=400)
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)}, status=500)
    
    return JsonResponse({'success': False, 'message': '只支持POST请求'}, status=405)

@login_required
def delete_item(request, item_id):
    """
    删除物品的API端点
    """
    if request.method == 'POST':
        try:
            # 获取物品
            item = Item.objects.get(id=item_id, user=request.user)
            
            # 删除物品
            item.delete()
            
            return JsonResponse({'success': True, 'message': '物品删除成功'})
        except Item.DoesNotExist:
            return JsonResponse({'success': False, 'message': '物品不存在'}, status=404)
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)}, status=500)
    
    return JsonResponse({'success': False, 'message': '只支持POST请求'}, status=405)

@login_required
def update_item_category(request, item_id):
    """
    更新物品分类的API端点
    """
    if request.method == 'POST':
        try:
            # 获取物品
            item = Item.objects.get(id=item_id, user=request.user)
            
            # 获取新分类
            data = json.loads(request.body)
            new_category = data.get('category')
            
            # 验证分类是否有效
            valid_categories = [choice[0] for choice in Item.CATEGORY_CHOICES]
            if new_category not in valid_categories:
                return JsonResponse({'success': False, 'message': '无效的分类'}, status=400)
            
            # 更新分类
            item.category = new_category
            item.save()
            
            # 获取分类的显示名称
            category_display = dict(Item.CATEGORY_CHOICES).get(new_category, new_category)
            
            return JsonResponse({'success': True, 'message': '分类更新成功', 'category': category_display})
        except Item.DoesNotExist:
            return JsonResponse({'success': False, 'message': '物品不存在'}, status=404)
        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'message': '无效的请求数据'}, status=400)
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)}, status=500)
    
    return JsonResponse({'success': False, 'message': '只支持POST请求'}, status=405)

@login_required
def update_item_location(request, item_id):
    """
    更新物品位置的API端点
    """
    if request.method == 'POST':
        try:
            # 获取物品
            item = Item.objects.get(id=item_id, user=request.user)
            
            # 获取新位置
            data = json.loads(request.body)
            new_location = data.get('location')
            
            if not new_location:
                return JsonResponse({'success': False, 'message': '位置不能为空'}, status=400)
            
            # 更新位置
            item.location = new_location
            item.save()
            
            return JsonResponse({'success': True, 'message': '位置更新成功', 'location': new_location})
        except Item.DoesNotExist:
            return JsonResponse({'success': False, 'message': '物品不存在'}, status=404)
        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'message': '无效的请求数据'}, status=400)
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)}, status=500)
    
    return JsonResponse({'success': False, 'message': '只支持POST请求'}, status=405)
