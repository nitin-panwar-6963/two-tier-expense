from flask import Flask, render_template, request, redirect, url_for, jsonify, flash
from config import Config
from models import db, Expense
from datetime import datetime
from sqlalchemy import and_

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    # main page; data loaded via AJAX
    return render_template('index.html')

@app.route('/api/expenses')
def api_expenses():
    query = Expense.query

    # Filters
    search = request.args.get('search', '').strip()
    start_date = request.args.get('start_date', '')
    end_date = request.args.get('end_date', '')

    if search:
        # search in title and category
        like = f"%{search}%"
        query = query.filter((Expense.title.like(like)) | (Expense.category.like(like)))

    if start_date:
        try:
            start = datetime.strptime(start_date, '%Y-%m-%d').date()
            query = query.filter(Expense.expense_date >= start)
        except:
            pass

    if end_date:
        try:
            end = datetime.strptime(end_date, '%Y-%m-%d').date()
            query = query.filter(Expense.expense_date <= end)
        except:
            pass

    expenses = query.order_by(Expense.expense_date.desc()).all()
    total = sum([float(e.amount) for e in expenses]) if expenses else 0.0

    return jsonify({
        'total': total,
        'expenses': [e.to_dict() for e in expenses]
    })

@app.route('/add', methods=['GET', 'POST'])
def add_expense():
    if request.method == 'POST':
        title = request.form['title']
        amount = request.form['amount']
        category = request.form.get('category', 'Other')
        expense_date = request.form['expense_date']
        note = request.form.get('note')
        try:
            e = Expense(
                title=title,
                amount=float(amount),
                category=category,
                expense_date=datetime.strptime(expense_date, '%Y-%m-%d').date(),
                note=note
            )
            db.session.add(e)
            db.session.commit()
            flash('Expense added.', 'success')
            return redirect(url_for('index'))
        except Exception as ex:
            db.session.rollback()
            flash('Error adding expense: ' + str(ex), 'danger')
            return redirect(url_for('add_expense'))
    return render_template('add_edit.html', action='Add', expense=None)

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_expense(id):
    expense = Expense.query.get_or_404(id)
    if request.method == 'POST':
        expense.title = request.form['title']
        expense.amount = float(request.form['amount'])
        expense.category = request.form.get('category', 'Other')
        expense.expense_date = datetime.strptime(request.form['expense_date'], '%Y-%m-%d').date()
        expense.note = request.form.get('note')
        try:
            db.session.commit()
            flash('Expense updated.', 'success')
            return redirect(url_for('index'))
        except Exception as ex:
            db.session.rollback()
            flash('Error updating expense: ' + str(ex), 'danger')
    return render_template('add_edit.html', action='Edit', expense=expense)

@app.route('/delete/<int:id>', methods=['POST'])
def delete_expense(id):
    expense = Expense.query.get_or_404(id)
    try:
        db.session.delete(expense)
        db.session.commit()
        return jsonify({'status': 'ok'})
    except Exception as ex:
        db.session.rollback()
        return jsonify({'status': 'error', 'message': str(ex)}), 500

if __name__ == '__main__':
    # run on localhost
    app.run(host='0.0.0.0', port=5000, debug=True)

