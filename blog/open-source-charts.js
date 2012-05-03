function makeChart(name, numbers, labels, participants) {
	var r = Raphael(name),
		fin = function () {
			r.barLabels[this.bar.id].animate({'stroke': '#AAAAAA'}, 300);
		},
		fout = function () {
			r.barLabels[this.bar.id].animate({'stroke': '#000000'}, 300);
		},
		txtattr = { font: "12px sans-serif" };

	var chart = r.barchart(10, 10, 300, 220, [numbers]).hover(fin, fout);

	var yStart = 220;
	var barLabels = _.map(labels, function(text) {
		var label = r.text(0, yStart, text).attr({'text-anchor': 'start', 'style': 'vertical-align: text-top'});
		label.attr('y', yStart + (label.node.offsetHeight/2));
		r.add(label);
		yStart += label.node.offsetHeight;
		return label;
	});

	var i = 0;
	r.barLabels = _.reduce(barLabels, function(mem, label) {
		var id = chart[1][i].bar.id;
		mem[id] = label;
		i++;
		return mem;
	}, {});
}

function analyze(data) {
	console.log(data);

	function reasonsFor(reason, filter) {
		var filtered = _.filter(data.results, filter);
		var participants = _.size(filtered);
		
		var vals = _.reduce(filtered, function(mem, o) { 
			for (key in o[reason]) {
				mem[o[reason][key]] ++;
			}
			return mem;
		}, _.map(data[reason], function(){ return 0; }));

		var sortable = _.map(vals, function(val, i) { return { key: i, val: val }; });
		var sorted = _.first(_.sortBy(sortable, function(pair) { return pair.val; }).reverse(), 5);
		var vals = _.map(sorted, function(pair) { return pair.val; });
		var labels = _.map(sorted, function(pair) { return data[reason][pair.key]; });
		return { values: vals, labels: labels, participants: participants };
	}

	var chartData = reasonsFor('conReasons', function(o) { return o.frequency == 'Never' 
		|| o.frequency == 'A few times a year' 
		|| o.frequency == 'less than 5 times in my life'; 
	});

	makeChart("chart1", chartData.values, chartData.labels, chartData.participants);

	var chartData2 = reasonsFor('proReasons', function(o) { return o.frequency == 'Once or twice a month' 
		|| o.frequency == 'Once or twice a week' 
		|| o.frequency == 'Most days'; 
	});

	makeChart("chart2", chartData2.values, chartData2.labels, chartData2.participants);
}
