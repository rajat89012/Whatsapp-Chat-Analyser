import re
import pandas as pd

def preprocess(data):
    # regular expression
    pattern = r'\d{1,2}/\d{1,2}/\d{4},\s\d{1,2}:\d{2}\s-\s'
    
    message=re.split(pattern,data)[1:]
    dates=re.findall('\d{1,2}/\d{1,2}/\d{4},\s\d{1,2}:\d{2}',data)
    
    # Create DataFrame
    df = pd.DataFrame({'user_message': message, 'message_date': dates})

    # Convert message_date type
    df['message_date'] = pd.to_datetime(df['message_date'], format="%d/%m/%Y, %H:%M")

    # Rename column
    df.rename(columns={'message_date': 'date'}, inplace=True)
    
    users=[]
    msg=[]
    pattern = r':\s*'
    for message in df['user_message']:
    #     print(message)
        entry=re.split(pattern,message)
        if entry[1:]:
            users.append(entry[0])
            msg.append(entry[1])
        else:
            users.append('group_notification')
            msg.append(entry[0])
            
    df['user']=users
    df['message']=msg
    df.drop(columns=['user_message'],inplace=True)

    df['year']=df['date'].dt.year
    df['month_num']=df['date'].dt.month
    df['onlydate']=df['date'].dt.date
    df['month']=df['date'].dt.month_name()
    df['day']=df['date'].dt.day
    df['day_name']=df['date'].dt.day_name()
    df['hour']=df['date'].dt.hour
    df['minute']=df['date'].dt.minute

    period=[]
    for hour in df[['day_name','hour']]['hour']:
        if hour ==23:
            period.append(str(hour) + "-" + str('00'))
        elif hour==0:
            period.append(str('00') + "-" + str(hour+1))
        else:
            period.append(str(hour) + "-" + str(hour+1))

    df['period']=period
    
    return df

    