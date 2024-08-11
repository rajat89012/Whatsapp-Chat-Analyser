import streamlit as st
import preprocessor,helper
import matplotlib.pyplot as plt
import seaborn as sns

st.sidebar.title("Whatsapp Chat Analyzer")

uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
    # st.text(data)
    df = preprocessor.preprocess(data)
    # st.dataframe(df)

    # fetch unique user
    user_list=df['user'].unique().tolist()

    # remove the group_notification as user
    user_list.remove('group_notification')
    user_list.sort()
    user_list.insert(0,'Overall')

    selected_user=st.sidebar.selectbox("Show Analysis wrt",user_list)

    if st.sidebar.button('Show Analysis'):

        num_messages,words,media_msg,links=helper.fetch_stats(selected_user,df)
        
        st.title("Power of Analysis")
        col1,col2,col3,col4=st.columns(4)

        with col1:
            st.header("Total Messages")
            st.title(num_messages)
        with col2:
            st.header("Total words")
            st.title(words)
        with col3:
            st.header("Total Media message")
            st.title(media_msg)
        with col4:
            st.header("Total link shared")
            st.title(links)
        
        # monthly timeline
        st.title("Monthly Timeline ")
        timeline=helper.monthly_timeline(selected_user,df)
        fig,ax=plt.subplots()
        plt.plot(timeline['time'],timeline['message'],color="green")
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        # daily timeline
        st.title("Daily timeline")
        daily_timeline=helper.daily_timeline(selected_user,df)
        fig,ax=plt.subplots()
        ax.plot(daily_timeline['onlydate'],daily_timeline['message'],color="brown")
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        # activity map
        st.title("Activity Map")
        col1,col2=st.columns(2)
        with col1:
            st.header("Most busy day")
            busy_day=helper.week_activity_map(selected_user,df)
            fig,ax=plt.subplots()
            ax.bar(busy_day.index,busy_day.values,color="orange")
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        with col2:
            st.header("Most busy month")
            busy_month=helper.month_activity_map(selected_user,df)
            fig,ax=plt.subplots()
            ax.bar(busy_month.index,busy_month.values,color="brown")
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        st.title("Weekly Activity Map")
        user_heatmap=helper.activity_heatmap(selected_user,df)
        fig,ax=plt.subplots()
        ax=sns.heatmap(user_heatmap)
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        # finding the busiest user in the group(Group level)
        if selected_user == 'Overall':
            st.title('Most busy user')
            x,new_df=helper.fetch_most_busyuser(df)
            fig,ax=plt.subplots()
            
            col1,col2=st.columns(2)

            with col1:
                ax.bar(x.index,x.values,color='gray')
                plt.xticks(rotation='vertical')
                st.pyplot(fig)
            with col2:   
                st.dataframe(new_df)

        # WordCloud
        st.title("WordCloud")
        df_wc=helper.create_wordcloud(selected_user,df)   
        fig,ax=plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)


        # most common word

        st.title("Most Common Words")
        most_common_df=helper.most_common_words(selected_user,df)
            
            # show table
        # st.dataframe(most_common_df)

        # bar graph
        fig,ax=plt.subplots()
        ax.barh(most_common_df[0],most_common_df[1],color='gray')   # barh --> horizontal bar graph
        plt.xticks(rotation='vertical')
        st.pyplot(fig)


        # # emoji analysis
        # emoji_df=helper.emoji_helper(selected_user,df)
        # st.dataframe(emoji_df)




