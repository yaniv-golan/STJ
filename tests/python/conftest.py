import sys
import os

# Add tools/python to sys.path
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, '../../'))
tools_python = os.path.join(project_root, 'tools', 'python')
sys.path.insert(0, tools_python)
