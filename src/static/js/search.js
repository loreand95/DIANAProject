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


function data2row(response){
    data = []

    const colorDatabase = {
        'miRTarBase':'#5DADE2;',
        'TargetScan':'#C70039',
        'PicTar' :'#FFC300',
        'RNA22':'#82E0AA'
    }

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
    return data;
}

function loadTable(query){

    confTable = {
        'pagination': {
          'limit': 10
        },
        data : ()=>{
            return searchAPI(query).then((response)=>{
                return data2row({data:response, target:query.source})})
        },
        'columns':[...['ID'],...query.source]
    }

    new gridjs.Grid(confTable).render(document.getElementById("wrapper"));
}