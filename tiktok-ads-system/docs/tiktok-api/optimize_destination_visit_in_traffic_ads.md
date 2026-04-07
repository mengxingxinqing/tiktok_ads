# Optimize Destination Visit in Traffic ads

**Doc ID**: 1782086241778690
**Path**: Use Cases/Campaign creation/Create Traffic ads/Optimize Destination Visit in Traffic ads

---

This article walks you through the steps to create a Traffic ad with optimization goal as Destination Visit, sending users to your in-app page or fallback to the website.

# Prerequisite
- The optimization goal Destination Visit is currently an allowlist-only feature. If you would like to access it, please contact your TikTok representative.
- The optimization goal Destination Visit requires deeplinks at the ad level. To learn more about deeplinks, see [Deeplink](https://business-api.tiktok.com/portal/docs?id=1779541971843073).

# Steps
## 1. Create a campaign
Create a campaign using [/campaign/create/](https://ads.tiktok.com/marketing_api/docs?id=1739318962329602). Note that the following requirements must be met.

  
| 
    Setting | 
    Requirement | 
    Parameter | 
    How to configure the parameter | 
   |

  
| 
    Advertising objective | 
    Traffic | 
    `objective_type` | 
    `TRAFFIC` | 
   |
  
| 
    Smart+ Campaign | 
    Disabled

If you are not sure about whether the campaign is Smart+ Campaign, you can use the `is_smart_performance_campaign` field returned from [/campaign/get/](https://ads.tiktok.com/marketing_api/docs?id=1739315828649986) to check. | 
    /
 | 
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

### Example

Request

```xcodeblock
(code curl http)
curl --location 'https://business-api.tiktok.com/open_api/v1.3/campaign/create/' \
--header 'Access-token: {{Access-token}}' \
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
HTTPS/1.1 200 OK
{
    "code": 0,
    "message": "OK",
    "request_id": "{{request_id}}",
    "data": {
        "budget_mode": "BUDGET_MODE_TOTAL",
        "is_search_campaign": false,
        "is_smart_performance_campaign": false,
        "secondary_status": "CAMPAIGN_STATUS_ENABLE",
        "objective": "LANDING_PAGE",
        "campaign_id": "{{campaign_id}}",
        "create_time": "{{create_time}}",
        "campaign_type": "REGULAR_CAMPAIGN",
        "roas_bid": 0.0,
        "is_new_structure": true,
        "deep_bid_type": null,
        "budget": {{budget}},
        "operation_status": "ENABLE",
        "modify_time": "{{modify_time}}",
        "campaign_name": "{{campaign_name}}",
        "objective_type": "TRAFFIC",
        "advertiser_id": "{{advertiser_id}}"
    }
}
(/code)
```

## 2. Create an ad group
Create an ad group using [/adgroup/create/](https://ads.tiktok.com/marketing_api/docs?id=1739499616346114). Note that the following requirements must be met.

``` xtable
| Setting {20%} | Requirement {25%} | Parameter {25%} | How to configure the parameter {30%} |
|---|---|---|
| Optimization location
(Promotion type)   | Android App or iOS App | `promotion_type` | `APP_ANDROID` or `APP_IOS` |
| Optimization event | Unset. 
 The default setting is Destination Visit. | `optimization_event` | `DESTINATION_VISIT` or not passed (recommended) |
| Placements | **Select Placement** with only TikTok placement |  
- `placement_type`
-  `placements` | Set `placement_type` to `PLACEMENT_TYPE_NORMAL`, and set `placements` to ` ["PLACEMENT_TIKTOK"]` |
| Optimization goal | Destination Visit | `optimization_goal` | `DESTINATION_VISIT` |
| Attribution settings | 
-  Attribution window: Unset. 
  The default setting is 7-day click & 1-day view 
-  Event count: Unset.
 The default setting is Once. | 
- `click_attribution_window`
- `view_attribution_window`
- `attribution_event_count` | Not passed. 
 
 
- `click_attribution_window` will default to `SEVEN_DAYS`. 
- `view_attribution_window` will default to `ONE_DAY`.
- `attribution_event_count` will default to `ONCE`. |
| Billing event | oCPM | `billing_event` | `OCPM` |
| Automated Creative Optimization (ACO) & Smart Creative | Disabled | `creative_material_mode` | Not passed |
| Split test | Disabled 
 
Traffic ad groups with optimization goal as Destination Visit cannot be used in [/split_test/create/](https://business-api.tiktok.com/portal/docs?id=1742666471475201) to create split tests. | / | / |
```

### Example
Request
```xcodeblock
(code curl http)
curl --location 'https://business-api.tiktok.com/open_api/v1.3/adgroup/create/' \
--header 'Access-Token: {{Access-Token}}' \
--header 'Content-Type: application/json' \
--data '{
    "advertiser_id": "{{advertiser_id}}",
    "campaign_id": "{{campaign_id}}",
    "adgroup_name": "{{adgroup_name}}",
    "promotion_type": "APP_IOS",
    "app_id": "{{app_id}}",
    "placement_type": "PLACEMENT_TYPE_NORMAL",
    "placements": ["PLACEMENT_TIKTOK"],
    "location_ids": [
        "{{location_id}}"
    ],
    "operating_systems": [
        "IOS"
    ],
    "budget_mode": "BUDGET_MODE_TOTAL",
    "budget": {{budget}},
    "schedule_type": "SCHEDULE_START_END",
    "schedule_start_time": "{{schedule_start_time}}",
    "schedule_end_time": "{{schedule_end_time}}",
    "optimization_goal": "DESTINATION_VISIT",
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
        "attribution_event_count": "ONCE",
        "creative_material_mode": "CUSTOM",
        "statistic_type": null,
        "adgroup_app_profile_page_state": null,
        "auto_targeting_enabled": false,
        "excluded_audience_ids": [],
        "rf_estimated_cpr": null,
        "next_day_retention": null,
        "rf_purchased_type": null,
        "scheduled_budget": 0.0,
        "frequency": null,
        "click_attribution_window": "SEVEN_DAYS",
        "gender": "GENDER_UNLIMITED",
        "deep_bid_type": null,
        "isp_ids": [],
        "deep_cpa_bid": 0.0,
        "interest_keyword_ids": [],
        "schedule_start_time": "{{schedule_start_time}}",
        "package": "{{package}}",
        "app_id": "{{app_id}}",
        "inventory_filter_enabled": false,
        "location_ids": [
            "{{location_id}}"
        ],
        "budget": {{budget}},
        "billing_event": "OCPM",
        "optimization_goal": "DESTINATION_VISIT",
        "ios14_quota_type": "UNOCCUPIED",
        "keywords": null,
        "campaign_id": "{{campaign_id}}",
        "search_result_enabled": true,
        "campaign_name": "{{campaign_name}}",
        "app_type": "APP_IOS",
        "purchased_impression": null,
        "secondary_optimization_event": null,
        "purchased_reach": null,
        "languages": [],
        "comment_disabled": false,
        "is_hfss": false,
        "frequency_schedule": null,
        "schedule_infos": null,
        "actions": [],
        "adgroup_id": "{{adgroup_id}}",
        "pacing": "PACING_MODE_SMOOTH",
        "ios14_targeting": "UNSET",
        "bid_display_mode": "CPMV",
        "device_price_ranges": null,
        "age_groups": null,
        "operating_systems": [
            "IOS"
        ],
        "category_id": "0",
        "conversion_bid_price": 0.0,
        "dayparting": "111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111",
        "network_types": [],
        "conversion_window": null,
        "is_new_structure": true,
        "brand_safety_type": "NO_BRAND_SAFETY",
        "bid_price": 0.0,
        "brand_safety_partner": null,
        "view_attribution_window": "ONE_DAY",
        "advertiser_id": "{{advertiser_id}}",
        "schedule_type": "SCHEDULE_START_END",
        "skip_learning_phase": true,
        "bid_type": "BID_TYPE_NO_BID",
        "interest_category_ids": [],
        "create_time": "{{create_time}}",
        "pixel_id": null,
        "adgroup_name": "{{adgroup_name}}",
        "operation_status": "ENABLE",
        "category_exclusion_ids": [],
        "delivery_mode": null,
        "app_download_url": "{{app_download_url}}",
        "budget_mode": "BUDGET_MODE_TOTAL",
        "placement_type": "PLACEMENT_TYPE_NORMAL",
        "optimization_event": "DESTINATION_VISIT",
        "audience_ids": [],
        "feed_type": null,
        "promotion_type": "APP_IOS",
        "is_smart_performance_campaign": false,
        "rf_estimated_frequency": null,
        "schedule_end_time": "{{schedule_end_time}}",
        "modify_time": "{{modify_time}}",
        "video_download_disabled": false,
        "placements": [
            "PLACEMENT_TIKTOK"
        ],
        "secondary_status": "ADGROUP_STATUS_CREATE",
        "share_disabled": false
    }
}
(/code)
```

## 3. Create an ad
Create an ad using [/ad/create/](https://ads.tiktok.com/marketing_api/docs?id=1739953377508354). Note that the following requirements must be met.

```xtable
| Setting {20%} | Requirement {20%} | Parameter {20%} | How to configure the parameter {40%} |
|---|---|---|---|
| Destination - Deeplink | Any of the following options: 
-  Universal/App link 
-  URL scheme with fallback type | 
- `deeplink_format_type`
-  `deeplink`
-  `fallback_type`
- `landing_page_url`|
-  To specify the deeplink as Universal/App link:  Set `deeplink_format_type` to `UNIVERSAL_OR_APP_LINK`.
-  Set `deeplink` to Apple’s universal link or Android App Link starting with `http://` or `https://`. 
-  Do not pass `fallback_type` and `landing_page_url`.
-  To specify the deeplink as URL scheme and specify fallback type:  Set `deeplink_format_type` to `SCHEME_LINK`.
-  Set `deeplink` to the Custom URL scheme of an App, in the format of `scheme://resource`. For instance, a Custom URL scheme of WhatsApp should follow the format `whatsapp://resource`. 
-  Pass `fallback_type`.  If `fallback_type` is set to `WEBSITE`, specify `landing_page_url` as a website page that you want the users fallback to.
-  If `fallback_type` is set to `APP_INSTALL`, do not pass `landing_page_url`.  |
| Destination - Deeplink type | Non-deferred deeplinks | `deeplink_type` | `NORMAL` or not passed |
| TikTok Instant Page | Disabled | `page_id` | Not passed |
```
### Example

Request
```xcodeblock
(code curl http)
curl --location 'https://business-api.tiktok.com/open_api/v1.3/ad/create/' \
--header 'Access-Token: {{Access-Token}}' \
--header 'Content-Type: application/json' \

--data '{
    "advertiser_id": "{{advertiser_id}}",
    "adgroup_id": "{{adgroup_id}}",
    "creatives": [
        {
            "ad_name": "{{ad_name}}",
            "identity_type": "CUSTOMIZED_USER",
            "identity_id": "{{identity_id}}",
            "ad_format": "SINGLE_VIDEO",
            "video_id": "{{video_id}}",
            "image_ids": [
                "{{image_id}}"
            ],
            "ad_text": "{{ad_text}}",
            "call_to_action": "CONTACT_US",
            "deeplink": "{{deeplink}}",
            "deeplink_type": "NORMAL",
            "deeplink_format_type": "UNIVERSAL_OR_APP_LINK"
        }
    ]
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
                "ad_name": "{{ad_name}}",
                "card_id": null,
                "call_to_action_id": null,
                "profile_image_url": "",
                "fallback_type": "UNSET",
                "creative_authorized": false,
                "vast_moat_enabled": false,
                "deeplink_format_type": "UNIVERSAL_OR_APP_LINK",
                "image_ids": [
                    "{{image_id}}"
                ],
                "is_aco": false,
                "campaign_id": "{{campaign_id}}",
                "video_id": "{{video_id}}",
                "click_tracking_url": null,
                "display_name": "",
                "campaign_name": "{{campaign_name}}",
                "app_name": "{{app_name}}",
                "ad_texts": null,
                "tracking_pixel_id": 0,
                "call_to_action": "CONTACT_US",
                "ad_id": "{{ad_id}}",
                "tracking_app_id": "{{tracking_app_id}}",
                "is_new_structure": true,
                "creative_type": null,
                "identity_type": "CUSTOMIZED_USER",
                "playable_url": "",
                "impression_tracking_url": null,
                "advertiser_id": "{{advertiser_id}}",
                "adgroup_id": "{{adgroup_id}}",
                "landing_page_urls": null,
                "create_time": "{{create_time}}",
                "ad_format": "SINGLE_VIDEO",
                "operation_status": "ENABLE",
                "identity_id": "{{identity_id}}",
                "adgroup_name": "{{adgroup_name}}",
                "viewability_vast_url": null,
                "tracking_offline_event_set_ids": [
                    "{{tracking_offline_event_set_id}}",
                    "{{tracking_offline_event_set_id}}",
                    "{{tracking_offline_event_set_id}}",
                    "{{tracking_offline_event_set_id}}",
                    "{{tracking_offline_event_set_id}}"
                ],
                "viewability_postbid_partner": "UNSET",
                "music_id": null,
                "brand_safety_vast_url": null,
                "optimization_event": "DESTINATION_VISIT",
                "deeplink": "{{deeplink}}",
                "deeplink_type": "NORMAL",
                "page_id": null,
                "brand_safety_postbid_partner": "UNSET",
                "landing_page_url": "",
                "modify_time": "{{modify_time}}",
                "ad_text": "{{ad_text}}",
                "avatar_icon_web_uri": ""
            }
        ]
    }
}
(/code)
```
