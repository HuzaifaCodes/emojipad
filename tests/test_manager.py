import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from core.emoji_manager import EmojiManager

def test_smart_sorting():
    manager = EmojiManager()
    
    # Test 1: Default Happy Profile
    manager.set_mode("Happy")
    
    print("Initial Mapping (Happy):")
    # Should be default order: 😀, 😃, 😄...
    # Mapping: 1->😀, 2->😃 etc.
    print(f"Key 1: {manager.get_mapping('1')}")
    print(f"Key 2: {manager.get_mapping('2')}")
    
    # Test 2: Usage Update
    # Let's say we use '😂' (which is further down the list initially) A LOT.
    # It is initially at index 7 -> Key 8?
    # Happy list: ["😀", "😃", "😄", "😁", "😆", "😅", "🤣", "😂", "🙂"]
    # Indices:      0     1     2     3     4     5     6     7     8
    # Keys:         1     2     3     4     5     6     7     8     9
    
    target_emoji = "😂" 
    print(f"\nTraining '{target_emoji}' with 50 usages...")
    for _ in range(50):
        manager.register_usage(target_emoji)
        
    # Now '😂' should have count 50. Others 0 (or whatever saved).
    # It should move to the TOP of the sorted list.
    # So it should be mapped to Key 1.
    
    print("New Mapping (Happy) after training:")
    new_key_1 = manager.get_mapping('1')
    print(f"Key 1: {new_key_1}")
    
    if new_key_1 == target_emoji:
        print("SUCCESS: Target emoji moved to Key 1.")
    else:
        print(f"FAILURE: Key 1 is {new_key_1}, expected {target_emoji}")

if __name__ == "__main__":
    test_smart_sorting()
