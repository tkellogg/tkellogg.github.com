$(function() {
	var Workspace = Backbone.Router.extend({
		routes: {
			'': 'home',
			'home': 'home',
			'bio': 'bio',
			'blog': 'blog'
		},

		_hideAll: function() {
			for(var route in this.routes) {
				if (route)
					$('#'+route).hide();
			}
		},

		home: function() {
			this._hideAll();
			$('#home').load('home.html').show();
		},

		blog: function() {
			this._hideAll();
			$('#blog').show();
			var posts = new BlogPostCollection();
			posts.loadTip(function(m) {
				blog = new BlogView({ el: $('#blog').item, collection: posts });
				blog.bindModels();
				$('#blog').html(blog.render().el);
			});
		},

		bio: function() {
			this._hideAll();
			$('#bio').load('bio.html').show();
		}

	});
	
	var ws = new Workspace();
	Backbone.history.start();
});

