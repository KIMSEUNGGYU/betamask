const modal = document.querySelector('.modal-wrapper');
const loading = document.querySelector('.loader-wrapper');

$('#modal-open-button').click(function() {
  modal.style.display = 'flex';
});

$('#close-button').click(function() {
  modal.style.display = 'none';
});

$('#send-button').click(function() {
  const toAddress = $('#input-address').val();
  const amount = parseFloat($('#input-amount').val());
  const fromAddress = $('.account')
    .text()
    .trim();

  if (toAddress && amount) {
    console.log('click', toAddress);
    console.log('click', amount);
    fetchSend(fromAddress, toAddress, amount);
    modal.style.display = 'none';
    loading.style.display = 'flex';

    return;
  }

  alert('올바르지 않는 경우 입니다.');
});

function fetchSend(fromAddress, toAddress, amount) {
  $.ajax({
    url: '/api/v2/send',
    contentType: 'application/json',
    method: 'POST',
    data: JSON.stringify({
      fromAddress: fromAddress,
      toAddress: toAddress,
      amount: amount,
    }),
    statusCode: {
      202: function(response) {
        console.log('res', response);
        loading.style.display = 'none';
        const { message } = response;
        alert(`트랜잭션 실패!! ${message}`);
      },
      200: function(result) {
        loading.style.display = 'none';
        alert('트랜잭션 성공');
        console.log('result', result);

        const { message } = result;
        console.log('data', message);
        window.location = '/main/' + fromAddress;
      },
    },
  }).fail(function(res) {
    console.log('res', res);
    loading.style.display = 'none';
    alert('서버 오류');
  });
}

function showPage() {
  var loader = $('div.loader');
  var container = $('div.container');
  loader.css('display', 'none');
  container.css('display', 'block');
}
