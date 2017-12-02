#!/user/bin/env python

import gzip
import datetime
import os
import glob
import json

def build_new_twitter_object (twitter_object):
    user_data = twitter_object.get('user')
    return {
        'local_timestamp_ms': str (int (twitter_object.get('timestamp_ms')) + (int(user_data.get('utc_offset'))*1000) ),
        'id': user_data.get('id'),
        'text': twitter_object.get('text'),
        'followers_count': user_data.get('followers_count'),
        'friends_count': user_data.get('friends_count'),
        'country': 'undefined' if twitter_object.get('place') is None else twitter_object.get('place').get('country'),
        'verified': user_data.get('verified'),
        'source': twitter_object.get('source'),
        'original_timestamp_ms': str (int (twitter_object.get('timestamp_ms'))),
        'utc_offset_s': user_data.get('utc_offset'),
        'time_zone': user_data.get('time_zone')
    }

if __name__ == "__main__":
    # Total twitter messages processed
    twitter_count_total=0
    # Filtered twitter messages
    twitter_count_filtered=0
    # Store filtered twitter messages
    data_filtered=[]

    # Loop through all the gzip file
    for file in glob.glob("./data/*.gz"):

        # Check file name
        print(file)

        # Open gzip file
        f = gzip.open(file,'rt')

        # Skip the first line since it is fragmentary
        f.readline();

        # Loop through each line in gzip file, every line is one twitter message obeject
        for line in f:

            twitter_count_total+=1

            # Track the progress
            print (str(twitter_count_total) + "(" + str(twitter_count_filtered) + ")")

            # Skip the last line since it is fragmentary
            if (line[-1:] =='\n'):
                # Load each line as a json object
                twitter_object = json.loads(line)

                # Filter to only include twitter messages in English
                if (twitter_object.get('lang')=='en' or twitter_object.get('lang')=='en-BG'):
                    # Filter to only include twitter messages that has timezone
                    if (twitter_object.get('user').get('utc_offset') is not None):

                        twitter_count_filtered+=1;

                        # Build simple twitter obejct only contains info we need
                        new_twitter_object = build_new_twitter_object(twitter_object)

                        #print(json.dumps(twitter_object, indent=4, sort_keys=False))
                        #print(json.dumps(new_twitter_object, indent=4, sort_keys=False))
                        data_filtered.append(new_twitter_object)
        f.close()

    with gzip.open("data-filtered.gz", 'wb') as outfile:
        # Write each twitter message in one line, append EOL
        for item in data_filtered:
            item = json.dumps(item) + "\n"
            outfile.write(item.encode("utf-8"))
        outfile.close()


