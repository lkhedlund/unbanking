from django.contrib import messages

def has_participated(request):
    submitted = request.session.get('has_submitted', False)
    voted = request.session.get('has_voted', False)
    participation_message = "Thank you for participating. Be sure to share your word get get the most votes to win!"
    if voted and submitted:
        messages.add_message(request, messages.ERROR, participation_message)
        return True
    elif submitted:
        messages.add_message(request, messages.ERROR, participation_message)
        return True
    elif voted:
        messages.add_message(request, messages.ERROR, participation_message)
        return True
    else:
        return False
