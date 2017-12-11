 // Initialize Firebase
  var config = {
    apiKey: "AIzaSyCHVUY5JdL1gqZx7juQQlaIAIB8R76A7ZE",
    authDomain: "oopproject-f5214.firebaseapp.com",
    databaseURL: "https://oopproject-f5214.firebaseio.com",
    projectId: "oopproject-f5214",
    storageBucket: "oopproject-f5214.appspot.com",
    messagingSenderId: "294439860189"

  };
  firebase.initializeApp(config);

  //Get Elements
var uploader = document.getElementById('uploader');
var fileButton = document.getElementById('fileButton');

//Listen for file selection
fileButton.addEventListener('change',function(e) {
//Get file
    var file = e.target.files[0];

//Create a storage ref
    var storageRef = firebase.storage().ref('Images/' + file.name);
    var firebaseRef = firebase.database().ref();
//Upload file
    var task = storageRef.put(file);

    function error(err) {
        console.log('error', err);
    }


//Get a reference to store file at photos/<FILENAME>.jpg
    task.on('state_changed', null, null, function () {
        //When the image has successfully uploaded we get its download URL
        var downloadURL = task.snapshot.downloadURL;
        document.querySelector('img').src = downloadURL;
        var messageText = downloadURL;
        firebaseRef.child('Images').push(messageText);
    });
});

