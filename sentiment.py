#!/user/bin/env python

import gzip
import datetime
import os
import glob
import json
#pip install vaderSentiment
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer



def get_text(twitter_object):
    return twitter_object.get('text')

def build_twitter_object_with_scores(twitter_object, neg_score, neu_score, compound_score, pos_score):
    return {
        'local_timestamp_ms': twitter_object.get('local_timestamp_ms'),
        'id': twitter_object.get('id'),
        'text': twitter_object.get('text'),
        'followers_count': twitter_object.get('followers_count'),
        'friends_count': twitter_object.get('friends_count'),
        'country': twitter_object.get('country'),
        'verified': twitter_object.get('verified'),
        'source': twitter_object.get('source'),
        'neg': neg_score,
        'neu': neu_score,
        'compound': compound_score,
        'pos': pos_score
    }

if __name__ == "__main__":
    # Total twitter messages processed
    twitter_count_total=0
    # Store filtered twitter messages
    data_with_scores = []

    # Loop through all the gzip file
    for file in glob.glob("./data/data-filtered.gz"):

        # Check file name
        print(file)

        # Open gzip file
        f = gzip.open(file,'rt')

        # Skip the first line since it is fragmentary
        f.readline()

        analyzer = SentimentIntensityAnalyzer()

        # Loop through each line in gzip file, every line is one twitter message obeject
        for line in f:

            twitter_count_total+=1

            # Track the progress
            print (str(twitter_count_total))

            # Load each line as a json object
            twitter_object = json.loads(line)

            text = get_text(twitter_object)

            vs = analyzer.polarity_scores(text)

            new_twitter_object = build_twitter_object_with_scores(twitter_object,
                                                                  vs.get('neg'),vs.get('neu'),
                                                                  vs.get('compound'), vs.get('pos'))
            data_with_scores.append(new_twitter_object)
            #print(json.dumps(new_twitter_object, indent=4, sort_keys=False))
        f.close()

    with gzip.open("tweet-scores.gz", 'wb') as outfile:
        # Write each twitter message in one line, append EOL
        for item in data_with_scores:
            item = json.dumps(item) + "\n"
            outfile.write(item.encode("utf-8"))
        outfile.close()


