# Control You
Web

## Challenge 

Only those who give us the flag are exempt from our control.

Author: kmh11

https://controlyou.2019.chall.actf.co/

## Hint

Your browser executes code when you're viewing a web page. Is it possible to see that code?

## Solution

	$ curl https://controlyou.2019.chall.actf.co/
	<!DOCTYPE html>
	<html>
	<head>
		<title>Hypnotization</title>
	</head>
	<body style="background: url(https://66.media.tumblr.com/15d3f53cb56f04dba66dfd53aed24b7f/tumblr_o87xi4XjVB1twd8ddo1_400.gif);">
		<div style="text-align: center; position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); color: red; font-family: 'Comic Sans MS', sans-serif;">
			<h1 style="background-color: blue;">Hypnotization in progress...</h1>
			<h2 style="color: green; background-color: yellow;">To stop hypnotization enter the flag below:</h2>
			<input type="password" id="flag" style="font-size: 3em;"><br>
			<button type="button" onclick="stop()" style="background: blue; border: 0.5em solid red; font-size: 2em; font-family: 'Comic Sans MS', sans-serif; margin-top: 1em; cursor: pointer;">Stop Hypnotization</button>
		</div>
		<script>
		function stop() {
			if (flag.value === "actf{control_u_so_we_can't_control_you}") {
				document.body.style.background = "red";
			}
		}
		</script>
	</body>

## Flag

	actf{control_u_so_we_can't_control_you}
