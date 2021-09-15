function save(){
    //Add name
    query['name'] = document.getElementById('fileName').value;
    
    saveSearchAPI(query).then((response)=>{

            let saveModal = document.getElementById('saveModal');
            bootstrap.Modal.getInstance(saveModal).toggle();

            let alertContainer = document.getElementById('alertContainer');
            let alert = createAlert("Search saved!");
            alertContainer.appendChild(alert);

            document.getElementById('fileName').value = '';
    });
}