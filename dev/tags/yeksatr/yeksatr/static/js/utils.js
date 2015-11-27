var timer = null;

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
}


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

  var dialogMarkup = "\
	<div id='forgotPasswordDialog' title='بازنشانی کلمه عبور'>\
      <p>\
		<form>\
          <p>لطفا نام کاربری خود را وارد نمایید تا در صورت صحیح بودن، راهنمایی های لازم برای آدرس پست الکترونیکی شما ارسال گردند.</p>\
          <br /><br />\
          <label>نام کاربری:</label>&nbsp;<br /><input type='text' id='txtUserForgotPassword' class='bigTextBox'></input>\
		  <br /><br />\
		</form>\
	  </p>\
	</div>";
  
  //resetLoginDialog();
  //$( '#registerDialog' ).dialog( "close" );

    $(dialogMarkup).dialog({
        modal: true,
        closeOnEscapeType: true,
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
                click: function() 
                {
                    $( this ).dialog( "close" );
                }
            }
        ]
    });
}

/*function resetLoginDialog()
{
    $('.loginRegisterDialog > * > .ui-dialog-buttonset > button:last > span').text(' ثبت نام ');
    $('#registerStartButton').show();
    $('#forgotPassword').show();
    $('#registerationFields').css('display','none');
}

function registrationDialogChangetoRegister()
{
  $('.loginRegisterDialog > * > .ui-dialog-buttonset > button:last > span').text(' ثبت نام ');
  $('#registerStartButton').hide();
  $('#registerationFields').css('display','block');
  $('#forgotPassword').hide();
}*/

function openRegistrationDialog()
{
	$('#registerDialog').dialog({
	  modal: true,
      dialogClass: 'loginRegisterDialog',
      closeOnEscapeType: true,
	  width: 500,
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
			  .find(".ui-button").eq(1).css({"float": "right", "width": "150px"});
		  $(this).closest(".ui-dialog")
			  .find(".ui-button").eq(2).css("width", "150px");

		  $('#forgotPassword').on("click", openForgotPasswordDialog);

		  $('#txtUser').focus();
	  }
  });
}

	function doRegister()
	{
		var usertxt = $('#txtUserReg').val();
		var pass = $('#txtPassReg').val();
		var email = $('#txtEmailReg').val();

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

		$.post( "/SignUp", { username: usertxt, email: email ,password: pass} ).
			done(function(data)
				 {
					 if(data.success)
					 {
						 showInfoAlert('ثبت نام با موفقیت انجام شد!');
					 }
					 else
					 {
						 showInfoAlert('نام کاربری یا پست الکترونیک تکراری است! لطفا مجددا تلاش نمایید.');
					 }
				 });


	}
function doLogin()
{
	var isRegisterMode = $('#registerationFields').is(':visible');
	var usertxt = $('#txtUser').val();
	var pass = $('#txtPass').val();

	alert('user='+usertxt+' password='+pass);
	$( this ).dialog( "close" );

	//sign in mode
	$.post( "/SignIn", { username: usertxt, password: pass} ).
		done(function(data)
			 {
				 if(data.success)
				 {
					 var userName = data.name;
					 
					 showInfoAlert('خوش آمدید '+userName+'!');
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
	var dialogMarkup = "\
		<div id='feedbackDialog' title='ارسال نظرات و پیشنهادات'>\
		<p>\
        <p>لطفا هر گونه انتقاد، پیشنهاد یا نظری در مورد یکسطر دارید وارد نموده و کلید ارسال را بزنید.</p>\
		<textarea id='txtFeedback' rows='10' cols='30'></textarea>\
		<br />\
	</p>\
	</div>";
	
    $( dialogMarkup ).dialog({
        modal: true,
        closeOnEscapeType: true,
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
                    $( this ).dialog( "close" );
                }
            }
        ],
		create:function ()
		{
			$(this).closest(".ui-dialog")
				.find(".ui-dialog-titlebar").css("border-radius", "0px");
		}
    });

}	


function resizeTopMenuSearchBox()
{
	var w = $(window).width() - 690;

	var usedWidth =
			$('#feedbackButton').outerWidth(true) +
			$('#topLogo').outerWidth(true) +
			$('#advSearchBtn').outerWidth(true) +
			$('#searchBtn').outerWidth(true);

	if ( $('#registerLink').is(':visible') )
	{
		usedWidth += $('#registerLink').outerWidth(true);
	}

	if ( $('#profileButton').is(':visible') )
	{
		usedWidth += $('#profileButton').outerWidth(true);
		w -= 60;
	}

	usedWidth += 120;
	

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
