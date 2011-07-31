
function mapBloggerData(data) {
	if (typeof(data) === 'Array')
	{
		for(var i in data) {
			data[i] = mapBloggerData(data[i]);
		}
		return data
	}
	else {
		for(var attr in data)
		{
			data[attr] = data[attr].$t ? data[attr].$t : data[attr];
		}
		return data;
	}
}

var BlogPost = Backbone.Model.extend({
	initialize: function(object) {
		this.set(mapBloggerData(object));
	}
});

function onBloggerPostsReceived(data)
{
	for(var i in data.feed.entry) {
		var model = new BlogPost(mapBloggerData(data.feed.entry[i]));
		this.models.push(model);
	}
}

var BlogPostCollection = Backbone.Collection.extend({
	model: BlogPost,
	url:'http://www.blogger.com/feeds/6849760623609771363/posts/default',
	xhrParams: { alt: 'json-in-script' },
	tipLength: 5,

	loadTip: function() {
		var params = _.extend(this.xhrParams, { 'max-results': this.tipLength });
		$.ajax(this.url, { crossDomain: true, dataType: jsonp, data: params, success: onBloggerPostsReceived, context: this });
	},

	// TODO: implement local storage via amplify and sync with blogger
	sync: function() {
		
	}
});

var BlogPostView = Backbone.View.extend({
	
	initialize: function() {
		this.template = _.template($('#'+this.template).html());
	},

	template: 'postTemplate',
	
	render: function() {
		$(this.el).html(this.template(this.model.toJSON()));
		return this;
	}

});

