// Настройки
Months =['Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь', 'Июль', 'Август', 'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь'];
$(document).ready(function() {
    const settings_button = document.getElementById('calendar-settings-btn')
    if (settings_button !== null) {
        settings_button.addEventListener('click', function (e) {
            const btns = doc.getElementById("delete-update-add-event-btns");
            const title = doc.getElementById("calendar-title");
            const dialog = doc.getElementById("add-event-dialog");
            const events = doc.getElementById("events");
            if (btns.hidden && dialog.hidden) {
                title.innerHTML = 'Настройки'
            } else {
                title.innerHTML = 'Календарь'
            }
            if (!dialog.hidden) {
                dialog.hidden = !dialog.hidden
            } else {
                btns.hidden = !btns.hidden
            }
            events.hidden = !events.hidden
            const delete_btns = doc.getElementsByClassName("delete-event-btn");
            const update_btns = doc.getElementsByClassName("update-event-btn");
            if (delete_btns.length > 0 && !delete_btns[0].hidden) {
                for (let i = 0; i < delete_btns.length; i++) {
                    let btn = delete_btns[i];
                    btn.hidden = !btn.hidden
                };
            }
            if (update_btns.length > 0 && !update_btns[0].hidden) {
                for (let i = 0; i < update_btns.length; i++) {
                    let btn = update_btns[i];
                    btn.hidden = !btn.hidden
                };
            }
        });
    }
});
// Добавить
$(document).ready(function() {
    document.getElementById('add-event').addEventListener('click', function (e) {
        document.getElementById('add-update-event-form').reset();
        const btns = doc.getElementById("delete-update-add-event-btns");
        const title = doc.getElementById("calendar-title");
        const dialog = doc.getElementById("add-event-dialog");
        if (btns.hidden) {
            title.innerHTML = 'Настройки'
        } else {
            title.innerHTML = 'Добавить'
        }
        btns.hidden = !btns.hidden
        dialog.hidden = !dialog.hidden
    });
});
// Изменить
$(document).ready(function() {
    document.getElementById('update-event').addEventListener('click', function (e) {
    const delete_update_add = doc.getElementById("delete-update-add-event-btns");
    const btns = doc.getElementsByClassName("update-event-btn");
    const dialog = doc.getElementById("add-event-dialog");
    const title = doc.getElementById("calendar-title");
    if (btns.hidden) {
        title.innerHTML = 'Настройки'
    } else {
        title.innerHTML = 'Изменить'
    }
    delete_update_add.hidden = !delete_update_add.hidden
    events.hidden = !events.hidden
    for (let i = 0; i < btns.length; i++) {
            let btn = btns[i];
            btn.hidden = !btn.hidden
        };
    });
});
// Удалить
$(document).ready(function() {
    document.getElementById('delete-event').addEventListener('click', function (e) {
        const btns = doc.getElementsByClassName("delete-event-btn");
        const delete_update_add = doc.getElementById("delete-update-add-event-btns");
        const title = doc.getElementById("calendar-title");
        const events = doc.getElementById("events");
        if (delete_update_add.hidden) {
            title.innerHTML = 'Настройки'
        } else {
            title.innerHTML = 'Удалить'
        }
        delete_update_add.hidden = !delete_update_add.hidden
        events.hidden = !events.hidden
        for (let i = 0; i < btns.length; i++) {
            let btn = btns[i];
            btn.hidden = !btn.hidden
        };
    });
});
// Проверка корректности введенного времени
function validationTime() {
    const start_time = document.getElementById("start-time");
    const end_time = document.getElementById("end-time");
    const div = document.getElementById("usernameError");
    const btn = document.getElementById("save-event-btn");
    if (start_time.value > end_time.value && div.hidden) {
        div.hidden = !div.hidden
        btn.disabled = true
    } else if (start_time.value <= end_time.value && !div.hidden) {
        div.hidden = !div.hidden
        btn.disabled = false
    }
}
function open_delete_modal(event) {
    insert_in_delete_modal();
    const modal = doc.getElementById("delete-modal");
    const input = doc.getElementById("event_pk");
    input.value = event
    modal.hidden = !modal.hidden
}
$(document).click(function (e) {
    if ($(e.target).is('.overlay-add-window')) {
      closeModal();
    }
});
function closeModal() {
  const modal = doc.getElementById("delete-modal");
  modal.hidden = !modal.hidden
};
function insert_in_delete_modal() {
    const day = document.querySelector('#selected').querySelector('.number').innerHTML;
    const input_field = document.querySelector('#delete-date');
    const month_name = document.getElementById('month-name').innerHTML;
    const month = Months.indexOf(month_name);
    const year = document.querySelector('#year-number').value;
    console.log(day, month, year);
    input_field.value = `${day}-${month+1}-${year}`;
}
function open_update_modal(event) {
    document.getElementById('add-update-event-form').reset();
    const btns = doc.getElementById("delete-update-add-event-btns");
    const title = doc.getElementById("calendar-title");
    const dialog = doc.getElementById("add-event-dialog");
    const data = 'event-title select date start-time end-time every-week-checkbox'
    if (btns.hidden) {
        title.innerHTML = 'Настройки'
    } else {
        title.innerHTML = 'Изменить'
    }


    $.ajax({
        data: $(this).serialize(),
        url: `get_event_data/${event}`,
        success: function (response) {
            console.log(response)
            const title = doc.getElementById('event-title')
            const select_group = doc.getElementById('select-group')
            const date = doc.getElementById('date')
            const start_time = doc.getElementById('start-time')
            const end_time = doc.getElementById('end-time')
            const checkbox = doc.getElementById('every-week-checkbox')
            const save_btn = doc.getElementById('save-event-btn')
            const event_pk = doc.getElementById('updated-event-pk')
            event_pk.value = event

            const input_start_time = new Date(Date.parse(response.start_time))
            const input_end_time = new Date(Date.parse(response.end_time))

            title.value = response.title;
            select_group.value = response.group_pk;
            date.value = response.date;
            start_time.value = input_start_time.getHours() + ':' + (input_start_time.getMinutes() === 0 ? '00' : input_start_time.getMinutes());
            console.log(input_end_time.getHours() + ':' + input_end_time.getMinutes())
            end_time.value = input_end_time.getHours() + ':' + (input_end_time.getMinutes() === 0 ? '00' : input_end_time.getMinutes());
            console.log(response.every_week)
            if (response.every_week) {
                checkbox.checked  = true;
            } else {
                checkbox.checked  = false;
            }

            const events = doc.getElementById("events");
            save_btn.textContent = 'Изменить';
            events.hidden = !events.hidden;
            dialog.hidden = !dialog.hidden;
        },
        error: function (response) {
            console.log(response.responseJSON.errors)
        }
    });
}