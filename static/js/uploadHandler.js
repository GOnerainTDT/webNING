document.addEventListener('DOMContentLoaded', function() {
    var uploadBtn = document.getElementById('upload-btn');
    var fileInput = document.getElementById('fileInput'); // 确保ID与HTML中的ID匹配

    if(uploadBtn && fileInput) {
        uploadBtn.addEventListener('click', function() {
            fileInput.click();
        });
    }

    // 添加事件监听器替代内联onchange事件处理器
    fileInput.addEventListener('change', previewAndUploadImage);
});
