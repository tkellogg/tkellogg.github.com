$(function() {
	var Workspace = Backbone.Router.extend({
		routes: {
			'': 'about',
			'about': 'about',
			'blog': 'blog'
		},

		about: function() {

		},

		blog: function() {
			var posts = new BlogPostCollection();
			posts.loadTip(function(m) {
				alert(m.length + ' but collection was '+ posts.length);
				blog = new BlogView(posts);
				blog.bindModels();
				blog.render();
			});
		}

	});

});

