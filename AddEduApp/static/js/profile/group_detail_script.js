document.querySelector('#detail-settings-btn').addEventListener('click', function (e) {
  const group_list = doc.getElementById("add-save-btns");
  group_list.hidden = !group_list.hidden
  const btns = doc.getElementsByClassName("delete-btn-field");
  const btns_delete = doc.getElementsByClassName("detail-btns");
  for (let i = 0; i < btns_delete.length; i++) {
    let btn_delete = btns_delete[i];
    btn_delete.hidden = !btn_delete.hidden
  };
  for (let i = 0; i < btns.length; i++) {
    console.log()
    let btn = btns[i];
    btn.hidden = !btn.hidden
  };
});
const add_enegry_btns = document.querySelectorAll('.add-energy');
for (let i = 0; i < add_enegry_btns.length; i++) {
    add_enegry_btns[i].addEventListener('click', function (e) {
        const modal = doc.getElementById("modal-detail");
        student_id = add_enegry_btns[i].querySelector('.student-pk').value;
        student_num = add_enegry_btns[i].id
        insertData('энергии', student_num[student_num.length - 1], student_id);
        modal.hidden = !modal.hidden
    })
};
$(document).click(function (e) {
    if ($(e.target).is('.overlay-add-window')) {
      closeModal();
    }
});
function closeModal() {
  const modal = doc.getElementById("modal-detail");
  modal.hidden = !modal.hidden
  const title = doc.querySelector(".modal-title-text");
  title.innerHTML = "Начисление "
  const insert_field = doc.querySelector(".student-name-modal");
  insert_field.innerHTML = ""
  const counter = document.getElementById('counter');
  counter.textContent = 1;
  const type = doc.querySelector("#add-type");
  type.value = "";
  const student = doc.querySelector("#student-add");
  student.value = ""
};
function insertData(add_title_text, num_of_student, student_pk) {
  const title = doc.querySelector(".modal-title-text");
  const type = doc.querySelector("#add-type");
  const student = doc.querySelector("#student-add");
  student.value = student_pk
  if (add_title_text === 'монет') {
      type.value = 'money';
  } else if (add_title_text === 'энергии') {
      type.value = 'energy';
  };
  title.innerHTML += add_title_text;
  const insert_field = doc.querySelector(".student-name-modal");
  const name = doc.getElementById("student-" + num_of_student).textContent;
  insert_field.innerHTML += name
};
$('#modal-detail').ready(function(){
document.getElementById('decrement').addEventListener('click', function(event) {
  event.preventDefault();
  incrementCounter(-1)
});
document.getElementById('increment').addEventListener('click', function(event) {
  event.preventDefault();
  incrementCounter(+1)
});
document.getElementById('modal-btns-cancel').addEventListener('click', function(event) {
  event.preventDefault();
  closeModal();
});
})
function incrementCounter(value) {
    const counter = document.getElementById('counter');
    const input_counter = document.getElementById('input-counter');
    let val = +counter.textContent + value;
    if (val < 1) {
        val = 1
    }
    counter.textContent = val;
    input_counter.value = val;
}
document.querySelector('#create_ref_link').addEventListener('click', () => {
    navigator.clipboard.writeText(window.location.host + document.querySelector("#link").value).then(function() {
        alert('Текст скопирован');
    }, function(err) {
        console.error('Произошла ошибка при копировании текста: ', err);
    })
});