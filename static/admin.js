function action(method, url) {
    var xhr = new XMLHttpRequest();
    xhr.open(method, url, false);
    xhr.send();
    return {
        "status": xhr.status,
        "text": xhr.responseText
    }
}

function schema() {
    console.log(action("POST", "/db/create_schema"))
}

function test() {
    console.log(action("GET", "/db/test"))
}

function resetDB() {
    console.log(action("GET", "/db/reset"))
}