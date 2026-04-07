# Create single image ads

**Doc ID**: 1777633230937090
**Path**: Use Cases/Campaign creation/Create single image ads

---

This article walks you through the steps to create single image ads on Pangle or Global App Bundle placement.

## Introduction
Single image is an ad format that enables you to present your product, service, or brand using a single image. It provides a visually appealing way to capture the attention of your audience and encourage conversions.

**You can use Campaign Management API to create single image ads, and this helps you streamline your ad creation experience, and elevate operational efficiency and scalability.**

## Prerequisites
- You've gained access to TikTok API for Business. See [Get Started - Step by step workflow](https://ads.tiktok.com/marketing_api/docs?id=1735713609895937) for details. 
  - To create single image ads, you need relevant permissions. See [API Reference](https://ads.tiktok.com/marketing_api/docs?id=1735713875563521) to find out permissions required for endpoints (including the endpoints listed in the **"Steps"** section) and see [Update app permissions](https://ads.tiktok.com/marketing_api/docs?id=1738855280338946) to find out how to configure permissions.  
- Creating single image Pangle ads by using an image of the resolution 640 x 100 pixels, 600 x 500 pixels, or 640 x 200 pixels is currently an allowlist-only feature. If you would like to access it, please contact your TikTok representative.

## Steps

### Create single image ads on Pangle placement
1. Create a campaign using [/campaign/create/](https://ads.tiktok.com/marketing_api/docs?id=1739318962329602). Note that the following requirements must be met.

```xtable
| Setting {20%} | Requirement {25%} | Parameter {20%} | How to configure the parameter {35%} |
|---|---|---|---|
| Advertising objective | One of the following objectives: 
-  App promotion 
-  Website conversions 
-  Traffic 
- Lead generation 
- Product sales
**Note**: If you select Lead generation, you need to set Optimization location as Website at the ad group level. To learn more about how to create single image Lead Generation ads, see [Create a Lead Generation ad with optimization location as Website](https://business-api.tiktok.com/portal/docs?id=1774482976097281).| `objective_type` | Any value below: 
- `APP_PROMOTION`
- `WEB_CONVERSIONS`
- `TRAFFIC`
- `LEAD_GENERATION`
- `PRODUCT_SALES`
**Note**: If you set this field to `LEAD_GENERATION`, you need to set `promotion_target_type` to `EXTERNAL_WEBSITE` at the ad group level. To learn more about how to create single image Lead Generation ads, see [Create a Lead Generation ad with optimization location as Website](https://business-api.tiktok.com/portal/docs?id=1774482976097281).|
```
> **Note**

> The Smart+ Campaign setting should be disabled for the single image campaign. If you are not sure about whether the campaign is Smart+ Campaign, you can use the `is_smart_performance_campaign` field returned from [/campaign/get/](https://ads.tiktok.com/marketing_api/docs?id=1739315828649986) to check.

**Example**

Request
```xcodeblock
(code curl http)
curl --location --request POST 'https://business-api.tiktok.com/open_api/v1.3/campaign/create/' \
--header 'Access-Token: {{Access-Token}}' \
--header 'Content-Type: application/json' \
--data '{
    "advertiser_id": "{{advertiser_id}}",
    "objective_type": "TRAFFIC",
    "campaign_name": "{{campaign_name}}",
    "budget_mode": "BUDGET_MODE_TOTAL",
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
        "create_time": "{{create_time}}",
        "secondary_status": "CAMPAIGN_STATUS_ENABLE",
        "is_smart_performance_campaign": false,
        "advertiser_id": "{{advertiser_id}}",
        "budget_mode": "BUDGET_MODE_TOTAL",
        "budget": {{budget}},
        "is_new_structure": true,
        "campaign_id": "{{campaign_id}}",
        "modify_time": "{{modify_time}}",
        "campaign_name": "{{campaign_name}}",
        "operation_status": "ENABLE",
        "campaign_type": "REGULAR_CAMPAIGN",
        "deep_bid_type": null,
        "objective_type": "TRAFFIC",
        "roas_bid": 0,
        "objective": "LANDING_PAGE"
    }
}
(/code)
```
2. Create an ad group using [/adgroup/create/](https://ads.tiktok.com/marketing_api/docs?id=1739499616346114). Note that the following requirements must be met.

  
| 
    Setting | 
    Requirement | 
    Parameter | 
    How to configure the parameter | 
   |

  
| 
    Placements | 
    **Select Placement **with Pangle placement
 | 
    `placement_type` | 
    `PLACEMENT_TYPE_NORMAL` | 
   |
  
| 
    `placements` | 
    `["PLACEMENT_PANGLE"]` | 
   |
  
| 
    Audience targeting - Location | 
    One or more locations that are available for Pangle placement | 
    `location_ids` | 
    Set `location_ids` to one or more locations available for Pangle placement.

To learn about the locations available for Pangle placement based on the place of registration for your ad account, refer to the Help Center article [Placements and Available Locations](https://ads.tiktok.com/help/article/placements-available-locations?lang=en#anchor-1).

To obtain the location IDs that are available for your ad account under Pangle placement, use [/tool/region/](https://business-api.tiktok.com/portal/docs?id=1737189539571713) and set `placements` to `["PLACEMENT_PANGLE"]`. | 
   |

**Example**

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
    "promotion_type": "WEBSITE",
    "placement_type": "PLACEMENT_TYPE_NORMAL",
    "placements": [
        "PLACEMENT_PANGLE"
    ],
    "video_download_disabled": true,
    "location_ids": ["102358"],
    "budget_mode": "BUDGET_MODE_TOTAL",
    "budget": {{budget}},
    "schedule_type": "SCHEDULE_START_END",
    "schedule_start_time": "{{schedule_start_time}}",
    "schedule_end_time": "{{schedule_end_time}}",
    "optimization_goal": "CLICK",
    "bid_type": "BID_TYPE_NO_BID",
    "billing_event": "CPC",
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
        "rf_estimated_frequency": null,
        "promotion_type": "WEBSITE",
        "feed_type": null,
        "is_new_structure": true,
        "optimization_event": null,
        "conversion_bid_price": 0,
        "bid_display_mode": "CPMV",
        "placements": [
            "PLACEMENT_PANGLE"
        ],
        "rf_estimated_cpr": null,
        "ios14_quota_type": "UNOCCUPIED",
        "statistic_type": null,
        "secondary_status": "ADGROUP_STATUS_CREATE",
        "app_download_url": null,
        "creative_material_mode": "CUSTOM",
        "app_type": null,
        "campaign_id": "{{campaign_id}}",
        "bid_price": 0,
        "campaign_name": "{{campaign_name}}",
        "schedule_start_time": "{{schedule_start_time}}",
        "adgroup_id": "{{adgroup_id}}",
        "category_id": "0",
        "purchased_impression": null,
        "actions": [],
        "schedule_type": "SCHEDULE_START_END",
        "interest_category_ids": [],
        "operation_status": "ENABLE",
        "frequency_schedule": null,
        "video_download_disabled": true,
        "bid_type": "BID_TYPE_NO_BID",
        "audience_ids": [],
        "adgroup_name": "{{adgroup_name}}",
        "schedule_infos": null,
        "skip_learning_phase": false,
        "operating_systems": [],
        "schedule_end_time": "{{schedule_end_time}}",
        "app_id": null,
        "optimization_goal": "CLICK",
        "conversion_window": null,
        "advertiser_id": "{{advertiser_id}}",
        "network_types": [],
        "brand_safety_type": "NO_BRAND_SAFETY",
        "brand_safety_partner": null,
        "delivery_mode": null,
        "scheduled_budget": 0,
        "comment_disabled": false,
        "search_result_enabled": false,
        "languages": [],
        "share_disabled": false,
        "isp_ids": [],
        "auto_targeting_enabled": false,
        "secondary_optimization_event": null,
        "placement_type": "PLACEMENT_TYPE_NORMAL",
        "next_day_retention": null,
        "location_ids": [
            "102358"
        ],
        "pixel_id": null,
        "billing_event": "CPC",
        "rf_purchased_type": null,
        "frequency": null,
        "keywords": null,
        "budget_mode": "BUDGET_MODE_TOTAL",
        "inventory_filter_enabled": false,
        "purchased_reach": null,
        "deep_bid_type": null,
        "interest_keyword_ids": [],
        "pacing": "PACING_MODE_SMOOTH",
        "dayparting": "111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111",
        "age_groups": null,
        "modify_time": "{{modify_time}}",
        "deep_cpa_bid": 0,
        "budget": {{}},
        "gender": "GENDER_UNLIMITED",
        "create_time": "{{create_time}}",
        "excluded_audience_ids": [],
        "device_price_ranges": null,
        "is_hfss": false,
        "adgroup_app_profile_page_state": null,
        "category_exclusion_ids": []
    }
}
(/code)
```

3. Create an ad using [/ad/create/](https://ads.tiktok.com/marketing_api/docs?id=1739953377508354). Note that the following requirements must be met.

```xtable
| Setting {20%} | Requirement {25%} | Parameter {20%} | How to configure the parameter {35%} |
|---|---|---|---|
| Ad format | Single image | `ad_format` | `SINGE_IMAGE` |
| Images | One image that is supported in the single image Pangle ad | `image_ids` | Pass one ID of the image that meets the specification requirements. 
The image to be used in the single image Pangle ad should meet the specification requirements below:
- File Type: JPG, JPEG, or PNG
-  Image Resolution: 720 x 1280 pixels
- 1200 x 628 pixels
- 640 x 640 pixels
- 640 x 100 pixels
- 600 x 500 pixels or
- 640 x 200 pixels
- File Size: within 100 MB
To obtain the image IDs, use [/file/image/ad/upload/](https://business-api.tiktok.com/portal/docs?id=1739067433456642) and [/file/image/ad/search/](https://business-api.tiktok.com/portal/docs?id=1740052016789506).  |
```

**Example**

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
        "identity_id": "{{identity_id}}",
        "identity_type": "CUSTOMIZED_USER",
        "ad_format": "SINGLE_IMAGE",
        "image_ids":["{{image_id}}"],
        "ad_text": "{{ad_text}}",
        "call_to_action": "SHOP_NOW",   
        "landing_page_url":"{{landing_page_url}}"
        }
    ]
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
                "tracking_pixel_id": 0,
                "ad_name": "{{ad_name}}",
                "creative_type": null,
                "ad_text": "{{ad_text}}",
                "campaign_id": "{{campaign_id}}",
                "tracking_offline_event_set_ids": [
                    "{{tracking_offline_event_set_id}}"
                ],
                "music_id": null,
                "page_id": null,
                "video_id": null,
                "create_time": "{{create_time}}",
                "is_aco": false,
                "identity_id": "{{identity_id}}",
                "click_tracking_url": null,
                "landing_page_urls": null,
                "adgroup_id": "{{adgroup_id}}",
                "ad_format": "SINGLE_IMAGE",
                "campaign_name": "{{campaign_name}}",
                "vast_moat_enabled": false,
                "deeplink": "",
                "impression_tracking_url": null,
                "is_new_structure": true,
                "app_name": "",
                "display_name": "{{display_name}}",
                "modify_time": "{{modify_time}}",
                "ad_id": "{{ad_id}}",
                "optimization_event": null,
                "playable_url": "",
                "advertiser_id": "{{advertiser_id}}",
                "adgroup_name": "{{adgroup_name}}",
                "fallback_type": "UNSET",
                "brand_safety_postbid_partner": "UNSET",
                "viewability_vast_url": null,
                "operation_status": "ENABLE",
                "call_to_action": "SHOP_NOW",
                "identity_type": "CUSTOMIZED_USER",
                "landing_page_url": "{{landing_page_url}}",
                "image_ids": [
                    "{{image_id}}"
                ],
                "brand_safety_vast_url": null,
                "avatar_icon_web_uri": "{{avatar_icon_web_uri}}",
                "ad_texts": null,
                "profile_image_url": "{{profile_image_url}}",
                "card_id": null,
                "call_to_action_id": null,
                "deeplink_type": "NORMAL",
                "viewability_postbid_partner": "UNSET",
                "creative_authorized": false
            }
        ]
    }
}
(/code)
```

4. Preview an ad using [/creative/ads_preview/create/](https://ads.tiktok.com/marketing_api/docs?id=1739403070695426). We offer preview types of `AD` and `ADS_CREATION` to enable you to preview single image Pangle ads that you plan to create, and existing single image Pangle ads.

### Create single image ads on Global App Bundle placement
1. Create a campaign using [/campaign/create/](https://ads.tiktok.com/marketing_api/docs?id=1739318962329602). Note that the following requirements must be met.

```xtable
| Setting {20%} | Requirement {25%} | Parameter {20%} | How to configure the parameter {35%} |
|---|---|---|---|
| Advertising objective | One of the following objectives: 
-  App promotion
- Website conversions
- Traffic | `objective_type` | Any value below:
- `APP_PROMOTION`
- `WEB_CONVERSIONS`
- `TRAFFIC` |
| App promotion type 
(when Advertising objective = App promotion) | App Install | `app_promotion_type` | `APP_INSTALL` |
| iOS 14 dedicated campaign | Disabled | `campaign_type` | `REGULAR_CAMPAIGN` |
```

> **Note**

> The Smart+ Campaign setting should be disabled for the single image campaign. If you are not sure about whether the campaign is Smart+ Campaign, you can use the `is_smart_performance_campaign` field returned from [/campaign/get/](https://ads.tiktok.com/marketing_api/docs?id=1739315828649986) to check.

**Example**

Request
```xcodeblock
(code curl http)
curl --location --request POST 'https://business-api.tiktok.com/open_api/v1.3/campaign/create/' \
--header 'Access-Token: {{Access-Token}}' \
--header 'Content-Type: application/json' \
--data '{
    "advertiser_id": "{{advertiser_id}}",
    "objective_type": "TRAFFIC",
    "campaign_name": "{{campaign_name}}",
    "budget_mode": "BUDGET_MODE_TOTAL",
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
        "create_time": "{{create_time}}",
        "secondary_status": "CAMPAIGN_STATUS_ENABLE",
        "is_smart_performance_campaign": false,
        "advertiser_id": "{{advertiser_id}}",
        "budget_mode": "BUDGET_MODE_TOTAL",
        "budget": {{budget}},
        "is_new_structure": true,
        "campaign_id": "{{campaign_id}}",
        "modify_time": "{{modify_time}}",
        "campaign_name": "{{campaign_name}}",
        "operation_status": "ENABLE",
        "campaign_type": "REGULAR_CAMPAIGN",
        "deep_bid_type": null,
        "objective_type": "TRAFFIC",
        "roas_bid": 0,
        "objective": "LANDING_PAGE"
    }
}
(/code)
```

2. Create an ad group using [/adgroup/create/](https://ads.tiktok.com/marketing_api/docs?id=1739499616346114). Note that the following requirements must be met.

  
| 
    Setting | 
    Requirement | 
    Parameter | 
    How to configure the parameter | 
   |

  
| 
    Placements
 | 
    **Select Placement** with Global App Bundle placement
 | 
    `placement_type` | 
    `PLACEMENT_TYPE_NORMAL` | 
   |
  
| 
    `placements` | 
    `["PLACEMENT_GLOBAL_APP_BUNDLE"]` | 
   |
  
| 
    Audience targeting - Automatic targeting | 
    Disabled | 
    `auto_targeting_enabled` | 
    Not passed | 
   |
  
| 
    Audience targeting - Location | 
    One or more locations that are available for Global App Bundle placement | 
    `location_ids` | 
    Set `location_ids` to one or more locations available for Global App Bundle placement.

The available locations you can target with the Global App Bundle placement are: 
- `BR` Brazil
- `ID`: Indonesia
- `JP`: Japan
- `MY`: Malaysia
- `MX`: Mexico
- `PH`: Philippines
- `SA`: Saudi Arabia
- `TH`: Thailand
- `VN`: Vietnam
To obtain the location IDs that are available for your ad account under Global App Bundle placement, use [/tool/region/](https://business-api.tiktok.com/portal/docs?id=1737189539571713) and set `placements` to `["PLACEMENT_GLOBAL_APP_BUNDLE"]`. | 
   |
  
| 
    Audience targeting - Spending power | 
    Disabled | 
    `spending_power` | 
    Not passed | 
   |
  
| 
    Audience targeting - Audience - Include and Exclude | 
    
- The only supported audience types are Engagement, App Activity, and Website Traffic.
- Lookalike audiences are not supported. | 
    `audience_ids`
`excluded_audience_ids` | 
    Pass IDs of Engagement audiences, App Activity audiences, Website Traffic audiences, or a combination of the three audience types.

To obtain the ID of these audience types, use [/dmp/custom_audience/list/](https://business-api.tiktok.com/portal/docs?id=1739940506015746) and select audience IDs with audience_type as `Engagement Audience`, `App Activity Audience`, or `Website Audience`. | 
   |
  
| 
    Audience targeting - Interest & Behaviors | 
    Disabled | 
    `interest_category_ids`
` interest_keyword_ids`
`purchase_intention_keyword_ids`
`actions `
` action_period `
`video_user_actions `
`action_category_ids  `
`action_scene` | 
    Not passed | 
   |
  
| 
    Audience targeting - Targeting expansion | 
    Disabled | 
    `targeting_expansion` | 
    Not passed | 
   |
  
| 
    Optimization goal | 
    
- If Advertising objective is App promotion, the only supported optimization goals are Click and Install.
- If Advertising objective is Website conversions, the only supported optimization goal is Click.
- If Advertising objective is Traffic, the only supported optimization goal is Click. | 
    `optimization_goal` | 
    
- If `objective_type` is set to `APP_PROMOTION`, set this field to `CLICK` or `INSTALL`
- If `objective_type` is set to `WEB_CONVERSIONS`, set this field to `CLICK`.
- If `objective_type` is set to `TRAFFIC`, set this field to `CLICK`. | 
   |
  
| 
    Billing event | 
    
- If optimization goal is Install, set billing event to oCPM.
- If optimization goal is Click, set billing event to CPC. | 
    `billing_event` | 
    
- If `optimization_goal` is set to `INSTALL`, set this field to `OCPM`.
- If `optimization_goal` is set to `CLICK`, set this field to `CPC`. | 
   |

**Example**

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
    "promotion_type": "WEBSITE",
    "placement_type": "PLACEMENT_TYPE_NORMAL",
    "placements": [
        "PLACEMENT_GLOBAL_APP_BUNDLE"
    ],
    "video_download_disabled": true,
    "location_ids": ["102358"],
    "budget_mode": "BUDGET_MODE_TOTAL",
    "budget": {{budget}},
    "schedule_type": "SCHEDULE_START_END",
    "schedule_start_time": "{{schedule_start_time}}",
    "schedule_end_time": "{{schedule_end_time}}",
    "optimization_goal": "CLICK",
    "bid_type": "BID_TYPE_NO_BID",
    "billing_event": "CPC",
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
        "skip_learning_phase": false,
        "adgroup_app_profile_page_state": null,
        "rf_purchased_type": null,
        "schedule_end_time": "{{schedule_end_time}}",
        "frequency": null,
        "create_time": "{{create_time}}",
        "advertiser_id": "{{advertiser_id}}",
        "placements": [
            "PLACEMENT_GLOBAL_APP_BUNDLE"
        ],
        "budget": {{budget}},
        "schedule_infos": null,
        "keywords": null,
        "purchased_reach": null,
        "promotion_type": "WEBSITE",
        "bid_price": 0.0,
        "app_download_url": null,
        "statistic_type": null,
        "share_disabled": false,
        "conversion_window": null,
        "is_hfss": false,
        "app_id": null,
        "delivery_mode": null,
        "interest_keyword_ids": [],
        "operating_systems": [],
        "adgroup_name": "{{adgroup_name}}",
        "excluded_audience_ids": [],
        "dayparting": "111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111",
        "deep_bid_type": null,
        "secondary_optimization_event": null,
        "pixel_id": null,
        "frequency_schedule": null,
        "ios14_quota_type": "UNOCCUPIED",
        "budget_mode": "BUDGET_MODE_TOTAL",
        "campaign_name": "{{campaign_name}}",
        "bid_type": "BID_TYPE_NO_BID",
        "comment_disabled": false,
        "rf_estimated_cpr": null,
        "brand_safety_partner": null,
        "deep_cpa_bid": 0.0,
        "optimization_goal": "CLICK",
        "placement_type": "PLACEMENT_TYPE_NORMAL",
        "audience_ids": [],
        "category_id": "0",
        "inventory_filter_enabled": false,
        "video_download_disabled": true,
        "schedule_type": "SCHEDULE_START_END",
        "creative_material_mode": "CUSTOM",
        "conversion_bid_price": 0.0,
        "location_ids": [
            "102358"
        ],
        "network_types": [],
        "schedule_start_time": "{{schedule_start_time}}",
        "brand_safety_type": "NO_BRAND_SAFETY",
        "interest_category_ids": [],
        "device_price_ranges": null,
        "rf_estimated_frequency": null,
        "next_day_retention": null,
        "secondary_status": "ADGROUP_STATUS_CREATE",
        "age_groups": null,
        "pacing": "PACING_MODE_SMOOTH",
        "campaign_id": "{{campaign_id}}",
        "scheduled_budget": 0.0,
        "feed_type": null,
        "modify_time": "{{modify_time}}",
        "languages": [],
        "purchased_impression": null,
        "billing_event": "CPC",
        "gender": "GENDER_UNLIMITED",
        "auto_targeting_enabled": false,
        "app_type": null,
        "isp_ids": [],
        "optimization_event": null,
        "search_result_enabled": false,
        "actions": [],
        "operation_status": "ENABLE",
        "is_new_structure": true,
        "adgroup_id": "{{adgroup_id}}",
        "bid_display_mode": "CPMV",
        "category_exclusion_ids": []
    }
}
(/code)
```
3. Create an ad using [/ad/create/](https://ads.tiktok.com/marketing_api/docs?id=1739953377508354). Note that the following requirements must be met.

```xtable
| Setting {20%} | Requirement {25%} | Parameter {20%} | How to configure the parameter {35%} |
|---|---|---|---|
| Ad format | Single image | `ad_format` | `SINGE_IMAGE` |
| Images | One image that is supported in the single image Global App Bundle ad | `image_ids` | Pass one ID of the image that meets the specification requirements. 
The image to be used in the single image Global App Bundle ad should meet the specification requirements below:
- File Type: JPG, JPEG, or PNG
-  Image Resolution: 720 x 1280 pixels
- 1200 x 628 pixels or
- 640 x 640 pixels
- File Size: within 100 MB
To obtain the image IDs, use [/file/image/ad/upload/](https://business-api.tiktok.com/portal/docs?id=1739067433456642) and [/file/image/ad/search/](https://business-api.tiktok.com/portal/docs?id=1740052016789506).  |
```

**Example**

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
        "identity_id": "{{identity_id}}",
        "identity_type": "CUSTOMIZED_USER",
        "ad_format": "SINGLE_IMAGE",
        "image_ids":["{{image_id}}"],
        "ad_text": "{{ad_text}}",
        "call_to_action": "SHOP_NOW",   
        "landing_page_url":"{{landing_page_url}}"
        }
    ]
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
                "is_aco": false,
                "click_tracking_url": null,
                "video_id": null,
                "call_to_action_id": null,
                "adgroup_id": "{{adgroup_id}}",
                "deeplink_type": "NORMAL",
                "create_time": "{{create_time}}",
                "ad_id": "{{ad_id}}",
                "app_name": "",
                "identity_id": "{{identity_id}}",
                "tracking_offline_event_set_ids": [
                    "{{tracking_offline_event_set_id}}"
                ],
                "brand_safety_postbid_partner": "UNSET",
                "viewability_postbid_partner": "UNSET",
                "page_id": null,
                "card_id": null,
                "call_to_action": "SHOP_NOW",
                "brand_safety_vast_url": null,
                "deeplink": "",
                "identity_type": "CUSTOMIZED_USER",
                "creative_authorized": false,
                "creative_type": null,
                "ad_text": "{{ad_text}}",
                "adgroup_name": "{{adgroup_name}}",
                "ad_name": "{{ad_name}}",
                "campaign_name": "{{campaign_name}}",
                "campaign_id": "{{campaign_id}}",
                "display_name": "{{display_name}}",
                "ad_texts": null,
                "fallback_type": "UNSET",
                "image_ids": [
                    "{{image_id}}"
                ],
                "music_id": null,
                "landing_page_url": "{{landing_page_url}}",
                "modify_time": "{{modify_time}}",
                "operation_status": "ENABLE",
                "tracking_pixel_id": 0,
                "playable_url": "",
                "is_new_structure": true,
                "viewability_vast_url": null,
                "ad_format": "SINGLE_IMAGE",
                "avatar_icon_web_uri": "{{avatar_icon_web_uri}}",
                "impression_tracking_url": null,
                "landing_page_urls": null,
                "advertiser_id": "{{advertiser_id}}",
                "profile_image_url": "{{profile_image_url}}",
                "vast_moat_enabled": false,
                "optimization_event": null
            }
        ]
    }
}
(/code)
```
