
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
	url:'http://www.blogger.com/feeds/6849760623609771363/posts/default?alt=json',
	tipLength: 5,

	loadTip: function(callback) {
		var self = this;
		$.getJSON(this.url + '&max-results=' + this.tipLength, null, function(data) {
			for(var i in data.feed.entry) {
				self.models.push(mapBloggerData(data.feed.entry[i]));
			}
			
			if (callback) {
				callback(data);
			}
		});
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

