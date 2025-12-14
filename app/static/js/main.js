// 全局变量
let selectedStyle = null;
let selectedImage = null;

// DOM 元素
const uploadArea = document.getElementById('upload-area');
const uploadInput = document.getElementById('image-upload');
const previewContainer = document.getElementById('preview-container');
const imagePreview = document.getElementById('image-preview');
const removePreview = document.getElementById('remove-preview');
const styleGrid = document.getElementById('style-grid');
const recommendBtn = document.getElementById('recommend-btn');
const results = document.getElementById('results');
const loading = document.getElementById('loading');
const initial = document.getElementById('initial');
const styleInfo = document.getElementById('style-info');
const sceneAnalysis = document.getElementById('scene-analysis');
const poseAdviceList = document.getElementById('pose-advice-list');
const adviceList = document.getElementById('advice-list');
const aiImageGrid = document.getElementById('ai-image-grid');
const imageGrid = document.getElementById('image-grid');

// 初始化
function init() {
    // 加载风格列表
    loadStyles();
    
    // 设置事件监听器
    setupEventListeners();
}

// 加载风格列表
async function loadStyles() {
    try {
        const response = await fetch('/api/styles');
        const data = await response.json();
        
        // 清空现有风格选项
        styleGrid.innerHTML = '';
        
        // 添加风格选项
        data.styles.forEach(style => {
            const styleOption = document.createElement('div');
            styleOption.className = 'style-option';
            styleOption.textContent = style;
            styleOption.addEventListener('click', () => selectStyle(styleOption, style));
            styleGrid.appendChild(styleOption);
        });
    } catch (error) {
        console.error('Failed to load styles:', error);
        alert('加载风格列表失败，请稍后重试');
    }
}

// 设置事件监听器
function setupEventListeners() {
    // 上传区域点击事件
    uploadArea.addEventListener('click', () => uploadInput.click());
    
    // 拖拽事件
    uploadArea.addEventListener('dragover', (e) => {
        e.preventDefault();
        uploadArea.classList.add('dragover');
    });
    
    uploadArea.addEventListener('dragleave', () => {
        uploadArea.classList.remove('dragover');
    });
    
    uploadArea.addEventListener('drop', (e) => {
        e.preventDefault();
        uploadArea.classList.remove('dragover');
        if (e.dataTransfer.files.length > 0) {
            handleFileUpload(e.dataTransfer.files[0]);
        }
    });
    
    // 文件选择事件
    uploadInput.addEventListener('change', (e) => {
        if (e.target.files.length > 0) {
            handleFileUpload(e.target.files[0]);
        }
    });
    
    // 移除预览事件
    removePreview.addEventListener('click', removeImagePreview);
    
    // 获取推荐按钮事件
    recommendBtn.addEventListener('click', getRecommendations);
}

// 处理文件上传
function handleFileUpload(file) {
    // 验证文件类型
    if (!file.type.startsWith('image/')) {
        alert('请选择图片文件');
        return;
    }
    
    // 验证文件大小（16MB）
    if (file.size > 16 * 1024 * 1024) {
        alert('图片大小不能超过16MB');
        return;
    }
    
    // 保存选中的图片
    selectedImage = file;
    
    // 显示预览
    const reader = new FileReader();
    reader.onload = (e) => {
        imagePreview.src = e.target.result;
        previewContainer.style.display = 'block';
    };
    reader.readAsDataURL(file);
    
    // 更新推荐按钮状态
    updateRecommendBtn();
}

// 移除图片预览
function removeImagePreview() {
    selectedImage = null;
    imagePreview.src = '';
    previewContainer.style.display = 'none';
    uploadInput.value = '';
    
    // 更新推荐按钮状态
    updateRecommendBtn();
}

// 选择风格
function selectStyle(element, style) {
    // 移除之前的选中状态
    document.querySelectorAll('.style-option').forEach(option => {
        option.classList.remove('selected');
    });
    
    // 添加当前选中状态
    element.classList.add('selected');
    selectedStyle = style;
    
    // 更新推荐按钮状态
    updateRecommendBtn();
}

// 更新推荐按钮状态
function updateRecommendBtn() {
    recommendBtn.disabled = !selectedImage || !selectedStyle;
}

// 获取推荐
async function getRecommendations() {
    if (!selectedImage || !selectedStyle) {
        return;
    }
    
    // 显示加载状态
    showLoading();
    
    try {
        // 创建FormData
        const formData = new FormData();
        formData.append('image', selectedImage);
        formData.append('style', selectedStyle);
        
        // 发送请求
        const response = await fetch('/api/recommend', {
            method: 'POST',
            body: formData
        });
        
        if (!response.ok) {
            throw new Error('请求失败');
        }
        
        const data = await response.json();
        
        // 显示结果
        displayResults(data);
    } catch (error) {
        console.error('获取推荐失败:', error);
        alert('获取推荐失败，请稍后重试');
        hideLoading();
    }
}

// 显示加载状态
function showLoading() {
    initial.style.display = 'none';
    results.style.display = 'none';
    loading.style.display = 'block';
}

// 隐藏加载状态
function hideLoading() {
    loading.style.display = 'none';
}

// 显示结果
function displayResults(data) {
    hideLoading();
    
    // 更新风格信息
    updateStyleInfo(data);
    
    // 更新场景分析
    updateSceneAnalysis(data);
    
    // 更新姿势建议
    updatePoseAdvice(data);
    
    // 更新拍摄建议
    updateAdvice(data);
    
    // 更新AI生成参考图片
    updateAIImageGrid(data);
    
    // 显示结果
    results.style.display = 'block';
}

// 更新风格信息
function updateStyleInfo(data) {
    styleInfo.innerHTML = `
        <h5>${data.style}</h5>
        <p>场景类型：${data.scene_features.scene_type}</p>
        <p>光线条件：${data.scene_features.light_type}</p>
        <p>主色调：${data.scene_features.colors.dominant_color}</p>
    `;
}

// 更新场景分析
function updateSceneAnalysis(data) {
    const sceneFeatures = data.scene_features;
    sceneAnalysis.innerHTML = `
        <div class="scene-description">
            <h5>场景描述</h5>
            <p>${sceneFeatures.scene_description}</p>
        </div>
        <div class="scene-elements mt-3">
            <h5>场景元素</h5>
            <div class="scene-elements-tags">
                ${sceneFeatures.scene_elements.map(element => `<span class="badge bg-primary m-1">${element}</span>`).join('')}
            </div>
        </div>
        <div class="detailed-analysis mt-3">
            <h5>详细分析</h5>
            <ul class="list-unstyled">
                <li><strong>场景总结：</strong>${sceneFeatures.detailed_analysis.scene_summary}</li>
                <li><strong>光线总结：</strong>${sceneFeatures.detailed_analysis.lighting_summary}</li>
                <li><strong>色彩总结：</strong>${sceneFeatures.detailed_analysis.color_summary}</li>
                <li><strong>构图总结：</strong>${sceneFeatures.detailed_analysis.composition_summary}</li>
            </ul>
        </div>
    `;
}

// 更新姿势建议
function updatePoseAdvice(data) {
    poseAdviceList.innerHTML = '';
    
    const advice = data.advice;
    
    // 整体姿势建议
    addAdviceItem('bi bi-person', advice.pose, poseAdviceList);
    
    // 手部动作建议
    if (advice.hand_movements) {
        addAdviceItem('bi bi-hand-index-thumb', advice.hand_movements, poseAdviceList);
    }
    
    // 脚部动作建议
    if (advice.foot_movements) {
        addAdviceItem('bi bi-shoe-prints', advice.foot_movements, poseAdviceList);
    }
    
    // 表情建议
    if (advice.expression) {
        addAdviceItem('bi bi-emoji-smile', advice.expression, poseAdviceList);
    }
}

// 更新AI生成参考图片
function updateAIImageGrid(data) {
    aiImageGrid.innerHTML = '';
    
    // 获取模态框元素
    const imagePreviewModal = new bootstrap.Modal(document.getElementById('imagePreviewModal'));
    const modalImage = document.getElementById('modalImage');
    
    // 检查是否有AI生成的图片
    if (data.ai_reference_images && data.ai_reference_images.length > 0) {
        data.ai_reference_images.forEach(image => {
            const imageContainer = document.createElement('div');
            imageContainer.className = 'reference-image';
            imageContainer.innerHTML = `
                <img src="${image.url}" alt="AI生成参考图片" loading="lazy" class="cursor-pointer">
                <div class="image-source">AI生成</div>
            `;
            
            // 添加点击事件，打开模态框查看大图
            const imgElement = imageContainer.querySelector('img');
            imgElement.addEventListener('click', () => {
                modalImage.src = image.url;
                imagePreviewModal.show();
            });
            
            aiImageGrid.appendChild(imageContainer);
        });
    } else {
        // 如果没有AI生成的图片，显示提示信息
        aiImageGrid.innerHTML = `
            <div class="no-ai-images text-center py-4">
                <i class="bi bi-robot" style="font-size: 3rem; color: #ccc;"></i>
                <p class="mt-2">暂无AI生成的参考图片</p>
            </div>
        `;
    }
}

// 更新拍摄建议
function updateAdvice(data) {
    adviceList.innerHTML = '';
    
    const advice = data.advice;
    
    // 角度建议
    addAdviceItem('bi bi-camera-reels', advice.angle);
    
    // 位置建议
    addAdviceItem('bi bi-map-pin', advice.position);
    
    // 光线建议
    addAdviceItem('bi bi-sun', advice.lighting);
    
    // 姿势建议
    addAdviceItem('bi bi-person', advice.pose);
    
    // 构图建议
    addAdviceItem('bi bi-grid', advice.composition);
    
    // 通用建议
    if (advice.general_tips && advice.general_tips.length > 0) {
        advice.general_tips.forEach(tip => {
            addAdviceItem('bi bi-lightbulb', tip);
        });
    }
}

// 添加建议项
function addAdviceItem(icon, text, container = adviceList) {
    const adviceItem = document.createElement('div');
    adviceItem.className = 'advice-item';
    adviceItem.innerHTML = `
        <i class="${icon}"></i>
        <p>${text}</p>
    `;
    container.appendChild(adviceItem);
}



// 页面加载完成后初始化
document.addEventListener('DOMContentLoaded', init);
