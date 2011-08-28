(function($, _, Backbone, amplify) {
	/*
	This class takes care of loading blog posts from Google and
	caching them in localStorage. There's a bit of logic involved
	so I wanted to separate concerns and unit test.
	*/
	var BlogLoader = function(url) {
		this.url = url;
		this.key = 'BlogLoader';

		this.sync = function() {

		};

		_.extend(this, Backbone.Events);
	};


	window.BlogLoader = BlogLoader;

})(jQuery, _, Backbone, amplify);
