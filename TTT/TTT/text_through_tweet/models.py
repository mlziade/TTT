from django.db import models


class Tweet(models.Model):
    """
        A model to store tweets and thei metadata.
        Target word is the word that was used to search for the tweet. There is only one entry for each target word.
        Last checked is used to make sure that the tweet is still valid/visible.
    """
    target_word = models.CharField(max_length=255, primary_key=True)
    target_word_position = models.IntegerField()
    last_checked_at = models.DateTimeField()
    # Tweet Metadata
    tweet_id = models.CharField(max_length=20, primary_key=True)
    username = models.CharField(max_length=255)
    author_id = models.BigIntegerField()
    tweet_text = models.TextField()
    created_at = models.DateTimeField()


class TextThroughTweet(models.Model):
    """
        A model to store the texts that were generated through the tweets.
    """
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
class TextTweetOrder(models.Model):
    """
        Intermediate model to store the order of tweets in a TextThroughTweet.
    """
    ttt = models.ForeignKey(TextThroughTweet, on_delete=models.CASCADE)
    tweet = models.ForeignKey(Tweet, on_delete=models.CASCADE)
    order = models.PositiveIntegerField()
    
    class Meta:
        ordering = ['order']
        unique_together = ['text', 'order']