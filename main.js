
$(function() {
	var url = 'http://www.blogger.com/feeds/6849760623609771363/posts/default?alt=json&max-results=5';
	$.getJSON(url, null, bloggerLoad);
});

function bloggerLoad(data) {
	window.blogData = data;
	for(var i in data.feed.entry)
	{
		$('#blog').append('<p>'+data.feed.entry[i].title+'</p>');
	}
	
}
