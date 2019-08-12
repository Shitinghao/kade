# lkade

## DB type
+ apis.py: CNDBpedia form
+ apis_v2.py: entities with ID, distinguish REL and ATTR.

## DEV
```
pushd lkade-backend
python apis.py   or  python apis_v2.py
popd
pushd lkade-front
npm run dev
```

ATTENTION: change lkade-backend/utils.py line 6 to always return True to disable authority testing becuase CORS.

## PROD
+ Directly run lkade-backend/apis.py or lkade-backend/apis_v2.py.
+ python apis.py prod
