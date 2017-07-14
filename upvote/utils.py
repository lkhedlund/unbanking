from django.contrib import messages

def has_voted(request):
    voted = request.session.get('has_voted', False)
    voted_message = "Thank you for your vote. Be sure to share your word get get the most votes to win!"
    if voted:
        messages.add_message(request, messages.ERROR, voted_message)
        return True
    else:
        return False
