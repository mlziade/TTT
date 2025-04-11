from django.db import models


class Tweet(models.Model):
    """
        A model to store tweets and thei metadata.
        Target word is the word that was used to search for the tweet. There is only one entry for each target word.
        Last checked is used to make sure that the tweet is still valid/visible.
    """
    target_word = models.CharField(max_length=255, unique=True)
    target_word_position = models.IntegerField()
    last_checked_at = models.DateTimeField()
    # Tweet Metadata
    tweet_id = models.CharField(max_length=20, primary_key=True)
    username = models.CharField(max_length=255)
    author_id = models.BigIntegerField()
    tweet_text = models.TextField(default="")
    created_at = models.DateTimeField()


class TextThroughTweet(models.Model):
    """
        A model to store the texts that were generated through the tweets.
    """
    id = models.AutoField(primary_key=True, auto_created=True)
    text = models.TextField()
    ciphered_text = models.TextField(default="")
    created_at = models.DateTimeField(auto_now_add=True)