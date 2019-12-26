console.log('tset 니모닉');

$('#nextButton').click(function() {
  console.log('ff');
  createConfirmBox();
  // window.location = './signin.html';
  // window.location = '/';
});

function createConfirmBox() {
  const retVal = confirm(
    '니모닉 코드를 완벽하게 복사 및 작성하셨나요? \n 실수를 되돌리수 없습니다.',
  );

  if (retVal === true) {
    window.location = '/signin';
  }
}
