// 댓글 수정 클릭시 textarea로 변경
$('.a_comment_edit').each(function(){
    var edit_mode = false
    $(this).on('click', function(e) {
        // 수정을 이전에 안누른 상태여야만 실행
        if (!edit_mode){
            edit_mode = !edit_mode
            var panel = $(e.target).closest('div.panel')
            panel.find('.comment-content').css('display', 'none')
            panel.find('.comment-post').append('<textarea id="changed-content" style="width:100%" cols="35" required="required" rows="2"></textarea>')
            panel.find('.comment-post-buttons').css('display', 'block')
            $('#changed-content').focus()
        }
    })
    // 취소 눌렀을때 수정 누른 상태 초기화
    $(this).closest('.panel-body').find('.edit-cancel').on('click', function(){
        edit_mode = !edit_mode
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
                    $('.comment-block').html(data)
                }
                else{
                    console.error('데이터가 안넘어옴')
                }
            },
            error: function(xhr,errmsg,err){
                console.error(err)
            },
            complete: function() {
                $.getScript(edit(), function(){})
            }
        })
    })
})
