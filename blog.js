
function mapBloggerData(data) {
	if (typeof(data) === 'Array')
	{
		for(var i in data) {
			data[i] = mapBloggerData(data[i]);
		}
		return data
	}
	else {
		return _.map(data, function(attr) { return attr.$t ? attr.$t : attr; });
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
		$.getJSON(url + '&max-results=' + this.tipLength, null, function(data) {
			this.add(mapBloggerData(data));
			if (callback) {
				callback(data);
			}
		});
	}

	// TODO: implement local storage via amplify and sync with blogger
	sync: function() {
		
	}
});

var BlogPostView = Backbone.View.extend({

	template = _.template($('#postTemplate').html()),
	
	render: function() {
		$(this.el).html(this.template(this.model.toJSON()));
		return this;
	}

});

