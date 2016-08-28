/*
//以下是使用ajax异步发送数据的js代码
//单独构建的异步加载的警告框
function showAlert(error){
	$(function(){
		var alert_model = '<div class="alert alert-warning"><strong></strong><button id="close" type="button" class="close" data-dismiss="alert"><span>&times;</span></button></div>' ;
		$("#alert-model .alert strong").text(error);
		$("#alert-model").show(300);
		$('#close').click(function(){
			$("#alert-model").hide(300,function(){
				var al = $(alert_model);
				if ($('.alert').length == 0)
				{
					$('#alert-model-in').append(al);
				}
			});
		});
	});
}
#匹配email格式
function regEmail(email){
		var re_email = /^[0-9a-zA-Z\-\.\_\$]+\@[0-9a-zA-Z]+(\.[a-zA-Z]{1,4})$/;
		return (re_email.test(email));
}
#匹配密码格式
function regPasswd(passwd){
		var re_pass = /^[0-9a-zA-Z\_\.]{6,20}$/;
		return (re_pass.test(passwd));
}
#获取浏览器cookie值
$(function(){
	function getCookie(name) {
	    var cookieValue = null;
	    if (document.cookie && document.cookie !== '') {
	        var cookies = document.cookie.split(';');
	        for (var i = 0; i < cookies.length; i++) {
	            var cookie = jQuery.trim(cookies[i]);
	            // Does this cookie string begin with the name we want?
	            if (cookie.substring(0, name.length + 1) === (name + '=')) {
	                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
	                break;
	            }
	        }
	    }
	    return cookieValue;
	}
	#获取到csrftoken
	var csrftoken = getCookie('csrftoken');
		function csrfSafeMethod(method) {
	    // these HTTP methods do not require CSRF protection
	    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
	}
	#对ajax进行设置
	$.ajaxSetup({
	    beforeSend: function(xhr, settings) {
	        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
	            xhr.setRequestHeader("X-CSRFToken", csrftoken);
	        }
	    }
	});
	#异步提交表单
	$('#btn_register').on("click",function(event){
		event.preventDefault();
		var username = $('#id_username').val();
		var passwd = $('#id_password').val();
		var passwd2 = $('#id_password2').val();
		var email = $('#id_email').val();
		if (passwd !== passwd2){
			showAlert("密码输入不一致，请重新输入！");
		}
		else{
			var password = CryptoJS.SHA1(passwd).toString();
			var datas = {
				username: username,
				password: password,
				email: email
			}
			$.ajax(
				'register',
				{
					type: 'POST',
					data: JSON.stringify(datas||{}),
					datatype:'json',
					contentType:'application/json'
				}).then(function(data,status,j){
					//alert(data);
					//alert(status);
					//alert((j.responseText).toString());
				});
		}
	});
});*/
//将密码表单在提交前，对其进行sha1加密
/*
function exchangePassword(){
	if ($('#id_password').val()) {
		var passwd = $('#id_password').val();
		$('#id_password').val(CryptoJS.SHA1(passwd).toString());
	}
	if ($('#id_password2').val()) {
		var passwd2 = $('#id_password2').val();
		$('#id_password2').val(CryptoJS.SHA1(passwd2).toString());
	}

	if ($('#id_old_password').val()) {
		var old_passwd = $('#id_old_password').val();
		$('#id_old_password').val(CryptoJS.SHA1(old_passwd).toString());
	}
	if ($('#id_new_password1').val()) {
		var new_passwd1 = $('#id_new_password1').val();
		$('#id_new_password1').val(CryptoJS.SHA1(new_passwd1).toString());
	}
	if ($('#id_new_password2').val()) {
		var new_passwd2 = $('#id_new_password2').val();
		$('#id_new_password2').val(CryptoJS.SHA1(new_passwd2).toString());
	}
	alert('123');
}
*/
//模拟使用搜索功能时的ajax动态显示，并非ajax
$(function(){
	$('.loading').hide(1000,function(){
		$('.search-bar').show(500);
	});
});

$(function(){
	var current_pathname = window.location.pathname;
	var reg_py = /^\/blog\/python\//;
	var reg_zz = /^\/blog\/zhuanzai\//;
	var reg_dj = /^\/blog\/djangoins\//;
	var reg_yc = /^\/blog\/yuanchuang\//;
	if (reg_py.test(current_pathname)){
		$('#nav-py').addClass('active');
	}
	else if (reg_zz.test(current_pathname)){
		$('#nav-zz').addClass('active');
	}
	else if (reg_dj.test(current_pathname)){
		$('#nav-dj').addClass('active');
	}
	else if (reg_yc.test(current_pathname)){
		$('#nav-yc').addClass('active');
	}
	else{
		$('#nav-ne').addClass('active');
	}
});


