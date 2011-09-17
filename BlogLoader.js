(function($, _, Backbone, amplify) {
	/*
	This class takes care of loading blog posts from Google and
	caching them in localStorage. There's a bit of logic involved
	so I wanted to separate concerns and unit test.
	*/
	var BlogLoader = function() {
		this.key = 'BlogLoader';
		this.posts = []
	};

	_.extend(BlogLoader.prototype, {

		url: 'http://www.blogger.com/feeds/6849760623609771363/posts/default',
		xhrParams: { alt: 'json-in-script' },
		tipLength: 5,
	
		load: function(callback) {
			var params = _.extend(this.xhrParams, { 'max-results': this.tipLength });
			this.doAjax(callback, params);
		},

		loadRemainder: function(callback) {
			this.doAjax(callback, this.xhrParams);
		},

		doAjax: function(callback, params) {
			$.ajax(this.url, { crossDomain: true, dataType: 'jsonp', data: params, 
					success: this.onSuccess.butUsing(this, callback) });
		},

		onSuccess: function(callback, data) {
			var entry = data.feed.entry;
			this.mergeNewPosts(entry);

			if (callback)
				callback(entry);

			this.loadRemainder(callback);
		},

		mergeNewPosts: function(data) {
			this.posts = amplify.store('posts');
			
			if (!this.posts) {
				this.posts = data;
			}
			else {
				var existing = _.map(this.posts, function(x) { return x.id; });
				var _new = _(data).chain()
					.map(function(x) { return x.id; })
					.difference(existing)
					.value();
				this.posts = _(this.posts).chain()
					.union(_.select(data, function(x) { 
							return _.any(existing, function(y) { return x.id == y; }); 
						})
					)
					.sortBy(function(x) { return x.published; })
					.value();
			}
			
			amplify.store('posts', this.posts);
		}
		
	});
	window.BlogLoader = BlogLoader;

})(jQuery, _, Backbone, amplify);
