/* VALIDATION */

function back(){
    window.history.back();
}

function validateGenes(){
    submitBtn = document.getElementById("submit")
    text = document.getElementById("genes").value;
    const regex = /([0-9]+)(\,[0-9]+)*$/
    if(regex.test(text)){
        document.getElementById('genes').style.border='';
        submitBtn.disabled = false;
    }else{
        document.getElementById('genes').style.border='1px solid red';
        submitBtn.disabled = true;
    }
}

function validatemRNAs(){
    submitBtn = document.getElementById("submit")
    text = document.getElementById("mrnas").value;
    const regex = /(mmu-[A-Za-z0-9_-]+)(\,(mmu-[A-Za-z0-9_-]+))*$/
    if(regex.test(text)){
        document.getElementById('mrnas').style.border='';
        submitBtn.disabled = false;
    }else{
        document.getElementById('mrnas').style.border='1px solid red';
        submitBtn.disabled = true;
    }
}

function checkDatabase(){
    checks = document.querySelectorAll('input[type="checkbox"]');
    submitBtn = document.getElementById("submit")

    let val = false;
    checks.forEach(element => {
        val = val || element.checked
    });

    if(val){
        document.getElementById('fieldDataset').style.borderColor='';
        submitBtn.disabled = false;
    }else{
        document.getElementById('fieldDataset').style.borderColor='red';
        submitBtn.disabled = true;
    }
}

function createAlert(message){
    let wrapper = document.createElement("div");
    wrapper.innerHTML = '<div class="alert alert-success alert-dismissible fade show mt-3" role="alert">'+
        '<button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>'+
        message+'</div>';
    return wrapper;
}

function save(){
    data['name'] = document.getElementById('fileName').value;
    
    const xhttp = new XMLHttpRequest();
    xhttp.onload = function() {
        if (this.readyState == 4 && this.status == 201) {
            console.log(this.response);
            let saveModal = document.getElementById('saveModal');
            bootstrap.Modal.getInstance(saveModal).toggle();

            let alertContainer = document.getElementById('alertContainer');
            let alert = createAlert("Search saved!");
            alertContainer.appendChild(alert);

            document.getElementById('fileName').value = '';
        }
    }
    xhttp.open("POST", "/api/search/", true);
    xhttp.setRequestHeader("Content-type", "application/json");
    xhttp.send(JSON.stringify(data));
}

function loadTable(query){
    
     confTable = {
        'pagination': {
          'limit': 10
        }
      }

    const colorDatabase = {
        'miRTarBase':'#5DADE2;',
        'TargetScan':'#C70039',
        'PicTar' :'#FFC300',
        'RNA22':'#82E0AA'
    }

    const xhttp = new XMLHttpRequest();
    xhttp.onload = function() {
        if (this.readyState == 4 && this.status == 200) {
            response = JSON.parse(this.response);

            data = []

            for(sourceId in response.data){
                row = [];
                row.push(sourceId);
                source = response.data[sourceId];
                response.target.forEach(el =>{
                    if(el in source){
                        let databases =[];
                        for(database in response.data[sourceId][el]){
                            databases.push(database)
                        }
                        let value = '<div class="mainCell" style="height:20px">';
                        databases.forEach(database=>{
                            value = value + `<div class="databaseCell" style="background-color:${colorDatabase[database]};"></div>`

                        })
                        value = value + '</div>'
                        row.push(gridjs.html(value));
                    }else{
                        row.push('');
                    }
                })
                data.push(row);
            }            

            confTable.columns = [...['Gene ID'],...response.target];
            confTable.data = data;

            new gridjs.Grid(confTable).render(document.getElementById("wrapper"));
        }
    }
    xhttp.open("POST", "/api/search/table", true);
    xhttp.setRequestHeader("Content-type", "application/json");
    xhttp.send(JSON.stringify(query));
}