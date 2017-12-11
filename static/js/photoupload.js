 // Initialize Firebase
  var config = {
    apiKey: "AIzaSyB1sMTQ-9UT2nrnHhwd2RxYVUAosh1_cdk",
    authDomain: "smartkampung-e3ec3.firebaseapp.com",
    databaseURL: "https://smartkampung-e3ec3.firebaseio.com",
    projectId: "smartkampung-e3ec3",
    storageBucket: "smartkampung-e3ec3.appspot.com",
    messagingSenderId: "643996718253"
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

