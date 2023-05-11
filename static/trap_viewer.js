window.addEventListener("load", (e) => {
    viewTRAP()
})

function viewTRAP(){
    var app_name = document.getElementById("app_name").value
    let xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if(xhttp.status === 200 ) {
            let trapResponse = JSON.parse(xhttp.response)
            fillTrapTable(trapResponse)
        }
    }    
    xhttp.open('GET', `/return_TRAP/${app_name}`, false);
    xhttp.send();
  
}

function fillTrapTable(trapObj) {
    let cells_to_fill = document.getElementsByClassName('trap_details')
    console.log(cells_to_fill.length)
    let data = trapObj['3']
    let objectLength = Object.keys(data).length
    for(let i = objectLength-1; i >=0 ; i--) {
      cells_to_fill[i].innerText = Object.values(data)[i]
      cells_to_fill[i].setAttribute("contenteditable", "true");
      console.log(Object.values(data)[i])
    }
}

let export_btn = document.getElementById("export_trap")
export_btn.addEventListener("click", function() {
  console.log(window.location.href)
})

function getTableCells(table){
    let tableBody = document.getElementById(table)
    let rowArray = []
    for(let i = 0; i < tableBody.rows.length; i++){
        let row = tableBody.rows[i]
        let rowData = []
        for(let j = 0; j < row.childNodes.length; j ++){
            if(row.childNodes[j].innerText){
                rowData.push(row.childNodes[j].innerText)
            }
        }
        rowArray.push(rowData)
    }
    return rowArray
}

function export_trap() {
  console.log(getTableCells("tbody_trap_table"))
  var app_name = document.getElementById("app_name").value
  let xhttp = new XMLHttpRequest();
  xhttp.open('POST', '/export_TRAP', true);
  let data = {"data":getTableCells("tbody_trap_table"), "app_name":app_name};
  let dataJSON = JSON.stringify(data);
  xhttp.setRequestHeader('Content-type', 'application/json;charset=UTF-8');
  xhttp.send(dataJSON);
}
