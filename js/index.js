var content_a = -1;
var content_s = new Array(0, 0, 0, 0, 0);

function getUrlParam(name) {
	var reg = new RegExp("(^|&)" + name + "=([^&]*)(&|$)"); //构造一个含有目标参数的正则表达式对象
	var r = window.location.search.substr(1).match(reg); //匹配目标参数
	if (r != null) return unescape(r[2]); return null; //返回参数值
};

function focusSearch(search){
	if (search.value == "Search..."){
		search.value = "";
	};
};

function blurSearch(search){
	if (search.value == ""){
		search.value = "Search...";
	};
};

function searchResult(){
	text = $("#input_search").val();
	if ((text.length > 0) && (text != "Search...")) {
		alert("搜索关键词：" + text);
	}else{
		alert("请输入需要搜索的关键词！");
	};
};

function showContent(n){
	if (n<5){
		if (content_a > -1){
			$("#content_" + content_a).hide();
		};
		$("#content_" + n).show();
		content_a = n;
		
		if (content_s[n] == 0) {
			var content = "content_" + n;
			$.each(var_load[content], function(name, value){
				$(name).load(value);
			});
			$.each(var_append[content], function(name, value){
				$(name).html("");
				$.each(value, function(i, item){
					$.get(item, function(data, status){
						if (status=="success"){$(name).append(data);}
						else{alert("Fail to download " + item);};
					});
				});
			});
			$(var_show[content]).show();
			content_s[n] = 1;
		};
	};
};

function viewHead(content, action){
	if (action != "null"){
		$(content + " #wrap-col-body").hide();
		$(content + " #wrap-col-head").show();
		$(content + " #wrap-col-head").load(action);
		$(content + " #wrap-col-head #view_head").attr("href", "javascript:viewHead('" + content + "');");
		
	}else{
		$(content + " #wrap-col-body").hide();
		$(content + " #wrap-col-head").show();
	};
};

function viewArticle(content, article){
	$(content + " #wrap-col-head").hide();
	$(content + " #wrap-col-body").show();
	$(content + " #wrap-col-body").load(article);
	$(content + " #wrap-col-body #view_head").attr("href", "javascript:viewHead('" + content + "');");
};