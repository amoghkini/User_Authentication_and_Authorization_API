from marshmallow import Schema, fields, validate, validates, ValidationError, validates_schema

gender = ["Male", "Female", "Other"]

class SignUpUser(Schema):
    first_name = fields.Str(required = True, 
                            validate=validate.Length(min = 2, max = 45))
    last_name = fields.Str(required = True, 
                           validate = validate.Length(min=2, max=45))
    email = fields.Str(required = True, 
                       validate=validate.Length(min=2, max=45))
    password = fields.Str(required=True, 
                          validate = validate.Length(min=2, max=45))
    confirm_password = fields.Str(required = True, 
                                  validate=validate.Length(min=2, max=45))
    gender = fields.Str(required = True,
                        validate = validate.OneOf(gender))
    mobile_no = fields.Str(required = True, 
                           validate=validate.Length(min=10,max=10))
    date_of_birth = fields.Str(required=True)
    
    # Just an example to demonstrate the single field validation to use in later stages of the development.
    @validates('password')
    def validate_password(self, password, ):
        if len(password) > 45:
            raise ValidationError('Lenght of the password should be less than or equal to 45')

    @validates_schema
    def validate_password_and_confirm_password(self, data, **kwargs):
        errors = {}
        if data['password'] != data['confirm_password']:
            errors['password'] = 'Password and confirm password should be same.'
            raise ValidationError(errors)