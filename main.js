$(function() {
	var Workspace = Backbone.Router.extend({
		routes: {
			'': 'home',
			'home': 'home',
			'blog': 'blog'
		},

		_hideAll: function() {
			for(var route in routes) {
				$('#'+route).hide();
			}
		},

		home: function() {
			$('#home').load('home.html').show();
		},

		blog: function() {
			$('#blog').show();
			var posts = new BlogPostCollection();
			posts.loadTip(function(m) {
				blog = new BlogView(posts);
				blog.bindModels();
				blog.render();
			});
		}

	});
	
	var ws = new Workspace();
	Backbone.history.start();
});

