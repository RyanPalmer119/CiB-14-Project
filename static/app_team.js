function send_id_2_server(){
    let xhttp = new XMLHttpRequest();
    xhttp.open('POST', '/export_tests_to_excel', true);
    let data = {"id":"add_app_ID", "app_name":app_name};
    let dataJSON = JSON.stringify(data);
    xhttp.setRequestHeader('Content-type', 'application/json;charset=UTF-8');
    xhttp.send(dataJSON);
}



