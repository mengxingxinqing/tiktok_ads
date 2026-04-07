# Create Website Conversions ads

**Doc ID**: 1775548501843970
**Path**: Use Cases/Campaign creation/Create Website Conversions ads

---

This article walks you through the steps to create Website Conversions ads.
# Introduction

The Web conversions campaign  empowers you to drive conversions on your website or TikTok Instant Page. 

**You can use Campaign Management API to create Website Conversions ads, and this helps you streamline your ad creation experience, and elevate operational efficiency and scalability.**

For a comprehensive introduction to and best practices for Web Conversions ads, consult [API for Business Playbook - Web Conversion Ads](https://bytedance.feishu.cn/file/KlASbCsJToyC18xHVzKcbWcGnbc).

# Prerequisites
- You've gained access to TikTok API for Business. See [Get Started - Step by step workflow](https://business-api.tiktok.com/portal/docs?id=1735713609895937) for details. 
- To create Website Conversions ads, you need relevant permissions. See [API Reference](https://business-api.tiktok.com/portal/docs?id=1735713875563521) to find out the permissions required for endpoints (including the endpoints listed in the "Steps" section) and see [Update app permissions](https://business-api.tiktok.com/portal/docs?id=1738855280338946) to find out how to configure permissions.

# Steps

## 1. Create a campaign
Create a campaign using [/campaign/create/](https://business-api.tiktok.com/portal/docs?id=1739318962329602). Note that the following requirements must be met.

  
| 
    Setting | 
    Requirement | 
    Parameter | 
    How to configure the parameter | 
   |

  
| 
    Advertising objective | 
    Website Conversions | 
    `objective_type` | 
    `WEB_CONVERSIONS` | 
   |
  
| 
    Smart+ Campaign | 
    Disabled

To learn about how to create a Smart+ Web Conversion campaign, see [Create a Smart+ Campaign](https://business-api.tiktok.com/portal/docs?id=1768006268820546) . | 
    / | 
    / | 
   |
    
| 
    iOS 14 Dedicated Campaign | 
    Disabled | 
    `campaign_type` | 
    `REGULAR_CAMPAIGN` or not passed. | 
   |
  
| 
    `app_id` | 
    Not passed | 
   |
  
| 
    `campaign_app_profile_page_state` | 
    Not passed | 
   |
  
| 
    Campaign Budget Optimization (CBO) | 
    Enabled or Disabled

To learn more about how to create a CBO Web Conversion campaign, see [Campaign Budget Optimization](https://business-api.tiktok.com/portal/docs?id=1739381757818881) . | 
    `budget_optimize_on` | 
    `true`, or `false` or not passed | 
   |

### Example

Request
```xcodeblock
(code curl http)
curl --location --request POST 'https://business-api.tiktok.com/open_api/v1.3/campaign/create/' \
--header 'Access-Token: {{Access-Token}}' \
--header 'Content-Type: application/json' \
--data '{
    "advertiser_id": "{{advertiser_id}}",
    "objective_type": "WEB_CONVERSIONS",
    "campaign_name": "{{campaign_name}}",
    "campaign_type": "REGULAR_CAMPAIGN",
    "budget_mode":"BUDGET_MODE_TOTAL",
    "budget": {{budget}}
}'
(/code)
```

Response
```xcodeblock
(code curl http)
{
    "code": 0,
    "message": "OK",
    "request_id": "{{request_id}}",
    "data": {
        "campaign_name": "{{campaign_name}}",
        "modify_time": "{{modify_time}}",
        "objective": "LANDING_PAGE",
        "roas_bid": 0,
        "budget": {{budget}},
        "secondary_status": "CAMPAIGN_STATUS_ENABLE",
        "is_smart_performance_campaign": false,
        "create_time": "{{create_time}}",
        "deep_bid_type": null,
        "campaign_type": "REGULAR_CAMPAIGN",
        "is_new_structure": true,
        "campaign_id": "{{campaign_id}}",
        "budget_mode": "BUDGET_MODE_INFINITE",
        "objective_type": "WEB_CONVERSIONS",
        "advertiser_id": "{{advertiser_id}}",
        "operation_status": "ENABLE"
    }
}
(/code)
```

## 2. Create an ad group
Create an ad group using [/adgroup/create/](https://business-api.tiktok.com/portal/docs?id=1739499616346114). Note that the following requirements must be met.

> **Note**

> Ad groups with the optimization goal Automatic Value Optimization cannot be used in [/split_test/create/](https://business-api.tiktok.com/portal/docs?id=1742666471475201) to create split tests.

``` xtable
| Setting{18%} | Requirement{25%} | Parameter{22%} | How to configure the parameter{35%} |
|---|---|---|
|Optimization location 
(Promotion type)| One of the following types: 
- WebsiteTikTok instant Page|`promotion_type`
`promotion_website_type`|
- To specify  optimization location as Website: Set `promotion_type` to `WEBSITE`.
- Set `promotion_website_type` to `UNSET` or do not pass this field.
- To specify optimization location as TikTok Instant Page: Set `promotion_type` to `WEBSITE`.
-  Set `promotion_website_type` to `TIKTOK_NATIVE_PAGE`. |
| Pixel | 
- Optional when the  optimization location is Website. 
- Not supported when the optimization location is TikTok Instant Page. | `pixel_id` |
- When `promotion_website_type` is set to `UNSET` or not passed, pass a valid value or not pass this field. 
- When `promotion_website_type` is set to `TIKTOK_NATIVE_PAGE`, do not pass this field. |
| Optimization event | 
- When the optimization location is Website and Pixel is not passed: Not supported.
- When the optimization location is Website and Pixel is passed, or when the optimization location is TikTok instant Page: Specified.
**Note**: When the optimization location is TikTok Instant Page, the only supported optimization event is Click Button.   | `optimization_event` | 
- When `promotion_website_type` is set to `UNSET` (or not passed) and `pixel_id` is not passed: Do not pass this field.
- When `promotion_website_type` is set to `UNSET` (or not passed) and `pixel_id` is passed, or when `promotion_website_type` is set to `TIKTOK_NATIVE_PAGE`: Pass a valid value.To obtain the optimization events that have been configured for a Pixel, use [/pixel/list/](https://business-api.tiktok.com/portal/docs?id=1740858697598978).
- See [Conversion events - Pixel events](https://business-api.tiktok.com/portal/docs?id=1739361474981889#item-link-Pixel%20events%0A%0A) for enum values. **Note**: When `promotion_website_type` is set to `TIKTOK_NATIVE_PAGE`, this field can only be set to `BUTTON`.|
| Placement | When the  optimization location is TikTok Instant Page, the placement should at least include TikTok or Pangle | `placement_type`
 `placements` | When `promotion_website_type` is set to `TIKTOK_NATIVE_PAGE`, you can either:
- set `placement_type` to `PLACEMENT_TYPE_AUTOMATIC`
- OR set `placement_type` to `PLACEMENT_TYPE_NORMAL` and include at least `PLACEMENT_TIKTOK` or `PLACEMENT_PANGLE` in the value of `placements` |
| Audience targeting
· Automatic targeting  | Disabled | `auto_targeting_enabled` | Not passed |
| Audience targeting
· Targeting expansion| Disabled | `targeting_expansion` | Not passed |
| Contextual Targeting | Disabled | `contextual_tag_ids` | Not passed |
| Pre-bid third-party brand safety filtering 
 (Inventory filter)  | Disabled | `brand_safety_type` |Do not set this field to `THIRD_PARTY`.  |
| Pre-bid third-party brand safety filtering  | Disabled | `brand_safety_partner` | Not passed |
| Optimization goal | 
- When the optimization location is Website, the supported optimization goals are Click, Conversion, Value, and Automatic Value Optimization. If CBO is enabled at the campaign level, the optimization goal Click is not supported.
- When the optimization location is TikTok Instant Page, the supported optimization goal is Conversion. | `optimization_goal` | 
- When `promotion_website_type` is set to `UNSET` or not passed, set `optimization_goal` to any of the following values: `CLICK`This value is not supported if `budget_optimize_on` is set to `true` at the campaign level.
- `CONVERT` (with `pixel_id` and `optimization_event` specified)
- `VALUE` (with `pixel_id` specified and `optimization_event` set to `SHOPPING`)To learn about how to use the optimization goal Value for the Web Conversions objective, see [Enable VBO for Web](https://business-api.tiktok.com/portal/docs?id=1770019181843458#item-link-Enable%20VBO%20for%20Web).
- `AUTOMATIC_VALUE_OPTIMIZATION` (with `pixel_id` specified and `optimization_event` set to `SHOPPING`)To learn about how to use the optimization goal Automatic Value Optimization for the Web Conversions objective, see [Enable VBO for Web](https://business-api.tiktok.com/portal/docs?id=1770019181843458#item-link-Enable%20VBO%20for%20Web).
- When `promotion_website_type` is set to `TIKTOK_NATIVE_PAGE`, set `optimization_goal` to `CONVERT`. 
**Note**: 
- Automatic Value Optimization is currently an allowlist-only feature. If you would like to access it, please contact your TikTok representative.
- Enabling Automatic Value Optimization and Campaign Budget Optimization at the same time is currently an allowlist-only feature. If you would like to access it, please contact your TikTok representative. |
| Bid Strategy | 
- If Optimization Goal is Click or Conversion, the strategy can be Maximum Delivery or Cost Cap (or Target CPA).
- If Optimization Goal is Value, the strategy can be Highest value or Minimum ROAS (or Target ROAS).
- If Optimization Goal is Automatic Value Optimization, the strategy can only be Highest value.  | `bid_type`
`bid_price` 
`conversion_bid_price` 
`deep_bid_type`
`roas_bid`  | 
- If `optimization_goal` is `CLICK` or `CONVERT`:Set `bid_type` to `BID_TYPE_CUSTOM` or `BID_TYPE_NO_BID`. Do not pass `deep_bid_type` and `roas_bid`.If `optimization_goal` is `CONVERT`, and `bid_type` is `BID_TYPE_CUSTOM`, pass `conversion_bid_price` at the same time. 
- If `optimization_goal` is `CLICK`, and `bid_type` is `BID_TYPE_CUSTOM`, pass `bid_price` at the same time. 
-  If `optimization_goal` is `VALUE`:Set `deep_bid_type` to `VO_MIN_ROAS` or `VO_HIGHEST_VALUE`, and set `bid_type` to `BID_TYPE_NO_BID`. Do not pass `conversion_bid_price` and `bid_price`. If you set `deep_bid_type` to `VO_MIN_ROAS`, pass in `roas_bid` at the same time.
- If `optimization_goal` is `AUTOMATIC_VALUE_OPTIMIZATION`:`roas_bid` is not supported. 
- Set `deep_bid_type` to `VO_HIGHEST_VALUE` and `bid_type` to `BID_TYPE_NO_BID`.The fields `deep_bid_type` and `bid_type` can be omitted. If you omit these fields, `deep_bid_type` will default to `VO_HIGHEST_VALUE` and `bid_type` will default to `BID_TYPE_NO_BID`. |
| Attribution settings | Select from the supported attribution setting options for the specific scenario. | `click_attribution_window`
`view_attribution_window`
`attribution_event_count`  | To learn about the supported attribution setting options for different scenarios, see [Attribution window and event count - Website conversions](https://business-api.tiktok.com/portal/docs?id=1777694366654465#item-link-Website%20conversions). |
| Billing event | 
- When the optimization goal is Click, the supported billing event is CPC. When the optimization goal is  Conversion, Value, or Automatic Value Optimization, the supported billing event is oCPM.   | `billing_event` | 
- When` optimization_goal` is set to `CLICK`, set `billing_event` to `CPC` When `optimization_goal` is set to `CONVERT`, `VALUE`, or `AUTOMATIC_VALUE_OPTIMIZATION`, set `billing_event` to `OCPM`.|
| Delivery Type | If Bid Strategy is set to Cost Cap, you can set Delivery Type to Standard or Accelerated.
- If Bid Strategy is set to Maximum Delivery, Highest Value or Minimum ROAS, you can only set Delivery Type to Standard.  | `pacing` | 
- If `bid_type` is `BID_TYPE_CUSTOM`, you can set pacing to `PACING_MODE_SMOOTH` or `PACING_MODE_FAST`.
-  If `bid_type` is `BID_TYPE_NO_BID`, you can only set pacing to `PACING_MODE_SMOOTH`. |
```

### Example 

Request
```xcodeblock
(code curl http)
curl --location --request POST 'https://business-api.tiktok.com/open_api/v1.3/adgroup/create/' \
--header 'Access-Token: {{Access-Token}}' \
--header 'Content-Type: application/json' \
--data '{
    "advertiser_id": "{{advertiser_id}}",
    "campaign_id": "{{campaign_id}}",
    "adgroup_name": "{{adgroup_name}}",
    "app_id": "{{app_id}}",
    "promotion_type": "WEBSITE",
    "promotion_website_type": "TIKTOK_NATIVE_PAGE",
    "optimization_event": "BUTTON",
    "placement_type": "PLACEMENT_TYPE_NORMAL",
    "placements": ["PLACEMENT_TIKTOK","PLACEMENT_PANGLE"],
    "location_ids": ["6252001"],
    "budget_mode": "BUDGET_MODE_DAY",
    "budget":{{budget}},
    "schedule_type": "SCHEDULE_START_END",
    "schedule_start_time": "{{schedule_start_time}}",
    "schedule_end_time":"{{schedule_end_time}}",
    "optimization_goal": "CONVERT",
    "bid_type": "BID_TYPE_CUSTOM",
    "conversion_bid_price": {{conversion_bid_price}},
    "billing_event": "OCPM",
    "pacing": "PACING_MODE_SMOOTH"
}'
(/code)
```
Response
```xcodeblock
(code curl http)
{
    "code": 0,
    "message": "OK",
    "request_id": "{{request_id}}",
    "data": {
        "interest_category_ids": [],
        "conversion_window": null,
        "rf_estimated_cpr": null,
        "bid_price": 0.0,
        "is_new_structure": true,
        "brand_safety_partner": null,
        "bid_display_mode": "CPMV",
        "purchased_impression": null,
        "location_ids": [
            "6252001"
        ],
        "campaign_id": "{{campaign_id}}",
        "schedule_end_time": "2033-10-21 00:21:13",
        "audience_ids": [],
        "video_download_disabled": false,
        "schedule_infos": null,
        "operating_systems": [],
        "feed_type": null,
        "actions": [],
        "languages": [],
        "comment_disabled": false,
        "app_type": null,
        "adgroup_id": "{{adgroup_id}}",
        "share_disabled": false,
        "search_result_enabled": false,
        "keywords": null,
        "secondary_status": "ADGROUP_STATUS_CREATE",
        "optimization_event": "BUTTON",
        "statistic_type": null,
        "schedule_type": "SCHEDULE_FROM_NOW",
        "campaign_name": "{{campaign_name}}",
        "adgroup_name": "{{adgroup_name}}",
        "conversion_bid_price": 0.0,
        "ios14_quota_type": "UNOCCUPIED",
        "network_types": [],
        "delivery_mode": null,
        "excluded_audience_ids": [],
        "brand_safety_type": "NO_BRAND_SAFETY",
        "modify_time": "{{modify_time}}",
        "targeting_expansion": {
            "expansion_types": [],
            "expansion_enabled": false
        },
        "adgroup_app_profile_page_state": null,
        "dayparting": "111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111",
        "rf_purchased_type": null,
        "advertiser_id": "{{advertiser_id}}",
        "gender": "GENDER_UNLIMITED",
        "device_price_ranges": null,
        "optimization_goal": "CONVERT",
        "bid_type": "BID_TYPE_NO_BID",
        "auto_targeting_enabled": false,
        "inventory_filter_enabled": false,
        "app_download_url": null,
        "budget": {{budget}},
        "skip_learning_phase": true,
        "pacing": "PACING_MODE_SMOOTH",
        "category_exclusion_ids": [],
        "promotion_type": "WEBSITE",
        "placements": [
            "PLACEMENT_TIKTOK",
            "PLACEMENT_GLOBAL_APP_BUNDLE",
            "PLACEMENT_PANGLE"
        ],
        "frequency_schedule": null,
        "creative_material_mode": "CUSTOM",
        "promotion_website_type": "TIKTOK_NATIVE_PAGE",
        "frequency": null,
        "is_hfss": false,
        "next_day_retention": null,
        "budget_mode": "BUDGET_MODE_DAY",
        "rf_estimated_frequency": null,
        "interest_keyword_ids": [],
        "isp_ids": [],
        "placement_type": "PLACEMENT_TYPE_AUTOMATIC",
        "schedule_start_time": "{{schedule_start_time}}",
        "category_id": "0",
        "scheduled_budget": 0.0,
        "operation_status": "ENABLE",
        "deep_bid_type": null,
        "billing_event": "OCPM",
        "purchased_reach": null,
        "pixel_id": null,
        "deep_cpa_bid": 0.0,
        "create_time": "{{create_time}}",
        "age_groups": null,
        "app_id": null,
        "secondary_optimization_event": null
    }
}
(/code)
```

## 3. Create an ad
Create an ad using [/ad/create/](https://business-api.tiktok.com/portal/docs?id=1739953377508354). Note that the following requirements must be met.

``` xtable
| Setting{15%} | Requirement{25%} | Parameter{18%} | How to configure the parameter{42%} |
|---|---|---|
| Ad format | 
- Single video
- Single image
- Carousel | `ad_format` | 
- `SINGLE_VIDEO`
- `SINGLE_IMAGE`
- `CAROUSEL_ADS`  |
| Destination |
- If optimization location is specified as Website at the ad group level, the destination can be website URL or a TikTok Instant Page. 
- If optimization location is specified as TikTok Instant Page at the ad group level, destination can only be a TikTok Instant Page. | `landing_page_url` 
`page_id`
 `creative_type` |
- If `promotion_website_type` is set to `UNSET` or not passed at the ad group level, you need to specify a website URL through `landing_page_url`, or specify a TikTok Instant Page through `page_id`. To filter TikTok Instant Pages within your ad account, call [/page/get/](https://business-api.tiktok.com/portal/docs?id=1820826387779586). Pass `advertiser_id` and set `business_type` to `TIKTOK_INSTANT_PAGE`.
-  If `promotion_website_type` is set to `TIKTOK_NATIVE_PAGE` at the ad group level, you need to specify a TikTok Instant Page through `page_id`.  If `page_id` is passed, you can omit `creative_type`, then the field will default to `CUSTOM_INSTANT_PAGE`. Or you can manually set `creative_type` to `CUSTOM_INSTANT_PAGE`.  |
```

### Example
Request
```xcodeblock
(code curl http)
curl --location --request POST 'https://business-api.tiktok.com/open_api/v1.3/ad/create/' \
--header 'Access-Token: {{Access-Token}}' \
--header 'Content-Type: application/json' \
--data '{
    "advertiser_id": "{{advertiser_id}}",
    "adgroup_id": "{{adgroup_id}}",
    "creatives": [{
        "ad_name": "{{ad_name}}",
        "identity_id":"{{identity_id}}",
        "identity_type":"CUSTOMIZED_USER",
        "ad_format": "SINGLE_VIDEO",
        "video_id":"{{video_id}}",
        "image_ids":["{{image_id}}"],
        "ad_text": "{{ad_text}}",
        "call_to_action": "SIGN_UP",
        "page_id":"{{page_id}}"
    }]
}'
(/code)
```

Response
```xcodeblock
(code curl http)
{
    "code": 0,
    "message": "OK",
    "request_id": "{{request_id}}",
    "data": {
        "ad_ids": [
            "{{ad_id}}"
        ],
        "need_audit": false,
        "creatives": [
            {
                "landing_page_urls": null,
                "vast_moat_enabled": false,
                "ad_texts": null,
                "creative_authorized": false,
                "campaign_name": "{{campaign_name}}",
                "music_id": null,
                "ad_name": "{{ad_name}}",
                "image_ids": [
                    "{{image_id}}"
                ],
                "adgroup_id": "{{adgroup_id}}",
                "brand_safety_postbid_partner": "UNSET",
                "impression_tracking_url": null,
                "ad_id": "{{ad_id}}",
                "ad_text": "{{ad_text}}",
                "ad_format": "SINGLE_VIDEO",
                "ad_ref_pixel_id": {{ad_ref_pixel_id}},
                "viewability_vast_url": null,
                "create_time": "{{create_time}}",
                "click_tracking_url": null,
                "app_name": "",
                "fallback_type": "UNSET",
                "campaign_id": "{{campaign_id}}",
                "modify_time": "{{modify_time}}",
                "deeplink": null,
                "avatar_icon_web_uri": "{{avatar_icon_web_uri}}",
                "call_to_action_id": "{{call_to_action_id}}",
                "playable_url": "",
                "adgroup_name": "{{adgroup_name}}",
                "video_id": "{{video_id}}",
                "is_new_structure": true,
                "tracking_offline_event_set_ids": [
                    "{{tracking_offline_event_set_id}}",
                    "{{tracking_offline_event_set_id}}"
                ],
                "viewability_postbid_partner": "UNSET",
                "card_id": null,
                "landing_page_url": "",
                "identity_id": "{{identity_id}}",
                "brand_safety_vast_url": null,
                "creative_type": "CUSTOM_INSTANT_PAGE",
                "page_id": {{page_id}},
                "profile_image_url": "{{profile_image_url}}",
                "optimization_event": "BUTTON",
                "tracking_pixel_id": 0,
                "identity_type": "CUSTOMIZED_USER",
                "advertiser_id": "{{advertiser_id}}",
                "operation_status": "ENABLE",
                "display_name": "{{display_name}}",
                "is_aco": false
            }
        ]
    }
}
(/code)
```

# Related docs
- [Campaign Management API](https://business-api.tiktok.com/portal/docs?id=1739381823123458)
- [Campaign Management Guide](https://business-api.tiktok.com/portal/docs?id=1735713781404673)
- [Web conversions](https://business-api.tiktok.com/portal/docs?id=1747553507237889)
