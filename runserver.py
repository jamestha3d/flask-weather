from api import create_app
from api.config.config import config_dict



app = create_app() #config=config_dict['production']

if __name__ == "__main__":
    app.run()

# migrate
#db.create_all()

# >>> import secrets
# >>> secrets.token_hex(12)

#test
#pytest

"""
#import os
#import re
#uri = os.getenv('DATABASE_URL')
if uri.startswith("postgres://"):
    uri = uri.replace("postgres://", "postgresql://", 1)
#  
# 
# """
