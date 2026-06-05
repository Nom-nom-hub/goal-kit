from goalkit.templates import TemplateManager
import sys

print(f"Python path: {sys.path}")
print(f"TemplateManager attributes: {dir(TemplateManager)}")

try:
    headers = TemplateManager._get_auth_headers("test")
    print(f"Auth headers success: {headers}")
except Exception as e:
    print(f"Auth headers failed: {e}")

manager = TemplateManager()
print(f"Manager instance attributes: {dir(manager)}")
