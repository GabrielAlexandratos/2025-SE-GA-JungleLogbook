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

@expense_bp.route('/delete/<int:id>', methods=['POST'])
def delete(id):
    expense_service.delete(db_session(), id)
    return redirect(url_for('home'))

@expense_bp.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    expense = expense_service.get_by_id(db_session(), id)
    form = ExpenseForm(obj=expense) 
    if form.validate_on_submit():
        expense_service.update(db_session(), id, form.title.data, form.category.data, form.amount.data, form.date.data, form.description.data)
        return redirect(url_for('home'))
    return render_template('edit_expense.html', form=form)
