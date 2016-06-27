var select = document.getElementById("select_panel");
var select_form = document.getElementById('selectForm');

for (var i = 0; i < list_of_scanners.length; i++) {
    var option = document.createElement("option");
    option.innerHTML = list_of_scanners[i];
    select.appendChild(option);
}

function submitQuery() {
    select_form.submit();
}