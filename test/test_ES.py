import sys
sys.path.append('.')
import pytest
import logging

logger = logging.getLogger(__name__)
from mapper import ESClient
from Kit.connector import es_client
from pytest import fixture


def test_search():
    res = es_client.search(  index_name="kenger_blog", query={"query": {"match_all": {}}})
    logger.info(res)


def test_search_by_content():
    res = es_client.search_by_content( index_name="kenger_blog", content="linux")
    logger.info(res)
    


def test_search_by_title():
    res = es_client.search_by_title( index_name="kenger_blog", title="大模型")
    logger.info(res)
    
    
import re
import uuid
from typing import List
from Kit import *
from service import *
from Kit.connector import es_client

# 测试示例
def test_save_all_md_to_es():
   save_all_md_to_es(es_client, "kenger_blog", "data")