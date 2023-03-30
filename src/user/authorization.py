
import json
import jwt
import re
from flask import request, make_response, g, jsonify
from functools import wraps
from sqlalchemy import text

class Authorization():

    @staticmethod
    def auth_required(endpoint=""):
        def inner1(func):
            @wraps(func)
            def inner2(*args):
                endpoint = str(request.url_rule)
                
                try:
                    authorization = request.headers.get("authorization")
                    if re.match("^Bearer *([^ ]+) *$", authorization, flags=0):
                        token = authorization.split(" ")[1]
                        try:
                            tokendata = jwt.decode(token, "secret_key", algorithms="HS256")
                        except Exception as e:
                            #return make_response({"ERROR": str(e)}, 401)
                            return make_response(jsonify({'status': 'error',
                                                          'message': str(e),
                                                          'data': None}),401)
                        
                        current_role = tokendata.get('payload').get('role_id')
                        
                        query = text("SELECT * FROM backtest.accessibility_view WHERE endpoint= :endpoint ")
                        result = g.session.execute(query, {'endpoint': endpoint})             
                        
                        result = result.fetchall()
                        
                        if len(result) > 0:
                            roles_allowed = json.loads(result[0][1])
                            if current_role in roles_allowed:
                                return func(*args)
                            else:
                                return make_response(jsonify({'status': 'error',
                                                              'message': 'Invalid Role',
                                                              'data': None}), 422)
                        else:
                            return make_response(jsonify({'status': 'error',
                                                          'message': 'Invalid endpoint',
                                                          'data': None}), 404)
                    else:
                        return make_response(jsonify({'status': 'error',
                                                      'message': 'Invalid token',
                                                      'data': None}), 401)
                except Exception as e:
                    return make_response(jsonify({'status': 'error',
                                                  'message': str(e),
                                                  'data': None}), 401)
            return inner2
        return inner1