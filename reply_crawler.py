from utils.reply.reply_runner import ReplyRunner
from utils.reply.reply_context import ReplyContext
from utils.reply.reply_task import ReplyTask
from utils.io.reply_export import ReplyExporter
import os
import json
no = []
keywords = ['修例', '逃犯條例', '一國兩制', '送中']

for keyword in keywords:
    folder = 'replies/'+keyword
    if not os.path.exists(folder):
        os.makedirs(folder)
    with open('crawled_tweets/' + keyword + '.json', 'r', encoding='utf-8') as f:
        dic = json.loads(f.read())
    print(keyword)
    tweets = dic['tweets']
    for tweet in tweets:
        reply_count = tweet['reply_count']
        if reply_count == 0:
            continue
        tweet_id= tweet['tweet_id']
        if os.path.exists(os.path.join(folder, tweet_id + '.json')):
            print(tweet_id, 'exists.')
            continue
        print('https://twitter.com/{}/status/{}'.format(tweet['screen_name'], tweet_id))
        reply_task = ReplyTask(
            tweet_id= tweet_id,
            
        )
        reply_context = ReplyContext()
        reply_runner = ReplyRunner(
            reply_task,
            reply_outputs=[]
        )
        reply_result = reply_runner.run()
        print(reply_count, 'expected.')
        if reply_result.count == 0:
            no.append(tweet_id)
            continue
        
        exporter = ReplyExporter()

        exporter.to_json_file(os.path.join(folder, tweet_id+'.json'), reply_result)







