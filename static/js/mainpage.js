var currentValue = '';
var file_merge_list = [];


function setDefaults(event) {
    'use strict';
    var image_frame = document.getElementById('image_frame');
    var displayImg = document.createElement('img');
    if (file_name_array[0] != null) {
        currentValue = file_name_array[0];
        displayImg.setAttribute("src", "/static/images/" + currentValue + ".png");
        displayImg.setAttribute("width", "480px");
        displayImg.setAttribute("height", "640px");
        image_frame.appendChild(displayImg);
    } else {
        displayImg.setAttribute("src", "https://s3.amazonaws.com/PandaExpressWebsite/Responsive/img/fundraiser-flyer/flyer-watermark.png");
        displayImg.setAttribute("width", "480px");
        displayImg.setAttribute("height", "640px");
        image_frame.appendChild(displayImg);
    }
}


var scanner_field = document.getElementById('scanner_name');
scanner_field.innerHTML = "<b>Current device:</b> " + scanner_name[0];

function startscan() {
    'use strict';
    location.href = '/scan';
}

var list_of_files = document.getElementById('list_of_files');

for (var i = 0; i < file_list.length; i++) {
    var breakLine = document.createElement("br");
    var li = document.createElement("li");
    var input = document.createElement("input");
    input.setAttribute("type", "text");
    input.setAttribute("value", file_list[i]);
    input.setAttribute("id", file_list[i]);
    input.setAttribute("class", "boxes");
    input.setAttribute("onchange", "rename(event)");
    input.setAttribute("onfocus", "getCurrentValue(event, document.getElementById(event.target.id).value)");
	input.setAttribute("ondblclick", "mergeDocuments(event, document.getElementById(event.target.id).value)")
    input.setAttribute("size", "25");
    li.appendChild(input);
    list_of_files.appendChild(li);
    list_of_files.appendChild(breakLine);
}

function mergeDocuments(event, elem) {
	var flag = 0;
	function contains(element) {
		for (var c = 0; c < file_merge_list.length; c++ ) {
			if (element === file_merge_list[c]) {
				flag = 1;
			}
		}
		if (flag === 1) {
			return "found"
		}
		else {
			return "not found"
		}
	}
	
	if (contains(elem) === "not found") {
		var input_box = document.getElementById(elem);
		input_box.style.backgroundColor = "green";
		file_merge_list.push(elem);
	}
	
	else if (contains(elem) === "found") {
		var indexof = file_merge_list.indexOf(elem)
		if (indexof > -1) {
			file_merge_list.splice(indexof, 1);
		}
		var input_box = document.getElementById(elem);
		input_box.style.backgroundColor = "transparent";
	}
}

var image_frame = document.getElementById('image_frame');

function getCurrentValue(event, currValue) {
    while (image_frame.firstChild) {
        image_frame.removeChild(image_frame.firstChild);
    }
    currentValue = currValue;
    var displayImg = document.createElement('img');
    displayImg.setAttribute("src", "/static/images/" + currentValue + ".png");
    displayImg.setAttribute("width", "480px");
    displayImg.setAttribute("height", "640px");
    image_frame.appendChild(displayImg);
    console.log(currentValue);
}

var sendFileName = document.getElementById('sendFileName');

function rename() {

    var changed_input = document.getElementById(event.target.id).value;
    console.log(changed_input)
    var hidden_tag = document.createElement('input');
    hidden_tag.setAttribute("type", "hidden");
    hidden_tag.setAttribute("name", "renamed");
    hidden_tag.setAttribute("id", "renamed");
    hidden_tag.setAttribute("value", changed_input);
    hidden_tag.setAttribute("form", "sendFileName");
    var cell_2_2 = document.getElementById('cell_2_2');
    cell_2_2.appendChild(hidden_tag);

    var hidden_tag_orginal = document.createElement('input');
    hidden_tag_orginal.setAttribute("type", "hidden");
    hidden_tag_orginal.setAttribute("name", "original");
    hidden_tag_orginal.setAttribute("id", "original");
    hidden_tag_orginal.setAttribute("value", currentValue);
    hidden_tag_orginal.setAttribute("form", "sendFileName");
    cell_2_2 = document.getElementById('cell_2_2');
    cell_2_2.appendChild(hidden_tag_orginal);
    sendFileName.submit();
}


function rotateImage(event) {

    var button_frame = document.getElementById('button_frame');

    if (button_frame.childNodes[8]) {
        button_frame.removeChild(button_frame.childNodes[8]);
    }
    if (button_frame.childNodes[7]) {
        button_frame.removeChild(button_frame.childNodes[7]);
    }

    var rotateValue = document.getElementById("rotateValue");
    var rotateFormElement = document.createElement("input");
    rotateFormElement.setAttribute("type", "hidden");
    rotateFormElement.setAttribute("name", "angle");
    rotateFormElement.setAttribute("id", "angle");
    rotateFormElement.setAttribute("form", "rotateValue");
    if (event.target.id === "left") {
        rotateFormElement.setAttribute("value", "90");
    } else {
        rotateFormElement.setAttribute("value", "-90");
    }
    button_frame.appendChild(rotateFormElement);

    var fileName = document.createElement("input");
    fileName.setAttribute("type", "hidden");
    fileName.setAttribute("name", "fileName");
    fileName.setAttribute("id", "fileName");
    fileName.setAttribute("form", "rotateValue");
    fileName.setAttribute("value", currentValue);
    button_frame.appendChild(fileName);
    rotateValue.submit();
}

function mergeFiles(event) {
	var container =  document.getElementById("textBox");
	var hiddenInput = document.createElement("input");
	hiddenInput.setAttribute("type","hidden");
	hiddenInput.setAttribute("name","mergeFileList");
	hiddenInput.setAttribute("id","mergeFileList");
	hiddenInput.setAttribute("value", file_merge_list.toString());
	hiddenInput.setAttribute("form","mergeFiles");
	container.appendChild(hiddenInput);
	var form = document.getElementById("mergeFiles");
	form.submit();
}



