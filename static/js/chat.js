$(document).ready(function() {
    $('#chat-form').submit(function(e) {
        e.preventDefault();
        var userMessage = $('#chat-input').val();
        if (userMessage.trim() === '') return;

        $.ajax({
            url: '/chat',
            type: 'POST',
            data: { message: userMessage },
            success: function(data) {
                $('#chat-box').append(`<div>你: ${userMessage}</div>`);
                $('#chat-box').append(`<div>ChatGPT: ${data.reply}</div>`);
                $('#chat-box').scrollTop($('#chat-box')[0].scrollHeight);
                $('#chat-input').val('');
                $('#remaining').text(data.remaining);
            },
            error: function(error) {
                console.error('Error:', error);
            }
        });
    })
});
