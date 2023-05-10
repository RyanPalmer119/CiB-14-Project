var logout_btn = document.getElementById("logout")

if (logout_btn != null) {
    logout_btn.addEventListener("click", (e) => {
        document.cookie = "token= ; path=/; expires = Thu, 01 Jan 1970 00:00:00 GMT"
        document.cookie = "userID= ; path=/; expires = Thu, 01 Jan 1970 00:00:00 GMT"
        window.location.assign("/")
    })    
}

var export_BTN = document.getElementByID()
