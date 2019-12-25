function createAccount() {
  const password = $('#password').val();
  const rePassword = $('#re-password').val();

  if (password && rePassword) {
    alert('회원가입을 성공했습니다.');
    window.location = './signin.html';
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
