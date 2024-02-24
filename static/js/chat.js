// 显示加载动画
function showLoading() {
    $('.loading').show();
}
  
  // 隐藏加载动画
function hideLoading() {
    $('.loading').hide();
}
$(document).ready(function() {
    $('#chat-form').submit(function(e) {
        e.preventDefault();
        var userMessage = $('#chat-input').val();
        if (userMessage.trim() === '') return;
        $('#chat-input').val('');
        // 禁用发送按钮
        $('form button[type="submit"]').prop('disabled', true);
        // 显示用户消息
        $('#chat-box').append(`<div class="message user-message">你: ${userMessage}</div>`);
        // 在发送请求之前显示加载动画
        showLoading();

        $.ajax({
            url: '/chat',
            type: 'POST',
            data: { message: userMessage },
            success: function(data) {
                $('form button[type="submit"]').prop('disabled', false);
                // 隐藏加载动画
                hideLoading();
                $('#chat-box').append(`<div class="message chatgpt-message">ChatGPT: ${data.reply}</div>`);
                $('#chat-box').scrollTop($('#chat-box')[0].scrollHeight);
                // $('#chat-input').val('');
                $('#remaining').text(data.remaining);
            },
            error: function(error) {
                $('form button[type="submit"]').prop('disabled', false);
                // 隐藏加载动画
                hideLoading();
                console.error('Error:', error);
            }
        });
    })
});
