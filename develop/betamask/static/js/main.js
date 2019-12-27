const modal = document.querySelector('.modal-wrapper');

$('#modal-open-button').click(function() {
  //   console.log('button');
  modal.style.display = 'flex';
});

$('#close').click(function() {
  modal.style.display = 'none';
});
