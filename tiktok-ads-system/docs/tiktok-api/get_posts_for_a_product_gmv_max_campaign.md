# Get posts for a Product GMV Max Campaign

**Doc ID**: 1822001168512129
**Path**: API Reference/GMV Max/Get posts for a Product GMV Max Campaign

---

Use this endpoint to retrieve the list of TikTok posts that are available for a Product GMV Max campaign using a specific TikTok Shop.

## Request

**Endpoint** https://business-api.tiktok.com/open_api/v1.3/gmv_max/video/get/

**Method** GET

**Header**

```xtable
|Field{36%}|Data Type{12%}|Description{52%}|
|---|---|---|
|Access-Token {Required}|string|Authorized access token. 
For details, see [Authentication](https://business-api.tiktok.com/portal/docs?id=1738373164380162).|
```

**Parameters**

``` xtable
|Field{36%}|Data Type{12%}|Description{52%}|
|--- |--- |--- |
| advertiser_id {Required} | string | Advertiser ID. |
| store_id {Required} | string | The ID of the TikTok Shop.

 To obtain a TikTok Shop that is available for GMV Max Campaigns, use [/gmv_max/store/list/](https://business-api.tiktok.com/portal/docs?id=1822001044479041) and confirm that the returned `is_gmv_max_available` is `true`. |
| store_authorized_bc_id {Required} | string | ID of the Business Center that is authorized to access the TikTok Shop (`store_id`). |
| spu_id_list  | string[] | A list of Product SPU (standard product unit) IDs to filter the results by.

 
- If you want to promote all products from the TikTok Shop in the Product GMV Max Campaign using authorized posts, you don't need to pass `spu_id_list` and `custom_posts_eligible`.
- If you want to promote specific products from the TikTok Shop in the Product GMV Max Campaign using authorized posts, specify these products via `spu_id_list` and do not specify `custom_posts_eligible`.
- If you want to promote a specific product from the TikTok Shop in the Product GMV Max Campaign using customized posts, specify the product via `spu_id_list` and set `custom_posts_eligible` to `true`.
Max size:
- When `custom_posts_eligible` is `false` or not specified: 50.
- When `custom_posts_eligible` is `true`: 1.
To obtain the list of SPU IDs for products within a TikTok Shop, use [/store/product/get/](https://business-api.tiktok.com/portal/docs?id=1793482248880130). Set `ad_creation_eligible` to `GMV_MAX` and select `item_group_id` values where `status` is `AVAILABLE` and `gmv_max_ads_status` is `UNOCCUPIED`. |
| custom_posts_eligible | boolean | Whether to query videos that can be used in customized posts promoting a specific product.

If you set this field to `true`, you need to specify one product using `spu_id_list` simultaneously.

Supported values:`true`,`false`.
Default value: `false`. |
| sort_field | string | Valid only when `custom_posts_eligible` is `false` or not provided.

The sorting field for videos available for authorized posts.

Enum values:
- `GMV`: GMV.
- `POST_TIME`: Post time.
- `VIDEO_VIEWS`: Video views.
- `VIDEO_LIKES`: Video likes.
- `CLICK_THROUGH_RATE`: Click-through Rate (CTR).
- `PRODUCT_CLICKS`: Product clicks.Default value: `GMV`. |
| sort_type | string | The sorting order for videos available for authorized posts or customized posts.

Enum values:
- `ASC`: ascending.
- `DESC`: descending.Default value: `DESC`.

- If `custom_posts_eligible` is `false` or not specified, you can sort the videos available for authorized posts by specifying both `sort_field` and `sort_type`.
- If `custom_posts_eligible` is `true`, you don't need to specify `sort_field`. In this case, videos available for customized posts are sorted by default in descending order of post time, with the latest posts appearing first. If you prefer to sort posts in ascending order (earliest posts first), set `sort_type` to `ASC`. 
|
| keyword | string | A search keyword to filter posts (videos).

You can specify a post ID or caption.
- To search by post caption (`text`), provide a text string. This search type supports multiple-language searches and fuzzy matches.
Example: `summer`.
-  To search by post ID (`item_id`), provide a numeric string with at least 19 characters. This search type supports exact matches.
Example: `1234567891234567891`. |
| need_auth_code_video| boolean| Whether to include posts associated with `AUTH_CODE` identities in the results.

 Supported values: `true`, `false`.
Default value: `false`.

**Note**: If `need_auth_code_video` is `false` or not passed and `identity_list` is not specified, you will retrieve an empty post list. |
| identity_list  | object[] | A list of `TT_USER`, `BC_AUTH_TT`, or `TTS_TT` identities to filter the results by.

To obtain a list of identities available for Product GMV Max Campaigns, use [/gmv_max/identity/get/](https://business-api.tiktok.com/portal/docs?id=1822001101474882) and select identities with `product_gmv_max_available` as `true`.

Max size: 20.

**Note**: If `need_auth_code_video` is `false` or not passed and `identity_list` is not specified, you will retrieve an empty post list. |
#| identity_id  | string | Identity ID. |
#| identity_type  | string |  Identity type. 

Enum values: 
- `TT_USER`: TikTok User. This type of identity is created when you bind your TikTok For Business account with your TikTok Business Account, or when you bind your TikTok For Business account with your regular TikTok account and then upgrade the account to Business Account.
- `BC_AUTH_TT`: TikTok Account User in Business Center. This type of identity is created when you add a TikTok account to your Business Center, and the TikTok account owner approves your request. 
- `TTS_TT`: TikTok Account User for TikTok Shop. This type of identity is created when you set an official TikTok account for the TikTok Shop. |
#| identity_authorized_bc_id {+Conditional} | string | Required when `identity_type` is `BC_AUTH_TT`. 

 The ID of the Business Center that a TikTok Account User in Business Center identity is associated with. |
#| identity_authorized_shop_id {+Conditional} | string | Required only when `dentity_type` is `BC_AUTH_TT` and `identity_authorized_shop_id` is returned for the identity from [/gmv_max/identity/get/](https://business-api.tiktok.com/portal/docs?id=1822001101474882). 

 The ID of the TikTok Shop that a TikTok Account User in Business Center identity is associated with. |
#| store_id {+Conditional} | string | Required when `identity_type` is `TTS_TT`. 

The ID of the TikTok Shop that a TikTok Account User for TikTok Shop identity is associated with. |
| page | number | Current page number.

 Value range: ≥ 1. 
Default value: 1. |
| page_size | number | Page size.

 Value range: 1-50.
Default value:10. |
```

### Example
```xcodeblock
(code curl http)
curl --location --request GET 'https://business-api.tiktok.com/open_api/v1.3/gmv_max/video/get/?advertiser_id={{advertiser_id}}&store_id={{store_id}}&store_authorized_bc_id={{store_authorized_bc_id}}&need_auth_code_video=true&identity_list=[{ "identity_type": "BC_AUTH_TT","identity_id": "{{identity_id}}","identity_authorized_bc_id": "{{identity_authorized_bc_id}}"}]&page=1&page_size=50' \
--header 'Access-Token: {{Access-Token}}'
(/code)
```
## Response

``` xtable
|Field{36%}|Data Type{12%}|Description{52%}|
|---|---|---|
|code |number|Response code. For the complete list of response codes and descriptions, see [Appendix-Return Code](https://ads.tiktok.com/marketing_api/docs?id=1737172488964097). |
|message|string|Response message. For details, see [Appendix - Return Codes](https://ads.tiktok.com/marketing_api/docs?id=1737172488964097).|
|request_id |string|The log ID of a request, which uniquely identifies the request.  |
|data |object|Returned data.

**Note**: If this field is an empty list, follow these steps to authorize posts with product links to the ad account:
1. Authorize posts to the ad account using [/tt_video/authorize/](https://business-api.tiktok.com/portal/docs?id=1738376435339265).
2. Check whether the posts contain product information (`spu_id`, `spu_name`, and `store_id`) using [/tt_video/info/](https://business-api.tiktok.com/portal/docs?id=1738376324021250) or [/tt_video/list/](https://business-api.tiktok.com/portal/docs?id=1738376465972226).|
#| item_list| object[] | A list of TikTok videos (posts) available for Product GMV Max campaigns using the specified TikTok Shop. |
##| item_id | string | The ID of the TikTok post. |
##| text | string | The caption of the TikTok post. |
##| spu_id_list| string[] | The list of Product SPU IDs that the TikTok post is associated with.

**Note**: This field is not included in the response for videos with no product anchor link. |
##| can_change_anchor | boolean | Whether you can change the product anchor link in this video.

Supported values:
- `true`: You can add a product anchor link to create a customized post.
- `false`: You cannot use the video to create a customized post.
**Note**: If `can_change_anchor` is `false`, you cannot pass the video to `custom_anchor_video_list` or `item_list` in [/campaign/gmv_max/create/](https://business-api.tiktok.com/portal/docs?id=1822000988713089) or [/campaign/gmv_max/update/](https://business-api.tiktok.com/portal/docs?id=1822001009002497) to create customized posts. |
##| identity_info | object | Information about the identity associated with the TikTok post. |
###| identity_id | string | Identity ID. |
###| identity_type | string | Identity type. 

Enum values: 
- `AUTH_CODE`: Authorized User. This type of identity is created when you use the authorization code to access a TikTok account or a TikTok post.
- `TT_USER`: TikTok User. This type of identity is created when you bind your TikTok For Business account with your TikTok Business Account, or when you bind your TikTok For Business account with your regular TikTok account and then upgrade the account to Business Account.
- `BC_AUTH_TT`: TikTok Account User in Business Center. This type of identity is created when you add a TikTok account to your Business Center, and the TikTok account owner approves your request. 
- `TTS_TT`: TikTok Account User for TikTok Shop. This type of identity is created when you set an official TikTok account for the TikTok Shop. |
###| identity_authorized_bc_id | string | Returned only when `identity_type` is `BC_AUTH_TT`. 

The ID of the Business Center that a TikTok Account User in Business Center identity is associated with. |
###| identity_authorized_shop_id | string | Returned for some `BC_AUTH_TT` identities. 

The ID of the TikTok Shop that the TikTok Account User in Business Center identity is associated with. |
###| store_id | string | Returned only when `identity_type` is `TTS_TT`. 

The ID of the TikTok Shop that a TikTok Account User for TikTok Shop identity is associated with. |
###| profile_image | string | Temporary profile image URL for the TikTok account that is associated with the identity. 

Validity period: around 48 hours. The expiration time is included in the URL after the `x-expires` parameter, in the format of an Epoch/Unix timestamp in seconds.

Once the URL expires, you need to call [/gmv_max/video/get/](https://business-api.tiktok.com/portal/docs?id=1822001168512129) to obtain a new URL. |
###| display_name| string | The display name of the TikTok account that is associated with the identity. |
##| video_info | object | Details of the video in the post. |
###| video_id | string | The ID of the video. |
###| video_cover_url | string | Temporary URL for the video cover.

Validity period: around 24 hours. The expiration time is included in the URL after the `x-expires` parameter, in the format of an Epoch/Unix timestamp in seconds. 

Once the URL expires, you need to call [/gmv_max/video/get/](https://business-api.tiktok.com/portal/docs?id=1822001168512129) to obtain a new URL. |
###| preview_url | string | Temporary preview URL for the video. 

Validity period: six hours.

Once the URL expires, you need to call [/gmv_max/video/get/](https://business-api.tiktok.com/portal/docs?id=1822001168512129) to obtain a new URL. |
###| height | number | The height of the video in pixels. 

 Example: 1920. |
###| width | number | The width of the video in pixels.

Example: 1080. |
###| bit_rate | number | The bit rate of the video in bps. 

Example: 8500323. |
###| duration | number | The duration of the video in seconds. 

Example: 3.669. |
###| size | number | The size of the video in bytes. 

Example: 3898461. |
###| signature | string | The MD5 of the video. 

Example: `ab1cd2345e678fghi91jkl23b456m7no`. |
###| format | string | The format of the video.

Example: `mp4`. |
###| definition | string | The definition of the video.

 Example: `1080p`. |
###| fps | number | The frames per second (FPS) of the video. 

Example: 27. |
#| page_info | object | Pagination information. |
##| page | number | Current page number. |
##| page_size | number | Page size. |
##| total_number | number | Total number of results. |
##| total_page | number | Total pages of results. |
```

### Example
```xcodeblock
(code Success-Response http)
HTTPS/1.1 200 OK
{
    "code": 0,
    "message": "OK",
    "request_id": "{{request_id}}",
    "data": {
        "item_list": [
            {
                "identity_info": {
                    "display_name": "{{display_name}}",
                    "identity_id": "{{identity_id}}",
                    "identity_type": "AUTH_CODE",
                    "profile_image": "{{profile_image}}"
                },
                "item_id": "{{item_id}}",
                "spu_id_list": [
                    "{{spu_id}}"
                ],
                "text": "{{text}}",
                "video_info": {
                    "bit_rate": 8500323,
                    "definition": "1080p",
                    "duration": 3.669,
                    "format": "mp4",
                    "fps": 30,
                    "height": 1920,
                    "preview_url": "{{preview_url}}",
                    "signature": "{{signature}}",
                    "size": 3898461,
                    "video_cover_url": "{{video_cover_url}}",
                    "video_id": "{{video_id}}",
                    "width": 1080
                }
            },
            {
                "identity_info": {
                    "display_name": "{{display_name}}",
                    "identity_id": "{{identity_id}}",
                    "identity_type": "AUTH_CODE",
                    "profile_image": "{{profile_image}}"
                },
                "item_id": "{{item_id}}",
                "spu_id_list": [
                    "{{spu_id}}"
                ],
                "text": "{{text}}",
                "video_info": {
                    "bit_rate": 109400,
                    "definition": "540p",
                    "duration": 5.256,
                    "format": "mp4",
                    "fps": 27,
                    "height": 1024,
                    "preview_url": "{{preview_url}}",
                    "signature": "{{signature}}",
                    "size": 71876,
                    "video_cover_url": "{{video_cover_url}}",
                    "video_id": "{{video_id}}",
                    "width": 576
                }
            },
            {
                "identity_info": {
                    "display_name": "{{display_name}}",
                    "identity_authorized_bc_id": "{{identity_authorized_bc_id}}",
                    "identity_id": "{{identity_id}}",
                    "identity_type": "BC_AUTH_TT",
                    "profile_image": "{{profile_image}}"
                },
                "item_id": "{{item_id}}",
                "spu_id_list": [
                    "{{spu_id}}"
                ],
                "text": "{{text}}",
                "video_info": {
                    "bit_rate": 164638,
                    "definition": "540p",
                    "duration": 5,
                    "format": "mp4",
                    "fps": 30,
                    "height": 1024,
                    "preview_url": "{{preview_url}}",
                    "signature": "{{signature}}",
                    "size": 107982,
                    "video_cover_url": "{{video_cover_url}}",
                    "video_id": "{{video_id}}",
                    "width": 576
                }
            }
        ],
        "page_info": {
            "page": 1,
            "page_size": 50,
            "total_number": 3,
            "total_page": 1
        }
    }
}
(/code)
```
