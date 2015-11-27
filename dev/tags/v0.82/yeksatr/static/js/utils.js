
function onAppLoad()
{
	$('#faq').click(function(e)
					{
						customDialog('#faqDialog','سوالات متداول');
						e.preventDefault();
						
						return false;
					});
	$('#tos').click(function(e)
					{
						customDialog('#tosDialog','شرایط خدمات');
						e.preventDefault();
						
						return false;
					});


	$('#pp').click(function(e)
				   {
					   customDialog('#ppDialog','حریم خصوصی');
					   e.preventDefault();
					   
					   return false;
				   });
	$('#about').click(function(e)
					  {
						  customDialog('#aboutDialog','درباره ما');
						  e.preventDefault();
						  
						  return false;
					  });


	$('#searchBtn').click(function(e)
					  {
						  window.location.href = "?q="+$('#searchBox').val();
						  return false;
					  });
					  
	$('#searchBox').on("keypress", function(e) {
            if (e.keyCode == 13) 
            	$('#searchBtn').click()
      });
	
	$('#registerDialog').hide();
	$('#feedbackDialog').hide();
	$('#tosDialog').hide();
	$('#faqDialog').hide();
	$('#ppDialog').hide();
	$('#aboutDialog').hide();
	
    $('#infoRow').hide();
    $('#forgotPasswordDialog').hide();
	$('#profileMenu').hide();

    $('.persiaNumber').persiaNumber();

    $('#searchBtn').focus();
    $('#advSearchBtn').on("click", toggleAdvancedSearchPanel);
    $('#registerButton').on("click", openRegistrationDialog);
    $('#alternativeRegisterLink').on("click", function()
									 {
										 openRegistrationDialog();
										 //      registrationDialogChangetoRegister();
									 });

	$(window).on("resize", resizeTopMenuSearchBox);


	$('#registerStartButton').on("click", openRegistrationDialog);


	$('#feedbackButton').on("click", openFeedbackDialog);
	$('#profileButton').on("click", toggleProfileMenu);

	$('#refreshCaptcha').on('click', function()
							{
								
								var temp = $('#captcha').attr("src");
								$('#captcha').attr("src", "");
								$('#captcha').attr("src", temp+"?timestamp=" + new Date().getTime());
							});

	resizeTopMenuSearchBox();

	$(document).mouseup(function (e)
						{
							var container = $("#profileMenu");

  							if ( $('#profileMenu').is(':visible'))
							{
								if (!container.is(e.target) // if the target of the click isn't the container...
									&& container.has(e.target).length === 0) // ... nor a descendant of the container
								{
									toggleProfileMenu();
								}
							}});

	$('#signOutMenuItem').on('click', onLogout);
	$( document ).tooltip(
		{
			open: function (event, ui) {
				setTimeout(function () {
					$(ui.tooltip).hide('fade');
				}, 1500)}
		});

	$("#faqDialog").load('static/html/faq.html');
	$("#ppDialog").load('static/html/pp.html');
	$("#tosDialog").load('static/html/tos.html');
	$("#aboutDialog").load('static/html/about.html');
	
	if($('#alertMessage').val().length > 0)
		showInfoAlert($('#alertMessage').val());
}
	  









/*var timer = null;

function setupTimePanel()
{
    var time = new Date()
    var hours = time.getHours()
    var minutes = time.getMinutes()
    minutes=((minutes < 10) ? "0" : "") + minutes
    var seconds = time.getSeconds()
    seconds=((seconds < 10) ? "0" : "") + seconds
    var clock = hours + ":" + minutes + ":" + seconds

    $('#cTime').html(clock).persiaNumber();
    timer = setTimeout("setupTimePanel()",1000)
}

function getDatePersian()
{
    week= new Array("يكشنبه","دوشنبه","سه شنبه","چهارشنبه","پنج شنبه","جمعه","شنبه")
    months = new Array("فروردين","ارديبهشت","خرداد","تير","مرداد","شهريور","مهر","آبان","آذر","دي","بهمن","اسفند");
    a = new Date();
    d= a.getDay();
    day= a.getDate();
    month = a.getMonth()+1;
    year= a.getYear();
    year = (year== 0)?2000:year;
    (year<1000)? (year += 1900):true;
    year -= ( (month < 3) || ((month == 3) && (day < 21)) )? 622:621;
    switch (month) 
    {
    case 1: (day<21)? (month=10, day+=10):(month=11, day-=20); break;
    case 2: (day<20)? (month=11, day+=11):(month=12, day-=19); break;
    case 3: (day<21)? (month=12, day+=9):(month=1, day-=20); break;
    case 4: (day<21)? (month=1, day+=11):(month=2, day-=20); break;
    case 5:
    case 6: (day<22)? (month-=3, day+=10):(month-=2, day-=21); break;
    case 7:
    case 8:
    case 9: (day<23)? (month-=3, day+=9):(month-=2, day-=22); break;
    case 10:(day<23)? (month=7, day+=8):(month=8, day-=22); break;
    case 11:
    case 12:(day<22)? (month-=3, day+=9):(month-=2, day-=21); break;
    default: break;
    }

    return (" "+week[d]+" "+day+" "+months[month-1]+" "+ year);
}

function toPersianNumber(x)
{
    var result = x;
    persian={0:'۰',1:'۱',2:'۲',3:'۳',4:'۴',5:'۵',6:'۶',7:'۷',8:'۸',9:'۹'};

    var list=x.match(/[0-9]/g);
    if(list!=null && list.length!=0)
    {
        for(var i=0;i<list.length;i++)
        {
            x = x.replace(list[i],persian[list[i]]);
        }
    }
    return result;
}*/


function showAdvancedSearchPanel()
{
    if (!$('#advSearchBtn').hasClass("activeButton") )
    {
        $('#advSearchBtn').addClass("activeButton");
        $( "#topMenu" ).animate({height: "+=40px"});
        $( "body" ).animate({paddingTop: "+=40px"});
		$("#infoRow").fadeIn();
    }
}

function hideAdvancedSearchPanel()
{
    if ($('#advSearchBtn').hasClass("activeButton") )
    {
        $('#advSearchBtn').removeClass("activeButton");
        $( "#topMenu" ).animate({height: "-=40px"});
        $( "body" ).animate({paddingTop: "-=40px"});
		$("#infoRow").fadeOut();
    }
}

function toggleAdvancedSearchPanel()
{
    if ($('#advSearchBtn').hasClass("activeButton") )
    {
        hideAdvancedSearchPanel();                
    }
    else
    {
        showAdvancedSearchPanel();
    }
}

function openForgotPasswordDialog()
{
	$( '#registerDialog' ).dialog( "close" );
	
    $('#forgotPasswordDialog').dialog({
        modal: true,
        closeOnEscapeType: true,
		dialogClass: 'loginRegisterDialog',
		width: 520,
        buttons: [
            {
                text: "انصراف",
                icons: { primary: "ui-icon-closethick" },
                click: function() 
                {
                    $( this ).dialog( "close" );
                }
            },
            {
                text: " بازنشانی کلمه عبور ",
                icons: { primary: "ui-icon-gear" },
                click: onForgotPassword                
            }
        ],
		open:function ()
		{
			$(this).closest(".ui-dialog")
				.find(".ui-dialog-buttonset").css("width", "100%");

			$(this).closest(".ui-dialog")
				.find(".ui-button").eq(1).css({"float": "right"});
			
			$(this).closest(".ui-dialog")
				.find(".ui-button").eq(2).css("width", "170px");

			$(this).closest(".ui-dialog")
				.find(".ui-dialog-titlebar").css("border-radius", "0px");

			$('#txtUserForgotPassword').focus();
		}
    });
}

function onForgotPassword()
{
	var usertxt = $('#txtUserForgotPassword').val();

	$.post( "/api/ForgotPassword", { username: usertxt} ).
		done(function(data)
			 {
				 showInfoAlert('اطلاعات لازم برای ورود به یکسطر تا چند دقیقه دیگر به آدرس پست الکترونیکی شما ارسال خواهند شد.');
			 });

	
    $( this ).dialog( "close" );
}

function onResetPassword(forgotKey)
{
	$.post( "/api/ResetPassword", { resetKey: forgotKey} ).
		done(function(data)
			 {
				 if(data.success)
				 {
					 showInfoAlert('اطلاعات مربوط به کلمه عبور جدید به آدرس پست الکترونیکی شما ارسال شد.');
				 }
				 else
				 {
					 showInfoalert('بروز مشکل در بازنشانی کلمه عبور! لطفا مجددا تلاش فرمایید')
				 }
			 });
}

function openRegistrationDialog()
{
	$('#registerDialog').dialog({
		modal: true,
		dialogClass: 'loginRegisterDialog',
		closeOnEscapeType: true,
		resizable: false,
		width: 520,
		buttons: [
		  {
			  text: " ثبت نام ",
			  icons: { primary: "ui-icon-pencil" },
			  click: doRegister
		  },
		  {
			  text: " ورود ",
			  icons: { primary: "ui-icon-gear" },
			  click: doLogin
		  }
	  ],
	  open:function ()
	  {
		  $(this).closest(".ui-dialog")
			  .find(".ui-dialog-buttonset").css("width", "100%");

		  $(this).closest(".ui-dialog")
			  .find(".ui-button").eq(1).css({"float": "right"});
		  
		  $(this).closest(".ui-dialog")
			  .find(".ui-button").slice(1).css("width", "160px");

		  $('#forgotPassword').on("click", openForgotPasswordDialog);

		  $(this).closest(".ui-dialog")
			  .find(".ui-dialog-titlebar").css("border-radius", "0px");

		  $('#txtUser').focus();
	  }
  });
}

	function doRegister()
	{
		var usertxt = $('#txtUserReg').val();
		var pass = $('#txtPassReg').val();
		var email = $('#txtEmailReg').val();
		var ci = $('#captchaImg').val();
		var ct = $('#captchaText').val();

		if ( usertxt.length < 6)
		{
			alert("طول نام کاربری باید حداقل شش حرف باشد! لطفا مجددا تلاش نمایید.");
			return false;
		}

		if ( pass.length < 6)
		{
			alert("طول کلمه عبور باید حداقل شش حرف باشد! لطفا مجددا تلاش نمایید.");
			return false;
		}

		if ( !isValidEmailAddress(email) )
		{
			alert("لطفا آدرس پست الکترونیک معتبری را وارد نمایید");

			return false;
		}

		$( this ).dialog( "close" );

		$.post( "/api/SignUp", { username: usertxt, email: email ,password: pass, captchaText: ct, captchaImg: ci} ).
			done(function(data)
				 {
					 if(data.success)
					 {
						 showInfoAlert('ثبت نام با موفقیت انجام شد!');
					 }
					 else
					 {
						 var fail_type = data.fail_type;

						 if ( fail_type == 'data' )
						 {
							 showInfoAlert('نام کاربری یا پست الکترونیک تکراری است! لطفا مجددا تلاش نمایید.');
						 }
						 else if ( fail_type == 'captcha' )
						 {
							 showInfoAlert('متن وارد شده مطابق عکس نمایش داده شده نیست.');
						 }
					 }
				 });


	}
function doLogin()
{
	var isRegisterMode = $('#registerationFields').is(':visible');
	var usertxt = $('#txtUser').val();
	var pass = $('#txtPass').val();

	$( this ).dialog( "close" );

	//sign in mode
	$.post( "/api/SignIn", { username: usertxt, password: pass} ).
		done(function(data)
			 {
				 if(data.success)
				 {
					 var userName = data.name;
					 
					 showInfoAlert('خوش آمدید '+userName+'!');

					 setTimeout(function(){location.reload(false);}, 3000);
				 }
				 else
				 {
					 showInfoAlert('نام کاربری یا کلمه عبور نادرست می باشد! لطفا مجددا تلاش کنید');
				 }
			 });


}


function showInfoAlert(msg)
{
    //Note: call showInfoAlert("سلام من اومدم"); to show short-length alert and info messages
    $('#alertDiv #textMsg').text(msg);
    $('#alertDiv').fadeIn(1200).delay(600).fadeOut(1200);
}


function isValidEmailAddress(emailAddress) {
    var pattern = new RegExp(/^[+a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}$/i);
    // alert( pattern.test(emailAddress) );
    return pattern.test(emailAddress);
};


function openFeedbackDialog()
{
    $('#feedbackDialog').dialog({
        modal: true,
		resizable: false, 
        closeOnEscapeType: true,
		width: 500, 
        buttons: [
            {
                text: "انصراف",
                icons: { primary: "ui-icon-closethick" },
                click: function() 
                {
                    $( this ).dialog( "close" );
                }
            },
            {
                text: " ارسال ",
                icons: { primary: "ui-icon-gear" },
                click: function() 
                {
					$.post( "/api/Feedback", { txtFeedback: $('#txtFeedback').val()} );
					$( this ).dialog( "close" );
					showInfoAlert('پیام شما برای مدیریت ارسال شد. از لطف شما سپاسگذاریم.');
				}
            }
        ],
		open:function ()
		{
			$(this).closest(".ui-dialog")
				.find(".ui-dialog-titlebar").css("border-radius", "0px");

			$(this).closest(".ui-dialog")
				.find(".ui-button").eq(2).css("width", "120px");

		}
    });

}	


function resizeTopMenuSearchBox()
{
	var w = $(window).width() - 600;

	if ( $('#profileButton').is(':visible') )
	{
		w -= 30;
	}


	$('#searchBox').width(w);
}


function toggleProfileMenu()
{
	if ( $('#profileMenu').is(':visible'))
	{
		$('#profileMenu').fadeOut(300);
	}
	else
	{
		var buttonLocation = $('#profileButton').position();
		$('#profileMenu').css('top', buttonLocation.top + 35);
		$('#profileMenu').css('left', buttonLocation.left);
		$('#profileMenu').width($('#profileButton').outerWidth()-2);
		$('#profileMenu').fadeIn(300);
	}
	
}

function customDialog(container, title_msg)
{
	if (!title_msg)
        title_msg = 'Alert';
	
    $(container).dialog({
        title: title_msg,
        resizable: false,
        modal: true,
		maxHeight: 500,
		width: 500,
        buttons: {
            " بازگشت ": function() 
            {
                $( this ).dialog( "close" );
            }
        }
    }); //.css({"height":"500px", "overflow-y":"auto"});
}

function onLogout()
{
	$.post( "/api/SignOut").
		done(function(data)
			 {
					 location.reload(false);
			 });
}
