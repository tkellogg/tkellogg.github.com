
$(function() {
	posts = new BlogPostCollection();
	blog = new BlogView(posts);
	posts.loadTip(function() {
		blog.bindModels();
		blog.render();
	});
});

