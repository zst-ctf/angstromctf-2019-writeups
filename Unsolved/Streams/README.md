# Streams
Binary

## Challenge 
White noise is useful whether you are trying to sleep, relaxing, or concentrating on writing papers. Find some natural white noise here.

Note: The flag is all lowercase and follows the standard format (e.g. actf{example_flag})

Author: ctfhaxor

## Hint
Are you sure that's an mp4 file? What's inside the file?

## Solution


https://streams.2019.chall.actf.co/video/stream.mp4

https://superuser.com/questions/1033563/how-to-download-video-with-blob-url
https://superuser.com/questions/1204497/download-all-m4s-files-of-a-mpeg-dash-stream


youtube-dl -F https://streams.2019.chall.actf.co/video/stream.mp4



https://stackoverflow.com/questions/23485759/combine-mpeg-dash-segments-ex-init-mp4-segments-m4s-back-to-a-full-source-m


	~/Library/Python/3.6/bin/youtube-dl -F https://streams.2019.chall.actf.co/video/stream.mp4?.mpd -v


## Flag

	??