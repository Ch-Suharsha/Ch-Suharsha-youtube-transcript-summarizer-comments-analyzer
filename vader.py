# -*- coding: utf-8 -*-
"""VADER.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1xKK-Ym6VP4urfhDX3SYRF7GRq4o0smmy
"""

from googleapiclient.discovery import build



import re

!pip install emoji

import emoji

!pip install vaderSentiment

from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

import matplotlib.pyplot as plt



API_KEY = 'AIzaSyDXOo5wlFHzrwKx0RbBT4Komw-0F023VXE'
youtube = build('youtube', 'v3', developerKey=API_KEY)

video_id='https://www.youtube.com/watch?v=SqcY0GlETPk'[-11:]
print("video id: " + video_id)
video_response = youtube.videos().list(
    part='snippet',
    id=video_id
).execute()
video_snippet = video_response['items'][0]['snippet']
uploader_channel_id = video_snippet['channelId']
print("channel id: " + uploader_channel_id)
print("Fetching Comments...")
comments = []
nextPageToken = None
while len(comments) < 600:
	request = youtube.commentThreads().list(
		part='snippet',
		videoId=video_id,
		maxResults=100, # You can fetch up to 100 comments per request
		pageToken=nextPageToken
	)
	response = request.execute()
	for item in response['items']:
		comment = item['snippet']['topLevelComment']['snippet']
		# Check if the comment is not from the video uploader
		if comment['authorChannelId']['value'] != uploader_channel_id:
			comments.append(comment['textDisplay'])
	nextPageToken = response.get('nextPageToken')

	if not nextPageToken:
		break
print(comments[:5])
hyperlink_pattern = re.compile(
	r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')

threshold_ratio = 0.65

relevant_comments = []

# Inside your loop that processes comments
for comment_text in comments:

	comment_text = comment_text.lower().strip()

	emojis = emoji.emoji_count(comment_text)

	# Count text characters (excluding spaces)
	text_characters = len(re.sub(r'\s', '', comment_text))

	if (any(char.isalnum() for char in comment_text)) and not hyperlink_pattern.search(comment_text):
		if emojis == 0 or (text_characters / (text_characters + emojis)) > threshold_ratio:
			relevant_comments.append(comment_text)

# Print the relevant comments
print(relevant_comments[:5])
f = open("ytcomments.txt", 'w', encoding='utf-8')
for idx, comment in enumerate(relevant_comments):
	f.write(str(comment)+"\n")
f.close()
print("Comments stored successfully!")
def sentiment_scores(comment, polarity):

	# Creating a SentimentIntensityAnalyzer object.
	sentiment_object = SentimentIntensityAnalyzer()

	sentiment_dict = sentiment_object.polarity_scores(comment)
	polarity.append(sentiment_dict['compound'])

	return polarity
polarity = []
positive_comments = []
negative_comments = []
neutral_comments = []

f = open("ytcomments.txt", 'r', encoding='`utf-8')
comments = f.readlines()
f.close()
print("Analysing Comments...")
for index, items in enumerate(comments):
	polarity = sentiment_scores(items, polarity)

	if polarity[-1] > 0.05:
		positive_comments.append(items)
	elif polarity[-1] < -0.05:
		negative_comments.append(items)
	else:
		neutral_comments.append(items)

# Print polarity
polarity[:5]

avg_polarity = sum(polarity)/len(polarity)
print("Average Polarity:", avg_polarity)
if avg_polarity > 0.05:
	print("The Video has got a Positive response")
elif avg_polarity < -0.05:
	print("The Video has got a Negative response")
else:
	print("The Video has got a Neutral response")

print("The comment with most positive sentiment:", comments[polarity.index(max(
	polarity))], "with score", max(polarity), "and length", len(comments[polarity.index(max(polarity))]))
print("The comment with most negative sentiment:", comments[polarity.index(min(
	polarity))], "with score", min(polarity), "and length", len(comments[polarity.index(min(polarity))]))
positive_count = len(positive_comments)
negative_count = len(negative_comments)
neutral_count = len(neutral_comments)
labels = ['Positive', 'Negative', 'Neutral']
comment_counts = [positive_count, negative_count, neutral_count]

# Creating bar chart
plt.bar(labels, comment_counts, color=['blue', 'red', 'grey'])

# Adding labels and title to the plot
plt.xlabel('Sentiment')
plt.ylabel('Comment Count')
plt.title('Sentiment Analysis of Comments')

# Displaying the chart
plt.show()

print(video_response)