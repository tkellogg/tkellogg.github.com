(function() {

	function addArgs(args, context, moreArgs) {
			var args = _(args).toArray();
			if (typeof(moreArgs) !== 'undefined')
				args = moreArgs.concat(args);
			if (typeof(context) !== 'undefined')
				args.unshift(this);
			return args;
	}

	Function.prototype.using = function(context) {
		var fn = this;
		var extras = _(arguments).toArray().slice(1);
		return function() {
			return fn.apply(context, addArgs(arguments, this, extras));
		};
	};

	Function.prototype.butUsing = function(context) {
		var fn = this;
		var extras = _(arguments).toArray().slice(1);
		return function() {
			return fn.apply(context, addArgs(arguments, undefined, extras));
		};
	};

})();

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

