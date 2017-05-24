scroll(function(direction) {
	if(direction=="down")
	{
		document.getElementById("topbar").className="hide";
		document.getElementById("fab").className="action hide";
	}
	else if(direction=="up"){
		document.getElementById("topbar").className="";
		document.getElementById("fab").className="action";
	}

});	
function scroll( fn ) {
	var beforeScrollTop = document.body.scrollTop,
		fn = fn || function() {};
	window.addEventListener("scroll", function() {
		var afterScrollTop = document.body.scrollTop,
		delta = afterScrollTop - beforeScrollTop;
		if( Math.abs(delta) < 18 ) return false;
		// if( delta === 0 ) return false;
		fn( delta > 0 ? "down" : "up" );
		beforeScrollTop = afterScrollTop;
	}, false);
}

window.addEventListener("scroll", function() {
	if($("#indexpage").height()==$(window).height()+document.body.scrollTop&&$(".pagelayout.focus").attr("id")=="indexpage")
	{
		loadmore()
	}
}, false);

function touch(){
	var startx;
	var endx;
	var offsetx;
	var el_navigation = document.getElementById('navigation');
	var el_drawer = document.getElementById('drawer');
	function cons(){


		if(Math.abs(startx-endx)<12&&startx<280)
			return

		var finalposition = Number(el_drawer.style.transform.slice(11,-3))

		if(finalposition>-140){
			el_navigation.className="active animate";
			el_drawer.style.transform="translateX(0px)";
			el_navigation.style.backgroundColor="rgba(0,0,0,0.6)"
			setTimeout(function(){
		 		el_navigation.className="active";
		 	},240)
		}
		else if(finalposition<=-140){
			el_navigation.className="active animate";
		 	el_drawer.style.transform="translateX(-280px)";
		 	el_navigation.style.backgroundColor="rgba(0,0,0,0)"
		 	setTimeout(function(){
		 		el_navigation.className="hidden";
		 		document.body.className="";
		 	},240)
		}

		if(Math.abs(startx-endx)<8&&startx>300)
		{
			el_navigation.className="active animate";
		 	el_drawer.style.transform="translateX(-280px)";
		 	el_navigation.style.backgroundColor="rgba(0,0,0,0)"
		 	setTimeout(function(){
		 		el_navigation.className="hidden";
		 		document.body.className="";
		 	},240)
		}

	}
	el_navigation.addEventListener('touchstart',function(e){
		startx = e.targetTouches[0].pageX;
		starty = e.targetTouches[0].pageY;
		if(el_drawer.style.transform=="")
		{
			offsetx = -280;
		}
		else
		{
			offsetx = Number(el_drawer.style.transform.slice(11,-3))
		}
	});
	el_navigation.addEventListener('touchmove',function(e){

		if(startx<=24&&e.changedTouches[0].pageX -startx>24){
			el_navigation.className="active";
			document.body.className="locking";
		}

		if((offsetx + e.changedTouches[0].pageX - startx <=0)){
			el_drawer.style.transform="translateX("+(offsetx + e.changedTouches[0].pageX - startx)+"px)"
			el_navigation.style.backgroundColor="rgba(0,0,0,"+ (offsetx + e.changedTouches[0].pageX - startx + 280)/466 +")"
		}
	});
	el_navigation.addEventListener('touchend',function(e){
		endx = e.changedTouches[0].pageX;
		cons();
	});
}


function opendrawer()
{
	document.body.className="locking";
	document.getElementById('navigation').className="active animate";
	document.getElementById('drawer').style.transform="translateX(0px)";
	document.getElementById('navigation').style.backgroundColor="rgba(0,0,0,0.6)"
	setTimeout(function(){
 		document.getElementById('navigation').className="active";
 	},240)
}

$(".compose_actionbar>.action#camera>form>input").on("change",
	function () {
		if($("#composeimageset").children(".composeimage").length>=9)
		{
			toast("最多只能传9张");
			$(this).parent()[0].reset();
			return;
		}

		var filepath = this.files[0].name;
		var extStart = filepath.lastIndexOf(".");
		var ext = filepath.substring(extStart, filepath.length).toUpperCase();
		if (ext != ".PNG" && ext != ".GIF" && ext != ".JPG" && ext != ".JPEG"){
			toast("只支持正经的图片格式");
			$(this).parent()[0].reset();
			return;
		}

		var size = this.files[0].size;
		if (size/1048576 > 2){
			toast("图片太大无法上传");
			$(this).parent()[0].reset();
			return;
		}

		var form = new FormData(document.getElementById("uploadimages"));
		$.ajax({
			url:"/api/images/upload?type=compose",
			type:"post",
			data: form,
			async: false,
			processData:false,
			contentType:false,
			success:function(jsonback){
				// console.log(jsonback)
				
				$("#composeimageset").append('<div class="composeimage"><div class="remove" onclick="$(this).parent().remove()"></div></div>')
				var selecteddom = $("#composeimageset").children(".composeimage").eq(-1)

				selecteddom.css("background-image","url(" + jsonback.thumbnail + ")")
				selecteddom.data('thumbnail',jsonback.thumbnail)
				selecteddom.data('original',jsonback.original)
				selecteddom.data('size',jsonback.size)
				document.getElementById("uploadimages").reset()
			},
			error:function(e){
				if(e.status==401){
					toast("身份认证已过期，请重新登录");
				}
				else if(e.status==500){
					toast("服务器出错了");
				}
			}
		});
})


$("#topbar>.action#send").click(
	function(){
		if(history.state.page=="repostpage")
		{
			var content
			if($("textarea#composetext").val().length>0){
				content = $("textarea#composetext").val()
			}
			else{
				content = "转发微博"
			}

			if(content.length>140){
				toast("最多只能写140字")
				return
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
					$("#postflow").prepend(data)

					setTimeout(function(){
						history.state.modify = 1
						history.replaceState(history.state,null,null)
						$("body").scrollTop($("body").scrollTop()+$("#postflow>.onepost").eq(0).height()+11)
					},180)
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
		else if(history.state.page=="composepage")
		{
			if($("textarea#composetext").val().length>140){
				toast("最多只能写140字")
				return
			}
			if($("textarea#composetext").val().length>0){
				var content = $("textarea#composetext").val()
			}
			else{
				return
			}

			var form = new FormData();
			form.append("content", content)

			if($("#composeimageset").children(".composeimage").length>0)
			{
				var withpic = []
				for(var i=0;i<$("#composeimageset").children(".composeimage").length;i++)
				{
					var onepic = {}
					onepic["thumbnail"] = $("#composeimageset").children(".composeimage").eq(i).data('thumbnail')
					onepic["size"] = $("#composeimageset").children(".composeimage").eq(i).data('size')
					onepic["original"] = $("#composeimageset").children(".composeimage").eq(i).data('original')
					withpic.push(onepic)
				}
				form.append("withpic", JSON.stringify(withpic))
			}

			console.log(withpic)

			$.ajax({
				url:"/api/posts/create",
				type:"post",
				data: form,
				async: true,
				processData:false,
				contentType:false,
				success:function(data){
					history.go(-1)
					$("#postflow").prepend(data)

					setTimeout(function(){
						history.state.modify = 1
						history.replaceState(history.state,null,null)
						$("textarea#composetext").val("")
						$("#composeimageset").empty()
						$("body").scrollTop($("body").scrollTop()+$("#postflow>.onepost").eq(0).height()+11)
					},800)
				},
				error:function(e){
					if(e.status==401){
						toast("身份认证已过期，请重新登录");
					}
					else if(e.statusText=="contain sensitive words"){
						toast("内容包含敏感词");
					}
					else if(e.status==500){
						toast("服务器出错了");
					}
				}
			})
		}
})


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


function loadmore(){
	if(history.state.query[1]==0){
		return
	}
	var page = history.state.query[0] + 1

	$.ajax({
		url:"/feed/index?page=" + page,
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
		$("#" + type + "flow>.flowbottom").attr("class","flowbottom end")
		return
	}

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
			url:"/feed/index?page=" + page,
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
					history.state.query[1] = 0
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

function changetheme()
{
	var current = $("#drawer>.list#nightmode>.switcher").attr("class").slice(9)
	var exp = new Date();
	exp.setTime(exp.getTime() + 365*24*60*60*1000);
	if(current=="day"){
		document.cookie = "THEME="+ escape ("NIGHT") + ";expires=" + exp.toGMTString();
		$("#drawer>.list#nightmode>.switcher").attr("class","switcher night")
	}
	else if(current=="night"){
		document.cookie = "THEME="+ escape ("DAY") + ";expires=" + exp.toGMTString();
		$("#drawer>.list#nightmode>.switcher").attr("class","switcher day")
	}
	window.location.reload(true)
}


function checktheme()
{
	if (document.cookie.length>0){
		startindex = document.cookie.indexOf("THEME=")
		if (startindex!=-1){
			endindex = document.cookie.indexOf(";",startindex+6)
			if (endindex == -1){
				endindex = document.cookie.length
			}
			var theme = unescape(document.cookie.substring(startindex + 6,endindex))
			if(theme == "DAY"){
				$("#drawer>.list#nightmode>.switcher").attr("class","switcher day")
			}
			else if(theme == "NIGHT"){
				$("#drawer>.list#nightmode>.switcher").attr("class","switcher night")
			}
		}
	}
}



window.onpopstate = function()
{
	if ($(".pagelayout#composepage").attr("class")=="pagelayout focus")
	{
		if($("#originview").css("display")=="block")
			repostquit()
		else
			composequit()
	}
}

$(document).ready(
	function (){
		touch()
		checktheme()
		if(history.state==null){
			var status = {}
			status.page = "indexpage"
			status.query = [0,1]
			status.modify = 0
			history.replaceState(status,null,null)
			loadmore()
		}
		else
		{
			if(history.state.page!="indexpage")
			{
				history.go(-1)
			}
			statusrestore()
			
		}
})
// window.onbeforeunload = function(){
// 	history.state.scroll = document.body.scrollTop
// 	history.replaceState(history.state,null,null)
// 	// return "onbeforeunload is work";
// }