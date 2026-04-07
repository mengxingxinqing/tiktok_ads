# Get catalogs

**Doc ID**: 1740315452868610
**Path**: API Reference/Catalog Management/Get catalogs

---

Use this endpoint to get information about a catalog or all catalogs under a Business Center.

## Comparing v1.2 and v1.3
 ```xtable
 |Changes{30%}|v1.2{35%}|v1.3{35%}|
|---|---|---|
|Endpoint path| /v1.2/catalog/get/| /v1.3/catalog/get/|
|Request parameter data type |`bc_id`: number
`catalog_id`: number|`bc_id`: string
`catalog_id`: string|
|Response parameter name|`name`|`catalog_name`|
|Response parameter data type|`bc_id`: number
`catalog_id`: number|`bc_id`: string
`catalog_id`: string|
|New response parameters|/|`ad_creation_eligible`
`additional_config_list`|
```

## Request

**Endpoint** https://business-api.tiktok.com/open_api/v1.3/catalog/get/

**Method** GET

**Header**

``` xtable
|Field|Data Type|Description|
|---|---|---|
|Access-Token {Required}|string|Authorized access token. For details, see [Authentication](https://ads.tiktok.com/marketing_api/docs?id=1738373164380162).|
```

**Parameters**

``` xtable
| Field | Type | Description |
|--- |--- |--- |
| bc_id {Required} | string | Business Center ID. |
| catalog_id | string | Catalog ID. 

If not specified, all catalogs will be returned. |
| page | number | Current number of pages.

 Default value: 1. 

Value range: ≥ 1. |
| page_size | number | Page size. 

Default value: 10. 

Value range: 1-1,000. |
```

### Example

```xcodeblock
(code curl http)

curl -X GET -H "Access-Token:YOUR_ACCESS_TOKEN" \
--data-urlencode "bc_id=BC_ID" \
--data-urlencode "catalog_id=CATALOG_ID" \

https://business-api.tiktok.com/open_api/v1.3/catalog/get/

(/code)

```

## Response
``` xtable
| Field | Type | Description |
|--- |--- |--- |
| code | number  |Return code. For the complete list of response codes and descriptions, see [Appendix - return codes](https://ads.tiktok.com/marketing_api/docs?id=1737172488964097). |
|message |string|Return message. For details, see [Appendix-Return codes](https://ads.tiktok.com/marketing_api/docs?id=1737172488964097).  |
| data |object | Returned data. |
#| list | object[] | Catalog list. |
##| catalog_id | string | Catalog ID. |
##| catalog_name | string | Catalog name. |
##| catalog_type | string | Catalog type.
Enum values: 
- `ECOM`: E-commerce catalog. 
-  `HOTEL`: hotel catalog.
- `FLIGHT`: flight catalog.
- `DESTINATION`:  destination catalog.
-  `ENTERTAINMENT`: entertainment catalog.
- `AUTO_VEHICLE`: Auto-Inventory catalog.
- `AUTO_MODEL`: Auto-Model catalog.
- `MINI_SERIES`: mini series catalog.|
##|ad_creation_eligible |string|Whether the catalog can be used in ads when it contains the number of available products required for the ad format.

Enum values:
- `NOT_AVAILABLE`: The catalog cannot be used in ads.
- `AVAILABLE`: The catalog can be used in ads when it contains the number of available products required for the ad format.|
##| create_time | string | Creation time. |
##| update_time | string | Update time. |
##|bc_info| object| Information about Business Center.|
###|bc_id|string|Business Center ID.|
###|bc_name|string| Business Center name.|
###|picture_url|string| URL of the profile image. An empty value is returned if the Business Center doesn't have a profile image.|
##|catalog_conf | object | Catalog configuration information. |
###|country|string|The region code of the primary targeting region.

To find out the corresponding region for a region code, refer to [Appendix - Location code](https://business-api.tiktok.com/portal/docs?id=1737585867307010).

Example: `US`.|
###|currency|string|Currency for the primary targeting region.

For supported currencies, see the **Code** column in [Budget verification ratio and precision of each currency](https://business-api.tiktok.com/portal/docs?id=1737585839634433#item-link-Budget%20verification%20ratio%20and%20precision%20of%20each%20currency).

Example: `USD`.|
###|channel|string|Channel for creating the catalog.

Enum values:
- `PARTNER`: Partners.
- `CLIENT`: Direct advertisers.|
###|additional_config_list|object[]|Returned only when `catalog_type` is `MINI_SERIES`.

Details of additional targeting regions.|
####|region_code|string|The region code of the additional targeting region.

To find out the corresponding region for a region code, refer to [Appendix - Location code](https://business-api.tiktok.com/portal/docs?id=1737585867307010).

Example: `GB`.|
####|currency|string|Currency for the additional targeting region.

For supported currencies, see the **Code** column in [Budget verification ratio and precision of each currency](https://business-api.tiktok.com/portal/docs?id=1737585839634433#item-link-Budget%20verification%20ratio%20and%20precision%20of%20each%20currency).

Example: `GBP`.|
#|page_info |object|Pagination information.|
##|page |number|Current page number.|
##|page_size |number|Page size.|
##|total_number |number|Total number of results.|
##|total_page |number|Total pages of results.|
| request_id | string | The log id of a request, which uniquely identifies the request. |
```

### Example

```xcodeblock
(code Success-Response http)
HTTPS/1.1 200 OK
{
    "message": "OK",
    "code": 0,
    "data": {
        "page_info": {
            "total_number": 14,
            "page": 1,
            "page_size": 14,
            "total_page": 1
        },
        "list": [
            {
                "update_time": "2021-07-23 10:34:36",
                "catalog_name": "test",
                "create_time": "2021-07-23 10:34:36",
                "bc_info": {
                    "bc_id": "{{bc_id}}",
                    "picture_url": "example URL",
                    "bc_name": "BC Demo"
                },
                "catalog_type": "ECOM",
                "catalog_id": "{{catalog_id}}",
				"ad_creation_eligible": "AVAILABLE",
                "catalog_conf": {
                    "currency": "USD",
                    "country": "US",
					"channel": "CLIENT"
                }
            },
            ...
        ]
    },
    "request_id": "{{request_id}}"
}
(/code);
```
