import unittest
from time_traveller.resolver import SpotifyResolver
from time_traveller.auth import get_access
from time_traveller.config import settings

class TestResolver(unittest.TestCase):
    def test_initialization(self):
        sp = get_access(dict(**settings.Auth))
        resolver = SpotifyResolver(sp)
        self.assertIsInstance(resolver, SpotifyResolver)

        print(resolver.sp.current_user())
        print(resolver.cache)
    
if __name__ == "__main__":
    unittest.main()