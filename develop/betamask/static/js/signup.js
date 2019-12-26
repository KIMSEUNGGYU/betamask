function createAccount() {
  const password = $('#password').val();
  const rePassword = $('#re-password').val();

  if (password && rePassword) {
    if (password === rePassword) fetchCreateAccount(password);
    else alert('비밀번호가 일치하지 않습니다.');
  } else {
    alert('비밀번호를 모두 입력해주세요.');
  }
}

$('#ex_chk').change(function() {
  if ($('#ex_chk').is(':checked') == true) {
    $('#createButton').addClass('activate');
    $('#createButton').click(createAccount); // 이벤트 등록
  } else {
    $('#createButton').removeClass('activate');
    $('#createButton').off('click', createAccount); // 이벤트 해제
  }
});

function fetchCreateAccount(password) {
  $.ajax({
    url: '/api/v2/user/create',
    contentType: 'application/json',
    method: 'POST',
    data: JSON.stringify({
      password: password,
    }),
  })
    .done(function(res) {
      // alert('회원가입에 성공했습니다.');
      const address = res['address'];
      window.location = '/mnemonic/' + address;
    })
    .fail(function(res) {
      alert('이미 존재하는 계정입니다.');
    });
}
