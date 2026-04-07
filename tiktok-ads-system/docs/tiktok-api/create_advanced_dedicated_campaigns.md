# Create Advanced Dedicated Campaigns

**Doc ID**: 1797011827608577
**Path**: Use Cases/Campaign creation/Create Advanced Dedicated Campaigns

---

This article walks you through the steps to create Advanced Dedicated Campaigns.

# Introduction
Advanced Dedicated Campaign is a new iOS campaign type that leverages advanced delivery models benefiting from real-time signals to achieve improved campaign performance on iOS.

**You can use Campaign Management API to create Advanced Dedicated Campaigns, and this helps you streamline your ad creation experience, and elevate operational efficiency and scalability.**

# Prerequisites
- You've gained access to TikTok API for Business. See [Get Started - Step by step workflow](https://business-api.tiktok.com/portal/docs?id=1735713609895937) for details. 
  - To create Advanced Dedicated Campaigns, you need relevant permissions. See [API Reference](https://business-api.tiktok.com/portal/docs?id=1735713875563521) to find out permissions required for endpoints (including the endpoints listed in the **"Steps"** section) and see [Update app permissions](https://business-api.tiktok.com/portal/docs?id=1738855280338946) to find out how to configure permissions.  

# Steps
Based on your preference for enabling Smart+ Campaign for your Advanced Dedicated Campaigns, you can create a Manual Advanced Dedicated Campaign or a Smart+ Advanced Dedicated Campaign. For detailed instructions on creating each type, refer to their respective sections: "**Steps for creating Manual Advanced Dedicated Campaigns**" and "**Steps for creating  Smart+ Advanced Dedicated Campaigns**".

## Steps for creating Manual Advanced Dedicated Campaigns
### 1. Create a campaign
Create a campaign using [/campaign/create/](https://business-api.tiktok.com/portal/docs?id=1739318962329602). Note that the following requirements must be met.

  
| 
    Setting | 
    Requirement | 
    Parameters | 
    How to configure the parameters | 
   |

  
| 
    Advertising objective | 
    App promotion | 
    `objective_type` | 
    `APP_PROMOTION` | 
   |
  
| 
    App promotion type | 
    App install | 
    `app_promotion_type` | 
    `APP_INSTALL` | 
   |
  
| 
    Smart+ Campaign | 
    Disabled.
Campaigns created via `/campaign/create/` are all standard (non-Smart+) campaigns.

If you want to create  Smart+ Advanced Dedicated Campaigns, see [Steps for creating Smart+ Advanced Dedicated Campaigns](#item-link-Steps for creating Smart+ Advanced Dedicated Campaigns). | 
    / | 
    /
 | 
   |
  
| 
    iOS 14 Dedicated Campaign | 
    Enabled | 
    `campaign_type` | 
    `IOS14_CAMPAIGN` | 
   |
  
| 
    `app_id` | 
    Pass the ID of an iOS app that is eligible for Advanced Dedicated Campaigns.

To find eligible apps, use [/app/list/](https://business-api.tiktok.com/portal/docs?id=1740859313270786). The eligible apps should meet the following requirements:
- `platform` is `IOS`
- `advanced_dedicated_campaign_allowed` is `true`
**Note**: Getting access to Advanced Dedicated Campaign requires the app to meet certain criteria. If your app is ineligible for Advanced Dedicated Campaign, reach out to your TikTok representative. Your TikTok representative will be able to provide troubleshooting support to help your app get access to Advanced Dedicated Campaign. | 
   |
  
| 
    `campaign_app_profile_page_state` | 
    `ON`, or `OFF` (or not passed) | 
   |
  
| 
    Use advanced dedicated campaign | 
    Enabled | 
    `is_advanced_dedicated_campaign` | 
    `true` | 
   |
  
| 
    SKAN attribution | 
    Enabled or disabled | 
    `disable_skan_campaign` | 
    Any of the following values: 
- `true`: To disable SKAN attribution. The campaign will not be bound by [Dedicated Campaign quota limits](https://business-api.tiktok.com/portal/docs?id=1752256248260610) and you will be able to retrieve [Self Attribution Network (SAN) metrics](https://business-api.tiktok.com/portal/docs?id=1751443967255553#item-link-SAN%20metrics) for the campaign. However, you cannot retrieve [SKAN reporting metrics](https://business-api.tiktok.com/portal/docs?id=1751443967255553#item-link-SKAN%20metrics) for the campaign. Learn more about [SAN integration](https://ads.tiktok.com/help/article/about-self-attribution-transition)
- `false`: To enable SKAN attribution. The campaign will be bound by [Dedicated Campaign quota limits](https://business-api.tiktok.com/portal/docs?id=1752256248260610) and you will be able to retrieve [SKAN metrics](https://business-api.tiktok.com/portal/docs?id=1751443967255553#item-link-SKAN%20metrics) for the campaign.
**Note**: Disabling SKAN attribution for Dedicated Campaigns is currently an allowlist-only feature. If you would like to access it, please contact your TikTok representative. | 
   |

#### Example

Request
```xcodeblock
(code curl http)
curl --location --request POST 'https://business-api.tiktok.com/open_api/v1.3/campaign/create/' \
--header 'Access-Token: {{Access-Token}}' \
--header 'Content-Type: application/json' \
--data '{
    "advertiser_id": "{{advertiser_id}}",
    "objective_type": "APP_PROMOTION",
    "app_promotion_type": "APP_INSTALL",
    "campaign_type": "IOS14_CAMPAIGN",
    "app_id": "{{app_id}}",
    "is_advanced_dedicated_campaign": true,
    "campaign_name": "{{campaign_name}}",
    "budget_mode": "BUDGET_MODE_TOTAL",
    "budget": {{budget}}
}'
(/code)
```

Response
```xcodeblock
(code curl http)
HTTPS/1.1 200 OK
{
    "code": 0,
    "message": "OK",
    "request_id": "{{request_id}}",
    "data": {
        "budget_mode": "BUDGET_MODE_TOTAL",
        "app_id": "{{app_id}}",
        "create_time": "{{create_time}}",
        "campaign_type": "IOS14_CAMPAIGN",
        "app_promotion_type": "APP_INSTALL",
        "budget": {{budget}},
        "is_search_campaign": false,
        "campaign_id": "{{campaign_id}}",
        "is_new_structure": true,
        "campaign_app_profile_page_state": "OFF",
        "modify_time": "{{modify_time}}",
        "operation_status": "ENABLE",
        "advertiser_id": "{{advertiser_id}}",
        "objective_type": "APP_PROMOTION",
        "secondary_status": "CAMPAIGN_STATUS_ENABLE",
        "deep_bid_type": null,
        "campaign_name": "{{campaign_name}}",
        "is_advanced_dedicated_campaign": true,
        "is_smart_performance_campaign": false,
        "objective": "APP",
        "roas_bid": 0
    }
}
(/code)
```

### 2. Create an ad group

Create an ad group using [/adgroup/create/](https://business-api.tiktok.com/portal/docs?id=1739499616346114). Note that the following requirements must be met.

```xtable
| Setting {20%} | Requirement {25%} | Parameter {20%} | How to configure the parameter {35%} |
|---|---|---|---|
| Optimization location
 (Promotion type) | iOS App | `promotion_type` | `APP_IOS` |
| Placement | Any of the following types: 
- **Automatic Placement**
- **Select Placement** with TikTok placement or Pangle placement or both  | `placement_type`
`placements`   | Any of the following configurations:
-  Set `placement_type` to `PLACEMENT_TYPE_AUTOMATIC`
- Set `placement_type` to `PLACEMENT_TYPE_NORMAL`, and only include `PLACEMENT_TIKTOK` or `PLACEMENT_PANGLE` or both in the value of `placements`  |
|  Device - OS versions| iOS 14.5 or later versions | `operating_systems`
 `min_ios_version`
 `ios14_targeting` | 
- Set `operating_systems` to `["IOS"]` 
-  Set `ios14_targeting` to `IOS14_PLUS`
- Set `min_ios_version` to `14.5` or a later version |
| Optimization goal | Any of the following types:
- Install   
- In-app event 
-  Value   | `optimization_goal` | Any of the following values: 
- `INSTALL`To use `INSTALL`, you need to ensure third-party tracking has been set up for the selected App. You can use [/app/info/](https://business-api.tiktok.com/portal/docs?id=1740859272887297) to check if third-party tracking (`tracking_url`) has been configured for an App.
-  To add third-party tracking for an existing App, use [/app/update/](https://business-api.tiktok.com/portal/docs?id=1740859300069378). To learn about how to obtain tracking links from a third-party partner, see [Mobile Measurement Partner (MMP) Tracking](https://ads.tiktok.com/help/article/mobile-measurement-partner-mmp-tracking?lang=en).
- `IN_APP_EVENT` (with `optimization_event` specified) To use `IN_APP_EVENT`, you need to ensure the specified event (`optimization_event`) is available for the selected App. You can use [/app/optimization_event/](https://business-api.tiktok.com/portal/docs?id=1740859338750977) to obtain the available optimization events  (`optimization_event`)  for the App.
- `VALUE` (with `optimization_event` specified)  To check whether certain settings are eligible for the Value optimization goal, use [/tool/vbo_status/](https://business-api.tiktok.com/portal/docs?id=1770016073586753).  |
| Bid Strategy | 
- If optimization goal is Install or In-app event, the strategy can be Maximum Delivery or Cost Cap.
-  If optimization goal is Value, the strategy can be Highest value (to spend your budget fully and maximize the value of results) or Minimum ROAS (to keep your average ROAS around or higher than the target ROAS value). | `bid_type`
`conversion_bid_price` 
`deep_bid_type`
`roas_bid`   |
- If `optimization_goal` is `INSTALL` or `IN_APP_EVENT`: Set `bid_type` to `BID_TYPE_CUSTOM` or `BID_TYPE_NO_BID`. Do not pass `deep_bid_type` and `roas_bid`. If `bid_type` is `BID_TYPE_CUSTOM`, pass `conversion_bid_price` at the same time. 
-  If `optimization_goal` is `VALUE`:Set `deep_bid_type` to `VO_MIN_ROAS` or `VO_HIGHEST_VALUE`, and set `bid_type` to `BID_TYPE_NO_BID`. Do not pass `conversion_bid_price`.If you set `deep_bid_type` to `VO_MIN_ROAS`, pass in `roas_bid` at the same time. |
| Select value | When optimization goal is Value and Self Attributing Network (SAN) is used, use any of the following types:
- Purchase value (also known as VBO IAP, which is short for Value-Based Optimization for in-app purchases) 
- Ad revenue value (also known as VBO IAA, which is short for Value-Based Optimization for in-app advertising)  
**Note**: To use Ad revenue value, ensure that the placement is TikTok only or Pangle only. | `optimization_event`
`secondary_optimization_event` | When `optimization_goal` is `VALUE` and at the campaign level `bid_align_type` is `SAN`: 
- If you want to select Purchase value, set `optimization_event` to `ACTIVE_PAY` and set `secondary_optimization_event` to `PURCHASE_ROI`.
- If you want to select Ad revenue value, set `optimization_event` to `AD_REVENUE_VALUE` and do not pass `secondary_optimization_event`.
**Note**: To use Ad revenue value, ensure that `placement_type` is `PLACEMENT_TYPE_NORMAL` and `placements` is `["PLACEMENT_TIKTOK"]` or `["PLACEMENT_PANGLE"]`.
 To retrieve the `bid_align_type` of a campaign, use [/campaign/get/](https://business-api.tiktok.com/portal/docs?id=1739315828649986).|
| Time window of the bid strategy | When optimization goal is Value and Self Attributing Network (SAN) is used, use any of the following types: Day 7 ROAS or Highest Value 
- Day 0 ROAS or Highest Value  | `vbo_window` | When `optimization_goal` is `VALUE` and at the campaign level `bid_align_type` is `SAN`, use any of the following values: 
- `SEVEN_DAYS`
- `ZERO_DAY` 
For example, if you set `deep_bid_type` to `VO_MIN_ROAS`, pass in `roas_bid`, and set `vbo_window` to `ZERO_DAY`, the system will aim to keep your average ROAS of the current day around or higher than the target ROAS value. 

 To retrieve the `bid_align_type` of a campaign, use [/campaign/get/](https://business-api.tiktok.com/portal/docs?id=1739315828649986). 

**Note**: 
- Day 0 or day 7 bidding (`vbo_window` is `ZERO_DAY` or `SEVEN_DAYS`) for **VBO IAP** in Advanced Dedicated Campaign scenarios are currently allowlist-only features. If you would like to access them, please contact your TikTok representative. 
- Day 0 or day 7 bidding (`vbo_window` is `ZERO_DAY` or `SEVEN_DAYS`) for **VBO IAA** in Advanced Dedicated Campaign scenarios are currently allowlist-only features. If you would like to access them, please contact your TikTok representative.|
| Billing event| oCPM|`billing_event`| `OCPM`|
| Delivery Type | 
- If Bid Strategy is set to Cost Cap, you can set Delivery Type to Standard or Accelerated.
- If Bid Strategy is set to Maximum Delivery, Highest Value or Minimum ROAS, you can only set Delivery Type to Standard.  | `pacing` | 
- If `bid_type` is `BID_TYPE_CUSTOM`, you can set `pacing` to `PACING_MODE_SMOOTH` or `PACING_MODE_FAST`.
- If `bid_type` is `BID_TYPE_NO_BID`, you can only set `pacing` to `PACING_MODE_SMOOTH`. |
```

#### Example

Request
```xcodeblock
(code curl http)
curl --location --request POST 'https://business-api.tiktok.com/open_api/v1.3/adgroup/create/' \
--header 'Access-Token: {{Access-Token}}' \
--header 'Content-Type: application/json' \
--data '{
    "advertiser_id": "{{advertiser_id}}",
    "campaign_id": "{{campaign_id}}",
    "adgroup_name": "{{adgroup_nam}}",
    "promotion_type": "APP_IOS",
    "placement_type": "PLACEMENT_TYPE_NORMAL",
    "placements": ["PLACEMENT_TIKTOK"],
    "location_ids": ["6252001"],
    "operating_systems":["IOS"],
    "ios14_targeting": "IOS14_PLUS",
    "min_ios_version": "14.5",
    "budget_mode": "BUDGET_MODE_TOTAL",
    "budget": {{budget}},
    "schedule_type": "SCHEDULE_START_END",
    "schedule_start_time": "{{schedule_start_time}}",
    "schedule_end_time": "{{schedule_end_time}}",
    "optimization_goal": "INSTALL",
    "bid_type": "BID_TYPE_NO_BID",
    "billing_event": "OCPM",
    "pacing": "PACING_MODE_SMOOTH"
}'
(/code)
```

Response
```xcodeblock
(code curl http)
HTTPS/1.1 200 OK
{
    "code": 0,
    "message": "OK",
    "request_id": "{{request_id}}",
    "data": {
        "adgroup_name": "{{adgroup_name}}",
        "adgroup_app_profile_page_state": "OFF",
        "is_new_structure": true,
        "video_download_disabled": false,
        "deep_bid_type": "DEFAULT",
        "engaged_view_attribution_window": "SEVEN_DAYS",
        "optimization_event": "ACTIVE",
        "conversion_bid_price": 0,
        "share_disabled": false,
        "schedule_type": "SCHEDULE_START_END",
        "interest_category_ids": [],
        "isp_ids": [],
        "keywords": null,
        "bid_display_mode": "CPMV",
        "creative_material_mode": "CUSTOM",
        "comment_disabled": false,
        "delivery_mode": null,
        "is_hfss": false,
        "brand_safety_type": "NO_BRAND_SAFETY",
        "audience_ids": [],
        "optimization_goal": "INSTALL",
        "category_id": "0",
        "auto_targeting_enabled": false,
        "promotion_type": "APP_IOS",
        "click_attribution_window": "SEVEN_DAYS",
        "skip_learning_phase": true,
        "ios14_targeting": "IOS14_PLUS",
        "adgroup_app_profile_page_type": "OFF",
        "gender": "GENDER_UNLIMITED",
        "bid_type": "BID_TYPE_NO_BID",
        "purchased_reach": null,
        "network_types": [],
        "frequency": null,
        "attribution_event_count": "ONCE",
        "secondary_status": "ADGROUP_STATUS_CREATE",
        "create_time": "{{create_time}}",
        "inventory_filter_enabled": false,
        "ios14_quota_type": "OCCUPIED",
        "app_type": "APP_IOS",
        "excluded_audience_ids": [],
        "category_exclusion_ids": [],
        "placements": [
            "PLACEMENT_TIKTOK"
        ],
        "smart_interest_behavior_enabled": null,
        "statistic_type": "NONE",
        "pixel_id": null,
        "advertiser_id": "{{advertiser_id}}",
        "operation_status": "ENABLE",
        "billing_event": "OCPM",
        "modify_time": "{{modify_time}}",
        "package": "{{package}}",
        "view_attribution_window": "ONE_DAY",
        "search_result_enabled": true,
        "deep_cpa_bid": 0,
        "campaign_id": "{{campaign_id}}",
        "rf_estimated_frequency": null,
        "next_day_retention": null,
        "age_groups": null,
        "actions": [],
        "scheduled_budget": 0,
        "adgroup_id": "{{adgroup_id}}",
        "location_ids": [
            "6252001"
        ],
        "schedule_infos": null,
        "conversion_window": null,
        "app_download_url": "{{app_download_url}}",
        "feed_type": null,
        "languages": [],
        "device_price_ranges": null,
        "placement_type": "PLACEMENT_TYPE_NORMAL",
        "min_ios_version": "14.5",
        "rf_estimated_cpr": null,
        "schedule_end_time": "{{schedule_end_time}}",
        "budget": {{budget}},
        "interest_keyword_ids": [],
        "operating_systems": [
            "IOS"
        ],
        "brand_safety_partner": null,
        "dayparting": "111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111",
        "frequency_schedule": null,
        "purchased_impression": null,
        "is_smart_performance_campaign": false,
        "rf_purchased_type": null,
        "schedule_start_time": "{{schedule_start_time}}",
        "budget_mode": "BUDGET_MODE_TOTAL",
        "campaign_name": "{{campaign_name}}",
        "app_id": "{{app_id}}",
        "pacing": "PACING_MODE_SMOOTH",
        "bid_price": 0,
        "secondary_optimization_event": null,
        "smart_audience_enabled": null
    }
}
(/code)
```
### 3. Create an ad
Create an ad using [/ad/create/](https://business-api.tiktok.com/portal/docs?id=1739953377508354). 

#### Example

Request
```xcodeblock
(code curl http)
curl --location --request POST 'https://business-api.tiktok.com/open_api/v1.3/ad/create/' \
--header 'Access-Token: {{Access-Token}}' \
--header 'Content-Type: application/json' \
--data '{
    "advertiser_id": "75960823018",
    "adgroup_id": "{{adgroup_id}}",
    "creatives": [{
        "ad_name": "{{ad_name}}",
        "identity_type":"CUSTOMIZED_USER",
        "identity_id":"{{identity_id}}",
        "ad_format": "SINGLE_VIDEO",
        "video_id":"{{video_id}}",
        "image_ids":["{{image_id}}"],
        "ad_text": "{{ad_text}}",
        "call_to_action": "SHOP_NOW",
        "landing_page_url":"{{landing_page_url}}"
    }]
}'
(/code)
```

Response
```xcodeblock
(code curl http)
HTTPS/1.1 200 OK
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
                "music_id": null,
                "image_ids": [
                    "{{image_id}}"
                ],
                "carousel_image_labels": null,
                "call_to_action": "SHOP_NOW",
                "ad_name": "{{ad_name}}",
                "impression_tracking_url": null,
                "tracking_app_id": "{{tracking_app_id}}",
                "landing_page_urls": null,
                "landing_page_url": "",
                "ad_text": "{{ad_text}}",
                "ad_texts": null,
                "click_tracking_url": "{{click_tracking_url}}",
                "brand_safety_vast_url": null,
                "creative_authorized": false,
                "page_id": null,
                "modify_time": "{{modify_time}}",
                "deeplink_type": "NORMAL",
                "tracking_pixel_id": 0,
                "tracking_offline_event_set_ids": [
                    "{{tracking_offline_event_set_id}}",
                    "{{tracking_offline_event_set_id}}"
                ],
                "profile_image_url": "{{profile_image_url}}",
                "identity_id": "{{identity_id}}",
                "creative_type": null,
                "viewability_vast_url": null,
                "card_id": null,
                "viewability_postbid_partner": "UNSET",
                "is_aco": false,
                "display_name": "",
                "identity_type": "CUSTOMIZED_USER",
                "campaign_name": "{{campaign_name}}",
                "optimization_event": "ACTIVE",
                "is_new_structure": true,
                "campaign_id": "{{campaign_id}}",
                "ad_format": "SINGLE_VIDEO",
                "adgroup_name": "{{adgroup_name}}",
                "playable_url": "",
                "deeplink": "",
                "avatar_icon_web_uri": "{{avatar_icon_web_uri}}",
                "video_id": "{{video_id}}",
                "app_name": "{{app_name}}",
                "operation_status": "ENABLE",
                "advertiser_id": "{{advertiser_id}}",
                "adgroup_id": "{{adgroup_id}}",
                "create_time": "{{create_time}}",
                "ad_id": "{{ad_id}}",
                "vast_moat_enabled": false,
                "call_to_action_id": null
            }
        ]
    }
}
(/code)
```
## Steps for creating Smart+ Advanced Dedicated Campaigns
Create a Smart+ Campaign using [/campaign/spc/create/](https://business-api.tiktok.com/portal/docs?id=1767334204047362). Note that the following requirements must be met.

  
| 
    Setting | 
    Requirement | 
    Parameters | 
    How to configure the parameters | 
   |

  
| 
    Advertising objective | 
    App promotion | 
    `objective_type` | 
    `APP_PROMOTION` | 
   |
  
| 
    App promotion type | 
    App install | 
    `app_promotion_type` | 
    `APP_INSTALL` | 
   |
  
| 
    Smart+ Campaign | 
    Enabled.
Campaigns created via `/campaign/spc/create/` are all Smart+ Campaigns. | 
    / | 
    /
 | 
   |
  
| 
    iOS 14 Dedicated Campaign | 
    Enabled | 
    `campaign_type` | 
    `IOS14_CAMPAIGN` | 
   |
  
| 
    `app_id` | 
    Pass the ID of an iOS app that is eligible for Advanced Dedicated Campaigns.

To find eligible apps, use [/app/list/](https://business-api.tiktok.com/portal/docs?id=1740859313270786). The eligible apps should meet the following requirements:
- `platform` is `IOS`
- `advanced_dedicated_campaign_allowed` is `true`**Note**: Getting access to Advanced Dedicated Campaign requires the app to meet certain criteria. If your app is ineligible for Advanced Dedicated Campaign, reach out to your TikTok representative. Your TikTok representative will be able to provide troubleshooting support to help your app get access to Advanced Dedicated Campaign. | 
   |
  
| 
    `campaign_app_profile_page_state` | 
    `ON`, or `OFF` (or not passed) | 
   |
  
| 
    Use advanced dedicated campaign | 
    Enabled | 
    `is_advanced_dedicated_campaign` | 
    `true` | 
   |
  
| 
    SKAN attribution | 
    Enabled or disabled | 
    `disable_skan_campaign` | 
    Any of the following values: 
- `true`: To disable SKAN attribution. The campaign will not be bound by [Dedicated Campaign quota limits](https://business-api.tiktok.com/portal/docs?id=1752256248260610) and you will be able to retrieve [Self Attribution Network (SAN) metrics](https://business-api.tiktok.com/portal/docs?id=1751443967255553#item-link-SAN%20metrics) for the campaign. However, you cannot retrieve [SKAN reporting metrics](https://business-api.tiktok.com/portal/docs?id=1751443967255553#item-link-SKAN%20metrics) for the campaign. Learn more about [SAN integration](https://ads.tiktok.com/help/article/about-self-attribution-transition)
- `false`: To enable SKAN attribution. The campaign will be bound by [Dedicated Campaign quota limits](https://business-api.tiktok.com/portal/docs?id=1752256248260610) and you will be able to retrieve [SKAN metrics](https://business-api.tiktok.com/portal/docs?id=1751443967255553#item-link-SKAN%20metrics) for the campaign.
**Note**: Disabling SKAN attribution for Dedicated Campaigns is currently an allowlist-only feature. If you would like to access it, please contact your TikTok representative. | 
   |
  
| 
    Optimization location
(Promotion type) | 
    iOS App | 
    `promotion_type` | 
    `APP_IOS` | 
   |
  
| 
    Placement | 
    Any of the following types:
- **Automatic Placement**
- **Select Placement** with TikTok placement or Pangle placement or both  | 
    `placement_type`
`placements` | 
    Any of the following configurations:
-  Set `placement_type` to `PLACEMENT_TYPE_AUTOMATIC`
- Set `placement_type` to `PLACEMENT_TYPE_NORMAL`, and only include `PLACEMENT_TIKTOK` or `PLACEMENT_PANGLE` or both in the value of `placements` | 
   |
  
| 
    Optimization goal | 
    Any of the following types: 
-  Install 
-  In-app event 
-  Value  | 
    `optimization_goal` | 
	Any of the following values:
- `INSTALL` To use `INSTALL`, you need to ensure third-party tracking has been set up for the selected App. You can use [/app/info/](https://business-api.tiktok.com/portal/docs?id=1740859272887297) to check if third-party tracking (`tracking_url`) has been configured for an App. 
-  To add third-party tracking for an existing App, use [/app/update/](https://business-api.tiktok.com/portal/docs?id=1740859300069378). To learn about how to obtain tracking links from a third-party partner, see [Mobile Measurement Partner (MMP) Tracking](https://ads.tiktok.com/help/article/mobile-measurement-partner-mmp-tracking?lang=en).
- `IN_APP_EVENT` (with `optimization_event` specified)  To use `IN_APP_EVENT`, you need to ensure the specified event (`optimization_event`) is available for the selected App. You can use [/app/optimization_event/](https://business-api.tiktok.com/portal/docs?id=1740859338750977) to obtain the available optimization events  (`optimization_event`)  for the App.
- `VALUE`  (with `optimization_event` set to `ACTIVE_PAY`  or `AD_REVENUE_VALUE`) To check whether certain settings are eligible for the Value optimization goal, use [/tool/vbo_status/](https://business-api.tiktok.com/portal/docs?id=1770016073586753). | 
   |
  
| 
    Bid Strategy | 
    
        
- If optimization goal is Install or In-app event, the strategy can be Maximum Delivery or Cost Cap.
        
- If optimization goal is Value, the strategy can be Highest value (to spend your budget fully and maximize the value of results) or Minimum ROAS (to keep your average ROAS around or higher than the target ROAS value).
       | 
    `bid_type`
`conversion_bid_price`
`deep_bid_type`
`roas_bid` | 
    
        
- If `optimization_goal` is `INSTALL` or `IN_APP_EVENT`:
          
            Set `bid_type` to `BID_TYPE_CUSTOM` or `BID_TYPE_NO_BID`. Do not pass `deep_bid_type` and `roas_bid`.
              
                If `bid_type` is `BID_TYPE_CUSTOM`, pass `conversion_bid_price` at the same time.
              
            
          
        
        
- If `optimization_goal` is `VALUE`:
          
            Set `deep_bid_type` to `VO_MIN_ROAS` or `VO_HIGHEST_VALUE`, and set `bid_type` to `BID_TYPE_NO_BID`. Do not pass `conversion_bid_price`.
              
                If you set `deep_bid_type` to `VO_MIN_ROAS`, pass in `roas_bid` at the same time.
              
            
          
        
       | 
   |
  
| 
    Select value | 
    
        
- When optimization goal is Value and Self Attributing Network (SAN) is used, use any of the following types:
          
			**Purchase value** (also known as VBO IAP, which is short for Value-Based Optimization for in-app purchases)
			
- **Ad revenue value**  (also known as VBO IAA, which is short for Value-Based Optimization for in-app advertising) Note: To use Ad revenue value, ensure that the placement is TikTok only or TikTok and Pangle.
          
        
       | 
    `optimization_event` | 
    When `optimization_goal` is `VALUE` and `bid_align_type` is `SAN`:
          
            
- If you want to select Purchase value, set `optimization_event` to `ACTIVE_PAY`.
			
- If you want to select Ad revenue value, set `optimization_event` to `AD_REVENUE_VALUE`.
              
**Note**: To use Ad revenue value, ensure that `placement_type` is `PLACEMENT_TYPE_NORMAL` and `placements` is `["PLACEMENT_TIKTOK"]` or `["PLACEMENT_TIKTOK","PLACEMENT_PANGLE"]`.
          
        
To retrieve the `bid_align_type` of a campaign, use [/campaign/get/](https://business-api.tiktok.com/portal/docs?id=1739315828649986). | 
   |
  
| 
    Time window of the bid strategy | 
    
        
- When optimization goal is Value and Self Attributing Network (SAN) is used, use any of the following types:
          
            Day 7 ROAS or Highest Value
            
- Day 0 ROAS or Highest Value
          
        
       | 
    `vbo_window` | 
    
        
- When `optimization_goal` is `VALUE` and `bid_align_type` is `SAN`, use any of the following values:
          
            `SEVEN_DAYS`
            
- `ZERO_DAY`
          
          
For example, if you set `deep_bid_type` to `VO_MIN_ROAS`, pass in `roas_bid`, and set `vbo_window` to `ZERO_DAY`, the system will aim to keep your average ROAS of the current day around or higher than the target ROAS value.
          

To retrieve the `bid_align_type` of a campaign, use [/campaign/get/](https://business-api.tiktok.com/portal/docs?id=1739315828649986).
          

**Note**:
            
              
- Day 0 or day 7 bidding (`vbo_window` is `ZERO_DAY` or `SEVEN_DAYS`) for **VBO IAP** in Advanced Dedicated Campaign scenarios are currently allowlist-only features. If you would like to access them, please contact your TikTok representative.
			  
- Day 0 or day 7 bidding (`vbo_window` is `ZERO_DAY` or `SEVEN_DAYS`) for **VBO IAA** in Advanced Dedicated Campaign scenarios are currently allowlist-only features. If you would like to access them, please contact your TikTok representative.
            
          

        
       | 
   |
  
| 
     Billing event | 
    oCPM | 
    `billing_event` | 
    `OCPM` | 
   |
  
| 
    Delivery Type | 
    
        
- If Bid Strategy is set to Cost Cap, you can set Delivery Type to Standard or Accelerated.
        
- If Bid Strategy is set to Maximum Delivery, Highest Value, or Minimum ROAS, you can only set Delivery Type to Standard.
       | 
    `pacing` | 
    
        
- If `bid_type` is `BID_TYPE_CUSTOM`, you can set `pacing` to `PACING_MODE_SMOOTH` or `PACING_MODE_FAST`.
        
- If `bid_type` is `BID_TYPE_NO_BID`, you can only set `pacing` to `PACING_MODE_SMOOTH`.
       | 
   |

#### Example

Request
```xcodeblock
(code curl http)
curl --location --request POST 'https://business-api.tiktok.com/open_api/v1.3/campaign/spc/create/' \
--header 'Access-Token: {{Access-Token}}' \
--header 'Content-Type: application/json' \
--data '{
    "advertiser_id": "{{advertiser_id}}",
    "objective_type": "APP_PROMOTION",
    "app_promotion_type": "APP_INSTALL",
    "campaign_type": "IOS14_CAMPAIGN",
    "app_id": "{{app_id}}",
    "is_advanced_dedicated_campaign": true,
    "campaign_name": "{{campaign_name}}",
    "promotion_type": "APP_IOS",
    "placement_type": "PLACEMENT_TYPE_NORMAL",
    "placements": [
        "PLACEMENT_TIKTOK"
    ],
    "location_ids": [
        "6252001"
    ],
    "budget_mode": "BUDGET_MODE_DYNAMIC_DAILY_BUDGET",
    "budget": {{budget}},
    "schedule_type": "SCHEDULE_FROM_NOW",
    "schedule_start_time": "{{schedule_start_time}}",
    "schedule_end_time": "{{schedule_end_time}}",
    "optimization_goal": "INSTALL",
    "bid_type": "BID_TYPE_NO_BID",
    "billing_event": "OCPM",
    "identity_type": "CUSTOMIZED_USER",
    "identity_id": "{{identity_id}}",
    "media_info_list": [
        {
            "media_info": {
                "video_info": {
                    "video_id": "{{video_id}}",
                    "file_name": "{{file_name}}"
                },
                "image_info": [
                    {
                        "web_uri": "{{web_uri}}"
                    }
                ]
            }
        }
    ],
    "title_list": [
        {
            "title": "{{title}}"
        }
    ],
    "call_to_action_id": "{{call_to_action_id}}"
}'
(/code)
```

Response
```xcodeblock
(code curl http)
HTTPS/1.1 200 OK
{
    "code": 0,
    "message": "OK",
    "request_id": "{{request_id}}",
    "data": {
        "modify_time": "{{modify_time}}",
        "click_attribution_window": "SEVEN_DAYS",
        "pixel_id": null,
        "campaign_type": "IOS14_CAMPAIGN",
        "page_list": null,
        "is_advanced_dedicated_campaign": true,
        "deep_bid_type": "DEFAULT",
        "call_to_action_id": "{{call_to_action_id}}",
        "placements": [
            "PLACEMENT_TIKTOK"
        ],
        "budget": {{budget}},
        "scheduled_budget": 0,
        "app_id": "{{app_id}}",
        "advertiser_id": "{{advertiser_i}}",
        "conversion_bid_price": null,
        "campaign_id": "{{campaign_id}}",
        "deeplink_type": null,
        "app_promotion_type": "APP_INSTALL",
        "landing_page_urls": null,
        "optimization_goal": "INSTALL",
        "placement_type": "PLACEMENT_TYPE_NORMAL",
        "billing_event": "OCPM",
        "bid_type": "BID_TYPE_NO_BID",
        "budget_mode": "BUDGET_MODE_DYNAMIC_DAILY_BUDGET",
        "click_tracking_url": "{{click_tracking_url}}",
        "view_attribution_window": "ONE_DAY",
        "deeplink": "",
        "bid_price": null,
        "excluded_audience_ids": null,
        "optimization_event": "ACTIVE",
        "schedule_start_time": "{{schedule_start_time}}",
        "identity_id": "{{identity_id}}",
        "video_download_disabled": false,
        "adgroup_secondary_status": "ADGROUP_STATUS_AUDIT",
        "create_time": "{{create_time}}",
        "title_list": [
            {
                "title": "{{title}}"
            }
        ],
        "schedule_end_time": "{{schedule_end_time}}",
        "app_name": "{{app_name}}",
        "operation_status": "ENABLE",
        "gender": "GENDER_UNLIMITED",
        "schedule_type": "SCHEDULE_FROM_NOW",
        "call_to_action_list": [],
        "comment_disabled": false,
        "share_disabled": false,
        "media_info_list": [
            {
                "media_info": {
                    "tiktok_item_id": null,
                    "identity_id": null,
                    "image_info": [
                        {
                            "web_uri": "{{web_uri}}"
                        }
                    ],
                    "video_info": {
                        "video_id": "{{video_id}}",
                        "file_name": "{{file_name}}"
                    },
                    "identity_type": null
                }
            }
        ],
        "campaign_secondary_status": "CAMPAIGN_STATUS_ENABLE",
        "dayparting": "111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111",
        "blocked_pangle_app_ids": null,
        "identity_type": "CUSTOMIZED_USER",
        "app_type": "APP_IOS",
        "card_list": null,
        "special_industries": null,
        "is_smart_performance_campaign": true,
        "campaign_app_profile_page_state": "OFF",
        "skip_learning_phase": true,
        "exclude_age_under_eighteen": true,
        "spc_type": "UNSET",
        "location_ids": [
            "6252001"
        ],
        "engaged_view_attribution_window": "SEVEN_DAYS",
        "languages": [],
        "impression_tracking_url": null,
        "campaign_name": "{{campaign_name}}",
        "attribution_event_count": "ONCE",
        "promotion_website_type": null,
        "promotion_type": "APP_IOS",
        "app_download_url": "{{app_download_url}}",
        "objective_type": "APP_PROMOTION"
    }
}
(/code)
```

## Related docs
- [Create a campaign](https://business-api.tiktok.com/portal/docs?id=1737719523561474) 
- [Dedicated Campaign](https://business-api.tiktok.com/portal/docs?id=1740029173531649) 
- [Smart+ Campaign](https://business-api.tiktok.com/portal/docs?id=1767959274087425)
