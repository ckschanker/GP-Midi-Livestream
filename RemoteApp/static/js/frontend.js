"use strict";
var network_address = "http://192.168.110.124:5000/";
var switch_mode = 0;

// HyperDeck control elements on the HTML page
var input_1     = document.getElementById("input_1");
var input_2     = document.getElementById("input_2");
var input_3     = document.getElementById("input_3");
var input_4     = document.getElementById("input_4");
var input_5     = document.getElementById("input_5");
var input_6     = document.getElementById("input_6");
var input_7     = document.getElementById("input_7");
var input_8     = document.getElementById("input_8");
var input_9     = document.getElementById("input_9");
var input_10    = document.getElementById("input_10");
var input_11    = document.getElementById("input_11");
var input_12    = document.getElementById("input_12");

function send_mess(button_num) {
    var isChecked=document.getElementById("transType").checked;

    var xhr = new XMLHttpRequest();
    xhr.open("POST", network_address, true);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.send(JSON.stringify({
        button: button_num,
        mode: isChecked
    }));
}

// Bind HTML elements to actions commands
input_1.onclick = function() {
    console.log("Button 1 Clicked!");
    send_mess('05');
    
};

input_2.onclick = function() {
    console.log("Button 2 Clicked!");
    send_mess('08');
};

input_3.onclick = function() {
    console.log("Button 3 Clicked!");
    send_mess('0e');
};

input_4.onclick = function() {
    console.log("Button 4 Clicked!");
    send_mess('0b');
};

input_5.onclick = function() {
    console.log("Button 5 Clicked!");
    send_mess('0c');
};

input_6.onclick = function() {
    console.log("Button 6 Clicked!");
    send_mess('0d');
};

input_7.onclick = function() {
    console.log("Button 7 Clicked!");
    send_mess('02');
};

input_8.onclick = function() {
    console.log("Button 8 Clicked!");
    send_mess('01');
};

input_9.onclick = function() {
    console.log("Button 9 Clicked!");
    send_mess('04');
};

input_10.onclick = function() {
    console.log("Button 10 Clicked!");
    send_mess('03');
};

input_11.onclick = function() {
    console.log("Button 11 Clicked!");
    send_mess('07');
};

input_12.onclick = function() {
    console.log("Button 12 Clicked!");
    send_mess('00');
};