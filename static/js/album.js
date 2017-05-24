window.addEventListener("scroll", function() {
	if($("#albumpage").height()==$(window).height()+document.body.scrollTop)
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
	var page = history.state.query[0] + 1
	var uid = history.state.uid
	$.ajax({
		url:"/p/album?page=" + page + "&id=" + uid,
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
				$("#photoflow>.flowbottom").before(jsonback.html)
			if(jsonback.goon==0)
				$("#photoflow>.flowbottom").attr("class","flowbottom end")
		},
		error:function(e){
			if(e.status==500){
				toast("服务器出错了");
			}
		}
	})
}

function statusrestore()
{
	if(history.state["query"][0]==0&&history.state["query"][1]==0){
		$("#photoflow>.flowbottom").attr("class","flowbottom end")
		return
	}
	var uid = history.state.uid
	for (var page = 1;page <= history.state["query"][0];page ++)
	{
		$.ajax({
			url:"/p/album?page=" + page + "&id=" + uid,
			type:"get",
			data: false,
			async: false,
			processData:false,
			contentType:false,
			success:function(jsonback){
				if(jsonback.html!="")		
					$("#photoflow>.flowbottom").before(jsonback.html)				
				if(jsonback.goon==0){
					$("#photoflow>.flowbottom").attr("class","flowbottom end")
					history.state.query[1] = jsonback.goon
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

$(document).ready(
function (){
	
	if(history.state==null){
		var status = {}
		status.page = "albumpage"
		status.query = [0,1]
		status.uid = window.location.href.match(/\/u\/(\d{10})/g)[0].slice(3)
		history.replaceState(status,null,null)
		while($(window).height()-56>$("#photoflow").height()&&history.state.query[1]==1){
			loadmore()
		}

		// $(".pagelayout#userpage").attr("class", "pagelayout animate stayright");
		$(".pagelayout#albumpage").attr("class", "pagelayout animate slideleft");
		setTimeout('$(".pagelayout#albumpage").attr("class", "pagelayout focus")',180);
	}
	else
	{
		$(".pagelayout#albumpage").attr("class", "pagelayout focus");
		statusrestore()
	}

});