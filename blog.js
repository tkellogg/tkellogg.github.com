
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

var BlogPostCollection = Backbone.Collection.extend({
	model: BlogPost,
	url:'http://www.blogger.com/feeds/6849760623609771363/posts/default',
	xhrParams: { alt: 'json-in-script' },
	tipLength: 5,

	loadTip: function(callback) {
		var params = _.extend(this.xhrParams, { 'max-results': this.tipLength });
		$.ajax(this.url, { crossDomain: true, dataType: 'jsonp', data: params, context: this, success: function(data) 
		{
			for(var i in data.feed.entry) {
				var model = new BlogPost(mapBloggerData(data.feed.entry[i]));
				this.models.push(model);
			}
			
			if (callback)
			{
				callback(this.models);
			}
		}});
	},

	// TODO: implement local storage via amplify and sync with blogger
	sync: function() {
		
	}
});

var BlogPostView = Backbone.View.extend({
	
	initialize: function(model) {
		this.model = model;
		this.template = _.template($('#'+this.template).html());
	},

	template: 'postTemplate',
	
	render: function() {
		$(this.el).html(this.template(this.model.model.toJSON()));
		return this;
	}

});

var BlogView = Backbone.View.extend({

	template: 'blogTemplate',
	itemTemplate: 'postTemplate',
	id: 'blog',
	
	initialize: function(collection) {
		this.model = collection;
		this.template = _.template($('#'+this.template).html());
		this.itemTemplate = _.template($('#'+this.itemTemplate).html());
		this.bindModels();
	},
	
	bindModels: function() {
		this.views = new Array();
		this.model.forEach(function(model) {
			var view = new BlogPostView(model);
			this.views.push(view);
		});
	},
	
	render: function() {
		$(this.el).html(this.template({ views: this.collection, template: this.itemTemplate }));
		return this;
	}
	
});

