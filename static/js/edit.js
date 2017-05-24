
$("#editpage>#topbar>.action#edit").click(
	function(){
		if($(this).children(".text").html()=="修改")
		{
			$(".nickname>.text").attr("contenteditable","true")
			$(".introduction>.text").attr("contenteditable","true")
			$(".nickname>.text").css("color","#006fcc")
			$(".introduction>.text").css("color","#006fcc")
			$(this).children(".text").html("完成")
		}
		else if($(this).children(".text").html()=="完成")
		{
			if($(".nickname>.text").html().length==0)
			{
				toast("昵称必须有")
				return
			}
			if($(".introduction>.text").html().length==0)
			{
				toast("写点介绍呗")
				return
			}
			
			var formData = new FormData();

			if($(".nickname>.text").data("original")!=$(".nickname>.text").html())
			{
				formData.append("nickname", $(".nickname>.text").html());
			}
			if($(".introduction>.text").data("original")!=$(".introduction>.text").html())
			{
				formData.append("introduction", $(".introduction>.text").html());
			}
			if($(".nickname>.text").data("original")==$(".nickname>.text").html()&&$(".introduction>.text").data("original")==$(".introduction>.text").html())
			{
				// console.log("no modify")
				history.go(-1)
			}

			$.ajax('/api/info/set', 
			{
				method: "POST",
				data: formData,
				processData: false,
				contentType: false,
				success: function () {
					toast("修改成功")
					setTimeout(function(){
						window.location.reload(true)
					},800)
				},
				error: function (e) {
					if(e.status==401){
						toast("身份认证已过期，请重新登录");
					}
					else if(e.status==500){
						toast("服务器出错了");
					}
					else if(e.statusText=="nickname has been used"){
						toast("昵称被使用了");
					}		
				}
			});
		}
	}
)
$("#userbg>input").on("change",function () { 

	if(this.files[0])
	{
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

		var formData = new FormData(document.getElementById("userbg"));
		$(this).parent()[0].reset()

		toast("正在上传");
		$.ajax('/api/images/upload?type=userbg', {
				method: "POST",
				data: formData,
				processData: false,
				contentType: false,
				success: function () {
					toast("修改成功")
					history.go(-1)
					setTimeout(function(){
						window.location.reload(true)
					},800)
				},
				error: function (e) {
					if(e.status==401){
						toast("身份认证已过期，请重新登录");
					}
					else if(e.status==500){
						toast("服务器出错了");
					}			
				}
			});

	}

})


$("#avatar>input").on("change",function () { 

	if(this.files[0])
	{
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

		var imgurl = window.URL.createObjectURL(this.files[0]);
		$(this).parent()[0].reset();

		var $image = $(".img-container>img");  
		$image.attr("src",imgurl);      
		$image.on("load", function() {

			history.state.page = "cutpage"
			history.pushState(history.state,null,null)

			$(".pagelayout").attr("class", "pagelayout unfocus")
			$(".pagelayout").eq(0).attr("class", "pagelayout under")
			$("body").addClass("locking")
			$(".pagelayout#cutpage").attr("class", "pagelayout staymiddle");
			$(".pagelayout#cutpage").attr("class", "pagelayout animate slidetop");


			setTimeout(function(){
				$(".pagelayout#cutpage").attr("class", "pagelayout focus")
				$(".pagelayout").eq(0).attr("class", "pagelayout unfocus")
			},180);

			$image.cropper({  
				aspectRatio: 1 / 1,// 1：1的比例进行裁剪，可以是任意比例，自己调整  
				background: false,

				resizable:false,
				center:false,
				highlight: false,
				viewMode: 1,
				dragMode: 'move',
				rotatable: false,
				cropBoxMovable:false,
				cropBoxResizable:false,
				autoCropArea: 0.86
			});  
		})

	}

})

$("#cutpage>#topbar>.action#edit").click(
	function(){
		$(".img-container>img").cropper('getCroppedCanvas').toBlob(function (blob) {

			var formData = new FormData();
			formData.append('croppedImage', blob);

			$.ajax('/api/images/upload?type=avatar', {
				method: "POST",
				data: formData,
				processData: false,
				contentType: false,
				success: function () {
					toast("修改成功")
					history.go(-1)
					setTimeout(function(){
						window.location.reload(true)
					},800)
				},
				error: function (e) {
					if(e.status==401){
						toast("身份认证已过期，请重新登录");
					}
					else if(e.status==500){
						toast("服务器出错了");
					}			
				}
			});
		});
	})


$(document).ready(
function (){
	
	if(history.state==null){
		var status = {}
		status.page = "editpage"
		status.uid = window.location.href.slice(-10)
		history.replaceState(status,null,null)

		// $(".pagelayout#userpage").attr("class", "pagelayout animate stayright");
		$(".pagelayout#editpage").attr("class", "pagelayout animate slideleft");
		setTimeout('$(".pagelayout#editpage").attr("class", "pagelayout focus")',180);
	}
	else
	{
		$(".pagelayout#editpage").attr("class", "pagelayout focus");
		if(history.state.page!="editpage")
		{
			history.go(-1)
		}
	}

});

function cutquit(){
	$(".pagelayout").eq(0).attr("class", "pagelayout under") //mainpage
	$(".pagelayout#cutpage").attr("class", "pagelayout staytop");
	$(".pagelayout#cutpage").attr("class", "pagelayout animate slidemiddle");
	setTimeout(function(){
		$("body").removeClass("locking")
		$(".img-container>img").cropper('destroy')
		$(".pagelayout").attr("class", "pagelayout unfocus");
		$(".pagelayout").eq(0).attr("class", "pagelayout focus"); //mainpage
	},180)
}

window.onpopstate = function(event)
{
	// console.log(history.state)
	if ($(".pagelayout#cutpage").attr("class")=="pagelayout focus")
	{
		cutquit()
	}
}