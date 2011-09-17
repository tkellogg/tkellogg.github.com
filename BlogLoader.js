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
			$.ajax(this.url, { crossDomain: true, dataType: 'jsonp', data: params, 
					success: this.onSuccess.butUsing(this, callback) });
		},

		onSuccess: function(callback, data) {
			this.mergeNewPosts(data);

			if (callback)
				callback(data);
		},

		mergeNewPosts: function(data) {
			this.posts = amplify.store('posts');
			
			window.posts = data;
			
			amplify.store('posts', this.posts);
		}
		
	});
	window.BlogLoader = BlogLoader;

})(jQuery, _, Backbone, amplify);
