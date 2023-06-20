import re
import pandas as pd
def preprocess(data):
    # take text data and convert it into data frame
    pattern='\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s-\s'
    messages = re.split(pattern, data)[1:]
    datetime = re.findall(pattern, data)
    df = pd.DataFrame({'usermessage': messages, 'date': datetime})
    df['date'] = pd.to_datetime(df['date'], format='%d/%m/%Y, %H:%M - ')
    # separate user and messages
    user = []
    message = []
    for i in df['usermessage']:
        entry = re.split('([\w\W]+?):\s', i)
        if entry[1:]:
            user.append(entry[1])
            message.append(entry[2])
        else:
            user.append('group notification')
            message.append(entry[0])
    df['user'] = user
    df['message'] = message
    df.drop(columns=['usermessage'], inplace=True)
    df['only_date']=df['date'].dt.date
    df['year'] = df['date'].dt.year
    df['day_name']=df['date'].dt.day_name()
    df['day'] = df['date'].dt.day
    df['month_num'] = df['date'].dt.month
    df['month'] = df['date'].dt.month_name()
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute
    period = []
    for hour in df[['day_name', 'hour']]['hour']:
        if hour == 23:
            period.append(str(hour) + "-" + str('00'))
        elif hour == 0:
            period.append(str('00') + "-" + str(hour + 1))
        else:
            period.append(str(hour) + "-" + str(hour + 1))
    df['period'] = period
    return df
