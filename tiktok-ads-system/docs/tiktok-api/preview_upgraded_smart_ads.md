# Preview Upgraded Smart+ Ads

**Doc ID**: 1843317445798914
**Path**: API Reference/Upgraded Smart+/Ads/Preview Upgraded Smart+ Ads

---

Use this endpoint to preview an Upgraded Smart+ Ad that you want to create or an existing Upgraded Smart+ Ad.

## Request
**Endpoint** https://business-api.tiktok.com/open_api/v1.3/smart_plus/ad/preview/

**Method** POST

**Header**

```xtable
|Field{30%}|Data Type{15%}|Description{55%}|
|---|---|---|
|Access-Token {Required}|string|Authorized access token. For details, see [Authentication](https://business-api.tiktok.com/portal/docs?id=1738373164380162).|
|Content-Type {Required}|string|Request content type.
 Allowed Value: `application/json`.|
```

**Parameters**

### Preview ads that you plan to create
This allows you to preview your ad before creating it.

```xtable
|Field{30%}|Data Type{15%}|Description{55%}|
|---|---|---|
|advertiser_id {Required}|string|Advertiser ID.|
|preview_type {Required}|string|Preview type.

Enum value: 
- `ADS_CREATION`: Preview an ad by ad creation parameters.|
|catalog_enabled|boolean|Whether to use catalog in the campaign.

Supported values: `true`, `false`.|
|catalog_id {+Conditional}|string|Required when `catalog_enabled` is `true`.

The ID of the catalog to use in the ad group.

To retrieve the catalogs within your Business Center, use [/catalog/get/](https://business-api.tiktok.com/portal/docs?id=1740315452868610).|
|catalog_authorized_bc_id {+Conditional}|string|Required when `catalog_enabled` is `true`.

The ID of the Business Center that the catalog (`catalog_id`) belongs to.|
|creative_list {Required}|object[]|A list of creatives.

Size range: 1- 31.|
#|creative_info {Required}|object|Creative information.|
##|video_info {+Conditional}|object|Required for the following types of ads:
- Non-Spark Ads Single Video ads. 
- Spark Ads Single Video ads through Spark Ads Push.
Video information.|
###|video_id {+Conditional}|string|Required when `video_info` is specified.

Video ID.

To upload a video and obtain the video ID, use [/file/video/ad/upload/](https://business-api.tiktok.com/portal/docs?id=1737587322856449).
To search for videos within your ad account, use [/file/video/ad/search/](https://business-api.tiktok.com/portal/docs?id=1740050472224769).|
##|image_info {+Conditional}|object[]|
- Required for the following types of ads:Non-Spark Ads Single Video ads. You need to specify a video cover.
- Spark Ads Single Video ads through Spark Ads Push. You need to specify a video cover.
- Non-Spark Ads Standard Carousel ads. You need to specify one to 35 carousel images.
- Spark Ads Standard Carousel ads through Spark Ads Push. You need to specify one to 35 carousel images.
- Not supported for Catalog Carousel ads.
Image information.|
###|web_uri {+Conditional}|string|Required when `image_info` is specified.

Image ID.

To upload an image and obtain the image ID, use [/file/image/ad/upload/](https://business-api.tiktok.com/portal/docs?id=1739067433456642).
To search for images within your ad account, use [/file/image/ad/search/](https://business-api.tiktok.com/portal/docs?id=1740052016789506).|
##|music_info {+Conditional}|object|
- Required for the following scenarios:When you create Standard Carousel Ads, including:Non-Spark Ads Standard Carousel ads
- Spark Ads Standard Carousel ads through Spark Ads Push
- Spark Ads Standard Carousel ads through Spark Ads Pull
- When `objective_type` is `WEB_CONVERSIONS` and `catalog_creative_toggle` is `true`. The system will automatically generate Catalog Carousel ads.Music information.|
###|music_id {+Conditional}|string|Required when `music_info` is specified.

The ID of the piece of music to use in the carousel ads.|
##|tiktok_item_id {+Conditional}|string|
- Required when you create Spark Ads through Spark Ads Pull, including:Spark Ads Single Video ads through Spark Ads Pull. You need to specify a TikTok video post.
- Spark Ads Standard Carousel ads through Spark Ads Pull. You need to specify a TikTok photo post.
- Not supported when `catalog_creative_toggle` is `true`.
The ID of the TikTok post to be used as an ad (Spark Ads).

Pass in the `item_id` you get from the response of the [/tt_video/info/](https://business-api.tiktok.com/portal/docs?id=1738376324021250) and [/identity/video/get/](https://business-api.tiktok.com/portal/docs?id=1740218475032577) endpoints.

When you pass in `tiktok_item_id`, you don't need to pass in the objects `image_info`, `video_info`, and `title_list`.

**Note**: By using Spark Ads, you confirm that you have the rights to use the music in the videos for commercial purposes.|
##|identity_type {+Conditional}|string|Required when you create Spark Ads without using catalog creatives.

Identity type.

Enum values: `AUTH_CODE`, `TT_USER`, `BC_AUTH_TT`.

For details about identities, see [Identities](https://business-api.tiktok.com/portal/docs?id=1738958351620097).

**Note**: 
- If you want to create Spark Ads using catalog creatives from an E-commerce catalog, specify the `identity_type` and `identity_id` within `ad_configuration`.
- If this field is set to `TT_USER`, `BC_AUTH_TT`, or `AUTH_CODE` and the following conditions are both met, you need to specify a dynamic CTA via `call_to_action_id`.At the campaign level, `objective_type` is `APP_PROMOTION` or `WEB_CONVERSIONS`.
- At the ad group level, `placement_type` is `PLACEMENT_TYPE_NORMAL` and `placements` includes `PLACEMENT_TIKTOK`, or `placement_type` is `PLACEMENT_TYPE_AUTOMATIC`.|
##|identity_id {+Conditional}|string|Required when you create Spark Ads without using catalog creatives.

Identity ID.

**Note**: If you want to create Spark Ads using catalog creatives from an E-commerce catalog, specify the `identity_type` and `identity_id` within `ad_configuration`.
|
##|identity_authorized_bc_id {+Conditional}|string|Required when `identity_type` within `creative_info` is `BC_AUTH_TT`.

ID of the Business Center that a TikTok Account User in Business Center identity is associated with.|
|ad_text_list {+Conditional}|object[]|Required when `tiktok_item_id` is not specified.

List of ad texts.
Ad texts are shown to your audience as part of your ad creatives, to deliver the message you intend to communicate to them.

Max size: 5.|
#|ad_text {+Conditional}|string|Required when `ad_text_list` is specified.

Ad text.|
|call_to_action_list|object[]|Call-to-action list.

Max size: 3.

**Note**:
- This field is not supported for Upgraded Smart+ Lead Generation Campaigns.
- The preview link will only display the first call-to-action in this list.|
#|call_to_action {+Conditional}|object|Required when `call_to_action_list` is specified.

Call-to-action text.

For enum values, see [Enumeration - Call-to-action](https://business-api.tiktok.com/portal/docs?id=1737174886619138#item-link-Call-to-action).|
|ad_configuration|object|Additional configurations.|
#|identity_type {+Conditional}|string|Required in any of the following scenarios:
- You are creating non-Spark Ads on non-TikTok placements. Non-Spark Ads on the TikTok placement are no longer supported.
- You are creating Spark Ads using catalog creatives from an E-commerce catalog. Learn more about how you can create such ads in [Create Upgraded Smart+ E-commerce Catalog Ads](https://business-api.tiktok.com/portal/docs?id=1847302895272962).
Identity type.
- Enum values for non-Spark Ads on non-TikTok placements: `CUSTOMIZED_USER`.
- Enum values for Upgraded Smart+ E-commerce Catalog Spark Ads (with `catalog_creative_toggle` as `true`): `TT_USER`, `BC_AUTH_TT`.
For details about identities, see [Identities](https://business-api.tiktok.com/portal/docs?id=1738958351620097).|
#|identity_id {+Conditional}|string|Required in any of the following scenarios:
- You are creating non-Spark Ads on non-TikTok placements. Non-Spark Ads on the TikTok placement are no longer supported.
- You are creating Spark Ads using catalog creatives from an E-commerce catalog. Learn more about how you can create such ads in [Create Upgraded Smart+ E-commerce Catalog Ads](https://business-api.tiktok.com/portal/docs?id=1847302895272962).
Identity ID.|
#|identity_authorized_bc_id {+Conditional}|string|Required when `identity_type` within `ad_configuration` is `BC_AUTH_TT`.

ID of the Business Center that a TikTok Account User in Business Center identity is associated with.|
#|product_specific_type {+Conditional}|string|Required when `catalog_enabled` is `true` at the campaign level.

Different dimensions to choose products.

Enum values:
- `ALL`: Allow TikTok to dynamically choose from all products.
- `PRODUCT_SET`: Specify a product set. TikTok will dynamically choose products from this set.
- `CUSTOMIZED_PRODUCTS`: Specify a customized number of products.

-  If this field is set to `ALL`, you don't need to input `product_set_id` and `product_ids`.
-  If this field is set to `PRODUCT_SET`, you need to pass in `product_set_id`.
-  If this field is set to `CUSTOMIZED_PRODUCTS`, `product_ids` is required.|
#|product_set_id {+Conditional}|string|Required when `product_specific_type` is `PRODUCT_SET`.

The ID of a product set.

- To retrieve the product sets within your ad account, use [/catalog/set/get/](https://business-api.tiktok.com/portal/docs?id=1740570556295169).
-  To create a product set, use [/catalog/set/create/](https://business-api.tiktok.com/portal/docs?id=1740572891104257).|
#|product_ids {+Conditional}|string[]|Required when `product_specific_type` is `CUSTOMIZED_PRODUCTS`.

The product IDs of the catalog products.

Max size: 20.

To retrieve the product ID (`product_id`) of each catalog product, use [/catalog/product/get/](https://business-api.tiktok.com/portal/docs?id=1740564136678402).|
#|catalog_creative_toggle|boolean|Valid only when `catalog_enabled` is `true`.

Whether to enable auto-selection of creatives from your catalog.

Supported values: `true`, `false`.
Default value: `false`.

If you set this field to `true`, you need to provide a `creative_info` with only `music_info` in it to specify the music to be used in Catalog Carousel.|
#|catalog_creative_info|object|Valid only when the following conditions are met:
- The ad is an [Upgraded Smart+ E-commerce Catalog Ad](https://business-api.tiktok.com/portal/docs?id=1847302895272962).
- `catalog_creative_toggle` is `true`.
Additional settings for catalog creatives to use in your ads.|
##|catalog_media_settings|string[]|The types of creatives from your E-commerce catalog to use in the ad.

Enum values:
- `VIDEO`: Video.
- `IMAGE`: Image.
- `TEMPLATE_VIDEO`: Video templates. If you include this value in `catalog_media_settings`, you can optionally specify `catalog_template_video_id` at the same time.If `catalog_template_video_id` is not specified, all video templates and video URLs from your catalog will be used to generate the ad.
- If `catalog_template_video_id` is specified, the selected video template will be used to generate the ad.|
##|catalog_template_video_id|string|Valid only when `TEMPLATE_VIDEO` is included in `catalog_media_settings`.

The ID of a video template in your catalog to use in the ad.

To obtain the IDs of video templates (video packages) in your catalog, use [/catalog/video_package/get/](https://business-api.tiktok.com/portal/docs?id=1740574099715073).
To learn about how to create video packages on TikTok Ads Manager, see [How to create video packages in a Catalog](https://ads.tiktok.com/help/article/how-to-create-video-packages-in-a-catalog).|
```

#### Example
```xcodeblock
(code curl http)
curl --location --request POST 'https://business-api.tiktok.com/open_api/v1.3/smart_plus/ad/preview/' \
--header 'Access-Token: "{{Access-Token}}"' \
--header 'Content-Type: application/json' \
--data '{
    "advertiser_id": "{{advertiser_id}}",
    "preview_type": "ADS_CREATION",
    "catalog_enabled": true,
    "catalog_id": "{{catalog_id}}",
    "catalog_authorized_bc_id": "{{catalog_authorized_bc_id}}",
    "creative_list": [
        {
            "creative_info": {
                "video_info": {
                    "video_id": "{{video_id}}"
                }
            },
            "image_info": [
                {
                    "web_uri": "{{web_uri}}"
                }
            ]
        },
        {
            "creative_info": {
                "tiktok_item_id": "{{tiktok_item_id}}",
                "identity_id": "{{identity_id}}",
                "identity_type": "BC_AUTH_TT",
                "identity_bc_id": "{{identity_bc_id}}"
            }
        },
        {
            "creative_info": {
                "image_info": [
                    {
                        "web_uri": "{{web_uri}}"
                    },
                    {
                        "web_uri": "{{web_uri}}"
                    }
                ],
                "music_info": {
                    "music_id": "{{music_id}}"
                }
            }
        },
        {
            "creative_info": {
                "music_info": {
                    "music_id": "{{music_id}}"
                }
            }
        }
    ],
    "ad_text_list": [
        {
            "ad_text": "{{ad_text}}"
        },
        {
            "ad_text": "{{ad_text}}"
        }
    ],
    "call_to_action_list": [
        {
            "call_to_action": "APPLY_NOW"
        },
        {
            "call_to_action": "DOWNLOAD_NOW"
        }
    ],
    "ad_configuration": {
        "product_specific_type": "ALL",
        "catalog_creative_toggle": true
    }
}'
(/code)
```

### Preview existing ads

```xtable
|Field{30%}|Data Type{15%}|Description{55%}|
|---|---|---|
|advertiser_id {Required}|string|Advertiser ID.|
|preview_type {Required}|string|Preview type.

Enum value:
- `AD`: preview an existing ad.|
|smart_plus_ad_id {Required}|string|ID of the Upgraded Smart+ Ad that you want to preview.

To obtain a list of Upgraded Smart+ Ad IDs, use [/smart_plus/ad/get/](https://business-api.tiktok.com/portal/docs?id=1843317378982914).|
```

#### Example
```xcodeblock
(code curl http)
curl --location --request POST 'https://business-api.tiktok.com/open_api/v1.3/smart_plus/ad/preview/' \
--header 'Access-Token: "{{Access-Token}}"' \
--header 'Content-Type: application/json' \
--data '{
    "advertiser_id": "{{advertiser_id}}",
    "preview_type": "AD",
    "smart_plus_ad_id": "{{smart_plus_ad_id}}"
}'
(/code)
```

## Response

```xtable
|Field{30%}|Data Type{15%}|Description{55%}|
|---|---|---|
|code|number|Response code. For the complete list of response codes and descriptions, see [Appendix - Return Codes](https://business-api.tiktok.com/portal/docs?id=1737172488964097).|
|message|string|Response message. For details, see [Appendix - Return Codes](https://business-api.tiktok.com/portal/docs?id=1737172488964097).|
|request_id|string|The log ID of a request, which uniquely identifies the request.|
|data|object|Returned data.|
#|preview_link|string|Preview link.

Validity period: 30 days.|
#|iframe|string|The iframe code snippet with the preview link. You can embed the iframe code into your HTML file.|
```

### Example
```xcodeblock
(code Success-Response http)
{
    "code": 0,
    "message": "OK",
    "request_id": "{{request_id}}",
    "data": {
        "iframe": "",
        "preview_link": "{{preview_link}}"
    }
}
(/code)
```
