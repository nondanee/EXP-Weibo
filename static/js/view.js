window.addEventListener("scroll", function() {
	scrollanimate()
}, false);

function scrollanimate()
{
	var nowScrollTop = document.body.scrollTop;
	var tabbarPosition = tabbaroffset - nowScrollTop
	if(nowScrollTop>54)
	{
		$("#topbar>.posterinfo").css("opacity","1")
	}
	else
	{
		$("#topbar>.posterinfo").css("opacity","0")
	}

	if(tabbarPosition>56)
	{
		$("#flowgroup").css("overflow","hidden")
	}
	else if(tabbarPosition==56)
	{	
		$("#flowgroup").css("overflow","auto")
	}
}

var composestatus = {}
var withpic = {}

window.onpopstate = function(event)
{
	console.log(history.state)

	if ($(".pagelayout#composepage").attr("class")=="pagelayout focus")
	{
		repostquit()
	}
	else if($(".pagelayout#commentpage").attr("class")=="pagelayout focus")
	{
		commentquit()
	}
	else if($(".pagelayout#optionspage").attr("class")=="pagelayout focus")
	{
		optionquit()
	}
}
$("#flowgroup").scroll(function(){

	if($("#flowgroup").height()==$("#flowgroup")[0].scrollHeight)
		return

	if($("#flowgroup").height()+$("#flowgroup").scrollTop()==$("#flowgroup")[0].scrollHeight)
	{
		loadmore(history.state.focus)
	}

});


$("#tabbar>.tab").click(function(){
	var current = $("#tabbar>.tab.active").attr("id")
	var target= $(this).attr("id")
	if( current==target )
		return

	history.state.focus = target
	history.replaceState(history.state,null,null)

	if($("#" + target + "flow").children(".one" + target).length == 0)
	{
		if(history.state[target + "s"][0] == 0&&history.state[target + "s"][1] == 1)
			loadmore(target)
	}

	$("#tabbar>.tab").attr("class","tab")
	$("#tabbar>.tab#" + target).attr("class","tab active")
	$(".detailflow").attr("class","detailflow")
	$(".detailflow#" + target + "flow").attr("class","detailflow active")
	$("#flowgroup").scrollTop(0)
});


function replyenter(onecomment)
{
	event.stopPropagation()

	history.state.page = "commentpage"
	history.pushState(history.state,null,null)

	var replyto = onecomment.children(".postinfo").children(".poster").html()
	var commenttext = onecomment.children(".postbody").children(".posttext").html()
	commenttext = commenttext.replace(/<[^>]+>/g,"")

	var replyinfo = "@" + replyto + ":" + commenttext
	var holdertext = "回复:@" + replyto

	$(".pagelayout#commentpage>#commentbox>#commenttext").val("")
	$(".pagelayout#commentpage>#commentbox>#replyto").html(replyinfo)


	$(".pagelayout").attr("class", "pagelayout unfocus")
	$(".pagelayout#detailpage").attr("class", "pagelayout under")
	$(".pagelayout#commentpage").attr("class", "pagelayout focus")
	$(".pagelayout#commentpage>#commentbox>#replyto").css("display","block")
	$(".pagelayout#commentpage>#commentbox>#commenttext").attr("placeholder",holdertext)
	$("body").addClass("locking")
	$(".pagelayout#commentpage>#commentbox>#commenttext").focus()

	commentwordcount()
}

function commententer()
{
	history.state.page = "commentpage"
	history.pushState(history.state,null,null)

	$(".pagelayout").attr("class", "pagelayout unfocus")
	$(".pagelayout#detailpage").attr("class", "pagelayout under")
	$(".pagelayout#commentpage").attr("class", "pagelayout focus")
	$(".pagelayout#commentpage>#commentbox>#replyto").css("display","none")
	$(".pagelayout#commentpage>#commentbox>#commenttext").attr("placeholder","添加评论...")
	$("body").addClass("locking")
	$(".pagelayout#commentpage>#commentbox>#commenttext").focus()

	commentwordcount()
}

function commentquit()
{
	if($(".pagelayout#commentpage>#commentbox>#replyto").css("display")=="block")
	{
		$(".pagelayout#commentpage>#commentbox>#commenttext").val("")
	}
	
	if($(".pagelayout#commentpage>#commentbox>#commenttext").val().length>0)
	{
		$("#bottombar>#addcomment>.text").addClass("save")
		$("#bottombar>#addcomment>.text").html($(".pagelayout#commentpage>#commentbox>#commenttext").val())
	}
	else
	{
		$("#bottombar>#addcomment>.text").removeClass("save")
		$("#bottombar>#addcomment>.text").html("添加评论...")
	}

	$("body").removeClass("locking")
	$(".pagelayout").attr("class", "pagelayout unfocus")
	$(".pagelayout#detailpage").attr("class", "pagelayout focus");
}



function loadmore(type)
{
	console.log("loadmore "+type)
	if(history.state[type + "s"][1]==0)
 		return

	var page = history.state[type + "s"][0] + 1
	var pid = history.state.pid

	$.ajax({
		url:"/api/" + type + "s/show?page=" + page + "&id=" + pid,
		type:"get",
		data: false,
		async: false,//false
		processData:false,
		contentType:false,
		success:function(jsonback){
			history.state[type + "s"][0] = history.state[type + "s"][0] + 1
			history.state[type + "s"][1] = jsonback.goon	
			history.replaceState(history.state,null,null)
			if(jsonback.html!="")
				$("#" + type + "flow>.flowbottom").before(jsonback.html)
			if(jsonback.goon==0)
				$("#" + type + "flow>.flowbottom").attr("class","flowbottom end")
		},
		error:function(e){
			if(e.status==500){
				toast("服务器出错了");
			}
		}
	})
}

function statusrestore(type)
{
	if(history.state[type + "s"][0]==0&&history.state[type + "s"][1]==0){
		$("#" + type + "flow>.flowbottom").attr("class","flowbottom end")
		return
	}

	var pid = history.state.pid

	for (var page = 1;page <= history.state[type + "s"][0];page ++)
	{
		console.log(type,page)
		$.ajax({
			url:"/api/" + type + "s/show?page=" + page + "&id=" + pid,
			type:"get",
			data: false,
			async: false,// true
			processData:false,
			contentType:false,
			success:function(jsonback){
				if(jsonback.html!="")
					$("#" + type + "flow>.flowbottom").before(jsonback.html)
				if(jsonback.goon==0){
					$("#" + type + "flow>.flowbottom").attr("class","flowbottom end")
					history.state[type + "s"][0] = page
					history.state[type + "s"][1] = 0
					history.replaceState(history.state,null,null)
				}
			},
			error:function(e){
				if(e.status==500){
					toast("服务器出错了");
				}
			}
		})
	}
}

function praiseoperation(action)
{
	var pid = history.state.pid
	var current = action.attr("class").slice(7)
	if(current=="already")
	{
		$.ajax({
			url:"/api/praises/destroy?id=" + pid,
			type:"post",
			data: false,
			async: true,
			processData:false,
			contentType:false,
			success:function(){
				$("#tabbar>.tab#praise>.num").html(Number($("#tabbar>.tab#praise>.num").html())-1)
				history.state["praises"] = [0,1]
				history.replaceState(history.state,null,null)
				$("#praiseflow>.onepraise").remove()
				$("#praiseflow>.flowbottom").attr("class","flowbottom goon")

				if(history.state.focus=="praise")
				{
					$("#flowgroup").scrollTop(0)
					loadmore("praise")
				}

				action.attr("class","action notyet animate")
				setTimeout(function(){
					action.attr("class","action notyet")
				},360)
			},
			error:function(e){
				if(e.status==401){
					toast("身份认证已过期，请重新登录");
				}
				else if(e.status==500){
					toast("服务器出错了");
				}
				else if(e.statusText=="not praise yet"){
					toast("之前好像并没有点过赞呢");
					action.attr("class","action notyet")
				}
			}
		})
		
	}
	else if(current=="notyet")
	{
		$.ajax({
			url:"/api/praises/create?id=" + pid,
			type:"post",
			data: false,
			async: true,
			processData:false,
			contentType:false,
			success:function(){
				$("#tabbar>.tab#praise>.num").html(Number($("#tabbar>.tab#praise>.num").html())+1)
				history.state["praises"] = [0,1]
				history.replaceState(history.state,null,null)
				$("#praiseflow>.onepraise").remove()
				$("#praiseflow>.flowbottom").attr("class","flowbottom goon")

				if(history.state.focus=="praise")
				{
					$("#flowgroup").scrollTop(0)
					loadmore("praise")
				}

				action.attr("class","action already animate")
				setTimeout(function(){
					action.attr("class","action already")
				},360)
			},
			error:function(e){
				if(e.status==401){
					toast("身份认证已过期，请重新登录");
				}
				else if(e.status==500){
					toast("服务器出错了");
				}
				else if(e.statusText=="nonexistent weibo"){
					toast("该微博可能已被删除");
				}
				else if(e.statusText=="already praise"){
					toast("好像已经点过赞了呢");
					action.attr("class","action already")
				}

			}
		})
	}
}

$(".comment_actionbar>.action#send").click(
	function(){

		var commenttext = $("textarea#commenttext").val().replace(/^\s+/g,"")
		commenttext = commenttext.replace(/^\s+/g,"")

		if(commenttext.length==0){
			return
		}

		if($("textarea#commenttext").attr("placeholder")!="添加评论..."){
			var prefix = $("textarea#commenttext").attr("placeholder").replace(/:/,"")
			var content = prefix + ":" + commenttext
		}
		else{
			var content = commenttext
		}

		if(content.length>140){
			toast("最多只能写140字")
			return
		}

		var form = new FormData();
		form.append("pid", history.state.pid)
		form.append("content", content)

		$.ajax({
			url:"/api/comments/create",
			type:"post",
			data: form,
			async: false,
			processData: false,
			contentType: false,
			success:function(data){	
				$("textarea#commenttext").val("")			
				history.go(-1)
				$("#tabbar>.tab#comment>.num").html(Number($("#tabbar>.tab#comment>.num").html()) + 1)
				history.state["comments"] = [0,1]
				history.replaceState(history.state,null,null)
				$("#commentflow>.onecomment").remove()
				$("#commentflow>.flowbottom").attr("class","flowbottom goon")

				if(history.state.focus=="comment")
				{
					$("#flowgroup").scrollTop(0)
					loadmore("comment")
				}
			},
			error:function(e){
				if(e.statusText=="nonexistent weibo"){
					toast("该微博可能已被删除");
				}
				else if(e.statusText=="contain sensitive words"){
					toast("内容包含敏感词");
				}
				else if(e.status==401){
					toast("身份认证已过期，请重新登录");
				}
				else if(e.status==500){
					toast("服务器出错了");
				}
			}
		})
})


$("#topbar>.action#send").click(
	function(){
		if($("textarea#composetext").val().length>0)
			var content = $("textarea#composetext").val()
		else
			var content = "转发微博"

		if(content.length>140){
			toast("最多只能写140字")
			return
		}

		var form = new FormData();
		form.append("rid", history.state.pid)
		form.append("content", content)

		$.ajax({
			url:"/api/posts/create",
			type:"post",
			data: form,
			async: true,
			processData:false,
			contentType:false,
			success:function(data){
				$("textarea#composetext").val("")
				history.go(-1)
				$("#tabbar>.tab#repost>.num").html(Number($("#tabbar>.tab#repost>.num").html()) + 1)

				history.state["reposts"] = [0,1]
				history.replaceState(history.state,null,null)
				$("#repostflow>.onerepost").remove()
				$("#repostflow>.flowbottom").attr("class","flowbottom goon")
				
				if(history.state.focus="repost")
				{
					$("#flowgroup").scrollTop(0)
					loadmore("repost")
				}

			},
			error:function(e){
				if(e.statusText=="nonexistent repost origin"){
					toast("该微博可能已被删除");
				}
				else if(e.statusText=="contain sensitive words"){
					toast("内容包含敏感词");
				}
				else if(e.status==401){
					toast("身份认证已过期，请重新登录");
				}
				else if(e.status==500){
					toast("服务器出错了");
				}
			}
		})

		if($("#checkradio").attr("class")=="selected")
		{
			var form = new FormData();
			form.append("pid", history.state.pid)
			form.append("content", content)

			$.ajax({
				url:"/api/comments/create",
				type:"post",
				data: form,
				async: true,
				processData:false,
				contentType:false,
				success:function(data){
					$("#tabbar>.tab#comment>.num").html(Number($("#tabbar>.tab#comment>.num").html()) + 1)
					history.state["comments"] = [0,1]
					history.replaceState(history.state,null,null)
					$("#commentflow>.onecomment").remove()
					$("#commentflow>.flowbottom").attr("class","flowbottom goon")
					if(history.state.focus="comment")
					{
						$("#flowgroup").scrollTop(0)
						loadmore("comment")
					}
				},
				error:function(e){
					if(e.statusText=="nonexistent weibo"){
						toast("该微博可能已被删除");
					}
					else if(e.statusText=="contain sensitive words"){
						toast("内容包含敏感词");
					}
					else if(e.status==401){
						toast("身份认证已过期，请重新登录");
					}
					else if(e.status==500){
						toast("服务器出错了");
					}
				}
			})
		}
		
})

$("#topbar>.action#more").click(
	function()
	{
		$(".pagelayout").attr("class", "pagelayout unfocus")
		$(".pagelayout").eq(0).attr("class", "pagelayout under") //mainpage

		history.state.page = "optionspage"
		history.pushState(history.state,null,null)

		$("body").addClass("locking")
		$(".pagelayout#optionspage").attr("class", "pagelayout focus");
	}
)


$(".pagelayout#optionspage").click(
	function()
	{
		history.go(-1)
	}
)

function optionoperation(option){
	event.stopPropagation()
	var type = option.attr("id")
	if(type=="follow")
	{
		var uid = option.attr("uid")
		$.ajax({
			url:"/api/follows/add?id=" + uid,
			type:"post",
			data: false,
			async: true,
			processData:false,
			contentType:false,
			success:function(){
				history.go(-1)
				toast("关注成功");
				setTimeout(function(){
					option.attr("id","following")
					option.children(".text").html("取消关注")
				},200)
			},
			error:function(e){
				history.go(-1)
				if(e.statusText=="already follow")
				{
					toast("已关注");
					setTimeout(function(){
						option.attr("id","following")
						option.children(".text").html("取消关注")
					},200)
				}
				else if(e.status==401){
					toast("身份认证已过期，请重新登录");
				}
				else if(e.status==500){
					toast("服务器出错了");
				}
			}
		})
	}
	else if(type=="following")
	{
		var uid = option.attr("uid")
		$.ajax({
			url:"/api/follows/remove?id=" + uid,
			type:"post",
			data: false,
			async: true,
			processData:false,
			contentType:false,
			success:function(){			
				history.go(-1)
				toast("取消关注成功");
				setTimeout(function(){
					option.attr("id","follow")
					option.children(".text").html("关注")
				},200)
			},
			error:function(e){
				history.go(-1)
				if(e.statusText=="not follow yet")
				{
					toast("未关注");
					setTimeout(function(){
						option.attr("id","follow")
						option.children(".text").html("关注")
					},200)
				}
				else if(e.status==401){
					toast("身份认证已过期，请重新登录");
				}
				else if(e.status==500){
					toast("服务器出错了");
				}
			}
		})
	}
	else if(type=="delete")
	{
		var pid = option.attr("pid")
		$.ajax({
			url:"/api/posts/destroy?id=" + pid,
			type:"post",
			data: false,
			async: true,
			processData:false,
			contentType:false,
			success:function(){			
				toast("已删除");
				setTimeout(function(){
					history.go(-2)
				},800)
			},
			error:function(e){
				if(e.statusText=="nonexistent weibo")
				{
					toast("好像已经删除了呢");
					setTimeout(function(){
						history.go(-2)
					},800)
				}
				else if(e.status==401){
					toast("身份认证已过期，请重新登录");
				}
				else if(e.status==500){
					toast("服务器出错了");
				}
			}
		})

	}
}

function optionquit(){
	$(".pagelayout#optionspage").attr("class", "pagelayout dispear");

	setTimeout(function(){
		$("body").removeClass("locking")
		$(".pagelayout").attr("class", "pagelayout unfocus")
		$(".pagelayout#detailpage").attr("class", "pagelayout focus");
	},200)
	
}
// window.onresize=function(){
// 	$(".detailflow").css("min-height",window.innerHeight-165)
// }

$(document).ready(
function (){

	$("#flowgroup").css("height",window.innerHeight-104)
	tabbaroffset = $("#tabbar").offset().top

	if(history.state==null){

		var status = {}
		status.page = "detailpage"
		status.pid = $(".onepost").eq(0).attr("pid")
		// status.pid = window.location.href.slice(-16)
		status.reposts = [0,1]
		status.comments = [0,1]
		status.praises = [0,1]
		status.focus = "comment"
		status.scroll = 0
		
		if($("#tabbar>.tab#repost>.num").html()=="0"){
			status.reposts[1] = 0
			$("#repostflow>.flowbottom").attr("class","flowbottom end")
		}
		if($("#tabbar>.tab#comment>.num").html()=="0"){
			status.comments[1] = 0
			$("#commentflow>.flowbottom").attr("class","flowbottom end")
		}
		if($("#tabbar>.tab#praise>.num").html()=="0"){
			console.log($("#tabbar>.tab#praise>.num").html())
			status.praises[1] = 0
			$("#praiseflow>.flowbottom").attr("class","flowbottom end")
		}

		history.replaceState(status,null,null)
		loadmore("comment")

		
		// $(".pagelayout#detailpage").attr("class", "pagelayout animate stayright");
		$(".pagelayout#detailpage").attr("class", "pagelayout animate slideleft");
		setTimeout(function(){
			$(".pagelayout#detailpage").attr("class", "pagelayout focus")
			if(window.location.href.search(/\?action=comment/)!=-1)
			{
				commententer()
				var removeaction = window.location.href.replace(/\?action=comment/,"")
				history.replaceState(history.state,null,removeaction)
			}
		},180);
	}
	else
	{
		$(".pagelayout#detailpage").attr("class", "pagelayout focus");
		if(history.state.page!="detailpage")
		{
			history.go(-1)
		}
		// console.log(history.state)
		var activetab = history.state.focus
		$("#tabbar>.tab").attr("class","tab")
		$("#tabbar>.tab#" + activetab).attr("class","tab active")
		$(".detailflow").attr("class","detailflow")
		$(".detailflow#" + activetab + "flow").attr("class","detailflow active")

		var reserved = history.state[activetab + "s"]
		history.state["praises"] = [0,1]
		history.state["reposts"] = [0,1]
		history.state["comments"] = [0,1]
		if($("#tabbar>.tab#repost>.num").html()=="0"){
			history.state["reposts"] = [0,0]
			$("#repostflow>.flowbottom").attr("class","flowbottom end")
		}
		if($("#tabbar>.tab#comment>.num").html()=="0"){
			history.state["comments"] = [0,0]
			$("#commentflow>.flowbottom").attr("class","flowbottom end")
		}
		if($("#tabbar>.tab#praise>.num").html()=="0"){
			history.state["praises"] = [0,0]
			$("#praiseflow>.flowbottom").attr("class","flowbottom end")
		}

		history.state[activetab + "s"] = reserved
		history.replaceState(history.state,null,null)
		statusrestore(activetab)
		$("#flowgroup").scrollTop(history.state.scroll)
	}

});




window.onbeforeunload = function(){
	history.state.scroll = $("#flowgroup").scrollTop()
	history.replaceState(history.state,null,null)
	if(history.state.page=="repostpage"||history.state.page=="commentpage"){
		return "onbeforeunload is work";
	}
}