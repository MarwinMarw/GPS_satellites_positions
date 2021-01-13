var add_sat;

function ajaxRINEXget(){
    console.log("AJAX")
    $.ajax({
        url: '/get_data',
        method: 'get',
        dataType: 'json',
        cache: false,
        success: processResult,
        error: showError
    });
}

function processResult(results){
    Object.entries(results).forEach(element => {
        console.log(element);
        add_sat(element[0], element[1])
    });  
}

function showError(results){
    console.log('ERROR')
    console.log(results)
}