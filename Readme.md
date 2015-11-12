# Route 53 Updater
I used to have a very stable internet connection, but since moving flats my IP was changing on a regular basis when my router kept crashing.

I use [Amazon Route 53](https://aws.amazon.com/route53/) as my DNS for most of my domains and while there's plenty of decent tooling for keeping DNS entries up to date if you use [DynDNS](http://dyn.com/) or [NoIP](http://www.noip.com/) there wasn't anything that worked for keeping Route 53 entries up to date. So I just made my own.

This is just a very small and quickly hacked together bit of python using the [Boto 3](https://github.com/boto/boto3) AWS SDK which I run in a cron job on my home server and it seems to work fairly well.
