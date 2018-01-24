import requests
import time
from datetime import datetime

config = {
    'domain': 'https://api.vk.com/method',
    'access_token': "3439b8692d001b5db1285e92b82dc647155fbf6990d6a7fffcb01dd783f9748e2a1f47ad48aeb96954965&expires_in"
}

user_id = 12603412


def get(url, params={}, timeout=5, max_retries=5, backoff_factor=0.3):
    for attempt in range(max_retries):
        try:
            response = requests.get(url, params=params, timeout=timeout)
            return response
        except requests.exceptions.RequestException:
            if attempt == max_retries - 1:
                raise
            backoff_value = backoff_factor * (2 ** attempt)
            

def get_data(user_id, field):
    # for configuration to another ethernet point you must get access_token
    # ones more because api check ip-address and then would give you token
    query_params = {
        'domain': config['domain'],
        'access_token': config['access_token'],
        'user_id': user_id,
        'fields': field,
    }

    query = "{domain}/friends.get?access_token={access_token}&user_id={user_id}&fields={fields}&v=5.53".format(
        **query_params)

    return requests.get(query).json()

def get_history(user_id):
    # for configuration to another ethernet point you must get access_token
    # ones more because api check ip-address and then would give you token
    query_params = {
        'domain': config['domain'],
        'access_token': config['access_token'],
        'user_id': user_id,
        'method' : 'messages.getHistory'
    }

    query = "{domain}/{method}?access_token={access_token}&user_id={user_id}&v=5.53".format(**query_params)

    return requests.get(query).json()


def age_predict(user_id):
    # check config data
    assert isinstance(user_id, int), "user_id must be positive integer"
    assert user_id > 0, "user_id must be positive integer"
    # function call
    data_1 = get_data(user_id, 'bdate')
    # for all datas
    temp_arr = []
    # for years only
    year_arr = []
    for i in range(data_1['response']['count']):
        try:
            temp_arr.append(data_1['response']['items'][i]['bdate'])
            pass
        except Exception as e:
            pass

    for i in range(len(temp_arr)):
        temp_arr[i] = temp_arr[i].replace('.', '')
        if(len(temp_arr[i]) > 4):
            year_arr.append(temp_arr[i][len(temp_arr[i])-4:len(temp_arr[i])])

    for i in range(len(year_arr)):
        year_arr[i] = 2017 - int(year_arr[i])

    return int(sum(year_arr)/len(year_arr))


def messages_get_history(user_id, offset=0, count=20):

    assert isinstance(user_id, int), "user_id must be positive integer"
    assert user_id > 0, "user_id must be positive integer"
    assert isinstance(offset, int), "offset must be positive integer"
    assert offset >= 0, "user_id must be positive integer"
    assert count >= 0, "user_id must be positive integer"

    max_count = 200

    messages = []

    query_params = {
        'domain': config['domain'],
        'access_token': config['access_token'],
        'user_id': user_id,
        'offset': offset,
        'count': min(count, max_count)
    }

    while count > 0:

        data_1 = get_history(user_id)
        response = get(data_1, params=query_params)
        count -= min(count, max_count)
        query_params['offset'] += 200
        query_params['count'] = min(count, max_count)
        print(response.json())
        messages += response.json()
        mes = messages
        print('obj:'+mes)

    
    return messages


if __name__ == '__main__':
    # config
    message = messages_get_history(user_id)
    age = age_predict(user_id)
    
   
    print(age)



      




