document.getElementById("searchMenuLink").classList.add('active');
document.getElementById("baseSearchLink").classList.add('active');
document.getElementById("loadModal").addEventListener("show.bs.modal",showModalSavedSearch);

function showModalSavedSearch(event){
    const xhttp = new XMLHttpRequest();

    getAllSearchAPI().then((response)=>{
      searches = response;
      //Create Table
      let table = document
        .getElementById("loadTable")
        .getElementsByTagName("tbody")[0];

      table.innerHTML = ""; //Clear table

      //Populate Table
      for (search in searches) {
        let row = table.insertRow();
        let cellName = row.insertCell();
        cellName.innerHTML = searches[search].name;

        let cellSource = row.insertCell(1);
        cellSource.innerHTML = searches[search].source;

        let cellTarget = row.insertCell(2);
        if(searches[search].isGeneTarget){
          cellTarget.innerHTML = 'Gene';
        }else{
          cellTarget.innerHTML = 'mRNAs';
        }
        

        let cellDatabase = row.insertCell(3);
        if (searches[search].databases.length == 4)
          cellDatabase.innerHTML = "ALL";
        else {
          cellDatabase.innerHTML = searches[search].databases;
        }

        let actionCell = row.insertCell(4);

        actionCell.innerHTML = `<button type="button" class="btn btn-primary btn-sm" aria-label="Load" id="${search}"">Load</button>`;
        const button = actionCell.children[0];
        button.addEventListener('click', (event)=>{
          fillSavedSearch(searches[event.target.id])
        });
      }
    });
}

function fillSavedSearch(search) {

  //Close modal
  let loadModal = document.getElementById("loadModal");
  bootstrap.Modal.getInstance(loadModal).toggle();

  // Fill form

  /* SOURCE */
  document.getElementById("source").value = search.source;

  /* TARGET */
  const labelSource = document.getElementById("labelSource");
  if (search.isGeneTarget) {
    labelSource.innerHTML = 'mRNAs';
    document.getElementById("geneTarget").checked = true;
  } else {
    labelSource.innerHTML = 'Genes';
    document.getElementById("mrnaTarget").checked = true;
  }

  /* DATABASE */ 
  // Unchecked all input
  document.querySelectorAll("#datasetForm input").forEach((checkbox) => {
    checkbox.checked = false;
  });
  // Check database
  search.databases.forEach((database) => {
    let checkbox = document.getElementById(database.toLowerCase());
    checkbox.checked = search.databases.includes(database);
  });
}

function switchSource(){

    const labelSource = document.getElementById('labelSource');
    const titleSearch = document.getElementById('titleSearch');

    const genesTarget = document.getElementById('geneTarget');
    const mrnasTarget = document.getElementById('mrnaTarget');

    if(genesTarget.checked){
        mrnasTarget.checked = !mrnasTarget.checked;
        labelSource.innerHTML = 'Genes';
        titleSearch.innerHTML = 'Search mRNAs from genes';
    }else{
        genesTarget.checked = !genesTarget.checked;
        labelSource.innerHTML = 'mRNAs ';
        titleSearch.innerHTML = 'Search genes from mRNAs';
    }

    const sourceText = document.getElementById("source").value;
    if(sourceText!==''){
        validateSource()
    }
}

// VALIDATION

function validateSource(){
    const isGeneTarget = document.getElementById('geneTarget').checked;

    if(isGeneTarget){
        return validatemRNAs();
    }else{
        return validateGenes();
    }
}

function validatemRNAs(){
  submitBtn = document.getElementById("submit")
  text = document.getElementById("source").value;
  const regex = /(mmu-[A-Za-z0-9_-]+)(\,(mmu-[A-Za-z0-9_-]+))*$/
  if(regex.test(text)){
      document.getElementById('source').style.border='';
      submitBtn.disabled = false;
      return true;
  }else{
      document.getElementById('source').style.border='1px solid red';
      submitBtn.disabled = true;
      return false;
  }
}

function validateGenes(){
    submitBtn = document.getElementById("submit")
    text = document.getElementById("source").value;
    const regex = /([0-9]+)(\,[0-9]+)*$/
    if(regex.test(text)){
        document.getElementById('source').style.border='';
        submitBtn.disabled = false;
        return true;
    }else{
        document.getElementById('source').style.border='1px solid red';
        submitBtn.disabled = true;
        return false;
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