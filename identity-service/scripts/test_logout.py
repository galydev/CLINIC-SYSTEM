"""Test script for logout functionality"""
import asyncio
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from infrastructure.security.token_blacklist import get_token_blacklist


async def test_logout_functionality():
    """Test the token blacklist functionality"""
    print("=" * 60)
    print("Testing Token Blacklist Functionality")
    print("=" * 60)

    blacklist = get_token_blacklist()

    # Test 1: Initial state
    print("\n[TEST 1] Initial state")
    print(f"Blacklist size: {blacklist.size()}")
    assert blacklist.size() == 0, "Blacklist should be empty initially"
    print("[OK] Blacklist is empty")

    # Test 2: Add token
    print("\n[TEST 2] Add token to blacklist")
    test_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.test.token"
    blacklist.add_token(test_token)
    print(f"Added token: {test_token[:20]}...")
    print(f"Blacklist size: {blacklist.size()}")
    assert blacklist.size() == 1, "Blacklist should have 1 token"
    print("[OK] Token added successfully")

    # Test 3: Check if token is blacklisted
    print("\n[TEST 3] Check if token is blacklisted")
    is_blacklisted = blacklist.is_blacklisted(test_token)
    print(f"Is token blacklisted? {is_blacklisted}")
    assert is_blacklisted, "Token should be blacklisted"
    print("[OK] Token is blacklisted")

    # Test 4: Check non-blacklisted token
    print("\n[TEST 4] Check non-blacklisted token")
    other_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.other.token"
    is_blacklisted = blacklist.is_blacklisted(other_token)
    print(f"Is other token blacklisted? {is_blacklisted}")
    assert not is_blacklisted, "Other token should not be blacklisted"
    print("[OK] Non-blacklisted token returns False")

    # Test 5: Add multiple tokens
    print("\n[TEST 5] Add multiple tokens")
    tokens = [
        "token1.test.abc",
        "token2.test.def",
        "token3.test.ghi"
    ]
    for token in tokens:
        blacklist.add_token(token)
    print(f"Added {len(tokens)} more tokens")
    print(f"Blacklist size: {blacklist.size()}")
    assert blacklist.size() == 4, "Blacklist should have 4 tokens"
    print("[OK] Multiple tokens added successfully")

    # Test 6: Remove token
    print("\n[TEST 6] Remove token from blacklist")
    removed = blacklist.remove_token(test_token)
    print(f"Token removed? {removed}")
    print(f"Blacklist size: {blacklist.size()}")
    assert removed, "Token should be removed successfully"
    assert blacklist.size() == 3, "Blacklist should have 3 tokens"
    print("[OK] Token removed successfully")

    # Test 7: Check removed token
    print("\n[TEST 7] Check removed token")
    is_blacklisted = blacklist.is_blacklisted(test_token)
    print(f"Is removed token still blacklisted? {is_blacklisted}")
    assert not is_blacklisted, "Removed token should not be blacklisted"
    print("[OK] Removed token is no longer blacklisted")

    # Test 8: Clear all tokens
    print("\n[TEST 8] Clear all tokens")
    blacklist.clear()
    print(f"Blacklist size after clear: {blacklist.size()}")
    assert blacklist.size() == 0, "Blacklist should be empty after clear"
    print("[OK] All tokens cleared successfully")

    # Test 9: Thread safety test
    print("\n[TEST 9] Thread safety test")
    import concurrent.futures

    def add_tokens_concurrently(start, count):
        for i in range(start, start + count):
            blacklist.add_token(f"concurrent.token.{i}")

    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        futures = []
        for i in range(5):
            future = executor.submit(add_tokens_concurrently, i * 10, 10)
            futures.append(future)
        concurrent.futures.wait(futures)

    print(f"Added tokens concurrently from 5 threads")
    print(f"Final blacklist size: {blacklist.size()}")
    assert blacklist.size() == 50, "Should have 50 tokens from concurrent additions"
    print("[OK] Thread-safe operations successful")

    # Cleanup
    blacklist.clear()

    print("\n" + "=" * 60)
    print("All tests passed!")
    print("=" * 60)


async def main():
    """Main test runner"""
    try:
        await test_logout_functionality()
        print("\n[SUCCESS] Logout functionality is working correctly")
        return 0
    except AssertionError as e:
        print(f"\n[FAILED] Test assertion failed: {e}")
        return 1
    except Exception as e:
        print(f"\n[ERROR] Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
