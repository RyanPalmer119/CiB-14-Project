function viewTRAP(){
    let xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if(xhttp.status === 200 ) {
            let trapResponse = JSON.parse(xhttp.response)
            let actualReponse = trapResponse['2']
            fillTrapTable(actualReponse)
        }
    }    
    xhttp.open('GET', '/return_TRAP', true);
    xhttp.send();
  
}

function fillTrapTable(trapObj) {
    let cells_to_fill = document.getElementsByClass('trap_details')
    let objectLength = Object.keys(trapObj).length
    let trapTable = document.getElementById('TrapEditorTable')
    for(let i = objectLength-1; i >=0 ; i--) {
        let row = trapTable.insertRow(0);
        let cell0 = row.insertCell(0);
        let cell1 = row.insertCell(1);
        cell1.contentEditable = "true"
        cell0.innerText = Object.keys(trapObj)[i]
        cell1.innerText = Object.values(trapObj)[i]
}

  
