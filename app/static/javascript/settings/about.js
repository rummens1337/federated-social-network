var centralServer = window.location.origin;

// Call this function when requesting an array of hobbies
function showHobbies(req) {
    // if (req.data.hobbies.length > 0) {
    if (0 == 1) {
      for (i=0; i < req.data.hobbies.length; i++) {
          var hobbie = req.data.hobbies[i];
          showHobbie(hobbie);
      }
    }
    else {
      $('#hobbies-list').append('<p>No hobbies added yet...</p>');
    }
}

// This function adds a friend in the div 'hobbie'
function showHobbie(hobbie) {
    var content = ' <li class="hobbie-selected"><div class="name">' +
        hobbie.title + '</div></li>';
    $('#hobbies-list').append(content);
}

// Call this function when requesting an array of hobbies
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

// This function adds a friend in the div 'hobbie'
function showSkill(skill) {
    var content = ' <li class="skill-selected"><div class="name">' +
        skill.title + '</div></li>';
    $('#skill-list').append(content);
}

// Call this function when requesting an array of hobbies
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

// This function adds a friend in the div 'hobbie'
function showLanguage(showLanguage) {
    var content = ' <li class="hobbie-selected"><div class="name">' +
        hobbie.title + '</div></li>';
    $('#hobbies-list').append(content);
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