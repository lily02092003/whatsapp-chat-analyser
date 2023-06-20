import streamlit as st
import preprocess
import help
import matplotlib.pyplot as plt
import seaborn as sns
st.sidebar.title('WHATSAPP CHAT ANALYZER')
uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    # To read file as bytes:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
    df = preprocess.preprocess(data)
    user_list = df['user'].unique().tolist()
    for user in user_list:
        if user=='group notification':
            user_list.remove('group notification')
    user_list.sort()
    user_list.insert(0,"Overall")
    selected_user = st.sidebar.selectbox(
        'Select analysis with respect to user:',
        user_list)
    if st.sidebar.button("Analyze"):
        #stats of user
        total_messages,emojis_len,numwords,media,links=help.fetch(selected_user,df)
        st.title("TOP STATISTICS")
        col1,col2,col3,col4,col5=st.columns(5)
        with col1:
           st.header("Total Messages")
           st.title(total_messages)
        with col2:
           st.header("Number of times emojis used")
           st.title(emojis_len)
        with col3:
           st.header("Number of words")
           st.title(numwords)
        with col4:
           st.header("Media shared")
           st.title(media)
        with col5:
           st.header("Links shared")
           st.title(links)
        #monthly timeline
        st.title("Monthly Timeline")
        timeline=help.monthly_timeline(selected_user,df)
        fig,axis=plt.subplots()
        axis.plot(timeline['time'],timeline['message'],color='#A020F0')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)
        #daily timeline
        st.title("Daily Timeline")
        timeline = help.daily_timeline(selected_user, df)
        fig, axis = plt.subplots()
        axis.plot(timeline['only_date'], timeline['message'])
        plt.xticks(rotation='vertical')
        plt.figure(figsize=(20,10))
        st.pyplot(fig)
        #week_activity
        st.title("Activity map")
        col1,col2=st.columns(2)
        with col1:
            st.header("Busiest Days")
            week_act=help.week_activity(selected_user, df)
            fig, axis = plt.subplots()
            axis.bar(week_act.index,week_act.values,color='orange')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)
        with col2:
            st.header("Busiest Months")
            month_act=help.month_activity(selected_user, df)
            fig, axis = plt.subplots()
            axis.bar(month_act.index, month_act.values,color='yellow')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)
        st.title("Weekly Activity Map")
        user_heatmap = help.activity_heatmap(selected_user,df)
        fig,ax = plt.subplots()
        axis = sns.heatmap(user_heatmap)
        st.pyplot(fig)
        #finding busiest users in group
        if selected_user=='Overall':
            st.title("User Analytics ")
            x,dataframe1=help.most_busyuser(df)
            fig,axis=plt.subplots()
            col1,col2=st.columns(2)
            with col1:
                st.header("Most Active users:")
                axis.bar(x.index,x.values,color='green')
                plt.xticks(rotation='vertical')
                st.pyplot(fig)
            with col2:
                st.header("Message contibutions")
                st.dataframe(dataframe1)
        #Word Cloud
        st.title("Most Commonly Used Words Statistics")
        wc_df=help.createwordcloud(selected_user,df)
        st.header("Word Cloud")
        fig, axis = plt.subplots()
        axis.imshow(wc_df)
        st.pyplot(fig)
        #Most common words by user
        return_df=help.mostcommonwords(selected_user,df)
        st.header("Most Common Words")
        fig,axis=plt.subplots()
        axis.bar(return_df[0],return_df[1],color='red')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)



