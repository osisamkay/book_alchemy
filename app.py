from flask import Flask, render_template, request, flash, redirect, url_for
from data_model import app, db, Author, Book


@app.route('/add_author', methods=['GET', 'POST'])
def add_author():
    if request.method == 'POST':
        name = request.form['name']
        birth_date = request.form['birthdate']
        date_of_death = request.form['date_of_death']

        author = Author(name=name, birth_date=birth_date, date_of_death=date_of_death)
        db.session.add(author)
        db.session.commit()

        return render_template('add_author.html', success_message="Author added successfully!")
    else:
        return render_template('add_author.html')


@app.route('/add_book', methods=['GET', 'POST'])
def add_book():
    authors = Author.query.all()

    if request.method == 'POST':
        isbn = request.form['isbn']
        title = request.form['title']
        publication_year = request.form['publication_year']
        author_id = request.form['author']

        book = Book(isbn=isbn, title=title, publication_year=publication_year, author_id=author_id)
        db.session.add(book)
        db.session.commit()

        return render_template('add_book.html', authors=authors, success_message="Book added successfully!")
    else:
        return render_template('add_book.html', authors=authors)


@app.route('/')
def home():
    books = Book.query.join(Author, Author.id == Book.author_id).all()
    return render_template('home.html', books=books)


@app.route('/sort_books', methods=['POST'])
def sort_books():
    sort_by = request.form['sort_by']
    books = Book.query.join(Author, Author.id == Book.author_id).add_columns(
        Book.title, Author.name, Book.isbn).all()

    if sort_by == 'title':
        books.sort(key=lambda x: x.title)
    elif sort_by == 'author':
        books.sort(key=lambda x: x.name)

    return render_template('home.html', books=books)


@app.route('/search_books', methods=['GET'])
def search_books():
    keyword = request.args.get('keyword', '').strip()

    if keyword:
        books = Book.query.join(Author, Author.id == Book.author_id).filter(
            (Book.title.like(f"%{keyword}%")) | (Author.name.like(f"%{keyword}%"))
        ).all()
    else:
        books = []

    return render_template('home.html', books=books)


@app.route('/book/<int:book_id>/delete', methods=['POST'])
def delete_book(book_id):
    book = Book.query.get_or_404(book_id)

    # Check if the book's author has any other books in the library
    author_id = book.author_id
    author = Author.query.get(author_id)
    has_other_books = Book.query.filter_by(author_id=author_id).count() > 1

    # Delete the book and, if necessary, the author
    db.session.delete(book)
    if not has_other_books:
        db.session.delete(author)

    db.session.commit()

    flash('The book has been deleted successfully!', 'success')
    return redirect(url_for('home'))


@app.route('/book/<int:book_id>')
def book_detail(book_id):
    book = Book.query.get_or_404(book_id)
    return render_template('book_detail.html', book=book)


@app.route('/author/<int:author_id>')
def author_detail(author_id):
    author = Author.query.get_or_404(author_id)
    return render_template('author_detail.html', author=author)


if __name__ == '__main__':
    app.run(debug=True)
