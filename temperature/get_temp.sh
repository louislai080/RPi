    #!/bin/bash
	curl -s "http://rss.accuweather.com/rss/liveweather_rss.asp?metric=1&locCode=ASI|TW|TW018|TAIPEI|" | sed -n '/Currently:/ s/.*: \(.*\): \([0-9]*\)\([CF]\).*/\2 \3, \1/p'