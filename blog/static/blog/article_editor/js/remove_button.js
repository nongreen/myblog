function sendRemoveRequest(){
    let xhr = new XMLHttpRequest();
    xhr.open("POST", "https://reqbin.com/echo/post/json");

    xhr.onload = () => console.log(xhr.responseText);

    let data = `{
        "delete": "true"
    }`

    xhr.send()
}

var r = $('<input/>').attr({
                 type: "button",
                 id: "field",
                 onclick: "sendRemoveRequest()",
                 text: "delete article"
            });

$("body").append(r)
