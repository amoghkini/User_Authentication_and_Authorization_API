from flask import jsonify, request
from flask.views import MethodView

engine = None

class SignUpAPI(MethodView):
    def get(self):
        # Retrieve all users from the database
        query = "SELECT * FROM users"
        return query
        with engine.connect() as connection:
            result = connection.execute(query)
            users = result.fetchall()

        # Convert the users to a JSON response
        users_dict = [{'id': u[0], 'username': u[1], 'email': u[2]}
                      for u in users]
        return jsonify(users_dict)

    def post(self):
        # Parse the JSON request data
        data = request.get_json()
        try:
            first_name = data.get('first_name')
            last_name = data.get('last_name')
            email = data.get('email')
            password = data.get('password')
            confirm_password = data.get('confirm_password')
            mobile_no = data.get('mobile_no')
            date_of_birth = data.get('date_of_birth')

            if len(email) < 10:
                raise ValueError("Invalid email address")
            
            # Insert the new user into the database
            query = f"INSERT INTO users (username, email) VALUES ('{first_name}', '{email}')"
            
            
            
            
            # Return a success message
            return jsonify({'message': 'User created successfully'})
        except Exception as e:
            print(e)
            return jsonify({"Error":str(e)})

'''
#Sample code to read from db
@app.route('/')
def index():
    # Retrieve user input from the query string
    user_input = request.args.get('user_input')

    # Use a parameterized query to avoid SQL injection
    query = text('SELECT * FROM my_table WHERE column1 = :input')
    result = g.session.execute(query, {'input': user_input})

    # Retrieve the rows returned by the query
    rows = result.fetchall()

    # Process the rows as needed
    for row in rows:
        print(row)

    return 'Hello World!'
'''