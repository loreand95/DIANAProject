function createAlert(message){
    let wrapper = document.createElement("div");
    wrapper.innerHTML = '<div class="alert alert-success alert-dismissible fade show mt-3" role="alert">'+
        '<button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>'+
        message+'</div>';
    return wrapper;
}

function back(){
    window.history.back();
}
