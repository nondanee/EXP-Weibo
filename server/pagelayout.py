
indexpage='''<!DOCTYPE html>
<html>
	<head>
		<link href="/favicon.ico" rel="shortcut icon">
		<meta name="mobile-web-app-capable" content="yes">
		<meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>
		<meta name="theme-color" content="#ffffff">
		<link rel="icon" sizes="256x256" href="/weibo-launcher.png">
		<meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=0">
		<link rel="stylesheet" type="text/css" href="whole.css">
		<link rel="stylesheet" type="text/css" href="preloader-28.css">
		<link rel="stylesheet" href="photoswipe.css"> 
		<link rel="stylesheet" href="default-skin/default-skin.css">
		<title>EXP-Weibo</title>
	</head>
	<body>
	<div id="toast"><div class="text"></div></div>
	<div id="cover"></div>
	<div class="pagelayout focus" id="indexpage">
		<div id="navigation" class="hidden">
			<div id="drawer">
				<div class="windows" style="background-image:url(/photo/{userid}/userbg.jpg)">
					<div class="avatar" style="background-image:url(/photo/{userid}/avatar.jpg)"></div>
					<div class="nickname">{nickname}</div>
				</div>
				<div class="list" id="personal" onclick="window.location.href='/u/{userid}'">
					<div class="icon"></div>
					<a>个人</a>
				</div>
				<div class="list" id="collection">
					<div class="icon"></div>
					<a>收藏</a>
				</div>
				<div class="list" id="nightmode" onclick="changetheme()">
					<div class="icon"></div>
					<a>夜间模式</a>
					<div class="switcher day"></div>
				</div>
				<div class="list" id="exit" onclick="window.location.href='/signout'">
					<div class="icon"></div>
					<a>退出</a>
				</div>
			</div>
		</div>
		<div id="topbar">
			<div class="action" id="menu" onclick="opendrawer()">
				<div class="icon"></div>
				<div class="spark"><div class="ripple"></div></div>
			</div>
			<div class="action false" id="search">
				<div class="icon"></div>
				<div class="spark"><div class="ripple"></div></div>
			</div>
			<div class="title">全部</div>
		</div>
		<div id="postflow">
			<div class="flowbottom goon">
				<div class="endinfo">没有更多内容</div>
				<div class="md-preloader"><svg xmlns="http://www.w3.org/2000/svg" version="1.1" height="28" width="28" viewbox="0 0 28 28"><circle cx="14" cy="14" r="12.5" stroke-width="3"/></svg></div>
			</div>
		</div>
		<div class="action" id="fab" onclick="composeenter()">
			<div class="icon"></div>
			<div class="spark"><div class="ripple"></div></div>
		</div>
	</div>
	<div class="pagelayout unfocus" id="composepage">{composepage}
	</div>{photoswipe_viewer}
	</body>
	<script src="https://cdn.bootcss.com/zepto/1.2.0/zepto.js"></script>
	<script src="/photoswipe.min.js"></script> 
	<script src="/photoswipe-ui-default.min.js"></script>
	<script src="/utility.js"></script>
	<script src="/index.js"></script> 
</html>'''


userpage='''<!DOCTYPE html>
<html>
	<head>
		<link href="/favicon.ico" rel="shortcut icon">
		<meta name="mobile-web-app-capable" content="yes">
		<meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>
		<meta name="theme-color" content="#ffffff">
		<meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=0">
		<title>首页</title>
		<link rel="stylesheet" href="/preloader-28.css">
		<link rel="stylesheet" href="/photoswipe.css"> 
		<link rel="stylesheet" href="/default-skin/default-skin.css">
		<link rel="stylesheet" href="/whole.css">
	</head>
	<body>
	<div id="toast"><div class="text"></div></div>
	<div class="pagelayout stayright" id="userpage">
		<div id="topbar">
			<div class="action" id="back" onclick="history.go(-1)">
				<div class="icon white"></div>
				<div class="spark"><div class="ripple"></div></div>
			</div>
			<div class="action false" id="more">
				<div class="icon white"></div>
				<div class="spark"><div class="ripple"></div></div>
			</div>
			<div class="userinfo">
				<div class="nickname">{nickname}</div>
				<div class="counter">{posts_count} 微博</div>
			</div>
			<div class="userbg" style="background-image:url(/photo/{uid}/userbg.jpg)"><div class="greycover"></div></div>
			<div class="bgnoblur" style="background-image:url(/photo/{uid}/userbg.jpg)"><div class="greycover"></div></div>
		</div>

		<div id="headphoto">
			<div class="userbg" style="background-image:url(/photo/{uid}/userbg.jpg)"><div class="greycover"></div></div>
			<div class="bgnoblur" style="background-image:url(/photo/{uid}/userbg.jpg)"><div class="greycover"></div></div>
		</div>
		<div class="pagecontent">

		<div id="userinfo">
			<div class="avatar" style="background-image:url(/photo/{uid}/avatar.jpg)"></div>
			<div class="action" id="{actiontype}" data-followu="{followu}">
				<div class="icon"></div>
			</div>
			<div class="nickname">{nickname}</div>
			<div class="introduction">个人简介: {introduction}</div>
			<div class="status">
				<div class="follow" onclick="window.location.href='/u/{uid}/follow'"><a class="num">{follows_count}</a>关注</div>
				<div class="fan" onclick="window.location.href='/u/{uid}/fan'"><a class="num">{fans_count}</a>粉丝</div>
			</div>
		</div>
		<div id="album" onclick="window.location.href='/u/{uid}/photo'">{album}
		</div>
		<div id="postflow">
			<div class="counter">全部微博 · {posts_count}</div>
			<div class="flowbottom goon">
				<div class="endinfo">没有更多内容</div>
				<div class="md-preloader"><svg xmlns="http://www.w3.org/2000/svg" version="1.1" height="28" width="28" viewbox="0 0 28 28"><circle cx="14" cy="14" r="12.5" stroke-width="3"/></svg></div>
			</div>
		</div>
		</div>
	</div>		
	<div class="pagelayout unfocus" id="composepage">{composepage}
	</div>{photoswipe_viewer}
	</body>
	<script src="https://cdn.bootcss.com/zepto/1.2.0/zepto.js"></script>
	<script src="/photoswipe.min.js"></script>
	<script src="/utility.js"></script> 
	<script src="/photoswipe-ui-default.min.js"></script> 
	<script src="/user.js"></script>
</html>'''

album='''
			<a>相册</a>
			<div class="view" style="background-image: url(%s)"></div>
			<div class="view" style="background-image: url(%s)"></div>
			<div class="view" style="background-image: url(%s)"></div>
			<div class="view" style="background-image: url(%s)"></div>
			<div class="view" style="background-image: url(%s)"><div class="more"><a>···</a></div></div>'''


viewpage='''<!DOCTYPE html>
<html>
	<head>
		<link href="/favicon.ico" rel="shortcut icon">
		<meta name="mobile-web-app-capable" content="yes">
		<meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>
		<meta name="theme-color" content="#ffffff">
		<meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=0">
		<title>EXP-weibo</title>
		<link rel="stylesheet" type="text/css" href="/preloader-26.css">
		<link rel="stylesheet" href="/photoswipe.css"> 
		<link rel="stylesheet" href="/default-skin/default-skin.css">
		<link rel="stylesheet" href="/whole.css">
		<style type="text/css">
		</style>
	</head>
	<body>
	<div id="toast"><div class="text"></div></div>
	<div class="pagelayout stayright" id="detailpage">{detailpage}
	</div>
	<div class="pagelayout unfocus" id="commentpage">{commentpage}
	</div>
	<div class="pagelayout unfocus" id="composepage">{composepage}
	</div>
	<div class="pagelayout unfocus" id="optionspage">
		<div id="optionsmenu">{options}
		</div>
	</div>{photoswipe_viewer}
	<script src="https://cdn.bootcss.com/zepto/1.2.0/zepto.js"></script>
	<script src="/photoswipe.min.js"></script> 
	<script src="/photoswipe-ui-default.min.js"></script> 
	<script src="/utility.js"></script> 
	<script src="/view.js"></script> 
</body>
</html>'''



oneoption='''
			<div class="option" id="{optiontype}" {optionvalue} onclick="optionoperation($(this))">
				<div class="icon"></div>
				<div class="text">{optiontext}</div>
			</div>'''

detailpage='''
		<div id="topbar">
			<div class="action" id="back" onclick="history.back()">
				<div class="icon"></div>
				<div class="spark"><div class="ripple"></div></div>
			</div>
			<div class="action" id="more">
				<div class="icon"></div>
				<div class="spark"><div class="ripple"></div></div>
			</div>
			<div class="posterinfo">
				<div class="avatar" style="background-image:url(/photo/{uid}/avatar.jpg)"></div>
				<div class="poster"><a>{nickname}</a></div>
			</div>
		</div>
		<div class="onepost" pid={pid}>	
			<div class="postinfo" onclick="window.location.href='/u/{uid}'">
				<div class="avatar" style="background-image:url(/photo/{uid}/avatar.jpg)"></div>
				<div class="poster">{nickname}</div>
				<div class="from"><a class="time">{posttime}</a>来自 <a class="source">{device}</a></div>
			</div>
			<div class="postbody">
				<p class="posttext">{posttext}</p>
				{gallery}
			</div>{repostbody}	
			<div class="entry_actionbar">
				<div class="action {praisestatus}" id="praise" onclick="praiseoperation($(this))">
					<div class="icon" ></div>
					<div class="spark"><div class="ripple"></div></div>
				</div>
				<div class="action" id="comment" onclick="commententer()">
					<div class="icon"></div>
					<div class="spark"><div class="ripple"></div></div>
				</div>
				<div class="action" id="repost" onclick="repostenter($(this))">
					<div class="icon"></div>
					<div class="spark"><div class="ripple"></div></div>
				</div>
				<div class="action" id="share">
					<div class="icon"></div>
					<div class="spark"><div class="ripple"></div></div>
				</div>
			</div>
		</div>
		<div id="flowgroup">
			<div id="tabbar">
				<div class="tab" id="repost">
					<a>转发</a><a class="num">{reposts_count}</a>
				</div>
				<div class="tab active" id="comment">
					<a>评论</a><a class="num">{comments_count}</a>
				</div>
				<div class="tab" id="praise">
					<a>赞</a><a class="num">{praises_count}</a>
				</div>
			</div>
			<div id="repostflow" class="detailflow">
				<div class="flowbottom goon">
					<div class="endinfo">没有更多内容</div>
					<div class="md-preloader"><svg xmlns="http://www.w3.org/2000/svg" version="1.1" height="26" width="26" viewbox="0 0 26 26"><circle cx="13" cy="13" r="11.5" stroke-width="3"/></svg></div>
				</div>
			</div>
			<div id="commentflow" class="detailflow active">
				<div class="flowbottom goon">
					<div class="endinfo">没有更多内容</div>
					<div class="md-preloader"><svg xmlns="http://www.w3.org/2000/svg" version="1.1" height="26" width="26" viewbox="0 0 26 26"><circle cx="13" cy="13" r="11.5" stroke-width="3"/></svg></div>
				</div>
			</div>
			<div id="praiseflow" class="detailflow">
				<div class="flowbottom goon">
					<div class="endinfo">没有更多内容</div>
					<div class="md-preloader"><svg xmlns="http://www.w3.org/2000/svg" version="1.1" height="26" width="26" viewbox="0 0 26 26"><circle cx="13" cy="13" r="11.5" stroke-width="3"/></svg></div>
				</div>
			</div>
		</div>
		<div id="bottombar" onclick="commententer()">
			<div id="addcomment">
				<div class="avatar" style="background-image:url(/photo/{userid}/avatar.jpg)"></div>
				<div class="text"><a>添加评论...</a></div>
			</div>
		</div>'''


commentpage='''
		<div id="greycover" onclick="history.go(-1)"></div>
		<div id="commentbox">
			<div id="replyto"></div>
			<textarea id="commenttext" placeholder="添加评论..."></textarea>
			<div class="comment_actionbar">
				<div class="action false" id="camera">
					<div class="icon"></div>
					<div class="spark"><div class="ripple"></div></div>
				</div>
				<div class="action" id="at">
					<div class="icon"></div>
					<div class="spark"><div class="ripple"></div></div>
				</div>
				<div class="action false" id="face">
					<div class="icon"></div>
					<div class="spark"><div class="ripple"></div></div>
				</div>
				<div class="action false" id="hotpic">
					<div class="icon"></div>
					<div class="spark"><div class="ripple"></div></div>
				</div>		
				<div class="action" id="send">
					<div class="icon"></div>
					<div class="spark"><div class="ripple"></div></div>
				</div>
				<div id="counter">140</div>
			</div>
		</div>'''


composepage='''
		<div id="topbar">
			<div class="action" id="close" onclick="history.go(-1)">
				<div class="icon"></div>
				<div class="spark"><div class="ripple"></div></div>
			</div>
			<div class="action false" id="send">
				<div class="icon"></div>
				<div class="spark"><div class="ripple"></div></div>
			</div>
			<div class="avatar" style="background-image:url(/photo/{userid}/avatar.jpg)"></div>	  
		</div>
		
		<div id="composebody">
			<textarea id="composetext" placeholder="说点什么"></textarea>
			<div id="originview">
				<div id="originpic"></div>
				<div id="origintext"></div>
			</div>
			<div id="composeimageset"></div>
		</div>

		<div id="bottombar">
			<div id="option">		
				<div id="withcommentcheck"  onclick="repostwithcommentcheck()">
					<div id="checkradio" class="unselected"></div>
					<a>同时评论此微博</a>
				</div>
				<div id="viewlimit"><a>公开</a></div>
			</div>

			<div class="compose_actionbar">
				<div class="action false" id="camera">
					<form id="uploadimages"><input type="file" name="images" multiple accept="image/*"></form>
					<div class="icon"></div>
					<div class="spark"><div class="ripple"></div></div>
				</div>
				<div class="action false" id="topic">
					<div class="icon"></div>
					<div class="spark"><div class="ripple"></div></div>
				</div>
				<div class="action" id="at">
					<div class="icon"></div>
					<div class="spark"><div class="ripple"></div></div>
				</div>
				<div class="action false" id="face">
					<div class="icon"></div>
					<div class="spark"><div class="ripple"></div></div>
				</div>
				<div class="action false" id="more">
					<div class="icon"></div>
					<div class="spark"><div class="ripple"></div></div>
				</div>
				<div id="counter">140</div>
			</div>
		</div>'''


editpage='''<html>
	<head>
		<link href="/favicon.ico" rel="shortcut icon">
		<meta name="mobile-web-app-capable" content="yes">
		<meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>
		<meta name="theme-color" content="#ffffff">
		<meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=0">
		<title>首页</title>
		<link rel="stylesheet" href="/whole.css">
		<link rel="stylesheet" href="/cropper.css">
	</head>
	<body>
	<div id="toast"><div class="text"></div></div>
	<div class="pagelayout stayright" id="editpage">
		<div id="topbar">
			<div class="action" id="back" onclick="history.back()">
				<div class="icon"></div>
				<div class="spark"><div class="ripple"></div></div>
			</div>
			<div class="title">个人资料</div>
			<div class="action" id="edit">
				<div class="text">修改</div>
				<div class="spark"><div class="ripple"></div></div>
			</div>
		</div>
		<div class="bgblock" style="background-image:url(/photo/{uid}/userbg.jpg)">
			<div class="avatar" style="background-image:url(/photo/{uid}/avatar.jpg)">
				<form id="avatar"><input type="file" name="avatar" multiple accept="image/*"></form>
			</div>
			<div class="overlay">
				<form id="userbg"><input type="file" name="userbg" multiple accept="image/*"></form>
			</div>
		</div>
		<div class="nickname">
			<div class="holder">昵称</div>
			<div class="text" data-original="{nickname}">{nickname}</div>
		</div>
		<div class="introduction">
			<div class="holder">个人介绍</div>
			<div class="text" data-original="{introduction}">{introduction}</div>
		</div>
	</div>

	<div class="pagelayout unfocus" id="cutpage">
		<div id="topbar">
			<div class="action" id="back" onclick="history.back()">
				<div class="icon white"></div>
				<div class="spark"><div class="ripple"></div></div>
			</div>
			<div class="title">裁剪头像</div>
			<div class="action" id="edit">
				<div class="text">完成</div>
				<div class="spark"><div class="ripple"></div></div>
			</div>
		</div>
		<div class="img-container">
			<img src="" alt="" style="max-width: 100%">
		</div>
	</div>
	</body>
	<script src="https://cdn.bootcss.com/jquery/3.1.1/jquery.min.js"></script>
	<script src="https://cdnjs.cloudflare.com/ajax/libs/cropper/2.3.4/cropper.js"></script>
	<script src="/utility.js"></script> 
	<script src="/edit.js"></script> 
</html>'''


emptypage='''<!DOCTYPE html>
<html>
<head>
	<meta charset="utf-8">
	<link href="/favicon.ico" rel="shortcut icon">
	<meta name="viewport" content="width=device-width,initial-scale=1,user-scalable=0">
	<title>EXP-weibo</title>
	<style type="text/css">
		body{background-color:#f1f1f1;margin:0;}
		div{margin:80px auto;width:80px;height:80px;background:url(/iconset/contour.svg) center no-repeat;background-size:80px}
	</style>
</head>
<body>
	<div></div>
</body>
</html>'''

listpage='''<!DOCTYPE html>
<html>
	<head>
		<link href="/favicon.ico" rel="shortcut icon">
		<meta name="mobile-web-app-capable" content="yes">
		<meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>
		<meta name="theme-color" content="#ffffff">
		<meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=0">
		<title>{title}</title>
		<link rel="stylesheet" href="/preloader-28.css">
		<link rel="stylesheet" href="/whole.css">
	</head>
	<body>
	<div id="toast"><div class="text"></div></div>
	<div class="pagelayout stayright" id="listpage">
		<div id="topbar">
			<div class="action" id="back" onclick="history.back()">
				<div class="icon"></div>
				<div class="spark"><div class="ripple"></div></div>
			</div>
			<div class="title">{title}</div>
		</div>
		<div id="userflow">
			<div class="flowbottom goon">
				<div class="endinfo">没有更多内容</div>
				<div class="md-preloader"><svg xmlns="http://www.w3.org/2000/svg" version="1.1" height="28" width="28" viewbox="0 0 28 28"><circle cx="14" cy="14" r="12.5" stroke-width="3"/></svg></div>
			</div>
		</div>
	</div>
	</body>
	<script src="https://cdn.bootcss.com/zepto/1.2.0/zepto.js"></script>
	<script src="/utility.js"></script>
	<script src="/list.js"></script>
</html>'''

oneuser='''<div class="oneuser" uid="{uid}" onclick="window.location.href='/u/{uid}'">
				<div class="avatar" style="background-image:url(/photo/{uid}/avatar.jpg)"></div>
				<div class="nickname">{nickname}</div>
				<div class="introduction">{introduction}</div>
				<div class="action" id="{icontype}" data-followu="{followu}" onclick="followoperation($(this))">
					<div class="icon"></div>
				</div>
			</div>'''


albumpage = '''<!DOCTYPE html>
<html>
	<head>
		<link href="/favicon.ico" rel="shortcut icon">
		<title>相册</title>
		<meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=0">
		<meta charset="utf-8">
		<link rel="stylesheet" type="text/css" href="/whole.css">
		<link rel="stylesheet" type="text/css" href="/preloader-28.css">
		<link rel="stylesheet" href="/photoswipe.css"> 
		<link rel="stylesheet" href="/default-skin/default-skin.css">
	</head>
	<body>
	<div id="toast"><div class="text"></div></div>
	<div class="pagelayout stayright" id="albumpage">
		<div id="topbar">
			<div class="action" id="back" onclick="history.back()">
				<div class="icon"></div>
				<div class="ripple"></div>
			</div>
			<div class="title">相册</div>
		</div>
		<div id="photoflow">
			<div class="flowbottom goon">
				<div class="endinfo">没有更多内容</div>
				<div class="md-preloader"><svg xmlns="http://www.w3.org/2000/svg" version="1.1" height="28" width="28" viewbox="0 0 28 28"><circle cx="14" cy="14" r="12.5" stroke-width="3"/></svg></div>
			</div>
		</div>
	</div>
	{photoswipe_viewer}
	<script src="https://cdn.bootcss.com/zepto/1.2.0/zepto.js"></script>
	<script src="/photoswipe.min.js"></script> 
	<script src="/photoswipe-ui-default.min.js"></script> 
	<script src="/album.js"></script>
	<script src="/utility.js"></script>
	</body>
<html>
'''


photoswipe_viewer='''
	<div class="pswp" tabindex="-1" role="dialog" aria-hidden="true">
		<div class="pswp__bg"></div>
		<div class="pswp__scroll-wrap">
			<div class="pswp__container">
				<div class="pswp__item"></div>
				<div class="pswp__item"></div>
				<div class="pswp__item"></div>
			</div>
			<div class="pswp__ui pswp__ui--hidden">
				<div class="pswp__top-bar">
					<div class="pswp__counter"></div>
					<button class="pswp__button pswp__button--close" title="Close (Esc)"></button>
					<button class="pswp__button pswp__button--fs" title="Toggle fullscreen"></button>
					<button class="pswp__button pswp__button--zoom" title="Zoom in/out"></button>
					<div class="pswp__preloader">
						<div class="pswp__preloader__icn">
						  <div class="pswp__preloader__cut">
							<div class="pswp__preloader__donut"></div>
						  </div>
						</div>
					</div>
				</div>
				<div class="pswp__share-modal pswp__share-modal--hidden pswp__single-tap">
					<div class="pswp__share-tooltip"></div> 
				</div>
				<button class="pswp__button pswp__button--arrow--left" title="Previous (arrow left)">
				</button>
				<button class="pswp__button pswp__button--arrow--right" title="Next (arrow right)">
				</button>
				<div class="pswp__caption">
					<div class="pswp__caption__center"></div>
				</div>
			</div>
		</div>
	</div>'''


onerepost='''
			<div class="onerepost" onclick="window.location.href='/status/{pid}'">
				<div class="postinfo">
					<div class="avatar" onclick="event.stopPropagation();window.location.href='/u/{uid}'" style="background-image:url(/photo/{uid}/avatar.jpg)"></div>
					<div class="poster">{nickname}</div>
					<div class="time">{reposttime}</div>
				</div>
				<div class="postbody">
					<p class="posttext">{reposttext}</p>
				</div>
			</div>'''

onecomment='''
			<div class="onecomment" onclick="replyenter($(this))">
				<div class="postinfo">
					<div class="avatar" onclick="event.stopPropagation();window.location.href='/u/{uid}'" style="background-image:url(/photo/{uid}/avatar.jpg)"></div>
					<div class="poster">{nickname}</div>
					<div class="time">{commenttime}</div>
				</div>
				<div class="postbody">
					<p class="posttext">{commenttext}</p>
				</div>
			</div>'''

onepraise='''
			<div class="onepraise" uid="{uid}" onclick="window.location.href='/u/{uid}'">
				<div class="posterinfo">
					<div class="avatar" style="background-image:url(/photo/{uid}/avatar.jpg)"></div>
					<div class="poster"><a>{nickname}</a></div>
				</div>
			</div>'''


onepost='''
			<div class="onepost" pid="{pid}">
				<div class="postinfo" onclick="window.location.href='/u/{uid}'">
					<div class="avatar" style="background-image:url(/photo/{uid}/avatar.jpg)"></div>
					<div class="poster">{nickname}</div>
					<div class="from"><a class="time">{posttime}</a>来自 <a class="source">{device}</a></div>
				</div>
				<div class="postbody" onclick="window.location.href='/status/{pid}'">
					<p class="posttext">{posttext}</p>
					{gallery}
				</div>{repostbody}
				<div class="entry_actionbar">
					<div class="action {praisestatus}" id="praise" onclick="praiseoperation($(this))">
						<div class="icon" ></div>
						<div class="num {praises_exist}"><a>{praises_count}</a></div>
						<div class="spark"><div class="ripple"></div></div>
					</div>
					<div class="action" id="comment" onclick="window.location.href='/status/{pid}?action=comment'">
						<div class="icon"></div>
						<div class="num {comments_exist}"><a>{comments_count}</a></div>
						<div class="spark"><div class="ripple"></div></div>
					</div>
					<div class="action" id="repost" onclick="repostenter($(this))">
						<div class="icon"></div>
						<div class="num {reposts_exist}"><a>{reposts_count}</a></div>
						<div class="spark"><div class="ripple"></div></div>
					</div>
					<div class="action" id="share">
						<div class="icon"></div>
						<div class="spark"><div class="ripple"></div></div>
					</div>
				</div>
			</div>'''


repostbody='''
				<div class="repostbody" onclick="window.location.href='/status/{rid}'">
					<p class="reposttext"><a class="user" href="/u/{uid}">{nickname}</a>:{reposttext}</p>
					<div class="repoststatus">{repoststatus}</div>
					{gallery}
				</div>'''


div_thumb='''
						<div class="thumb" onclick="openPhotoSwipe($(this))" data-size="{size}" href="{original}" style="background-image: url({thumbnail});"></div>'''