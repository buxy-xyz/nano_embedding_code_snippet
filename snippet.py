twitter_pattern = re.compile('twitter\.com\/\w+\/status\/(\d+)')
ayytwitter_pattern = re.compile('ayytwitter\.com\/\w+\/status\/(\d+)')
txwtter_pattern = re.compile('twxtter\.com\/\w+\/status\/(\d+)')
twitter64_pattern = re.compile('twitter64\.com\/\w+\/status\/(\d+)')
vxtwitter_pattern = re.compile('fxtwitter\.com\/\w+\/status\/(\d+)')


async def fix(message):

  msg = message.content
  ctx = message.channel

  is_tweet = twitter_pattern.search(msg)
  is_tweet64 = twitter64_pattern.search(msg)
  is_vxtweet = vxtwitter_pattern.search(msg)
  is_ayytweet = ayytwitter_pattern.search(msg)
  is_txwtweet = txwtter_pattern.search(msg)

  if (is_tweet or is_vxtweet or is_tweet64 or is_ayytweet or is_txwtweet):
    
    if (is_tweet):
      tweet_id = is_tweet.group(1)
    elif (is_vxtweet):
      tweet_id = is_vxtweet.group(1)
    elif (is_tweet64):
      tweet_id = is_tweet64.group(1)
    elif (is_ayytweet):
      tweet_id = is_ayytweet.group(1)
    elif (is_txwtweet):
      tweet_id = is_txwtweet.group(1)

    try:

      t = GetTweetData(twitter_token)
      response = t.getTweetData(tweet_id)

      media_type = response['media_type']

      if (media_type == 'multi_media'):

        # because this shit can fail

            post_type = response['post_type']

            if (post_type == 'photo'):

              profile_custom_name = response['display_name']
              profile_fixed_name = response['profile_handle']
              profile_image_url = response['profile_image']
              post_url =  f"https://{response['post_url']}"
              post_image = response['post_image']
              post_likes =  response['likes']
              post_retweets = response['retweets']
              post_text = response['post_text']
              post_image_count = response['total_images']

              profile_display_name = profile_custom_name + ' (@' + profile_fixed_name + ')'

              # remove '_normal' at the profile icon url causes twitter to output the semi full size
              profile_image_url = profile_image_url.replace('_normal', '')

              # print("after convert: " + post_image)

              source_link = f"[Link]({post_url})"

              embed_twitter = nextcord.Embed( description=post_text, color=color_picker(post_image) ) #1940464

              embed_twitter.set_author(name=profile_display_name, url=post_url, icon_url=profile_image_url)
              embed_twitter.set_thumbnail(url=profile_image_url)

              if post_likes != 0:
                embed_twitter.add_field(name="Likes", value=post_likes, inline=True)

              if post_retweets != 0:
                embed_twitter.add_field(name="Retweets", value=post_retweets, inline=True)

              if post_image_count >= 2:
                embed_twitter.add_field(name="Images", value=post_image_count, inline=True)

              embed_twitter.add_field(name="Source", value=source_link, inline=True)

              embed_twitter.set_image(url=post_image)

              # embed_twitter.set_thumbnail(url=message.author.display_avatar)

              if post_image_count == 1:
                embed_twitter.set_footer(text="Twitter  •  Nano", icon_url="https://i.imgur.com/vJJe2Ws.png")

              sent_message = await message.reply(embed=embed_twitter, mention_author=False)
              nano_message_id = sent_message.id

              if post_image_count >= 2:

                post_image_2nd = response['2nd_post_image']

                embed_twitter = nextcord.Embed( color=color_picker(post_image_2nd) )

                # print("after convert: " + post_image_2nd)

                embed_twitter.set_image(url=post_image_2nd)

                if post_image_count == 2:
                  embed_twitter.set_footer(text="Twitter  •  Nano", icon_url="https://i.imgur.com/vJJe2Ws.png")

                sent_message = await ctx.send(embed=embed_twitter)
                nano_message_id = sent_message.id
              
              if post_image_count >= 3:

                post_image_3rd = response['3rd_post_image']

                embed_twitter = nextcord.Embed( color=color_picker(post_image_3rd) )

                # print("after convert: " + post_image_3rd)

                embed_twitter.set_image(url=post_image_3rd)

                if post_image_count == 3:
                  embed_twitter.set_footer(text="Twitter  •  Nano", icon_url="https://i.imgur.com/vJJe2Ws.png")

                sent_message = await ctx.send(embed=embed_twitter)
                nano_message_id = sent_message.id

              if post_image_count >= 4:

                post_image_4th = response['4th_post_image']

                embed_twitter = nextcord.Embed( color=color_picker(post_image_4th) )

                # print("after convert: " + post_image_4th)

                embed_twitter.set_image(url=post_image_4th)

                if post_image_count == 4:
                  embed_twitter.set_footer(text="Twitter  •  Nano", icon_url="https://i.imgur.com/vJJe2Ws.png")

                sent_message = await ctx.send(embed=embed_twitter)
                nano_message_id = sent_message.id

              await suppress_embed(message)

            if (post_type == 'animated_gif'):

              gif_url = response['gif_url']

              sent_message = await message.reply("> " + gif_url, mention_author=False)
              nano_message_id = sent_message.id

              profile_custom_name = response['display_name']
              profile_fixed_name = response['profile_handle']
              profile_image_url = response['profile_image']
              post_url =  f"https://{response['post_url']}"
              post_likes =  response['likes']
              post_retweets = response['retweets']
              post_text = response['post_text']
              post_image = response['post_image']
              post_image_count = response['total_images']

              profile_image_url = profile_image_url.replace('_normal', '')

              profile_display_name = profile_custom_name + ' (@' + profile_fixed_name + ')'

              source_link = f"[Link]({post_url})"

              download_link = f"[Link]({gif_url})"

              embed_twitter = nextcord.Embed( description=post_text, color=color_picker(post_image) )

              embed_twitter.set_author(name=profile_display_name, url=post_url, icon_url=profile_image_url)

              embed_twitter.set_thumbnail(url=post_image)

              # embed_twitter.set_thumbnail(url=profile_image_url)

              if post_likes != 0:
                embed_twitter.add_field(name="Likes", value=post_likes, inline=True)

              if post_retweets != 0:
                embed_twitter.add_field(name="Retweets", value=post_retweets, inline=True)

              embed_twitter.add_field(name="Source", value=source_link, inline=True)

              embed_twitter.add_field(name="Download", value=download_link, inline=False)
              embed_twitter.set_footer(text="Twitter  •  Nano", icon_url="https://i.imgur.com/vJJe2Ws.png")

              # sent_message = await message.reply(file=file, embed=embed_twitter)
              sent_message = await ctx.send(embed=embed_twitter)
              nano_message_id = sent_message.id

              reaction_message = await message.channel.fetch_message(nano_message_id)
              await reaction_message.add_reaction('<:gif:978012587088285767>')

              await suppress_embed(message)

            if (post_type == 'video'):

              video_url = response['video_url']

              sent_message = await message.reply("> " + video_url, mention_author=False)
              nano_message_id = sent_message.id

              profile_custom_name = response['display_name']
              profile_fixed_name = response['profile_handle']
              profile_image_url = response['profile_image']
              post_url =  f"https://{response['post_url']}"
              post_likes =  response['likes']
              post_retweets = response['retweets']
              post_text = response['post_text']
              post_image = response['post_image']
              post_image_count = response['total_images']

              profile_display_name = profile_custom_name + ' (@' + profile_fixed_name + ')'

              source_link = f"[Link]({post_url})"

              embed_twitter = nextcord.Embed( description=post_text, color=color_picker(post_image) )

              embed_twitter.set_author(name=profile_display_name, url=post_url, icon_url=profile_image_url)
              embed_twitter.set_thumbnail(url=post_image)

              if post_likes != 0:
                embed_twitter.add_field(name="Likes", value=post_likes, inline=True)

              if post_retweets != 0:
                embed_twitter.add_field(name="Retweets", value=post_retweets, inline=True)
                
              embed_twitter.add_field(name="Source", value=source_link, inline=True)

              embed_twitter.set_footer(text="Twitter  •  Nano", icon_url="https://i.imgur.com/vJJe2Ws.png")

              sent_message = await ctx.send(embed=embed_twitter)
              nano_message_id = sent_message.id

              reaction_message = await message.channel.fetch_message(nano_message_id)
              await reaction_message.add_reaction('<:mp4:978012620063916162>')

              await suppress_embed(message)

      elif (media_type == 'text'):
          
        post_type = 'text'

        if (post_type == 'text'):

          # async with message.channel.typing():

          profile_custom_name = response['display_name']
          profile_fixed_name = response['profile_handle']
          profile_image_url = response['profile_image']
          post_url =  f"https://{response['post_url']}"
          post_likes =  response['likes']
          post_retweets = response['retweets']
          post_text = response['post_text']

          profile_display_name = profile_custom_name + ' (@' + profile_fixed_name + ')'

          # remove '_normal' at the profile icon url causes twitter to output the semi full size
          profile_image_url = profile_image_url.replace('_normal', '')

          # print("after convert: " + post_image)

          source_link = f"[Link]({post_url})"

          embed_twitter = nextcord.Embed( description=post_text, color=color_picker(profile_image_url) ) #1940464

          embed_twitter.set_author(name=profile_display_name, url=post_url, icon_url=profile_image_url)
          embed_twitter.set_thumbnail(url=profile_image_url)

          if post_likes != 0:
            embed_twitter.add_field(name="Likes", value=post_likes, inline=True)

          if post_retweets != 0:
            embed_twitter.add_field(name="Retweets", value=post_retweets, inline=True)

          embed_twitter.add_field(name="Source", value=source_link, inline=True)

          embed_twitter.set_footer(text="Twitter  •  Nano", icon_url="https://i.imgur.com/vJJe2Ws.png")

          sent_message = await message.reply(embed=embed_twitter, mention_author=False)
          nano_message_id = sent_message.id

          await suppress_embed(message)
# await suppress_embed(message)

    except Exception as e:
        embed_info = nextcord.Embed(description="An error occured.", color=1579032 )
        await ctx.send(embed=embed_info, delete_after=15)
        print(e)
        
        
@bot.event
async def on_message(message):

    if message.author.bot:
      return
    
    msg = message.content
    ctx = message.channel

    await fix(message)

    await bot.process_commands(message)