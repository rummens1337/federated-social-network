function register_server() {
  $("form[name='registerdataserver']").validate({
    rules: {
      server_name: "required",
      server_address: {
        "required": true,
        startsWithHTTP: true,
        endsWithSlash: true
      }
    },

    submitHandler: function(form) {
      function registerCentral() {
        serverForm = {name:form.server_name.value, address:form.server_address.value};
        requestJSON("POST", "/api/server/register", serverForm, registerCentralSucces, registerCentralFailed);
      }

      function registerCentralSucces() {
        toggle_modal("registerServer");
        alertError("Your server has been successfully registered!", 2000);
        $("#btnSubmitServer").attr("disabled", true);
      }

      function registerCentralFailed(response) {
        alertError(response.reason, 2000, "registerServer");
      }
      registerCentral();
    }
  });
}

$(document).ready(function() {
  jQuery.validator.addMethod("startsWithHTTP", function(value, element) {
    return value.startsWith('http://');
  }, "Server address should start with http://");

  jQuery.validator.addMethod("endsWithSlash", function(value, element) {
    return !value.endsWith('/');
  }, "Server address may not end with /");
});
