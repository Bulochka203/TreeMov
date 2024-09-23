document.querySelector('#settings-btn').addEventListener('click', function (e) {
  const group_list = doc.getElementById("add-save-btns");
  group_list.hidden = !group_list.hidden
  const btns = doc.getElementsByClassName("delete-btn-field");
  for (let i = 0; i < btns.length; i++) {
    let btn = btns[i];
    btn.hidden = !btn.hidden
  };
});
document.querySelector('#add-group-btn').addEventListener('click', function (e) {
  const modal = doc.getElementById("modal");
  modal.hidden = !modal.hidden
});
$(document).click(function (e) {
    if ($(e.target).is('.overlay-add-window')) {
      closeModal();
    }
});
function closeModal() {
  const modal = doc.getElementById("modal");
  const modal_report = doc.getElementById("modal-for-report");
  if (!modal.hidden && modal_report.hidden) {
      const input = doc.getElementById("input-group-name");
      input.value = ''
      $('#input-group-name').removeClass('is-invalid').addClass('is-valid');
      modal.hidden = !modal.hidden
  } else if (modal.hidden && !modal_report.hidden) {
      const groups = doc.getElementById('groups-modal')
      groups.innerHTML = ''
      modal_report.hidden = !modal_report.hidden
  }
};
$(document).ready(function (){
    $('#input-group-name').on('input', function () {
        $.ajax({
            data: $(this).serialize(),
            url: "validate_group_name",
            success: function (response) {
                const button = document.querySelector("#add-group-btn-modal");
                if (response.is_taken == true) {
                    if ($('#input-group-name').hasClass('is-valid')) {
                        $('#input-group-name').removeClass('is-valid').addClass('is-invalid');
                        $('#input-group-name').after('<div class="invalid-feedback d-block" id="usernameError">Группа с таким именем уже существует!</div>');
                        button.setAttribute('disabled', '');
                    }
                } else {
                    $('#input-group-name').removeClass('is-invalid').addClass('is-valid');
                    $('#usernameError').remove();
                    button.removeAttribute('disabled')
                }
            },
            error: function (response) {
                console.log(response.responseJSON.errors)
            }
        });
        return false;
    });
})
document.querySelector('#report-btn').addEventListener('click', function (e) {
  const modal = doc.getElementById("modal-for-report");
  const form = doc.getElementById('groups-modal')
  modal.hidden = !modal.hidden

  groups = doc.getElementsByClassName("group");
  group_info = [];
  for (let i = 0; i < groups.length; i++) {
    group_info.push({
        name: groups[i].querySelector('.group-name').textContent,
        value: groups[i].querySelector('[name="group-delete"]').value
    })
  }

  group_info.forEach((elem) => {
    form.innerHTML += `<label class="modal-checkbox"><input type="checkbox" name="groups" value=${elem.value}>${elem.name}</label>`
  });
});