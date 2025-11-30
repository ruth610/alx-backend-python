from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.shortcuts import redirect

@login_required
def delete_user(request):
    """
    Allows a user to delete their account.
    """
    user = request.user
    logout(request)        # Log out first
    user.delete()          # Trigger deletion (signals included)
    return redirect('/')   # Redirect to home page

