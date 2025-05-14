from app import myapp_obj, db

if __name__ == "__main__":

    with myapp_obj.app_context():
        db.create_all()

    myapp_obj.run(debug=True)

