import os
from itsdangerous import URLSafeTimedSerializer


s = URLSafeTimedSerializer(os.environ['SECRET_KEY_AUTH'])