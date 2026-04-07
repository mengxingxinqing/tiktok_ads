# Get the product handling log

**Doc ID**: 1740570027173889
**Path**: API Reference/Catalog Products/Get the product handling log

---

Use this endpoint to check if the products are uploaded or deleted successfully, and what to do if the upload or deletion fails.

## Comparing v1.2 and v1.3
 ```xtable
 |Changes{20%}|v1.2{35%}|v1.3{35%}|
|---|---|---|
|Endpoint path| /v1.2/catalog/product/log/| /v1.3/catalog/product/log/|
|Request parameter data type |`bc_id`: number
`catalog_id`: number
`feed_log_id`: number|`bc_id`: string
`catalog_id`: string 
`feed_log_id`: string|
|Response parameter name|`status` 
`product_feeds_log`
`feeds_Log_data`
`error_effected_products`
- `effected_product_count` 
- `items_product_item_list`
- `id`
- `link`
- `suggest``warn_effected_products`
- `effected_product_count` 
- `items_product_item_list`
- `id`
- `link`
- `suggest` |`process_status`
`product_feed_log`
`feed_log_data`
`error_affected_products`
- `affected_product_count`
- `affected_product_item_list`
- `sku_id`
- `product_url`
- `suggestion``warn_affected_products`
- `affected_product_count`
- `affected_product_item_list`
- `sku_id`
- `product_url`
- `suggestion`|
|Response parameter data type|`catalog_id`: number|`catalog_id` : string|
|Response parameter name and data type|`feeds_id`: number|`feed_id` : string|
|New response parameters|/|
- `hotel_id`
- `name`
- `flight_id`
- `airline_company`
- `media_title_id`
- `vehicle_id`
- `make`
- `series_id`|
```

## Request

**Endpoint** 
https://business-api.tiktok.com/open_api/v1.3/catalog/product/log/

**Method** GET

**Header**

``` xtable
| Field {30%}| Type{15%} | Description{55%} |
|---|---|---|
|Access-Token {Required}|string|Authorized access token. For details, see [Authentication](https://ads.tiktok.com/marketing_api/docs?id=1738373164380162).|
```

**Parameters**

``` xtable
| Field {30%}| Type{15%} | Description{55%} |
|--- |--- |--- |
| bc_id {Required} | string | Business Center ID. |
| catalog_id {Required} | string | Catalog ID. |
| feed_log_id {Required} | string | Product handling ID. |
| language | string | Supported languages.
- `en`: English
- `zh-CN`: Chinese
- `ja-JP`: Japanese
- `de`: German
- `es`: Spanish
- `fr`: French
- `hi-IN`: Hindi (India)
- `id`: Indonesian
- `it`: Italian
- `ko`: Korean
- `ms`: Malay
-  `ru`: Russian
- `th`: Thai
- `tr`: Turkish
- `vi`: Vietnamese
Default value: `en`.|
```

### Example

```xcodeblock
(code curl http)

    curl -X GET -H "Access-Token:YOUR_ACCESS_TOKEN" \
    -H "Content-Type:application/json" \
    -d '{\"bc_id\": BC_ID,\"catalog_id\": CATALOG_ID,\"feed_log_id\": FEED_LOG_ID,\"language\": \"LANGUAGE\"}' \
    https://business-api.tiktok.com/open_api/v1.3/catalog/product/log/

(/code)
```

## Response

``` xtable
| Field {35%}| Type{15%} | Description{50%} |
|--- |--- |--- |
| code | number  |Return code, see [Appendix - Return code](https://ads.tiktok.com/marketing_api/docs?id=1737172488964097). |
|message |string|Return message, see [Appendix-Return message](https://ads.tiktok.com/marketing_api/docs?id=1737172488964097).  |
| request_id | string | The log id of a request, which uniquely identifies the request. |
| data |object| Returned data. |
#| product_feed_log | object | Product handling results. |
##| catalog_id | string | Catalog ID. |
##| feed_id|string|Feeds ID.|
##| add_count | number | Total number of new items. |
##| update_count | number | Total number of items modified. |
##| delete_count | number | Total number of items deleted. |
##| error_count | number | Number of errors.|
##| warn_count | number | Number of warnings.|
##| process_status | string | Processing status.

Enum values:
- `WAITING`: On hold and waiting for other tasks to complete. 
- `PROCESSING`: In progress. 
-  `SUCCESS`: Succeeded.
- `FAILED`: Failed. |
##| update_mode | number | Update mode.

Enum values:
- `INCREASE`: incremental.
- `REPLACE`: full replacement.|
##| start_time | string | Start time. |
##| end_time | string | End time. |
##| feed_log_data | object | Detailed processing information. |
###| download_path | object | File download address with all error/warning messages, key is language, value is file address. |
###| error_affected_products | object[] | Error message. |
####| affected_product_count | number | Number of products affected. |
####| affected_product_item_list | object[] | List of affected items, showing only the first five items. |
#####| index | number | Index that identifies the position of the product among the products you uploaded.
For example, an index of `2` represents the first product you uploaded through [/catalog/product/file/](https://business-api.tiktok.com/portal/docs?id=1740496787164161) or [/catalog/product/upload/](https://business-api.tiktok.com/portal/docs?id=1740497429681153). |
#####| title | string |Returned only for products in E-commerce catalogs, entertainment catalogs, Auto-Inventory catalogs, Auto-Model catalogs, or mini series catalogs.

The title of the E-commerce, entertainment, Auto-Inventory catalogs, or Auto-Model product, or the name of the short drama series.|
#####|sku_id|string| Returned only for products in E-commerce catalogs.

A unique ID for the product, such as a SKU.|
#####|hotel_id|string|Returned only for products in hotel catalogs.

 A unique ID for the hotel.|
#####|name|string|Returned only for products in hotel catalogs or destination catalogs.

The name of the hotel or the destination.|
#####|flight_id|string|Returned only for products in flight catalogs.

The unique ID specified for the flight.|
#####|airline_company|string|Returned only for products in flight catalogs.

The name of the airline company operating the flight.|
#####|media_title_id|string|Returned only for products in entertainment catalogs.

A unique ID for the media title item.|
#####| vehicle_id | string | Returned only for products in Auto-Inventory or Auto-Model catalogs.

A unique ID for the vehicle. |
#####| series_id | string | Returned only for products in mini series catalogs.

A unique self-defined ID for the short drama series.|
#####| make | string | Returned only for products in Auto-Inventory or Auto-Model catalogs.

 The make (brand) of the vehicle.|
#####| product_url | string | Product link. |
#####| description | string | Product description. |
#####| value | string | Field value. |
####| field | string | The field with issue. |
####| issue | string | Issue details. |
####| suggestion | string |Suggestions for solving the issue. |
###| warn_affected_products | object[] | Warning message. |
####| affected_product_count | number | Number of products affected. |
####| affected_product_item_list | object[] | List of affected items, showing only the first five items. |
#####| index | number | Index that identifies the position of the product among the products you uploaded.
For example, an index of `2` represents the first product you uploaded through [/catalog/product/file/](https://business-api.tiktok.com/portal/docs?id=1740496787164161) or [/catalog/product/upload/](https://business-api.tiktok.com/portal/docs?id=1740497429681153). |
#####| title | string |Returned only for products in E-commerce catalogs, entertainment catalogs, Auto-Inventory catalogs, Auto-Model catalogs, or mini series catalogs.

The title of the E-commerce, entertainment, Auto-Inventory catalogs, or Auto-Model product, or the name of the short drama series.|
#####|sku_id|string| Returned only for products in E-commerce catalogs.

A unique ID for the product, such as a SKU.|
#####|hotel_id|string|Returned only for products in hotel catalogs.

 A unique ID for the hotel.|
#####|name|string|Returned only for products in hotel catalogs or destination catalogs.

The name of the hotel or the destination.|
#####|flight_id|string|Returned only for products in flight catalogs.

The unique ID specified for the flight.|
#####|airline_company|string|Returned only for products in flight catalogs.

The name of the airline company operating the flight.|
#####|media_title_id|string|Returned only for products in entertainment catalogs.

A unique ID for the media title item.|
#####| description | string | Product description. |
#####| vehicle_id | string | Returned only for products in Auto-Inventory or Auto-Model catalogs.

A unique ID for the vehicle. |
#####| series_id | string | Returned only for products in mini series catalogs.

A unique self-defined ID for the short drama series.|
#####| make | string | Returned only for products in Auto-Inventory or Auto-Model catalogs.

 The make (brand) of the vehicle.|
#####| product_url | string | Product link. |
#####| value | string | Field value. |
####| field | string |  The field with issue. |
####| issue | string |  Issue details. |
####| suggestion | string | Suggestions for solving the issue. |
```

### Example

```xcodeblock
(code Success-Response http)
HTTPS/1.1 200 OK
{
"message": "OK",
"code": 0,
"data": {
    "product_feed_log": {
        "process_status": "SUCCESS",
        "update_mode": "INCREASE",
        "error_count": 0,
        "add_count": 0,
        "feeds_id": 2335,
        "warn_count": 1,
        "delete_count": 0,
        "feed_log_data": {
            "error_affected_products": null,
            "warn_affected_products": [
                {
                    "suggestion": "The \"age_group\" field is using an invalid value. Supported values only include: newborn/infant/toddler/kids/adult",
                    "issue": "Invalid value: age_group",
                    "field": "age_group",
                    "affected_product_count": 1,
                    "affected_product_item_list": [
                        {
                            "index": 3,
                            "sku_id": "tiktok_item_12424",
                            "description": "qgs test product description",
                            "title": "qgs test product",
                            "value": "None",
                            "product_url": "https://ads.tiktok.com"
                        }
                    ]
                },
                {
                    "suggestion": "The \"gender\" field is using an invalid value. Supported values only include: male/female/unisex",
                    "issue": "Invalid value: gender",
                    "field": "gender",
                    "affected_product_count": 1,
                    "affected_product_item_list": [
                        {
                            "index": 3,
                            "sku_id": "tiktok_item_12424",
                            "description": "qgs test product description",
                            "title": "qgs test product",
                            "value": "None",
                            "product_url": "https://ads.tiktok.com"
                        }
                    ]
                }
            ],
            "download_path": {
                "ru": "http://tosv.boei18n.byted.org/obj/dpafeed/6865965734837634822_73472_ru.csv",
                "fr": "http://tosv.boei18n.byted.org/obj/dpafeed/6865965734837634822_73472_fr.csv",
                "en": "http://tosv.boei18n.byted.org/obj/dpafeed/6865965734837634822_73472_en.csv",
                "ms": "http://tosv.boei18n.byted.org/obj/dpafeed/6865965734837634822_73472_ms.csv",
                "ko": "http://tosv.boei18n.byted.org/obj/dpafeed/6865965734837634822_73472_ko.csv",
                "vi": "http://tosv.boei18n.byted.org/obj/dpafeed/6865965734837634822_73472_vi.csv",
                "de": "http://tosv.boei18n.byted.org/obj/dpafeed/6865965734837634822_73472_de.csv",
                "tr": "http://tosv.boei18n.byted.org/obj/dpafeed/6865965734837634822_73472_tr.csv",
                "it": "http://tosv.boei18n.byted.org/obj/dpafeed/6865965734837634822_73472_it.csv",
                "zh-CN": "http://tosv.boei18n.byted.org/obj/dpafeed/6865965734837634822_73472_zh-CN.csv",
                "hi-IN": "http://tosv.boei18n.byted.org/obj/dpafeed/6865965734837634822_73472_hi-IN.csv",
                "th": "http://tosv.boei18n.byted.org/obj/dpafeed/6865965734837634822_73472_th.csv",
                "ja-JP": "http://tosv.boei18n.byted.org/obj/dpafeed/6865965734837634822_73472_ja-JP.csv",
                "id": "http://tosv.boei18n.byted.org/obj/dpafeed/6865965734837634822_73472_id.csv",
                "es": "http://tosv.boei18n.byted.org/obj/dpafeed/6865965734837634822_73472_es.csv"
            }
        },
        "catalog_id": 6865965734837634822,
        "update_count": 2,
        "start_time": "2020-09-14 05:15:09",
        "end_time": "2020-09-14 05:15:09"
    }
},
"request_id": "2020091406394701023125321410044"
}
(/code);
```
