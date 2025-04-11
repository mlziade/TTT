from django.contrib import admin
from .models import Tweet, TextThroughTweet

@admin.register(Tweet)
class TweetAdmin(admin.ModelAdmin):
    list_display = ('tweet_id', 'target_word', 'username', 'target_word_position', 'created_at', 'last_checked_at')
    list_display_links = ('tweet_id', 'target_word')
    search_fields = ('target_word', 'username', 'tweet_text')
    list_filter = ('created_at', 'last_checked_at')

@admin.register(TextThroughTweet)
class TextThroughTweetAdmin(admin.ModelAdmin):
    list_display = ('id', 'text_preview', 'created_at')
    list_display_links = ('id', 'text_preview')
    search_fields = ('text', 'ciphered_text')
    list_filter = ('created_at',)
    
    def text_preview(self, obj):
        """Returns a truncated version of the text for display in admin"""
        max_length = 50
        if len(obj.text) > max_length:
            return obj.text[:max_length] + '...'
        return obj.text
    
    text_preview.short_description = 'Text'