// 폼 클릭시 확인/취소 버튼 나오도록
$('.form-control').on('focus', function() {
    $('#comment-footer').css('display','inline')
})
$('.form-cancel').on('click', function() {
    $('#comment-footer').css('display','none')
})

// 댓글 다는 부분 ajax 처리
$('.add_comment').on('click', function(e) {
    if ($('.form-control').val() == ''){
        return
    }
    $.ajax({
        url: $(location).attr('href'),
        type: 'POST',
        data: {
            'contents': $('.form-control').val(),
            'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val(),
            'formtype': 'comment-add',
        },
        success: function(data) {
            if (data){
                $('.form-control').val('')
                $('.comment-block').html(data)
                $('#results').html('<div class="alert alert-success">성공적으로 댓글을 달았습니다.<a href="javascript:void(0)" class="close" data-dismiss="alert" aria-label="close">&times;</a></div>')
            }
            else{
                console.error('데이터가 안넘어옴')
            }
        },
        error: function(xhr,errmsg,err) {
            $('#results').html('<div class="alert alert-danger">에러가 발생했습니다 : '+errmsg+'('+xhr.status+')'+'<a href="javascript:void(0)" class="close" data-dismiss="alert" aria-label="close">&times;</a></div>')
        },
        complete: function() {
            $.getScript(edit(), function() {})
        }
    })
})
