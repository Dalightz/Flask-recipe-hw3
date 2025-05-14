from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from app.forms import LoginForm, RecipeForm, RegisterForm
from app.models import User, Recipe
from app import myapp_obj, db 



# Home page - shows all recipes (accessible to all)
@myapp_obj.route("/")
@myapp_obj.route("/recipes")
def recipes():
    all_recipes = Recipe.query.order_by(Recipe.created.desc()).all()
    return render_template("recipes.html", recipes=all_recipes)

# New Recipe page (requires login)
@myapp_obj.route("/recipe/new", methods=['GET', 'POST'])
@login_required
def new_recipe():
    form = RecipeForm()
    if form.validate_on_submit():
        # Create a new Recipe, linking it to the current user
        recipe = Recipe( title=form.title.data,
            description=form.description.data,
            ingredients=form.ingredients.data,
            instructions=form.instructions.data,
            author=current_user  # This sets user_id automatically
        )
        db.session.add(recipe)
        db.session.commit()
        flash("Recipe added successfully!")
        return redirect(url_for('recipes'))
    return render_template("new_recipe.html", form=form)

# Recipe detail page
@myapp_obj.route("/recipe/<int:recipe_id>")
@login_required
def recipe_detail(recipe_id):
    recipe = Recipe.query.get_or_404(recipe_id)
    return render_template("recipe_detail.html", recipe=recipe)

# Delete Recipe
@myapp_obj.route("/recipe/<int:recipe_id>/delete", methods=['POST'])
@login_required
def delete_recipe(recipe_id):
    recipe = Recipe.query.get_or_404(recipe_id)
    # Only author can delete recipe
    if recipe.author != current_user:
        flash("You are not authorized to delete this recipe.")
        return redirect(url_for('recipes'))
    db.session.delete(recipe)
    db.session.commit()
    flash("Recipe deleted.")
    return redirect(url_for('recipes'))

# Login 
@myapp_obj.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        # login user
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.password == form.password.data:
            login_user(user, remember=form.remember_me.data)
            flash("Logged in successfully.")
            return redirect(url_for('recipes'))
        else:
            flash("Invalid username or password.")
    return render_template("login.html", form=form)

# Logout 
@myapp_obj.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Logged out successfully.")
    return redirect(url_for('recipes'))


@myapp_obj.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        # Check if username exists
        if User.query.filter_by(username=form.username.data).first():
            flash('Username already taken.', 'warning')
            return render_template('register.html', form=form)

        # Create and save new user
        new_user = User( username=form.username.data, password=form.password.data)
        db.session.add(new_user)
        db.session.commit()

        # log in immediately
        login_user(new_user)
        flash('Registration successful! You are now logged in.', 'success')
        return redirect(url_for('recipes'))

    return render_template('register.html', form=form)



