
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

document.getElementById("signin_btn").addEventListener("click", (e) => {
    var username = document.getElementById("username").value // Get Username
    var password = document.getElementById("password").value // Get Password
    
    hash(password).then(hex_passhash => { // Hash Password
        var data = {
            "username": username,
            "passhash": hex_passhash
        }
        var xhr = new XMLHttpRequest();
        xhr.open('POST', `/api/login`, false);
        xhr.send(JSON.stringify(data));
        console.log(xhr.responseText)
        if (xhr.status === 200) {
            hash(`${username}${hex_passhash}`).then(token => {
                document.cookie = `token=${token}; path=/`
                document.cookie = `userID=${xhr.responseText}; path=/`
            })   
            window.location.assign("/app")
        } else {
            alert(xhr.responseText)
        }
    })
    

})