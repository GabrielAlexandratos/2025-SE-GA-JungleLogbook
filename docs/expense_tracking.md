# Expense Tracking

Finally, we can add expense tracking to our application. This will allow users to record expenses and view spending history.

## Step 1: Create an Expense Model

We already have our model from earlier in `models.py`

```python
class Expense(db.Model):
    """Model for storing expense details."""

    __tablename__ = "expense"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    amount = db.Column(db.Float, nullable=False, default=0.0)
    date = db.Column(db.Date, nullable=False, default=datetime.now(timezone.utc))
    description = db.Column(db.String(255), nullable=True)

    def __repr__(self):
        return f"Expense('{self.title}', '{self.category}', {self.amount}, {self.date})"
```

# Step 2: Create Expense Form

We will create a form for users to input expense details. This can be done using Flask-WTF. Add the following to a new file called `forms.py`. 

```python
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
```

In the code above are examples of using placeholders and a default date of today. You could improve this by providing a dropdown menu for the category field, allowing users to select from a list of pre-defined categories. This would make the form more user-friendly and reduce the likelihood of errors.

# Step 3: Create a route for adding an expense

Create a new file called `expense_routes.py` in `src/expense_tracking/` directory. Add the following code to create a new route for the expense form:

```python
from flask import Blueprint, render_template, redirect, url_for
from forms import ExpenseForm
from services import ExpenseService
from extensions import db_session

expense_bp = Blueprint("expenses", __name__, url_prefix="/expenses", template_folder="templates")
expense_service = ExpenseService() 

@expense_bp.route('/add_expense', methods=['GET', 'POST'])
def add_expense():
    form = ExpenseForm()
    if form.validate_on_submit():
        expense_service.create(db_session(), form.title.data, form.category.data, form.amount.data, form.date.data, form.description.data)
        return redirect(url_for('home'))
    return render_template('add_expense.html', form=form)

```

We also need to update the navigation to use the `add_expense` route. Update the `home.html` file to include a link to the expense form.

```html
<!-- home.html ... -->
     <div class="collapse navbar-collapse" id="navbarText">
        <ul class="navbar-nav me-auto mb-2 mb-lg-0">
          <li class="nav-item">
            <a class="nav-link active" aria-current="page" href="#">Home</a>
          </li>
          <li class="nav-item">
            <a class="nav-link" href="/expenses/add_expense">Add Expense</a>  <!-- Change this line -->
          </li>
```

# Step 4: Create a service to handle expenses
Add the following to `services.py`.

```python
from sqlalchemy import func
from sqlalchemy.orm import Session

from models import User, Expense

# ....

class ExpenseService:
    def get_expenses(self, session: Session):
        return session.query(Expense).order_by('date').all()
    
    def create(self, session: Session, title, category, amount, date, description) -> Expense:
        new_expense = Expense(title=title, category=category, amount=amount, date=date, description=description)
        session.add(new_expense)
        session.commit()
        return new_expense

    def update(self, session, expense_id, title=None, category=None, amount=None, date=None, description=None) -> Expense:
        expense = session.query(Expense).get(expense_id)
        if not expense:
            raise ValueError(f"Expense {expense_id} does not exist")
        if title is not None:
            expense.title = title
        if category is not None:
            expense.category = category
        if amount is not None:
            expense.amount = amount
        if date is not None:
            expense.date = date
        if description is not None:
            expense.description = description
        session.commit()
        return expense

    def delete(self, session, expense_id) -> Expense:
        expense = session.query(Expense).get(expense_id)
        if not expense:
            raise ValueError("Expense does not exist")
        session.delete(expense)
        session.commit()
        return expense
    
    def get_by_id(self, session, expense_id) -> Expense:
        expense = session.query(Expense).get(expense_id)
        if not expense:
            raise ValueError(f"Expense {expense_id} does not exist")
        return expense

    def calculate_total(self, session) -> float:
        total_expenses = session.query(func.sum(Expense.amount)).scalar()
        return total_expenses or 0.0
```

# Step 5: Create a template for the expense form

Create a new file called `add_expense.html` in the templates directory. Add the following code to create a new template for the expense form:

```html
{% extends 'base.html' %}
{% block content %}
<h1>Add Expense</h1>
<form method="POST" novalidate>
    {{ form.hidden_tag() }}
    <div class="form-group">
        {{ form.title.label }}<br>
        {{ form.title(size=20) }}
        {% for error in form.title.errors %}
        <span style="color: red;">[{{ error }}]</span>
        {% endfor %}
    </div>
    <div class="form-group">
        {{ form.category.label }}<br>
        {{ form.category(size=20) }}
    </div>
    <div class="form-group">
        {{ form.amount.label }}<br>
        {{ form.amount(size=20) }}
    </div>
    <div class="form-group">
        {{ form.date.label }}<br>
        {{ form.date(size=20) }}
    </div>
    <div class="form-group">
        {{ form.description.label }}<br>
        {{ form.description(size=20) }}
    </div>
    <p>{{ form.submit() }}</p>
</form>
{% endblock %}
```

The above code is a Flask template for adding an expense. It extends the `base.html` template and includes a form with fields for title, category, amount, date, and description. The form uses WTForms to generate the HTML input elements and labels. The form also has a submit button. This is an alternative way of creating forms in Flask using WTForms rather than HTML forms directly. The benefit here is that WTForms provides more functionality such as validation and CSRF protection out of the box. We also display the form errors if any are present for th title field.

Try running the code and see if it works as expected. There is more you could do with making the UI more user friendly, but this should give you a good starting point for enhancing the expense tracking form in Flask using WTForms.

# Step 5: Displaying Expenses

Once you have created the form to add expenses, you will need to display them on a page. You can do this by querying the database and passing the results to the template. Modify the `home` route to display all expenses and a total. Make the following changes to `app.py`.

```python
# ...
from config import config, Config
from extensions import db, migrate, login_manager, db_session, csrf
from services import UserService, ExpenseService
# ...
from auth import auth_bp
from expense_routes import expense_bp        # Add this line to import the expense routes
# ...
def create_app(configuration: str = "default") -> Flask:
    app = Flask(__name__)
    app.register_blueprint(auth_bp)
    app.register_blueprint(expense_bp)     # Add this line to register the expense blueprint
# ...
    @app.route("/home")
    @login_required
    def home():
        logger.info("Rendering the home page")
        expenses = expense_service.get_expenses()
        total = sum(expense.amount for expense in expenses)
        logger.info(f"Calculated total expenses: {total}")
        logger.info(f"Retrieved {len(expenses)} expenses for the current user")
        logger.info("Rendering the home page with expenses")
        return render_template("home.html", expenses=expenses, total_amount=total)

    return app

user_service = UserService()
expense_service = ExpenseService()

```

The primary activity here is querying the `Expense` model via an expense service to retrieve all expenses. The reason for using a service rather than directly accessing the database is:
- it improves testability of the code
- follows the Single Responsibility Principle (SRP) by encapsulating database access logic in a separate service class.

We then pass this list of expenses and total to the `home.html` template as variables `expenses` and `total_amount` respectively. In the template, we loop through each expense and display its title, description, and amount.

```html
<!-- other nav code above here -->
</nav>
<div class="container">
    <h1>Daily Expenses</h1>
    <table class="table table-striped">
        <thead>
            <tr>
                <th>Date</th>
                <th>Title</th>
                <th>Category</th>
                <th>Description</th>
                <th class="text-end">Amount</th>
            </tr>
        </thead>
        <tbody>
            {% for expense in expenses %}
            <tr>
                <td>{{ expense.date }}</td>
                <td>{{ expense.title }}</td>
                <td>{{ expense.category }}</td>
                <td>{{ expense.description }}</td>
                <td class="text-end">{{ '{0:.2f}'.format(expense.amount) }}</td>
                <td class="text-end"><a href="/expenses/edit/{{ expense.id }}" class="btn btn-warning">Edit</a></td>
                <td>
                    <form action="/expenses/delete/{{ expense.id }}" method=post>
                        <input type="hidden" name="_csrf_token" value="{{ csrf_token() }}">
                        <button type="submit" class="btn btn-danger">Delete</button>
                    </form> 
                </td>
            </tr>
            {% endfor %}
            <tr>
                <td colspan="4"><strong>Total Amount:</strong></td>
                <td class="text-end">{{ total_amount }}</td>
            </tr>
        </tbody>
    </table>
    <a href="/search_entries" class="btn btn-primary">Search Entries</a>
</div>

{% endblock %}
```
The other feature added to the expense table is the ability to edit and delete expenses. The edit button takes the user to a new page where they can update the expense details, while the delete button submits a form that sends a POST request to the server with the ID of the expense to be deleted.

An improvement in the code would be to use pagination when displaying a large number of expenses. This can be achieved by passing the page number and number of items per page as arguments to the `get_all_expenses` method, and then using Flask's built-in support for pagination in the template.

# Step 6: Delete an Expense
To delete an expense, we need to add a new route that handles the deletion request. This route will take the ID of the expense to be deleted as a parameter, call the `delete_expense` method on the expense service with this ID, and then redirect the user back to the expense list page.

```python
# expense_routes.py
@expense_bp.route('/delete/<int:id>', methods=['POST'])
def delete(id):
    expense_service.delete(db_session(), id)
    return redirect(url_for('home'))

```

# Step 7: Update an Expense
To update an expense, we need to add a new route that handles the update request. This route will take the ID of the expense to be updated as a parameter, retrieve the updated data from the form, call the `update_expense` method on the expense service with this data and ID, and then redirect the user back to the expense list page.

```python
# expense_routes.py
@expense_bp.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    expense = expense_service.get_by_id(db_session(), id)
    form = ExpenseForm(obj=expense) 
    if form.validate_on_submit():
        expense_service.update(db_session(), id, form.title.data, form.category.data, form.amount.data, form.date.data, form.description.data)
        return redirect(url_for('home'))
    return render_template('edit_expense.html', form=form)
```

Add in the `edit_expense.html` template to display the form for editing an expense.

```html
<!-- templates/edit_expense.html -->
{% extends "base.html" %}
{% block content %}

<h1>Edit Expense</h1>
<form method="POST">
    {{ form.hidden_tag() }}
    <div class="form-group">
        {{ form.title.label }}<br>
        {{ form.title(size=20) }}
    </div>
    <div class="form-group">
        {{ form.category.label }}<br>
        {{ form.category(size=20) }}
    </div>
    <div class="form-group">
        {{ form.amount.label }}<br>
        {{ form.amount(size=20) }}
    </div>
    <div class="form-group">
        {{ form.date.label }}<br>
        {{ form.date(size=20) }}
    </div>
    <div class="form-group">
        {{ form.description.label }}<br>
        {{ form.description(size=20) }}
    </div>
    <p>{{ form.submit() }}</p>
</form>

{% endblock %}
```

The edit page is almost identical to the add page. We create both rather that reuse the same template because we may want to have different forms for each action. For example, we might want to validate the date differently on the edit page than on the add page. Also using the same form for 2 purposes could lead to confusion and bugs. The down side of this is that we need to duplicate code. However, in this case, the duplication is minimal and the benefits outweigh the costs.


[< Prev: Authentication Frontend ](./expense_tracking.md) | [Next: Testing >](./testing.md)








