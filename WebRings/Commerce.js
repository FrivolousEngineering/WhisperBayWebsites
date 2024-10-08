function addWebring(response) {
    var base = $("<div>", {class: "webring-container"});
    var inner = $("<div>", {class: "inner-webring-container"});

    inner.append($("<h2>").html("Part of the <span>" + response.name + "</span> webring"));
    inner.append($("<img>", {src:"../WebRings/images/Trolley.gif"}));
    //inner.append($("<p>").text("Navigate through our collection of linked websites!"));
    var links = $("<div>", {class: "webring-links"});
    links.append("[")
    links.append($("<a>", {href: response.previous_site_url, style: "margin: 0 10px;", target:"_top"}).text("Previous"));
    links.append("] [")
    links.append($("<a>", {href: response.next_site_url, style: "margin: 0 10px;", target:"_top"}).text("Next"));
    links.append("]");
    inner.append(links);
    inner.append($("<p>", {class: "copyright"}).text("©1991 Webringer"));

    base.append(inner);
    base.appendTo("#webring");
}


document.addEventListener('DOMContentLoaded', (event) => {
    var base_url = "http://localhost:8000/webring/?site="
    
    $.get(base_url.concat(window.site_name).concat("&ring=commerce"), function (data) {
        addWebring(data);
    });
});


