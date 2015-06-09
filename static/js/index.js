 
function signinCallback(authResult) {
  if (authResult['status']['signed_in']) {
    // Update the app to reflect a signed in user
    // Hide the sign-in button now that the user is authorized, for example:

    gapi.client.load('plus', 'v1', function() {
          var request = gapi.client.plus.people.get({
            'userId': 'me'
          });
          request.execute(function(resp) {
            
			  console.log('Profile URL: ' + resp.emails[0].value);


			  $.ajax({
                type: 'POST',
                url: '/login',
                data: {'oauth':'yes' ,'email':resp.emails[0].value},
                success: function(data){
                    
                     //location.href="profile.html?argument="+argument;
                     //alert(data.argument);
                     email = data.argument;
                     var link = 'profile.html';  
				     //   //alert(link);
				     // window.open(link,"_self");
				     window.location.replace(link);


				      
                     
                },
                error:function(e){
                	console.log(JSON.stringify(e));
                }
            });


          });
        });
 
    //document.getElementById('signinButton').setAttribute('style', 'display: none');
    


  } else {
    // Update the app to reflect a signed out user
    // Possible error values:
    //   "user_signed_out" - User is signed-out
    //   "access_denied" - User denied access to your app
    //   "immediate_failed" - Could not automatically log in the user
    console.log('Sign-in state: ' + authResult['error']);
  }
}

function signOut(){
  gapi.auth.signOut();
}