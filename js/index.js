
function showContent($obj){
	var $remove = $obj.parent().parent().find("li.active");
	if($remove.length === 1){
		var $active = $obj.parent();
		if($remove.data("href") != $active.data("href")){
			$remove.removeClass("active");
			$active.addClass("active");
			$($remove.data("href")).addClass("d-none");
			$($active.data("href")).removeClass("d-none");
		};
	}else{
		alert("程序错误！");
	}
};

function viewHead($obj){
	var $page = $obj.parents(".content:first");
	var $part = $page.find(".view-part:first");
	var $full = $page.find(".view-full:first");
	if($part.length === 1 && $full.length === 1){
		if(!$full.hasClass("d-none")){
			$full.addClass("d-none");
		};
		if($part.hasClass("d-none")){
			$part.removeClass("d-none");
		};
	}else{
		alert("程序错误！")
	};
};

function viewArticle($page, url){
	var $part = $page.find(".view-part:first");
	var $full = $page.find(".view-full:first");
	if($part.length === 1 && $full.length === 1){
		$.ajax({
			url: url,
			async: true,
			cache: false,
			dataType: "html",
			success: (data) => {
				if(!$part.hasClass("d-none")){
					$part.addClass("d-none");
				};
				if($full.hasClass("d-none")){
					$full.removeClass("d-none");
				};
				$full.html(data);
			},
			error: function(){
				alert("获取文章失败！");
			}
		});
	}else{
		alert("程序错误！")
	};
};

$(document).ready(function(){
	// 显示活动标签
	// var $page = $($("#navbar > ul > li.active").data("href"));
	// alert($page.html());
	// $page.removeClass("hidden");
	// $page.addClass("show");
});
