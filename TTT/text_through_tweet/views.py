from django.shortcuts import render
from django.views import View

from .forms import TextForm
from .models import Tweet, TextThroughTweet
from .tweet_api import search_new_word

class HomeView(View):
    template_name = 'home.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)
    
class TextView(View):
    template_name = 'text.html'

    def get(self, request, *args, **kwargs):

        # Create form
        form = TextForm()

        return render(request, self.template_name, {'form': form})
    
    def post(self, request, *args, **kwargs):
        # Create form with POST data
        form = TextForm(request.POST)

        if form.is_valid():
            # Process the data in form.cleaned_data
            text = form.cleaned_data['text'].lower()
            
            # Generate cipher from text
            cipher = generate_cipher_from_text(text)

            # Save the text and cipher to the database
            text_through_tweet = TextThroughTweet(text=text, ciphered_text=cipher)
            text_through_tweet.save()

            return render(request, self.template_name, {'form': form, 'text': text, 'cipher_text': cipher})

        return render(request, self.template_name, {'form': form})
    
def generate_cipher_from_text(text: str) -> str:
    """
    This function takes a text and generates a cipher from it.
    It searches for each word in the database and returns a string with the tweet id and the position of the word in the tweet.
    """
    words: list[str] = text.lower().split()
    words_to_search = words.copy()

    # Create array of ciphered words
    ciphered_words = [
        ["", ""] for _ in range(len(words))
    ]

    # Remove duplicates from words_to_search
    words_to_search = list(dict.fromkeys(words_to_search))

    # Search for words in the database
    cached_tweets = Tweet.objects.filter(
        target_word__in=words
    ).order_by('target_word_position')

    #TODO: Validate cached_tweets

    # Remove words that are already in the database from words_to_search
    # Add them to the ciphered_words array
    for word in words_to_search.copy():
        cached_values = cached_tweets.values_list('target_word', flat=True)
        if word in cached_values:
            cached_tweet = cached_tweets.get(target_word=word)
            # Add the tweet id and the position of the word in the tweet to the ciphered_words array
            ciphered_words[words.index(word)][0] = cached_tweet.tweet_id
            ciphered_words[words.index(word)][1] = cached_tweet.target_word_position
            # Remove the word from words_to_search
            words_to_search.remove(word)

    # Seach for words in tweets
    for word in words_to_search:
        # Search for the word in the Twitter API and saves it to the database
        tweet: Tweet = search_new_word(word)

        # Add the tweet id and the position of the word in the tweet to the ciphered_words array
        ciphered_words[words.index(word)][0] = tweet.tweet_id
        ciphered_words[words.index(word)][1] = tweet.target_word_position

    cipher: str = ""
    for word in ciphered_words:
        cipher += f"{word[0]} {word[1]}\n"
    
    return cipher