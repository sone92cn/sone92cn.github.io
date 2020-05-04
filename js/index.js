let MyApp = {
	data: {
		cate: null,
		full: null,
		mode: "none", // 过滤类别
		ilen: 0,      // 当前页
		size: 12,    // 单页展示数量
		filter: "",  // 类别
		recent: "",  // 时间
		search: ""	 // 搜索
	}
};

function dateToString(dt){
    let year = dt.getFullYear();
    let month =(dt.getMonth() + 1).toString();
    let day = (dt.getDate()).toString();
    if (month.length == 1) {
        month = "0" + month;
    }
    if (day.length == 1) {
        day = "0" + day;
    }
    return year + "-" + month + "-" + day;
}

// 首次激活全部文章时初始化Vue
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
					MyApp.data.cate = arts.cate;
					MyApp.data.full = arts.full;
					new Vue({
						el: "#content_1",
						data: MyApp.data,
						computed: {
							menu: function(){ // 全部文章
								let m = {};
								if(this.mode === "filter" && this.filter.length > 0){
									for(let k in this.full){
										if(this.full[k].indexOf(this.filter) != -1){
											m[k] = this.full[k];
										};
									};
								}else if(this.mode === "recent" && this.recent.length>0){
									for(let k in this.full){
										if(k >= this.recent){
											m[k] = this.full[k];
										};
									};
								}else if(this.mode === "search" && this.search.length>0){
									for(let k in this.full){
										if(k.toUpperCase().indexOf(this.search) != -1){
											m[k] = this.full[k];
										};
									};
								}else if(this.mode === "none"){
									return this.full;
								};
								return m;
							},
							page: function(){ // 分页标签
								let arr = [];
								if(this.nlen > 0){
									for (let i = 0; i < this.nlen; i++) {
										arr.push(i);
									};
								};
								return arr;
							},
							nlen: function(){ // 总页数
								this.ilen = 0;
								return Math.ceil(Object.keys(this.menu).length / this.size);
							},
							show: function(){
								if(this.nlen > 1){  // 大于1页才需要截取
									let m = {};
									let n = this.ilen > this.nlen ? this.nlen : this.ilen;
									let keys = Object.keys(this.menu).slice(n * this.size, (n+1) * this.size);
									for(let k of keys) {
									    m[k] = this.menu[k];
									};
									return m;
								}else{
									return this.menu;
								};
							}
						},
						methods: {
							filterArticle: function(event){
								let filter = $(event.target).data("filter");
								if(filter.length > 0){
									this.filter = filter;
									this.mode = "filter";
									viewHead($(event.target));
								}else{
									this.mode = "none";
									// this.filter = filter;
								};
							},
							recentArticle: function(event){
								let recent = parseInt($(event.target).data("recent"));
								if(recent > 0){
									let dt = new Date();
									dt.setMonth(dt.getMonth()-recent);
									this.recent = dateToString(dt);
									this.mode = "recent";
									viewHead($(event.target));
								}else{
									this.mode = "none";
									viewHead($(event.target));
									// this.recent = recent;
								};
							},
							gotoPage: function(event){
								let posi = parseInt($(event.target).data("index"));
								if(posi >= 0 && posi < this.nlen && posi != this.ilen){
									this.ilen = posi;
								};
							},
							movePage: function(event){
								let posi = parseInt($(event.target).data("index")) + this.ilen;
								if(posi >= 0 && posi < this.nlen && posi != this.ilen){
									this.ilen = posi;
								};
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
		alert("程序错误-无活动页面！");
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
		alert("程序错误，页面结构错误！")
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

function searchArticle(search){
	if(!$("#content_1").hasClass("d-none")){
		if(search != ""  && search != '搜索'){
			MyApp.data.search = search.toUpperCase();
			MyApp.data.mode = "search";
			viewHead($("#content_1").children(":first"));
		}else{
			MyApp.data.mode = "none";
			// MyApp.data.search = "";
		};
	}else{
		alert("本页面不支持搜索！");
	};
};

$(document).ready(function(){
	//
});
