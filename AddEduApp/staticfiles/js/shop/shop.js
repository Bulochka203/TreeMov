BALANCE = 0

window.addEventListener("load", function() {
    const btns = document.getElementsByClassName('buster-buy-button')
    const modal = document.getElementById("modal");
    for (let i = 0; i < btns.length; i++) {
        btns[i].addEventListener('click', function (e) {
            const div = e.target.closest('.div-item');
            const title = div.querySelector('.buster-title').textContent;
            const description = div.querySelector('.buster-description').textContent;
            const cost = div.querySelector('.buster-cost').textContent;
            const img_src = div.closest('.item-container').querySelector('.shop-item-img').src;
            const buster_id = div.querySelector('.buster-id').value;

            const modal_title = document.querySelector('#modal-title');
            const modal_description = document.querySelector('#modal-description');
            const modal_cost = document.querySelector('#modal-cost');
            const modal_img = document.querySelector('#modal-img');
            const modal_buster_id = document.querySelector('#buster-id-modal');
            const confirm_btn = document.querySelector('#confirm');

            modal_title.innerText = title;
            modal_description.innerText = description;
            modal_cost.innerText = +cost;
            modal_img.src = img_src;
            modal_buster_id.value = buster_id;

            modal.hidden = !modal.hidden
        });
    }
})
$(document).click(function (e) {
    if ($(e.target).is('.overlay-add-window')) {
      closeModal();
    }
});
function closeModal() {
  const modal = document.getElementById("modal");
  modal.hidden = !modal.hidden
};