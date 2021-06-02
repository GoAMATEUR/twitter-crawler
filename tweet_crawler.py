from utils.search.search_runner import SearchRunner
from utils.search.search_context import SearchContext
from utils.search.search_task import SearchTask
from utils.io.result_export import ResultExporter
import os

# set search task
keyword = '修例'
tweets_limit = 100 # recommend no more than 20000 a time
fetching_cycle = 1
save_filename = keyword + str(fetching_cycle) + '.json'

savepath = 'search_raw_result\\' + keyword
if not os.path.exists(savepath):
    os.makedirs(savepath)

# Start crawling from a specific cursor, no parameters if crawling from the beginning.
search_context = SearchContext(
    #scroll_token='scroll:thGAVUV0VFVBaAwLWFmvep6x8WisCi4cH52qomEnEV7IlaFYCJehgHREVGQVVMVDUBFdwGFQAA'
)
search_task = SearchTask(
    keyword = keyword,
    tweets_limit = tweets_limit,
    original_tweet = True,
    language_restriction=['zh', 'en', 'und', 'zh-cn', 'zh-tw'] # language list
)
search_runner = SearchRunner(
    search_task,
    search_context=search_context
)

print('keyword:', keyword)
print('limit:', tweets_limit)
print('result save path:', os.path.join(savepath, save_filename))
print()

search_result = search_runner.run()

print(search_result.count, 'crawled.')

if os.path.exists(os.path.join(savepath, save_filename)):
    print()
    print('WARNING: Save path conflict. Existing file will be overwritten if not renamed manually.')
    os.system('pause')

result_exporter = ResultExporter()
result_exporter.to_json_file(os.path.join(savepath, save_filename),search_result)
result_exporter.save_last_cursor(os.path.join(savepath,'last_cursor.json'), search_result)

'''
Note:
@dataclass
class Tweet:
    time: str
    tweet_id: str
    content: str
    name: str
    screen_name: str
    user_id: str
    favorite_count: int
    quote_count: int
    reply_count: int
    replies=[]
'''

