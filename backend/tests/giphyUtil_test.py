from .. import tests
import pytest
from backend import giphyUtil
@pytest.fixture(autouse=True)
def giphy_util(request):
    return giphyUtil.GiphyUtil(tests.GIPHY_API_KEY)

valid_giphy_test_tags=tests.valid_giphy_test_tags
assert len(valid_giphy_test_tags) >=1
@pytest.mark.parametrize('query',valid_giphy_test_tags)
def test__fetch_giphy(giphy_util: giphyUtil.GiphyUtil,query: str):
    giphy_urls = giphy_util._fetch_giphy(query)
    assert len(giphy_urls) > 1
    assert len(giphy_urls) == len(set(giphy_urls))
    
@pytest.mark.parametrize('giphy_tag',valid_giphy_test_tags)
def test_fetch_multimedia(giphy_util: giphyUtil.GiphyUtil,giphy_tag: str):
    (_, returned_tag) = giphy_util.fetch_multimedia(giphy_tag)
    assert returned_tag==giphy_tag
