import sys
import os

if not getattr(sys, 'frozen', False):
    # Add the src directory to the module path for non-frozen execution
    sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'src'))

if __name__ == '__main__':
    from emojipad.__main__ import main
    main()
