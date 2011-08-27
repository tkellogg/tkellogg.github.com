
$(function() {
	posts = new BlogPostCollection();
	posts.loadTip(function(m) {
		blog = new BlogView({collection: posts});
		$('#blog').append(blog.render().el);
	});
});

