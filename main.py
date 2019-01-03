from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['DEBUG'] = True      # displays runtime errors in the browser, too
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:password123@localhost:3306/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
app.secret_key = 'secret'

db = SQLAlchemy(app)



#create a blog class with an ID, Title, and Body

class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(1000))

    def __init__(self, title, body):
        self.title = title
        self.body = body
    
    def valid_blog(self):
        if self.title and self.body:
            return True
        else:
            return False

def blog_by_id(blog_id):
    print("Blog ID")
    return Blog.query.filter_by(id=blog_id)


#routes
@app.route('/')

def index():
    return redirect('/blogs')

@app.route('/blog_post')
def route_blog():
    return render_template('blog_post.html')



@app.route('/blogs')
def show_blogs():
    blog_id = request.args.get('id')
    if blog_id:
        print('---------')
        print(blog_id)
        blogs = Blog.query.all()
        title = blogs[int(blog_id) - 1].title
        body = blogs[int(blog_id) - 1].body
        return render_template('blog_post.html', blog_title=title, blog_body=body)
        '''
        blog_title = request.args.get('title')
        blog_body = request.args.get('body')
        return render_template('blog_post.html',
                                title='Build-A-Blog', 
                                blog_title=blog_title,
                                blog_body=blog_body)
                                '''
    else:
        print("Test")
        blogs = Blog.query.all()
        return render_template('blogs.html', title="All Blogs", blogs=blogs)
    

@app.route('/add_blog',methods=['POST','GET'])

def add_blog():

    blog_error = ''

    if request.method == 'POST':
        blog_title = request.form['title']
        blog_body = request.form['body']
        new_blog = Blog(blog_title, blog_body)

        if new_blog.valid_blog():
            db.session.add(new_blog)
            db.session.commit()

            return redirect("/?id=" + str(new_blog.id))
        else:
            blog_error = "Blog Entry Criteria not met, try again! Provide a title and content!"
            flash("Please check your entry for errors. Both a title and a body are required.")
            return render_template('add_blog.html',
                title="Add-A-Blog",
                blog_title=blog_title,
                blog_body=blog_body,
                blog_error=blog_error)

    else: # GET request
        return render_template('add_blog.html', title="Add-A-Blog")

if __name__ == '__main__':
    app.run()