# Create a regular Upgraded Smart+ Web Campaign

**Doc ID**: 1847302878676994
**Path**: Use Cases/Campaign creation/Create an Upgraded Smart+ Campaign/Create Upgraded Smart+ Web Campaigns/Create a regular Upgraded Smart+ Web Campaign

---

A regular Upgraded Smart+ Web Campaign is an Upgraded Smart+ Web Campaign that doesn't use catalog products to deliver ads. 

For such campaigns, you can set the parameter `catalog_enabled` to `false` or leave `catalog_enabled` unspecified at the campaign level.

# Steps

## Create a campaign

Create a campaign using [/smart_plus/campaign/create/](https://business-api.tiktok.com/portal/docs?id=1843312852800706). 

Note that the following requirements must be met. To find a complete list of parameters, see [/smart_plus/campaign/create/](https://business-api.tiktok.com/portal/docs?id=1843312852800706).

    
        
| 
            Setting | 
            Requirement | 
            Parameter | 
            How to configure the parameter | 
         |
    
    
    
| 
        Advertising objective | 
        Sales | 
        `objective_type` | 
        `WEB_CONVERSIONS` | 
     |
    
| 
        Sales destination | 
        Website | 
        `sales_destination` | 
        `WEBSITE` | 
     |
    
| 
        iOS 14 dedicated campaign | 
        Disabled | 
        `campaign_type` | 
        `REGULAR_CAMPAIGN` or not specified | 
     |
    
| 
        `app_id` | 
        Not specified | 
     |
    
| 
        `campaign_app_profile_page_state` | 
        Not specified | 
     |
    
| 
        Use catalog | 
        **Disabled**

To use a catalog in your Upgraded Smart+ Web Campaign, see the following sections:
- For using an E-commerce catalog: [Create Upgraded Smart+ E-commerce Catalog Ads](https://business-api.tiktok.com/portal/docs?id=1847302895272962).
- For using a travel (hotel, flight, or destination) catalog: [Create Upgraded Smart+ Travel Ads](https://business-api.tiktok.com/portal/docs?id=1847302908327938).
- For using an entertainment catalog: [Create Upgraded Smart+ Streaming Ads](https://business-api.tiktok.com/portal/docs?id=1847302920924306).
- For using a mini series catalog: [Create Upgraded Smart+ Mini Series Catalog Ads](https://business-api.tiktok.com/portal/docs?id=1847302935967746). | 
        `catalog_enabled` | 
        `false` or not specified | 
     |
    
| 
        Campaign name | 
        Specify a valid name | 
        `campaign_name` | 
        Specify a valid value | 
     |
    
| 
        Special ad categories
(Optional) | 
        Disabled or enabled

**Note**: This setting is only supported for advertisers who are registered in the US or Canada. | 
        `special_industries` | 
        Not specified or specify a valid value | 
     |
     
| 
      Campaign budget strategy | 
      Any of the following types:
- **Automatic campaign budget**: Your budget will be automatically allocated and optimized across ad groups. All ad groups must share the same budget and optimization settings.
- **Custom ad group budget**: Precisely control spend for each ad group, using different budget and optimization settings for each. | 
      `budget_optimize_on` | 
      
- To set an automatic campaign budget, set this field to `true` or leave it unspecified.
- To set a custom ad group budget, set this field to `false`. | 
     |
    
| 
      Campaign budget mode | 
      
- When Campaign budget strategy is Automatic campaign budget, specify any of the following modes:Daily
- Lifetime
- When Campaign budget strategy is Custom ad group budget:Disabled | 
      `budget_mode` | 
      
- When `budget_optimize_on` is `true` or not specified, use any of the following values :`BUDGET_MODE_TOTAL`
- `BUDGET_MODE_DYNAMIC_DAILY_BUDGET`
- When `budget_optimize_on` is `false`:Not specified | 
     |
	
| 
      Automatic budget increase (when Campaign budget strategy is Automatic campaign budget and campaign budget mode is daily) | 
      Any of the following options:
- Enabled
- Disabled | 
      `budget_auto_adjust_strategy` | 
      When `budget_optimize_on` is `true` or not specified and `budget_mode` is `BUDGET_MODE_DYNAMIC_DAILY_BUDGET`:
-  To enable the setting, use the following value:`AUTO_BUDGET_INCREASE`. Allow your budget to automatically increase when your ads are performing well and target CPA, Day 0 target ROAS, and budget requirements are met. Your daily budget will be allowed to automatically increase by 20%, up to 10 times per day, when your budget utilization reaches 90% or more. Your daily budget will reset to your original daily budget each day.
- To disable the setting: Not specified
**Note**: Enabling automatic budget increase is currently an allowlist-only feature. If you would like to access it, please contact your TikTok representative.
 | 
     |
    
| 
      Campaign budget | 
      
- When Campaign budget strategy is Automatic campaign budget, specify a valid budget.
- When Campaign budget strategy is Custom ad group budget:Disabled | 
      `budget` | 
      
- When `budget_optimize_on` is `true` or not specified, specify a valid value.
- When `budget_optimize_on` is `false`:Not specified | 
     |
    

### Example

**Creating a CBO campaign**

Request

```xcodeblock
(code http)
curl --location --request POST 'https://business-api.tiktok.com/open_api/v1.3/smart_plus/campaign/create/' \
--header 'Access-Token: {{Access-Token}}' \
--header 'Content-Type: application/json' \
--data '{
    "advertiser_id": "{{advertiser_id}}",
    "request_id": "{{request_id}}",
    "objective_type": "WEB_CONVERSIONS",
    "sales_destination": "WEBSITE",
    "campaign_name": "{{campaign_name}}",
    "budget": {{budget}}
}'
(/code)
```

Response

```xcodeblock
(code http)
{
    "code": 0,
    "message": "OK",
    "request_id": "{{request_id}}",
    "data": {
        "advertiser_id": "{{advertiser_id}}",
        "budget": {{budget}},
        "budget_mode": "BUDGET_MODE_DYNAMIC_DAILY_BUDGET",
        "budget_optimize_on": true,
        "campaign_id": "{{campaign_id}}",
        "campaign_name": "s++_campaign_web_non_catalog_0723",
        "campaign_type": "REGULAR_CAMPAIGN",
        "create_time": "{{create_time}}",
        "modify_time": "{{modify_time}}",
        "objective_type": "WEB_CONVERSIONS",
        "operation_status": "ENABLE",
        "sales_destination": "WEBSITE",
        "secondary_status": "CAMPAIGN_STATUS_ENABLE",
        "smart_plus_adgroup_mode": "MULTIPLE"
    }
}
(/code)
```

## Create an ad group

Create an ad group using [/smart_plus/adgroup/create/](https://business-api.tiktok.com/portal/docs?id=1843314887930946). 

Note that the following requirements must be met. To find a complete list of parameters, see [/smart_plus/adgroup/create/](https://business-api.tiktok.com/portal/docs?id=1843314887930946).

    
        
| 
            Setting | 
            Requirement | 
            Parameter | 
            How to configure the parameter | 
         |
    
    
        
| 
            Ad group name | 
            Specify a valid name | 
            `adgroup_name` | 
            Specify a valid value | 
         |
        
| 
            Optimization and bidding
· Location | 
            Website | 
            `promotion_type` | 
            `WEBSITE` | 
         |
        
| 
            `promotion_target_type` | 
            Not specified | 
         |
        
| 
            Optimization and bidding
· Goal | 
            Any of the following types:
- Click
- Conversion
- Landing page view
- Value

**Note**: When you select a campaign budget mode, this setting must be the same across ad groups within the same campaign. | 
            `optimization_goal` | 
            Any of the following values:
- `CLICK`
- `CONVERT`
- `TRAFFIC_LANDING_PAGE_VIEW`
- `VALUE`
**Note**: When you select a campaign budget mode, this setting must be the same across ad groups within the same campaign. | 
         |
        
| 
            Optimization and bidding
· Event 
  · Data connection | 
            
- When Goal is Conversion or Value, specify a valid Pixel.
- When Goal is Click or Landing page view, Pixel is not supported. | 
            `pixel_id` | 
            
- Required when `optimization_goal` is set to `CONVERT` or `VALUE`.
- To obtain the list of Pixels within your ad account, use [/pixel/list/](https://business-api.tiktok.com/portal/docs?id=1740858697598978).
- Not supported when `optimization_goal` is set to `CLICK` or `TRAFFIC_LANDING_PAGE_VIEW`. | 
         |
        
| 
            Optimization and bidding
· Event 
  ·· Optimization event | 
            
- Required when Goal is Conversion or Value.
- When Goal is Value, specify the optimization event as Complete Payment.
- When Goal is Conversion, specify any of the following:
- Standard Event
- Custom Conversion
- Not supported when Goal is Click or Landing page view.
**Note**: When you select a campaign budget mode, this setting, if specified, must be the same across ad group within the same campaign. | 
            `optimization_event`
`custom_conversion_id` | 
            
- Required when `optimization_goal` is set to `CONVERT` or `VALUE`.
- When `optimization_goal` is set to `VALUE`, set this field to `SHOPPING`.
- When `optimization_goal` is set to `CONVERT`, specify any of the following:
- A Standard Event through `optimization_event` .To obtain the optimization events that have been configured for a Pixel, use [/pixel/list/](https://business-api.tiktok.com/portal/docs?id=1740858697598978). 
See [Conversion events - Pixel events](https://business-api.tiktok.com/portal/docs?id=1739361474981889#item-link-Pixel%20events) for enum values.
- A Custom Conversion along with the associated conversion event through `custom_conversion_id` and `optimization_event`.To obtain the list of Custom Conversions associated with a Pixel, use [/custom_conversion/list/](https://business-api.tiktok.com/portal/docs?id=1842225174460673).To confirm the eligibility of the Custom Conversion for ad group creation:Ensure the returned `optimization_event` matches the `optimization_event` specified during ad group creation. 
- Ensure the `activity_status` is `NO_RECENT_ACTIVITY` or `ACTIVE`.
- Not supported when `optimization_goal` is set to `CLICK`.
- Can be omitted when `optimization_goal` is set to `TRAFFIC_LANDING_PAGE_VIEW`. Then `optimization_event` will default to `LANDING_PAGE_VIEW`.
**Note**: When`budget_optimize_on` is `true` at the campaign level, the `optimization_event` and `custom_conversion_id`, if specified, must be the same for ad groups within the same campaign. | 
         |
        
| 
            Optimization and bidding
· Bid Strategy, 
(Optional) Target CPA, 
and (Optional) Target ROAS | 
            
- If Goal is Click, Conversion, or Landing page view, the strategy can be Maximum Delivery or Cost Cap.
- For Cost Cap, you need to specify a Target CPA at the same time.
- If Goal is Value, the strategy can be Highest value or Minimum ROAS.
- For Minimum ROAS, you need to specify a Target ROAS at the same time.
**Note**: 
- The bid strategy must be the same across ad groups within the same campaign.
- When you select a campaign budget mode, the Target CPA or Target ROAS, if specified, must be the same across ad groups within the same campaign.
- Target CPA or Target ROAS is only available when your campaign or ad group budget mode is set to daily. | 
            `bid_type`
`bid_price`
`conversion_bid_price`
`deep_bid_type`
`roas_bid` | 
            
- If `optimization_goal` is `CLICK`, `CONVERT`, or `TRAFFIC_LANDING_PAGE_VIEW`:
- Set `bid_type` to `BID_TYPE_CUSTOM` or `BID_TYPE_NO_BID`. Do not specify`deep_bid_type` and `roas_bid`.
- If `optimization_goal` is `CONVERT` or `TRAFFIC_LANDING_PAGE_VIEW` and `bid_type` is `BID_TYPE_CUSTOM`, specify `conversion_bid_price` at the same time.
- If `optimization_goal` is `CLICK`, and `bid_type` is `BID_TYPE_CUSTOM`, specify `bid_price` at the same time.
- If `optimization_goal` is `VALUE`, set `deep_bid_type` to `VO_HIGHEST_VALUE` or `VO_MIN_ROAS`, and set `bid_type` to `BID_TYPE_NO_BID`. Do not specify`conversion_bid_price` and `bid_price`.
- If you set `deep_bid_type` to `VO_MIN_ROAS`, specify `roas_bid` at the same time.
**Note**: 
- The `bid_type` must be the same across ad groups within the same campaign.
- When`budget_optimize_on` is `true` at the campaign level, the following settings, if specified, must be the same for ad groups within the same campaign:
- `conversion_bid_price`
- `bid_price`
- `deep_bid_type`
- `roas_bid`
- You can only set `bid_type` to `BID_TYPE_CUSTOM` or `deep_bid_type` to `VO_MIN_ROAS` in any of the following scenarios:
- At the campaign level, `budget_mode` is `BUDGET_MODE_DYNAMIC_DAILY_BUDGET` 
- At the ad group level, `budget_mode` is `BUDGET_MODE_DYNAMIC_DAILY_BUDGET` | 
         |
        
| 
            Optimization and bidding
· Attribution settings | 
            Select from the supported attribution setting options for the specific scenario. | 
            
- `click_attribution_window`
- `view_attribution_window`
- `engaged_view_attribution_window`
- `attribution_event_count` | 
            To learn about the supported attribution setting options for different scenarios, see [Attribution window and event count - Website conversions](https://business-api.tiktok.com/portal/docs?id=1777694366654465#item-link-Website%20conversions). | 
         |
        
| 
            Optimization and bidding
· Billing event | 
            
- If Goal is Click, the billing event should be CPC.
- If Goal is Conversion, Landing page view, or Value, the billing event should be oCPM.
**Note**: When you select a campaign budget mode, the billing event must be the same across ad groups within the same campaign. | 
            `billing_event` | 
            
- If `optimization_goal` is `CLICK`, set this field to `CPC`.
- If `optimization_goal` is `CONVERT`, `TRAFFIC_LANDING_PAGE_VIEW`, or `VALUE`, set this field to `OCPM`.
**Note**: When`budget_optimize_on` is `true` at the campaign level, specify the same `billing_event`for ad groups within the same campaign. | 
         |
        
| 
            Optimization and bidding
· Delivery Type | 
            Standard (default) | 
            N/A | 
            By default, the Delivery Type for the Upgraded Smart+ Campaign is Standard. | 
         |
        
| 
            Budget and schedule
· Budget | 
            
- When you select a campaign budget mode:
- The ad group budget is disabled. The campaign-level budget will be used as the ad group budget.
- When you select an ad group budget strategy, you can use any of the following ad group budget modes:
- Lifetime
- Daily
**Note**: The ad group budget mode, if specified, must be the same across ad groups within the same campaign. | 
            `budget_mode`
`budget` | 
            
- When `budget_optimize_on` is `true` at the campaign level, `budget_mode` and `budget`are not supported.
- When `budget_optimize_on` is `false` at the campaign level:
- Set `budget_mode` to `BUDGET_MODE_TOTAL` or `BUDGET_MODE_DYNAMIC_DAILY_BUDGET`
- Specify a valid budget via `budget`
**Note**: The `budget_mode`, if specified, must be the same across ad groups within the same campaign. | 
         |
	    
| 
            Budget and schedule 
· Automatic budget increase (when Goal is Value) | 
            Enabled or disabled

To enable this setting, the following conditions should be met:
- At the campaign level: CBO is disabled.
- At the ad group level:Ad group budget is Daily
- Goal is Value
- Bid Strategy is Target ROAS
- Time window of the bid strategy is Day 0 ROAS | 
            `budget_auto_adjust_strategy` | 
            Use any of the following values:
- `AUTO_BUDGET_INCREASE`: To enable automatic budget increase. Allow your budget to automatically increase when your ads are performing well and target CPA, Day 0 target ROAS, and budget requirements are met. Your daily budget will be allowed to automatically increase by 20%, up to 10 times per day, when your budget utilization reaches 90% or more. Your daily budget will reset to your original daily budget each day.
- `UNSET`: To disable automatic budget increase.
You can only set this field to `AUTO_BUDGET_INCREASE` when the following conditions are all met:
- At the campaign level: `budget_optimize_on` is `false`.
- At the ad group level:`budget_mode` is `BUDGET_MODE_DYNAMIC_DAILY_BUDGET`.
- `optimization_goal` is `VALUE`.
- `deep_bid_type` is `VO_MIN_ROAS`.
- `vbo_window` is `ZERO_DAY`.
**Note**: Enabling automatic budget increase is currently an allowlist-only feature. If you would like to access it, please contact your TikTok representative.
 | 
         |
        
| 
            Budget and schedule
· Add spend target per ad group
  · Daily minimum | 
            
- When you use a lifetime campaign budget, you can enable or disable this setting.
- When you use a daily campaign budget or an ad group budget, this setting is not supported. | 
            `min_budget` | 
            
- When `budget_optimize_on` is `true` and `budget_mode` is `BUDGET_MODE_TOTAL` at the campaign level, you can either specify a valid value through this field or leave it unspecified.
- When `budget_optimize_on` is `true` and `budget_mode` is `BUDGET_MODE_DYNAMIC_DAILY_BUDGET` or when `budget_optimize_on` is `false` at the campaign level, this field is not supported. | 
         |
    
| 
        Budget and schedule
· Schedule | 
        Any of the following types:
- Set start time and run ad group continuously
- Set start and end time
**Note**: You can only choose "Set start time and run ad group continuously" in any of the following scenarios: 
- At the campaign level, a daily campaign budget is set.
- At the ad group level, a daily ad group budget is set. | 
        `schedule_type`
`schedule_start_time`
`schedule_end_time` | 
        
- To set start time and run the ad group continuously, set `schedule_type` to `SCHEDULE_FROM_NOW` and specify `schedule_start_time`. Do not specify `schedule_end_time`.
- To run the ad group between the scheduled start time and end time, set `schedule_type` to `SCHEDULE_START_END` and specify both `schedule_start_time` and `schedule_end_time`.**Note**: You can only set `schedule_type` to `SCHEDULE_FROM_NOW` in any of the following scenarios: 
- At the campaign level, `budget_mode` is `BUDGET_MODE_DYNAMIC_DAILY_BUDGET`
- At the ad group level, `budget_mode` is `BUDGET_MODE_DYNAMIC_DAILY_BUDGET` | 
     |
    
| 
        Budget and schedule
· Dayparting (Optional) | 
        Any of the following types:
- All day (default)
- Select specific time | 
        `dayparting` | 
        Any of the following configurations:
- Specify an all-1 value, or do not specify this field
- Specify a value that contains 0 to indicate non-delivery | 
     |
    
| 
        Audience targeting optimization mode | 
        Any of the following modes:
- **Automatic targeting**
- You can use automatic targeting to leverage real-time data and machine learning to target audiences most likely to engage with your ads.
- **Custom targeting**
- You can use custom targeting settings to precisely control who sees your ads. This may limit delivery and impact campaign performance.
To learn about the supported targeting settings for each mode, see [Available targeting settings for different targeting optimization modes](https://business-api.tiktok.com/portal/docs?id=1847839827327106). | 
        `targeting_optimization_mode` | 
        Any of the following values:
- `AUTOMATIC`
- `MANUAL`
To learn about the supported targeting settings for each mode, see [Available targeting settings for different targeting optimization modes](https://business-api.tiktok.com/portal/docs?id=1847839827327106). | 
     |
    
| 
        Placements and brand safety
· Placement | 
        Any of the following types:
- **Automatic Placement**
- **Select specific placements**:
- TikTok
- Global App Bundle
- Pangle | 
        `placement_type`
`placements` | 
        
- To use Automatic Placement, do not specify `placement_type` and `placements`.
- The system will automatically configure placements for your Upgraded Smart+ Ad Groups based on your other settings and select high-quality traffic from various placements to deliver better results. If provided, the parameters `placement_type` and `placements` will be ignored.
- To retrieve the exact placement setting of an Upgraded Smart+ Ad Group, use [/smart_plus/adgroup/get/](https://business-api.tiktok.com/portal/docs?id=1843314879617026).
- To use specific placements, set `placement_type` to `PLACEMENT_TYPE_NORMAL` and specify one or more of the following placements in `placements`:
- `PLACEMENT_TIKTOK`
- `PLACEMENT_PANGLE`
- `PLACEMENT_GLOBAL_APP_BUNDLE` | 
     |
    
| 
        Placements and brand safety
· Brand safety and suitability | 
        These settings only apply to **TikTok in-feed** and **search feed** ads. Any previous account-level settings in the brand safety hub will apply to your campaign. | 
        N/A | 
        N/A

To retrieve the ad account-level brand safety and suitability settings in the brand safety hub, use [/tiktok_inventory_filters/get/](https://business-api.tiktok.com/portal/docs?id=1830112550443073).
To configure or update the ad account-level brand safety and suitability settings in the brand safety hub, use [/tiktok_inventory_filters/update/](https://business-api.tiktok.com/portal/docs?id=1830112569774274). | 
     |
    
| 
        Placements and brand safety
· User comment | 
        Enabled or disabled | 
        `comment_disabled` | 
        Specify valid values or not specified | 
     |
    
| 
        Placements and brand safety
· Allow video download | 
        Enabled or disabled | 
        `share_disabled` | 
        Specify valid values or not specified | 
     |
    
| 
        Placements and brand safety
· Allow video sharing | 
        Enabled or disabled | 
        `video_download_disabled` | 
        Specify valid values or not specified | 
     |
    
| 
        Placements and brand safety
· Pangle block list | 
        Disabled | 
        N/A | 
        N/A | 
     |

### Example

Request

```xcodeblock
(code http)
curl --location --request POST 'https://business-api.tiktok.com/open_api/v1.3/smart_plus/adgroup/create/' \
--header 'Access-Token: {{Access-Token}}' \
--header 'Content-Type: application/json' \
--data '{
    "advertiser_id": "{{advertiser_id}}",
    "campaign_id": "{{campaign_id}}",
    "request_id": "{{request_id}}",
    "adgroup_name": "{{adgroup_name}}",
    "promotion_type": "WEBSITE",
    "optimization_goal": "CONVERT",
    "pixel_id": "{{pixel_id}}",
    "optimization_event": "ADD_BILLING",
    "bid_type": "BID_TYPE_CUSTOM",
    "conversion_bid_price": {{conversion_bid_price}},
    "billing_event": "OCPM",
    "schedule_type": "SCHEDULE_START_END",
    "schedule_start_time": "{{schedule_start_time}}",
    "schedule_end_time": "{{schedule_end_time}}",
    "targeting_spec": {
        "location_ids": [
            "1562822"
        ]
    }
}'
(/code)
```

Response

```xcodeblock
(code http)
{
    "code": 0,
    "message": "OK",
    "request_id": "{{request_id}}",
    "data": {
        "adgroup_id": "{{adgroup_id}}",
        "adgroup_name": "{{adgroup_name}}",
        "advertiser_id": "{{advertiser_id}}",
        "attribution_event_count": "EVERY",
        "bid_type": "BID_TYPE_CUSTOM",
        "billing_event": "OCPM",
        "campaign_id": "{{campaign_id}}",
        "campaign_name": "{{campaign_name}}",
        "click_attribution_window": "SEVEN_DAYS",
        "comment_disabled": false,
        "conversion_bid_price": {{conversion_bid_price}},
        "create_time": "{{create_time}}",
        "dayparting": "111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111",
        "modify_time": "{{modify_time}}",
        "optimization_event": "ADD_BILLING",
        "optimization_goal": "CONVERT",
        "pixel_id": "{{pixel_id}}",
        "placement_type": "PLACEMENT_TYPE_AUTOMATIC",
        "placements": [
            "PLACEMENT_TIKTOK",
            "PLACEMENT_GLOBAL_APP_BUNDLE",
            "PLACEMENT_PANGLE"
        ],
        "product_source": "UNSET",
        "promotion_type": "WEBSITE",
        "promotion_website_type": "UNSET",
        "schedule_end_time": "{{schedule_end_time}}",
        "schedule_start_time": "{{schedule_start_time}}",
        "schedule_type": "SCHEDULE_START_END",
        "search_result_enabled": true,
        "secondary_status": "ADGROUP_STATUS_CREATE",
        "share_disabled": false,
        "skip_learning_phase": true,
        "targeting_optimization_mode": "AUTOMATIC",
        "targeting_spec": {
            "age_groups": [
                "AGE_18_24",
                "AGE_25_34",
                "AGE_35_44",
                "AGE_45_54",
                "AGE_55_100"
            ],
            "brand_safety_type": "EXPANDED_INVENTORY",
            "gender": "GENDER_UNLIMITED",
            "location_ids": [
                "1562822"
            ],
            "spc_audience_age": "OVER_EIGHTEEN"
        },
        "video_download_disabled": false,
        "view_attribution_window": "ONE_DAY"
    }
}
(/code)
```

## Create an ad

Create an ad using [/smart_plus/ad/create/](https://business-api.tiktok.com/portal/docs?id=1843317390059522). 

Note that the following requirements must be met. To find a complete list of parameters, see [/smart_plus/ad/create/](https://business-api.tiktok.com/portal/docs?id=1843317390059522).

    
        
| 
            Setting | 
            Requirement | 
            Parameter | 
            How to configure the parameter | 
         |
    
    
        
| 
            Ad name
(Optional) | 
            By default, the system will auto-generate the ad name.
You can customize the ad name by specifying a valid ad name. | 
            `ad_name` | 
            
- To have the system auto-generate the ad name, set this field to `""`(empty string).
- To customize the ad name, specify a non-empty string value. | 
         |
        
| 
            Destination URL | 
            Enabled | 
            `landing_page_url_list` | 
            Provide one URL of the landing page or website you want to promote. The link should match the data connection you specified in the ad group. | 
         |
        
| 
            `page_list` | 
            Not specified | 
         |
        
| 
            UTM parameters
(Optional) | 
            Enabled or disabled | 
            `utm_params` | 
            Specify valid values or not specified.

If you set `landing_page_url_list` to a URL that already includes URL parameters, you can optionally specify `utm_params` at the same time to store the URL parameters used in the URL.
In such cases, you need to ensure that `utm_params` exactly matches the used URL parameters. The URL parameters will not be automatically appended to the `landing_page_url_list` upon ad delivery. | 
         |
        
| 
            Creative assets 
· Identity | 
            Any of the following options:
- Custom User (custom identity)
- Authorized User
- TikTok User
- TikTok Account User in Business Center | 
            `identity_type` | 
            Any of the following values:
- `CUSTOMIZED_USER`
- `AUTH_CODE`
- `TT_USER`
- `BC_AUTH_TT`
**Note**:
- For non-Spark Ads identities (`CUSTOMIZED_USER`), specify values to `identity_type` and `identity_id` in the `ad_configuration` object.
- For Spark Ads identities, specify values to `identity_type` and `identity_id` within the `creative_info` object. | 
         |
        
| 
            `identity_id` | 
            Specify a valid value
To get the list of identities under your ad account, use [/identity/get/](https://business-api.tiktok.com/portal/docs?id=1740218420781057). | 
         |
        
| 
            `identity_authorized_bc_id` | 
            Specify a valid value when `identity_type` is `BC_AUTH_TT` | 
         |
        
| 
            Creative assets 
· Ad creatives & Ad text | 
            For a single ad, you can include one to **50 ad creatives** that can consist of the following types:
- Videos
- TikTok video posts
- TikTok photo posts
- Carousel
To learn about the combination of available ad creatives based on identity type, see [Ad creative combinations by identity and ad type](https://business-api.tiktok.com/portal/docs?id=1847839781968897). | 
            `ad_format` | 
            Specify a valid value | 
         |
        
| 
            `creative_list`
`video_info`
`image_info`
`music_info`
`ad_text_list`
`tiktok_item_id` | 
            Specify one to 50 ad creatives through `creative_list`. The ad creatives can be any of the following:
- Videos
- TikTok video posts
- TikTok photo posts
- Carousel
To learn about configurations of the available ad creative combinations based on identity type, see [Ad creative combinations by identity and ad type](https://business-api.tiktok.com/portal/docs?id=1847839781968897). | 
         |
        
| 
            Add product and service information
(Optional) | 
            Disabled | 
            N/A | 
            N/A | 
         |
    
| 
      Disclaimer 
(Optional) | 
      Enabled or disabled | 
      `disclaimer` | 
      Specify a valid value or not specified | 
     |
        
| 
            Call to action | 
            Any of the following options:
- Dynamic
- Standard
**Note**: When you use a Spark Ads identity, you can only use dynamic call to action. | 
            `call_to_action_id`
`call_to_action_list` | 
            
- To use dynamic call to action, specify `call_to_action_id`.
- To use standard call to action, specify `call_to_action_list`.
**Note**: If you set `identity_type` within the `creative_info` object to `TT_USER`, `BC_AUTH_TT`, or `AUTH_CODE`, `call_to_action_id` is required. | 
         |
        
| 
            Interactive add-ons | 
            Disabled | 
            `interactive_add_on_list` | 
            Not specified | 
         |
        
| 
            Tracking
· TikTok events tracking
  · App events
 (Optional) | 
            Enabled or disabled | 
            `tracking_app_id` | 
            Specify a valid value or not specified | 
         |
        
| 
            Tracking
· Third-party tracking settings
  · Impression tracking URL
 (Optional) | 
            Enabled or disabled | 
            `impression_tracking_url` | 
            Specify a valid value or not specified | 
         |
        
| 
            Tracking
· Third-party tracking settings
  · Click tracking URL 
 (Optional) | 
            Enabled or disabled | 
            `click_tracking_url` | 
            Specify a valid value or not specified | 
         |
    

### Example

Request

```xcodeblock
(code http)
curl --location --request POST 'https://business-api.tiktok.com/open_api/v1.3/smart_plus/ad/create/' \
--header 'Access-Token: {{Access-Token}}' \
--header 'Content-Type: application/json' \
--data '{
    "advertiser_id": "{{advertiser_id}}",
    "adgroup_id": "{{adgroup_id}}",
    "ad_name": "{{ad_name}}",
    "landing_page_url_list": [
        {
            "landing_page_url": "{{landing_page_url}}"
        }
    ],
    "creative_list": [
        {
            "creative_info": {
                "ad_format":"CAROUSEL_ADS",
                "image_info": [
                    {
                        "web_uri": "{{web_uri}}"
                    }
                ],
                "music_info": {
                    "music_id": "{{music_id}}"
                },
                "identity_type": "TT_USER",
                "identity_id": "{{identity_id}}"
            }
        },
        {
            "creative_info": {
                "ad_format":"SINGLE_VIDEO",
                "video_info": {
                    "video_id": "{{video_id}}"
                },
                "image_info": [
                    {
                        "web_uri": "{{web_uri}}"
                    }
                ],
                "identity_type": "TT_USER",
                "identity_id": "{{identity_id}}"
            }
        },
        {
            "creative_info": {
                "ad_format":"SINGLE_VIDEO",
                "tiktok_item_id": "{{tiktok_item_id}}",
                "identity_type": "TT_USER",
                "identity_id": "{{identity_id}}"
            }
        },
        {
            "creative_info": {
                "ad_format":"SINGLE_VIDEO",
                "tiktok_item_id": "{{tiktok_item_id}}",
                "identity_type": "BC_AUTH_TT",
                "identity_id": "{{identity_id}}",
                "identity_authorized_bc_id": "{{identity_authorized_bc_id}}"
            }
        },
        {
            "creative_info": {
                "ad_format":"SINGLE_VIDEO",
                "tiktok_item_id": "{{tiktok_item_id}}",
                "identity_type": "AUTH_CODE",
                "identity_id": "{{identity_id}}"
            }
        }
    ],
    "ad_text_list": [
        {
            "ad_text": "{{ad_text}}"
        },
        {
            "ad_text": "{{ad_text}}"
        },
        {
            "ad_text": "{{ad_text}}"
        },
        {
            "ad_text": "{{ad_text}}"
        },
        {
            "ad_text": "{{ad_text}}"
        }
    ],
    "ad_configuration": {
        "utm_params": [
            {
                "key": "{{key}}",
                "value": "{{value}}"
            }
        ],
        "call_to_action_id": "{{call_to_action_id}}"
    }
}'
(/code)
```

Response

```xcodeblock
(code http)
{
    "code": 0,
    "message": "OK",
    "request_id": "{{request_id}}",
    "data": {
        "ad_configuration": {
            "call_to_action_id": "{{call_to_action_id}}",
            "tracking_info": {},
            "utm_params": [
                {
                    "key": "{{key}}",
                    "value": "{{value}}"
                }
            ]
        },
        "ad_name": "{{ad_name}}",
        "ad_text_list": [
            {
                "ad_text": "{{ad_text}}"
            },
            {
                "ad_text": "{{ad_text}}"
            },
            {
                "ad_text": "{{ad_text}}"
            },
            {
                "ad_text": "{{ad_text}}"
            },
            {
                "ad_text": "{{ad_text}}"
            }
        ],
        "adgroup_id": "{{adgroup_id}}",
        "adgroup_name": "{{adgroup_name}}",
        "advertiser_id": "{{advertiser_id}}",
        "call_to_action_list": [],
        "campaign_id": "{{campaign_id}}",
        "campaign_name": "{{campaign_name}}",
        "create_time": "{{create_time}}",
        "creative_list": [
            {
                "ad_material_id": "{{ad_material_id}}",
                "creative_info": {
                    "ad_format":"SINGLE_VIDEO",
                    "identity_authorized_bc_id": "0",
                    "identity_id": "{{identity_id}}",
                    "identity_type": "TT_USER",
                    "image_info": [
                        {
                            "web_uri": "{{web_uri}}"
                        }
                    ],
                    "material_name": "",
                    "video_info": {
                        "file_name": "",
                        "video_id": "{{video_id}}"
                    }
                },
                "material_operation_status": "ENABLE"
            },
            {
                "ad_material_id": "{{ad_material_id}}",
                "creative_info": {
                    "ad_format":"SINGLE_VIDEO",
                    "identity_authorized_bc_id": "0",
                    "identity_id": "{{identity_id}}",
                    "identity_type": "TT_USER",
                    "tiktok_item_id": "{{tiktok_item_id}}"
                },
                "material_operation_status": "ENABLE"
            },
            {
                "ad_material_id": "{{ad_material_id}}",
                "creative_info": {
                    "ad_format":"SINGLE_VIDEO",
                    "identity_authorized_bc_id": "{{identity_authorized_bc_id}}",
                    "identity_id": "{{identity_id}}",
                    "identity_type": "BC_AUTH_TT",
                    "tiktok_item_id": "{{tiktok_item_id}}"
                },
                "material_operation_status": "ENABLE"
            },
            {
                "ad_material_id": "{{ad_material_id}}",
                "creative_info": {
                    "ad_format":"CAROUSEL_ADS",
                    "identity_authorized_bc_id": "0",
                    "identity_id": "{{identity_id}}",
                    "identity_type": "TT_USER",
                    "image_info": [
                        {
                            "web_uri": "{{web_uri}}"
                        }
                    ],
                    "material_name": "{{material_name}}",
                    "music_info": {
                        "music_id": "{{music_id}}"
                    }
                },
                "material_operation_status": "ENABLE"
            },
            {
                "ad_material_id": "{{ad_material_id}}",
                "creative_info": {
                    "ad_format":"SINGLE_VIDEO",
                    "identity_authorized_bc_id": "0",
                    "identity_id": "{{identity_id}}",
                    "identity_type": "AUTH_CODE",
                    "tiktok_item_id": "{{tiktok_item_id}}"
                },
                "material_operation_status": "ENABLE"
            }
        ],
        "deeplink_list": [],
        "interactive_add_on_list": [],
        "landing_page_url_list": [
            {
                "landing_page_url": "{{landing_page_url}}"
            }
        ],
        "modify_time": "{{modify_time}}",
        "operation_status": "ENABLE",
        "page_list": [],
        "secondary_status": "AD_STATUS_AUDIT",
        "smart_plus_ad_id": "{{smart_plus_ad_id}}"
    }
}
(/code)
```
