
class text_colors:
  BRIGHT_GREEN = '\033[1;32;40m'
  YELLOW = '\033[1;33;40m'
  RED = '\033[1;31;40m'
  RESET = '\033[m'

def current_time():
  now = datetime.now().strftime("%d.%m.%Y | %H:%M:%S")
  return now 

def print_log(status, text):
  color = text_colors()

  cur_time = f"[ {current_time()} ]"

  if status == 'info':
    print(f"{color.BRIGHT_GREEN}{cur_time} - {text} {color.RESET}")
  
  if status == 'warning':
    print(f"{color.YELLOW}{cur_time} - {text} {color.RESET}")

  if status == 'error':
    print(f"{color.RED}{cur_time} - {text} {color.RESET}")

"""
twitter.oauth.OAuth(access_token_key, access_token_secret, consumer_key, consumer_secret)
"""

auth_1 = twitter.oauth.OAuth("XXXXXXXXXXXXXXXXXXXXXXXXXX", "XXXXXXXXXXXXXXXXXXXXXXXXXX", "XXXXXXXXXXXXXXXXXXXXXXXXXX", "XXXXXXXXXXXXXXXXXXXXXXXXXX")
key_1 = twitter.Twitter(auth=auth_1)

twitter_at = re.compile('@\w+')

t_pattern = re.compile('t\.co\/\w+')

def trim_t_co_link(input):
  is_t = t_pattern.search(input)
  t_co = f"https://{is_t.group(0)}"
  input = input.replace(t_co, '')
  output = input
  return str(output)

def fix_format(input):
  input = input.replace("&lt;", "<")
  input = input.replace("&gt;", ">")
  input = input.replace("&amp;", "&")
  try:
    input = trim_t_co_link(input)
  except Exception as e:
    input = input

  output = input

  # has_at = twitter_at.search(output)
  # output = output.replace(f"{has_at.group(0)}", f"[{has_at.group(0)}](https://twitter.com/{has_at.group(0)})")

  return str(output)

def data_type_convert(url):
  if (url.find(".jpg") != -1):
    url = url
  else:
    url = url + ".jpg"

  # ghetto but we don't care at all because it works
  if (url.find(".png.jpg") != -1):
    url = url.replace('.jpg', '')

  fixed_url = url

  fixed_url = fixed_url + "?name=large"

  return str(fixed_url)

def grab_playback_data(response, post_type):
  if (post_type == 'animated_gif'):
    if response['extended_entities']['media'][0]['video_info']['variants']:
        for video in response['extended_entities']['media'][0]['video_info']['variants']:
            if video['content_type'] == "video/mp4":
              output_url = video['url']

        output_url = output_url.replace('?tag=12', '')
      
    return output_url

  if (post_type == 'video'):
    if response['extended_entities']['media'][0]['video_info']['variants']:

      bitrate_value_1 = 0
      bitrate_value_2 = 0
      bitrate_value_3 = 0

      index = 0
      for video in response['extended_entities']['media'][0]['video_info']['variants']:
        if video['content_type'] == "video/mp4":

          if index == 0:
            bitrate_value_1 = video['bitrate']

          if index == 1:
            bitrate_value_2 = video['bitrate']

          if index == 2:
            bitrate_value_3 = video['bitrate']

          index = index + 1

          bitrate_list = [bitrate_value_1, bitrate_value_2, bitrate_value_3]

          if video['bitrate'] ==  max(bitrate_list):
            output_url = video['url']

      output_url = output_url.replace('?tag=12', '')

    return output_url

def tweet_type(response):
  try:
    type_field = response['extended_entities']['media'][0]['type']

    if ('photo' in  type_field or 'animated_gif' in type_field or 'video' in type_field):
      out = 'multi_media'
      return out
  except Exception as e:
    out = 'text'
    return out

def image_type(response):
  image_field = len(response['extended_entities']['media'])

  if image_field == 1:
    out = 'single_image'
  elif image_field > 1:
    out = 'multi_image'

  return str(out)

class GetTweetData:
  def __init__(self, token):
    self.token = token
    # self.base_url = 'https://api.twitter.com/2/tweets/'
    # self.headers = {'authorization': f'Bearer {self.token}'}
    
    # self.params = {
    #   'tweet.fields': 'public_metrics',
    #   'expansions': 'author_id,attachments.media_keys',
    #   'user.fields': 'name,profile_image_url',
    #   'media.fields': 'type,url'
    # }

      return response

  def getTweetData(self, id):
    dto = _DTO().returnDTO

    response = key_1.statuses.show(_id=id, tweet_mode="extended")

    dto['media_type'] = tweet_type(response)


    if (tweet_type(response) == 'multi_media'):
      try:
        post_type = response['extended_entities']['media'][0]['type']
        dto['post_type'] = post_type

        # multiple image support
        index = 0
        for el in response['extended_entities']['media']:
          
          # since we count from 0, 1 is our 2nd, 3rd, 4th post image
          if index == 1:
            dto['2nd_post_image'] = data_type_convert(response['extended_entities']['media'][1]['media_url_https'])
          if index == 2:
            dto['3rd_post_image'] = data_type_convert(response['extended_entities']['media'][2]['media_url_https'])
          if index == 3:
            dto['4th_post_image'] = data_type_convert(response['extended_entities']['media'][3]['media_url_https'])

          index = index + 1

        # looks over image posts
        if (post_type == 'photo'):
          dto['profile_handle'] = response['user']['screen_name']
          dto['profile_image'] = response['user']['profile_image_url_https']
          dto['post_url'] =  'twitter.com/{}/status/{}'.format(dto['profile_handle'], id)
          dto['post_image'] = data_type_convert(response['extended_entities']['media'][0]['media_url_https'])
          dto['total_images'] = len(response['extended_entities']['media'])
          dto['display_name'] = response['user']['name']
          dto['post_text'] = fix_format(response['full_text'])
          dto['likes'] = response['favorite_count']
          dto['retweets'] = response['retweet_count']
          dto['image_type'] = image_type(response)

        # looks over gif posts
        if (post_type == 'animated_gif'):
          dto['gif_url'] = grab_playback_data(response, "animated_gif")
          dto['profile_handle'] = response['user']['screen_name']
          dto['profile_image'] = response['user']['profile_image_url_https']
          dto['post_url'] =  'twitter.com/{}/status/{}'.format(dto['profile_handle'], id)
          dto['post_image'] = data_type_convert(response['extended_entities']['media'][0]['media_url_https'])
          dto['display_name'] = response['user']['name']
          dto['post_text'] = fix_format(response['full_text'])
          dto['likes'] = response['favorite_count']
          dto['retweets'] = response['retweet_count']

        # looks over video posts
        if (post_type == 'video'):
          dto['video_url'] = grab_playback_data(response, "video")
          dto['profile_handle'] = response['user']['screen_name']
          dto['profile_image'] = response['user']['profile_image_url_https']
          dto['post_url'] =  'twitter.com/{}/status/{}'.format(dto['profile_handle'], id)
          dto['post_image_low_res'] = data_type_convert(response['extended_entities']['media'][0]['media_url_https'])
          dto['display_name'] = response['user']['name']
          dto['post_text'] = fix_format(response['full_text'])
          dto['likes'] = response['favorite_count']
          dto['retweets'] = response['retweet_count']

    # media key doesn't exist or something
      except KeyError:
        return None
      except Exception as e:
        return str(e)

    elif (tweet_type(response) == 'text'):
      try:
        dto['profile_handle'] = response['user']['screen_name']
        dto['profile_image'] = response['user']['profile_image_url_https']
        dto['post_url'] =  'twitter.com/{}/status/{}'.format(dto['profile_handle'], id)
        dto['display_name'] = response['user']['name']
        dto['post_text'] = fix_format(response['full_text'])
        dto['likes'] = response['favorite_count']
        dto['retweets'] = response['retweet_count']
        
      except KeyError:
        return None
      except Exception as e:
        print(e)
        return str(e)


    return dto

class _DTO:
  returnDTO = {
    'id': None,
    'image_index_count': None,
    'gif_url': None,
    'video_url': None,
    'media_type':  None,
    'post_type':  None,
    'profile_handle': None,
    'profile_image': None,
    '2nd_post_image': None,
    '3rd_post_image': None,
    '4th_post_image': None,
    'post_url': None,
    'total_images': None,
    'display_name': None,
    'post_text': None,
    'likes': None,
    'retweets': None,
    'image_type': None
  }