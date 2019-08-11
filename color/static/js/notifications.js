$(function(){
    //定位弹出框
    const tag = $('#notifications')
    const emptyMessage = '没有未读通知'
    function checkRecentNotification(){
        $.ajax({
            url:'/notification/recent_notifications/',
            cache:false,
            success:function(data){
                if(!data.includes(emptyMessage)){
                    $('.btn-sm').addClass('btn-danger')
                }
            }
        })
    };
    checkRecentNotification()//打开首页自动执行此函数

    //当首页动态发生点赞或者评论时
    function dynamic_update(id){
        const news = $("[news-id=" +id+"]")
        $.ajax({
            url:'/news/interaction/',
            type:'POST',
            cache:false,
            data:{"id":id},
            success:function (data) {
                $('.like-count').text(data.likers)
                $('.comment-count').text(data.comment)
            }
        })
    }

    //点击导航处的弹出框
    tag.click(function(){
        //如果已经点开
        if($('.popover').is(':visible')){
            tag.popover('hide');
            checkRecentNotification()
        }else{
            tag.popover('dispose');//删除原本的提示框
            $.ajax({
                url:'/notification/recent_notifications/',
                cache: false,
                success:function(data){
                    tag.popover(
                        {
                            html:true,
                            trigger:"foucs",
                            container: 'body',
                            placement: 'bottom',
                            content: data,
                        }
                    );
                    tag.popover('show');
                    tag.removeClass('btn-danger')
                }
            })
        }

    });
    //websocket 监听
    var ws_schme = window.location.protocol === 'https'? 'wss':'ws';
    var ws_path = ws_schme+'://'+window.location.host+"/ws/" + 'notification/'
    var websocket = new ReconnectingWebSocket(ws_path);
    websocket.onmessage = function(event){
        var data = JSON.parse(event.data);
        switch (data.key) {
            case "notification": //如果是私信收到了回复
                if(!currentUser !== data.trigger){
                    $('#notifications').addClass('btn-danger')
                };
                break;
            case "news_update": //首页动态发生评论、点赞
                if(currentUser !== data.trigger){
                    $('#notifications').addClass('btn-danger')
                    dynamic_update(data.id)
                };
                break;
            case "add_news":
                if (currentUser !== data.trigger) {
                    $('.stream-update').show()
                };
                break;
            default:
                console.log("error", data);
                break

        }
    }

})
