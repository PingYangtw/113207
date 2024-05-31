// Callback function for successful sign-in
function onSignIn(googleUser) {
  // Handle sign-in logic here, e.g., send user data to server
  var profile = googleUser.getBasicProfile();
  console.log('ID: ' + profile.getId()); // Do something with the user's ID
  console.log('Name: ' + profile.getName()); // Do something with the user's name
  console.log('Image URL: ' + profile.getImageUrl()); // Do something with the user's image URL
  console.log('Email: ' + profile.getEmail()); // Do something with the user's email
}
