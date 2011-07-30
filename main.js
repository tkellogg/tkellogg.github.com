
$(function() {
	posts = new BlogPostCollection();
	posts.loadTip();

	var $blog = $('#blog');
	posts.forEach(function(post) {
		var div = $blog.append("<div/>");
		var view = new BlogPostView({el: div, model: post});
		view.render();
	});
});

