class Config:
    SECRET_KEY = '12b6eb605e8a828ede6c58d0621cd2c7'
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:4561@localhost:5432/nix_edu'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = 'D:\\nix_ed_film_library\\images'
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
