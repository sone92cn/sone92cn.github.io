let MyApp = {
	cate: [],
	full: {}
};

function showContent($obj){
	let $remove = $obj.parent().parent().find("li.active");
	if($remove.length === 1){
		let $active = $obj.parent();
		if($remove.data("href") != $active.data("href")){
			$remove.removeClass("active");
			$active.addClass("active");
			$($remove.data("href")).addClass("d-none");
			$($active.data("href")).removeClass("d-none");
		};
		if($active.data("href") === "#content_1" && ($($active.data("href")).data("init") === "none")){
			$.ajax({
				url: "/json/articles.json",
				type: "GET",
				async: true,
				cache: false,
				dataType: "json",
				success: function(arts){
					let view = new Vue({
						el: "#content_1",
						data:{
							cate: arts.cate,
							full: arts.full,
							filter: ""
						},
						computed: {
							menu: function(){
								if(this.filter.length > 0){
									let m = {};
									for(let k in this.full){
										if(this.full[k].indexOf(this.filter) != -1){
											m[k] = this.full[k];
										};
									};
									for(let k in m){
								    return m;
								  };
									return {"无满足满足要求的内容": "#"};
								}else{
									return this.full;
								};
							}
						},
						methods: {
							filterArticle: function(event){
								this.filter = $(event.target).data("filter");
								// showContent($(event.target));
								viewHead($(event.target));
							}
						}
					});
					$($active.data("href")).data("init", "init");
					// alert(JSON.stringify(arts));
				},
				error: function(){
					alert("获取文章失败！");
				}
			});
		};
	}else{
		alert("程序错误！");
	}
};

function viewHead($obj){
	let $page = $obj.parents(".content:first");
	let $part = $page.find(".view-part:first");
	let $full = $page.find(".view-full:first");
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
	if(url === "#"){
		return;
	};
	let $part = $page.find(".view-part:first");
	let $full = $page.find(".view-full:first");
	if($part.length === 1 && $full.length === 1){
		$.ajax({
			url: url,
			type: "GET",
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
	//
});
