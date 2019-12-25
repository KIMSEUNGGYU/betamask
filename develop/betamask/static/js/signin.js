function login() {
  console.log('로그인 이벤트 발생');
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
