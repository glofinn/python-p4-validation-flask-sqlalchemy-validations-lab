from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
db = SQLAlchemy()

class Author(db.Model):
    __tablename__ = 'authors'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, unique = True)
    phone_number = db.Column(db.Integer)

    @validates('name')
    def validate_name(self, key, name):
        names = db.session.query(Author.name).all()
        if not name:
            raise ValueError('Name must not be empty')
        elif name in names:
            raise ValueError('Name already in use')
        return name

    @validates('phone_number',)
    def validate_phone(self, key, phone):
        if len(phone) != 10:
            raise ValueError('Phone number must be 10 characters')
        return phone
    

class Post(db.Model):
    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String)
    summary = db.Column(db.String)
    category = db.Column(db.String)

    @validates('title')
    def validate_title(self, key, title):
        clickbait = ["Won't Believe", "Secret", "Top", "Guess"]
        if not any(substring in title for substring in clickbait):
            raise ValueError('No clickbait found')
        return title
    

    @validates('content', 'summary')
    def validate_content(self, key, string):
        if (key == 'content'):
            if len(string) <= 250:
                raise ValueError('Post content must be greater than 250 characters')
        if (key == 'summary'):
            if len(string) >= 250:
                raise ValueError('Post summary must be less than 250 characters')
            
            return string
    
    # @validates('post_content')
    # def validate_post_content(self, key, post_content):
    #     if len(post_content) <= 250:
    #         raise ValueError('Post content must be greater than 250 characters')
    #     return post_content

    # @validates('post_summary')
    # def validate_post_summary(self, key, post_summary):
    #     if len(post_summary) >= 250:
    #         raise ValueError('Post summary must be less than 250 characters')
    #     return post_summary
        
    @validates('category')
    def validate_post_category(self, key, category):
        if category != 'Fiction' and category != 'Non-Fiction':
            raise ValueError('Post category must be Fiction or Non-Fiction')
        return category