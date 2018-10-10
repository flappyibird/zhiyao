function checkPPhone() {
	if($.trim(document.getElementById("pPhone").value).length !=11){
		$('#telephoneError').html("请输入中国大陆11位手机号码");
	}
	else {
		$('#telephoneError').html("");
		return true;
	}
}

function checkSPhone() {
	if($.trim(document.getElementById("sPhone").value).length !=11){
		$('#telephoneError').html("请输入中国大陆11位手机号码");
	}
	else {
		$('#telephoneError').html("");
		return true;
	}
}