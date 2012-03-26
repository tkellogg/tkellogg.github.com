#!/usr/bin/env ruby
# html2md.rb
# ================
#
# A script that converts HTML that was generated via Blogger's WYSIWYG editor into 
# markdown ready for consumption by jekyll. This was only tested by me personally,
# so I only accounted for situations that I was in. I converted _Large_ and _Larger_
# styles in blogger to `----` and `====` respectively. I also wired up some code to
# auto-retrieve gists and change them to pygments code blocks.
#
# This program is licensed to the public domain. I make no guarantees that it works
# as expected, so please backup your files first (which you probably are if you're 
# using jekyll via github).

require 'open-uri'

def get_pygments_language(filename)
	ext = File.extname filename
	known_extensions = {
		'.js' => 'js',
		'.json' => 'js',
		'.fs' => 'ocaml',
		'.cs' => 'csharp',
		'.sql' => 'sql',
		'.rb' => 'ruby',
	}

	known_extensions[ext]
end

def substitute_gist(line)
	pattern = %r{<script src="https://gist.github.com/(.*?).js\?file=(.*)"></script>}
	line.gsub! pattern do |m|
		code = nil
		url = m.sub pattern, "https://raw.github.com/gist/\\1/\\2"
		puts url
		open(url) do |response|
			code = response.read
		end

		lang = get_pygments_language m.sub(pattern, '\2')
		<<-END
{% highlight #{lang} %}
#{code}
{% endhighlight %}
		END
	end
end

def convert_stream(from, to)
	from.readlines.each do |line|
		line.gsub! %r{<br ?/>}, "\n"
		line.gsub! %r{&nbsp;}, " "
		line.gsub! %r{&amp;}, "&"
		line.gsub! %r{<span style="font-size: large;">(.+?)</span>}, "\n\\1\n-----------------"
		line.gsub! %r{<span style="font=size: x=large;">(.+?)</span>}, "\n\\1\n================="
		line.gsub! %r{<a href="([^"]+)"[^>]*>(.*?)</a>}, "[\\2](\\1)"
		line.gsub! %r{<i>(.*?)</i>}, "_\\1_"
		line.gsub! %r{<b>(.*?)</b>}, "**\\1**"
		line.gsub! %r{<span style="font-family: 'Courier New'.*?">(.*?)</span>}, '`\1`'
		line.gsub! %r{</?div.*?>}, ""
		substitute_gist line
		to.puts line
	end
end

def convert(from, to)
	File.open from do |a|
		File.open(to, 'w') do |z|
			convert_stream a, z
		end
	end
end

def rename(html)
	"#{File.dirname html}/#{File.basename html, '.*'}.markdown"
end

if ARGV.count == 1 
	convert ARGV[0], rename(ARGV[0])
elsif ARGV.count == 2
	convert ARGV[0], ARGV[1]
end
