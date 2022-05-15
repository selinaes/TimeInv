# =================================================================================
#  Helper functions for app.py
#  Authors: Francisca Moya Jimenez, Jiawei Liu, Candice Ye, and Diana Hernandez
# =================================================================================

from flask import session, flash, redirect, url_for

def check_permissions(permission):
    """
   Checks whether a user has the appropriate permission levels to access
   a page. It redirects the user if they don't have the necessary permissions.

    Parameters:
        permission (string): a string indicating the permission level required

    Returns:
        None
    """
    permissions = session.get('permissions', '')

    # Check if user is logged in or if user is trying to access a forbidden route
    if session.get('logged_in') == None or 'product' not in permissions:
        if 'product' not in permissions:
            flash("You attempted to access a forbidden page. Please log in again.", "error")
        return redirect(url_for('logout'))
    
