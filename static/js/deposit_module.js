/**
 * 存物品功能模块 - 独立组件
 * 提供物品录入和标签生成功能
 */

class DepositModule {
    constructor() {
        // 初始化模态窗口和相关元素
        this.initElements();
        // 绑定事件监听器
        this.bindEvents();
    }

    initElements() {
        // 模态窗口元素
        this.modal = document.getElementById('depositModal');
        this.openModalBtn = document.getElementById('openDepositModal');
        this.closeModalBtn = document.getElementById('closeDepositModal');
        
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
        this.previewItemName = document.getElementById('previewItemName');
        this.previewItemCode = document.getElementById('previewItemCode');
        this.idName = document.getElementById('id_name');
    }

    bindEvents() {
        // 模态窗口事件
        this.openModalBtn.addEventListener('click', () => this.openModal());
        this.closeModalBtn.addEventListener('click', () => this.closeModal());
        this.modal.addEventListener('click', (event) => this.handleModalClick(event));
        document.addEventListener('keydown', (event) => this.handleKeyDown(event));
        
        // 图片上传事件
        this.imageUploadArea.addEventListener('click', (event) => this.handleUploadAreaClick(event));
        this.imageInput.addEventListener('change', () => this.handleFileChange());
        this.removeImageBtn.addEventListener('click', () => this.removeImage());
        
        // 标签生成事件
        this.generateTagBtn.addEventListener('click', () => this.generateTag());
        this.retryGenerateBtn.addEventListener('click', () => this.retryGenerate());
    }

    // 打开模态窗口
    openModal() {
        this.modal.classList.remove('hidden');
        document.body.style.overflow = 'hidden'; // 防止背景滚动
    }

    // 关闭模态窗口
    closeModal() {
        this.modal.classList.add('hidden');
        document.body.style.overflow = ''; // 恢复背景滚动
    }

    // 点击模态窗口外部关闭
    handleModalClick(event) {
        if (event.target === this.modal) {
            this.closeModal();
        }
    }

    // 按ESC键关闭
    handleKeyDown(event) {
        if (event.key === 'Escape' && !this.modal.classList.contains('hidden')) {
            this.closeModal();
        }
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
        this.confirmName.value = name;
        this.previewItemName.textContent = name;
        this.previewItemCode.textContent = this.generateItemCode();
        
        // 显示标签预览区域
        this.tagPreviewArea.classList.remove('hidden');
        this.tagPreviewArea.scrollIntoView({ behavior: 'smooth', block: 'start' });
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
    // 检查是否存在必要的DOM元素
    if (document.getElementById('depositModal')) {
        const depositModule = new DepositModule();
        // 暴露到全局以便外部调用
        window.depositModule = depositModule;
    }
});