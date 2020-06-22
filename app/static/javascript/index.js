function setUserSettings(req) {
    document.getElementById('image_url').src = req.data.image_url;
    document.getElementById('location').innerHTML = req.data.location;
    document.getElementById('name').innerHTML = req.data.firstname + ' ' + req.data.lastname;
    document.getElementById('study').innerHTML = req.data.study;
    document.getElementById('status').innerHTML = req.data.relationship_status;
    document.getElementById('number').innerHTML = req.data.phone_number;
}

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
    '<p>' + skill.title + '</p>' +
    '<div class="w3-light-grey w3-round-xlarge w3-small" style="color:#52B77C;">' +
        '<div class="w3-container w3-center w3-round-xlarge w3-teal" style="width:' + skill.skill_level + '%">' + skill.skill_level + '%</div>' +
    '</div>'
    $('#skills-list').append(content);
}

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
    '<p>' + language.title + '</p>' +
    '<div class="w3-light-grey w3-round-xlarge">' +
        '<div class="w3-round-xlarge w3-teal" style="height:24px;width:' + language.skill_level + '%"></div>' +
    '</div>'
    $('#languages-list').append(content);
}

function setDataAddress(req) {
    dataServer = req.data.address;
    requestJSON('GET', dataServer + '/api/user', null, setUserSettings, function(req) {
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
    requestJSON('GET', '/api/user/address', null, setDataAddress, function(req) {
        alertError(req.reason, 2000);
      });
});
