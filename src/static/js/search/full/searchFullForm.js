document.getElementById("searchMenuLink").classList.add("active");
document.getElementById("fullSearchLink").classList.add("active");

function fillForm(search) {
  //Close modal
  let loadModal = document.getElementById("loadModal");
  bootstrap.Modal.getInstance(loadModal).toggle();

  // Fill form

  /* SOURCE & TARGET */
  
  if(search.isGeneTarget){
    document.getElementById("mrnas").value = search.source;
    document.getElementById("genes").value = search.target;
  }else{
    document.getElementById("mrnas").value = search.target;
    document.getElementById("genes").value = search.source;
  }

  /* IS GENE TARGET */

  if (search.isGeneTarget) {
    document.getElementById("geneTarget").checked = true;
  } else {
    document.getElementById("geneTarget").checked = false;
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

/* VALIDATION */
function validateGenes() {
  submitBtn = document.getElementById("submit");
  text = document.getElementById("genes").value;

  const regex = /([0-9]+)(\,[0-9]+)*$/;
  if (regex.test(text) || text === "") {
    document.getElementById("genes").style.border = "";
    submitBtn.disabled = false;
    return true;
  } else {
    document.getElementById("genes").style.border = "1px solid red";
    submitBtn.disabled = true;
    return false;
  }
}

function validatemRNAs() {
  submitBtn = document.getElementById("submit");
  text = document.getElementById("mrnas").value;

  const regex = /(mmu-[A-Za-z0-9_-]+)(\,(mmu-[A-Za-z0-9_-]+)?)*$/;
  if (regex.test(text) || text === "") {
    document.getElementById("mrnas").style.border = "";
    submitBtn.disabled = false;

    return true;
  } else {
    document.getElementById("mrnas").style.border = "1px solid red";
    submitBtn.disabled = true;

    return false;
  }
}

function checkDatabase() {
  checks = document.querySelectorAll('input[type="checkbox"]');
  submitBtn = document.getElementById("submit");

  let val = false;
  checks.forEach((element) => {
    val = val || element.checked;
  });

  if (val) {
    document.getElementById("fieldDataset").style.borderColor = "";
    submitBtn.disabled = false;
  } else {
    document.getElementById("fieldDataset").style.borderColor = "red";
    submitBtn.disabled = true;
  }
}

function validateSource() {
  const sourceId =
    document.getElementById("swapRow").children[0].children[0].children[0].id;

  const inputSource = document.getElementById(sourceId);

  if (inputSource.value === "") {
    inputSource.style.border = "1px solid red";
    document.getElementById("submit").disabled = true;

    return false;
  }

  return true;
}

function swapField() {
  let row = document.getElementById("swapRow");

  //Swap div
  row.appendChild(row.children[0]);
  row.prepend(row.children[1]);

  // Switch target
  document.getElementById("geneTarget").checked = !document.getElementById("geneTarget").checked;
}

function submitForm() {
  const isValid = validateSource() && validateGenes() && validatemRNAs();

  if (isValid) {
    const sourceId =
      document.getElementById("swapRow").children[0].children[0].children[0].id;

    const form = document.getElementsByClassName("form");

    const input = document.createElement("input");
    input.setAttribute("name", sourceType);
    input.setAttribute("value", sourceId);

    form.appendChild(input);

    return true;
  }
  return false;
}
