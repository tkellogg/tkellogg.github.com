
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
	initialize: function() {
		this.loader = new BlogLoader();
	},

	model: BlogPost,

	loadTip: function(callback) {
		this.callback = callback;
		this.loader.load(this.onPostLoad.using(this));
	},

	onPostLoad: function(x, data)
	{
			for(var i in data.feed.entry) {
				var model = new BlogPost(mapBloggerData(data.feed.entry[i]));
				this.models.push(model);
			}
			
			if (this.callback)
			{
				this.callback(this.models);
			}
	}

});

var BlogPostView = Backbone.View.extend({
	
	initialize: function() {
		this.template = _.template($('#'+this.template).html());
	},

	template: 'postTemplate',
	
	render: function() {
		window.thingy = this.model.toJSON();
		$(this.el).html(this.template(this.model.toJSON()));
		return this;
	}

});

var BlogView = Backbone.View.extend({

	template: 'blogTemplate',
	itemTemplate: 'postTemplate',
	id: 'blog',
	
	initialize: function() {
		this.model = this.collection;
		this.template = _.template($('#'+this.template).html());
		this.itemTemplate = _.template($('#'+this.itemTemplate).html());
		this.bindModels();
	},
	
	bindModels: function() {
		this.views = new Array();
		var _views = this.views;
		window.m = this;
		this.model.models.forEach(function(m) {
			var view = new BlogPostView({model: m});
			_views.push(view);
		});
	},
	
	render: function() {
		$(this.el).html(this.template({ views: this.views, template: this.itemTemplate }));
		return this;
	}
	
});

