from fastapi.templating import Jinja2Templates
from jinja2 import ChoiceLoader, FileSystemLoader

# Global instance for shared templates (includes, layouts)
common_templates = Jinja2Templates(directory="templates")

# For user pages: first search in pages/user, then fallback to templates
user_templates = Jinja2Templates(directory="templates/pages/user")
user_templates.env.loader = ChoiceLoader([
    FileSystemLoader("templates/pages/user"),
    FileSystemLoader("templates")
])

# For admin pages: first search in pages/admin, then fallback to templates
admin_templates = Jinja2Templates(directory="templates/pages/admin")
admin_templates.env.loader = ChoiceLoader([
    FileSystemLoader("templates/pages/admin"),
    FileSystemLoader("templates")
])
