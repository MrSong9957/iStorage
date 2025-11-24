/**
 * 存物品功能模块 - 独立页面版本
 * 提供物品录入和标签生成功能
 */

class DepositModule {
    constructor() {
        // 初始化页面元素
        this.initElements();
        // 绑定事件监听器
        this.bindEvents();
    }

    initElements() {
        // 图片上传相关元素
        this.imageUploadArea = document.getElementById('image_upload_area');
        this.imageInput = document.getElementById('id_image');
        this.imagePreview = document.getElementById('image_preview');
        this.previewImg = document.getElementById('preview_img');
        this.uploadHint = document.getElementById('upload_hint');
        this.removeImageBtn = document.getElementById('remove_image');
        
        // 标签生成相关元素
        this.generateTagBtn = document.getElementById('generateTagBtn');
        this.tagPreviewArea = document.getElementById('tagPreviewArea');
        this.retryGenerateBtn = document.getElementById('retryGenerateBtn');
        this.confirmName = document.getElementById('confirmName');
        this.confirmDescription = document.getElementById('confirmDescription');
        this.confirmImage = document.getElementById('confirmImage');
        this.previewItemName = document.getElementById('previewItemName');
        this.previewItemCode = document.getElementById('previewItemCode');
        this.qrcodeContainer = document.getElementById('qrcodeContainer');
        
        // 表单相关元素
        this.idName = document.getElementById('id_name');
        this.idDescription = document.getElementById('id_description');
        this.depositForm = document.getElementById('depositForm');
        this.confirmForm = document.getElementById('confirmForm');
    }

    bindEvents() {
        // 图片上传事件
        this.imageUploadArea.addEventListener('click', (event) => this.handleUploadAreaClick(event));
        this.imageInput.addEventListener('change', () => this.handleFileChange());
        this.removeImageBtn.addEventListener('click', () => this.removeImage());
        
        // 标签生成事件
        this.generateTagBtn.addEventListener('click', () => this.generateTag());
        this.retryGenerateBtn.addEventListener('click', () => this.retryGenerate());
        
        // 表单提交事件
        this.depositForm.addEventListener('submit', (event) => this.handleFormSubmit(event));
        this.confirmForm.addEventListener('submit', (event) => this.handleConfirmFormSubmit(event));
    }

    // 图片上传区域点击
    handleUploadAreaClick(event) {
        if (!event.target.closest('#remove_image')) {
            this.imageInput.click();
        }
    }

    // 文件选择变化
    handleFileChange() {
        if (this.imageInput.files && this.imageInput.files[0]) {
            this.showImagePreview(this.imageInput.files[0]);
        }
    }

    // 显示图片预览
    showImagePreview(file) {
        if (!file.type.match('image.*')) {
            return;
        }
        
        const reader = new FileReader();
        reader.onload = (e) => {
            this.previewImg.src = e.target.result;
            this.imagePreview.classList.remove('hidden');
            this.uploadHint.classList.add('hidden');
        }
        reader.readAsDataURL(file);
    }

    // 移除图片
    removeImage() {
        this.imageInput.value = '';
        this.imagePreview.classList.add('hidden');
        this.uploadHint.classList.remove('hidden');
    }

    // 验证表单
    validateForm() {
        const name = this.idName.value.trim();
        const hasImage = this.imageInput.files.length > 0;
        
        if (!name && !hasImage) {
            alert('请输入物品名称或上传物品图片（至少选择一项）');
            return false;
        }
        return true;
    }

    // 生成标签
    generateTag() {
        if (!this.validateForm()) {
            return;
        }
        
        // 设置预览信息
        const name = this.idName.value.trim() || '未命名物品';
        const description = this.idDescription.value.trim();
        
        // 显示加载状态
        this.generateTagBtn.textContent = '生成中...';
        this.generateTagBtn.disabled = true;
        
        // 创建FormData并发送请求到后端
        const formData = new FormData();
        formData.append('name', name);
        
        // 调用后端API获取标签数据
        fetch('/items/generate_tag/', {
            method: 'POST',
            headers: {
                'X-CSRFToken': this.getCSRFToken()
            },
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                // 填充确认表单数据
                this.confirmName.value = name;
                this.confirmDescription.value = description;
                
                // 预览区域显示
                this.previewItemName.textContent = data.name;
                this.previewItemCode.textContent = data.item_code;
                
                // 使用后端返回的二维码
                this.generateQRCode(data.qr_code);
                
                // 显示标签预览区域
                this.tagPreviewArea.classList.remove('hidden');
                this.tagPreviewArea.scrollIntoView({ behavior: 'smooth', block: 'start' });
            } else {
                alert('生成标签失败: ' + (data.error || '未知错误'));
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('网络错误，请重试');
        })
        .finally(() => {
            // 恢复按钮状态
            this.generateTagBtn.textContent = '识别并生成标签';
            this.generateTagBtn.disabled = false;
        });
    }
    
    // 获取CSRF Token
    getCSRFToken() {
        const cookieValue = document.cookie
            .split('; ')
            .find(row => row.startsWith('csrftoken='))
            ?.split('=')[1];
        return cookieValue || '';
    }
    
    // 生成二维码（使用后端返回的base64数据）
    generateQRCode(qrBase64) {
        // 清空容器
        this.qrcodeContainer.innerHTML = '';
        
        // 创建二维码图像
        const qrCodeImage = document.createElement('img');
        qrCodeImage.src = `data:image/png;base64,${qrBase64}`;
        qrCodeImage.alt = '物品二维码';
        qrCodeImage.className = 'w-48 h-48';
        
        this.qrcodeContainer.appendChild(qrCodeImage);
    }
    
    // 处理表单提交
    handleFormSubmit(event) {
        // 阻止默认提交，因为我们使用生成标签的流程
        event.preventDefault();
    }
    
    // 处理确认表单提交
    handleConfirmFormSubmit(event) {
        // 这里可以添加最后的验证或数据处理
        // 表单将正常提交到服务器
    }

    // 生成物品编号
    generateItemCode() {
        const timestamp = Date.now();
        const random = Math.floor(Math.random() * 1000).toString().padStart(3, '0');
        return `ITEM-${timestamp}-${random}`;
    }

    // 重新生成
    retryGenerate() {
        this.tagPreviewArea.classList.add('hidden');
    }
}

// 当DOM加载完成后初始化模块
document.addEventListener('DOMContentLoaded', () => {
    // 检查是否存在必要的DOM元素（针对独立页面）
    if (document.getElementById('image_upload_area')) {
        const depositModule = new DepositModule();
        // 暴露到全局以便外部调用
        window.depositModule = depositModule;
    }
});