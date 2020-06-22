var centralServer = window.location.origin;

// Call this function when requesting an array of hobbies
function showHobbies(req) {
    // if (req.data.hobbies.length > 0) {
    if (0 == 1) {
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
    var content = ' <li class="hobby-selected"><div class="name">' +
        hobby.title + '</div></li>';
    $('#hobbies-list').append(content);
}

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
    var content = ' <li class="skill-selected"><div class="name">' +
        skill.title + '</div></li>';
    $('#skill-list').append(content);
}

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
function showLanguage(showLanguage) {
    var content = ' <li class="language-selected"><div class="name">' +
        language.title + '</div></li>';
    $('#languages-list').append(content);
}

function setDataAddress(req) {
    dataServer = req.data.address;
    requestJSON('GET', dataServer + '/api/friend/all', null, showHobbies, function(req) {
        alertError(req.reason, 2000);
    });
    requestJSON('GET', dataServer + '/api/friend/all', null, showSkills, function(req) {
        alertError(req.reason, 2000);
    });
    requestJSON('GET', dataServer + '/api/friend/all', null, showLanguages, function(req) {
        alertError(req.reason, 2000);
    });
}

$(document).ready(function() {
    requestJSON('GET', '/api/user/address', null, setDataAddress, function(req) {
        alertError(req.reason, 2000);
    });
});