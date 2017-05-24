$("textarea#commenttext").on('input', function () { 
	// this.style.height = '72px';
	// this.style.height = (this.scrollHeight)+'px';
	commmentheightadjust()
	commentwordcount()
});
$("textarea#composetext").on('input', function () { 
	// this.style.height = '76px';
	// this.style.height = (this.scrollHeight)+'px';
	// $("textarea#composetext").css("height",'76px');
	// $("textarea#composetext").css("height", ($("textarea#composetext")[0].scrollHeight)+'px');
	composeheightadjust()
	composewordcount()
	// $("#composebody").scrollTop($("#composebody").height())
	
});

function commmentheightadjust()
{
	var el_composetext = document.getElementById("commenttext")
	el_composetext.style.height = '72px'
	el_composetext.style.height = (el_composetext.scrollHeight) + 'px'
}

function composeheightadjust()
{
	var el_composetext = document.getElementById("composetext")
	el_composetext.style.height = '76px'
	el_composetext.style.height = (el_composetext.scrollHeight) + 'px'
}

function commentwordcount(){
	var wordcount = $("textarea#commenttext").val().length
	if($("textarea#commenttext").attr("placeholder")=="添加评论...")
		$(".comment_actionbar>#counter").html(140 - wordcount)
	else
		$(".comment_actionbar>#counter").html(140 - $("textarea#commenttext").attr("placeholder").length - wordcount)

	if(wordcount>140)
		$(".comment_actionbar>#counter").attr("class","textoverflow")
	else
		$(".comment_actionbar>#counter").attr("class","")
}

function composewordcount(){
	var wordcount = $("textarea#composetext").val().length
	$(".compose_actionbar>#counter").html(140 - wordcount)
	if(wordcount > 140)
	{		$(".compose_actionbar>#counter").attr("class","textoverflow")
			$("#topbar>.action#send").attr("class","action false")
	}
	else
	{
		$(".compose_actionbar>#counter").attr("class","")
		$("#topbar>.action#send").attr("class","action")
	}

	if(wordcount == 0&&$("#originview").css("display") == "none")
	{
		$("#topbar>.action#send").attr("class","action false")
	}
}

function repostprepare(onepost)
{
	var poster = onepost.children(".postinfo").children(".poster").html()
	var bgurl = ""
	var filledtext = ""
	var origintext = "@" + poster + ":" + onepost.children(".postbody").children(".posttext").html()

	if(onepost.children(".postbody").children(".gallery").children(".thumb").length>0)
	{
		bgurl = onepost.children(".postbody").children(".gallery").children(".thumb:first-child").css("background-image")
	}

	//repost to repost
	if(onepost.children(".repostbody").length>0)
	{
		filledtext = "//@" + poster + ":" + onepost.children(".postbody").children(".posttext").html()
		origintext = onepost.children(".repostbody").children(".reposttext").html()
		if(onepost.children(".repostbody").children(".gallery").children(".thumb").length>0)
		{
			bgurl = onepost.children(".repostbody").children(".gallery").children(".thumb:first-child").css("background-image")
		}
	}

	origintext = origintext.replace(/<[^>]+>/g,"")

	$("#originview>#origintext").html(origintext)
	$("textarea#composetext").attr("placeholder","转发微博")

	if(bgurl.length == 0)
	{
		$("#originview").attr("class", "withoutpic")
	}
	else
	{
		$("#originview").attr("class", "")
		$("#originview>#originpic").css("background-image",bgurl)
	}

	if(filledtext.length != 0)
	{
		filledtext = filledtext.replace(/<[^>]+>/g,"")
		$("textarea#composetext").val(filledtext)
		composeheightadjust()
		$("textarea#composetext").get(0).setSelectionRange(0,0);
	}
	else
	{
		$("textarea#composetext").val("")
	}
}



function repostenter(action)
{
	var onepost = action.parent().parent()
	var pid = onepost.attr("pid")

	// var status = {}
	// status.page = "repostpage"
	// status.pid = pid
	// history.pushState(status,null,null)

	history.state.page = "repostpage"
	history.state.pid = pid
	history.pushState(history.state,null,null)

	repostprepare(onepost)

	$("#originview").css("display","block")
	$("#withcommentcheck").css("display","block")
	$(".compose_actionbar>.action#camera").attr("class","action false")
	$("#composeimageset").empty()
	$("#composeimageset").css("display","none")

	$(".pagelayout").attr("class", "pagelayout unfocus")
	$(".pagelayout").eq(0).attr("class", "pagelayout under") //mainpage

	$("body").addClass("locking")
	$(".pagelayout#composepage").attr("class", "pagelayout staymiddle");
	$(".pagelayout#composepage").attr("class", "pagelayout animate slidetop");


	var textouterWidth = $("#originview>#origintext").width() + Number($("#originview>#origintext").css("margin-left").slice(0,-2)) + Number($("#originview>#origintext").css("margin-right").slice(0,-2))

	if($("#originview").width()>textouterWidth)
	{
		$("#originview>#origintext").attr("class","oneline")
	}
	else
	{
		$("#originview>#origintext").attr("class","")
	}

	composewordcount()

	setTimeout(function(){
	 	$(".pagelayout#composepage").attr("class", "pagelayout focus")
	 	$(".pagelayout").eq(0).attr("class", "pagelayout unfocus") //mainpage
	 	$("textarea#composetext").focus()
	},180);

}

function repostquit()
{
	$(".pagelayout").eq(0).attr("class", "pagelayout under") //mainpage
	$(".pagelayout#composepage").attr("class", "pagelayout staytop");
	$(".pagelayout#composepage").attr("class", "pagelayout animate slidemiddle");
	setTimeout(function(){
		$("body").removeClass("locking")
		$(".pagelayout").attr("class", "pagelayout unfocus");
		$(".pagelayout").eq(0).attr("class", "pagelayout focus"); //mainpage
	},180)
}



function composeenter(){
	// var status = {}
	// status.page = "composepage"
	// history.pushState(status,null,null)

	history.state.page = "composepage"
	history.pushState(history.state,null,null)

	$(".pagelayout").attr("class", "pagelayout unfocus")
	$(".pagelayout#composepage").attr("class", "pagelayout focus")

	if($("#originview").css("display")!="none")
	{
		$("#originview").css("display","none")
		$("textarea#composetext").val("")
	}
	$("#withcommentcheck").css("display","none")
	$("textarea#composetext").attr("placeholder","说点什么")

	$(".compose_actionbar>.action#camera").attr("class","action")
	$("#composeimageset").css("display","table")

	$("body").addClass("locking")

	$("#cover").css("visibility","visible");
	$("#cover").css("transform","scale(40)")

	composewordcount()	
	
	setTimeout(function(){
		$("#cover").css("visibility","hidden");
		$(".pagelayout#composepage>#composetext").focus()
	},800)
	
}

function composequit()
{
	$("#cover").css("visibility","visible");
	$("#cover").css("transform","scale(1)")
	setTimeout(function(){
		$(".pagelayout").attr("class", "pagelayout unfocus");
		$(".pagelayout#indexpage").attr("class", "pagelayout focus");
		$("body").removeClass("locking")
		$("#cover").css("visibility","hidden");
	},800)
}


function repostwithcommentcheck()
{
	if($(".pagelayout#composepage #checkradio").attr("class")=="unselected")
	{
		$(".pagelayout#composepage #checkradio").attr("class", "selected");
	}
	else if($(".pagelayout#composepage #checkradio").attr("class")=="selected")
	{
		$(".pagelayout#composepage #checkradio").attr("class", "unselected");
	}
}


function toast(info)
{
	$("#toast").css("visibility","visible")
	$("#toast").css("opacity","1")
	$("#toast>.text").html(info)
	setTimeout(function(){
		$("#toast").css("opacity","0")
		setTimeout(function(){
			$("#toast").css("visibility","hidden")
		},360)
	},2000)
}


function adjustcounter(numdom,operation)
{
	if(operation=="inc")
	{
		if(numdom.attr("class")=="num empty"&&numdom.children("a").html()==""){
			numdom.children("a").html(1)
			numdom.attr("class","num")
		}
		else{
			numdom.children("a").html(Number(numdom.children("a").html())+1)
		}
	}
	else if(operation=="dec")
	{
		if(numdom.children("a").html()=="1"){
			numdom.children("a").html("")
			numdom.attr("class","num empty")
		}
		else{
			numdom.children("a").html(Number(numdom.children("a").html())-1)
		}
	}
}