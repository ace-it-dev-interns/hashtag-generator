import datetime
import requests
import json


def getCreds():
	""" Get creds required for use in the applications
	
	Returns:
		dictonary: credentials needed globally
	"""

	creds = dict() # dictionary to hold everything
	creds['access_token'] = 'EAAFEzPo2nKMBAEnaqLj74ZAiXIYYZAZB8RUKFmZCZAPIVzaG7eZCHOexp5v4ZAuiehn5MSzyw8NmQMhNPeRCNKKZBa5L0WTeZCZAHMHA1wyBCHK08rY3xLsyLdHlfYvSfHtHpf1abiMdZAC55qZAv8dXfQQKYT0PDNeF9UHyXiyaCjqp0AZDZD' # access token for use with all api calls
	creds['client_id'] = '357122138610851' # client id from facebook app hashtag-generator
	creds['client_secret'] = '8a3384e6ad85e79ecea9e3b24fb8db20' # client secret from facebook app
	creds['graph_domain'] = 'https://graph.facebook.com/' # base domain for api calls
	creds['graph_version'] = 'v8.0' # version of the api we are hitting
	creds['endpoint_base'] = creds['graph_domain'] + creds['graph_version'] + '/' # base endpoint with domain and version
	creds['debug'] = 'no' # debug mode for api call
	creds['page_id'] = '103099641435304' # users page id
	creds['instagram_account_id'] = '17841434402398007' # users instagram account id
	creds['ig_username'] = 'getaheadtutor' # ig username

	return creds

def makeApiCall( url, endpointParams, debug = 'no' ):
	""" Request data from endpoint with params
	
	Args:
		url: string of the url endpoint to make request from
		endpointParams: dictionary keyed by the names of the url parameters
	Returns:
		object: data from the endpoint
	"""

	data = requests.get( url, endpointParams ) # make get request; gets output data from API call

	response = dict() # hold response info
	response['url'] = url # url we are hitting
	response['endpoint_params'] = endpointParams #parameters for the endpoint
	response['endpoint_params_pretty'] = json.dumps( endpointParams, indent = 4 ) # pretty print for cli
	response['json_data'] = json.loads( data.content ) # response data from the api
	response['json_data_pretty'] = json.dumps( response['json_data'], indent = 4 ) # pretty print for cli

	if ( 'yes' == debug ) : # display out response info
		displayApiCallData( response ) # display response

	return response # get and return content

def displayApiCallData( response ) :
	""" Print out to cli response from api call """

	print("\nURL: ") # title
	print(response['url']) # display url hit
	print("\nEndpoint Params: ") # title
	print(response['endpoint_params_pretty']) # display params passed to the endpoint
	print("\nResponse: ") # title
	print(response['json_data_pretty']) # make look pretty for cli

def debugAccessToken( params ) :
	""" Get info on an access token 
	
	API Endpoint:
		https://graph.facebook.com/debug_token?input_token={input-token}&access_token={valid-access-token}
	Returns:
		object: data from the endpoint
	"""

	endpointParams = dict() # parameter to send to the endpoint
	endpointParams['input_token'] = params['access_token'] # input token is the access token
	endpointParams['access_token'] = params['access_token'] # access token to get debug info on

	url = params['graph_domain'] + '/debug_token' # endpoint url

	return makeApiCall( url, endpointParams, params['debug'] ) # make the api call

def getLongLivedAccessToken( params ):
	""" Get long lived access token
	
	API Endpoint:
		https://graph.facebook.com/{graph-api-version}/oauth/access_token?grant_type=fb_exchange_token&client_id={app-id}&client_secret={app-secret}&fb_exchange_token={your-access-token}
	Returns:
		object: data from the endpoint
	"""

	endpointParams = dict() # parameter to send to the endpoint
	endpointParams['grant_type'] = 'fb_exchange_token' # tell facebook we want to exchange token
	endpointParams['client_id'] = params['client_id'] # client id from facebook app
	endpointParams['client_secret'] = params['client_secret'] # client secret from facebook app
	endpointParams['fb_exchange_token'] = params['access_token'] # access token to get exchange for a long lived token

	url = params['endpoint_base'] + 'oauth/access_token' # endpoint url

	return makeApiCall( url, endpointParams, params['debug'] ) # make the api call

def getHashtagInfo( hashtag, params ) :
	""" Get info on a hashtag
	
	API Endpoint:
		https://graph.facebook.com/{graph-api-version}/ig_hashtag_search?user_id={user-id}&q={hashtag-name}&fields={fields}
	Returns:
		object: data from the endpoint
	"""

	endpointParams = dict() # parameter to send to the endpoint
	endpointParams['user_id'] = params['instagram_account_id'] # user id making request
	endpointParams['q'] = hashtag # hashtag name
	endpointParams['fields'] = 'id,name' # fields to get back
	endpointParams['access_token'] = params['access_token'] # access token

	url = params['endpoint_base'] + 'ig_hashtag_search' # endpoint url

	return makeApiCall( url, endpointParams, params['debug'] ) # make the api call

def getHashtagMedia( params ) :
	""" Get posts for a hashtag
	
	API Endpoints:
		https://graph.facebook.com/{graph-api-version}/{ig-hashtag-id}/top_media?user_id={user-id}&fields={fields}
		https://graph.facebook.com/{graph-api-version}/{ig-hashtag-id}/recent_media?user_id={user-id}&fields={fields}
	Returns:
		object: data from the endpoint
	"""

	endpointParams = dict() # parameter to send to the endpoint
	endpointParams['user_id'] = params['instagram_account_id'] # user id making request
	endpointParams['fields'] = 'id,children,caption,comments_count,like_count,media_type,media_url,permalink' # fields to get back
	endpointParams['access_token'] = params['access_token'] # access token

	url = params['endpoint_base'] + params['hashtag_id'] + '/' + params['type'] # endpoint url

	return makeApiCall( url, endpointParams, params['debug'] ) # make the api call

def getHashtagMediaAll( hashtag_id, params ):
	"""
	Get top and recent hashtag media for hashtag_id
	"""
	
	params = params.copy() #create local version of cred params

	# params['hashtag_id'] = '17841593875074036' #provides target hashtag id
	params['hashtag_id'] = hashtag_id #provides target hashtag id
	params['type'] = 'top_media' #sets media type to top
	top_response = getHashtagMedia(params) #function call that returns post info

	params['hashtag_id'] = hashtag_id #provides target hashtag id
	params['type'] = 'recent_media' #sets media type to recent
	recent_response = getHashtagMedia(params) #function call that returns post info

	return top_response, recent_response

def getMediaCommentCount ( top_response, recent_response ) : 
	""" 
		Gets comment counts from recent and top posts, and compiles data into a list of tuples
		containing the media id and its comment count
	"""
	comment_counts = [] #creates a list that will contain each top post's comment count
	comment_counts = [post['comments_count'] for post in top_response['json_data']['data']]  #appends each top post's comment count to the list
	post_id = [] #creates a list that will contain each top post's id
	post_id = [post['id'] for post in top_response['json_data']['data']] #appends each top post id to the list
	post_id_and_comment_counts = list(zip(post_id, comment_counts)) #creates a tuple that combines top post id and comment count

	recent_comment_counts = [] #creates a list that will contain each recent post's comment count
	recent_comment_counts = [post['comments_count'] for post in recent_response['json_data']['data']] #appends each recent post's comment count to the list
	recent_post_id = [] #creates a list that will contain each recent post's id
	recent_post_id = [post['id'] for post in recent_response['json_data']['data']] #appends each recent post id to the list
	recent_post_id_and_comment_counts = list(zip(recent_post_id, recent_comment_counts)) #creates a tuple that combines recent post id and comment count
 
	post_id_and_comment_counts += recent_post_id_and_comment_counts #appends recent comment counts to top comment counts3

	return post_id_and_comment_counts

def getMediaLikeCount ( top_response, recent_response ) : 
	""" 
		Gets like counts from recent and top posts, and compiles data into a list of tuples containing the media
		id and its number of likes.
	"""
	like_counts = [] #creates a list that will contain each top post's like count
	like_counts = [post['like_count'] for post in top_response['json_data']['data']]  #appends each top post's like count to the list
	post_id = [] #creates a list that will contain each top post's id
	post_id = [post['id'] for post in top_response['json_data']['data']] #appends each top post id to the list
	post_id_and_like_counts = list(zip(post_id, like_counts)) #creates a tuple that combines top post id and like count
	
	recent_like_counts = [] #creates a list that will contain each recent post's like count
	recent_like_counts = [post['like_count'] for post in recent_response['json_data']['data']] #appends each recent post's like count to the list
	recent_post_id = [] #creates a list that will contain each recent post's id
	recent_post_id = [post['id'] for post in recent_response['json_data']['data']] #appends each recent post id to the list
	recent_post_id_and_like_counts = list(zip(recent_post_id, recent_like_counts)) #creates a tuple that combines recent post id and like count
 
	post_id_and_like_counts += recent_post_id_and_like_counts #appends recent like counts to top like counts
	
	return post_id_and_like_counts

def getMediaCaptions ( top_response, recent_response ) :
	"""
		Creates a list of tuples containing media ids and their captions
	"""
	captions = [] #creates a list that will contain each top post's caption
	captions = [post['caption'] for post in top_response['json_data']['data']] #appends each top post's caption to the list
	post_id = [] #creates a list that will contain each top post's id
	post_id = [post['id'] for post in top_response['json_data']['data']] #appends each top post id to the list
	post_id_and_captions = list(zip(post_id,captions)) #creates a tuple that combines top post id and captions
	
	recent_captions = [] #creates a list that will contain each recent post's caption
	recent_captions = [post['caption'] for post in recent_response['json_data']['data']] #appends each recent post's like caption to the list
	recent_post_id = [] #creates a list that will contain each recent post's id
	recent_post_id = [post['id'] for post in recent_response['json_data']['data']] #appends each recent post id to the list
	recent_post_id_and_captions = list(zip(recent_post_id, recent_captions)) #creates a tuple that combines recent post id and captions
 
	post_id_and_captions += recent_post_id_and_captions #appends recent captions to top captions
	
	return post_id_and_captions

def getRelatedHashtags ( captions_and_ids ) : 
	"""
		Creates a list of tuples that each contain a media id and a list of the media's related hashtags.
	"""
	# captions_and_ids = getMediaCaptions() #function call that returns a list of media ids and their captions.
	ids, captions = zip(*captions_and_ids) #separates the ids and captions into 2 lists
	split_captions = [caption.split() for caption in captions] #separates each caption into a list of words
	related_hashtags = [] #declaration of a list that will store lists of hashtags, wherein each inner list represents a single post 
	for caption in split_captions: #iterates through each caption in the initial list of captions
		caption_hashtags = [] #creates a new inner list for each caption 
		for item in caption: #iterates through each item in the caption 
			if item[0] == '#': #checks if the item's first character is a hashtag
				caption_hashtags.append(item) #adds the item to the inner list if so
		related_hashtags.append(caption_hashtags) #adds the inner list to the outter list 
	related_hashtags = list(zip(ids, related_hashtags)) #creates a list of tuples that each contain the post id and a list of its related hashtags
	
	return related_hashtags

def compilePostData ( like_counts, comment_counts, media_captions, media_hashtags ) :
	"""
		Creates a list of dictionaries that each represent a single ID and contain related hashtags and pertinent metrics
	"""
 
	ids, likes = zip(*like_counts)
	ids, comments = zip(*comment_counts)
	ids, captions = zip(*media_captions)
	ids, hashtags = zip(*media_hashtags)
	
	list_of_dicts = []
	index = 0
	for id in ids:
		id_dict = {}
		id_dict['id'] = id
		id_dict['caption'] = captions[index]
		id_dict['hashtags'] = hashtags[index]
		id_dict['likes'] = likes[index]
		id_dict['comments'] = comments[index]
		list_of_dicts.append(id_dict)
		index += 1
	return list_of_dicts

def getLikeTotals ( related_hashtags, list_of_dictionaries ) : 
	"""
		Creates a nested list containing like totals for each individual hashtag on a piece of related media
	"""
	
	ids, lists_of_hashtags = zip(*related_hashtags)
	aggregated_like_counts = []
	for list_ in lists_of_hashtags:
		like_counts = []
		for hashtag in list_:
			like_count = 0
			for dictionary in list_of_dictionaries:
				if hashtag in dictionary['hashtags']:
					like_count += dictionary['likes']
			like_counts.append(like_count)
		aggregated_like_counts.append(like_counts)
	return aggregated_like_counts
			
def getCommentTotals ( related_hashtags, list_of_dictionaries ) :  
	"""
		Creates a nested list containing comment totals for each individual hashtag on a piece of related media
	"""
	
	ids, lists_of_hashtags = zip(*related_hashtags)
	aggregated_comment_counts = []
	for list_ in lists_of_hashtags:
		comment_counts = []
		for hashtag in list_:
			comment_count = 0
			for dictionary in list_of_dictionaries:
				if hashtag in dictionary['hashtags']:
					comment_count += dictionary['comments']
			comment_counts.append(comment_count)
		aggregated_comment_counts.append(comment_counts)
	return aggregated_comment_counts

def getNumberOfPosts ( related_hashtags, list_of_dictionaries ) :  
	"""
		Creates a nested list containing number of posts for each individual hashtag on a piece of related media
	"""

	ids, lists_of_hashtags = zip(*related_hashtags)
	aggregated_post_counts = []
	for list_ in lists_of_hashtags:
		post_counts = []
		for hashtag in list_:
			post_count = 0
			for dictionary in list_of_dictionaries:
				if hashtag in dictionary['hashtags']:
					post_count += 1
			post_counts.append(post_count)
		aggregated_post_counts.append(post_counts)
	return aggregated_post_counts
	
def compileHashtagData ( related_hashtags, list_of_dictionaries, number_of_posts, total_likes, total_comments) :
	"""
		Creates a nested dict with each hashtag and their respective values.			
	"""
    
	ids, lists_of_hashtags = zip(*related_hashtags)
	hashtag_info = {}

	outer_index = 0
	for list_ in lists_of_hashtags:
		inner_index = 0
		for hashtag in list_:
			if hashtag not in hashtag_info:  
				hashtag_info['{}'.format(hashtag)] = {}
				hashtag_info['{}'.format(hashtag)]['total_likes'] = total_likes[outer_index][inner_index]
				hashtag_info['{}'.format(hashtag)]['total_comments'] = total_comments[outer_index][inner_index]
				hashtag_info['{}'.format(hashtag)]['number_of_posts'] = number_of_posts[outer_index][inner_index]
			inner_index += 1
		outer_index += 1
	return hashtag_info

def getHashtagList (params) :
    
    hashtag_id = params['json_data']['data'][0]['id']
    
    top_response, recent_response = getHashtagMediaAll(hashtag_id, params)
    
    comment_counts = getMediaCommentCount(top_response, recent_response)
    like_counts = getMediaLikeCount(top_response, recent_response)
    captions_and_ids = getMediaCaptions(top_response, recent_response)
    related_hashtags = getRelatedHashtags(captions_and_ids)
    
    list_of_dictionaries = compilePostData(like_counts, comment_counts, captions_and_ids, related_hashtags)
    
    number_of_posts = getNumberOfPosts(related_hashtags, list_of_dictionaries)
    total_likes = getLikeTotals(related_hashtags, list_of_dictionaries)
    total_comments = getCommentTotals(related_hashtags, list_of_dictionaries)
    
    hashtag_data = compileHashtagData(related_hashtags, list_of_dictionaries, number_of_posts, total_likes, total_comments)
    
    df = pd.DataFrame(hashtag_data).T.sort_values('total_comments')
    df['avg_engagement'] = (df['total_likes'] + df['total_comments']) / df['number_of_posts']
    
    
    return df.sort_values('number_of_posts', ascending=False).head(30)

if __name__ == "__main__" : 
    print(getHashtagList())
