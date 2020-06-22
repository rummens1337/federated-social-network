var centralServer = window.location.origin;

// Hobby functions

// Call this function when requesting an array of hobbies
function showHobbies(req) {
    if (req.data.hobbies.length > 0) {
      for (i=0; i < req.data.hobbies.length; i++) {
          var hobby = req.data.hobbies[i];
          showHobby(hobby);
      }
    }
    else {
      $('#hobbies-list').append('<p>No hobbies added yet...</p>');
    }
}

function deleteHobby() {
    $("form[name='hobby']").validate({
        rules: {
            id: 'required'
        },

        submitHandler: function(form) {
            var data = new FormData(form)

            requestJSONFile('POST', dataServer + '/api/user/deleteHobby', data, editSucces, editFailed);
        }
    });
};

// This function adds a hobby in the div 'hobbies'
function showHobby(hobby) {
    var content =
    '<form enctype="multipart/form-data" name="hobby">' +
        '<p>' + hobby.title + '</p>' +
        '<input type="hidden" id="id" name="id">' +
        '<button type="submit" class="btn-danger" onclick="deleteHobby()">Delete</button>' +
    '</form>'
    $('#hobbies-list').append(content);

    document.getElementById('id').value = hobby.id;
}

function addHobby() {
    $("form[name='hobby']").validate({
        rules: {
            title: 'required'
        },

        submitHandler: function(form) {
            var data = new FormData(form)

            requestJSONFile('POST', dataServer + '/api/user/addHobby', data, editSucces, editFailed);
        }
    });
};



// Skills functions

// Call this function when requesting an array of skills
function showSkills(req) {
    // if (req.data.skills.length > 0) {
    if (0 == 1) {
      for (i=0; i < req.data.skills.length; i++) {
          var skill = req.data.skills[i];
          showSkill(skill);
      }
    }
    else {
      $('#skills-list').append('<p>No skills added yet...</p>');
    }
}

// This function adds a skill in the div 'skills'
function showSkill(skill) {
    var content = '<p>' + skill.title + '</p>' +
        '<p>' +
        '<button type="button" class="btn-danger" onclick="deleteSkill">Delete</button>' +
        '</p>'
    $('#skill-list').append(content);
}

function addSkill() {
    $("form[name='skill']").validate({
        rules: {
            new_skill: 'required',
            new_level: 'required'
        },

        submitHandler: function(form) {
            var data = new FormData(form)

            requestJSONFile('POST', dataServer + '/api/user/edit', data, editSucces, editFailed);
        }
    });
};

// Language functions

// Call this function when requesting an array of languages
function showLanguages(req) {
    // if (req.data.languages.length > 0) {
    if (0 == 1) {
      for (i=0; i < req.data.languages.length; i++) {
          var languages = req.data.languages[i];
          showLanguage(languages);
      }
    }
    else {
      $('#languages-list').append('<p>No languages added yet...</p>');
    }
}

// This function adds a language in the div 'languages'
function showLanguage(language) {
    var content = '<p>' + language.title + '</p>' +
        '<p>' +
        '<button type="button" class="btn-danger" onclick="deleteSkill">Delete</button>' +
        '</p>'
    $('#languages-list').append(content);
}


function addLanguage() {
    $("form[name='language']").validate({
        rules: {
            new_skill: 'required',
            new_level: 'required'
        },

        submitHandler: function(form) {
            var data = new FormData(form)

            requestJSONFile('POST', dataServer + '/api/user/edit', data, editSucces, editFailed);
        }
    });
};

// Main functions
function editSucces() {
    window.location.reload();
}

function editFailed(response) {
    alertError(response.reason, 2000);
}

function setDataAddress(req) {
    dataServer = req.data.address;
    requestJSON('GET', dataServer + '/api/user/hobby', null, showHobbies, function(req) {
        alertError(req.reason, 2000);
    });
    requestJSON('GET', dataServer + '/api/user/skill', null, showSkills, function(req) {
        alertError(req.reason, 2000);
    });
    requestJSON('GET', dataServer + '/api/user/language', null, showLanguages, function(req) {
        alertError(req.reason, 2000);
    });
}

$(document).ready(function() {
    requestJSON('GET', centralServer + '/api/user/address', null, setDataAddress, function(req) {
        alertError(req.reason, 2000);
    });
});