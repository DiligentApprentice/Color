$(function () {

    // 滚动条下拉到底
    function scrollConversationScreen() {
        $("input[name='message']").focus();
        $('.messages-list').scrollTop($('.messages-list')[0].scrollHeight);
    }


    // AJAX POST发送消息
    $("#send").submit(function () {
        console.log('为什么不走这里')
        $.ajax({
            url: '/chat/messages/send-message/',
            data: $("#send").serialize(),
            cache: false,
            type: "POST",
            success: function (data) {
                $(".send-message").before(data);  // 将接收到的消息插入到聊天框
                $("input[name='message']").val(''); // 消息发送框置为空
                scrollConversationScreen();  // 滚动条下拉到底
            }
        });
        return false;
    });

    // WebSocket连接
    var ws_scheme = window.location.protocol === "https:" ? "wss" : "ws";  // 使用wss(https)或者ws(http)
    var ws_path = ws_scheme + '://' + window.location.host +  "/ws/"+"message/"+ currentUser + "/";
    var websocket = new ReconnectingWebSocket(ws_path)
    websocket.onmessage = function(event){
        const data = JSON.parse(event.data)
        if (data.sender === activeUser){
            $('.send-message').before(data.message);
            scrollConversationScreen();  // 滚动条下拉到底
        }
    }
});
