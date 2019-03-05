function checkPhone() {
	if($.trim(document.getElementById("username").value).length == 0) {
		$('#telephoneError').html("手机号码不可为空");
		//document.getElementById("username").focus();
		return false;
	}else if($.trim(document.getElementById("username").value).length !=11){
		$('#telephoneError').html("请输入中国大陆11位手机号码");
	}
	else {
		$('#telephoneError').html("");
		return true;
	}
}

function checkPassword() {
	if($.trim(document.getElementById("password").value).length == 0) {
		//.html() 方法为jQuery的方法，需要加载相应的js文件
		$('#passwordError').html("密码不可为空");
		//document.getElementById("password").focus();
		return false;
	} else {
		$('#passwordError').html("");
		return true;
	}
}

function checkPasswordAgain(){
	var passwordjs=$.trim(document.getElementById("password").value);
	var passwordAgain = $.trim(document.getElementById("passwordagain").value);
	if (passwordjs.length==0) {
		$('#passwordAgainError').html("再次输入密码不可为空");
		return false;
	}else if(passwordjs!=passwordAgain){
		$('#passwordAgainError').html("两次输入密码需相同");
		return false;
	}
	else{
		$('#passwordAgainError').html("");
		return true;
	}
}

