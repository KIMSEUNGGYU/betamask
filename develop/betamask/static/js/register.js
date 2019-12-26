function regist() {
  $.ajax({
    url: '/api/v1/users/register',
    contentType: 'application/json',
    method: 'POST',
    data: JSON.stringify({
      userid: $('#userid').val(),
      username: $('#username').val(),
      password: $('#password').val(),
      're-password': $('#re-password').val(),
    }),
  })
    .done(function(res) {
      console.log(res);
      // success: function(res) {
      // console.log('res', res);
      // alert('회원가입에 성공했습니다.');
      // window.location = '/';
      // },
      // fail: function(data) {
      // alert('fail');
      // },
    })
    .fail(function(textStatus) {
      alert('회원가입을 하지 못합니다.', textStatus);
    });
}
