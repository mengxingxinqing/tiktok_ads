# Get the review info of Upgraded Smart+ Ads

**Doc ID**: 1843317465695233
**Path**: API Reference/Upgraded Smart+/Ad Review/Get the review info of Upgraded Smart+ Ads

---

Use this endpoint to retrieve the review results of Upgraded Smart+ Ads, including creatives within the ads.

An ad needs to be approved before it can be delivered, and it may get rejected due to various reasons, such as incorrect placement or targeting selections. Based on the rejection reasons and suggestions you get, you can modify your ad accordingly using [/smart_plus/ad/update/](https://business-api.tiktok.com/portal/docs?id=1843317411665921).

## Request
**Endpoint** https://business-api.tiktok.com/open_api/v1.3/smart_plus/ad/review_info/

**Method** GET

**Header**

```xtable
|Field{30%}|Data Type{15%}|Description{55%}|
|---|---|---|
|Access-Token {Required}|string|Authorized access token. For details, see [Authentication](https://business-api.tiktok.com/portal/docs?id=1738373164380162).|
```

**Parameters**

```xtable
|Field{30%}|Data Type{15%}|Description{55%}|
|---|---|---|
|advertiser_id {Required}|string|Advertiser ID.|
|smart_plus_ad_ids {Required}|string[]|A list of Ad IDs.

Max size: 100.

To obtain ad IDs, use [/smart_plus/ad/get/](https://business-api.tiktok.com/portal/docs?id=1843317378982914).|
|lang|string|The code of the language for the returned `reasons`,`suggestion`, and `specification` within the `reject_info` object array.

For enum values, see [List of values for `lang`](#item-link-List of values for lang).

Default value: `en`.|
|extra_info_setting|object|Additional settings.|
#|include_reject_info|boolean|Whether to include the reason for rejection.

Supported values: `true`, `false`.

Default value: `false`.|
#|include_violation_frame|boolean|Whether to include the video frames @that have been flagged for violations.

Supported values: `true`, `false`.

Default value: `false`.

**Note**: You can only set this field to `true` when `include_reject_info` is `true`.|
```

### List of values for `lang`
The following table outlines the enum values for `lang`.

```xtable
|Language code (`lang`){30%}|Language{70%}|
|---|---|
|`ar`|Arabic|
|`cs-CZ`|Czech|
|`de`|German|
|`en`|English|
|`es`|Spanish|
|`fr`|French|
|`id`|Indonesian|
|`it`|Italian|
|`ja`|Japanese|
|`ko`|Korean|
|`ms`|Malay|
|`pl-PL`|Polish|
|`pt-BR`|Portuguese (Brazil)|
|`ru`|Russian|
|`sv-SE`|Swedish|
|`th`|Thai|
|`tr`|Turkish|
|`vi`|Vietnamese|
|`zh`|Simplified Chinese|
```

### Example
```xcodeblock
(code curl http)
curl --location  --request GET 'https://business-api.tiktok.com/open_api/v1.3/smart_plus/ad/review_info/?advertiser_id={{advertiser_id}}&smart_plus_ad_ids=["{{smart_plus_ad_ids}}"]&extra_info_setting={"include_reject_info": true, "include_violation_frame": true}' \
--header 'Access-Token: {{Access-Token}}'
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
#|smart_plus_ad_review_infos|object[]|Information about the review result for the ads.|
##|smart_plus_ad_id|string|Ad ID.|
##|review_status|string|The review status of the ad.

Enum values:
- `ALL_AVAILABLE`: The ad has been reviewed and can be delivered to all specified targeting countries.
- `PART_AVAILABLE`: The ad has been reviewed and can only be delivered to some of the specified targeting countries.
- `UNAVAILABLE`: The ad has been reviewed and cannot be delivered.|
##|passed_locations|string[]|The targeted regions that passed the review.

For enum values, see [Appendix - Location codes](https://business-api.tiktok.com/portal/docs?id=1737585867307010).|
##|appeal_status|string|The appeal status of the ad.

Enum values:
- `NOT_APPEALED`: The appeal is not submitted.
- `APPEALING`: The appeal is being processed.
- `APPEAL_SUCCESSFUL`: The appeal has succeeded.
- `APPEAL_FAILED`: The appeal failed.
- `APPEAL_DONE`: The appeal went through an additional review. To confirm whether the appeal succeeded or failed, check the `review_status` value.|
##|appeal_reject_reasons|string[]|The reasons for rejecting the appeal.|
##|reject_info|object[]|Details of the rejection.|
###|reasons|string[]|The reasons for failing the ad review.|
###|suggestion|string|The review suggestion.|
###|forbidden_ages|string[]|The age groups that failed the review.

For enum values, see [Enumeration - Age Group](https://business-api.tiktok.com/portal/docs?id=1737174886619138#item-link-Age%20Group).|
###|forbidden_locations|string[]|The codes of the targeted regions that failed the review.

For enum values, see [Appendix - Location codes](https://business-api.tiktok.com/portal/docs?id=1737585867307010).|
###|forbidden_placements|string[]|The placements that failed the review.

For enum values, see [Enumeration - Placement](https://business-api.tiktok.com/portal/docs?id=1737174886619138#item-link-Placement).|
###|content_info|object|Details of the content that was rejected.|
####|content_type|string|Content type.

Enum values:
- `ModeString`: string.
- `ModeImage`: image.
- `ModeVideo`: video.
- `ModeMusic`: music to be used in a carousel.
- `LandingPage`: landing page.
- `ModeCollection`: series collection.
- `ModePhotoPost:` TikTok photo post.|
####|text_content|string|The text that was rejected.|
####|image_content|object|The image content that was rejected.|
#####|image_id|string|The ID of the image.|
####|video_content|object|The video content that was rejected.|
#####|video_id|string|The ID of the video.|
####|carousel_music_info|object|The music content in a carousel that was rejected.|
#####|music_id|string|The ID of the music.|
###|violation_frames|object[]|Returned only when `include_violation_frame` is set to `true` in the request.

Details of the video frames that have been flagged for violations.|
####|type|string|The type of frame.|
####|video_id|string|Video ID.|
####|web_url_list|string[]|A list of image URLs or landing page URLs flagged for violations.|
####|violation_frame_material_type|string|The type of creative that was considered a violative item in the frame.

Enum values:
- `DOWNLOAD URL`: Download URL.
- `EXTERNAL_URL`: Landing page URL.
- `INSTANT_PAGE`: TikTok Instant Page.
- `LEAD_GENERATION`: Instant Form.
- `OPEN_URL`: Deeplink.
- `VIDEO`: Video.
- `UNSET`: Other.|
###|specification|string|An auto-generated summary for the rejection reason.|
###|video_violation_frames|object[]|Details of images flagged for violations.|
####|web_url|string|The URL of the image of a specific frame where a violation has occurred.|
####|hover_periods|string[]|A list of time periods when violations occur in hover images.|
####|thumbnail_periods|string[]|A list of time periods when violations occur in thumbnail images.|
#|material_review_infos|object[]|Information about the review result for the creatives.|
##|ad_material_id|string|An ad-specific material ID generated when a particular creative is used in an ad.

This ID differs from the creative ID you receive when uploading the creative to your ad account’s Creative Library.

**Note**: For carousel creatives, this ID identifies an image inside the carousel, while the `ad_material_id` from [/smart_plus/ad/get/](https://business-api.tiktok.com/portal/docs?id=1843317378982914) identifies the entire carousel itself.|
##|smart_plus_ad_id|string|Ad ID.|
##|review_status|string|The review status of the creative.

Enum values:
- `ALL_AVAILABLE`: The creative has been reviewed and can be delivered to all specified targeting countries.
- `PART_AVAILABLE`: The creative has been reviewed and can only be delivered to some of the specified targeting countries.
- `UNAVAILABLE`: The creative has been reviewed and cannot be delivered.|
##|passed_locations|string[]|The targeted regions that passed the review.

For enum values, see [Appendix - Location codes](https://business-api.tiktok.com/portal/docs?id=1737585867307010).|
##|reject_info|object[]|Details of the rejection.|
###|reasons|string[]|The reasons for failing the ad review.|
###|suggestion|string|The review suggestion.|
###|forbidden_ages|string[]|The age groups that failed the review.

For enum values, see [Enumeration - Age Group](https://business-api.tiktok.com/portal/docs?id=1737174886619138#item-link-Age%20Group).|
###|forbidden_locations|string[]|The codes of the targeted regions that failed the review.

For enum values, see [Appendix - Location codes](https://business-api.tiktok.com/portal/docs?id=1737585867307010).|
###|forbidden_placements|string[]|The placements that failed the review.

For enum values, see [Enumeration - Placement](https://business-api.tiktok.com/portal/docs?id=1737174886619138#item-link-Placement).|
###|content_info|object|Details of the content that was rejected.|
####|content_type|string|Content type.

Enum values:
- `ModeString`: string.
- `ModeImage`: image.
- `ModeVideo`: video.
- `ModeMusic`: music to be used in a carousel.
- `LandingPage`: landing page.
- `ModeCollection`: series collection.
- `ModePhotoPost:` TikTok photo post.|
####|text_content|string|The text that was rejected.|
####|image_content|object|The image content that was rejected.|
#####|image_id|string|The ID of the image.|
####|video_content|object|The video content that was rejected.|
#####|video_id|string|The ID of the video.|
####|carousel_music_info|object|The music content in a carousel that was rejected.|
#####|music_id|string|The ID of the music.|
###|violation_frames|object[]|Returned only when `include_violation_frame` is set to `true` in the request.

Details of the video frames that have been flagged for violations.|
####|type|string|The type of frame.|
####|video_id|string|Video ID.|
####|web_url_list|string[]|A list of image URLs or landing page URLs flagged for violations.|
####|violation_frame_material_type|string|The type of creative that was considered a violative item in the frame.

Enum values:
- `DOWNLOAD URL`: Download URL.
- `EXTERNAL_URL`: Landing page URL.
- `INSTANT_PAGE`: TikTok Instant Page.
- `LEAD_GENERATION`: Instant Form.
- `OPEN_URL`: Deeplink.
- `VIDEO`: Video.
- `UNSET`: Other.|
###|specification|string|An auto-generated summary for the rejection reason.|
###|video_violation_frames|object[]|Details of images flagged for violations.|
####|web_url|string|The URL of the image of a specific frame where a violation has occurred.|
####|hover_periods|string[]|A list of time periods when violations occur in hover images.|
####|thumbnail_periods|string[]|A list of time periods when violations occur in thumbnail images.|
```

### Example
```xcodeblock
(code Success-Response http)
{
    "code": 0,
    "message": "OK",
    "request_id": "{{request_id}}",
    "data": {
        "material_review_infos": [
            {
                "ad_material_id": "{{ad_material_id}}",
                "passed_locations": null,
                "reject_info": null,
                "review_status": "ALL_AVAILABLE",
                "smart_plus_ad_id": "{{smart_plus_ad_id}}"
            },
            {
                "ad_material_id": "{{ad_material_id}}",
                "passed_locations": null,
                "reject_info": null,
                "review_status": "ALL_AVAILABLE",
                "smart_plus_ad_id": "{{smart_plus_ad_id}}"
            }
        ],
        "smart_plus_ad_review_infos": [
            {
                "appeal_reject_reasons": null,
                "appeal_status": "NOT_APPEALED",
                "passed_locations": null,
                "reject_info": [],
                "review_status": "ALL_AVAILABLE",
                "smart_plus_ad_id": "{{smart_plus_ad_id}}"
            }
        ]
    }
}
(/code)
```
