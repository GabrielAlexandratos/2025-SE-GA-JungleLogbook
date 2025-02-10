from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, SubmitField, DateField, TextAreaField
from wtforms.validators import DataRequired, Length

class ExpenseForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired('Title is required and a minimum of 2 characters'), Length(min=2, max=50)], render_kw={'placeholder': 'e.g. IGA'})
    category = StringField('Category', validators=[DataRequired(), Length(min=2, max=50)], render_kw={'placeholder': 'e.g. Groceries'})
    amount = FloatField('Amount', validators=[DataRequired()])
    date = DateField('Date', validators=[DataRequired()], default=datetime.today)
    description = TextAreaField('Description', validators=[Length(max=255)])
    submit = SubmitField('Submit')

    def __repr__(self):
        return f"ExpenseForm('{self.title.data}', '{self.category.data}', {self.amount.data}, {self.date.data})"
