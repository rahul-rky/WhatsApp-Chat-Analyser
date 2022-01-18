import matplotlib.pyplot as plt
import streamlit as st
import preprocessor,helper
import seaborn as sns

st.sidebar.title("Whatsapp Chat Analyser")
st.title("Upload chat txt file in 24:00 hour Format")

uploaded_file=st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    bytes_data=uploaded_file.getvalue()
    data=bytes_data.decode("utf-8")
    df=preprocessor.preprocess(data)

    #st.dataframe(df)

    #fetch unique users
    user_list=df['user'].unique().tolist()
    #user_list.remove('group_notifications')
    user_list.sort()
    user_list.insert(0,'overall')

    selected_user=st.sidebar.selectbox("Show analysis wrt",user_list)
    if st.sidebar.button("Show Analysis"):
        st.title("Top Statics")
        num_messages,num_words,num_media ,num_links = helper.fetch_stats(selected_user,df)
        col1,col2,col3,col4=st.columns(4)
        with col1:
            st.header("Total Messages")
            st.title(num_messages)
        with col2:
            st.header("Total Words")
            st.title(num_words)
        with col3:
            st.header("Total Media")
            st.title(num_media)
        with col4:
            st.header("Links Shared1")
            st.title(num_links)

        col1,col2=st.columns(2)
        #Monthly analysis
        with col1:
            st.title("Monthly Timeline")
            timeline=helper.monthly_timeline(selected_user,df)
            fig,ax=plt.subplots()
            ax.bar(timeline['time'], timeline['message'],color='darkgreen')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)
        #Daily analysis
        with col2:
            st.title("Daily Timeline")
            dailytimeline=helper.daily_timeline(selected_user,df)
            fig,ax=plt.subplots()
            ax.bar(dailytimeline['day_name'],dailytimeline['message'],color='teal')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        #heatmap
        # st.title("Weekly Heatmap")
        # user_heatmap=helper.activity_heatmap(selected_user,df)
        # fig,ax=plt.subplots()
        # ax=sns.heatmap(user_heatmap)
        # st.pyplot(fig)

        #Most busy user
        if selected_user=='overall':
            st.title('Most Busy User')
            x,new_df=helper.most_busy_user(df)
            fig,ax=plt.subplots()
            col1,col2=st.columns(2)
            with col1:
                ax.bar(x.index,x.values,color='olive')
                plt.xticks(rotation='vertical')
                st.pyplot(fig)
            with col2:
                st.dataframe(new_df)
        #Word cloud
        st.title('Word Cloud')
        df_wc=helper.create_word_clud(selected_user,df)
        fig,ax=plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)

        ##most Common words
        st.title("Most Common Words")
        most_common_df=helper.most_common_words(selected_user,df)
        fig,ax=plt.subplots()
        ax.barh(most_common_df[0],most_common_df[1],color='peru')
        st.pyplot(fig)
        #st.dataframe(most_common_df)

        #Emoji analysis
        emoji_df=helper.emoji_helper(selected_user,df)
        st.title("Emoji Analysis")
        col1,col2=st.columns(2)
        with col1:
            st.dataframe(emoji_df)
        with col2:
            fig,ax=plt.subplots();
            ax.pie(emoji_df[1],labels=emoji_df[0],autopct="%0.2f")
            st.pyplot(fig)

        # bad word used in chat
        st.title("Bad word used by users")
        data_of_bad_words = helper.bad_word_used_by_user(selected_user, df)
        col1, col2 = st.columns(2)
        with col1:
            st.dataframe(data_of_bad_words)
        fig, ax = plt.subplots()

        ax.barh(data_of_bad_words[0], data_of_bad_words[1])
        plt.xticks(rotation='vertical')

        with col2:
            st.pyplot(fig)