# Create an Upgraded Smart+ Minis Campaign

**Doc ID**: 1853377811982657
**Path**: Use Cases/Campaign creation/Create an Upgraded Smart+ Campaign/Create Upgraded Smart+ App Campaigns/Create an Upgraded Smart+ Minis Campaign

---

This article walks you through the steps to create an Upgraded Smart+ Minis Campaign.

Based on your preference for using a catalog to promote TikTok Minis, you can create Upgraded Smart+ Minis Non-Catalog Campaigns or Upgraded Smart+ Minis Catalog Campaigns. For detailed instructions on creating each type, refer to their respective sections: "[Create an Upgraded Smart+ Minis Non-Catalog Campaign](#item-link-Create an Upgraded Smart+ Minis Non-Catalog Campaign)" and "[Create an Upgraded Smart+ Minis Catalog Campaign](#item-link-Create an Upgraded Smart+ Minis Catalog Campaign)".

# Create an Upgraded Smart+ Minis Non-Catalog Campaign
An Upgraded Smart+ Minis Non-Catalog Campaign is an Upgraded Smart+ App Campaign promoting a TikTok Minis without using a mini series catalog. 

## Steps
### Create a campaign
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
      App promotion | 
      `objective_type` | 
      `APP_PROMOTION` | 
     |
    
| 
      App promotion type | 
      TikTok Minis | 
      `app_promotion_type` | 
      `MINIS` | 
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

To create an Upgraded Smart+ Minis Campaign using a mini series catalog, see [Create an Upgraded Smart+ Minis Catalog Campaign](#item-link-Create an Upgraded Smart+ Minis Catalog Campaign). | 
      `catalog_enabled` | 
      `false` | 
     |
    
| 
      Campaign name | 
      Specify a valid name | 
      `campaign_name` | 
      Specify a valid value | 
     |
    
| 
        Campaign budget strategy | 
        Any of the following types:
- **Campaign budget**: Your budget will be automatically allocated and optimized across ad groups. All ad groups must share the same budget and optimization settings.
- **Ad group budget**: Precisely control spend for each ad group, using different budget and optimization settings for each. | 
        `budget_optimize_on` | 
        
- To set a campaign budget, set this field to `true` or leave it unspecified.
- To set an ad group budget, set this field to `false`. | 
     |
	
| 
        Campaign budget mode | 
        
- When Campaign budget strategy is Campaign budget, specify any of the following modes:Daily
- Lifetime
- When Campaign budget strategy is Ad group budget, specify any of the following modes to determine the budget limit for all ad groups:No limit
- Daily
- Lifetime | 
        `budget_mode` | 
        
- When `budget_optimize_on` is `true` or not specified, use any of the following values:`BUDGET_MODE_TOTAL`
- `BUDGET_MODE_DYNAMIC_DAILY_BUDGET`
- When `budget_optimize_on` is `false`, use any of the following values:`BUDGET_MODE_INFINITE`
- `BUDGET_MODE_DAY`
- `BUDGET_MODE_TOTAL` | 
	 |
	
| 
        Campaign budget | 
        
- When Campaign budget strategy is Campaign budget:Specify a valid budget.
- When Campaign budget strategy is Ad group budget:If the budget limit is No limit:Disabled
- If the budget limit is Daily or Lifetime limit:Specify a valid budget | 
        `budget` | 
        
- When `budget_optimize_on` is `true` or not specified:Specify a valid value.
- When `budget_optimize_on` is `false`:If `budget_mode` is `BUDGET_MODE_INFINITE`:Not specified
- If `budget_mode` is `BUDGET_MODE_DAY` or `BUDGET_MODE_TOTAL`:Specify a valid value | 
     |
    
| 
      PO number (Optional) | 
      Enabled or disabled | 
      `po_number` | 
      Specify valid values or not specified | 
     |
  

#### Example
Request
```xcodeblock
(code curl http)
curl --location --request POST 'https://business-api.tiktok.com/open_api/v1.3/smart_plus/campaign/create/' \
--header 'Access-Token: {{Access-Token}}' \
--header 'Content-Type: application/json' \
--data '{
    "advertiser_id": "{{advertiser_id}}",
    "request_id": "{{request_id}}",
    "objective_type": "APP_PROMOTION",
    "app_promotion_type": "MINIS",
    "campaign_type": "REGULAR_CAMPAIGN",
    "catalog_enabled": false,
    "campaign_name": "{{campaign_name}}",
    "budget_optimize_on": true,
    "budget_mode": "BUDGET_MODE_DYNAMIC_DAILY_BUDGET",
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
        "advertiser_id": "{{advertiser_id}}",
        "app_promotion_type": "MINIS",
        "budget": {{budget}},
        "budget_mode": "BUDGET_MODE_DYNAMIC_DAILY_BUDGET",
        "budget_optimize_on": true,
        "campaign_id": "{{campaign_id}}",
        "campaign_name": "{{campaign_name}}",
        "campaign_type": "REGULAR_CAMPAIGN",
        "create_time": "{{create_time}}",
        "modify_time": "{{modify_time}}",
        "objective_type": "APP_PROMOTION",
        "operation_status": "ENABLE",
        "secondary_status": "CAMPAIGN_STATUS_ENABLE",
        "smart_plus_adgroup_mode": "MULTIPLE"
    }
}
(/code)
```

### Create an ad group
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
· TikTok Minis | 
      Specify an active TikTok Minis of the mini series or mini game type

**Note**: When you select a campaign budget mode, this setting must be the same across ad groups within the same campaign.
 | 
      `promotion_type` | 
      
- For a TikTok Minis of the mini series type, set this field to `MINI_APP`.
- For a TikTok Minis of the mini game type, set this field to `MINI_GAME`.
**Note**: When`budget_optimize_on` is `true` at the campaign level, specify the same `promotion_type` for ad groups within the same campaign.
 | 
     |
    
| 
      `minis_id` | 
      Specify the ID of an active TikTok Minis.
To obtain the ID of an active TikTok Minis within an ad account, use [/minis/get/](https://business-api.tiktok.com/portal/docs?id=1853450329535490) and select a TikTok Minis with `minis_status` as `ACTIVE`. | 
     |
    
| 
      Optimization and bidding
· Goal | 
      Value: We'll deliver your ads to users that are more likely to make a purchase in order to maximize your total purchase value.

**Note**: When you select a campaign budget mode, this setting must be the same across ad groups within the same campaign.
 | 
      `optimization_goal` | 
      `VALUE` (with `optimization_event` specified)

**Note**: When`budget_optimize_on` is `true` at the campaign level, specify the same `optimization_goal`for ad groups within the same campaign.
 | 
     |
    
| 
      Optimization and bidding
· Select value | 
      Any of the following types:
- **Purchase value**
- **Ad revenue value**
**Note**: 
- When you select a campaign budget mode, this setting, if specified, must be the same across ad group within the same campaign.
- Ad revenue value for Upgraded Smart+ Minis Ads for Mini Series is currently an allowlist-only feature. If you would like to access it, please contact your TikTok representative.
 | 
      `optimization_event` | 
      
- To use Purchase value, set this field to `ACTIVE_PAY` .
- To use Ad revenue value, set this field to `AD_REVENUE_VALUE`.To confirm whether your settings are eligible for enabling Purchase value or Ad revenue value, use [/tool/vbo_status/](https://business-api.tiktok.com/portal/docs?id=1770016073586753).

**Note**: 
- When`budget_optimize_on` is `true` at the campaign level, the `optimization_event`, if specified, must be the same for ad groups within the same campaign.
- Ad revenue value (`AD_REVENUE_VALUE`) for Upgraded Smart+ Minis Ads for Mini Series is currently an allowlist-only feature. If you would like to access it, please contact your TikTok representative.
 | 
     |
    
| 
      Optimization and bidding
·  Bid Strategy and (Optional) Target ROAS | 
      Any of the following options
- Highest value
- Minimum ROAS.For Minimum ROAS, you need to specify a Target ROAS at the same time.
**Note**:
- The bid strategy must be the same across ad groups within the same campaign.
- When you select a campaign budget mode, the Target ROAS, if specified, must be the same across ad groups within the same campaign.
- Target ROAS is only available when your campaign or ad group budget mode is set to daily.
 | 
      
- `bid_type`
- `bid_price`
- `conversion_bid_price`
- `deep_bid_type`
- `roas_bid` | 
      Set `deep_bid_type` to `VO_MIN_ROAS` or `VO_HIGHEST_VALUE`, and set `bid_type` to `BID_TYPE_NO_BID`. Do not specify `conversion_bid_price` and `bid_price`.
- If you set `deep_bid_type` to `VO_MIN_ROAS`, specify `roas_bid` at the same time.
**Note**:
- The `bid_type` must be the same across ad groups within the same campaign.
- When`budget_optimize_on` is `true` at the campaign level, the following settings, if specified, must be the same for ad groups within the same campaign:`deep_bid_type`
- `roas_bid`
- You can only set `deep_bid_type` to `VO_MIN_ROAS` in any of the following scenarios:At the campaign level, `budget_mode` is `BUDGET_MODE_DYNAMIC_DAILY_BUDGET`
- At the ad group level, `budget_mode` is `BUDGET_MODE_DYNAMIC_DAILY_BUDGET`
 | 
     |
    
| 
      Optimization and bidding
· Time window of the bid strategy | 
      Any of the following types:
- Day 7 ROAS or Highest Value
- Day 0 ROAS or Highest Value
**Note**: When you select a campaign budget mode, this setting, if specified, must be the same across ad groups within the same campaign.
 | 
      `vbo_window` | 
      Any of the following values:
- `SEVEN_DAYS`
- `ZERO_DAY`For example, if you set `deep_bid_type` to `VO_MIN_ROAS`, specify `roas_bid`, and set `vbo_window` to `ZERO_DAY`, the system will aim to keep your average ROAS of the current day around or higher than the target ROAS value.

To confirm whether your settings are eligible for enabling the Day 0 time window or Day 7 time window, use [/tool/vbo_status/](https://business-api.tiktok.com/portal/docs?id=1770016073586753).

**Note**: When`budget_optimize_on` is `true` at the campaign level, `vbo_window`, if specified, must be the same for ad groups within the same campaign:
 | 
     |
    
| 
      Optimization and bidding
· Attribution settings | 
      
- When the type of the selected TikTok Minis is mini series and Purchase value is selected, the attribution window will default to 180-day click and the event count will default to every.
- When the type of the selected TikTok Minis is mini game, the attribution window will default to 30-day click and the event count will default to every. | 
      
- `click_attribution_window`
- `attribution_event_count` | 
      Not specified
- When the `minis_type` of the specified `minis_id` is `MINI_SERIES` and `optimization_event` is `active_pay`:`click_attribution_window` will default to `ONE_HUNDRED_EIGHTY_DAYS`.
- `attribution_event_count`will default to `EVERY`.
- When the `minis_type` of the specified `minis_id` is  `MINI_GAME`:`click_attribution_window` will default to `THIRTY_DAYS`.
- `attribution_event_count`will default to `EVERY`. | 
     |
    
| 
      Optimization and bidding
· Billing event | 
      oCPM

**Note**: When you select a campaign budget mode, the billing event must be the same across ad groups within the same campaign.
 | 
      `billing_event` | 
      `OCPM`

**Note**: When`budget_optimize_on` is `true` at the campaign level, specify the same `billing_event`for ad groups within the same campaign.
 | 
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
            
- When you select a campaign budget mode:The ad group budget is disabled. The campaign-level budget will be used as the ad group budget.
- When you select an ad group budget strategy:If the ad group budget limit is No limit or Lifetime limit, you can use any of the following ad group budget modes:Lifetime
- Daily
- If the ad group budget limit is Daily limit, you can use the following ad group budget mode:Daily

**Note**: The ad group budget mode, if specified, must be the same across ad groups within the same campaign.
 | 
            `budget_mode`
`budget` | 
            
- When `budget_optimize_on` is `true` at the campaign level, `budget_mode` and `budget` are not supported.
- When `budget_optimize_on` is `false` and `budget_mode` is `BUDGET_MODE_INFINITE` or `BUDGET_MODE_TOTAL` at the campaign level:Set `budget_mode` to `BUDGET_MODE_TOTAL` or `BUDGET_MODE_DYNAMIC_DAILY_BUDGET`
- Specify a valid budget via `budget`
- When `budget_optimize_on` is `false` and `budget_mode` is `BUDGET_MODE_DAY` at the campaign level:Set `budget_mode` to `BUDGET_MODE_DYNAMIC_DAILY_BUDGET`
- Specify a valid budget via `budget`

**Note**: The `budget_mode`, if specified, must be the same across ad groups within the same campaign.
 | 
         |
    
| 
      Budget and schedule
· Add spend target per ad group
  · Daily minimum | 
      
- When you use a daily campaign budget, you can enable or disable this setting.
- When you use a lifetime campaign budget or an ad group budget, this setting is not supported. | 
      `min_budget` | 
      
- When `budget_optimize_on` is `true` and `budget_mode` is `BUDGET_MODE_DYNAMIC_DAILY_BUDGET` at the campaign level, you can either specify a valid value through this field or leave it unspecified.
- When `budget_optimize_on` is `true` and `budget_mode` is `BUDGET_MODE_TOTAL` or when `budget_optimize_on` is `false` at the campaign level, this field is not supported. | 
     |
    
| 
      Budget and schedule
· Schedule | 
      Any of the following types:
- Set start time and run ad group continuously
- Set start and end time
**Note**: You can only choose "Set start time and run ad group continuously" in any of the following scenarios:
- At the campaign level, a daily campaign budget is set.
- At the ad group level, a daily ad group budget is set.
 | 
      `schedule_type`
`schedule_start_time`
`schedule_end_time` | 
      
- To set start time and run the ad group continuously, set `schedule_type` to `SCHEDULE_FROM_NOW` and specify `schedule_start_time`. Do not specify `schedule_end_time`.
- To run the ad group between the scheduled start time and end time, set `schedule_type` to `SCHEDULE_START_END` and specify both `schedule_start_time` and `schedule_end_time`.
**Note**: You can only set `schedule_type` to `SCHEDULE_FROM_NOW` in any of the following scenarios:
- At the campaign level, `budget_mode` is `BUDGET_MODE_DYNAMIC_DAILY_BUDGET`
- At the ad group level, `budget_mode` is `BUDGET_MODE_DYNAMIC_DAILY_BUDGET`
 | 
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
      **Automatic targeting**
- You can use automatic targeting to leverage real-time data and machine learning to target audiences most likely to engage with your ads.To learn about the supported targeting settings, see [Available targeting settings for different targeting optimization modes in Upgraded Smart+ Minis Non-Catalog Campaigns](#item-link-Available targeting settings for different targeting optimization modes in Upgraded Smart+ Minis Non-Catalog Campaigns). | 
      `targeting_optimization_mode` | 
      `AUTOMATIC` or not specified

To learn about the supported targeting settings, see [Available targeting settings for different targeting optimization modes in Upgraded Smart+ Minis Non-Catalog Campaigns](#item-link-Available targeting settings for different targeting optimization modes in Upgraded Smart+ Minis Non-Catalog Campaigns). | 
     |
    
| 
      Placements and brand safety
· Placement | 
      TikTok | 
      `placement_type` | 
      `PLACEMENT_TYPE_NORMAL` | 
     |
    
| 
      `placements` | 
      `PLACEMENT_TIKTOK` | 
     |
    
| 
      Placements and brand safety
· Brand safety and suitability | 
      These settings only apply to **TikTok in-feed** and search ads. Any previous account-level settings in the brand safety hub will apply to your campaign. | 
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
  

#### Available targeting settings for different targeting optimization modes in Upgraded Smart+ Minis Non-Catalog Campaigns

  
    
| 
      Targeting optimization mode | 
      Available targeting setting | 
      Requirement | 
      Parameter | 
      How to configure the parameter | 
     |
  
  
    
| 
      Automatic targeting
(`targeting_optimization_mode` as `AUTOMATIC` or not specified) | 
      Audience controls
· Location | 
      The targeted locations should match or be the subset of the targeting locations of your TikTok Minis. | 
      `location_ids` or `zipcode_ids` or both | 
      Specify IDs of locations that match or are the subset of the targeting locations of the specified `minis_id`.
To obtain the targeting locations of a TikTok Minis, use [/minis/get/](https://business-api.tiktok.com/portal/docs?id=1853450329535490) and check the returned `region_codes`. | 
     |
    
| 
      Audience controls
· Minimum age | 
      Any of the following options:
        
          
- 18
          
- 25
         | 
      `spc_audience_age` | 
      Any of the following values:
        
          
- `OVER_EIGHTEEN` or unspecified
          
- `OVER_TWENTY_FIVE`
         | 
     |
    
| 
      Audience controls
· Languages (Optional) | 
      Enabled or disabled | 
      `languages` | 
      Specify valid values or not specified | 
     |
    
| 
      Audience controls
· Gender (Optional) | 
      Enabled or disabled | 
      `gender` | 
      Specify valid values or not specified | 
     |
    
| 
      Audience controls
· Exclude audience (Optional) | 
      Enabled or disabled | 
      `excluded_audience_ids` | 
      Specify valid values or not specified | 
     |
  

#### Example

##### When the TikTok Minis is of the mini series type
Request
```xcodeblock
(code curl http)
curl --location --request POST 'https://business-api.tiktok.com/open_api/v1.3/smart_plus/adgroup/create/' \
--header 'Access-Token: {{Access-Token}}' \
--header 'Content-Type: application/json' \
--data '{
    "advertiser_id": "{{advertiser_id}}",
    "campaign_id": "{{campaign_id}}",
    "request_id": "{{request_id}}",
    "adgroup_name": "{{adgroup_name}}",
    "promotion_type": "MINI_APP",
    "minis_id": "{{minis_id}}",
    "optimization_goal": "VALUE",
    "optimization_event": "ACTIVE_PAY",
    "bid_type": "BID_TYPE_NO_BID",
    "deep_bid_type": "VO_HIGHEST_VALUE",
    "vbo_window": "ZERO_DAY",
    "billing_event": "OCPM",
    "schedule_type": "SCHEDULE_START_END",
    "schedule_start_time": "{{schedule_start_time}}",
    "schedule_end_time": "{{schedule_end_time}}",
    "placement_type": "PLACEMENT_TYPE_NORMAL",
    "placements": [
        "PLACEMENT_TIKTOK"
    ],
    "targeting_optimization_mode": "AUTOMATIC",
    "targeting_spec": {
        "location_ids": [
            "{{location_id}}"
        ]
    }
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
        "adgroup_id": "{{adgroup_id}}",
        "adgroup_name": "{{adgroup_name}}",
        "advertiser_id": "{{advertiser_id}}",
        "attribution_event_count": "EVERY",
        "bid_type": "BID_TYPE_NO_BID",
        "billing_event": "OCPM",
        "budget": 0,
        "budget_mode": "BUDGET_MODE_INFINITE",
        "campaign_id": "{{campaign_id}}",
        "campaign_name": "{{campaign_name}}",
        "click_attribution_window": "THIRTY_TWO_DAYS",
        "comment_disabled": false,
        "conversion_bid_price": 0,
        "create_time": "{{create_time}}",
        "dayparting": "111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111",
        "deep_bid_type": "VO_HIGHEST_VALUE",
        "engaged_view_attribution_window": "OFF",
        "is_hfss": false,
        "is_lhf_compliance": false,
        "min_budget": 0,
        "minis_id": "{{minis_id}}",
        "modify_time": "{{modify_time}}",
        "operation_status": "ENABLE",
        "optimization_event": "ACTIVE_PAY",
        "optimization_goal": "VALUE",
        "pacing": "PACING_MODE_SMOOTH",
        "phone_info": {},
        "placement_type": "PLACEMENT_TYPE_NORMAL",
        "placements": [
            "PLACEMENT_TIKTOK"
        ],
        "promotion_type": "MINI_APP",
        "schedule_end_time": "{{schedule_end_time}}",
        "schedule_start_time": "{{schedule_start_time}}",
        "schedule_type": "SCHEDULE_START_END",
        "search_result_enabled": false,
        "secondary_optimization_event": "PURCHASE_ROI",
        "secondary_status": "ADGROUP_STATUS_CREATE",
        "share_disabled": false,
        "skip_learning_phase": true,
        "targeting_optimization_mode": "AUTOMATIC",
        "targeting_spec": {
            "actions": [],
            "age_groups": [
                "AGE_18_24",
                "AGE_25_34",
                "AGE_35_44",
                "AGE_45_54",
                "AGE_55_100"
            ],
            "brand_safety_type": "LIMITED_INVENTORY",
            "category_exclusion_ids": [
                "200",
                "202",
                "203"
            ],
            "gender": "GENDER_UNLIMITED",
            "location_ids": [
                "{{location_id}}"
            ],
            "spc_audience_age": "OVER_EIGHTEEN"
        },
        "vbo_window": "ZERO_DAY",
        "video_download_disabled": false,
        "view_attribution_window": "OFF"
    }
}
(/code)
```

##### When the TikTok Minis is of the mini game type
Request
```xcodeblock
(code curl http)
curl --location --request POST 'https://business-api.tiktok.com/open_api/v1.3/smart_plus/adgroup/create/' \
--header 'Access-Token: {{Access-Token}}' \
--header 'Content-Type: application/json' \
--data '{
    "advertiser_id": "{{advertiser_id}}",
    "campaign_id": "{{campaign_id}}",
    "request_id": "{{request_id}}",
    "adgroup_name": "{{adgroup_name}}",
    "promotion_type": "MINI_GAME",
    "minis_id": "{{minis_id}}",
    "optimization_goal": "VALUE",
    "optimization_event": "ACTIVE_PAY",
    "bid_type": "BID_TYPE_NO_BID",
    "deep_bid_type": "VO_HIGHEST_VALUE",
    "vbo_window": "ZERO_DAY",
    "billing_event": "OCPM",
    "schedule_type": "SCHEDULE_START_END",
    "schedule_start_time": "{{schedule_start_time}}",
    "schedule_end_time": "{{schedule_end_time}}",
    "placement_type": "PLACEMENT_TYPE_NORMAL",
    "placements": [
        "PLACEMENT_TIKTOK"
    ],
    "targeting_optimization_mode": "AUTOMATIC",
    "targeting_spec": {
        "location_ids": [
            "{{location_id}}"
        ]
    }
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
        "adgroup_id": "{{adgroup_id}}",
        "adgroup_name": "{{adgroup_name}}",
        "advertiser_id": "{{advertiser_id}}",
        "attribution_event_count": "EVERY",
        "bid_type": "BID_TYPE_NO_BID",
        "billing_event": "OCPM",
        "budget": 0,
        "budget_mode": "BUDGET_MODE_INFINITE",
        "campaign_id": "{{campaign_id}}",
        "campaign_name": "{{campaign_name}}",
        "click_attribution_window": "THIRTY_DAYS",
        "comment_disabled": false,
        "conversion_bid_price": 0,
        "create_time": "{{create_time}}",
        "dayparting": "111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111",
        "deep_bid_type": "VO_HIGHEST_VALUE",
        "engaged_view_attribution_window": "OFF",
        "is_hfss": false,
        "is_lhf_compliance": false,
        "min_budget": 0,
        "minis_id": "{{minis_id}}",
        "modify_time": "{{modify_time}}",
        "operation_status": "ENABLE",
        "optimization_event": "ACTIVE_PAY",
        "optimization_goal": "VALUE",
        "pacing": "PACING_MODE_SMOOTH",
        "phone_info": {},
        "placement_type": "PLACEMENT_TYPE_NORMAL",
        "placements": [
            "PLACEMENT_TIKTOK"
        ],
        "promotion_type": "MINI_GAME",
        "schedule_end_time": "{{schedule_end_time}}",
        "schedule_start_time": "{{schedule_start_time}}",
        "schedule_type": "SCHEDULE_START_END",
        "search_result_enabled": false,
        "secondary_optimization_event": "PURCHASE_ROI",
        "secondary_status": "ADGROUP_STATUS_CREATE",
        "share_disabled": false,
        "skip_learning_phase": true,
        "targeting_optimization_mode": "AUTOMATIC",
        "targeting_spec": {
            "actions": [],
            "age_groups": [
                "AGE_18_24",
                "AGE_25_34",
                "AGE_35_44",
                "AGE_45_54",
                "AGE_55_100"
            ],
            "brand_safety_type": "LIMITED_INVENTORY",
            "category_exclusion_ids": [
                "200",
                "202",
                "203"
            ],
            "gender": "GENDER_UNLIMITED",
            "location_ids": [
                "{{location_id}}"
            ],
            "spc_audience_age": "OVER_EIGHTEEN"
        },
        "vbo_window": "ZERO_DAY",
        "video_download_disabled": false,
        "view_attribution_window": "OFF"
    }
}
(/code)
```

### Create an ad
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
- For Spark Ads identities, specify values to `identity_type` and `identity_id` within the `creative_info` object.
 | 
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
- CarouselTo learn about the combination of available ad creatives based on identity type, see [Ad creative combinations by identity and ad type](https://business-api.tiktok.com/portal/docs?id=1847839781968897).

**Note**: Your creative may be eligible for [paid and organic optimization](https://ads.tiktok.com/help/article/about-smart-plus-paid-and-organic-optimization). As part of this process, the ad destination link and associated URL parameters may be synchronized to your TikTok post as an organic anchor displayed in the For You feed. Organic creatives subject to such optimization will have their performance reported in aggregation with paid ads as a single entity across TikTok and authorized third-party reporting systems.
 | 
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
- CarouselTo learn about configurations of the available ad creative combinations based on identity type, see [Ad creative combinations by identity and ad type](https://business-api.tiktok.com/portal/docs?id=1847839781968897).

**Note**: Your creative may be eligible for [paid and organic optimization](https://ads.tiktok.com/help/article/about-smart-plus-paid-and-organic-optimization). As part of this process, the ad destination link and associated URL parameters may be synchronized to your TikTok post as an organic anchor displayed in the For You feed. Organic creatives subject to such optimization will have their performance reported in aggregation with paid ads as a single entity across TikTok and authorized third-party reporting systems.
 | 
     |
    
| 
      Selling points (Optional) | 
      Enabled or disabled | 
      `selling_points` | 
      Specify valid values or not specified | 
     |
    
| 
      Call to action | 
      Dynamic | 
      `call_to_action_id` | 
      Specify a valid value

To learn about how to create Dynamic CTAs, see [CTA recommendations > Dynamic CTAs](https://business-api.tiktok.com/portal/docs?id=1740307296329730#item-link-Dynamic%20CTAs). | 
     |
    
| 
      `call_to_action_list` | 
      Not specified | 
     |
    
| 
      Interactive add-ons
(Optional)
(When a TikTok Minis of the mini series type is specified and the ad creatives include videos or video posts ) | 
      Disabled or enabled with up to one add-on in any of the following types:
- Display Card
- Countdown Sticker
- Gift Code Sticker | 
      `interactive_add_on_list` | 
      Not specified or specify up to one ID of any of the following add-on types:
- Countdown Sticker
- Gift Code Sticker
- Display Card
**Note**:
- You can only use add-ons when the following conditions are both met:At the ad group level: A TikTok Minis of the mini series type is specified through `minis_id`.
- At the ad level: `creative_list` contains video creatives, including videos and TikTok video posts.To create an interactive add-on (creative portfolio), use [/creative/portfolio/create/](https://business-api.tiktok.com/portal/docs?id=1739091950439426).
- To learn about how to obtain the ID of a Display Card portfolio, see [Cards](https://business-api.tiktok.com/portal/docs?id=1749019652141058#item-link-Display%20Card).
- To learn about how to obtain the ID of a Countdown Sticker or Gift Code Sticker portfolio, see [Stickers](https://business-api.tiktok.com/portal/docs?id=1749019667506177).
 | 
     |
    
| 
      Destination | 
      TikTok Minis URL. This is a link that will lead directly to the TikTok Minis interface through an ad. | 
      `landing_page_url_list` | 
      Specify a valid TikTok Minis URL.
Ensure the URL matches the `minis_id` specified at the ad group level.
To obtain a valid TikTok Minis URL, contact your TikTok representative. | 
     |
    
| 
      Disclaimer 
(Optional) | 
      Enabled or disabled | 
      `disclaimer` | 
      Specify a valid value or not specified | 
     |
  

#### Example
Request
```xcodeblock
(code curl http)
curl --location --request POST 'https://business-api.tiktok.com/open_api/v1.3/smart_plus/ad/create/' \
--header 'Access-Token: {{Access-Token}}' \
--header 'Content-Type: application/json' \
--data '{
    "advertiser_id": "{{advertiser_id}}",
    "adgroup_id": "{{adgroup_id}}",
    "ad_name": "{{ad_name}}",
    "creative_list": [
        {
            "creative_info": {
                "ad_format": "SINGLE_VIDEO",
                "video_info": {
                    "video_id": "{{video_id}}"
                },
                "image_info": [
                    {
                        "web_uri": "{{web_uri}}"
                    }
                ],
                "identity_type": "BC_AUTH_TT",
                "identity_id": "{{identity_id}}",
                "identity_authorized_bc_id": "{{identity_authorized_bc_id}}"
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
    "landing_page_url_list": [
        {
            "landing_page_url": "{{landing_page_url}}"
        }
    ],
    "ad_configuration": {
        "call_to_action_id": "{{call_to_action_id}}",
        "product_info": {
            "selling_points": [
                "{{selling_point}}"
            ]
        }
    }
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
        "ad_configuration": {
            "call_to_action_id": "{{call_to_action_id}}",
            "dark_post_status": "OFF",
            "deeplink_utm_params": [],
            "phone_info": {},
            "tracking_info": {},
            "utm_params": []
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
        "auto_message_list": [],
        "call_to_action_list": [],
        "campaign_id": "{{campaign_id}}",
        "campaign_name": "{{campaign_name}}",
        "create_time": "{{create_time}}",
        "creative_list": [
            {
                "ad_material_id": "{{ad_material_id}}",
                "creative_info": {
                    "ad_format": "SINGLE_VIDEO",
                    "identity_authorized_bc_id": "{{bc_id}}",
                    "identity_id": "{{identity_id}}",
                    "identity_type": "BC_AUTH_TT",
                    "image_info": [
                        {
                            "web_uri": "{{image_web_uri}}"
                        }
                    ],
                    "material_name": "",
                    "video_info": {
                        "file_name": "",
                        "video_id": "{{video_id}}"
                    }
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
        "smart_plus_ad_id": "{{ad_id}}"
    }
}
(/code)
```

# Create an Upgraded Smart+ Minis Catalog Campaign
An Upgraded Smart+ Minis Catalog Campaign is an Upgraded Smart+ App Campaign promoting a TikTok Minis using a mini series catalog.

## Prerequisite
Creating an Upgraded Smart+ Minis Catalog Campaign requires setting up a mini series catalog in Business Center first.

To set up the mini series catalog:

1. Create a **mini series** catalog using [/catalog/create/](https://business-api.tiktok.com/portal/docs?id=1740306481704961).

2. Upload mini series to the catalog using [/catalog/product/upload/](https://business-api.tiktok.com/portal/docs?id=1740497429681153) (JSON schema), [/catalog/product/file/](https://business-api.tiktok.com/portal/docs?id=1740564136678402) (CSV feed template), or [/catalog/feed/create/](https://business-api.tiktok.com/portal/docs?id=1740665161957377)(online data feed schedule).

3. Check the product handling results.
	- For CSV feed and JSON schema, use [/catalog/product/log/](https://business-api.tiktok.com/portal/docs?id=1740570027173889).
		- Pass in the `feed_log_id` obtained from Step 2. If the field `error_affected_products` in the response is not null, examine the issue details and return to Step 2 to reupload the product.
	- For online feed, use [/catalog/feed/log/](https://business-api.tiktok.com/portal/docs?id=1740665225631810).
		- Pass in the `feed_id` obtained from Step 2. If the field `error_count` in the response is not 0, examine your online feed and return to Step 2 to reupload the product.

4. (Optional) Invite members to Business Center and grant the admin permission using [/bc/member/invite/](https://business-api.tiktok.com/portal/docs?id=1739939455765505).
You can also choose `advertiser_role` that you want to assign to the members invited.

5. (Optional) Share a catalog with members and grant catalog management access using [/bc/asset/assign/](https://business-api.tiktok.com/portal/docs?id=1739438211077121).
Make sure to specify `CATALOG` in the `asset_type` field and `ADMIN` in the `catalog_role` field.

## Steps
### Create a campaign
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
      App promotion | 
      `objective_type` | 
      `APP_PROMOTION` | 
     |
    
| 
      App promotion type | 
      TikTok Minis | 
      `app_promotion_type` | 
      `MINIS` | 
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
      **Enabled**

To create an Upgraded Smart+ Minis Campaign without using a mini series catalog, see [Create an Upgraded Smart+ Minis Non-Catalog Campaign](#item-link-Create an Upgraded Smart+ Minis Non-Catalog Campaign). | 
      `catalog_enabled` | 
      `true` | 
     |
    
| 
      Campaign name | 
      Specify a valid name | 
      `campaign_name` | 
      Specify a valid value | 
     |
    
| 
        Campaign budget strategy | 
        Any of the following types:
- **Campaign budget**: Your budget will be automatically allocated and optimized across ad groups. All ad groups must share the same budget and optimization settings.
- **Ad group budget**: Precisely control spend for each ad group, using different budget and optimization settings for each. | 
        `budget_optimize_on` | 
        
- To set a campaign budget, set this field to `true` or leave it unspecified.
- To set an ad group budget, set this field to `false`. | 
     |
	
| 
        Campaign budget mode | 
        
- When Campaign budget strategy is Campaign budget, specify any of the following modes:Daily
- Lifetime
- When Campaign budget strategy is Ad group budget, specify any of the following modes to determine the budget limit for all ad groups:No limit
- Daily
- Lifetime | 
        `budget_mode` | 
        
- When `budget_optimize_on` is `true` or not specified, use any of the following values:`BUDGET_MODE_TOTAL`
- `BUDGET_MODE_DYNAMIC_DAILY_BUDGET`
- When `budget_optimize_on` is `false`, use any of the following values:`BUDGET_MODE_INFINITE`
- `BUDGET_MODE_DAY`
- `BUDGET_MODE_TOTAL` | 
     |
	
| 
        Campaign budget | 
        
- When Campaign budget strategy is Campaign budget:Specify a valid budget.
- When Campaign budget strategy is Ad group budget:If the budget limit is No limit:Disabled
- If the budget limit is Daily or Lifetime limit:Specify a valid budget | 
        `budget` | 
        
- When `budget_optimize_on` is `true` or not specified:Specify a valid value.
- When `budget_optimize_on` is `false`:If `budget_mode` is `BUDGET_MODE_INFINITE`:Not specified
- If `budget_mode` is `BUDGET_MODE_DAY` or `BUDGET_MODE_TOTAL`:Specify a valid value | 
     |
    
| 
      PO number (Optional) | 
      Enabled or disabled | 
      `po_number` | 
      Specify valid values or not specified | 
     |
  

#### Example
Request
```xcodeblock
(code curl http)
curl --location --request POST 'https://business-api.tiktok.com/open_api/v1.3/smart_plus/campaign/create/' \
--header 'Access-Token: {{Access-Token}}' \
--header 'Content-Type: application/json' \
--data '{
    "advertiser_id": "{{advertiser_id}}",
    "request_id": "{{request_id}}",
    "objective_type": "APP_PROMOTION",
    "app_promotion_type": "MINIS",
    "campaign_type": "REGULAR_CAMPAIGN",
    "catalog_enabled": true,
    "campaign_name": "{{campaign_name}}",
    "budget_optimize_on": true,
    "budget_mode": "BUDGET_MODE_DYNAMIC_DAILY_BUDGET",
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
        "advertiser_id": "{{advertiser_id}}",
        "app_promotion_type": "MINIS",
        "budget": {{budget}},
        "budget_mode": "BUDGET_MODE_DYNAMIC_DAILY_BUDGET",
        "budget_optimize_on": true,
        "campaign_id": "{{campaign_id}}",
        "campaign_name": "{{campaign_name}}",
        "campaign_type": "REGULAR_CAMPAIGN",
        "catalog_enabled": true,
        "create_time": "{{create_time}}",
        "modify_time": "{{modify_time}}",
        "objective_type": "APP_PROMOTION",
        "operation_status": "ENABLE",
        "secondary_status": "CAMPAIGN_STATUS_ENABLE",
        "smart_plus_adgroup_mode": "MULTIPLE"
    }
}
(/code)
```

### Create an ad group
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
· TikTok Minis | 
      Specify an active TikTok Minis of the mini series type

**Note**: When you select a campaign budget mode, this setting must be the same across ad groups within the same campaign.
 | 
      `promotion_type` | 
      `MINI_APP`

**Note**: When`budget_optimize_on` is `true` at the campaign level, specify the same `promotion_type` for ad groups within the same campaign.
 | 
     |
    
| 
      `minis_id` | 
      Specify the ID of an active TikTok Minis of the mini series type.
To obtain the ID of an active TikTok Minis of the mini series type within an ad account, use [/minis/get/](https://business-api.tiktok.com/portal/docs?id=1853450329535490) and select a TikTok Minis with `minis_status` as `ACTIVE` and `minis_type` as `MINI_SERIES`. | 
     |
    
| 
      Optimization and bidding
· Goal | 
      Value: We'll deliver your ads to users that are more likely to make a purchase in order to maximize your total purchase value.

**Note**: 

- When you select a campaign budget mode, this setting must be the same across ad groups within the same campaign.
 | 
      `optimization_goal` | 
      `VALUE` (with `optimization_event` specified)

**Note**: When`budget_optimize_on` is `true` at the campaign level, specify the same `optimization_goal`for ad groups within the same campaign.
 | 
     |
    
| 
      Optimization and bidding
· Select value | 
      Any of the following types:
- **Purchase value**
- **Ad revenue value**

**Note**: 
- When you select a campaign budget mode, this setting, if specified, must be the same across ad group within the same campaign.
- Ad revenue value for Upgraded Smart+ Minis Ads for Mini Series is currently an allowlist-only feature. If you would like to access it, please contact your TikTok representative.
 | 
      `optimization_event` | 
      
- To use Purchase value, set this field to `ACTIVE_PAY` .
- To use Ad revenue value, set this field to `AD_REVENUE_VALUE`.
To confirm whether your settings are eligible for enabling Purchase value or Ad revenue value, use [/tool/vbo_status/](https://business-api.tiktok.com/portal/docs?id=1770016073586753).

**Note**: 
- When`budget_optimize_on` is `true` at the campaign level, the `optimization_event`, if specified, must be the same for ad groups within the same campaign.
- Ad revenue value (`AD_REVENUE_VALUE`) for Upgraded Smart+ Minis Ads for Mini Series is currently an allowlist-only feature. If you would like to access it, please contact your TikTok representative.
 | 
     |
    
| 
      Optimization and bidding
·  Bid Strategy and (Optional) Target ROAS | 
      Any of the following options
- Highest value
- Minimum ROAS.For Minimum ROAS, you need to specify a Target ROAS at the same time.

**Note**: 
- The bid strategy must be the same across ad groups within the same campaign.
- When you select a campaign budget mode, the Target ROAS, if specified, must be the same across ad groups within the same campaign.
- Target ROAS is only available when your campaign or ad group budget mode is set to daily.
 | 
      `bid_type`
`bid_price`
`conversion_bid_price`
`deep_bid_type`
`roas_bid` | 
      Set `deep_bid_type` to `VO_MIN_ROAS` or `VO_HIGHEST_VALUE`, and set `bid_type` to `BID_TYPE_NO_BID`. Do not specify `conversion_bid_price` and `bid_price`.
- If you set `deep_bid_type` to `VO_MIN_ROAS`, specify `roas_bid` at the same time.
**Note**: 
- The `bid_type` must be the same across ad groups within the same campaign.
-  When`budget_optimize_on` is `true` at the campaign level, the following settings, if specified, must be the same for ad groups within the same campaign:`deep_bid_type`
- `roas_bid`
- You can only set `deep_bid_type` to `VO_MIN_ROAS` in any of the following scenarios:At the campaign level, `budget_mode` is `BUDGET_MODE_DYNAMIC_DAILY_BUDGET`
- At the ad group level, `budget_mode` is `BUDGET_MODE_DYNAMIC_DAILY_BUDGET` | 
     |
    
| 
      Optimization and bidding
· Time window of the bid strategy | 
      Any of the following types:
- Day 7 ROAS or Highest Value
- Day 0 ROAS or Highest Value
**Note**: When you select a campaign budget mode, this setting, if specified, must be the same across ad groups within the same campaign.
 | 
      `vbo_window` | 
      Any of the following values:
- `SEVEN_DAYS`
- `ZERO_DAY`
For example, if you set `deep_bid_type` to `VO_MIN_ROAS`, specify `roas_bid`, and set `vbo_window` to `ZERO_DAY`, the system will aim to keep your average ROAS of the current day around or higher than the target ROAS value.

To confirm whether your settings are eligible for enabling the Day 0 time window or Day 7 time window, use [/tool/vbo_status/](https://business-api.tiktok.com/portal/docs?id=1770016073586753).

**Note**: When`budget_optimize_on` is `true` at the campaign level, `vbo_window`, if specified, must be the same for ad groups within the same campaign:
 | 
     |
    
| 
      Optimization and bidding
· Attribution settings | 
      The attribution window will default to 180-day click and the event count will default to every. | 
      `click_attribution_window`
`attribution_event_count` | 
      Not specified

- `click_attribution_window` will default to `ONE_HUNDRED_EIGHTY_DAYS`.
- `attribution_event_count`will default to `EVERY`. | 
     |
    
| 
      Optimization and bidding
· Billing event | 
      oCPM

**Note**: 

- When you select a campaign budget mode, the billing event must be the same across ad groups within the same campaign. | 
      `billing_event` | 
      `OCPM`

**Note**: When`budget_optimize_on` is `true` at the campaign level, specify the same `billing_event`for ad groups within the same campaign.
 | 
     |
    
| 
      Optimization and bidding
· Delivery Type | 
      Standard (default) | 
      N/A | 
      By default, the Delivery Type for the Upgraded Smart+ Campaign is Standard. | 
     |
    
| 
      Catalog | 
      Specify **a mini series catalog with at least one approved mini series** | 
      `catalog_id`
`catalog_authorized_bc_id` | 
      Specify valid values.
The catalog (`catalog_id`) needs to have at least one approved mini series. You can verify this by checking the value of `approved` returned from [/catalog/overview/](https://business-api.tiktok.com/portal/docs?id=1740492470201345), which should be at least 1. 

- To obtain mini series catalogs within a Business Center, use [/catalog/get/](https://business-api.tiktok.com/portal/docs?id=1740315452868610). The `catalog_type` of a mini series catalog will be `MINI_SERIES`.
- To learn about how to create a mini series catalog, see [Prerequisite](#item-link-Prerequisite). | 
     |
          
| 
            Budget and schedule
· Budget | 
            
- When you select a campaign budget mode:The ad group budget is disabled. The campaign-level budget will be used as the ad group budget.
- When you select an ad group budget strategy:If the ad group budget limit is No limit or Lifetime limit, you can use any of the following ad group budget modes:Lifetime
- Daily
- If the ad group budget limit is Daily limit, you can use the following ad group budget mode:Daily

**Note**: The ad group budget mode, if specified, must be the same across ad groups within the same campaign.
 | 
            `budget_mode`
`budget` | 
            
- When `budget_optimize_on` is `true` at the campaign level, `budget_mode` and `budget` are not supported.
- When `budget_optimize_on` is `false` and `budget_mode` is `BUDGET_MODE_INFINITE` or `BUDGET_MODE_TOTAL` at the campaign level:Set `budget_mode` to `BUDGET_MODE_TOTAL` or `BUDGET_MODE_DYNAMIC_DAILY_BUDGET`
- Specify a valid budget via `budget`
- When `budget_optimize_on` is `false` and `budget_mode` is `BUDGET_MODE_DAY` at the campaign level:Set `budget_mode` to `BUDGET_MODE_DYNAMIC_DAILY_BUDGET`
- Specify a valid budget via `budget`

**Note**: The `budget_mode`, if specified, must be the same across ad groups within the same campaign.
 | 
         |
    
| 
      Budget and schedule
· Add spend target per ad group
  · Daily minimum | 
      
- When you use a daily campaign budget, you can enable or disable this setting.
- When you use a lifetime campaign budget or an ad group budget, this setting is not supported. | 
      `min_budget` | 
      
- When `budget_optimize_on` is `true` and `budget_mode` is `BUDGET_MODE_DYNAMIC_DAILY_BUDGET` at the campaign level, you can either specify a valid value through this field or leave it unspecified.
- When `budget_optimize_on` is `true` and `budget_mode` is `BUDGET_MODE_TOTAL` or when `budget_optimize_on` is `false` at the campaign level, this field is not supported. | 
     |
    
| 
      Budget and schedule
· Schedule | 
      Any of the following types:
- Set start time and run ad group continuously
- Set start and end time

**Note**: You can only choose "Set start time and run ad group continuously" in any of the following scenarios: 
- At the campaign level, a daily campaign budget is set.
- At the ad group level, a daily ad group budget is set.
 | 
      `schedule_type`
`schedule_start_time`
`schedule_end_time` | 
      
- To set start time and run the ad group continuously, set `schedule_type` to `SCHEDULE_FROM_NOW` and specify `schedule_start_time`. Do not specify `schedule_end_time`.
- To run the ad group between the scheduled start time and end time, set `schedule_type` to `SCHEDULE_START_END` and specify both `schedule_start_time` and `schedule_end_time`.

**Note**: You can only set `schedule_type` to `SCHEDULE_FROM_NOW` in any of the following scenarios:
- At the campaign level, `budget_mode` is `BUDGET_MODE_DYNAMIC_DAILY_BUDGET`
- At the ad group level, `budget_mode` is `BUDGET_MODE_DYNAMIC_DAILY_BUDGET`
 | 
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
      **Automatic targeting**
- You can use automatic targeting to leverage real-time data and machine learning to target audiences most likely to engage with your ads.
To learn about the supported targeting settings, see [Available targeting settings for different targeting optimization modes in Upgraded Smart+ Minis Catalog Campaigns](#item-link-Available targeting settings for different targeting optimization modes in Upgraded Smart+ Minis Catalog Campaigns). | 
      `targeting_optimization_mode` | 
      `AUTOMATIC` or not specified

To learn about the supported targeting settings, see [Available targeting settings for different targeting optimization modes in Upgraded Smart+ Minis Catalog Campaigns](#item-link-Available targeting settings for different targeting optimization modes in Upgraded Smart+ Minis Catalog Campaigns). | 
     |
    
| 
      Placements and brand safety
· Placement | 
      TikTok | 
      `placement_type` | 
      `PLACEMENT_TYPE_NORMAL` | 
     |
    
| 
      `placements` | 
      `PLACEMENT_TIKTOK` | 
     |
    
| 
      Placements and brand safety
· Brand safety and suitability | 
      These settings only apply to **TikTok in-feed** and search ads. Any previous account-level settings in the brand safety hub will apply to your campaign. | 
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
  

#### Available targeting settings for different targeting optimization modes in Upgraded Smart+ Minis Catalog Campaigns

  
    
| 
      Targeting optimization mode | 
      Available targeting setting | 
      Requirement | 
      Parameter | 
      How to configure the parameter | 
     |
  
  
    
| 
      Automatic targeting
(`targeting_optimization_mode`
 as `AUTOMATIC` or not specified) | 
      Audience controls
· Location | 
      The targeted locations should match or be the subset of the targeting locations of both your TikTok Minis and the mini series catalog. | 
      `location_ids` or `zipcode_ids` or both | 
      Specify IDs of locations that match or are the subset of the targeting locations of the specified `minis_id` and `catalog_id`.

- To obtain the targeting locations of a TikTok Minis, use [/minis/get/](https://business-api.tiktok.com/portal/docs?id=1853450329535490) and check the returned `region_codes`.
- To obtain the targeting locations of a mini series catalog, use [/catalog/get/](https://business-api.tiktok.com/portal/docs?id=1740315452868610) and check the returned `country` and `additional_config_list`. | 
     |
    
| 
      Audience controls
· Minimum age | 
      Any of the following options:
- 18
- 25 | 
      `spc_audience_age` | 
      Any of the following values:
- `OVER_EIGHTEEN` or unspecified
- `OVER_TWENTY_FIVE` | 
     |
    
| 
      Audience controls
· Languages
 (Optional) | 
      Enabled or disabled | 
      `languages` | 
      Specify valid values or not specified | 
     |
    
| 
      Audience controls
· Gender
 (Optional) | 
      Enabled or disabled | 
      `gender` | 
      Specify valid values or not specified | 
     |
    
| 
      Audience controls
· Exclude audience
(Optional) | 
      Enabled or disabled | 
      `excluded_audience_ids` | 
      Specify valid values or not specified | 
     |
  

#### Example
Request
```xcodeblock
(code curl http)
curl --location --request POST 'https://business-api.tiktok.com/open_api/v1.3/smart_plus/adgroup/create/' \
--header 'Access-Token: {{Access-Token}}' \
--header 'Content-Type: application/json' \
--data '{
    "advertiser_id": "{{advertiser_id}}",
    "campaign_id": "{{campaign_id}}",
    "request_id": "{{request_id}}",
    "adgroup_name": "{{adgroup_name}}",
    "promotion_type": "MINI_APP",
    "minis_id": "{{minis_id}}",
    "optimization_goal": "VALUE",
    "optimization_event": "ACTIVE_PAY",
    "bid_type": "BID_TYPE_NO_BID",
    "deep_bid_type": "VO_HIGHEST_VALUE",
    "vbo_window": "ZERO_DAY",
    "catalog_id": "{{catalog_id}}",
    "catalog_authorized_bc_id": "{{catalog_authorized_bc_id}}",
    "billing_event": "OCPM",
    "schedule_type": "SCHEDULE_START_END",
    "schedule_start_time": "{{schedule_start_time}}",
    "schedule_end_time": "{{schedule_end_time}}",
    "placement_type": "PLACEMENT_TYPE_NORMAL",
    "placements": [
        "PLACEMENT_TIKTOK"
    ],
    "targeting_optimization_mode": "AUTOMATIC",
    "targeting_spec": {
        "location_ids": [
            "{{location_id}}"
        ]
    }
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
        "adgroup_id": "{{adgroup_id}}",
        "adgroup_name": "{{adgroup_name}}",
        "advertiser_id": "{{advertiser_id}}",
        "attribution_event_count": "EVERY",
        "bid_type": "BID_TYPE_NO_BID",
        "billing_event": "OCPM",
        "budget": 0,
        "budget_mode": "BUDGET_MODE_INFINITE",
        "campaign_id": "{{campaign_id}}",
        "campaign_name": "{{campaign_name}}",
        "catalog_authorized_bc_id": "{{catalog_authorized_bc_id}}",
        "catalog_id": "{{catalog_id}}",
        "click_attribution_window": "THIRTY_TWO_DAYS",
        "comment_disabled": false,
        "conversion_bid_price": 0,
        "create_time": "{{create_time}}",
        "dayparting": "11111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111",
        "deep_bid_type": "VO_HIGHEST_VALUE",
        "engaged_view_attribution_window": "OFF",
        "is_hfss": false,
        "is_lhf_compliance": false,
        "min_budget": 0,
        "minis_id": "{{minis_id}}",
        "modify_time": "{{modify_time}}",
        "operation_status": "ENABLE",
        "optimization_event": "ACTIVE_PAY",
        "optimization_goal": "VALUE",
        "pacing": "PACING_MODE_SMOOTH",
        "phone_info": {},
        "placement_type": "PLACEMENT_TYPE_NORMAL",
        "placements": [
            "PLACEMENT_TIKTOK"
        ],
        "product_source": "CATALOG",
        "promotion_type": "MINI_APP",
        "schedule_end_time": "{{schedule_end_time}}",
        "schedule_start_time": "{{schedule_start_time}}",
        "schedule_type": "SCHEDULE_START_END",
        "search_result_enabled": false,
        "secondary_optimization_event": "PURCHASE_ROI",
        "secondary_status": "ADGROUP_STATUS_CREATE",
        "share_disabled": false,
        "skip_learning_phase": true,
        "targeting_optimization_mode": "AUTOMATIC",
        "targeting_spec": {
            "actions": [],
            "age_groups": [
                "AGE_18_24",
                "AGE_25_34",
                "AGE_35_44",
                "AGE_45_54",
                "AGE_55_100"
            ],
            "brand_safety_type": "LIMITED_INVENTORY",
            "category_exclusion_ids": [
                "200",
                "202",
                "203"
            ],
            "gender": "GENDER_UNLIMITED",
            "location_ids": [
                "{{location_id}}"
            ],
            "spc_audience_age": "OVER_EIGHTEEN"
        },
        "vbo_window": "ZERO_DAY",
        "video_download_disabled": false,
        "view_attribution_window": "OFF"
    }
}
(/code)
```

### Create an ad
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
      Specific series | 
      Select one mini series | 
      `product_specific_type` | 
      `CUSTOMIZED_PRODUCTS` | 
     |
    
| 
      `product_ids` | 
      Specify one available mini series within the `catalog_id` specified at the ad group level.

- To retrieve the product ID (`product_id`) of each mini series, use [/catalog/product/get/](https://business-api.tiktok.com/portal/docs?id=1740564136678402) and select one product with `audit_status` as `approved`. | 
     |
    
| 
      `product_set_id` | 
      Not specified | 
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
To learn about the combination of available ad creatives based on identity type, see [Ad creative combinations by identity and ad type](https://business-api.tiktok.com/portal/docs?id=1847839781968897).

**Note**: Your creative may be eligible for [paid and organic optimization](https://ads.tiktok.com/help/article/about-smart-plus-paid-and-organic-optimization). As part of this process, the ad destination link and associated URL parameters may be synchronized to your TikTok post as an organic anchor displayed in the For You feed. Organic creatives subject to such optimization will have their performance reported in aggregation with paid ads as a single entity across TikTok and authorized third-party reporting systems.
 | 
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
To learn about configurations of the available ad creative combinations based on identity type, see [Ad creative combinations by identity and ad type](https://business-api.tiktok.com/portal/docs?id=1847839781968897).

**Note**: Your creative may be eligible for [paid and organic optimization](https://ads.tiktok.com/help/article/about-smart-plus-paid-and-organic-optimization). As part of this process, the ad destination link and associated URL parameters may be synchronized to your TikTok post as an organic anchor displayed in the For You feed. Organic creatives subject to such optimization will have their performance reported in aggregation with paid ads as a single entity across TikTok and authorized third-party reporting systems.
 | 
     |
    
| 
      Selling points | 
      Disabled | 
      `selling_points` | 
      Not specified | 
     |
    
| 
      Call to action | 
      Dynamic | 
      `call_to_action_id` | 
      Specify a valid value

To learn about how to create Dynamic CTAs, see [CTA recommendations > Dynamic CTAs](https://business-api.tiktok.com/portal/docs?id=1740307296329730#item-link-Dynamic%20CTAs). | 
     |
    
| 
      `call_to_action_list` | 
      Not specified | 
     |
    
| 
      Interactive add-ons
(Optional)
(When a TikTok Minis of the mini series type is specified and the ad creatives include videos or video posts ) | 
      Disabled or enabled with up to one add-on in any of the following types:
- Display Card
- Countdown Sticker
- Gift Code Sticker | 
      `interactive_add_on_list` | 
      Not specified or specify up to one ID of any of the following add-on types:
- Countdown Sticker
- Gift Code Sticker
- Display Card
**Note**: 
- You can only use add-ons when the following conditions are both met:At the ad group level: A TikTok Minis of the mini series type is specified through `minis_id`.
- At the ad level: `creative_list` contains video creatives, including videos and TikTok video posts.
To create an interactive add-on (creative portfolio), use [/creative/portfolio/create/](https://business-api.tiktok.com/portal/docs?id=1739091950439426).
- To learn about how to obtain the ID of a Display Card portfolio, see [Cards](https://business-api.tiktok.com/portal/docs?id=1749019652141058#item-link-Display%20Card).
- To learn about how to obtain the ID of a Countdown Sticker or Gift Code Sticker portfolio, see [Stickers](https://business-api.tiktok.com/portal/docs?id=1749019667506177). | 
     |
    
| 
      Destination | 
      TikTok Minis URL. This is a link that will lead directly to the TikTok Minis interface through an ad. | 
      `landing_page_url_list` | 
      Specify a valid TikTok Minis URL.
Ensure the URL matches the `minis_id` specified at the ad group level.
To obtain a valid TikTok Minis URL, contact your TikTok representative. | 
     |
    
| 
      Disclaimer 
(Optional) | 
      Enabled or disabled | 
      `disclaimer` | 
      Specify a valid value or not specified | 
     |
  

#### Example
Request
```xcodeblock
(code curl http)
curl --location --request POST 'https://business-api.tiktok.com/open_api/v1.3/smart_plus/ad/create/' \
--header 'Access-Token: {{Access-Token}}' \
--header 'Content-Type: application/json' \
--data '{
    "advertiser_id": "{{advertiser_id}}",
    "adgroup_id": "{{adgroup_id}}",
    "ad_name": "{{ad_name}}",
    "creative_list": [
        {
            "creative_info": {
                "ad_format": "SINGLE_VIDEO",
                "video_info": {
                    "video_id": "{{video_id}}"
                },
                "image_info": [
                    {
                        "web_uri": "{{web_uri}}"
                    }
                ],
                "identity_type": "BC_AUTH_TT",
                "identity_id": "{{identity_id}}",
                "identity_authorized_bc_id": "{{bc_id}}"
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
    "landing_page_url_list": [
        {
            "landing_page_url": "{{landing_page_url}}"
        }
    ],
    "ad_configuration": {
        "call_to_action_id": "{{call_to_action_id}}",
        "product_specific_type": "CUSTOMIZED_PRODUCTS",
        "product_ids": [
            "{{product_id}}"
        ]
    }
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
        "ad_configuration": {
            "call_to_action_id": "{{call_to_action_id}}",
            "dark_post_status": "OFF",
            "deeplink_utm_params": [],
            "phone_info": {},
            "product_ids": [
                "{{product_id}}"
            ],
            "product_specific_type": "CUSTOMIZED_PRODUCTS",
            "tracking_info": {},
            "utm_params": []
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
        "auto_message_list": [],
        "call_to_action_list": [],
        "campaign_id": "{{campaign_id}}",
        "campaign_name": "{{campaign_name}}",
        "create_time": "{{create_time}}",
        "creative_list": [
            {
                "ad_material_id": "{{ad_material_id}}",
                "creative_info": {
                    "ad_format": "SINGLE_VIDEO",
                    "identity_authorized_bc_id": "{{bc_id}}",
                    "identity_id": "{{identity_id}}",
                    "identity_type": "BC_AUTH_TT",
                    "image_info": [
                        {
                            "web_uri": "{{image_web_uri}}"
                        }
                    ],
                    "material_name": "",
                    "video_info": {
                        "file_name": "",
                        "video_id": "{{video_id}}"
                    }
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
