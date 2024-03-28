import streamlit as st
from pygments.lexer import words

import matplotlib.pyplot as plt

import preprocessor, helper

import seaborn as sns


st.sidebar.title("Whatsapp Chat Analyzer")
st.sidebar.title("By Aakif Mohamed")


uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()

#    the above three lines is for sidebar choosing the whatsapp text file

    data = bytes_data.decode("utf-8")
    df = preprocessor.preprocess(data)
    # down will how the grps chats full,if dont want to show then just comment it
    # st.dataframe(df)

    # fetch unique users
    user_list = df['user'].unique().tolist()
    user_list.remove('group_notification')
    user_list.sort()
    user_list.insert(0,"Overall")

    selected_user = st.sidebar.selectbox("Show analysis wrt", user_list)

    if st.sidebar.button("Show Analysis"):
        num_messages,words,num_media_messages,num_links = helper.fetch_stats(selected_user,df)
        st.title("Top Statistics")
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.header("Total Messages:")
            st.title(num_messages)
        with col2:
            st.header("Total Words:")
            st.title(words)
        with col3:
            st.header("Media Shared:")
            st.title(num_media_messages)
        with col4:
            st.header("Links Shared:")
            st.title(num_links)


# timline in months
        st.title("Monthly Timeline:")

        timeline = helper.monthly_timeline(selected_user,df)
        fig,ax = plt.subplots()
        ax.plot(timeline['time'], timeline['message'],color='green')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

#         timeline in days
        st.title("Daily Timeline")
        daily_timeline = helper.daily_timeline(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(daily_timeline['only_date'], daily_timeline['message'], color='black')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

#       most active day and opposite
        st.title("Most Active/Inactive Day:")
        col1, col2 = st.columns(2)

        with col1:
            st.header("Most busy day:")
            busy_day = helper.week_activity_map(selected_user,df)
            fig, ax = plt.subplots()
            ax.bar(busy_day.index, busy_day.values)
            plt.xticks(rotation='vertical')

            st.pyplot(fig)

        with col2:
            st.header("Most busy Month:")
            busy_month = helper.month_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_month.index, busy_month.values, color='orange')
            plt.xticks(rotation='vertical')

            st.pyplot(fig)
        #     weekly map using seaborn library
        st.title("Weekly Activity Map:")
        user_heatmap = helper.activity_heatmap(selected_user, df)
        fig, ax =plt.subplots()
        ax = sns.heatmap(user_heatmap)
        st.pyplot(fig)

        #finding the most active users

        if selected_user =='Overall':
            st.title('Most Active Users:')
            x,new_df = helper.most_busy_users(df)
            fig, ax = plt.subplots()


            col1, col2 = st.columns(2)

            with col1:
                ax.barh(x.index, x.values,color='green')
                plt.xticks(rotation='vertical',color='red')
                st.pyplot(fig)
            with col2:
                st.dataframe(new_df)

        st.title("WordCloud")
        df_wc = helper.create_wordcloud(selected_user,df)
        fig,ax = plt.subplots()
        plt.imshow(df_wc)
        st.pyplot(fig)

        #most common words 25

        st.title("Top 20 Words Used:")

        most_common_df = helper.most_common_words(selected_user,df)

        fig, ax = plt.subplots()
        # ax.bar(most_common_df)
        ax.barh(most_common_df[0], most_common_df[1])
        plt.xticks(rotation='vertical')

        # st.dataframe(most_common_df[0],most_common_df[1])
        st.pyplot(fig)

        # st.dataframe(most_common_df)

#         emoji analysis broooo
        st.title("Emoji Analysis:")

        emoji_df = helper.emoji_helper(selected_user,df)

        col1,col2 = st.columns(2)

        with col1:
            st.dataframe(emoji_df)

        with col2:
            fig,ax = plt.subplots()
            # SOME DIFFICULTY IN GETTING EMOJIS SHOULD DO RESEARCH ON IT:
            # ax.pie(emoji_df[1],labels=emoji_df[0])

            ax.pie(emoji_df[1].head(),labels=emoji_df[0].head(),autopct="%0.2f")

            st.pyplot(fig)
