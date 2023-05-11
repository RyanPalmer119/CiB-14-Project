var logout_btn = document.getElementById("logout")

if (logout_btn != null) {
    logout_btn.addEventListener("click", (e) => {
        document.cookie = "token= ; path=/; expires = Thu, 01 Jan 1970 00:00:00 GMT"
        document.cookie = "userID= ; path=/; expires = Thu, 01 Jan 1970 00:00:00 GMT"
        window.location.assign("/")
    })    
}

function getCookie(cname) {
  let name = cname + "=";
  let decodedCookie = decodeURIComponent(document.cookie);
  let ca = decodedCookie.split(';');
  for(let i = 0; i <ca.length; i++) {
    let c = ca[i];
    while (c.charAt(0) == ' ') {
      c = c.substring(1);
    }
    if (c.indexOf(name) == 0) {
      return c.substring(name.length, c.length);
    }
  }
  return "";
}


function show_notifs() {
    document.getElementById("notif-body").replaceChildren()
    var user_id = getCookie("userID")
    var xhr = new XMLHttpRequest();
    xhr.open('GET', `/notifs/${user_id}`, false);
        xhr.send();
        if (xhr.status === 200) {
            res = JSON.parse(xhr.responseText)
            for (var item of res) {
                var row = document.createElement("tr"); // Create the table row
                row.innerHTML = `<td>${item[0]} <span class='badge bg-secondary'>${item[1]}</span></td><td>${item[2]}</td>`
                console.log(typeof row)
                document.getElementById("notif-body").appendChild(row)
            }
            
        } else {
            alert(xhr.responseText)
        }
}


//var export_BTN = document.getElementByID()
