const mark = '<div class="dot"><svg class="markk" viewBox="0 0 8 8" fill="none" xmlns="http://www.w3.org/2000/svg"><circle cx="4" cy="4" r="4" fill="url(#paint0_linear_401_1851)"/><defs><linearGradient id="paint0_linear_401_1851" x1="4" y1="0" x2="4" y2="8" gradientUnits="userSpaceOnUse"><stop stop-color="#A816DB"/><stop offset="0.979167" stop-color="#16C1DB"/><stop offset="1" stop-color="#D9D9D9" stop-opacity="0"/></linearGradient></defs></svg><div>';
Months =['Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь', 'Июль', 'Август', 'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь'];
const button_next = '<button id="btnNext" class="next-prev-months"><svg class="next-month-svg" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M21.6 11.4L13.8375 3.525C13.5 3.1875 12.975 3.1875 12.6375 3.525C12.3 3.8625 12.3 4.3875 12.6375 4.725L18.9375 11.1375H3C2.55 11.1375 2.175 11.5125 2.175 11.9625C2.175 12.4125 2.55 12.825 3 12.825H19.0125L12.6375 19.3125C12.3 19.65 12.3 20.175 12.6375 20.5125C12.7875 20.6625 13.0125 20.7375 13.2375 20.7375C13.4625 20.7375 13.6875 20.6625 13.8375 20.475L21.6 12.6C21.9375 12.2625 21.9375 11.7375 21.6 11.4Z" fill="white"/></svg></button>'
const button_previusly = '<button id="btnPrev" class="next-prev-months"><svg class="prev-month-svg" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M21 11.175H4.98751L11.3625 4.6875C11.7 4.35 11.7 3.825 11.3625 3.4875C11.025 3.15 10.5 3.15 10.1625 3.4875L2.40001 11.3625C2.06251 11.7 2.06251 12.225 2.40001 12.5625L10.1625 20.4375C10.3125 20.5875 10.5375 20.7 10.7625 20.7C10.9875 20.7 11.175 20.625 11.3625 20.475C11.7 20.1375 11.7 19.6125 11.3625 19.275L5.02501 12.8625H21C21.45 12.8625 21.825 12.4875 21.825 12.0375C21.825 11.55 21.45 11.175 21 11.175Z" fill="white"/></svg></button>'
var Cal = function(divId) {
  this.divId = divId;
  this.DaysOfWeek = [
    'Пн',
    'Вт',
    'Ср',
    'Чт',
    'Пт',
    'Сб',
    'Вс'
  ];
  Months =['Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь', 'Июль', 'Август', 'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь'];
  var d = new Date();
  this.currMonth = d.getMonth();
  this.currYear = d.getFullYear();
  this.currDay = d.getDate();
};
function set_marks() {
  const year_number = document.getElementById('year-number').value
  const month_name = document.getElementById('month-name').innerHTML
  const month_number = Months.indexOf(month_name) + 1

  $.ajax({
        data: $(this).serialize(),
        url: `get_all_events/${month_number}/${year_number}`,
        success: function (response) {
        exceptions = [...response.exceptions]
            document.querySelectorAll('.this-month-day').forEach((element) => {
                let num = +element.querySelector('.number').innerHTML;
                if (response.exceptions.indexOf(num) !== -1 && response.dates.indexOf(num) != -1) {
                    element.innerHTML += mark
                }
                if (response.exceptions.indexOf(num) === -1) {
                    if (response.dates.indexOf(num) != -1 || response.week_days.indexOf(new Date(year_number, month_number - 1, num).getDay()) !== -1)  {
                        element.innerHTML += mark
                    }
                }
            });
        },
        error: function (response) {
            console.log(response.responseJSON.errors)
        }
    });
}
function set_listeners_to_numbers() {
    const month_name = document.getElementById('month-name').innerHTML
    const month_number = Months.indexOf(month_name) + 1
    const year = document.getElementById('year-number').value

    document.querySelectorAll('.this-month-day').forEach((element) => {

        // при клике добавляется стиль выделения, очищаются все ивенты, и идёт аякс запрос для добавления ивентов которые есть сегодня
        element.addEventListener('click', function (e) {
            const remove_selected = document.getElementById('selected')
            if (remove_selected !== null) {
                remove_selected.removeAttribute('id')
            }
            element.setAttribute('id', 'selected');

            const day_of_the_month = element.querySelector('.number').innerHTML
            const event_list = document.getElementById('events')
            event_list.innerHTML = ''

            $.ajax({
                data: $(this).serialize(),
                url: `get_events/${month_number}/${day_of_the_month}/${year}`,
                success: function (response) {
                    response.events.forEach((item) => {
                        event_list.insertAdjacentHTML('beforeEnd', get_event(item.title, item.time, item.group, item.event_pk))
                    })
                },
                error: function (response) {
                    console.log(response.responseJSON.errors)
                }
            });
        });
    });
}
// Переход к следующему месяцу
Cal.prototype.nextMonth = function() {
  const year = document.getElementById('year-number')
  if ( this.currMonth == 11 ) {
    this.currMonth = 0;
    this.currYear = this.currYear + 1;
    year.value = this.currYear + 1
  }
  else {
    this.currMonth = this.currMonth + 1;
  }
  this.showcurr();
  set_marks();
  set_listeners_to_numbers();
  const event_list = document.getElementById('events');
  event_list.innerHTML = '';
  addListenersToNextAndPreviusMonth(this)
};
// Переход к предыдущему месяцу
Cal.prototype.previousMonth = function() {
  const year = document.getElementById('year-number')
  if ( this.currMonth == 0 ) {
    this.currMonth = 11;
    this.currYear = this.currYear - 1;
    year.value = this.currYear - 1
  }
  else {
    this.currMonth = this.currMonth - 1;
  }
  this.showcurr();
  set_marks();
  set_listeners_to_numbers();
  const event_list = document.getElementById('events');
  event_list.innerHTML = '';
  addListenersToNextAndPreviusMonth(this)
};
// Показать текущий месяц
Cal.prototype.showcurr = function() {
  this.showMonth(this.currYear, this.currMonth);
};
// Показать месяц (год, месяц)
Cal.prototype.showMonth = function(y, m) {
  var d = new Date()
  , firstDayOfMonth = new Date(y, m, 7).getDay() // Первый день недели в выбранном месяце
  , lastDateOfMonth =  new Date(y, m+1, 0).getDate() // Последний день выбранного месяца
  , lastDayOfLastMonth = m == 0 ? new Date(y-1, 11, 0).getDate() : new Date(y, m, 0).getDate(); // Последний день предыдущего месяца
  var html = '<table>';
  html += '<thead><tr>';
  html += '<td colspan="7" class="calendar-text"><div class="month">' + button_previusly + '<p id="month-name">' + Months[m] + '</p>' + button_next + '</div></td>';
  html += '<input autocomplete="off" type="hidden" name="year-number" id="year-number" value="' + this.currYear + '">';
  html += '</tr></thead>';
  html += '</tr>';
  var i=1;
  do {
    var dow = new Date(y, m, i).getDay();
    // Начать новую строку в понедельник
    if ( dow == 1 ) {
      html += '<tr>';
    }
    // Если первый день недели не понедельник показать последние дни предыдущего месяца
    else if ( i == 1 ) {
      html += '<tr>';
      var k = lastDayOfLastMonth - firstDayOfMonth+1;
      for(var j=0; j < firstDayOfMonth; j++) {
        html += '<td class="calendar-text not-current">' + '<p class="number">' + k + '</p>' + '</td>';
        k++;
      }
    }
    var chk = new Date();
    var chkY = chk.getFullYear();
    var chkM = chk.getMonth();
    if (chkY == this.currYear && chkM == this.currMonth && i == this.currDay) {
      html += '<td class="this-month-day calendar-text current today">' + '<p class="number">' + i + '</p></td>';
    } else {
      html += '<td class="this-month-day calendar-text current">' + '<p class="number">' + i + '</p></td>';
    }
    // закрыть строку в воскресенье
    if ( dow == 0 ) {
      html += '</tr>';
    }
    // Если последний день месяца не воскресенье, показать первые дни следующего месяца
    else if ( i == lastDateOfMonth ) {
      var k=1;
      for(dow; dow < 7; dow++) {
        html += '<td class="calendar-text not-current">' + '<p class="number">' + k + '</p>' + '</td>';
        k++;
      }
    }
    i++;
  }while(i <= lastDateOfMonth);
  html += '</table>';
  document.getElementById(this.divId).innerHTML = html;
};
window.onload = function() {
  var c = new Cal("divCal");
  c.showcurr();

  addListenersToNextAndPreviusMonth(c)
}
// Привязываем кнопки «Следующий» и «Предыдущий»
function addListenersToNextAndPreviusMonth(c) {
  getId('btnNext').onclick = function() {
    c.nextMonth();
  };
  getId('btnPrev').onclick = function() {
    c.previousMonth();
  };
}
function getId(id) {
  return document.getElementById(id);
}

window.addEventListener("load", function() {
    const year_number = document.getElementById('year-number').value
    const month_name = document.getElementById('month-name').innerHTML
    const month_number = Months.indexOf(month_name) + 1

    set_marks();

    document.querySelectorAll('.this-month-day').forEach((element) => {
        // при загрузке страницы выделяется сегодняшний день
        const today = document.getElementsByClassName('today')[0]
        today.setAttribute('id', 'selected');

        // при клике добавляется стиль выделения, очищаются все ивенты, и идёт аякс запрос для добавления ивентов которые есть сегодня
        element.addEventListener('click', function (e) {
            const remove_selected = document.getElementById('selected')
            if (remove_selected !== null) {
                remove_selected.removeAttribute('id')
            }
            element.setAttribute('id', 'selected');

            const day_of_the_month = element.querySelector('.number').innerHTML
            const event_list = document.getElementById('events')
            event_list.innerHTML = ''

            const year = document.getElementById('year-number').value

            $.ajax({
                data: $(this).serialize(),
                url: `get_events/${month_number}/${day_of_the_month}/${year}`,
                success: function (response) {
                    response.events.forEach((item) => {
                        event_list.insertAdjacentHTML('beforeEnd', get_event(item.title, item.time, item.group, item.event_pk))
                    })
                },
                error: function (response) {
                    console.log(response.responseJSON.errors)
                }
            });
        });
    });
});

function get_event(title, time, group, event_pk) {
 return `<div class="event">
  <div class="event-svg">
    <svg class="timer-img" viewBox="0 0 51 51" fill="none" xmlns="http://www.w3.org/2000/svg">
      <path opacity="0.4" d="M25.4999 46.7498C30.3862 46.7498 35.0724 44.8088 38.5275 41.3537C41.9826 37.8985 43.9237 33.2124 43.9237 28.3261C43.9237 23.4398 41.9826 18.7537 38.5275 15.2985C35.0724 11.8434 30.3862 9.90234 25.4999 9.90234C20.6136 9.90234 15.9275 11.8434 12.4724 15.2985C9.01724 18.7537 7.07617 23.4398 7.07617 28.3261C7.07617 33.2124 9.01724 37.8985 12.4724 41.3537C15.9275 44.8088 20.6136 46.7498 25.4999 46.7498Z" fill="url(#paint0_linear_401_1411)"/>
      <path d="M25.4999 29.2188C24.6286 29.2188 23.9061 28.4963 23.9061 27.625V17C23.9061 16.1287 24.6286 15.4062 25.4999 15.4062C26.3711 15.4062 27.0936 16.1287 27.0936 17V27.625C27.0936 28.4963 26.3711 29.2188 25.4999 29.2188ZM31.6411 7.33125H19.3586C18.5086 7.33125 17.8286 6.65125 17.8286 5.80125C17.8286 4.95125 18.5086 4.25 19.3586 4.25H31.6411C32.4911 4.25 33.1711 4.93 33.1711 5.78C33.1711 6.63 32.4911 7.33125 31.6411 7.33125Z" fill="url(#paint1_linear_401_1411)"/>
      <defs>
        <linearGradient id="paint0_linear_401_1411" x1="25.4999" y1="9.90234" x2="25.4999" y2="46.7498" gradientUnits="userSpaceOnUse">
          <stop stop-color="#A816DB"/>
          <stop offset="1" stop-color="#16C1DB"/>
        </linearGradient>
        <linearGradient id="paint1_linear_401_1411" x1="25.4999" y1="4.25" x2="25.4999" y2="29.2188" gradientUnits="userSpaceOnUse">
          <stop stop-color="#A816DB"/>
          <stop offset="1" stop-color="#16C1DB"/>
        </linearGradient>
      </defs>
    </svg>
  </div>
  <div class="event-text-block">
    <p class="event-text-title">${title}</p>
    <p class="event-text-title">${time}</p>
    <p class="event-text-group">Группа: “${group}”</p>
  </div>
  <div id="delete-event-block" class="delete-event-block">
    <button hidden class="delete-event-btn" onclick="open_delete_modal(${event_pk})">
      <svg class="delete-event-svg" viewBox="0 0 57 57" fill="none" xmlns="http://www.w3.org/2000/svg">
        <g clip-path="url(#clip0_401_2314)">
          <path opacity="0.4" d="M40.0692 40.0694C46.5781 33.5605 46.5781 23.0081 40.0692 16.4992C33.5603 9.99027 23.0079 9.99027 16.499 16.4992C9.99006 23.0081 9.99006 33.5605 16.499 40.0694C23.0079 46.5783 33.5603 46.5783 40.0692 40.0694Z" fill="black"/>
          <path d="M32.1144 22.6864L28.2842 26.5165L24.4541 22.6864C23.9709 22.2032 23.1695 22.2032 22.6863 22.6864C22.2031 23.1696 22.2031 23.971 22.6863 24.4541L26.5165 28.2843L22.6863 32.1145C22.2031 32.5977 22.2031 33.399 22.6863 33.8822C23.1695 34.3654 23.9709 34.3654 24.4541 33.8822L28.2842 30.0521L32.1144 33.8822C32.5976 34.3654 33.399 34.3654 33.8822 33.8822C34.3654 33.399 34.3654 32.5977 33.8822 32.1145L30.052 28.2843L33.8822 24.4541C34.3654 23.971 34.3654 23.1696 33.8822 22.6864C33.399 22.2032 32.5976 22.2032 32.1144 22.6864Z" fill="black"/>
        </g>
        <defs>
          <clipPath id="clip0_401_2314">
            <rect width="40" height="40" fill="white" transform="translate(0 28.2843) rotate(-45)"/>
          </clipPath>
        </defs>
      </svg>
    </button>
    <button hidden class="update-event-btn" onclick="open_update_modal(${event_pk})">
        <svg class="update-event-svg" viewBox="0 0 40 40" fill="none" xmlns="http://www.w3.org/2000/svg">
          <path opacity="0.4" d="M18.3335 26.9167V31.4167C18.3335 35.1667 16.8335 36.6667 13.0835 36.6667H8.5835C4.8335 36.6667 3.3335 35.1667 3.3335 31.4167V26.9167C3.3335 23.1667 4.8335 21.6667 8.5835 21.6667H13.0835C16.8335 21.6667 18.3335 23.1667 18.3335 26.9167ZM29.1668 18.3333C30.1517 18.3333 31.127 18.1393 32.037 17.7624C32.9469 17.3855 33.7737 16.8331 34.4701 16.1366C35.1666 15.4402 35.719 14.6134 36.0959 13.7035C36.4728 12.7935 36.6668 11.8182 36.6668 10.8333C36.6668 9.84841 36.4728 8.87314 36.0959 7.9632C35.719 7.05326 35.1666 6.22647 34.4701 5.53003C33.7737 4.83359 32.9469 4.28114 32.037 3.90423C31.127 3.52732 30.1517 3.33333 29.1668 3.33333C27.1777 3.33333 25.2701 4.1235 23.8635 5.53003C22.457 6.93655 21.6668 8.8442 21.6668 10.8333C21.6668 12.8225 22.457 14.7301 23.8635 16.1366C25.2701 17.5432 27.1777 18.3333 29.1668 18.3333Z" fill="url(#paint0_linear_718_337)"/>
              <path d="M24.6335 36.6667C24.4121 36.6654 24.195 36.6056 24.0043 36.4932C23.8135 36.3808 23.6559 36.2199 23.5476 36.0269C23.4392 35.8339 23.3839 35.6155 23.3873 35.3942C23.3906 35.1728 23.4526 34.9563 23.5668 34.7667L25.1835 32.0667C25.5335 31.4667 26.3002 31.2833 26.9002 31.6333C27.5002 31.9833 27.6835 32.75 27.3335 33.35L27.0335 33.85C29.0792 33.3194 30.891 32.1251 32.185 30.4541C33.4789 28.7831 34.1818 26.73 34.1835 24.6167C34.1835 23.9333 34.7502 23.3667 35.4335 23.3667C36.1168 23.3667 36.6668 23.9333 36.6668 24.6333C36.6668 31.2667 31.2668 36.6667 24.6335 36.6667ZM4.5835 16.6167C3.90016 16.6167 3.3335 16.0667 3.3335 15.3667C3.3335 8.73333 8.7335 3.33333 15.3668 3.33333C15.8335 3.33333 16.2335 3.58333 16.4668 3.96666C16.6835 4.36666 16.6835 4.83333 16.4502 5.23333L14.8335 7.91666C14.4668 8.51666 13.7002 8.71666 13.1168 8.35C12.9753 8.26607 12.8518 8.15499 12.7533 8.02316C12.6549 7.89132 12.5834 7.74131 12.5432 7.58178C12.5029 7.42224 12.4946 7.25631 12.5186 7.09354C12.5427 6.93077 12.5988 6.77437 12.6835 6.63333L12.9835 6.13333C8.8835 7.19999 5.8335 10.9333 5.8335 15.3667C5.8335 16.0667 5.26683 16.6167 4.5835 16.6167Z" fill="url(#paint1_linear_718_337)"/>
              <defs>
                <linearGradient id="paint0_linear_718_337" x1="20.0002" y1="3.33333" x2="20.0002" y2="36.6667" gradientUnits="userSpaceOnUse">
                  <stop stop-color="#A816DB"/>
                  <stop offset="1" stop-color="#16C1DB"/>
                </linearGradient>
                <linearGradient id="paint1_linear_718_337" x1="20.0002" y1="3.33333" x2="20.0002" y2="36.6667" gradientUnits="userSpaceOnUse">
                  <stop stop-color="#A816DB"/>
                  <stop offset="1" stop-color="#16C1DB"/>
                </linearGradient>
              </defs>
            </svg>
          </button>
  </div>
</div>`
}