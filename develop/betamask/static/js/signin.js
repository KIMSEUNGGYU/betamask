function login() {
  // console.log('로그인 이벤트 발생');
  // console.log('dafds', $('#password-input').val());
  $.ajax({
    url: '/signin',
    contentType: 'application/json',
    method: 'POST',
    data: JSON.stringify({
      password: $('#password-input').val(),
    }),
    statusCode: {
      202: function() {
        // 로그인 실패
        alert('로그인 실패, 비밀번호를 확인해주세요');
      },
      200: function(result) {
        // 로그이 성공

        const { data } = result;
        console.log('data', data);
        window.location = '/main/' + data;
      },
    },
  }).fail(function(res) {
    console.log('res', res);
    alert('서버 오류');
    // alert('이미 존재하는 계정입니다.');
  });
}

const passwordElement = $('#password-input');
passwordElement.on('change keyup paste', function() {
  // https://karismamun.tistory.com/66
  const passwordValue = passwordElement.val();

  if (passwordValue.length) {
    console.log(passwordValue);
    $('#loginButton').addClass('activate');
    $('#loginButton').off('click', login); // 이벤트 해제
    $('#loginButton').click(login); // 이벤트 등록
    return;
  }

  console.log('값없음');
  $('#loginButton').removeClass('activate');
  $('#loginButton').off('click', login); // 이벤트 해제
});

$('#get-mnemonic-text').click(function() {
  window.location = '/update';
});
