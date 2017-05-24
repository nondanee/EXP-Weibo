window.addEventListener("scroll", function() {
	if($("#listpage").height()==$(window).height()+document.body.scrollTop)
	{
		if(document.body.scrollTop==0)
			return
		loadmore()
	}
}, false);


$(document).ready(
function (){
	
	if(history.state==null){
		var status = {}
		if($("#topbar>.title").html()=="关注")
			status.page = "followpage"
		else if($("#topbar>.title").html()=="粉丝")
			status.page = "fanpage"
		status.uid = window.location.href.match(/\/u\/(\d{10})/g)[0].slice(3)
		status.query = [0,1]
		history.replaceState(status,null,null)
		loadmore()

		// $(".pagelayout#userpage").attr("class", "pagelayout animate stayright");
		$(".pagelayout#listpage").attr("class", "pagelayout animate slideleft");
		setTimeout('$(".pagelayout#listpage").attr("class", "pagelayout focus")',180);
	}
	else
	{
		$(".pagelayout#listpage").attr("class", "pagelayout focus");
		statusrestore()
	}

});

function followoperation(action){
	event.stopPropagation()
	var type = action.attr("id")
	var uid = action.parent().attr("uid")

	// console.log(uid)
	// console.log(type)

	// console.log(action.data("followu"))
	// console.log(action.attr("id"))

	if(type=="follow")
	{
		$.ajax({
			url:"/api/follows/add?id=" + uid,
			type:"post",
			data: false,
			async: true,
			processData:false,
			contentType:false,
			success:function(){
				if(action.data("followu")==false)
					action.attr("id","following")
				else if(action.data("followu")==true)
					action.attr("id","mutual")
				toast("关注成功");
			},
			error:function(e){
				if(e.statusText=="already follow")
				{
					toast("已关注");
					if(action.data("followu")==false)
						action.attr("id","following")
					else if(action.data("followu")==true)
						action.attr("id","mutual")
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
	else if(type=="following"||type=="mutual")
	{
		$.ajax({
			url:"/api/follows/remove?id=" + uid,
			type:"post",
			data: false,
			async: true,
			processData:false,
			contentType:false,
			success:function(){
				action.attr("id","follow")
				toast("关注成功");
			},
			error:function(e){
				if(e.statusText=="already follow")
				{
					toast("已关注");
					action.attr("id","follow")
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


function loadmore(){
	if(history.state.query[1]==0){
		return
	}
	var page = history.state.query[0] + 1

	if(history.state.page == "followpage")
		var type = "follows"

	else if(history.state.page == "fanpage")
		var type = "fans"

	var uid = history.state.uid
	var page = history.state.query[0] + 1

	$.ajax({
		url:"/p/" + type + "?id=" + uid + "&page=" + page,
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
				$("#userflow>.flowbottom").before(jsonback.html)
			if(jsonback.goon==0)
				$("#userflow>.flowbottom").attr("class","flowbottom end")
		},
		error:function(e){
			if(e.status==500){
				toast("服务器出错了");
			}
		}
	})
}


function statusrestore(){

	var uid = history.state.uid

	if(history.state.page == "followpage")
		var type = "follows"

	else if(history.state.page == "fanpage")
		var type = "fans"

	for (var page = 1;page <= history.state["query"][0];page ++)
	{
		$.ajax({
			url:"/p/" + type + "?id=" + uid + "&page=" + page,
			type:"get",
			data: false,
			async: false,// true
			processData:false,
			contentType:false,
			success:function(jsonback){
				if(jsonback.html!="")
					$("#userflow>.flowbottom").before(jsonback.html)
				if(jsonback.goon==0){
					$("#userflow>.flowbottom").attr("class","flowbottom end")
					history.state["query"][0] = page
					history.state["query"][1] = 0
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