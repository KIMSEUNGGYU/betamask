const passwordElement = $('#password');
const rePasswordElement = $('#re-password');
const textareaElement = $('#mnemonic-input');

function changeInput() {
  if (passwordElement.val() && rePasswordElement.val() && textareaElement.val())
    return true;
}

function changeEvent() {
  if (changeInput()) {
    $('#update-button').addClass('activate');
    $('#update-button').off('click', fetchUpdate); // 이벤트 해제
    $('#update-button').click(fetchUpdate); // 이벤트 등록
    return;
  }

  console.log('값없음');
  $('#update-button').removeClass('activate');
  $('#update-button').off('click', fetchUpdate); // 이벤트 해제
}

function fetchUpdate() {
  console.log('button click');
  const password = passwordElement.val();
  const rePassword = rePasswordElement.val();
  const text = textareaElement.val();

  if (password == rePassword) update(password, text);
}

function update(password, text) {
  $.ajax({
    url: '/api/v2/update',
    contentType: 'application/json',
    method: 'POST',
    data: JSON.stringify({
      password: password,
      mnemonic: text,
    }),
    statusCode: {
      202: function() {
        // 로그인 실패
        alert('변경 실패, 올바른 니모닉 코드가 없거나 아닙니다.');
      },
      200: function(result) {
        // 로그인 성공
        alert('정상적으로 변경했습니다.');
        window.location = '/signin';
      },
    },
  }).fail(function(res) {
    console.log('res', res);
    alert('서버 오류');
  });
}
passwordElement.on('change keyup paste', changeEvent);
rePasswordElement.on('change keyup paste', changeEvent);
textareaElement.on('change keyup paste', changeEvent);
