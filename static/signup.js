
function hash(string) {
  const utf8 = new TextEncoder().encode(string);
  return crypto.subtle.digest('SHA-256', utf8).then((hashBuffer) => {
    const hashArray = Array.from(new Uint8Array(hashBuffer));
    const hashHex = hashArray
      .map((bytes) => bytes.toString(16).padStart(2, '0'))
      .join('');
    return hashHex;
  });
}

document.getElementById("signup_btn").addEventListener("click", (e) => {
    var username = document.getElementById("username").value // Get Username
    var password = document.getElementById("password").value // Get Password
    var role = document.getElementById("team-select").value // Get Password
    if (role === "error") {
        alert("Please select a Role Group")
        return;
    } 
    if (password.length <= 0) {
        alert("Please input a Password")
        return;
    }
    
    hash(password).then(hex_passhash => { // Hash Password
        var data = {
            "username": username,
            "passhash": hex_passhash,
            "role": role
        }
        var xhr = new XMLHttpRequest();
        xhr.open('POST', `/api/new_user`, false);
        xhr.send(JSON.stringify(data));
        if (xhr.status === 200) {
            hash(`${username}${hex_passhash}`).then(token => {
                document.cookie = `token=${token}; path=/`
                document.cookie = `userID=${xhr.responseText}; path=/`
            })   
            window.location.assign("/app")
        } else {
            alert(`${xhr.responseText}`)
        }
    })
    

})