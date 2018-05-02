def st(st1, st2):
    
	# check the length of strings
    if(len(st1) == len(st2)):
    	st1chet = []
    	st1nechet = []
    	st2chet = []
    	st2nechet = []
    	for i in range(len(st1)):
    		if i % 2 == 0:
    			st1chet.append(st1[i])
    		else:
    			st1nechet.append(st1[i])

    	for i in range(len(st2)):
    		if i % 2 == 0:
    			st2chet.append(st2[i])
    		else:
    			st2nechet.append(st2[i])

    	st1chet = sorted(st1chet)
    	st2chet = sorted(st2chet)
    	st1nechet = sorted(st1nechet)
    	st2nechet = sorted(st2nechet)

    	if st1chet==st2chet and st2nechet==st1nechet:
    		print('true')
    	else:
    		print('false')
    else:
        print('length does not match')

if __name__ == '__main__':
    st('abcd','cdab')
