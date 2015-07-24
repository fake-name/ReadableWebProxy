from flask.ext.wtf import Form
from flask.ext.babel import gettext
from wtforms import StringField
from wtforms import BooleanField
from wtforms import TextAreaField
from wtforms import FormField
from wtforms import PasswordField
from wtforms import SelectField
from wtforms import HiddenField
from wtforms.fields import RadioField
from wtforms.fields.html5 import DateTimeField
from wtforms.validators import DataRequired
from wtforms.validators import Length
from wtforms.validators import Email
from wtforms.validators import EqualTo
from wtforms.validators import ValidationError
from wtforms.validators import URL
from flask.ext.bcrypt import check_password_hash

def loginError():
	raise ValidationError("Your username or password is incorrect.")


class NewSeriesForm(Form):
	name =   StringField('Series Title', validators=[DataRequired(), Length(min=1)])
	type =   RadioField( 'Series Type',
				validators=[DataRequired(message='You must supply select a type.')],
				choices=[('oel', 'OEL - (original english language)'), ('translated', 'Translated')])

class NewGroupForm(Form):
	name  =   StringField('Group Name', validators=[DataRequired(), Length(min=1)])



def check_group(form, field):

	try:
		dat = int(field.data)
	except ValueError:
		raise ValidationError("Invalid group value! You must select a group.")
	if dat < 0:
		raise ValidationError("Invalid group value! You must select a group.")
	print("group validated")

def check_volume(form, field):
	if field.data:
		try:
			dat = int(field.data)
		except ValueError:
			raise ValidationError("Volume must be an integer value!")
	if not (field.data or form.chapter.data):
		raise ValidationError("Volume and chapter cannot both be empty!")


def check_chapter(form, field):
	if field.data:
		try:
			dat = int(field.data)
		except ValueError:
			raise ValidationError("Chapter must be an integer value!")
	if not (field.data or form.volume.data):
		raise ValidationError("Volume and chapter cannot both be empty!")

def check_sub_chapter(form, field):
	if field.data:
		try:
			dat = int(field.data)
		except ValueError:
			raise ValidationError("Sub-Chapter must be an integer value!")



class NewReleaseForm(Form):
	volume      = StringField('Volume', validators=[check_volume])
	chapter     = StringField('Chapter', validators=[check_chapter])
	subChap     = StringField('Sub-Chapter', validators=[check_sub_chapter])
	postfix     = StringField('Additional release titles', [Length(max=64)])
	group       = SelectField('Group', validators=[check_group], coerce=int, default=-1)
	series_id   = HiddenField('series')
	is_oel      = HiddenField('is_oel')
	release_pg  = StringField('Release URL', [URL(message='You must supply a link to the released chapter/volume.')])
	releasetime = DateTimeField('Release Date', format='%Y/%m/%d %H:%M')


# class EditForm(Form):
# 	nickname = StringField('nickname', validators=[DataRequired()])
# 	about_me = TextAreaField('about_me', validators=[Length(min=0, max=140)])

# 	def __init__(self, original_nickname, *args, **kwargs):
# 		Form.__init__(self, *args, **kwargs)
# 		self.original_nickname = original_nickname

# 	def validate(self):
# 		if not Form.validate(self):
# 			return False
# 		if self.nickname.data == self.original_nickname:
# 			return True
# 		if self.nickname.data != Users.make_valid_nickname(self.nickname.data):
# 			self.nickname.errors.append(gettext(
# 				'This nickname has invalid characters. '
# 				'Please use letters, numbers, dots and underscores only.'))
# 			return False
# 		user = Users.query.filter_by(nickname=self.nickname.data).first()
# 		if user is not None:
# 			self.nickname.errors.append(gettext(
# 				'This nickname is already in use. '
# 				'Please choose another one.'))
# 			return False
# 		return True


class PostForm(Form):
	title = StringField('Title', validators=[DataRequired(), Length(max=128)])
	content = TextAreaField('Content', validators=[DataRequired()])


class SearchForm(Form):
	search = StringField('search', validators=[DataRequired()])

