function toggle() {
    const div = document.querySelector('#teacher-code')
    div.required = false;
    console.log(div)
    if (this.checked) {
        div.hidden = !div.hidden
    } else {
        div.hidden = !div.hidden
    }
}
$(document).ready(function () {
    document.querySelector('#checkbox').onchange = toggle;
});