from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def dashboard(request):
    print("User logged in:", request.user)
    return render(request, 'accounts/dashboard.html', {'user': request.user})
