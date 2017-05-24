

function scrollanimate(){
	var nowScrollTop = document.body.scrollTop;
		if(nowScrollTop>8)
		{
			$("#userpage>.pagecontent>#userinfo>.avatar").addClass("dispear")
		}
		else{
			$("#userpage>.pagecontent>#userinfo>.avatar").removeClass("dispear")
		}

		if(nowScrollTop>64)
		{
			$("#userpage>#topbar").addClass("active")
			$(".userbg").css("-webkit-filter","blur(5px)")
			// $("#headphoto").css("display","none")
		}
		else{
			$("#userpage>#topbar").removeClass("active")
			// $("#headphoto").css("display","block")
		}


		if(nowScrollTop>=0&&nowScrollTop<=64)
		{
			$(".userbg").css("-webkit-filter","blur(" + nowScrollTop/64*5+ "px)")
		}

}

window.addEventListener("scroll", function() {
	scrollanimate()
	if($("#userpage").height()==$(window).height()+document.body.scrollTop&&$(".pagelayout.focus").attr("id")=="userpage")
	{
		if(document.body.scrollTop==0)
			return
		loadmore()
	}
}, false);

function loadmore(){
	if(history.state.query[1]==0){
		return
	}

	var uid = history.state.uid
	var requests = history.state.query[0] + 1

	$.ajax({
		url:"/feed/personal?id=" + uid + "&page=" + requests,
		type:"get",
		data: false,
		async: false,
		processData:false,
		contentType:false,
		success:function(jsonback){			
			
			history.state.query[0] = history.state.query[0] + 1
			history.state.query[1] = jsonback.goon	
			history.replaceState(history.state,null,null)
			if(jsonback.html!="")
				$("#postflow>.flowbottom").before(jsonback.html)
			if(jsonback.goon==0)
				$("#postflow>.flowbottom").attr("class","flowbottom end")
		},
		error:function(e){
			if(e.status==401){
				toast("身份认证已过期，请重新登录");
			}
			else if(e.status==500){
				toast("服务器出错了");
			}
		}
	})
}

function statusrestore()
{
	if(history.state["query"][0]==0&&history.state["query"][1]==0){
		$("#postflow>.flowbottom").attr("class","flowbottom end")
		return
	}

	var uid = history.state.uid

	if(history.state.modify==1){
		usecache = false
	}
	else if(history.state.modify==0){
		usecache = true
	}

	history.state.modify = 0
	history.replaceState(history.state,null,null)

	for (var page = 1;page <= history.state["query"][0];page ++)
	{
		$.ajax({
			url:"/feed/personal?id=" + uid + "&page=" + page,
			type:"get",
			data: false,
			cache: usecache,
			async: false,
			processData:false,
			contentType:false,
			success:function(jsonback){
				if(jsonback.html!="")		
					$("#postflow>.flowbottom").before(jsonback.html)				
				if(jsonback.goon==0){
					$("#postflow>.flowbottom").attr("class","flowbottom end")
					history.state.query[0] = page
					history.state.query[1] = jsonback.goon
					history.replaceState(history.state,null,null)
				}
			},
			error:function(e){
				if(e.status==401){
					toast("身份认证已过期，请重新登录");
				}
				else if(e.status==500){
					toast("服务器出错了");
				}
			}
		})
	}
}

$("#topbar>.action#send").click(
	function(){
		var content
		if($("textarea#composetext").val().length>140){
			toast("最多只能写140字")
			return
		}
		else if($("textarea#composetext").val().length>0){
			content = $("textarea#composetext").val()
		}
		else{
			content = "转发微博"
		}

		var rid = history.state.pid
		var form = new FormData();
		form.append("rid", rid)
		form.append("content", content)

		$.ajax({
			url:"/api/posts/create",
			type:"post",
			data: form,
			async: true,
			processData:false,
			contentType:false,
			success:function(data){
				history.go(-1)
				adjustcounter($("[pid='" + rid + "']").children(".entry_actionbar").children(".action#repost").children(".num"),"inc")
				if(data!=""){
					$("#postflow>.counter").after(data)

					setTimeout(function(){
						history.state.modify = 1
						history.replaceState(history.state,null,null)
						$("body").scrollTop($("body").scrollTop()+$("#postflow>.onepost").eq(0).height()+11)
					},180)
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
					adjustcounter($("[pid='" + rid + "']").children(".entry_actionbar").children(".action#comment").children(".num"),"inc")
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
	}
)

function praiseoperation(action)
{
	var pid = action.parent().parent().attr("pid")
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
				
				adjustcounter(action.children(".num"),"dec")
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
				else if(e.statusText=="nonexistent weibo"){
					toast("该微博可能已被删除");
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
				
				adjustcounter(action.children(".num"),"inc")
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
				else if(e.statusText=="already praise"){
					toast("好像已经点过赞了呢");
					action.attr("class","action already")
				}

			}
		})
	}
}


$("#userinfo>.action").click(
	function(){
		var operation = $("#userinfo>.action").attr("id")
		var uid = history.state.uid
		if(operation=="edit")
		{
			window.location.href="/u/" + uid + "/edit"
		}
		else if(operation=="follow")
		{
			$.ajax({
			url:"/api/follows/add?id=" + uid,
			type:"post",
			data: false,
			async: true,
			processData:false,
			contentType:false,
			success:function(){	
				if($("#userinfo>.action").data("followu")==false)
					$("#userinfo>.action").attr("id","following")
				else if($("#userinfo>.action").data("followu")==true)
					$("#userinfo>.action").attr("id","mutual")
				toast("关注成功");
			},
			error:function(e){
				if(e.statusText=="already follow")
				{
					toast("已关注");
					if($("#userinfo>.action").data("followu")==false)
						$("#userinfo>.action").attr("id","following")
					else if($("#userinfo>.action").data("followu")==true)
						$("#userinfo>.action").attr("id","mutual")
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
		else if(operation=="following"||operation=="mutual")
		{
			$.ajax({
			url:"/api/follows/remove?id=" + uid,
			type:"post",
			data: false,
			async: true,
			processData:false,
			contentType:false,
			success:function(){			
				$("#userinfo>.action").attr("id","follow")
				toast("取消关注成功");
			},
			error:function(e){
				if(e.statusText=="not follow yet")
				{
					toast("未关注");
					$("#userinfo>.action").attr("id","follow")
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
)



window.onpopstate = function(event)
{
	// console.log('backtouch')
	if ($(".pagelayout#composepage").attr("class")=="pagelayout focus")
	{
		repostquit()
	}
}


$(document).ready(
function (){
	
	if(history.state==null){
		var status = {}
		status.page = "userpage"
		status.uid = window.location.href.slice(-10)
		status.query = [0,1]
		status.modify = 0
		history.replaceState(status,null,null)
		loadmore()
		// $(".pagelayout#userpage").attr("class", "pagelayout animate stayright");
		$(".pagelayout#userpage").attr("class", "pagelayout animate slideleft");
		setTimeout('$(".pagelayout#userpage").attr("class", "pagelayout focus")',180);
	}
	else
	{
		$(".pagelayout#userpage").attr("class", "pagelayout focus");
		if(history.state.page!="userpage")
		{
			history.go(-1)
		}
		statusrestore()
	}



});