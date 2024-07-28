function addWebringEducation(response) {
    var base = $("<div>", {class: "webring-container-edu"});
    var inner = $("<div>", {class: "inner-webring-container-edu"});

    inner.append($("<h2>").html("Part of the <span>" + response.name + "</span> webring"));
    inner.append($("<img>", {src:"../WebRings/images/book.gif"}));
    inner.append($("<p>").text("Learn more on the other sites of this ring!"));
    var links = $("<div>", {class: "webring-links-edu"});
    links.append("[")
    links.append($("<a>", {href: response.previous_site_url, style: "margin: 0 10px;", target:"_top"}).text("Previous"));
    links.append("] [")
    links.append($("<a>", {href: response.next_site_url, style: "margin: 0 10px;", target:"_top"}).text("Next"));
    links.append("]");
    inner.append(links);
    inner.append($("<p>", {class: "copyright-edu"}).text("©1991 Webringer"));

    base.append(inner);
    base.appendTo("#webring");
}


document.addEventListener('DOMContentLoaded', (event) => {
    var base_url = "http://localhost:8000/webring/?site="
    
    $.get(base_url.concat(window.site_name).concat("&ring=education"), function (data) {
        addWebringEducation(data);
    });
});


