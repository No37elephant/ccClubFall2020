import os
import psycopg2
import flask
from flask import Flask, request, abort, render_template, json
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import (MessageEvent, TextMessage, TextSendMessage,
                            PostbackEvent, LocationMessage, FollowEvent,
                            QuickReply, QuickReplyButton, LocationAction,
                            URIAction, PostbackAction, TemplateSendMessage,
                            ButtonsTemplate, CarouselColumn, CarouselTemplate,
                            RichMenu, RichMenuArea, RichMenuBounds, RichMenuSize,
                            FlexSendMessage, ConfirmTemplate)

from random import randint
import pandas as pd
from haversine import haversine, Unit
import numpy
import random

#connecting database
conn = psycopg2.connect(database='d9gnei48mbovh8',
                        user='fusoiorzocvqjt',
                        password='f73bec6757bce818757e1a8894f40ca1a104ffa4459db7a62c424b71263b4bdd',
                        host='ec2-54-211-99-192.compute-1.amazonaws.com',port='5432')
conn.set_session(autocommit=True)

#bar_info
cur = conn.cursor()
cur.execute("select * from bar")
all_data = cur.fetchall()
df_bar = pd.DataFrame({'name':[n[0] for n in all_data], 'rating':[n[1] for n in all_data],
                       'address':[n[2] for n in all_data],'price':[n[3] for n in all_data],
                       'lat':[n[6] for n in all_data],'lng':[n[7] for n in all_data],
                       'review':[n[8] for n in all_data]
                  })


#image_info
lst = range(1, 33)
a, b, c, d, e= random.sample(lst,5)

cur.execute(f'select name, image_{a}, image_{b}, image_{c}, image_{d}, image_{e} from bar_image;')
all_data = cur.fetchall()

df_image = pd.DataFrame({'name':[n[0] for n in all_data],'image_0':[n[1] for n in all_data],
                        'image_1':[n[2] for n in all_data], 'image_2':[n[3] for n in all_data],
                        'image_3':[n[4] for n in all_data], 'image_4':[n[5] for n in all_data]})


#merge two dataframe, and get rid of duplicated ones
df = pd.merge(df_bar,df_image,on='name')
df.drop(df[df['name'].duplicated()].index, inplace=True)


#mrt_info
cur.execute("select * from taipei_mrt")
all_data = cur.fetchall()


df_mrt = pd.DataFrame({'station_code':[n[0] for n in all_data], 'station_name':[n[1] for n in all_data],
                       'lat':[n[2] for n in all_data], 'lng':[n[3] for n in all_data]
                      })

#cur.close()
#conn.close()


df_shortest, df_cost, df_rating = None, None, None


#handle review
def convert_review_to_json(review):
    review = review.replace('[','')
    review = review.replace(']','')
    review = review.replace("\'",'\"')
    review = eval(review)
    json.loads(json.dumps(review))
    return review


#終極密碼
lowest = 1
highest = 100
answer = randint(2, 99)
guess_round = 0



app = Flask(__name__)
line_bot_api = LineBotApi("ZRenw4zKciZ66CnPJYuRwqq35sQ1H/MVamEplfr1DTvRYHML1IVNsR9kJXPvccFTiMvyCx0fElkMm6cTvrvTa8GbpZeNHbHr/ww4CJyIvu1UOH91AvEvayalWceli7QM7+lt3ivY2UbjOm7sMxch5AdB04t89/1O/w1cDnyilFU=")
handler = WebhookHandler("ef182b4b1e515da5c715c480052207aa")


@app.route('/')
def index():
    return render_template('index.html', latitude=25.03, longitude=121.55)

@app.route('/<latitude>/<longitude>')
def index_location(latitude, longitude):
    return render_template('index.html', latitude=latitude, longitude=longitude)

@app.route("/callback", methods=['POST'])
def callback():

    signature = request.headers['X-Line-Signature']

    body = request.get_data(as_text=True)
    app.logger.info("Request body: "+ body)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

#welcome message
@handler.add(FollowEvent)
def follow_event(event):
    global cur
    
    user=event.source.user_id
    
    record = (f'{event.source.user_id}','false', 'false')
    table_columns = '(user_id, back_home, game_room)'
    
    try:
        postgres_insert_query=f"""insert into account {table_columns}
                                values (%s, %s, %s)"""
        cur.execute(postgres_insert_query, record)
    except:
        print(f'{event.source.user_id} already exist, processing the updates')
        
        user = event.source.user_id
        
        postgres_insert_query = f"""update account set back_home = 'f', game_room = 'f'
        where user_id = %s"""
        cur.execute(postgres_insert_query, (user,))
        print('Successfully updates')

    line_bot_api.reply_message(
        event.reply_token,
        FlexSendMessage(
            alt_text='hello',
            contents={
  "type": "bubble",
  "size": "mega",
  "hero": {
    "type": "image",
    "url": "https://no37elephant.github.io/logo-03.png",
    "size": "full",
    "aspectRatio": "20:15",
    "aspectMode": "cover",
    "offsetTop": "none",
    "margin": "none"
  },
  "body": {
    "type": "box",
    "layout": "vertical",
    "contents": [
      {
        "type": "text",
        "text": "【 Bar.py | 你的酒吧導航 】",
        "weight": "bold",
        "size": "lg",
        "color": "#464F69"
      },
      {
        "type": "box",
        "layout": "vertical",
        "margin": "lg",
        "spacing": "sm",
        "contents": [
          {
            "type": "box",
            "layout": "vertical",
            "spacing": "sm",
            "contents": []
          },
          {
            "type": "box",
            "layout": "vertical",
            "spacing": "sm",
            "contents": [
              {
                "type": "text",
                "text": "全台最完整的酒吧資訊就在這裡 🍺 要微",
                "size": "xs",
                "flex": 1,
                "margin": "none",
                "adjustMode": "shrink-to-fit"
              },
              {
                "type": "text",
                "text": "醺還是買醉，Bar.py都能找到最合你意的！",
                "size": "xs",
                "flex": 1,
                "margin": "sm",
                "adjustMode": "shrink-to-fit"
              }
            ]
          }
        ]
      },
      {
        "type": "separator",
        "margin": "lg"
      },
      {
        "type": "box",
        "layout": "vertical",
        "contents": [
          {
            "type": "text",
            "text": "使用說明",
            "margin": "md",
            "size": "md",
            "color": "#646f82"
          },
          {
            "type": "text",
            "text": "1. 告訴我們你的位置",
            "margin": "sm",
            "size": "sm"
          },
          {
            "type": "text",
            "text": "2. 按條件篩選酒吧",
            "margin": "sm",
            "size": "sm"
          },
          {
            "type": "text",
            "text": "3. 瀏覽我們的精選名單",
            "margin": "sm",
            "size": "sm"
          },
          {
            "type": "text",
            "text": "4. 前往酒吧！",
            "margin": "sm",
            "size": "sm"
          },
          {
            "type": "button",
            "action": {
              "type": "message",
              "label": "點我試試看",
              "text": "我想試試看"
            },
            "margin": "md",
            "style": "link",
            "color": "#03245c"
          }
        ]
      }
    ]
  }
}
    ))

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    
    user_id = event.source.user_id
    cur.execute(f'''select game_room, lowest, highest, round, answer from account where user_id='{user_id}' ''')
    game_state, lowest, highest, game_round, answer = cur.fetchone()
    
    if game_state:
        try:
            guess = int(event.message.text)
            print(game_round, game_round>10)
            
            if guess <= lowest or guess >= highest:
                    line_bot_api.reply_message(
                    event.reply_token,
                    TextSendMessage(text = f'醉了嗎？密碼介於{lowest}與{highest}之間誒！'))
                    game_round += 1
                    
                    if game_round > 10:
                        line_bot_api.push_message(
                        user_id,
                        TextSendMessage(text=f'''是不是不想玩了啊，都猜{game_round}次了！如果不想玩的話輸入 Quit 可以直接看答案喔！'''))

            elif guess < answer:
                    lowest = guess
                    line_bot_api.reply_message(
                    event.reply_token,
                    TextSendMessage(text = f'接近囉！密碼介於{lowest}與{highest}之間！'))
                    game_round += 1
                    
                    if game_round > 10:
                        line_bot_api.push_message(
                        user_id,
                        TextSendMessage(text=f'''是不是不想玩了啊，都猜{game_round}次了！如果不想玩的話輸入 Quit 可以直接看答案喔！'''))


            elif guess > answer:
                    highest = guess
                    line_bot_api.reply_message(
                    event.reply_token,
                    TextSendMessage(text = f'接近囉！密碼介於{lowest}與{highest}之間！'))
                    game_round += 1
                    
                    if game_round > 10:
                        line_bot_api.push_message(
                        user_id,
                        TextSendMessage(text=f'''是不是不想玩了啊，都猜{game_round}次了！如果不想玩的話輸入 Quit 可以直接看答案喔！'''))


            elif guess == answer:
                    if game_round < 3:
                        game_round += 1
                        line_bot_api.reply_message(
                        event.reply_token,
                        TextSendMessage(text = f'恭喜答對了，只猜{game_round}次就成功了，看樣子喝不夠！喝！喝！喝！'))
                    elif game_round >= 3 and game_round < 6:
                        game_round += 1
                        line_bot_api.reply_message(
                        event.reply_token,
                        TextSendMessage(text = f'恭喜答對了，你猜了{game_round}次，應該還能再喝一點喔！'))
                    else:
                        game_round += 1
                        line_bot_api.reply_message(
                        event.reply_token,
                        TextSendMessage(text = f'答對了！不過猜了{game_round}次才成功，該回家囉！使用『捷運回家』幫你找到最近的捷運站喔！'))
                    
                    line_bot_api.push_message(
                        user_id,
                        TemplateSendMessage(
                            alt_text=f'''再玩一次嗎？''',
                            template=ConfirmTemplate(
                                text='再玩一次嗎？',
                                actions=[
                                    PostbackAction(
                                    label='Yes',
                                    display_text='yes',
                                    data='終極密碼'
                                    ),
                                    
                                    PostbackAction(
                                    label='No',
                                    display_text='no',
                                    data='不要終極密碼')
                            ])))
                    
            
        except:
            
            guess = event.message.text
            
            if guess == 'Quit':
                line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text=f'''答案是{answer}'''))
                
                line_bot_api.push_message(
                        user_id,
                        TemplateSendMessage(
                            alt_text=f'''再玩一次嗎？''',
                            template=ConfirmTemplate(
                                text='再玩一次嗎？',
                                actions=[
                                    PostbackAction(
                                    label='Yes',
                                    display_text='yes',
                                    data='終極密碼'
                                    ),
                                    
                                    PostbackAction(
                                    label='No',
                                    display_text='no',
                                    data='不要終極密碼')
                            ])))
                
            else:
                line_bot_api.reply_message(
                    event.reply_token,
                    TextSendMessage(text=f'''誒誒誒，醒醒！{guess}不是整數啦！再試一次密碼介於{lowest}與{highest}之間。''')
                    )

                game_round += 1
                
        finally:
            
            postgres_update_query = f'''update account
                                        set lowest='{lowest}', highest='{highest}', round='{game_round}'
                                        where user_id = %s '''
            print(user_id)
            
            cur.execute(postgres_update_query, (user_id,))
            cur.execute(f'''select * from account where user_id = '{user_id}' ''')
            print(cur.fetchone())
    
    
    else:
        
        if event.message.text == '我想試試看':
            line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text='好～告訴我你的位置吧！\n \n對了！點擊下方「理性癮酒」可以重新開始，也有更多驚喜服務！😈',
                           quick_reply=QuickReply(items=[
                               QuickReplyButton(action=LocationAction(label='I am here.'))

                ])))


@handler.add(MessageEvent, message=LocationMessage)
def handle_location(event):
    
    print(event)
    
    global df, df_shortest, df_cost, df_rating, df_mrt, cur
    
    user_id = event.source.user_id
        
    postgres_insert_query = f"""select back_home from account where user_id = %s"""
    cur.execute(postgres_insert_query, (user_id,))
    state = cur.fetchone()[0]
    print(state)
    
    latitude = event.message.latitude
    longitude = event.message.longitude
    
    #計算距離
    user = (latitude, longitude)
    
    if state:
        df_mrt['dist'] = df_mrt.apply(lambda x: haversine(user, (x['lat'], x['lng'])), axis=1)
        df_mrt_shortest = df_mrt.sort_values(by=['dist'])
        
        line_bot_api.reply_message(
            event.reply_token,
            TemplateSendMessage(
                alt_text='Button',
                template=ButtonsTemplate(
                title='最近的捷運站',
                text=df_mrt_shortest['station_name'].iloc[0],
                actions=[
                    URIAction(
                        label='這樣去！',
                        uri=f"https://www.google.com/maps/search/?api=1&query={df_mrt_shortest['lat'].iloc[0]},{df_mrt_shortest['lng'].iloc[0]}"
                    )]
                )
            ))
        
        df_mrt.drop(['dist'], axis=1, inplace=True)
        
        postgres_insert_query = f"""update account set back_home = 'f' where user_id = %s"""
        cur.execute(postgres_insert_query, (user_id,))
        
    else:
        df['dist'] = df.apply(lambda x: haversine(user, (x['lat'], x['lng'])), axis=1)

        #最快醉
        df_shortest = df.sort_values(by=['dist']).head(10)
        #最便宜
        df_cost = df_shortest.sort_values(by=['price'])
        #最推薦
        df_rating = df_shortest.sort_values(by=['rating'], ascending=False)

        line_bot_api.reply_message(
            event.reply_token,
            TemplateSendMessage(
                alt_text='Buttons template',
                template=ButtonsTemplate(
                thumbnail_image_url='https://no37elephant.github.io/buttontemplate-04.png',
                text='你想怎麼喝！',
                actions=[
                    PostbackAction(
                        label='喝近的',
                        data='critera=shortest'
                    ),
                    PostbackAction(
                        label='喝便宜的',
                        data='criteria=cheapest'
                    ),
                    PostbackAction(
                        label='喝評分高的',
                        data='criteria=hotest'),
                    URIAction(
                        label='自己找不用推薦謝謝',
                        uri=f'https://ccbarbarbar.herokuapp.com/{latitude}/{longitude}'
                    )])
            )



        )
        df.drop(['dist'], axis=1, inplace=True)


@handler.add(PostbackEvent)
def handle_postback(event):
    
    global df_shortest, df_cost, df_rating, df, cur
    
    if '評論' in event.postback.data:
        print(event.postback.data)
        
        index = event.postback.data.split('@')[-1]
        review = df[df['name']==index]['review'].iloc[0]
        review = convert_review_to_json(review)
        review = random.sample(review,1)
        
        line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=f'''{review[0]['author_name']}覺得{index}：{review[0]['text']}'''))
        
    
    if event.postback.data == '重頭開始':
        line_bot_api.reply_message(
                event.reply_token,
                FlexSendMessage(alt_text='hello',
                contents={
  "type": "bubble",
  "size": "mega",
  "body": {
    "type": "box",
    "layout": "vertical",
    "contents": [
      {
        "type": "text",
        "text": "【 Bar.py | 你的酒吧導航 】",
        "weight": "bold",
        "size": "lg",
        "color": "#464F69"
      },
      {
        "type": "box",
        "layout": "vertical",
        "margin": "lg",
        "spacing": "sm",
        "contents": [
          {
            "type": "box",
            "layout": "vertical",
            "spacing": "sm",
            "contents": []
          },
          {
            "type": "box",
            "layout": "vertical",
            "spacing": "xs",
            "contents": [
              {
                "type": "text",
                "text": "全台最完整的酒吧資訊就在這裡 🍺 要微醺",
                "size": "xs",
                "flex": 1,
                "margin": "none",
                "adjustMode": "shrink-to-fit"
              },
              {
                "type": "text",
                "text": "還是買醉，Bar.py都能找到最合你意的！",
                "size": "xs",
                "flex": 1,
                "margin": "sm",
                "adjustMode": "shrink-to-fit"
              }
            ]
          }
        ]
      },
      {
        "type": "separator",
        "margin": "lg"
      },
      {
        "type": "box",
        "layout": "vertical",
        "contents": [
          {
            "type": "text",
            "text": "使用說明",
            "margin": "md",
            "size": "md",
            "color": "#646f82"
          },
          {
            "type": "text",
            "text": "1. 告訴我們你的位置",
            "margin": "sm",
            "size": "sm"
          },
          {
            "type": "text",
            "text": "2. 按條件篩選酒吧",
            "margin": "sm",
            "size": "sm"
          },
          {
            "type": "text",
            "text": "3. 瀏覽我們的精選名單",
            "margin": "sm",
            "size": "sm"
          },
          {
            "type": "text",
            "text": "4. 前往酒吧！",
            "margin": "sm",
            "size": "sm"
          },
          {
            "type": "button",
            "action": {
              "type": "message",
              "label": "點我試試看",
              "text": "我想試試看"
            },
            "margin": "md",
            "style": "link",
            "color": "#03245c",
            "adjustMode": "shrink-to-fit"
          }
        ]
      }
    ]
  }
}
                            ))
           
    if event.postback.data == '回家':
            
        user_id = event.source.user_id
        postgres_update_query = f"""update account set back_home = 't'
            where user_id = %s"""
        cur.execute(postgres_update_query, (user_id,))
            
        line_bot_api.reply_message(
            event.reply_token,
            TemplateSendMessage(
                alt_text='回家囉！',
                template=ButtonsTemplate(
                title='回家嗎？',
                text='我幫你找最近的捷運站！',
                actions=[LocationAction(
                label='告訴我你在哪？')])))
        
        
    
    if event.postback.data == '終極密碼':
            
            #initiallization
            
        lowest = 1
        highest = 100
        answer = randint(2, 99)
        guess_round = 0
            
        user_id = event.source.user_id
        postgres_update_query = f'''update account set
            game_room = 't', lowest='{lowest}', highest='{highest}', round='{guess_round}', answer='{answer}'
            where user_id = %s'''
            
        cur.execute(postgres_update_query, (user_id,))
            
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=f'測測看你的酒醉程度，來玩終極密碼吧，看你要花多少回合猜對我心中的數字，數字是整數喔！密碼介於{lowest}與{highest}之間。'))
        
    if event.postback.data == '不要終極密碼':
            
        user_id = event.source.user_id
        postgres_update_query = f'''update account set game_room='f' where user_id=%s '''
        cur.execute(postgres_update_query, (user_id,))
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text='好～那要去探索酒吧嗎？告訴我你在哪～',
                            quick_reply=QuickReply(items=[
                            QuickReplyButton(action=LocationAction(label='I am here.'))])))

    if event.postback.data=='critera=shortest':
            contents={
  "type": "carousel",
  "contents": [
    {
      "type": "bubble",
      "body": {
        "type": "box",
        "layout": "vertical",
        "contents": [
          {
            "type": "image",
            "url": f"{df_shortest['image_0'].iloc[0]}",
            "size": "full",
            "aspectMode": "cover",
            "aspectRatio": "2:3",
            "gravity": "top"
          },
          {
            "type": "box",
            "layout": "vertical",
            "contents": [
              {
                "type": "box",
                "layout": "vertical",
                "contents": [
                  {
                    "type": "text",
                    "text": f"{df_shortest['name'].iloc[0]}",
                    "size": "xl",
                    "color": "#ffffff",
                    "weight": "bold"
                  }
                ]
              },
              {
                "type": "box",
                "layout": "vertical",
                "contents": [
                  {
                    "type": "filler"
                  },
                  {
                    "type": "box",
                    "layout": "baseline",
                    "contents": [
                      {
                        "type": "filler"
                      },
                      {
                        "type": "text",
                        "text": "這樣去",
                        "color": "#ffffff",
                        "flex": 0,
                        "offsetTop": "-2px"
                      },
                      {
                        "type": "filler"
                      }
                    ],
                    "spacing": "sm"
                  },
                  {
                    "type": "filler"
                  }
                ],
                "borderWidth": "1px",
                "cornerRadius": "4px",
                "spacing": "sm",
                "borderColor": "#ffffff",
                "margin": "xl",
                "height": "40px",
                "action": {
                  "type": "uri",
                  "label": "action",
                  "uri": f"https://www.google.com/maps/search/?api=1&query={df_shortest['lat'].iloc[0]},{df_shortest['lng'].iloc[0]}"
                }
              },
              {
                "type": "box",
                "layout": "vertical",
                "contents": [
                  {
                    "type": "filler"
                  },
                  {
                    "type": "box",
                    "layout": "baseline",
                    "contents": [
                      {
                        "type": "filler"
                      },
                      {
                        "type": "text",
                        "text": "別人怎麼說",
                        "offsetTop": "0px",
                        "color": "#ffffff",
                        "size": "md",
                        "flex": 0,
                        "align": "center"
                      },
                      {
                        "type": "filler"
                      }
                    ],
                    "spacing": "sm"
                  },
                  {
                    "type": "filler"
                  }
                ],
                "height": "40px",
                "cornerRadius": "4px",
                "borderWidth": "1px",
                "borderColor": "#ffffff",
                "margin": "lg",
                "action": {
                  "type": "postback",
                  "label": "action",
                  "data": f'''評論@{df_shortest['name'].iloc[0]}'''
                }
              }
            ],
            "position": "absolute",
            "offsetBottom": "0px",
            "offsetStart": "0px",
            "offsetEnd": "0px",
            "backgroundColor": "#03303Acc",
            "paddingAll": "20px",
            "paddingTop": "18px"
          },
          {
            "type": "box",
            "layout": "vertical",
            "contents": [
              {
                "type": "text",
                "text": "No.1",
                "color": "#ffffff",
                "align": "center",
                "size": "xs",
                "offsetTop": "3px"
              }
            ],
            "position": "absolute",
            "cornerRadius": "20px",
            "offsetTop": "18px",
            "backgroundColor": "#ff334bcc",
            "offsetStart": "18px",
            "height": "25px",
            "width": "53px"
          }
        ],
        "paddingAll": "0px"
      }
    },
  {
      "type": "bubble",
      "body": {
        "type": "box",
        "layout": "vertical",
        "contents": [
          {
            "type": "image",
            "url": f"{df_shortest['image_0'].iloc[1]}",
            "size": "full",
            "aspectMode": "cover",
            "aspectRatio": "2:3",
            "gravity": "top"
          },
          {
            "type": "box",
            "layout": "vertical",
            "contents": [
              {
                "type": "box",
                "layout": "vertical",
                "contents": [
                  {
                    "type": "text",
                    "text": f"{df_shortest['name'].iloc[1]}",
                    "size": "xl",
                    "color": "#ffffff",
                    "weight": "bold"
                  }
                ]
              },
              {
                "type": "box",
                "layout": "vertical",
                "contents": [
                  {
                    "type": "filler"
                  },
                  {
                    "type": "box",
                    "layout": "baseline",
                    "contents": [
                      {
                        "type": "filler"
                      },
                      {
                        "type": "text",
                        "text": "這樣去",
                        "color": "#ffffff",
                        "flex": 0,
                        "offsetTop": "-2px"
                      },
                      {
                        "type": "filler"
                      }
                    ],
                    "spacing": "sm"
                  },
                  {
                    "type": "filler"
                  }
                ],
                "borderWidth": "1px",
                "cornerRadius": "4px",
                "spacing": "sm",
                "borderColor": "#ffffff",
                "margin": "xl",
                "height": "40px",
                "action": {
                  "type": "uri",
                  "label": "action",
                  "uri": f"https://www.google.com/maps/search/?api=1&query={df_shortest['lat'].iloc[1]},{df_shortest['lng'].iloc[1]}"
                }
              },
              {
                "type": "box",
                "layout": "vertical",
                "contents": [
                  {
                    "type": "filler"
                  },
                  {
                    "type": "box",
                    "layout": "baseline",
                    "contents": [
                      {
                        "type": "filler"
                      },
                      {
                        "type": "text",
                        "text": "別人怎麼說",
                        "offsetTop": "0px",
                        "color": "#ffffff",
                        "size": "md",
                        "flex": 0,
                        "align": "center"
                      },
                      {
                        "type": "filler"
                      }
                    ],
                    "spacing": "sm"
                  },
                  {
                    "type": "filler"
                  }
                ],
                "height": "40px",
                "cornerRadius": "4px",
                "borderWidth": "1px",
                "borderColor": "#ffffff",
                "margin": "lg",
                "action": {
                  "type": "postback",
                  "label": "action",
                  "data": f'''評論@{df_shortest['name'].iloc[1]}'''
                }
              }
            ],
            "position": "absolute",
            "offsetBottom": "0px",
            "offsetStart": "0px",
            "offsetEnd": "0px",
            "backgroundColor": "#03303Acc",
            "paddingAll": "20px",
            "paddingTop": "18px"
          },
          {
            "type": "box",
            "layout": "vertical",
            "contents": [
              {
                "type": "text",
                "text": "No.2",
                "color": "#ffffff",
                "align": "center",
                "size": "xs",
                "offsetTop": "3px"
              }
            ],
            "position": "absolute",
            "cornerRadius": "20px",
            "offsetTop": "18px",
            "backgroundColor": "#ff334bcc",
            "offsetStart": "18px",
            "height": "25px",
            "width": "53px"
          }
        ],
        "paddingAll": "0px"
      }
    },{
      "type": "bubble",
      "body": {
        "type": "box",
        "layout": "vertical",
        "contents": [
          {
            "type": "image",
            "url": f"{df_shortest['image_0'].iloc[2]}",
            "size": "full",
            "aspectMode": "cover",
            "aspectRatio": "2:3",
            "gravity": "top"
          },
          {
            "type": "box",
            "layout": "vertical",
            "contents": [
              {
                "type": "box",
                "layout": "vertical",
                "contents": [
                  {
                    "type": "text",
                    "text": f"{df_shortest['name'].iloc[2]}",
                    "size": "xl",
                    "color": "#ffffff",
                    "weight": "bold"
                  }
                ]
              },
              {
                "type": "box",
                "layout": "vertical",
                "contents": [
                  {
                    "type": "filler"
                  },
                  {
                    "type": "box",
                    "layout": "baseline",
                    "contents": [
                      {
                        "type": "filler"
                      },
                      {
                        "type": "text",
                        "text": "這樣去",
                        "color": "#ffffff",
                        "flex": 0,
                        "offsetTop": "-2px"
                      },
                      {
                        "type": "filler"
                      }
                    ],
                    "spacing": "sm"
                  },
                  {
                    "type": "filler"
                  }
                ],
                "borderWidth": "1px",
                "cornerRadius": "4px",
                "spacing": "sm",
                "borderColor": "#ffffff",
                "margin": "xl",
                "height": "40px",
                "action": {
                  "type": "uri",
                  "label": "action",
                  "uri": f"https://www.google.com/maps/search/?api=1&query={df_shortest['lat'].iloc[2]},{df_shortest['lng'].iloc[2]}"
                }
              },
              {
                "type": "box",
                "layout": "vertical",
                "contents": [
                  {
                    "type": "filler"
                  },
                  {
                    "type": "box",
                    "layout": "baseline",
                    "contents": [
                      {
                        "type": "filler"
                      },
                      {
                        "type": "text",
                        "text": "別人怎麼說",
                        "offsetTop": "0px",
                        "color": "#ffffff",
                        "size": "md",
                        "flex": 0,
                        "align": "center"
                      },
                      {
                        "type": "filler"
                      }
                    ],
                    "spacing": "sm"
                  },
                  {
                    "type": "filler"
                  }
                ],
                "height": "40px",
                "cornerRadius": "4px",
                "borderWidth": "1px",
                "borderColor": "#ffffff",
                "margin": "lg",
                "action": {
                  "type": "postback",
                  "label": "action",
                  "data": f'''評論@{df_shortest['name'].iloc[2]}'''
                }
              }
            ],
            "position": "absolute",
            "offsetBottom": "0px",
            "offsetStart": "0px",
            "offsetEnd": "0px",
            "backgroundColor": "#03303Acc",
            "paddingAll": "20px",
            "paddingTop": "18px"
          },
          {
            "type": "box",
            "layout": "vertical",
            "contents": [
              {
                "type": "text",
                "text": "No.3",
                "color": "#ffffff",
                "align": "center",
                "size": "xs",
                "offsetTop": "3px"
              }
            ],
            "position": "absolute",
            "cornerRadius": "20px",
            "offsetTop": "18px",
            "backgroundColor": "#ff334bcc",
            "offsetStart": "18px",
            "height": "25px",
            "width": "53px"
          }
        ],
        "paddingAll": "0px"
      }
    },{
      "type": "bubble",
      "body": {
        "type": "box",
        "layout": "vertical",
        "contents": [
          {
            "type": "image",
            "url": f"{df_shortest['image_0'].iloc[3]}",
            "size": "full",
            "aspectMode": "cover",
            "aspectRatio": "2:3",
            "gravity": "top"
          },
          {
            "type": "box",
            "layout": "vertical",
            "contents": [
              {
                "type": "box",
                "layout": "vertical",
                "contents": [
                  {
                    "type": "text",
                    "text": f"{df_shortest['name'].iloc[3]}",
                    "size": "xl",
                    "color": "#ffffff",
                    "weight": "bold"
                  }
                ]
              },
              {
                "type": "box",
                "layout": "vertical",
                "contents": [
                  {
                    "type": "filler"
                  },
                  {
                    "type": "box",
                    "layout": "baseline",
                    "contents": [
                      {
                        "type": "filler"
                      },
                      {
                        "type": "text",
                        "text": "這樣去",
                        "color": "#ffffff",
                        "flex": 0,
                        "offsetTop": "-2px"
                      },
                      {
                        "type": "filler"
                      }
                    ],
                    "spacing": "sm"
                  },
                  {
                    "type": "filler"
                  }
                ],
                "borderWidth": "1px",
                "cornerRadius": "4px",
                "spacing": "sm",
                "borderColor": "#ffffff",
                "margin": "xl",
                "height": "40px",
                "action": {
                  "type": "uri",
                  "label": "action",
                  "uri": f"https://www.google.com/maps/search/?api=1&query={df_shortest['lat'].iloc[3]},{df_shortest['lng'].iloc[3]}"
                }
              },
              {
                "type": "box",
                "layout": "vertical",
                "contents": [
                  {
                    "type": "filler"
                  },
                  {
                    "type": "box",
                    "layout": "baseline",
                    "contents": [
                      {
                        "type": "filler"
                      },
                      {
                        "type": "text",
                        "text": "別人怎麼說",
                        "offsetTop": "0px",
                        "color": "#ffffff",
                        "size": "md",
                        "flex": 0,
                        "align": "center"
                      },
                      {
                        "type": "filler"
                      }
                    ],
                    "spacing": "sm"
                  },
                  {
                    "type": "filler"
                  }
                ],
                "height": "40px",
                "cornerRadius": "4px",
                "borderWidth": "1px",
                "borderColor": "#ffffff",
                "margin": "lg",
                "action": {
                  "type": "postback",
                  "label": "action",
                  "data": f'''評論@{df_shortest['name'].iloc[3]}'''
                }
              }
            ],
            "position": "absolute",
            "offsetBottom": "0px",
            "offsetStart": "0px",
            "offsetEnd": "0px",
            "backgroundColor": "#03303Acc",
            "paddingAll": "20px",
            "paddingTop": "18px"
          },
          {
            "type": "box",
            "layout": "vertical",
            "contents": [
              {
                "type": "text",
                "text": "No.4",
                "color": "#ffffff",
                "align": "center",
                "size": "xs",
                "offsetTop": "3px"
              }
            ],
            "position": "absolute",
            "cornerRadius": "20px",
            "offsetTop": "18px",
            "backgroundColor": "#ff334bcc",
            "offsetStart": "18px",
            "height": "25px",
            "width": "53px"
          }
        ],
        "paddingAll": "0px"
      }
    },{
      "type": "bubble",
      "body": {
        "type": "box",
        "layout": "vertical",
        "contents": [
          {
            "type": "image",
            "url": f"{df_shortest['image_0'].iloc[4]}",
            "size": "full",
            "aspectMode": "cover",
            "aspectRatio": "2:3",
            "gravity": "top"
          },
          {
            "type": "box",
            "layout": "vertical",
            "contents": [
              {
                "type": "box",
                "layout": "vertical",
                "contents": [
                  {
                    "type": "text",
                    "text": f"{df_shortest['name'].iloc[4]}",
                    "size": "xl",
                    "color": "#ffffff",
                    "weight": "bold"
                  }
                ]
              },
              {
                "type": "box",
                "layout": "vertical",
                "contents": [
                  {
                    "type": "filler"
                  },
                  {
                    "type": "box",
                    "layout": "baseline",
                    "contents": [
                      {
                        "type": "filler"
                      },
                      {
                        "type": "text",
                        "text": "這樣去",
                        "color": "#ffffff",
                        "flex": 0,
                        "offsetTop": "-2px"
                      },
                      {
                        "type": "filler"
                      }
                    ],
                    "spacing": "sm"
                  },
                  {
                    "type": "filler"
                  }
                ],
                "borderWidth": "1px",
                "cornerRadius": "4px",
                "spacing": "sm",
                "borderColor": "#ffffff",
                "margin": "xl",
                "height": "40px",
                "action": {
                  "type": "uri",
                  "label": "action",
                  "uri": f"https://www.google.com/maps/search/?api=1&query={df_shortest['lat'].iloc[4]},{df_shortest['lng'].iloc[4]}"
                }
              },
              {
                "type": "box",
                "layout": "vertical",
                "contents": [
                  {
                    "type": "filler"
                  },
                  {
                    "type": "box",
                    "layout": "baseline",
                    "contents": [
                      {
                        "type": "filler"
                      },
                      {
                        "type": "text",
                        "text": "別人怎麼說",
                        "offsetTop": "0px",
                        "color": "#ffffff",
                        "size": "md",
                        "flex": 0,
                        "align": "center"
                      },
                      {
                        "type": "filler"
                      }
                    ],
                    "spacing": "sm"
                  },
                  {
                    "type": "filler"
                  }
                ],
                "height": "40px",
                "cornerRadius": "4px",
                "borderWidth": "1px",
                "borderColor": "#ffffff",
                "margin": "lg",
                "action": {
                  "type": "postback",
                  "label": "action",
                  "data": f'''評論@{df_shortest['name'].iloc[4]}'''
                }
              }
            ],
            "position": "absolute",
            "offsetBottom": "0px",
            "offsetStart": "0px",
            "offsetEnd": "0px",
            "backgroundColor": "#03303Acc",
            "paddingAll": "20px",
            "paddingTop": "18px"
          },
          {
            "type": "box",
            "layout": "vertical",
            "contents": [
              {
                "type": "text",
                "text": "No.5",
                "color": "#ffffff",
                "align": "center",
                "size": "xs",
                "offsetTop": "3px"
              }
            ],
            "position": "absolute",
            "cornerRadius": "20px",
            "offsetTop": "18px",
            "backgroundColor": "#ff334bcc",
            "offsetStart": "18px",
            "height": "25px",
            "width": "53px"
          }
        ],
        "paddingAll": "0px"
      }
    }]
}
            line_bot_api.reply_message(
            event.reply_token,
            FlexSendMessage(
                alt_text='hello',
                contents=contents
            ))
    if event.postback.data=='criteria=cheapest':
        contents={
  "type": "carousel",
  "contents": [
    {
      "type": "bubble",
      "body": {
        "type": "box",
        "layout": "vertical",
        "contents": [
          {
            "type": "image",
            "url": f"{df_cost['image_0'].iloc[0]}",
            "size": "full",
            "aspectMode": "cover",
            "aspectRatio": "2:3",
            "gravity": "top"
          },
          {
            "type": "box",
            "layout": "vertical",
            "contents": [
              {
                "type": "box",
                "layout": "vertical",
                "contents": [
                  {
                    "type": "text",
                    "text": f"{df_cost['name'].iloc[0]}",
                    "size": "xl",
                    "color": "#ffffff",
                    "weight": "bold"
                  }
                ]
              },
              {
                "type": "box",
                "layout": "vertical",
                "contents": [
                  {
                    "type": "filler"
                  },
                  {
                    "type": "box",
                    "layout": "baseline",
                    "contents": [
                      {
                        "type": "filler"
                      },
                      {
                        "type": "text",
                        "text": "這樣去",
                        "color": "#ffffff",
                        "flex": 0,
                        "offsetTop": "-2px"
                      },
                      {
                        "type": "filler"
                      }
                    ],
                    "spacing": "sm"
                  },
                  {
                    "type": "filler"
                  }
                ],
                "borderWidth": "1px",
                "cornerRadius": "4px",
                "spacing": "sm",
                "borderColor": "#ffffff",
                "margin": "xl",
                "height": "40px",
                "action": {
                  "type": "uri",
                  "label": "action",
                  "uri": f"https://www.google.com/maps/search/?api=1&query={df_cost['lat'].iloc[0]},{df_cost['lng'].iloc[0]}"
                }
              },
              {
                "type": "box",
                "layout": "vertical",
                "contents": [
                  {
                    "type": "filler"
                  },
                  {
                    "type": "box",
                    "layout": "baseline",
                    "contents": [
                      {
                        "type": "filler"
                      },
                      {
                        "type": "text",
                        "text": "別人怎麼說",
                        "offsetTop": "0px",
                        "color": "#ffffff",
                        "size": "md",
                        "flex": 0,
                        "align": "center"
                      },
                      {
                        "type": "filler"
                      }
                    ],
                    "spacing": "sm"
                  },
                  {
                    "type": "filler"
                  }
                ],
                "height": "40px",
                "cornerRadius": "4px",
                "borderWidth": "1px",
                "borderColor": "#ffffff",
                "margin": "lg",
                "action": {
                  "type": "postback",
                  "label": "action",
                  "data": f'''評論@{df_cost['name'].iloc[0]}'''
                }
              }
            ],
            "position": "absolute",
            "offsetBottom": "0px",
            "offsetStart": "0px",
            "offsetEnd": "0px",
            "backgroundColor": "#03303Acc",
            "paddingAll": "20px",
            "paddingTop": "18px"
          },
          {
            "type": "box",
            "layout": "vertical",
            "contents": [
              {
                "type": "text",
                "text": "No.1",
                "color": "#ffffff",
                "align": "center",
                "size": "xs",
                "offsetTop": "3px"
              }
            ],
            "position": "absolute",
            "cornerRadius": "20px",
            "offsetTop": "18px",
            "backgroundColor": "#ff334bcc",
            "offsetStart": "18px",
            "height": "25px",
            "width": "53px"
          }
        ],
        "paddingAll": "0px"
      }
    },
  {
      "type": "bubble",
      "body": {
        "type": "box",
        "layout": "vertical",
        "contents": [
          {
            "type": "image",
            "url": f"{df_cost['image_0'].iloc[1]}",
            "size": "full",
            "aspectMode": "cover",
            "aspectRatio": "2:3",
            "gravity": "top"
          },
          {
            "type": "box",
            "layout": "vertical",
            "contents": [
              {
                "type": "box",
                "layout": "vertical",
                "contents": [
                  {
                    "type": "text",
                    "text": f"{df_cost['name'].iloc[1]}",
                    "size": "xl",
                    "color": "#ffffff",
                    "weight": "bold"
                  }
                ]
              },
              {
                "type": "box",
                "layout": "vertical",
                "contents": [
                  {
                    "type": "filler"
                  },
                  {
                    "type": "box",
                    "layout": "baseline",
                    "contents": [
                      {
                        "type": "filler"
                      },
                      {
                        "type": "text",
                        "text": "這樣去",
                        "color": "#ffffff",
                        "flex": 0,
                        "offsetTop": "-2px"
                      },
                      {
                        "type": "filler"
                      }
                    ],
                    "spacing": "sm"
                  },
                  {
                    "type": "filler"
                  }
                ],
                "borderWidth": "1px",
                "cornerRadius": "4px",
                "spacing": "sm",
                "borderColor": "#ffffff",
                "margin": "xl",
                "height": "40px",
                "action": {
                  "type": "uri",
                  "label": "action",
                  "uri": f"https://www.google.com/maps/search/?api=1&query={df_cost['lat'].iloc[1]},{df_cost['lng'].iloc[1]}"
                }
              },
              {
                "type": "box",
                "layout": "vertical",
                "contents": [
                  {
                    "type": "filler"
                  },
                  {
                    "type": "box",
                    "layout": "baseline",
                    "contents": [
                      {
                        "type": "filler"
                      },
                      {
                        "type": "text",
                        "text": "別人怎麼說",
                        "offsetTop": "0px",
                        "color": "#ffffff",
                        "size": "md",
                        "flex": 0,
                        "align": "center"
                      },
                      {
                        "type": "filler"
                      }
                    ],
                    "spacing": "sm"
                  },
                  {
                    "type": "filler"
                  }
                ],
                "height": "40px",
                "cornerRadius": "4px",
                "borderWidth": "1px",
                "borderColor": "#ffffff",
                "margin": "lg",
                "action": {
                  "type": "postback",
                  "label": "action",
                  "data": f'''評論@{df_cost['name'].iloc[1]}'''
                }
              }
            ],
            "position": "absolute",
            "offsetBottom": "0px",
            "offsetStart": "0px",
            "offsetEnd": "0px",
            "backgroundColor": "#03303Acc",
            "paddingAll": "20px",
            "paddingTop": "18px"
          },
          {
            "type": "box",
            "layout": "vertical",
            "contents": [
              {
                "type": "text",
                "text": "No.2",
                "color": "#ffffff",
                "align": "center",
                "size": "xs",
                "offsetTop": "3px"
              }
            ],
            "position": "absolute",
            "cornerRadius": "20px",
            "offsetTop": "18px",
            "backgroundColor": "#ff334bcc",
            "offsetStart": "18px",
            "height": "25px",
            "width": "53px"
          }
        ],
        "paddingAll": "0px"
      }
    },{
      "type": "bubble",
      "body": {
        "type": "box",
        "layout": "vertical",
        "contents": [
          {
            "type": "image",
            "url": f"{df_cost['image_0'].iloc[2]}",
            "size": "full",
            "aspectMode": "cover",
            "aspectRatio": "2:3",
            "gravity": "top"
          },
          {
            "type": "box",
            "layout": "vertical",
            "contents": [
              {
                "type": "box",
                "layout": "vertical",
                "contents": [
                  {
                    "type": "text",
                    "text": f"{df_cost['name'].iloc[2]}",
                    "size": "xl",
                    "color": "#ffffff",
                    "weight": "bold"
                  }
                ]
              },
              {
                "type": "box",
                "layout": "vertical",
                "contents": [
                  {
                    "type": "filler"
                  },
                  {
                    "type": "box",
                    "layout": "baseline",
                    "contents": [
                      {
                        "type": "filler"
                      },
                      {
                        "type": "text",
                        "text": "這樣去",
                        "color": "#ffffff",
                        "flex": 0,
                        "offsetTop": "-2px"
                      },
                      {
                        "type": "filler"
                      }
                    ],
                    "spacing": "sm"
                  },
                  {
                    "type": "filler"
                  }
                ],
                "borderWidth": "1px",
                "cornerRadius": "4px",
                "spacing": "sm",
                "borderColor": "#ffffff",
                "margin": "xl",
                "height": "40px",
                "action": {
                  "type": "uri",
                  "label": "action",
                  "uri": f"https://www.google.com/maps/search/?api=1&query={df_cost['lat'].iloc[2]},{df_cost['lng'].iloc[2]}"
                }
              },
              {
                "type": "box",
                "layout": "vertical",
                "contents": [
                  {
                    "type": "filler"
                  },
                  {
                    "type": "box",
                    "layout": "baseline",
                    "contents": [
                      {
                        "type": "filler"
                      },
                      {
                        "type": "text",
                        "text": "別人怎麼說",
                        "offsetTop": "0px",
                        "color": "#ffffff",
                        "size": "md",
                        "flex": 0,
                        "align": "center"
                      },
                      {
                        "type": "filler"
                      }
                    ],
                    "spacing": "sm"
                  },
                  {
                    "type": "filler"
                  }
                ],
                "height": "40px",
                "cornerRadius": "4px",
                "borderWidth": "1px",
                "borderColor": "#ffffff",
                "margin": "lg",
                "action": {
                  "type": "postback",
                  "label": "action",
                  "data": f'''評論@{df_cost['name'].iloc[2]}'''
                }
              }
            ],
            "position": "absolute",
            "offsetBottom": "0px",
            "offsetStart": "0px",
            "offsetEnd": "0px",
            "backgroundColor": "#03303Acc",
            "paddingAll": "20px",
            "paddingTop": "18px"
          },
          {
            "type": "box",
            "layout": "vertical",
            "contents": [
              {
                "type": "text",
                "text": "No.3",
                "color": "#ffffff",
                "align": "center",
                "size": "xs",
                "offsetTop": "3px"
              }
            ],
            "position": "absolute",
            "cornerRadius": "20px",
            "offsetTop": "18px",
            "backgroundColor": "#ff334bcc",
            "offsetStart": "18px",
            "height": "25px",
            "width": "53px"
          }
        ],
        "paddingAll": "0px"
      }
    },{
      "type": "bubble",
      "body": {
        "type": "box",
        "layout": "vertical",
        "contents": [
          {
            "type": "image",
            "url": f"{df_cost['image_0'].iloc[3]}",
            "size": "full",
            "aspectMode": "cover",
            "aspectRatio": "2:3",
            "gravity": "top"
          },
          {
            "type": "box",
            "layout": "vertical",
            "contents": [
              {
                "type": "box",
                "layout": "vertical",
                "contents": [
                  {
                    "type": "text",
                    "text": f"{df_cost['name'].iloc[3]}",
                    "size": "xl",
                    "color": "#ffffff",
                    "weight": "bold"
                  }
                ]
              },
              {
                "type": "box",
                "layout": "vertical",
                "contents": [
                  {
                    "type": "filler"
                  },
                  {
                    "type": "box",
                    "layout": "baseline",
                    "contents": [
                      {
                        "type": "filler"
                      },
                      {
                        "type": "text",
                        "text": "這樣去",
                        "color": "#ffffff",
                        "flex": 0,
                        "offsetTop": "-2px"
                      },
                      {
                        "type": "filler"
                      }
                    ],
                    "spacing": "sm"
                  },
                  {
                    "type": "filler"
                  }
                ],
                "borderWidth": "1px",
                "cornerRadius": "4px",
                "spacing": "sm",
                "borderColor": "#ffffff",
                "margin": "xl",
                "height": "40px",
                "action": {
                  "type": "uri",
                  "label": "action",
                  "uri": f"https://www.google.com/maps/search/?api=1&query={df_cost['lat'].iloc[3]},{df_cost['lng'].iloc[3]}"
                }
              },
              {
                "type": "box",
                "layout": "vertical",
                "contents": [
                  {
                    "type": "filler"
                  },
                  {
                    "type": "box",
                    "layout": "baseline",
                    "contents": [
                      {
                        "type": "filler"
                      },
                      {
                        "type": "text",
                        "text": "別人怎麼說",
                        "offsetTop": "0px",
                        "color": "#ffffff",
                        "size": "md",
                        "flex": 0,
                        "align": "center"
                      },
                      {
                        "type": "filler"
                      }
                    ],
                    "spacing": "sm"
                  },
                  {
                    "type": "filler"
                  }
                ],
                "height": "40px",
                "cornerRadius": "4px",
                "borderWidth": "1px",
                "borderColor": "#ffffff",
                "margin": "lg",
                "action": {
                  "type": "postback",
                  "label": "action",
                  "data": f'''評論@{df_cost['name'].iloc[3]}'''
                }
              }
            ],
            "position": "absolute",
            "offsetBottom": "0px",
            "offsetStart": "0px",
            "offsetEnd": "0px",
            "backgroundColor": "#03303Acc",
            "paddingAll": "20px",
            "paddingTop": "18px"
          },
          {
            "type": "box",
            "layout": "vertical",
            "contents": [
              {
                "type": "text",
                "text": "No.4",
                "color": "#ffffff",
                "align": "center",
                "size": "xs",
                "offsetTop": "3px"
              }
            ],
            "position": "absolute",
            "cornerRadius": "20px",
            "offsetTop": "18px",
            "backgroundColor": "#ff334bcc",
            "offsetStart": "18px",
            "height": "25px",
            "width": "53px"
          }
        ],
        "paddingAll": "0px"
      }
    },{
      "type": "bubble",
      "body": {
        "type": "box",
        "layout": "vertical",
        "contents": [
          {
            "type": "image",
            "url": f"{df_cost['image_0'].iloc[4]}",
            "size": "full",
            "aspectMode": "cover",
            "aspectRatio": "2:3",
            "gravity": "top"
          },
          {
            "type": "box",
            "layout": "vertical",
            "contents": [
              {
                "type": "box",
                "layout": "vertical",
                "contents": [
                  {
                    "type": "text",
                    "text": f"{df_cost['name'].iloc[4]}",
                    "size": "xl",
                    "color": "#ffffff",
                    "weight": "bold"
                  }
                ]
              },
              {
                "type": "box",
                "layout": "vertical",
                "contents": [
                  {
                    "type": "filler"
                  },
                  {
                    "type": "box",
                    "layout": "baseline",
                    "contents": [
                      {
                        "type": "filler"
                      },
                      {
                        "type": "text",
                        "text": "這樣去",
                        "color": "#ffffff",
                        "flex": 0,
                        "offsetTop": "-2px"
                      },
                      {
                        "type": "filler"
                      }
                    ],
                    "spacing": "sm"
                  },
                  {
                    "type": "filler"
                  }
                ],
                "borderWidth": "1px",
                "cornerRadius": "4px",
                "spacing": "sm",
                "borderColor": "#ffffff",
                "margin": "xl",
                "height": "40px",
                "action": {
                  "type": "uri",
                  "label": "action",
                  "uri": f"https://www.google.com/maps/search/?api=1&query={df_cost['lat'].iloc[4]},{df_cost['lng'].iloc[4]}"
                }
              },
              {
                "type": "box",
                "layout": "vertical",
                "contents": [
                  {
                    "type": "filler"
                  },
                  {
                    "type": "box",
                    "layout": "baseline",
                    "contents": [
                      {
                        "type": "filler"
                      },
                      {
                        "type": "text",
                        "text": "別人怎麼說",
                        "offsetTop": "0px",
                        "color": "#ffffff",
                        "size": "md",
                        "flex": 0,
                        "align": "center"
                      },
                      {
                        "type": "filler"
                      }
                    ],
                    "spacing": "sm"
                  },
                  {
                    "type": "filler"
                  }
                ],
                "height": "40px",
                "cornerRadius": "4px",
                "borderWidth": "1px",
                "borderColor": "#ffffff",
                "margin": "lg",
                "action": {
                  "type": "postback",
                  "label": "action",
                  "data": f'''評論@{df_cost['name'].iloc[4]}'''
                }
              }
            ],
            "position": "absolute",
            "offsetBottom": "0px",
            "offsetStart": "0px",
            "offsetEnd": "0px",
            "backgroundColor": "#03303Acc",
            "paddingAll": "20px",
            "paddingTop": "18px"
          },
          {
            "type": "box",
            "layout": "vertical",
            "contents": [
              {
                "type": "text",
                "text": "No.5",
                "color": "#ffffff",
                "align": "center",
                "size": "xs",
                "offsetTop": "3px"
              }
            ],
            "position": "absolute",
            "cornerRadius": "20px",
            "offsetTop": "18px",
            "backgroundColor": "#ff334bcc",
            "offsetStart": "18px",
            "height": "25px",
            "width": "53px"
          }
        ],
        "paddingAll": "0px"
      }
    }]
}

        line_bot_api.reply_message(
            event.reply_token,
            FlexSendMessage(
                alt_text='hello',
                contents=contents
            ))

    if event.postback.data=='criteria=hotest':
        contents={
  "type": "carousel",
  "contents": [
    {
      "type": "bubble",
      "body": {
        "type": "box",
        "layout": "vertical",
        "contents": [
          {
            "type": "image",
            "url": f"{df_rating['image_0'].iloc[0]}",
            "size": "full",
            "aspectMode": "cover",
            "aspectRatio": "2:3",
            "gravity": "top"
          },
          {
            "type": "box",
            "layout": "vertical",
            "contents": [
              {
                "type": "box",
                "layout": "vertical",
                "contents": [
                  {
                    "type": "text",
                    "text": f"{df_rating['name'].iloc[0]}",
                    "size": "xl",
                    "color": "#ffffff",
                    "weight": "bold"
                  }
                ]
              },
              {
                "type": "box",
                "layout": "vertical",
                "contents": [
                  {
                    "type": "filler"
                  },
                  {
                    "type": "box",
                    "layout": "baseline",
                    "contents": [
                      {
                        "type": "filler"
                      },
                      {
                        "type": "text",
                        "text": "這樣去",
                        "color": "#ffffff",
                        "flex": 0,
                        "offsetTop": "-2px"
                      },
                      {
                        "type": "filler"
                      }
                    ],
                    "spacing": "sm"
                  },
                  {
                    "type": "filler"
                  }
                ],
                "borderWidth": "1px",
                "cornerRadius": "4px",
                "spacing": "sm",
                "borderColor": "#ffffff",
                "margin": "xl",
                "height": "40px",
                "action": {
                  "type": "uri",
                  "label": "action",
                  "uri": f"https://www.google.com/maps/search/?api=1&query={df_rating['lat'].iloc[0]},{df_rating['lng'].iloc[0]}"
                }
              },
              {
                "type": "box",
                "layout": "vertical",
                "contents": [
                  {
                    "type": "filler"
                  },
                  {
                    "type": "box",
                    "layout": "baseline",
                    "contents": [
                      {
                        "type": "filler"
                      },
                      {
                        "type": "text",
                        "text": "別人怎麼說",
                        "offsetTop": "0px",
                        "color": "#ffffff",
                        "size": "md",
                        "flex": 0,
                        "align": "center"
                      },
                      {
                        "type": "filler"
                      }
                    ],
                    "spacing": "sm"
                  },
                  {
                    "type": "filler"
                  }
                ],
                "height": "40px",
                "cornerRadius": "4px",
                "borderWidth": "1px",
                "borderColor": "#ffffff",
                "margin": "lg",
                "action": {
                  "type": "postback",
                  "label": "action",
                  "data": f'''評論@{df_rating['name'].iloc[0]}'''
                }
              }
            ],
            "position": "absolute",
            "offsetBottom": "0px",
            "offsetStart": "0px",
            "offsetEnd": "0px",
            "backgroundColor": "#03303Acc",
            "paddingAll": "20px",
            "paddingTop": "18px"
          },
          {
            "type": "box",
            "layout": "vertical",
            "contents": [
              {
                "type": "text",
                "text": "No.1",
                "color": "#ffffff",
                "align": "center",
                "size": "xs",
                "offsetTop": "3px"
              }
            ],
            "position": "absolute",
            "cornerRadius": "20px",
            "offsetTop": "18px",
            "backgroundColor": "#ff334bcc",
            "offsetStart": "18px",
            "height": "25px",
            "width": "53px"
          }
        ],
        "paddingAll": "0px"
      }
    },
  {
      "type": "bubble",
      "body": {
        "type": "box",
        "layout": "vertical",
        "contents": [
          {
            "type": "image",
            "url": f"{df_cost['image_0'].iloc[1]}",
            "size": "full",
            "aspectMode": "cover",
            "aspectRatio": "2:3",
            "gravity": "top"
          },
          {
            "type": "box",
            "layout": "vertical",
            "contents": [
              {
                "type": "box",
                "layout": "vertical",
                "contents": [
                  {
                    "type": "text",
                    "text": f"{df_rating['name'].iloc[1]}",
                    "size": "xl",
                    "color": "#ffffff",
                    "weight": "bold"
                  }
                ]
              },
              {
                "type": "box",
                "layout": "vertical",
                "contents": [
                  {
                    "type": "filler"
                  },
                  {
                    "type": "box",
                    "layout": "baseline",
                    "contents": [
                      {
                        "type": "filler"
                      },
                      {
                        "type": "text",
                        "text": "這樣去",
                        "color": "#ffffff",
                        "flex": 0,
                        "offsetTop": "-2px"
                      },
                      {
                        "type": "filler"
                      }
                    ],
                    "spacing": "sm"
                  },
                  {
                    "type": "filler"
                  }
                ],
                "borderWidth": "1px",
                "cornerRadius": "4px",
                "spacing": "sm",
                "borderColor": "#ffffff",
                "margin": "xl",
                "height": "40px",
                "action": {
                  "type": "uri",
                  "label": "action",
                  "uri": f"https://www.google.com/maps/search/?api=1&query={df_rating['lat'].iloc[1]},{df_rating['lng'].iloc[1]}"
                }
              },
              {
                "type": "box",
                "layout": "vertical",
                "contents": [
                  {
                    "type": "filler"
                  },
                  {
                    "type": "box",
                    "layout": "baseline",
                    "contents": [
                      {
                        "type": "filler"
                      },
                      {
                        "type": "text",
                        "text": "別人怎麼說",
                        "offsetTop": "0px",
                        "color": "#ffffff",
                        "size": "md",
                        "flex": 0,
                        "align": "center"
                      },
                      {
                        "type": "filler"
                      }
                    ],
                    "spacing": "sm"
                  },
                  {
                    "type": "filler"
                  }
                ],
                "height": "40px",
                "cornerRadius": "4px",
                "borderWidth": "1px",
                "borderColor": "#ffffff",
                "margin": "lg",
                "action": {
                  "type": "postback",
                  "label": "action",
                  "data": f'''評論@{df_rating['name'].iloc[1]}'''
                }
              }
            ],
            "position": "absolute",
            "offsetBottom": "0px",
            "offsetStart": "0px",
            "offsetEnd": "0px",
            "backgroundColor": "#03303Acc",
            "paddingAll": "20px",
            "paddingTop": "18px"
          },
          {
            "type": "box",
            "layout": "vertical",
            "contents": [
              {
                "type": "text",
                "text": "No.2",
                "color": "#ffffff",
                "align": "center",
                "size": "xs",
                "offsetTop": "3px"
              }
            ],
            "position": "absolute",
            "cornerRadius": "20px",
            "offsetTop": "18px",
            "backgroundColor": "#ff334bcc",
            "offsetStart": "18px",
            "height": "25px",
            "width": "53px"
          }
        ],
        "paddingAll": "0px"
      }
    },{
      "type": "bubble",
      "body": {
        "type": "box",
        "layout": "vertical",
        "contents": [
          {
            "type": "image",
            "url": f"{df_rating['image_0'].iloc[2]}",
            "size": "full",
            "aspectMode": "cover",
            "aspectRatio": "2:3",
            "gravity": "top"
          },
          {
            "type": "box",
            "layout": "vertical",
            "contents": [
              {
                "type": "box",
                "layout": "vertical",
                "contents": [
                  {
                    "type": "text",
                    "text": f"{df_rating['name'].iloc[2]}",
                    "size": "xl",
                    "color": "#ffffff",
                    "weight": "bold"
                  }
                ]
              },
              {
                "type": "box",
                "layout": "vertical",
                "contents": [
                  {
                    "type": "filler"
                  },
                  {
                    "type": "box",
                    "layout": "baseline",
                    "contents": [
                      {
                        "type": "filler"
                      },
                      {
                        "type": "text",
                        "text": "這樣去",
                        "color": "#ffffff",
                        "flex": 0,
                        "offsetTop": "-2px"
                      },
                      {
                        "type": "filler"
                      }
                    ],
                    "spacing": "sm"
                  },
                  {
                    "type": "filler"
                  }
                ],
                "borderWidth": "1px",
                "cornerRadius": "4px",
                "spacing": "sm",
                "borderColor": "#ffffff",
                "margin": "xl",
                "height": "40px",
                "action": {
                  "type": "uri",
                  "label": "action",
                  "uri": f"https://www.google.com/maps/search/?api=1&query={df_rating['lat'].iloc[2]},{df_rating['lng'].iloc[2]}"
                }
              },
              {
                "type": "box",
                "layout": "vertical",
                "contents": [
                  {
                    "type": "filler"
                  },
                  {
                    "type": "box",
                    "layout": "baseline",
                    "contents": [
                      {
                        "type": "filler"
                      },
                      {
                        "type": "text",
                        "text": "別人怎麼說",
                        "offsetTop": "0px",
                        "color": "#ffffff",
                        "size": "md",
                        "flex": 0,
                        "align": "center"
                      },
                      {
                        "type": "filler"
                      }
                    ],
                    "spacing": "sm"
                  },
                  {
                    "type": "filler"
                  }
                ],
                "height": "40px",
                "cornerRadius": "4px",
                "borderWidth": "1px",
                "borderColor": "#ffffff",
                "margin": "lg",
                "action": {
                  "type": "postback",
                  "label": "action",
                  "data": f'''評論@{df_rating['name'].iloc[2]}'''
                }
              }
            ],
            "position": "absolute",
            "offsetBottom": "0px",
            "offsetStart": "0px",
            "offsetEnd": "0px",
            "backgroundColor": "#03303Acc",
            "paddingAll": "20px",
            "paddingTop": "18px"
          },
          {
            "type": "box",
            "layout": "vertical",
            "contents": [
              {
                "type": "text",
                "text": "No.3",
                "color": "#ffffff",
                "align": "center",
                "size": "xs",
                "offsetTop": "3px"
              }
            ],
            "position": "absolute",
            "cornerRadius": "20px",
            "offsetTop": "18px",
            "backgroundColor": "#ff334bcc",
            "offsetStart": "18px",
            "height": "25px",
            "width": "53px"
          }
        ],
        "paddingAll": "0px"
      }
    },{
      "type": "bubble",
      "body": {
        "type": "box",
        "layout": "vertical",
        "contents": [
          {
            "type": "image",
            "url": f"{df_rating['image_0'].iloc[3]}",
            "size": "full",
            "aspectMode": "cover",
            "aspectRatio": "2:3",
            "gravity": "top"
          },
          {
            "type": "box",
            "layout": "vertical",
            "contents": [
              {
                "type": "box",
                "layout": "vertical",
                "contents": [
                  {
                    "type": "text",
                    "text": f"{df_rating['name'].iloc[3]}",
                    "size": "xl",
                    "color": "#ffffff",
                    "weight": "bold"
                  }
                ]
              },
              {
                "type": "box",
                "layout": "vertical",
                "contents": [
                  {
                    "type": "filler"
                  },
                  {
                    "type": "box",
                    "layout": "baseline",
                    "contents": [
                      {
                        "type": "filler"
                      },
                      {
                        "type": "text",
                        "text": "這樣去",
                        "color": "#ffffff",
                        "flex": 0,
                        "offsetTop": "-2px"
                      },
                      {
                        "type": "filler"
                      }
                    ],
                    "spacing": "sm"
                  },
                  {
                    "type": "filler"
                  }
                ],
                "borderWidth": "1px",
                "cornerRadius": "4px",
                "spacing": "sm",
                "borderColor": "#ffffff",
                "margin": "xl",
                "height": "40px",
                "action": {
                  "type": "uri",
                  "label": "action",
                  "uri": f"https://www.google.com/maps/search/?api=1&query={df_rating['lat'].iloc[3]},{df_rating['lng'].iloc[3]}"
                }
              },
              {
                "type": "box",
                "layout": "vertical",
                "contents": [
                  {
                    "type": "filler"
                  },
                  {
                    "type": "box",
                    "layout": "baseline",
                    "contents": [
                      {
                        "type": "filler"
                      },
                      {
                        "type": "text",
                        "text": "別人怎麼說",
                        "offsetTop": "0px",
                        "color": "#ffffff",
                        "size": "md",
                        "flex": 0,
                        "align": "center"
                      },
                      {
                        "type": "filler"
                      }
                    ],
                    "spacing": "sm"
                  },
                  {
                    "type": "filler"
                  }
                ],
                "height": "40px",
                "cornerRadius": "4px",
                "borderWidth": "1px",
                "borderColor": "#ffffff",
                "margin": "lg",
                "action": {
                  "type": "postback",
                  "label": "action",
                  "data": f'''評論@{df_rating['name'].iloc[3]}'''
                }
              }
            ],
            "position": "absolute",
            "offsetBottom": "0px",
            "offsetStart": "0px",
            "offsetEnd": "0px",
            "backgroundColor": "#03303Acc",
            "paddingAll": "20px",
            "paddingTop": "18px"
          },
          {
            "type": "box",
            "layout": "vertical",
            "contents": [
              {
                "type": "text",
                "text": "No.4",
                "color": "#ffffff",
                "align": "center",
                "size": "xs",
                "offsetTop": "3px"
              }
            ],
            "position": "absolute",
            "cornerRadius": "20px",
            "offsetTop": "18px",
            "backgroundColor": "#ff334bcc",
            "offsetStart": "18px",
            "height": "25px",
            "width": "53px"
          }
        ],
        "paddingAll": "0px"
      }
    },{
      "type": "bubble",
      "body": {
        "type": "box",
        "layout": "vertical",
        "contents": [
          {
            "type": "image",
            "url": f"{df_rating['image_0'].iloc[4]}",
            "size": "full",
            "aspectMode": "cover",
            "aspectRatio": "2:3",
            "gravity": "top"
          },
          {
            "type": "box",
            "layout": "vertical",
            "contents": [
              {
                "type": "box",
                "layout": "vertical",
                "contents": [
                  {
                    "type": "text",
                    "text": f"{df_rating['name'].iloc[4]}",
                    "size": "xl",
                    "color": "#ffffff",
                    "weight": "bold"
                  }
                ]
              },
              {
                "type": "box",
                "layout": "vertical",
                "contents": [
                  {
                    "type": "filler"
                  },
                  {
                    "type": "box",
                    "layout": "baseline",
                    "contents": [
                      {
                        "type": "filler"
                      },
                      {
                        "type": "text",
                        "text": "這樣去",
                        "color": "#ffffff",
                        "flex": 0,
                        "offsetTop": "-2px"
                      },
                      {
                        "type": "filler"
                      }
                    ],
                    "spacing": "sm"
                  },
                  {
                    "type": "filler"
                  }
                ],
                "borderWidth": "1px",
                "cornerRadius": "4px",
                "spacing": "sm",
                "borderColor": "#ffffff",
                "margin": "xl",
                "height": "40px",
                "action": {
                  "type": "uri",
                  "label": "action",
                  "uri": f"https://www.google.com/maps/search/?api=1&query={df_rating['lat'].iloc[4]},{df_rating['lng'].iloc[4]}"
                }
              },
              {
                "type": "box",
                "layout": "vertical",
                "contents": [
                  {
                    "type": "filler"
                  },
                  {
                    "type": "box",
                    "layout": "baseline",
                    "contents": [
                      {
                        "type": "filler"
                      },
                      {
                        "type": "text",
                        "text": "別人怎麼說",
                        "offsetTop": "0px",
                        "color": "#ffffff",
                        "size": "md",
                        "flex": 0,
                        "align": "center"
                      },
                      {
                        "type": "filler"
                      }
                    ],
                    "spacing": "sm"
                  },
                  {
                    "type": "filler"
                  }
                ],
                "height": "40px",
                "cornerRadius": "4px",
                "borderWidth": "1px",
                "borderColor": "#ffffff",
                "margin": "lg",
                "action": {
                  "type": "postback",
                  "label": "action",
                  "data": f'''評論@{df_rating['name'].iloc[4]}'''
                }
              }
            ],
            "position": "absolute",
            "offsetBottom": "0px",
            "offsetStart": "0px",
            "offsetEnd": "0px",
            "backgroundColor": "#03303Acc",
            "paddingAll": "20px",
            "paddingTop": "18px"
          },
          {
            "type": "box",
            "layout": "vertical",
            "contents": [
              {
                "type": "text",
                "text": "No.5",
                "color": "#ffffff",
                "align": "center",
                "size": "xs",
                "offsetTop": "3px"
              }
            ],
            "position": "absolute",
            "cornerRadius": "20px",
            "offsetTop": "18px",
            "backgroundColor": "#ff334bcc",
            "offsetStart": "18px",
            "height": "25px",
            "width": "53px"
          }
        ],
        "paddingAll": "0px"
      }
    }]
}
            
        line_bot_api.reply_message(
            event.reply_token,
            FlexSendMessage(
                alt_text='hello',
                contents=contents
            ))

           
    if event.postback.data=="隨機推薦":
        index = random.randint(0, len(df)-1)
        url = df['image_0'].iloc[index]
        price = int(df['price'].iloc[index])
        name = df['name'].iloc[index]
        rating = df['rating'].iloc[index]
        address= df['address'].iloc[index]
            
        contents={
  "type": "bubble",
  "body": {
    "type": "box",
    "layout": "vertical",
    "contents": [
      {
        "type": "image",
        "url": f"{url}",
        "size": "full",
        "aspectMode": "cover",
        "aspectRatio": "1:1",
        "gravity": "center",
        "action": {
          "type": "uri",
          "label": "action",
          "uri": f"https://www.google.com/maps/search/?api=1&query={df['lat'].iloc[index]},{df['lng'].iloc[index]}"
        }
      },
      {
        "type": "box",
        "layout": "vertical",
        "contents": [],
        "position": "absolute",
        "background": {
          "type": "linearGradient",
          "angle": "0deg",
          "endColor": "#00000000",
          "startColor": "#00000099"
        },
        "width": "100%",
        "height": "40%",
        "offsetBottom": "0px",
        "offsetStart": "0px",
        "offsetEnd": "0px"
      },
      {
        "type": "box",
        "layout": "horizontal",
        "contents": [
          {
            "type": "box",
            "layout": "vertical",
            "contents": [
              {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                  {
                    "type": "text",
                    "text": f"{name}",
                    "size": "xl",
                    "color": "#ffffff"
                  }
                ]
              },
              {
                "type": "box",
                "layout": "baseline",
                "contents": [
                  {
                    "type": "text",
                    "text": f"地址：{address}",
                    "color": "#fffcfc"
                  }
                ],
                "spacing": "xs"
              },
              {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                  {
                    "type": "box",
                    "layout": "baseline",
                    "contents": [
                      {
                        "type": "text",
                        "text": f"NT${price}",
                        "color": "#ffffff",
                        "size": "md",
                        "flex": 0,
                        "align": "end"
                      }
                    ],
                    "flex": 0,
                    "spacing": "lg"
                  }
                ]
              }
            ],
            "spacing": "xs"
          }
        ],
        "position": "absolute",
        "offsetBottom": "0px",
        "offsetStart": "0px",
        "offsetEnd": "0px",
        "paddingAll": "20px"
      }
    ],
    "paddingAll": "0px"
  }
}
                
        line_bot_api.reply_message(
                    event.reply_token,
                    FlexSendMessage(
                    alt_text='Look what I get for you!',
                    contents=contents)
                    )


if __name__ == "__main__":
    app.config["JSON_AS_ASCII"] = False
    app.run()
