# This file is just simply a quick way to setup a web server
# via sinatra. Just a development server...

require 'sinatra'

get '/*' do |path|
	File.read path
end