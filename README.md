# youtube-transcript-summarizer-comments-analyzer
A web application that summarizes YouTube video transcripts and analyzes comments using sentiment analysis and NLP. Includes MySQL for data management and frameworks for data processing
# YouTube Transcript Summarizer and Comments Analyzer

This project is a web application that allows users to summarize YouTube video transcripts and analyze comments for sentiment. It uses Natural Language Processing (NLP) and Sentiment Analysis to extract insights from video content and user comments.

## Features:
- Summarize video transcripts.
- Analyze comments to determine sentiment (positive, negative, neutral).
- MySQL is used for storing and retrieving video data and comments.
- User-friendly interface for easy interaction.

## Technologies Used:
- **Frontend**: HTML, CSS
- **Backend**: Python, Flask (for web framework)
- **Database**: MySQL
- **Libraries**: NLTK (Natural Language Toolkit), TextBlob for sentiment analysis
- **APIs**: YouTube Data API for fetching transcripts and comments.

## Setup Instructions:
1. Clone this repository.
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
Set up the MySQL database and import the SQL schema.
## Sentiment Analysis:
# For Fetching Comments 
from googleapiclient.discovery import build 
# For filtering comments 
import re 
# For filtering comments with just emojis 
import emoji
# Analyze the sentiments of the comment
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
# For visualization 
import matplotlib.pyplot as plt
API_KEY = 'AIzaSyCNO6aypXXXXXXXXXXXXXXXXXXXXXXXXXX'# Put in your API Key

youtube = build('youtube', 'v3', developerKey=API_KEY) # initializing Youtube API

# Taking input from the user and slicing for video id
video_id = input('Enter Youtube Video URL: ')[-11:]
print("video id: " + video_id)

# Getting the channelId of the video uploader
video_response = youtube.videos().list(
	part='snippet',
	id=video_id
).execute()

# Splitting the response for channelID
video_snippet = video_response['items'][0]['snippet']
uploader_channel_id = video_snippet['channelId']
print("channel id: " + uploader_channel_id)
# Fetch comments
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
# Print the 5 comments
comments[:5]
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
relevant_comments[:5]
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

# labels and data for Bar chart
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
## Transcript Summariser :




