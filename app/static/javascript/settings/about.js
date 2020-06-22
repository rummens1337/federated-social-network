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


// This function adds a hobby in the div 'hobbies'
function showHobby(hobby) {
    var content =
    '<form enctype="multipart/form-data" name="hobby">' +
        '<p>' + hobby.title + '</p>' +
        '<button type="submit" class="btn-danger" onclick="deleteHobby(' + hobby.id+ ')">Delete</button>' +
    '</form>'
    $('#hobbies-list').append(content);
}

function deleteHobby(id) {
    var data = {'id' : id}
    requestJSON('POST', dataServer + '/api/user/deleteHobby', data, editSucces, editFailed);
};

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
    if (req.data.skills.length > 0) {
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
    var content =
    '<form enctype="multipart/form-data" name="editSkill">' +
    '<p>' + skill.title + '</p>' +
    '<input name="id" type="hidden" value="' + skill.id + '">' +
    '<p><input name="skill_level" input type="range" min="1" max="100" value="' + skill.skill_level + '" ></p>' +
    '<button name="slider" type="submit" class="btn-danger" onclick="deleteSkill(' + skill.id + ')">Delete</button>' +
    ' <button type="submit" class="btn-primary" onclick="updateSkill()">Update</button>' +
    '</form>'
    $('#skills-list').append(content);
}

function addSkill() {
    $("form[name='skill']").validate({
        rules: {
            title: 'required',
            skill_level: 'required'
        },

        submitHandler: function(form) {
            var data = new FormData(form)

            requestJSONFile('POST', dataServer + '/api/user/addSkill', data, editSucces, editFailed);
        }
    });
};

function updateSkill() {
    $("form[name='editSkill']").validate({
        rules: {
            skill_level: 'required',
            id: 'required'
        },

        submitHandler: function(form) {
            var data = new FormData(form)

            requestJSONFile('POST', dataServer + '/api/user/editSkill', data, editSucces, editFailed);
        }
    });
};

function deleteSkill(id) {
    var data = {'id' : id}
    requestJSON('POST', dataServer + '/api/user/deleteSkill', data, editSucces, editFailed);
};

// Language functions

// Call this function when requesting an array of languages
function showLanguages(req) {
    if (req.data.languages.length > 0) {
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
    var content =
    '<form enctype="multipart/form-data" name="editLanguage">' +
    '<p>' + language.title + '</p>' +
    '<input name="id" type="hidden" value="' + language.id + '">' +
    '<p><input name="skill_level" type="range" min="1" max="100" value="' + language.skill_level + '" ></p>' +
    '<button type="submit" class="btn-danger" onclick="deleteLanguage(' + language.id + ')">Delete</button>' +
    ' <button type="submit" class="btn-primary" onclick="updateLanguage()">Update</button>' +
    '</form>'
    $('#languages-list').append(content);
}


function addLanguage() {
    $("form[name='language']").validate({
        rules: {
            title: 'required',
            skill_level: 'required'
        },

        submitHandler: function(form) {
            var data = new FormData(form)

            requestJSONFile('POST', dataServer + '/api/user/addLanguage', data, editSucces, editFailed);
        }
    });
};

function deleteLanguage(id) {
    var data = {'id' : id}
    requestJSON('POST', dataServer + '/api/user/deleteLanguage', data, editSucces, editFailed);
};

function updateLanguage() {
    $("form[name='editLanguage']").validate({
        rules: {
            skill_level: 'required',
            id: 'required'
        },

        submitHandler: function(form) {
            var data = new FormData(form)

            requestJSONFile('POST', dataServer + '/api/user/editLanguage', data, editSucces, editFailed);
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