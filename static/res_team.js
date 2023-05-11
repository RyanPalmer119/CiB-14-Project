function open_details(app) {
    window.location.assign(`/res/details/${app}`)
}

function open_report(id, name) {
    alert(`File Downloaded: app_documents/${name}/test_report.csv`)
    let xhttp = new XMLHttpRequest();
    xhttp.open('POST', '/export_tests_to_excel', true);
    let data = {"id": id, "app_name": name};
    let dataJSON = JSON.stringify(data);
    console.log(data)
    xhttp.setRequestHeader('Content-type', 'application/json;charset=UTF-8');
    xhttp.send(dataJSON);
} 
