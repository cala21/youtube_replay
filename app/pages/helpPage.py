from dash import dcc, html

layout = html.Div(children=[
    html.H1(children="How to use the YouTube Replay app"),
    html.Hr(),
    html.H4(children='Part 1 : How to Get a Copy of Your YouTube History'),
    
    html.P(children='Your YouTube history is available through Google Takeout, a tool that Google provides to consult practically the history and stored data of any of the products that you have used. Follow these steps to get a copy of your YouTube history:'),
    
    html.Ol(children=[
        html.Li(children=[
            'Go to ',
            html.A(children='https://takeout.google.com/settings/takeout', href='https://takeout.google.com/settings/takeout'),
            ' and log in with your personal account.'
        ]),
        html.Li(children=[
            'Click on "Deselect All" to unselect all products.',
            html.Img(src='assets/deselect_all.png', width=500)
        ]),
        html.Li(children=[
            dcc.Markdown('Scroll all the way down to "YouTube and YouTube Music".'),
            html.Img(src='assets/scroll_to_youtube.png', width=500)
        ]),
        html.Li(children=[
            dcc.Markdown('Select JSON format and make sure to just select "history" via the "All YouTube data included" link.'),
            html.Img(src='assets/select_history.png', width=500)
        ]),
        html.Li(children=[
            dcc.Markdown('Click on "Next" and follow the steps to request the download of your YouTube history.'),
            html.Img(src='assets/final_step.png', width=500)
        ]),
        html.Li(children=[
            dcc.Markdown('Once the file is generated, you will receive a notification email. Click on the link provided in the email to download your file.'),
            #html.Img(src='assets/notification_email.png', width=500)
        ]),
        html.Li(children='For security, the file has an expiration date, so make sure to download it before the date indicated in the email.')
    ]),
    
    html.P(children="That's it! Once you have downloaded your YouTube history file, you can upload it to YouTube Replay and start exploring your data."),
    html.Hr(),
    html.H4(children='Part 2 : How to use History Analysis'),
    html.P(children='Once you have your "watch_history.json" file, navigate to the  "History Analysis"  tab of the application'),
    html.P(children=[
        'Or ',
        html.A('Download example watch_history.json', href='/assets/watch_history.json', download='watch_history.json', target='_blank')
    ]),

    html.Ol(children=[
        html.Li(children=[
            'Drag and Drop (or) Select the "watch_history.json" file into the Uploader ',
            html.Img(src='assets/uploader.png', width=800)
        ]),
        html.Li(children=[
            dcc.Markdown('A loading spinner will indicate the file is being processed".'),
            html.Img(src='assets/spinner-load.png', width=50)
        ]),
        html.Li(children=[
            dcc.Markdown('You can use the Select the date range to filter the data. It will filter date for all the graphs'),
            html.Img(src='assets/date-time-filter.png', width=500)
         ]),
        ]),
    
    html.H5(children='Interactive Graphs:'),

    html.Ol(children=[
        html.Li(children=[
            dcc.Markdown('Scatter plot of the Popularity of your watched videos. You can hover around each point and see the Title, Views and the Date you watched the video'),
            html.Img(src='assets/scatter-plot.png', width=500)
        ]),
        html.Li(children=[
            dcc.Markdown('Bar graph of Ads vs Videos, shows how many Ads have you watched compared to the actual Video content you wanted to see. Note: YouTube "Shorts" do not have Ads, so if your watched videos are significantly higher you may be watching "Shorts"'),
            html.Img(src='assets/bar-graph-ads.png', width=500)
        ]),
        html.Li(children=[
            dcc.Markdown('This area chart shows the percentage of videos watched thought the day. It is helpful in giving you an insight into your viewing habits. Select the timezone filter accordingly.'),
            html.Img(src='assets/graph-time-trend.png', width=500)
        ]),
        html.Li(children=[
            dcc.Markdown('This graph is used to show how the genres of videos watch compare over time. You can group data by "Yearly", "Monthly" etc '),
            html.Img(src='assets/bar-chart-genre.png', width=500)
        ]),
        ]),
    
    html.H5(children='Non-Interactive Elements:'),
    html.P(children="We have added some elements which are non-interactive but show more insights of your youtube data"),

    html.Ol(children=[
        html.Li(children=[
        dcc.Markdown('Top Most Watched videos shows your 5 videos that you have watched the most number of times.'),
        html.Img(src='assets/most-watched.png', width=800)
        ]),
        html.Li(children=[
            dcc.Markdown('The word cloud, using NLP to populate 20% of most popular words from your watch video titles and displays them with larger words occurring more frequently'),
            html.Img(src='assets/word-cloud.png', width=500)
        ]),
        html.Li(children=[
            dcc.Markdown('History based recommendation gives the list of 5 videos you may like based on your viewing history!'),
            html.Img(src='assets/rec-video.png', width=800)
        ]),
        ]),
    html.Hr(),
    html.H4(children='Part 3 : How to get Personalized Recommendations'),
    html.P(children='Navigate to the  "Personalized Recommendations"  tab of the application to connect your YouTube account and get personalized recommendations based on your liked videos!'),
    html.P(children="We have OAuth 2.0 functionality to show how to connect to YouTube account to fetch data"),

    html.Ul(children=[
        html.Li(children=[
        dcc.Markdown('Click on Get Connected User Info, If you are connected it will show the User information or give you a link to "Connect to your YouTube account". Follow and approve the application (you may have to request to be added for OAuth)'),
        html.Img(src='assets/OAuth2.png', width=300)
        ]),
        html.Li(children=[
        dcc.Markdown('Once you have authorized your account, clicking on the "Get Connected User Info" will show the user information'),
        html.Img(src='assets/connected-user.png', width=400)
        ]),
        html.Li(children=[
            dcc.Markdown('The algorithm fetches your liked videos and based on that generates more videos related to them and shows the top 10 recommendations'),
            html.Img(src='assets/yt-rec-videos.png', width=800)
        ]),
    ]),

], style={'max-width': '800px', 'margin': '0 auto'})
