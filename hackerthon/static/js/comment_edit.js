// 댓글 수정 클릭시 textarea로 변경
$('.a_comment_edit').each(function(){
    $(this).on('click', function(e) {
        var panel = $(e.target).closest('div.panel')
        panel.find('.comment-content').css('display', 'none')
        panel.find('.comment-post').append('<textarea id="changed-content" cols="35" required="required" rows="2"></textarea>')
        panel.find('.comment-post-buttons').css('display', 'block')
        $('#changed-content').focus()
    })
})

// 댓글 수정 클릭 후 취소 클릭시 되돌리기
$('.edit-cancel').each(function(){
    $(this).on('click', function(e) {
        var panel = $(e.target).closest('div.panel')
        panel.find('.comment-post-buttons').css('display', 'none')
        panel.find('.comment-content').css('display', 'inline')
        $('#changed-content').remove()
    })
})

// 댓글 수정 클릭 후 확인
$('.edit-submit').each(function(){
    $(this).on('click', function(e) {
        var panel = $(e.target).closest('div.panel')
        if (panel.find('#changed-content').val() == ''){
            return
        }
        $.ajax({
            url: $(location).attr('href'),
            type: 'POST',
            data: {
                'contents': panel.find('#changed-content').val(),
                'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val(),
                'formtype': 'comment-edit',
                'comment': panel.find('.comment-pk').val(),
            },
            success: function(data){
                if (data){
                    console.log('success~')
                    $('.comment-block').html(data)
                }
            },
            error: function(xhr,errmsg,err){
                console.error(err)
            },
            complete: function() {
                $.getScript(edit(), function(){
                    console.log('js loaded - js')
                })
            }
        })
    })
})
