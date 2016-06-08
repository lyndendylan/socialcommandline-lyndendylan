function setApiKey() {
  gapi.client.setApiKey("495648704485-v26akd5cfusb7aibvraaonnmp1d9sd0n.apps.googleusercontent.com ");
}

function onSuccess(googleUser) {
    window.gu = googleUser;
    console.log('Logged in as: ' + googleUser.getBasicProfile().getName());
    plus();
}

function onFailure(error) {
  console.log(error);
}

function renderButton() {
  gapi.signin2.render('my-signin2', {
    'scope': 'profile email https://www.googleapis.com/auth/plus.login https://www.googleapis.com/auth/plus.me',
    'theme': 'dark',
    'onsuccess': onSuccess,
    'onfailure': onFailure
  });
}

function plus() {
  gapi.client.load('plus','v1', function(){
    var request = gapi.client.plus.people.list({
      'userId': "me",
      'collection': 'visible'
    });
    request.execute(function(resp) {
      console.log(resp);
      //console.log('Num people visible:' + resp.totalItems);
    });
  });
}

