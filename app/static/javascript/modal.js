
function toggle_modal(modal_id) {
    if (document.body.contains(document.getElementById(modal_id))) {
        $(function () {
            $('#' + modal_id).modal('toggle');
        });
    }
    else {
        alert("no");
    }
}