(function ($) {
    var $content_md = $('#div_id_content_md');
    var $content_ck = $('#div_id_content_ck');
    var $is_md = $('input[name=is_md]');
    var switch_editor = function (is_md) {
        if(is_md){
            $content_md.show();
            $content_ck.hide();
        }else{
            $content_ck.show();
            $content_md.hide();
        }
    };
    // is_md监测点击事件，点击后执行switch_editor函数切换编辑器
    $is_md.on('click', function () {
        switch_editor($(this).is(':checked'));
    });
    // 首次加载完页面后执行switch_editor函数确认展示的编辑器
    switch_editor($is_md.is(':checked'));
    // xadmin已经加载了jQuery，可以直接使用，这里的jQuery中的Q要大写
})(jQuery);
