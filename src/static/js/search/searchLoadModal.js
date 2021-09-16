document.getElementById("loadModal").addEventListener("show.bs.modal",showModalSavedSearch);

function showModalSavedSearch(event){
    //Retrieve saved search
    getAllSearchAPI().then((response)=>{
      console.log(response)
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
        if(searches[search].target){
          cellTarget.innerHTML = searches[search].target;
        }else{
          cellTarget.innerHTML = 'ND';
        }
        

        let cellDatabase = row.insertCell(3);
        if (searches[search].databases.length == 4)
          cellDatabase.innerHTML = "ALL";
        else {
          cellDatabase.innerHTML = searches[search].databases;
        }

        let actionCell = row.insertCell(4);

        actionCell.innerHTML = 
        `<div style="display:flex">
          <button type="button" class="btn btn-primary btn-sm" aria-label="Load" id="${search}"">Load</button>
          <button style="margin-left:15px" type="button" class="btn btn-danger btn-sm" aria-label="Delete" id="${search}"">Remove</button>
        </div>`;

        const loadButton = actionCell.firstChild.children[0];
        loadButton.addEventListener('click', (event)=>{
          fillForm(searches[event.target.id])
        });

        const removeButton = actionCell.firstChild.children[1];
        removeButton.addEventListener('click', (event)=>{
          removeSavedSearch(searches[event.target.id])
        });
      }
    });
}

function removeSavedSearch(search){
  console.log('renoved '+search.id)
  deleteSearchAPI(search.id);
  showModalSavedSearch();
}