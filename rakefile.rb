require 'rake'
require 'maruku'

task :default => 'build:all' 

namespace :build do

	task :markdown do
		Dir.glob('*.markdown').each do |f|
			File.open f do |txt|
				md = Maruku.new txt.read
				htmlname = f.sub 'markdown', 'html'
				File.open htmlname, 'w' do |x| 
					x.write(md.to_html) 
				end	
			end
		end
	end

end

