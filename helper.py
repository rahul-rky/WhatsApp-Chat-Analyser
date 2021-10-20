from urlextract import URLExtract
extractor=URLExtract()
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import pandas as pd
from collections import Counter
import emoji
import seaborn as sns


def fetch_stats(selected_user,df):
    if(selected_user!='overall'):
        df=df[df['user']==selected_user]


    # 1. Fetch number of messages
    num_messages= df.shape[0]
    # 2 Fetch words
    words = []
    for message in df['message']:
        words.extend(message.split(' '))
    num_words=len(words)

    # 3 Counting media
    num_media = df[df['message']=='<Media omitted>\n'].shape[0]

    # 4 Counting links
    links = []
    for message in df['message']:
        links.extend(extractor.find_urls(message))
    num_links=(len(links))

    return num_messages,num_words,num_media,num_links

def most_busy_user(df):
    x = df['user'].value_counts().head()
    df = round(df['user'].value_counts() / df.shape[0] * 100, 2).reset_index().rename(
        columns={'index': 'name', 'user': 'percent'})
    return x,df

def create_word_clud(selected_user,df):
    if (selected_user != 'overall'):
        df = df[df['user'] == selected_user]
    wc=WordCloud(width=500,height=500,background_color='black')
    df_wc=wc.generate(df['message'].str.cat(sep=" "))
    return df_wc

def most_common_words(selected_user,df):
    if (selected_user != 'overall'):
        df = df[df['user'] == selected_user]

    temp = df[df['user'] != 'group_notification']
    temp = temp[temp['message'] != '<Media omitted>\n']

    f = open('stop_words.txt', 'r')
    stop_words = f.read()
    words = []
    for message in temp['message']:
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)
    returnd_df = pd.DataFrame(Counter(words).most_common(20))
    return returnd_df

def emoji_helper(selected_user,df):
    if (selected_user != 'overall'):
        df = df[df['user'] == selected_user]
    emojis = []

    for message in df['message']:
        emojis.extend([c for c in message if c in emoji.UNICODE_EMOJI['en']])
    emoji_df=pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))
    return emoji_df

def monthly_timeline(selected_user,df):
    if (selected_user != 'overall'):
        df = df[df['user'] == selected_user]
    timeline = df.groupby(['year', 'month_num', 'month']).count()['message'].reset_index()
    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i] + "-" + str(timeline['year'][i]))
    timeline['time'] = time
    return timeline

def daily_timeline(selected_user,df):
    if (selected_user != 'overall'):
        df = df[df['user'] == selected_user]
    dailytimeline = df.groupby(['day_name']).count()['message'].reset_index()
    return dailytimeline

def activity_heatmap(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    user_heatmap = df.pivot_table(index='day_name', columns='period', values='message', aggfunc='count').fillna(0)

    return user_heatmap
