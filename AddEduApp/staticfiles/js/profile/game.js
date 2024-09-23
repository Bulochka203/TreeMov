const MODELS_PATH = '/static/game/'
const PICTURES = {
  stage0: MODELS_PATH + 'tree_0.png',
  stage1: MODELS_PATH + 'tree_1.png',
  stage2: MODELS_PATH + 'tree_2.png',
  stage3: MODELS_PATH + 'tree_3.png',
  stage4: MODELS_PATH + 'tree_4.png',
  clouds: MODELS_PATH + 'clouds.png',
  ufo: MODELS_PATH + 'ufo.gif',
  drought: MODELS_PATH + 'drought.gif',
  rain: MODELS_PATH + 'rain.gif',
  delete_ufo: MODELS_PATH + 'ufo_delete.gif',
  delete_drought: MODELS_PATH + 'drought_delete.gif',
  delete_flood: MODELS_PATH + 'flood_delete.gif',
}
let CATACLYSM = ''
let TREE_STAGE = ''

$(document).ready(function () {
    $.ajax({
        data: $(this).serialize(),
        url: `tree_stage_progress/`,
        success: function (response) {
          const negativeEvent = response['negative_event']
          const loseTree = response['lose_tree']
          TREE_STAGE = response['tree_stage']

          const field = document.querySelector('#game')
          field.innerHTML = `<img class="clouds resize" src=${PICTURES['clouds']} />`

          if (loseTree) {
              CATACLYSM = ''
              TREE_STAGE = 0
              field.innerHTML += `<img class="tree-pic img0 resize" src=${PICTURES['stage0']} />`
          } else if (negativeEvent !== null) {
              if (negativeEvent[1] === 'UFO') {
                  CATACLYSM = 'UFO'
                  field.innerHTML += `<img class="tree-pic img2 resize" src=${PICTURES['ufo']} />`
              }
              if (negativeEvent[1] === 'Drought') {
                  CATACLYSM = 'Drought'
                  field.innerHTML += `<img class="tree-pic drought resize" src=${PICTURES['drought']} />`
              }
              if (negativeEvent[1] === 'Flood') {
                  CATACLYSM = 'Flood'
                  field.innerHTML += `<img class="tree-pic img2 resize" src=${PICTURES['rain']} />`
              }
          } else if (TREE_STAGE >= 0 && TREE_STAGE <= 4) {
              const stage = PICTURES['stage' + TREE_STAGE]
              const field = document.querySelector('#game')
              field.innerHTML += `<img class="clouds resize" src=${PICTURES['clouds']} />`

              var group = '';
              if (TREE_STAGE == 0 || TREE_STAGE == 1) {
                  group = 'tree-pic img0'
              } else {
                  group = 'tree-pic img1'
              }
              field.innerHTML += `<img class="${group} resize" src=${stage} />`
          }
        },
        error: function (response) {
            console.log(response.responseJSON.errors)
        }
    });

    if (document.querySelector('#game-start-btn')) {
        document.querySelector('#game-start-btn').addEventListener('click', plant_tree);
    } else if (document.querySelector('#collect-coins')) {
        document.querySelector('#collect-coins').addEventListener('click', collect_coins);
    }

    document.querySelector('#waterbucket').addEventListener('click', function (e) {
        let txt = '';
        let style = '';
        let flag = false;
        let counter_of_buster = +document.querySelector('#waterbucket-counter').textContent;

        if (CATACLYSM == '') {
            txt = 'Сейчас не нужно использовать ведро с водой'
            style = {background: "linear-gradient(to right, rgb(255, 95, 109), rgb(255, 195, 113))",}
        } else if (counter_of_buster < 1) {
            txt = 'У вас нет ведра с водой'
            style = {background: "linear-gradient(to right, rgb(255, 95, 109), rgb(255, 195, 113))",}
        } else {
            if (CATACLYSM !== 'Drought') {
                if (CATACLYSM === 'UFO') {
                    txt = 'Нельзя справится с НЛО с помощью ведра воды';
                } else {
                    txt = 'Нельзя справится с наводнением с помощью ведра воды';
                }
                style = {background: "linear-gradient(to right, rgb(255, 95, 109), rgb(255, 195, 113))",};
            } else {
                txt = 'Вы справились с засухой';
                flag = true;
            }
        };

        Toastify({
          text: txt,
          className: 'info',
          gravity: 'top',
          position: 'left',
          stopOnFocus: true,
          style: style,
        }).showToast();

        if (flag) {
            $.ajax({
                type: "POST",
                data: $('#waterbucket-form').serialize(),
                url: "repulse_the_attack/",
                success: function (response) {
                    const counter = document.querySelector('#waterbucket-counter')
                    const field = document.querySelector('#game')

                    CATACLYSM = ''

                    counter.innerText = response['buster_count']
                    field.querySelector('.tree-pic').remove()
                    field.innerHTML += `<img class="tree-pic img2 resize" src=${PICTURES['delete_drought']} />`
                    setTimeout(function () {
                        field.querySelector('.tree-pic').remove()
                        field.innerHTML += `<img class="tree-pic img1 resize" src=${PICTURES['stage' + response['tree_stage']]} />`
                    }, 2000);

                },
                error: function (response) {
                    console.log(response.responseJSON.errors)
                }
            });
        }
    });
    document.querySelector('#antimagnet').addEventListener('click', function (e) {
        let txt = '';
        let style = '';
        let flag = false;
        let counter_of_buster = +document.querySelector('#antimagnet-counter').textContent;

        if (CATACLYSM === '') {
            txt = 'Сейчас не нужно использовать антимагнит'
            style = {background: "linear-gradient(to right, rgb(255, 95, 109), rgb(255, 195, 113))",}
        } else if (counter_of_buster < 1) {
            txt = 'У вас нет антмагнита'
            style = {background: "linear-gradient(to right, rgb(255, 95, 109), rgb(255, 195, 113))",}
        } else {
            if (CATACLYSM !== 'UFO') {
                if (CATACLYSM === 'Drought') {
                    txt = 'Нельзя справится с засухой с помощью антимагнита';
                } else {
                    txt = 'Нельзя справится с наводнением с помощью антимагнита';
                }
                style = {background: "linear-gradient(to right, rgb(255, 95, 109), rgb(255, 195, 113))",};
            } else {
                txt = 'Вы отбили атаку НЛО';
                flag = true;
            };
        };

        Toastify({
          text: txt,
          className: 'info',
          gravity: 'top',
          position: 'left',
          stopOnFocus: true,
          style: style,
        }).showToast();

        if (flag) {
            $.ajax({
                type: "POST",
                data: $('#antimagnet-form').serialize(),
                url: "repulse_the_attack/",
                success: function (response) {
                    const counter = document.querySelector('#antimagnet-counter')
                    const field = document.querySelector('#game')

                    CATACLYSM = ''

                    counter.innerText = response['buster_count']
                    field.querySelector('.tree-pic').remove()
                    field.innerHTML += `<img class="tree-pic img2 resize" src=${PICTURES['delete_ufo']} />`
                    setTimeout(function () {
                        field.querySelector('.tree-pic').remove()
                        field.innerHTML += `<img class="tree-pic img1 resize" src=${PICTURES['stage' + response['tree_stage']]} />`
                    }, 1500);

                },
                error: function (response) {
                    console.log(response.responseJSON.errors)
                }
            });
        }
    });
    document.querySelector('#magicdom').addEventListener('click', function (e) {
        let txt = ''
        let style = ''
        let flag = false;
        let counter_of_buster = +document.querySelector('#magicdom-counter').textContent

        if (CATACLYSM === '') {
            txt = 'Сейчас не нужно использовать магический купол'
            style = {background: "linear-gradient(to right, rgb(255, 95, 109), rgb(255, 195, 113))",}
        } else if (counter_of_buster < 1) {
            txt = 'У вас нет магического купола'
            style = {background: "linear-gradient(to right, rgb(255, 95, 109), rgb(255, 195, 113))",}
        } else {
            if (CATACLYSM !== 'Flood') {
                if (CATACLYSM === 'Drought') {
                    txt = 'Нельзя справится с засухой с помощью магического купола'
                } else {
                    txt = 'Нельзя справится с атакой НЛО с помощью магического купола'
                }
                style = {background: "linear-gradient(to right, rgb(255, 95, 109), rgb(255, 195, 113))",}
            } else {
                txt = 'Вы отбили наводнение'
                flag = true;
            }
        }

        Toastify({
          text: txt,
          className: 'info',
          gravity: 'top',
          position: 'left',
          stopOnFocus: true,
          style: style,
        }).showToast();

        if (flag) {
            $.ajax({
                type: "POST",
                data: $('#magicdom-form').serialize(),
                url: "repulse_the_attack/",
                success: function (response) {
                    const counter = document.querySelector('#magicdom-counter')
                    const field = document.querySelector('#game')

                    CATACLYSM = ''

                    counter.innerText = response['buster_count']
                    field.querySelector('.tree-pic').remove()
                    field.innerHTML += `<img class="tree-pic img2 resize" src=${PICTURES['delete_flood']} />`
                    setTimeout(function () {
                        field.querySelector('.tree-pic').remove()
                        field.innerHTML += `<img class="tree-pic img1 resize" src=${PICTURES['stage' + response['tree_stage']]} />`
                    }, 1500);

                },
                error: function (response) {
                    console.log(response.responseJSON.errors)
                }
            });
        }
    });
})

function plant_tree() {
    $.ajax({
        data: $(this).serialize(),
        url: "plant_tree/",
        success: function (response) {
            if (response['created']) {
                TREE_STAGE = 1
                const field = document.querySelector('#game')
                rename_button()
                field.innerHTML += `<img class="clouds resize" src=${PICTURES['clouds']} />`
                field.querySelector('.tree-pic').remove()
                field.innerHTML += `<img class="tree-pic img0 resize" src=${PICTURES['stage1']} />`
            }
        },
        error: function (response) {
            console.log(response.responseJSON.errors)
        }
    });
}

function collect_coins() {
    if (CATACLYSM !== '') {
        Toastify({
          text: 'Вы не можете собрать урожай во время нападения',
          className: 'info',
          gravity: 'top',
          position: 'left',
          stopOnFocus: true,
          style: {background: "linear-gradient(to right, rgb(255, 95, 109), rgb(255, 195, 113))",},
        }).showToast();
    } else if (TREE_STAGE != 4) {
        Toastify({
          text: 'Дерево ещё не выросло',
          className: 'info',
          gravity: 'top',
          position: 'left',
          stopOnFocus: true,
          style: {background: "linear-gradient(to right, rgb(255, 95, 109), rgb(255, 195, 113))",},
        }).showToast();
    } else {
        $.ajax({
            data: $(this).serialize(),
            url: "collect_coins/",
            success: function (response) {
                const field = document.querySelector('#game')
                field.innerHTML += `<img class="clouds resize" src=${PICTURES['clouds']} />`
                field.querySelector('.tree-pic').remove()
                field.innerHTML += `<img class="tree-pic img1 resize" src=${PICTURES['stage3']} />`
                TREE_STAGE--

                Toastify({
                  text: 'Урожай собран',
                  className: 'info',
                  gravity: 'top',
                  position: 'left',
                  stopOnFocus: true,
                }).showToast();
            },
            error: function (response) {
                console.log(response.responseJSON.errors)
            }
        });
    }
}

function rename_button() {
    if (document.querySelector('#game-start-btn')) {
        const btn = document.querySelector('#game-start-btn')
        $('#game-start-btn').off()
        btn.id = 'collect-coins'
        btn.textContent = 'Собрать урожай'
        btn.addEventListener('click', collect_coins);
    } else if (document.querySelector('#collect-coins')) {
        const btn = document.querySelector('#collect-coins')
        $('#collect-coins').off()
        btn.id = 'game-start-btn'
        btn.textContent = 'Посадить'
        btn.addEventListener('click', plant_tree);
    }
}