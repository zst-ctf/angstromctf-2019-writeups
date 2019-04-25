echo "" > output.m4s

url="https://streams.2019.chall.actf.co/video/init-stream2.m4s"
curl -s $url >> output.m4s

for i in $(seq -f "%05g" 1 7)
do
    url="https://streams.2019.chall.actf.co/video/chunk-stream2-$i.m4s"
    curl -s $url >> output.m4s
    echo $url
done