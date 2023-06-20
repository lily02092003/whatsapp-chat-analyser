import re
from urlextract import URLExtract
from wordcloud import WordCloud
from collections import Counter
import pandas as pd
import emoji
f=open('stopwords.txt','r')
stop_words=f.read()
def fetch(selected_user,df):
    emoji_pattern = re.compile("["
                               u"\U0001F600-\U0001F64F"  # emoticons
                               u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                               u"\U0001F680-\U0001F6FF"  # transport & map symbols
                               u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                               "]+", flags=re.UNICODE)

    if selected_user!='Overall':
        df = df[df['user'] == selected_user]
    #total number of messages
    total_messages= len(df['message'])
    #Number of times emoji is used
    joined_text = ' '.join(df['message'])
    emojis = emoji_pattern.findall(joined_text)
    emoji_len=len(emojis)
    #number of words
    #number of links
    extractor=URLExtract()
    words=[]
    links=[]
    for message in df['message']:
        words.extend(message.split())
        links.extend(extractor.find_urls(message))
    #media file shared
    media=df[df['message']=='<Media omitted>\n'].shape[0]
    return total_messages, emoji_len,len(words),media,len(links)
def most_busyuser(df):
    x=df['user'].value_counts().head()
    df=round((df['user'].value_counts()/df.shape[0])*100,2).reset_index().rename(columns={'index':'name','user':'percentage'})
    return x,df
def createwordcloud(selected_user,df):
    if selected_user!='Overall':
        df = df[df['user'] == selected_user]
    temp = df[df['user'] != 'group notification']
    temp = temp[temp['message'] != '<Media omitted>\n']
    temp=temp[temp['message']!= 'This message was deleted\n']
    def remove_stop_words(message):
        y = []
        for word in message.lower().split():
            if word not in stop_words:
                y.append(word)
        return " ".join(y)

    wc = WordCloud(width=500, height=500, min_font_size=10, background_color='white')
    temp['message'] = temp['message'].apply(remove_stop_words)
    wc_df=wc.generate(temp['message'].str.cat(sep=" "))
    return wc_df
def mostcommonwords(selected_user,df):
    if selected_user!='Overall':
        df = df[df['user'] == selected_user]
    temp = df[df['user'] != 'group notification']
    temp = temp[temp['message'] != '<Media omitted>\n']
    temp=temp[temp['message']!= 'This message was deleted\n']
    def remove_emojis(text):
        emoji_pattern = re.compile("["
                                   u"\U0001F600-\U0001F64F"  # emoticons
                                   u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                                   u"\U0001F680-\U0001F6FF"  # transport & map symbols
                                   u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                                   u"\U00002500-\U00002BEF"  # Chinese characters
                                   u"\U00002702-\U000027B0"
                                   u"\U00002702-\U000027B0"
                                   u"\U000024C2-\U0001F251"
                                   u"\U0001f926-\U0001f937"
                                   u"\U00010000-\U0010ffff"
                                   u"\u2640-\u2642"
                                   u"\u2600-\u2B55"
                                   u"\u200d"
                                   u"\u23cf"
                                   u"\u23e9"
                                   u"\u231a"
                                   u"\ufe0f"  # dingbats
                                   u"\u3030"
                                   "]+", flags=re.UNICODE)
        return emoji_pattern.sub(r'', text)
    temp['message'] = temp['message'].apply(remove_emojis)
    words = []
    for message in temp['message']:
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)
    most_common_df = pd.DataFrame(Counter(words).most_common(20))
    return most_common_df

def monthly_timeline(selected_user, df):
        if selected_user != 'Overall':
            df = df[df['user'] == selected_user]
        timeline = df.groupby(['year', 'month_num', 'month']).count()['message'].reset_index()
        time = []
        for i in range(timeline.shape[0]):
            time.append(timeline['month'][i] + "-" + str(timeline['year'][i]))
        timeline['time'] = time
        return timeline

def daily_timeline(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    timeline = df.groupby(['only_date']).count()['message'].reset_index()
    return timeline
def week_activity(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    week_act=df['day_name'].value_counts()
    return week_act

def month_activity(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    month_act=df['month'].value_counts()
    return month_act
def activity_heatmap(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    user_heatmap = df.pivot_table(index='day_name', columns='period', values='message', aggfunc='count').fillna(0)
    return user_heatmap
