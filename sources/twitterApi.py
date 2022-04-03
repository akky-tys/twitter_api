import urllib3
import setting
import json



def getTweetById2(http, key, searchId):
    url  = 'https://api.twitter.com/2/tweets/' + searchId
    req = http.request('GET',
                        url,
                        headers= {'Authorization': 'Bearer '+key}
                      )

    print(req)

    if (req.status == 200):
        tweets = json.loads(req.data)

        print(tweets)
    else:
        print(req.status)


def getTweetById(http, key, searchId, searchFeild={}):
    url  = 'https://api.twitter.com/2/tweets/' + searchId
    req = http.request('GET',
                        url,
                        headers= {'Authorization': 'Bearer '+key},
                        fields = searchFeild
                      )


    result = json.loads(req.data)
    if (req.status == 200):
        print(result)
    else:
        print(req.status)
        print(result['errors'])


def getTweetByText(http, key, searchFeild):
    url  = 'https://api.twitter.com/2/tweets/search/recent'
    req = http.request('GET',
                        url,
                        headers= {'Authorization': 'Bearer '+key},
                        fields = searchFeild
                      )

    if (req.status == 200):
        result = json.loads(req.data)
        if ('meta' in result):
          print('検索結果は' + str(result['meta']['result_count']) + '件でした')
        return result
    else:
        print(req.status)
        print(result['errors'])


