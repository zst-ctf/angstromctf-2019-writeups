# Cookie Cutter
Web

## Challenge 

I stumbled upon this very interesting site lately while looking for cookie recipes, which claims to have a flag. However, the admin doesn't seem to be available and the site looks secure - can you help me out?

Author: lamchcl

https://cookiecutter.2019.chall.actf.co/

## Solution

Original cookie

	eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJwZXJtcyI6InVzZXIiLCJzZWNyZXRpZCI6MjUsInJvbGxlZCI6Im5vIiwiaWF0IjoxNTU1OTkwMjEzfQ.qr6AetDp8L_V71hWa1MDR0vDaFOWk-WqSxa0f7D3wDM

	session=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJwZXJtcyI6InVzZXIiLCJzZWNyZXRpZCI6OTUsInJvbGxlZCI6Im5vIiwiaWF0IjoxNTU1OTkyMTg3fQ.Ft_BpPuSlmMDIEhSBryvq_a6xvntfbghUveNmdNlnFU


How JWT works

- https://auth0.com/blog/brute-forcing-hs256-is-possible-the-importance-of-using-strong-keys-to-sign-jwts/

Exploit JWT

- https://auth0.com/blog/brute-forcing-hs256-is-possible-the-importance-of-using-strong-keys-to-sign-jwts/

- http://www.blog.hatsec.io/pentesterlab/jwt/

> Change the algorithm. This way, we can change the payload while bypassing the check from asymmetric encryption (private key). Edit the payload on https://jwt.io/ and then change the cookie accordingly...

Changing to None doesn't work though.

	{"alg":"None","typ":"JWT"}
	eyJhbGciOiJOb25lIiwidHlwIjoiSldUIn0=

	{"alg":undefined,"typ":"JWT"}
	eyJhbGciOnVuZGVmaW5lZCwidHlwIjoiSldUIn0K



	eyJhbGciOiJOb25lIiwidHlwIjoiSldUIn0.eyJwZXJtcyI6InVzZXIiLCJzZWNyZXRpZCI6MjUsInJvbGxlZCI6Im5vIiwiaWF0IjoxNTU1OTkwMjEzfQ.qr6AetDp8L_V71hWa1MDR0vDaFOWk-WqSxa0f7D3wDM

eyJhbGciOiJOb25lIiwidHlwIjoiSldUIn0.eyJwZXJtcyI6ImFkbWluIiwic2VjcmV0aWQiOjI1LCJyb2xsZWQiOiJubyIsImlhdCI6MTU1NTk5MDIxM30.tZYOFZwUn6Tnmu6wpKwQ-H6rkrKbrC9TWtSxzH5XTDo


eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJwZXJtcyI6ImFkbWluIiwic2VjcmV0aWQiOjEwMCwicm9sbGVkIjoibm8iLCJpYXQiOjE1NTU5OTAyMTN9.jmwka0C5Cka8LP9RrRJEpYmzF47KNjqDntvF6TJyhnQ



eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJwZXJtcyI6ImFkbWluIiwic2VjcmV0aWQiOiJ0ZXN0Iiwicm9sbGVkIjoibm8iLCJpYXQiOjE1NTU5OTIxODd9.kJoMZrspZeJh5zb7bpHJkP20g_tYxv6uQcUmhM3UVjI


eyJhbGciOnVuZGVmaW5lZCwidHlwIjoiSldUIn0K

Verify with undefined?
let secrets = [];
undefined
secrets[10]
undefined

https://github.com/brendan-rius/c-jwt-cracker

https://github.com/auth0/node-jsonwebtoken

## Flag

	??