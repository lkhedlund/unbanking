from django.contrib import messages

def has_voted(request):
    voted = request.session.get('has_voted', False)
    voted_message = "Thank you for your vote. Be sure to share your word get get the most votes to win!"
    if voted:
        messages.add_message(request, messages.WARNING, voted_message)
        return True
    else:
        return False

def format_word(word):
    lower_word = word.lower()
    if lower_word[-3:] == 'ing':
        return lower_word[:-3]
    else:
        return lower_word