import sys
sys.path.insert(0, 'C:/Users/Kaiden/Desktop/goal-dev-spec/src')
from goal_kit.cli import main
import click

# Print all registered commands
print("Registered commands:")
for name, cmd in main.commands.items():
    print(f"  {name}: {cmd}")

# Try to invoke the check command directly
try:
    ctx = click.Context(main)
    ctx.invoke(main.get_command(ctx, 'check'))
except Exception as e:
    print(f"Error invoking check command: {e}")