from django.shortcuts import redirect

def login_required(view_func):
    """
    Decorator to ensure the user is logged in before accessing a view.
    """
    def wrapper(request, *args, **kwargs):
        if not request.session.get("email") or not request.session.get("password"):
            return redirect("login")  # Redirect to login page
        return view_func(request, *args, **kwargs)
    return wrapper
