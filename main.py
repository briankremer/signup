import webapp2
import re
import cgi

signup_form = """
<html>
	<head>
		<style>
			div {
                background-color:  #99ccff;
                padding: 20px;
                margin: 0px;
                font: 16px sans-serif;
                border-radius: 20px;
            }

            .labels {
            	font-weight: bold;
            }

            .error {
            	color: red;
            }

            .submit {
            	width: 100px;
            	height: 40px;
            	font-size: 20px;
            	text-align: center;
            }
		</style>
	</head>
	<body>
		<div>
			<form action="/" method="post">
				<h1>Sign Up!<h1>
				<table colspan="3">
					<tr>
						<td><label class="labels">User Name</label></td>
						<td><input type="text" name="username" value="%(typed_username)s"></td>
						<td><label class="error">%(username)s</label></td>
					</tr>
					<tr>
						<td><label class="labels">Password</label></td>
						<td><input type="password" name="password1"></td>
						<td><label class="error">%(password)s</label></td>
					</tr>
					<tr>
						<td><label class="labels">Re-enter Password</label></td>
						<td><input type="password" name="password2"></td>
						<td><label class="error">%(verify)s</label></td>
					</tr>
					<tr>
						<td><label class="labels">Email (optional)</label></td>
						<td><input type="text" name="email" value="%(typed_email)s"></td>
						<td><label class="error">%(email)s</label></td>
					</tr>
				</table>
				<input class="submit" type="submit" value="Sign Up"</input>
			</form>
		</div>
	</body>
</html>
"""

USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
def valid_username(username):
	return USER_RE.match(username)

PASSWORD_RE = re.compile(r"^.{3,20}$")
def valid_password(password):
	return PASSWORD_RE.match(password)

EMAIL_RE = re.compile(r"^[\S]+@[\S]+.[\S]+$")
def valid_email(email):
	return EMAIL_RE.match(email)

class Signup(webapp2.RequestHandler):

	def get(self):
		self.response.write(signup_form % {"typed_username": "", "typed_email": "","username": "", "password": "", "verify": "", "email": ""})

	def post(self):
		have_error = False
		username = cgi.escape(self.request.get('username'))
		password = cgi.escape(self.request.get('password1'))
		verify = cgi.escape(self.request.get('password2'))
		email = cgi.escape(self.request.get('email'))

		if username and valid_username(username):
			ck_username = ""
		else:
			ck_username = "Invalid User Name"
			have_error = True

		if password and valid_password(password):
			ck_password = ""
		else:
			ck_password = "Invalid Password"
			have_error = True

		if verify and password == verify:
			ck_verify = ""
		else:
			ck_verify = "Passwords don't match"
			have_error = True

		if email and not valid_email(email):
			ck_email = "Invalid Email"
			have_error = True
		else:
			ck_email = ""

		if have_error:
			self.response.write(signup_form % {"typed_username": username, "typed_email": email, "username": ck_username, "password": ck_password, "verify": ck_verify, "email": ck_email})
		else:
			self.redirect('/welcome?username=' + username)			


class Welcome(webapp2.RequestHandler):
	
	def get(self):

		welcome_user = cgi.escape(self.request.get('username'))

		welcome = """
		<html>
			<head>
				<style>
					p {
						font-size: 40px;
						font-weight: bold;
					}
				</style>
			</head>
			<body>
				<p>Welcome %s!</p>
			</body>
		</html>
		""" % (welcome_user.capitalize())
		self.response.write(welcome)

app = webapp2.WSGIApplication([
    ('/', Signup),
    ('/welcome', Welcome)
], debug=True)
