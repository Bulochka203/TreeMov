const doc = window.document;
const links = doc.querySelectorAll(".group-event");
const linksCount = links.length;
const currentURL = doc.URL;

for (let i = 0; i < linksCount; i++) {
    let linkURL = links[i].href;
    if (currentURL === linkURL) {
        if (links[i].children[0].className.baseVal.indexOf("nav-home-student") !== -1) {
            links[i].innerHTML =
    }
}