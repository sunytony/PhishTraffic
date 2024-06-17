now=`date +'%Y-%m-%d_%H-%M-%S'`

curl https://openphish.com/feed.txt > /home/seungmin/phish/files/"openphish_${now}".txt
curl https://phishunt.io/feed.txt > /home/seungmin/phish/files/"phishhunt_${now}".txt
#python3 /home/seungmin/phish/traffic_crawl.py "openphish_${now}".txt
#python3 /home/seungmin/phish/traffic_crawl.py "phishhunt_${now}".txt
