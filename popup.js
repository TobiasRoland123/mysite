document.querySelectorAll('.open-dialog-btn').forEach((itemOpenBtn) => {
  itemOpenBtn.addEventListener('click', function () {
    showDialog(this.getAttribute('data-dialog-id'));
  });
});

document.querySelectorAll('.close-dialog-btn').forEach((itemCloseBtn) => {
  itemCloseBtn.addEventListener('click', function () {
    closeDialog(this.getAttribute('data-dialog-id'));
  });
});
function showDialog(dataDialogId) {
  const dialog = document.querySelector(`#${dataDialogId}`);
  dialog.showModal();
}

function closeDialog(dataDialogId) {
  const dialog = document.querySelector(`#${dataDialogId}`);
  dialog.close();
}
