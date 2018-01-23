import requests

config = {
    'domain' : 'https://api.vk.com/method',
    # here! 
    'access_token': ""
}

def get_data(user_id, field):
	# for configuration to another ethernet point you must get access_token ones more because api check ip-address and then would give you token 
	query_params = {
	    'domain' : config['domain'],
	    'access_token': config['access_token'],
	    'user_id': user_id,
	    'fields': field,
	}
	
	query = "{domain}/friends.get?access_token={access_token}&user_id={user_id}&fields={fields}&v=5.53".format(**query_params)
	
	return requests.get(query).json()

def age_predict(user_id):
    # check config data
    assert isinstance(user_id, int), "user_id must be positive integer"
    assert user_id > 0, "user_id must be positive integer"
    # function call
    data_1 = get_data(user_id, 'bdate' )
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
    	temp_arr[i] = temp_arr[i].replace('.','')
    	if( len(temp_arr[i]) > 4):
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
    
    data_mes = get_data(user_id, '' )
    pass

if __name__ == '__main__':
	#config
	user_id = 1999327
	
	# function call
	age = age_predict(user_id)

	# check result
	print(age)
	
