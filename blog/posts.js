---
layout: nil
---
allposts = [
	{% for post in site.posts %}
	{
		title: "{{ post.title }}",
		url: "{{ post.url }}",
		date: new Date("{{ post.date }}"),
		dateString: "{{ post.date | date_to_string }}",
		tags: [ {% for tag in post.categories %} {{ '"' | append:tag }}{{ '",' }} {% endfor %} ],
	},
	{% endfor %}
];

(function(allposts) {

	function calculateTagCloud(posts) {
		var cloud = { };
		for (var index in posts) {
			var post = posts[index];
			for (var iTag in post.tags) {
				var tag = post.tags[iTag];
				if (!cloud.hasOwnProperty(tag))
					cloud[tag] = 0;

				cloud[tag] ++;
			}
		}
		return cloud;
	}

	allposts.getTagCloud = function() {
		var emStart = 0.9;
		var emMultiplier = 0.05;
		var ret = '<div class="tag-cloud">';
		var cloud = calculateTagCloud(allposts);
		for (var tag in cloud) {
			var size = emStart + (Math.pow(cloud[tag], 1.5) * emMultiplier);
			ret += '<a class="tag" style="font-size: '
					+ size + 'em" href="#tag/' 
					+ tag + '">' + tag + '</a>';
		}
		return ret + '</div>';
	};

})(allposts);
