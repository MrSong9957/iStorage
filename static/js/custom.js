// 导航项管理功能

// 获取CSRF令牌
function getCookie(name) {
    const match = document.cookie.match(`(^|;) ?${name}=([^;]*)(;|$)`);
    return match ? decodeURIComponent(match[2]) : null;
}

// 显示导航项模态框
function showNavModal() {
    const modal = document.getElementById('nav-modal');
    const title = document.getElementById('nav-modal-title');
    const actionInput = document.getElementById('nav-action');
    const navIdInput = document.getElementById('nav-id');
    const parentIdInput = document.getElementById('parent-id');
    const nameInput = document.getElementById('nav-name');
    const urlInput = document.getElementById('nav-url');
    const iconInput = document.getElementById('nav-icon');
    
    // 重置表单
    title.textContent = '添加子标签';
    actionInput.value = 'add';
    navIdInput.value = '';
    parentIdInput.value = '';
    nameInput.value = '';
    urlInput.value = '';
    iconInput.value = '';
    
    // 显示模态框
    modal.style.display = 'flex';
    document.body.style.overflow = 'hidden';
}

// 编辑导航项
function editNavItem(id, name) {
    const modal = document.getElementById('nav-modal');
    const title = document.getElementById('nav-modal-title');
    const actionInput = document.getElementById('nav-action');
    const navIdInput = document.getElementById('nav-id');
    const nameInput = document.getElementById('nav-name');
    const urlInput = document.getElementById('nav-url');
    const iconInput = document.getElementById('nav-icon');
    
    // 填充表单数据
    title.textContent = '编辑子标签';
    actionInput.value = 'edit';
    navIdInput.value = id;
    nameInput.value = name;
    
    // 显示模态框
    modal.style.display = 'flex';
    document.body.style.overflow = 'hidden';
}

// 隐藏导航项模态框
function hideNavModal() {
    const modal = document.getElementById('nav-modal');
    modal.style.display = 'none';
    document.body.style.overflow = 'auto';
}

// 提交导航项表单
function submitNavForm() {
    const form = document.getElementById('nav-form');
    const formData = new FormData(form);
    
    // 获取表单数据
    const navId = document.getElementById('nav-id').value;
    const action = document.getElementById('nav-action').value;
    
    // 发送请求
    fetch('{% url 'items:manage_navigation' %}', {
        method: 'POST',
        credentials: 'same-origin',
        headers: {
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            // 刷新页面
            window.location.reload();
        } else {
            alert('操作失败: ' + (data.error || '未知错误'));
        }
    })
    .catch(error => {
        console.error('操作失败:', error);
        alert('操作失败: 网络错误');
    });
}

// 删除导航项
function deleteNavItem(id) {
    if (confirm('确定要删除这个导航项吗？')) {
        // 创建表单数据
        const formData = new FormData();
        formData.append('action', 'delete');
        formData.append('nav_id', id);
        
        // 发送请求
        fetch('{% url 'items:manage_navigation' %}', {
            method: 'POST',
            credentials: 'same-origin',
            headers: {
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                // 刷新页面
                window.location.reload();
            } else {
                alert('删除失败: ' + (data.error || '未知错误'));
            }
        })
        .catch(error => {
            console.error('删除失败:', error);
            alert('删除失败: 网络错误');
        });
    }
}

// 添加删除图标
function addDeleteIcons() {
    const tagItems = document.querySelectorAll('.tag-item');
    tagItems.forEach(item => {
        // 只给非添加项添加删除图标
        if (!item.classList.contains('add-tag-item')) {
            const actionsDiv = item.querySelector('.tag-actions');
            if (actionsDiv) {
                // 检查是否已添加删除图标
                if (!actionsDiv.querySelector('.delete-icon')) {
                    const deleteIcon = document.createElement('button');
                    deleteIcon.className = 'action-icon delete-icon';
                    deleteIcon.title = '删除';
                    deleteIcon.innerHTML = '🗑️';
                    deleteIcon.onclick = function() {
                        const navId = item.dataset.navId;
                        deleteNavItem(navId);
                    };
                    actionsDiv.appendChild(deleteIcon);
                }
            }
        }
    });
}

// 页面加载完成后执行
document.addEventListener('DOMContentLoaded', function() {
    // 添加删除图标
    addDeleteIcons();
    
    // 模态框外部点击关闭
    const modal = document.getElementById('nav-modal');
    if (modal) {
        modal.addEventListener('click', function(e) {
            if (e.target === modal) {
                hideNavModal();
            }
        });
    }
});