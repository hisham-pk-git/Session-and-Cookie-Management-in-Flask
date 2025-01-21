from flask import Flask, request, redirect, render_template, session, make_response, url_for

app = Flask(__name__)
app.secret_key = 'supersecretkey'  

# Route: Home
@app.route('/')
def home():
    username = request.cookies.get('username')
    if username:
        return f"Welcome back, {username}! <br> Go to your <a href='/profile'>profile</a>"
    else:
        return redirect(url_for('login'))

# Route: Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        if username:
            # Check if the cookie already exists
            if request.cookies.get('username'):
                return redirect(url_for('profile'))

            # Set username cookie and initialize session for visit count
            resp = make_response(redirect(url_for('profile')))
            resp.set_cookie('username', username, max_age=30 * 60)  # Expires after 30 minutes
            session['visit_count'] = 0  # Initialize visit count
            return resp
    # If the cookie exists, redirect to profile
    if request.cookies.get('username'):
        return redirect(url_for('profile'))
    return render_template('login.html')

# Route: Profile
@app.route('/profile')
def profile():
    username = request.cookies.get('username')
    if username:
        # Increment visit count using session
        session['visit_count'] = session.get('visit_count', 0) + 1
        return render_template('profile.html', username=username, visits=session['visit_count'])
    else:
        return redirect(url_for('login'))

# Route: Logout
@app.route('/logout')
def logout():
    resp = make_response(redirect(url_for('login')))
    resp.delete_cookie('username')
    session.clear()
    return resp

if __name__ == '__main__':
    app.run(debug=True)
