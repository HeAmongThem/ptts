from typing import Any
repoUsers:list[dict[str, Any]]  = [
    {"id": 1, "email": "admin@trust-tower.example", "password": "$2b$12$DlxERftUa4BJsKvUhmbtVOq89mrasl0BBogV2GFsU4VlF5Cn1j9hG", "business_unit": {"id": 1, "name": "BU Retail"}, "role": "ADMIN"},
    {"id": 2, "email": "cfo@trust-tower.example", "password": "$2b$12$DlxERftUa4BJsKvUhmbtVOq89mrasl0BBogV2GFsU4VlF5Cn1j9hG", "business_unit": {"id": 2, "name": "BU Corporate"}, "role": "CFO"}    ,
    {"id": 3, "email": "bu@trust-tower.example", "password": "$2b$12$DlxERftUa4BJsKvUhmbtVOq89mrasl0BBogV2GFsU4VlF5Cn1j9hG", "business_unit": {"id": 3, "name": "BU Digital"}, "role": "BU"}    ,
    {"id": 4, "email": "buHead@trust-tower.example", "password": "$2b$12$DlxERftUa4BJsKvUhmbtVOq89mrasl0BBogV2GFsU4VlF5Cn1j9hG", "business_unit": {"id": 4, "name": "BU International"}, "role": "BU_HEAD"} ,
    {"id": 5, "email": "bu.ret@trust-tower.example", "password": "$2b$12$DlxERftUa4BJsKvUhmbtVOfO4jQUI079JrEyb6H77wLcU8ht.rAde", "business_unit": {"id": 1, "name": "BU Retail"}, "role": "BU"} ,
    {"id": 6, "email": "bu-head.ret@trust-tower.example", "password": "$2b$12$DlxERftUa4BJsKvUhmbtVOgAm1F5XelixzpP5VLxLCjvkIUhHUV4e", "business_unit": {"id": 1, "name": "BU Retail"}, "role": "BU_HEAD"}   ,
    {"id": 7, "email": "bu.corp@trust-tower.example", "password": "$2b$12$DlxERftUa4BJsKvUhmbtVOfO4jQUI079JrEyb6H77wLcU8ht.rAde", "business_unit": {"id": 2, "name": "BU Corporate"}, "role": "BU"} ,
    {"id": 8, "email": "bu-head.corp@trust-tower.example", "password": "$2b$12$DlxERftUa4BJsKvUhmbtVOgAm1F5XelixzpP5VLxLCjvkIUhHUV4e", "business_unit": {"id": 2, "name": "BU Corporate"}, "role": "BU_HEAD"}   ,
    {"id": 9, "email": "bu.dig@trust-tower.example", "password": "$2b$12$DlxERftUa4BJsKvUhmbtVOfO4jQUI079JrEyb6H77wLcU8ht.rAde", "business_unit": {"id": 3, "name": "BU Digital"}, "role": "BU"}    ,
    {"id": 10, "email": "bu-head.dig@trust-tower.example", "password": "$2b$12$DlxERftUa4BJsKvUhmbtVOgAm1F5XelixzpP5VLxLCjvkIUhHUV4e", "business_unit": {"id": 3, "name": "BU Digital"}, "role": "BU_HEAD"} ,
    {"id": 11, "email": "bu.int@trust-tower.example", "password": "$2b$12$DlxERftUa4BJsKvUhmbtVOfO4jQUI079JrEyb6H77wLcU8ht.rAde", "business_unit": {"id": 4, "name": "BU International"}, "role": "BU"} ,
    {"id": 12, "email": "bu-head.int@trust-tower.example", "password": "$2b$12$DlxERftUa4BJsKvUhmbtVOgAm1F5XelixzpP5VLxLCjvkIUhHUV4e", "business_unit": {"id": 4, "name": "BU International"}, "role": "BU_HE   AD"},
    {"id": 13, "email": "bu.serv@trust-tower.example", "password": "$2b$12$DlxERftUa4BJsKvUhmbtVOfO4jQUI079JrEyb6H77wLcU8ht.rAde", "business_unit": {"id": 5, "name": "BU Services"}, "role": "BU"} ,
    {"id": 14, "email": "bu-head.serv@trust-tower.example", "password": "$2b$12$DlxERftUa4BJsKvUhmbtVOgAm1F5XelixzpP5VLxLCjvkIUhHUV4e", "business_unit": {"id": 5, "name": "BU Services"}, "role": "BU_HEAD"}
]