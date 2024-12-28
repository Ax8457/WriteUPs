# Santa Sweet Words (day18)

<p align="center"><img src="Screenshots/S1.png" alt="Desc"></p>

````ruby
require 'sinatra'

set :bind, '0.0.0.0'
set :show_exceptions, false
set :environment, :production

get '/' do
  send_file File.join(settings.public_folder, 'index.html')
end

get '/love' do
    send_file File.join(settings.public_folder, 'love.html')
end

get '/api/message' do
  number = params[:number]

  file_name = "#{number}.txt"

  content = open(file_name, "rb") { |f| f.read }
  content_type 'application/octet-stream'
  attachment file_name
  body content
end

get '/source' do
  content_type 'text/plain'
  File.read(__FILE__)
end
````

<a href="https://cheatsheetseries.owasp.org/cheatsheets/Ruby_on_Rails_Cheat_Sheet.html"> here </a>
