function showpass() {
  var x = document.getElementById("password");
  if (x.type === "password") {
    x.type = "text";
  } else {
    x.type = "password";
  }

var y = document.getElementById("myInput1");
  if (y.type === "password") {
    y.type = "text";
  } else {
    y.type = "password";
  }


}

function regbtn() {

var password = document.getElementById("password")
  , confirm_password = document.getElementById("myInput1");

function validatePassword(){
  if(password.value != confirm_password.value) {
    confirm_password.setCustomValidity("Password doesn't Match");
  } else {
    confirm_password.setCustomValidity('');
  }
}

password.onchange = validatePassword;
confirm_password.onkeyup = validatePassword;
}



