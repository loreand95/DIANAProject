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
