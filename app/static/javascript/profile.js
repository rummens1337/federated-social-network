var username = null;

function addFriend(friend) {
    requestJSON('GET', '/api/user/address', null, function(req) {
      requestJSON('POST', req.data.address + "/api/friend/add", {"friend" : friend }, function(req) {
        // Friend request is sent
        location.reload();
      }, function(req) {
        alertError(req.reason, 2000);
      });
    }, function(req) {
      alertError(req.reason, 2000);
    });
}

function deleteFriend(friend) {
    requestJSON('GET', '/api/user/address', null, function(req) {
        requestJSON('POST', req.data.address + "/api/friend/delete", {"friend" : friend }, function(req) {
            // Friend is deleted
            location.reload();
        }, function(req) {
            alertError(req.reason, 2000);
        });
    }, function(req) {
        alertError(req.reason, 2000);
    });
}

function acceptFriend(friend) {
    location.href = "/friend/requests";
}

// Set the HTML
// TODO
function profile(req) {
    var friend_status = req.data.friend;

    if (friend_status == 1) {
        document.getElementById('image_url').src = req.data.image_url;
        document.getElementById('location').innerHTML = req.data.location;
        document.getElementById('name').innerHTML = req.data.firstname + ' ' + req.data.lastname;
        document.getElementById('study').innerHTML = req.data.study;
        document.getElementById('bio').innerHTML = req.data.bio;
        document.getElementById('status').innerHTML = req.data.relationship_status;
        document.getElementById('number').innerHTML = req.data.phone_number;
    } else {
        document.getElementById('name').innerHTML = req.data.username;
        $("#stats").remove();
        $("#about").remove();
        $("#posts").remove();
    }

    if (document.getElementById('add_friend') != null) {
      var friend = req.data.username;
      if (friend_status == 0) document.getElementById('add_friend').innerHTML = "Befriend me!";
      else if (friend_status == 1) {
        document.getElementById('add_friend').innerHTML = "Unfriend";
        $("#add_friend").attr("onclick", "deleteFriend('"+friend+"')");
      }
      else if (friend_status == 2) {
        document.getElementById('add_friend').innerHTML = "Pending..";
        $("#add_friend").attr("onclick", "deleteFriend('"+friend+"')");
      }
      else if (friend_status == 3) {
        document.getElementById('add_friend').innerHTML = "Accept friendship request";
        $("#add_friend").attr("onclick", "acceptFriend('"+friend+"')");
      }
    }
}

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
    '<h6 class="w3-text-teal"><i class="fa fa-circle fa-fw w3-margin-right"></i>' +
    hobby.title +
    '</h6> <hr>'
  $('#hobbies-list').append(content);
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
  '</div>' + '<br>'
  $('#languages-list').append(content);
}

// Get the data of the profile
function getProfile(req) {
    var dataServer = req.data.address;
    if (username == null || username == "") {
      var urlProfile = dataServer + '/api/user'
      var urlSkills = dataServer + '/api/user/skill'
      var urlLanguages = dataServer + '/api/user/language'
      var urlHobbies = dataServer + '/api/user/hobby'
    }
    else {
      var urlProfile = dataServer + '/api/user?username=' + username
      var urlSkills = dataServer + '/api/user/skill?username=' + username
      var urlLanguages = dataServer + '/api/user/language?username=' + username
      var urlHobbies = dataServer + '/api/user/hobby?username=' + username
    }

    requestJSON('GET', urlProfile, null, profile, function(req) {
        alertError(req.reason, 2000);
        location.href = "/";
    });
    requestJSON('GET', urlSkills, null, showSkills, function(req) {
        alertError(req.reason, 2000);
        location.href = "/";
    });
    requestJSON('GET', urlLanguages, null, showLanguages, function(req) {
          alertError(req.reason, 2000);

      location.href = "/";
    });
    requestJSON('GET', urlHobbies, null, showHobbies, function(req) {
      alertError(req.reason, 2000);

  location.href = "/";
});
}

function editSucces() {
  window.location.reload();
}

function editFailed(response) {
  alertError(response.reason, 2000);
}

// Get the address of the profile
function loadProfile(u) {
    username = u;
    setup();
    var url = (username == null || username == "") ?
      '/api/user/address' :
      '/api/user/address?username=' + username;

    requestJSON('GET', url, null, getProfile, function(req) {
      alertError(req.reason, 2000);
      location.href = "/";
    });
}

// Setup the profile page
function setup() {
  if (getUsername() == username) {
    $("#add_friend").remove();
  }
}