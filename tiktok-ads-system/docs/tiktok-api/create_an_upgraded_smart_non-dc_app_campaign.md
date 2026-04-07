# Create an Upgraded Smart+ non-DC App Campaign

**Doc ID**: 1853377390815233
**Path**: Use Cases/Campaign creation/Create an Upgraded Smart+ Campaign/Create Upgraded Smart+ App Campaigns/Create an Upgraded Smart+ non-DC App Campaign

---

An Upgraded Smart+ non-DC App Campaign is an Upgraded Smart+ App Campaign with iOS 14 dedicated campaign setting disabled and without using a catalog. For such campaigns, you can set the `campaign_type` parameter to `REGULAR_CAMPAIGN` or leave `campaign_type` unspecified.

# Steps

## Steps for App Install Campaigns
An App Install Campaign is an App Campaign that gets people to install and use your app. For such campaigns, you need to set `app_promotion_type` to `APP_INSTALL`.

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
      App install | 
      `app_promotion_type` | 
      `APP_INSTALL` | 
     |
    
| 
      iOS 14 dedicated campaign | 
      **Disabled**

To learn about how to create an Upgraded Smart+ App Campaign with iOS 14 Dedicated Campaign enabled, see [Create an Upgraded Smart+ DC App Campaign](https://business-api.tiktok.com/portal/docs?id=1853377803841537). | 
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
      Campaign name | 
      Specify a valid name | 
      `campaign_name` | 
      Specify a valid value | 
     |
    
| 
      Special ad categories
(Optional) | 
      Disabled or enabled

**Note**: This setting is only supported for advertisers who are registered in the US or Canada.
 | 
      `special_industries` | 
      Not specified or specify a valid value | 
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
        Goal-based budget increase 
 (when Campaign budget strategy is Campaign budget and campaign budget mode is daily) | 
        Any of the following options:
- Enabled
- Disabled | 
        `budget_auto_adjust_strategy` | 
        When `budget_optimize_on` is `true` or not specified and `budget_mode` is `BUDGET_MODE_DYNAMIC_DAILY_BUDGET`:
-  To enable the setting, use the following value:`AUTO_BUDGET_INCREASE`. Allow your budget to automatically increase when your ads are performing well and target CPA, Day 0 target ROAS, and budget requirements are met. Your daily budget will be allowed to automatically increase by 20%, up to 10 times per day, when your budget utilization reaches 90% or more. Your daily budget will reset to your original daily budget each day.
- To disable the setting: Not specified

**Note**: Enabling Goal-based budget increase is currently an allowlist-only feature. If you would like to access it, please contact your TikTok representative.
 | 
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
    "objective_type": "APP_PROMOTION",
    "app_promotion_type": "APP_INSTALL",
    "campaign_type": "REGULAR_CAMPAIGN",
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
        "app_promotion_type": "APP_INSTALL",
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
· App | 
      Any of the following types:
- Android App
- iOS App

**Note**: When you select a campaign budget mode, this setting must be the same across ad groups within the same campaign.
 | 
      `promotion_type`
`app_id` | 
      
- To specify an Android App:Specify an Android App via `app_id`.
- Set `promotion_type` to `APP_ANDROID`.
- To specify an iOS App:Specify an iOS App via `app_id`.
- Set `promotion_type` to `APP_IOS`.
- To obtain the list of Apps under your ad account, use [/app/list/](https://business-api.tiktok.com/portal/docs?id=1740859313270786).For Android Apps, the returned `platform` will be `ANDROID`.
- For iOS Apps, the returned `platform` will be `IOS`.

**Note**: When `budget_optimize_on` is `true` at the campaign level, specify the same `promotion_type` for ad groups within the same campaign.
 | 
     |
    
| 
      Optimization and bidding
· Goal | 
      Any of the following types:
- ClickWe'll deliver your ads to the people most likely to click on your ad.
- InstallWe'll show your ads to the people who are most likely to install your app.
- In-app eventWe'll show your ads to the people who are most likely to perform certain actions within your app.
- ValueWe'll deliver your ads to users that are more likely to make a purchase in order to maximize your total purchase value.In Upgraded Smart+ non-DC App Campaigns, this Goal is only available for Android Apps.
- If you want to enable the Value goal for an iOS App, [Create an Upgraded Smart+ DC App Campaign](https://business-api.tiktok.com/portal/docs?id=1853377803841537).

**Note**: When you select a campaign budget mode, this setting must be the same across ad groups within the same campaign.
 | 
      `optimization_goal` | 
      Any of the following values:
- `CLICK`
- `INSTALL`To use `INSTALL`, you need to ensure third-party tracking has been set up for the selected App.
- To check whether third-party tracking (`tracking_url`) has been configured for an App, use [/app/info/](https://business-api.tiktok.com/portal/docs?id=1740859272887297).
- To add third-party tracking for an existing App, use [/app/update/](https://business-api.tiktok.com/portal/docs?id=1740859300069378). To learn about how to obtain tracking links from a third-party partner, see [Mobile Measurement Partner Tracking](https://ads.tiktok.com/help/article/mobile-measurement-partner-mmp-tracking).
- `IN_APP_EVENT` (with `optimization_event` specified)To use `IN_APP_EVENT`, you need to ensure the specified event (`optimization_event`) is available for the selected App.
- `VALUE` (with `optimization_event` specified)When you set this field to `VALUE`, specify the placement parameters (`placement_type` or both `placement_type` and `placements`) at the same time.
- Learn more about [Value-Based Optimization](https://business-api.tiktok.com/portal/docs?id=1739381743067137).In Upgraded Smart+ non-DC App Campaigns, this Goal is only available for Android Apps.
- If you want to enable the `VALUE` goal for an iOS App, [Create an Upgraded Smart+ DC App Campaign](https://business-api.tiktok.com/portal/docs?id=1853377803841537).

**Note**: When `budget_optimize_on` is `true` at the campaign level, specify the same `optimization_goal` for ad groups within the same campaign.
 | 
     |
    
| 
      Optimization and bidding
· Select in-app event
(when Goal is In-app event) | 
      Any of the following types:
- Standard Event
- Custom Conversion

**Note**: When you select a campaign budget mode, this setting, if specified, must be the same across ad group within the same campaign.
 | 
      `optimization_event`
`custom_conversion_id` | 
      When `optimization_goal` is `IN_APP_EVENT`, specify any of the following:
- A Standard Event through `optimization_event`
- A Custom Conversion along with the associated conversion event through `custom_conversion_id` and `optimization_event`

- To obtain the available optimization events (`optimization_event`) for the App, use [/app/optimization_event/](https://business-api.tiktok.com/portal/docs?id=1740859338750977).
- To obtain the list of Custom Conversions associated with an App, use [/custom_conversion/list/](https://business-api.tiktok.com/portal/docs?id=1842225174460673).To confirm the eligibility of the Custom Conversion for ad group creation:Ensure the returned `optimization_event` matches the `optimization_event` specified during ad group creation.
- Ensure the `activity_status` is `NO_RECENT_ACTIVITY` or `ACTIVE`.

**Note**: When `budget_optimize_on` is `true` at the campaign level, the `optimization_event` and `custom_conversion_id`, if specified, must be the same for ad groups within the same campaign.
 | 
     |
    
| 
      Optimization and bidding
· Select value
(when Goal is Value) | 
      When Goal is Value, use the following type:
- **Purchase value** (also known as VBO IAP, which is short for Value-Based Optimization for in-app purchases)Maximize your revenue from in-app purchases.
- **Ad revenue value** (also known as VBO IAA, which is short for Value-Based Optimization for in-app advertising)Optimize your revenue from in-app advertising.

**Note**: When you select a campaign budget mode, this setting, if specified, must be the same across ad group within the same campaign.
 | 
      `optimization_event` | 
      When `optimization_goal` is `VALUE`:
- To use Purchase value, set `optimization_event` to `ACTIVE_PAY`.
- To use Ad revenue value, set `optimization_event` to `AD_REVENUE_VALUE`.

**Note**: When `budget_optimize_on` is `true` at the campaign level, the `optimization_event`, if specified, must be the same for ad groups within the same campaign.
 | 
     |
    
| 
      Optimization and bidding
· Bid Strategy, (Optional) Target CPA,
and (Optional) Target ROAS | 
      
- If Goal is Click, Install, or In-app event, the strategy can only be **Maximum Delivery** or **Cost Cap**.For Cost Cap, you need to specify a Target CPA at the same time.
- If Goal is Value, the strategy can be **Highest value** or **Minimum ROAS**.For Minimum ROAS, you need to specify a Target ROAS at the same time.

**Note**: 
- The bid strategy must be the same across ad groups within the same campaign.
- When you select a campaign budget mode, the Target CPA or Target ROAS, if specified, must be the same across ad groups within the same campaign.
- Target CPA or Target ROAS is only available when your campaign or ad group budget mode is set to daily.
 | 
      `bid_type`
`bid_price`
`conversion_bid_price`
`deep_bid_type`
`roas_bid` | 
      
- If `optimization_goal` is `CLICK`, `INSTALL`, or `IN_APP_EVENT`:
  	     Set `bid_type` to `BID_TYPE_CUSTOM` (Cost Cap) or `BID_TYPE_NO_BID` (Maximum Delivery). Do not specify `deep_bid_type` and `roas_bid`.
		   If `optimization_goal` is `INSTALL` or `IN_APP_EVENT` and `bid_type` is `BID_TYPE_CUSTOM`, specify `conversion_bid_price` at the same time.
- If `optimization_goal` is `CLICK` and `bid_type` is `BID_TYPE_CUSTOM`, specify `bid_price` at the same time.
		   
		   
- If `optimization_goal` is `VALUE`:
  	          Set `deep_bid_type` to `VO_MIN_ROAS` or `VO_HIGHEST_VALUE`, and set `bid_type` to `BID_TYPE_NO_BID`. Do not specify `conversion_bid_price` and `bid_price`.
				If you set `deep_bid_type` to `VO_MIN_ROAS`, specify `roas_bid` at the same time.
				
  	       

**Note**: 
  
- The `bid_type` must be the same across ad groups within the same campaign.
	
- When `budget_optimize_on` is `true` at the campaign level, the following settings, if specified, must be the same for ad groups within the same campaign:`conversion_bid_price`
- `bid_price`
- `deep_bid_type`
- `roas_bid`
	
- You can only set `bid_type` to `BID_TYPE_CUSTOM` or `deep_bid_type` to `VO_MIN_ROAS` in any of the following scenarios:At the campaign level, `budget_mode` is `BUDGET_MODE_DYNAMIC_DAILY_BUDGET`
- At the ad group level, `budget_mode` is `BUDGET_MODE_DYNAMIC_DAILY_BUDGET`
 | 
     |
    
| 
      Optimization and bidding
· Time window of the bid strategy
(when Goal is Value) | 
      When Goal is Value, use any of the following types:
- Day 7 ROAS or Highest Value
- Day 0 ROAS or Highest Value

**Note**: When you select a campaign budget mode, this setting, if specified, must be the same across ad groups within the same campaign.
 | 
      `vbo_window` | 
      
- When `optimization_goal` is `VALUE`, use any of the following values:`SEVEN_DAYS`
- `ZERO_DAY`
- For example, if you set `deep_bid_type` to `VO_MIN_ROAS`, specify `roas_bid`, and set `vbo_window` to `ZERO_DAY`, the system will aim to keep your average ROAS of the current day around or higher than the target ROAS value.

**Note**: When `budget_optimize_on` is `true` at the campaign level, `vbo_window`, if specified, must be the same for ad groups within the same campaign.
 | 
     |
    
| 
      Optimization and bidding
· Attribution settings | 
      Select from the supported attribution setting options for the specific scenario. | 
      `click_attribution_window`
`view_attribution_window`
`engaged_view_attribution_window`
`attribution_event_count` | 
      To learn about the supported attribution setting options for different scenarios, see [Attribution window and event count - App promotion](https://business-api.tiktok.com/portal/docs?id=1777694366654465#item-link-App promotion). | 
     |
    
| 
      Optimization and bidding
· Billing event | 
      
- If Goal is Click, the billing event should be **CPC**.
- If Goal is Install, In-app event, or Value, the billing event should be **oCPM**.

**Note**: When you select a campaign budget mode, the billing event must be the same across ad groups within the same campaign.
 | 
      `billing_event` | 
      
- If `optimization_goal` is `CLICK`, set this field to `CPC`.
- If `optimization_goal` is `INSTALL`, `IN_APP_EVENT`, or `VALUE`, set this field to `OCPM`.

**Note**: When `budget_optimize_on` is `true` at the campaign level, specify the same `billing_event` for ad groups within the same campaign.
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
· Goal-based budget increase (when Goal is Value) | 
      Enabled or disabled

To enable this setting, the following conditions should be met:
- At the campaign level: CBO is disabled.
- At the ad group level:Ad group budget is Daily
- Goal is Value
- Bid Strategy is Target ROAS
- Time window of the bid strategy is Day 0 ROAS | 
      `budget_auto_adjust_strategy` | 
      Use any of the following values:
- `AUTO_BUDGET_INCREASE`: To enable Goal-based budget increase. Allow your budget to automatically increase when your ads are performing well and target CPA, Day 0 target ROAS, and budget requirements are met. Your daily budget will be allowed to automatically increase by 20%, up to 10 times per day, when your budget utilization reaches 90% or more. Your daily budget will reset to your original daily budget each day.
- `UNSET`: To disable Goal-based budget increase.
You can only set this field to `AUTO_BUDGET_INCREASE` when the following conditions are all met:
- At the campaign level: `budget_optimize_on` is `false`.
- At the ad group level:`budget_mode` is `BUDGET_MODE_DYNAMIC_DAILY_BUDGET`.
- `optimization_goal` is `VALUE`.
- `deep_bid_type` is `VO_MIN_ROAS`.
- `vbo_window` is `ZERO_DAY`.

**Note**: Enabling Goal-based budget increase is currently an allowlist-only feature. If you would like to access it, please contact your TikTok representative.
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
      Any of the following values:
- **Automatic targeting**You can use automatic targeting to leverage real-time data and machine learning to target audiences most likely to engage with your ads.
- **Custom targeting**You can use custom targeting settings to precisely control who sees your ads. This may limit delivery and impact campaign performance.
To learn about the supported targeting settings for each mode, see [Available targeting settings for different targeting optimization modes](https://business-api.tiktok.com/portal/docs?id=1847839827327106). | 
      `targeting_optimization_mode` | 
      Any of the following values:
- `AUTOMATIC`
- `MANUAL`To learn about the supported targeting settings for each mode, see [Available targeting settings for different targeting optimization modes](https://business-api.tiktok.com/portal/docs?id=1847839827327106). | 
     |
    
| 
      Placements and brand safety
· Placement | 
      Any of the following types:
- **Automatic Placement**
- **Select specific placements**:TikTok
- Global App Bundle
- Pangle | 
      `placement_type`
`placements` | 
      
- To use Automatic Placement, do not specify `placement_type` and `placements`.The system will automatically configure placements for your Upgraded Smart+ Ad Groups based on your other settings and select high-quality traffic from various placements to deliver better results. If provided, the parameters `placement_type` and `placements` will be ignored.
- To retrieve the exact placement setting of an Upgraded Smart+ Ad Group, use [/smart_plus/adgroup/get/](https://business-api.tiktok.com/portal/docs?id=1843314879617026).
- To use specific placements, set `placement_type` to `PLACEMENT_TYPE_NORMAL` and specify one or more of the following placements in `placements`:`PLACEMENT_TIKTOK`
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
  

#### Example
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
    "app_id": "{{app_id}}",
    "promotion_type": "APP_ANDROID",
    "optimization_goal": "INSTALL",
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
        "adgroup_name": "smart_plus_adg_app_non_DC_Android_0723",
        "advertiser_id": "{{advertiser_id}}",
        "app_id": "{{app_id}}",
        "attribution_event_count": "ONCE",
        "bid_type": "BID_TYPE_CUSTOM",
        "billing_event": "OCPM",
        "campaign_id": "{{campaign_id}}",
        "campaign_name": "{{campaign_name}}",
        "click_attribution_window": "SEVEN_DAYS",
        "comment_disabled": false,
        "conversion_bid_price": {{conversion_bid_price}},
        "create_time": "{{create_time}}",
        "dayparting": "111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111",
        "deep_bid_type": "DEFAULT",
        "engaged_view_attribution_window": "SEVEN_DAYS",
        "modify_time": "{{modify_time}}",
        "optimization_event": "ACTIVE",
        "optimization_goal": "INSTALL",
        "placement_type": "PLACEMENT_TYPE_NORMAL",
        "placements": [
            "PLACEMENT_TIKTOK",
            "PLACEMENT_GLOBAL_APP_BUNDLE"
        ],
        "promotion_type": "APP_ANDROID",
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
      
- To have the system auto-generate the ad name, set this field to `""` (empty string).
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
      Specify a valid value.

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
      Selling points (Optional) | 
      Disabled | 
      N/A | 
      N/A | 
     |
    
| 
      Call to action | 
      Any of the following options:
- Dynamic
- Standard

**Note**: When you use a Spark Ads identity, you can only use dynamic call to action.
 | 
      `call_to_action_id`
`call_to_action_list` | 
      
- To use dynamic call to action, specify `call_to_action_id`.
- To use standard call to action, specify `call_to_action_list`.

**Note**: If you set `identity_type` within the `creative_info` object to `TT_USER`, `BC_AUTH_TT`, or `AUTH_CODE`, `call_to_action_id` is required.
 | 
     |
    
| 
      Interactive add-ons
(Optional)
(When the ad creatives include videos or video posts ) | 
      Disabled or enabled with up to one add-on in any of the following types:
- Display Card
- Countdown Sticker
- Gift Code Sticker | 
      `interactive_add_on_list` | 
      Not specified or specify up to one ID of any of the following add-on types:
- Countdown Sticker
- Gift Code Sticker
- Display Card

**Note**: You can only use add-ons when `creative_list` contains video creatives, including videos and TikTok video posts.

To create an interactive add-on (creative portfolio), use [/creative/portfolio/create/](https://business-api.tiktok.com/portal/docs?id=1739091950439426).
- To learn about how to obtain the ID of a Display Card portfolio, see [Cards](https://business-api.tiktok.com/portal/docs?id=1749019652141058#item-link-Display Card).
- To learn about how to obtain the ID of a Countdown Sticker or Gift Code Sticker portfolio, see [Stickers](https://business-api.tiktok.com/portal/docs?id=1749019667506177). | 
     |
    
| 
      Destination | 
      When the promoted App is an Android App: Google Play

When the promoted App is an iOS App: App Store | 
      `landing_page_url_list`
`page_list` | 
      
- When `promotion_type` at the ad group level is `APP_ANDROID`, you can only set the Destination as Google Play.Do not specify `landing_page_url_list` and `page_list`.
- When `promotion_type` at the ad group level is `APP_IOS`, you can only set the Destination as App Store.Do not specify `landing_page_url_list` and `page_list`. | 
     |
    
| 
      Deferred deeplink
(Optional)
(When Destination is Google Play/App Store) | 
      Disabled or enabled with a valid deeplink.
A deferred deeplink sends the user to a specific page when they open your app for the first time after installing. It must be used with a third-party tracking link. | 
      `deeplink_type` | 
      Not specified or specify `DEFERRED_DEEPLINK` | 
     |
    
| 
      `deeplink` | 
      
- When `deeplink_type` is not specified:Not specified
- When `deeplink_type` is `DEFERRED_DEEPLINK`Specify a custom deeplink | 
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
(code http)
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
    "interactive_add_on_list": [
        {
            "card_id": "{{card_id}}"
        }
    ],
    "ad_configuration": {
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
            "tracking_info": {
                "tracking_app_id": "{{tracking_app_id}}"
            },
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
                    "material_name": "Image carousel 1",
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
        "interactive_add_on_list": [
            {
                "card_id": "{{card_id}}"
            }
        ],
        "landing_page_url_list": [],
        "modify_time": "{{modify_time}}",
        "operation_status": "ENABLE",
        "page_list": [],
        "secondary_status": "AD_STATUS_AUDIT",
        "smart_plus_ad_id": "{{smart_plus_ad_id}}"
    }
}
(/code)
```

## Steps for App Retargeting Campaigns
An App Retargeting Campaign is an App Campaign that re-engages existing app users to take action in your app. For such campaigns, you need to set `app_promotion_type` to `APP_RETARGETING`.

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
      App retargeting | 
      `app_promotion_type` | 
      `APP_RETARGETING` | 
     |
    
| 
      iOS 14 dedicated campaign | 
      **Disabled** | 
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
      Campaign name | 
      Specify a valid name | 
      `campaign_name` | 
      Specify a valid value | 
     |
    
| 
      Special ad categories
(Optional) | 
      Disabled or enabled

**Note**: This setting is only supported for advertisers who are registered in the US or Canada.
 | 
      `special_industries` | 
      Not specified or specify a valid value | 
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
        Goal-based budget increase 
 (when Campaign budget strategy is Campaign budget and campaign budget mode is daily) | 
        Any of the following options:
- Enabled
- Disabled | 
        `budget_auto_adjust_strategy` | 
        When `budget_optimize_on` is `true` or not specified and `budget_mode` is `BUDGET_MODE_DYNAMIC_DAILY_BUDGET`:
-  To enable the setting, use the following value:`AUTO_BUDGET_INCREASE`. Allow your budget to automatically increase when your ads are performing well and target CPA, Day 0 target ROAS, and budget requirements are met. Your daily budget will be allowed to automatically increase by 20%, up to 10 times per day, when your budget utilization reaches 90% or more. Your daily budget will reset to your original daily budget each day.
- To disable the setting: Not specified

**Note**: Enabling Goal-based budget increase is currently an allowlist-only feature. If you would like to access it, please contact your TikTok representative.
 | 
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
    
| 
      Realtime API (RTA)
(Optional) | 
      Enabled or disabled

**Note**: The available placements at the ad group level might vary based on your RTA setting.
 | 
      `rta_id` | 
      Specify one of the RTA IDs associated with your ad account.

To obtain the list of RTA IDs associated with your ad account, contact your TikTok representative.

**Note**: The available placement setting (`placement_type` and `placements`) at the ad group level might vary based on your `rta_id` configuration.
 | 
     |
    
| 
      Use RTA bid 
(Optional) | 
      
- When RTA is disabled, this setting is not supported.
- When RTA is enabled, you can either enable or disable this setting. | 
      `rta_bid_enabled` | 
      
- When `rta_id` is not specified:`false` or not specified
- When `rta_id` is specified, use any of the following configurations :`true`
- `false` or not specified | 
     |
  

#### Example
**Creating a CBO campaign**

Request
```xcodeblock
(code http)
curl --location --request POST 'https://business-api.tiktok.com//open_api/v1.3/smart_plus/campaign/create/' \
--header 'Access-Token: {{Access-Token}}' \
--header 'Content-Type: application/json' \
--data '{
    "advertiser_id": "{{advertiser_id}}",
    "request_id": "{{request_id}}",
    "objective_type": "APP_PROMOTION",
    "app_promotion_type": "APP_RETARGETING",
    "campaign_type": "REGULAR_CAMPAIGN",
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
        "app_promotion_type": "APP_RETARGETING",
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
· App | 
      Any of the following types:
- Android App
- iOS App

**Note**: When you select a campaign budget mode, this setting must be the same across ad groups within the same campaign.
 | 
      `promotion_type`
`app_id` | 
      
- To specify an Android App:Specify an Android App via `app_id`.
- Set `promotion_type` to `APP_ANDROID`.
- To specify an iOS App:Specify an iOS App via `app_id`.
- Set `promotion_type` to `APP_IOS`.To obtain the list of Apps under your ad account, use [/app/list/](https://business-api.tiktok.com/portal/docs?id=1740859313270786).
- For Android Apps, the returned `platform` will be `ANDROID`.
- For iOS Apps, the returned `platform` will be `IOS`.

**Note**: When`budget_optimize_on` is `true` at the campaign level, specify the same `promotion_type` for ad groups within the same campaign.
 | 
     |
    
| 
      Agree to the Compliance Assurance Policy for Gaming Advertisers on TikTok | 
      Any of the following options:
- AgreedBy agreeing to the policy, you confirm and attest that any gaming application, product or service (game) you desire to advertise on TikTok, including any associated URL(s), (a) complies with all applicable laws and regulations of the jurisdictions where the game can be accessed or played, and upon request, can provide supporting documentation as evidence of why the game is not considered illegal gambling or lottery; and (b) has not been and is not part of any investigation or lawsuit regarding the game's legality or regulatory compliance.
- Not agreed | 
      `gaming_ad_compliance_agreement` | 
      Any of the following values:
- `true`
- `false`

**Note**: Agreeing to the Compliance Assurance Policy for Gaming Advertisers on TikTok is currently an allowlist-only feature. If you would like to access it, please contact your TikTok representative.
 | 
     |
    
| 
      Optimization and bidding
· Goal | 
      Any of the following types:
- In-app eventWe'll show your ads to the people who are most likely to perform certain actions within your app.
- Value We'll deliver your ads to users that are more likely to make a purchase in order to maximize your total purchase value.

**Note**: When you select a campaign budget mode, this setting must be the same across ad groups within the same campaign.
 | 
      `optimization_goal` | 
      Any of the following values:
- `IN_APP_EVENT` (with `optimization_event` specified)To use `IN_APP_EVENT`, you need to ensure the specified event (`optimization_event`) is available for the selected App. 
- `VALUE` (with `optimization_event` specified)When you set this field to `VALUE`, specify the placement parameters (`placement_type` or both `placement_type` and `placements`) at the same time.

**Note**: When`budget_optimize_on` is `true` at the campaign level, specify the same `optimization_goal`for ad groups within the same campaign.
 | 
     |
    
| 
      Optimization and bidding
· Select in-app event
(when Goal is In-app event) | 
      Any of the following types:
- Standard Event
- Custom Conversion

**Note**: When you select a campaign budget mode, this setting, if specified, must be the same across ad group within the same campaign.
 | 
      `optimization_event`
`custom_conversion_id` | 
      When `optimization_goal` is `IN_APP_EVENT`, specify any of the following:
- A Standard Event through `optimization_event`
- A Custom Conversion along with the associated conversion event through `custom_conversion_id` and `optimization_event`
- To obtain the available optimization events (`optimization_event`) for the App, use [/app/optimization_event/](https://business-api.tiktok.com/portal/docs?id=1740859338750977).
- To obtain the list of Custom Conversions associated with an App, use [/custom_conversion/list/](https://business-api.tiktok.com/portal/docs?id=1842225174460673).To confirm the eligibility of the Custom Conversion for ad group creation:Ensure the returned `optimization_event` matches the `optimization_event` specified during ad group creation.
- Ensure the `activity_status` is `NO_RECENT_ACTIVITY` or `ACTIVE`.

**Note**: When `budget_optimize_on` is `true` at the campaign level, the `optimization_event` and `custom_conversion_id`, if specified, must be the same for ad groups within the same campaign.
 | 
     |
    
| 
      Optimization and bidding
· Optimization event
(when Goal is Value) | 
      **Purchase value** (also known as VBO IAP, which is short for Value-Based Optimization for in-app purchases)
- Maximize your revenue from in-app purchases.

**Note**: When you select a campaign budget mode, this setting, if specified, must be the same across ad group within the same campaign.
 | 
      `optimization_event` | 
      When `optimization_goal` is `VALUE`: `ACTIVE_PAY` .

**Note**: When `budget_optimize_on` is `true` at the campaign level, the `optimization_event`, if specified, must be the same for ad groups within the same campaign.
 | 
     |
    
| 
      Optimization and bidding
· Bid Strategy, (Optional) Target CPA, 
and (Optional) Target ROAS | 
      
- If Goal is In-app event, the strategy can only be Maximum Delivery or Cost Cap.For Cost Cap, you need to specify a Target CPA at the same time.
- If Goal is Value, the strategy can be Highest value or Minimum ROAS.For Minimum ROAS, you need to specify a Target ROAS at the same time.

**Note**: 
- The bid strategy must be the same across ad groups within the same campaign.
- When you select a campaign budget mode, the Target CPA or Target ROAS, if specified, must be the same across ad groups within the same campaign.
- Target CPA or Target ROAS is only available when your campaign or ad group budget mode is set to daily.
 | 
      `bid_type`
`bid_price`
`conversion_bid_price`
`deep_bid_type`
`roas_bid` | 
      
- If `optimization_goal` is `IN_APP_EVENT`:Set `bid_type` to `BID_TYPE_CUSTOM` (Cost Cap) or `BID_TYPE_NO_BID` (Maximum Delivery). Do not specify `deep_bid_type` and `roas_bid`.If `optimization_goal` is `IN_APP_EVENT` and `bid_type` is `BID_TYPE_CUSTOM`, specify `conversion_bid_price` at the same time.
- If `optimization_goal` is `VALUE`:Set `deep_bid_type` to `VO_MIN_ROAS` or `VO_HIGHEST_VALUE`, and set `bid_type` to `BID_TYPE_NO_BID`. Do not specify `conversion_bid_price` and `bid_price`.If you set `deep_bid_type` to `VO_MIN_ROAS`, specify `roas_bid` at the same time.

**Note**: 
- The `bid_type` must be the same across ad groups within the same campaign.
-  When `budget_optimize_on` is `true` at the campaign level, the following settings, if specified, must be the same for ad groups within the same campaign:`conversion_bid_price`
- `deep_bid_type`
- `roas_bid`
- You can only set `bid_type` to `BID_TYPE_CUSTOM` or `deep_bid_type` to `VO_MIN_ROAS` in any of the following scenarios:At the campaign level, `budget_mode` is `BUDGET_MODE_DYNAMIC_DAILY_BUDGET` 
- At the ad group level, `budget_mode` is `BUDGET_MODE_DYNAMIC_DAILY_BUDGET`
 | 
     |
    
| 
      Optimization and bidding
· Attribution settings | 
      Select from the supported attribution setting options for the specific scenario. | 
      `click_attribution_window`
`view_attribution_window`
`engaged_view_attribution_window`
`attribution_event_count` | 
      To learn about the supported attribution setting options for different scenarios, see [Attribution window and event count - App promotion](https://business-api.tiktok.com/portal/docs?id=1777694366654465#item-link-App%20promotion). | 
     |
    
| 
      Optimization and bidding
· Billing event | 
      oCPM

**Note**: When you select a campaign budget mode, the billing event must be the same across ad groups within the same campaign.
 | 
      `billing_event` | 
      `OCPM`

**Note**: When `budget_optimize_on` is `true` at the campaign level, specify the same `billing_event` for ad groups within the same campaign.
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
· Goal-based budget increase (when Goal is Value) | 
      Enabled or disabled

To enable this setting, the following conditions should be met:
- At the campaign level: CBO is disabled.
- At the ad group level:Ad group budget is Daily
- Goal is Value
- Bid Strategy is Target ROAS
- Time window of the bid strategy is Day 0 ROAS | 
      `budget_auto_adjust_strategy` | 
      Use any of the following values:
- `AUTO_BUDGET_INCREASE`: To enable Goal-based budget increase. Allow your budget to automatically increase when your ads are performing well and target CPA, Day 0 target ROAS, and budget requirements are met. Your daily budget will be allowed to automatically increase by 20%, up to 10 times per day, when your budget utilization reaches 90% or more. Your daily budget will reset to your original daily budget each day.
- `UNSET`: To disable Goal-based budget increase.
You can only set this field to `AUTO_BUDGET_INCREASE` when the following conditions are all met:
- At the campaign level: `budget_optimize_on` is `false`.
- At the ad group level:`budget_mode` is `BUDGET_MODE_DYNAMIC_DAILY_BUDGET`.
- `optimization_goal` is `VALUE`.
- `deep_bid_type` is `VO_MIN_ROAS`.
- `vbo_window` is `ZERO_DAY`.

**Note**: Enabling Goal-based budget increase is currently an allowlist-only feature. If you would like to access it, please contact your TikTok representative.
 | 
     |
    
| 
      Budget and schedule
· Add spend target per ad group
  · Daily minimum | 
      
- When you use a daily campaign budget:When Bid strategy is Maximum Delivery (Highest volume), you can enable or disable this setting.
- When Bid Strategy is Target CPA or Target ROAS, this setting is not supported.
- When you use a lifetime campaign budget or an ad group budget, this setting is not supported. | 
      `min_budget` | 
      
- When `budget_optimize_on` is `true` and `budget_mode` is `BUDGET_MODE_DYNAMIC_DAILY_BUDGET` at the campaign level:When `bid_type` is `BID_TYPE_NO_BID` at the ad group level , you can either specify a valid value through this field or leave it unspecified.
- When `bid_type` is `BID_TYPE_CUSTOM` or `deep_bid_type` is `VO_HIGHEST_VALUE` at the ad group level, this field is not supported.
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
      Any of the following modes:
- **Automatic targeting**You can use automatic targeting to leverage real-time data and machine learning to target audiences most likely to engage with your ads.
- **Custom targeting**You can use custom targeting settings to precisely control who sees your ads. This may limit delivery and impact campaign performance.
To learn about the supported targeting settings for each mode, see [Available targeting settings for different targeting optimization modes in Upgraded Smart+ App Retargeting Campaigns](#item-link-Available targeting settings for different targeting optimization modes in Upgraded Smart+ App Retargeting Campaigns). | 
      `targeting_optimization_mode` | 
      Any of the following values:
- `AUTOMATIC`
- `MANUAL`To learn about the supported targeting settings for each mode, see [Available targeting settings for different targeting optimization modes in Upgraded Smart+ App Retargeting Campaigns](#item-link-Available targeting settings for different targeting optimization modes in Upgraded Smart+ App Retargeting Campaigns). | 
     |
    
| 
      Placements and brand safety
· Placement | 
      Any of the following types:
- **Automatic Placement**
- **Select specific placements**:TikTok
- Global App Bundle
- Pangle

**Note**: When Realtime API is enabled at the campaign level, the only supported type is **Select specific placements** with TikTok only placement.
 | 
      `placement_type`
`placements` | 
      
- To use Automatic Placement, do not specify `placement_type` and `placements`.The system will automatically configure placements for your Upgraded Smart+ Ad Groups based on your other settings and select high-quality traffic from various placements to deliver better results. If provided, the parameters `placement_type` and `placements` will be ignored.
- To retrieve the exact placement setting of an Upgraded Smart+ Ad Group, use [/smart_plus/adgroup/get/](https://business-api.tiktok.com/portal/docs?id=1843314879617026).
- To use specific placements, set `placement_type` to `PLACEMENT_TYPE_NORMAL` and specify one or more of the following placements in `placements`:`PLACEMENT_TIKTOK`
- `PLACEMENT_PANGLE`
- `PLACEMENT_GLOBAL_APP_BUNDLE`

**Note**: When `rta_id` is specified at the campaign level, set `placement_type` to `PLACEMENT_TYPE_NORMAL` and `placements` to `["PLACEMENT_TIKTOK"]`.
 | 
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
  

#### Available targeting settings for different targeting optimization modes in Upgraded Smart+ App Retargeting Campaigns

 

  
    
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
      Specify valid locations | 
      `location_ids` or `zipcode_ids` or both | 
      Specify valid values | 
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
· Retargeting custom audience
(Optional)
  · Include audience (Optional) | 
      Enabled or disabled

**Note**: When at the campaign level Realtime API is enabled, this setting is not supported.
 | 
      `audience_ids` | 
      Specify valid values or not specified

**Note**: When at the campaign level `rta_id` is specified, this setting is not supported.
 | 
     |
    
| 
      Audience controls
· Retargeting custom audience
(Optional)
  · Exclude audience (Optional) | 
      Enabled or disabled

**Note**: When at the campaign level Realtime API is enabled, this setting is not supported.
 | 
      `excluded_audience_ids` | 
      Specify valid values or not specified

**Note**: When at the campaign level `rta_id` is specified, this setting is not supported.
 | 
     |
    
| 
      Audience suggestions
· Age
 (Optional)

**Note**: Audience suggestions guide automatic targeting by choosing additional audience settings. These serve as suggestions only, and delivery to those audiences is not guaranteed.
 | 
      Enabled or disabled

**Note**: When at the campaign level Realtime API is enabled, this setting is not supported.
 | 
      `age_groups` | 
      Specify valid values or not specified

**Note**: When at the campaign level `rta_id` is specified, this setting is not supported.
 | 
     |
    
| 
      Audience suggestions
· Gender
 (Optional) | 
      Enabled or disabled

**Note**: When at the campaign level Realtime API is enabled, this setting is not supported.
 | 
      `gender` | 
      Specify valid values or not specified

**Note**: When at the campaign level `rta_id` is specified, this setting is not supported.
 | 
     |
    
| 
      Audience suggestions
· Interests & behaviors
  · Interests
 (Optional) | 
      Enabled or disabled

**Note**: When at the campaign level Realtime API is enabled, this setting is not supported.
 | 
      `interest_category_ids`
`interest_keyword_ids` | 
      Specify valid values or not specified

**Note**: When at the campaign level `rta_id` is specified, this setting is not supported.
 | 
     |
    
| 
      Audience suggestions
· Interests & behaviors
  · Purchase intention
 (Optional) | 
      Enabled or disabled

**Note**: When at the campaign level Realtime API is enabled, this setting is not supported.
 | 
      `purchase_intention_keyword_ids` | 
      Specify valid values or not specified

**Note**: When at the campaign level `rta_id` is specified, this setting is not supported.
 | 
     |
    
| 
      Audience suggestions
· Interests & behaviors
  · Video interactions
  · Creator interactions
  · Hashtag interactions
(Optional) | 
      Enabled or disabled

**Note**: When at the campaign level Realtime API is enabled, this setting is not supported.
 | 
      `actions` | 
      Specify valid values or not specified

**Note**: When at the campaign level `rta_id` is specified, this setting is not supported.
 | 
     |
    
| 
      Custom targeting
(`targeting_optimization_mode` 
as `MANUAL`) | 
      Demographics
· Location | 
      Specify a valid value.
If a catalog is specified, the location should match or be the subset of the targeting location of your catalog. | 
      `location_ids` or `zipcode_ids` or both | 
      Specify a valid value.
If a catalog is specified, specify IDs of locations that match or are a subset of the targeting location of `catalog_id`.
To obtain the targeting location of a catalog, use [/catalog/get/](https://business-api.tiktok.com/portal/docs?id=1740315452868610) and check the returned `country`. | 
     |
    
| 
      Demographics
· HFSS Product/Brand | 
      Enabled or disabled
- You can enable this setting when your targeting locations include locations in the UK, Australia, New Zealand, and the European Union. | 
      `is_hfss` | 
      `true` or `false`.

You can set it to `true` when your targeting locations include locations in the UK, Australia, New Zealand, and the European Union. | 
     |
    
| 
      Demographics
· LHF (Less Healthy Foods) compliance | 
      Enabled or disabled
- This setting must be enabled when your targeting locations include locations in the UK and HFSS Product/Brand is enabled. | 
      `is_lhf_compliance` | 
      `true` or `false`.

 You need to set it to `true` when your targeting locations include locations in the UK and `is_hfss` is `true`. | 
     |
    
| 
      Demographics
· Age
 (Optional) | 
      Enabled or disabled | 
      `age_groups` | 
      Specify valid values or not specified | 
     |
    
| 
      Demographics
· Gender
 (Optional) | 
      Enabled or disabled | 
      `gender` | 
      Specify valid values or not specified | 
     |
    
| 
      Demographics
· Languages
 (Optional) | 
      Enabled or disabled | 
      `languages` | 
      Specify valid values or not specified | 
     |
    
| 
      Custom audience
· Include audience
 (Optional) | 
      Enabled or disabled

**Note**: When at the campaign level Realtime API is enabled, this setting is not supported.
 | 
      `audience_ids` | 
      Specify valid values or not specified

**Note**: When at the campaign level `rta_id` is specified, this setting is not supported.
 | 
     |
    
| 
      Custom audience
· Exclude audience
 (Optional) | 
      Enabled or disabled

**Note**: When at the campaign level Realtime API is enabled, this setting is not supported.
 | 
      `excluded_audience_ids` | 
      Specify valid values or not specified

**Note**: When at the campaign level `rta_id` is specified, this setting is not supported.
 | 
     |
    
| 
      Detailed targeting
· Interests & behaviors
  · Interests
 (Optional) | 
      Enabled or disabled | 
      `interest_category_ids`
`interest_keyword_ids` | 
      Specify valid values or not specified | 
     |
    
| 
      Detailed targeting
· Interests & behaviors
  · Purchase intention
 (Optional) | 
      Enabled or disabled | 
      `purchase_intention_keyword_ids` | 
      Specify valid values or not specified | 
     |
    
| 
      Detailed targeting
· Interests & behaviors
  · Video interactions
  · Creator interactions
  · Hashtag interactions
 (Optional) | 
      Enabled or disabled | 
      `actions` | 
      `true` or `false` | 
     |
   
| 
      Detailed targeting
· Spending power (Optional) | 
      Enabled or disabled | 
      `spending_power` | 
      Specify valid values or not specified | 
     |
    
| 
      Detailed targeting
· Household income (Optional) | 
      Enabled or disabled | 
      `household_income` | 
      Specify valid values or not specified | 
     |
    
| 
      Device
· Operating system (Optional) | 
      Enabled or disabled | 
      `operating_systems` | 
      Specify valid values or not specified | 
     |
    
| 
      Device
· OS versions (Optional) | 
      Enabled or disabled | 
      `min_android_version`
`min_ios_version` | 
      Specify valid values or not specified | 
     |
    
| 
      Device
· Device model (Optional) | 
      Enabled or disabled | 
      `device_model_ids` | 
      Specify valid values or not specified | 
     |
    
| 
      Device
· Connection type (Optional) | 
      Enabled or disabled | 
      `network_types` | 
      Specify valid values or not specified | 
     |
    
| 
      Device
· Carriers (Optional) | 
      Enabled or disabled | 
      `carrier_ids` | 
      Specify valid values or not specified | 
     |
    
| 
      Device
· Internet service provider (Optional) | 
      Enabled or disabled | 
      `isp_ids` | 
      Specify valid values or not specified | 
     |
    
| 
      Device
· Device price (Optional) | 
      Enabled or disabled | 
      `device_price_ranges` | 
      Specify valid values or not specified | 
     |
    
| 
      Use saved audience (Optional) | 
      Enabled or disabled | 
      `saved_audience_id` | 
      Specify valid values or not specified | 
     |
  

#### Example
Request
```xcodeblock
(code http)
curl --location --request POST 'https://business-api.tiktok.com//open_api/v1.3/smart_plus/adgroup/create/' \
--header 'Access-Token: {{Access-Token}}' \
--header 'Content-Type: application/json' \
--data '{
    "advertiser_id": "{{advertiser_id}}",
    "campaign_id": "{{campaign_id}}",
    "request_id": "{{request_id}}",
    "adgroup_name": "{{adgroup_name}}",
    "app_id": "{{app_id}}",
    "promotion_type": "APP_IOS",
    "optimization_goal": "IN_APP_EVENT",
    "optimization_event": "ADD_PAYMENT_INFO",
    "bid_type": "BID_TYPE_NO_BID",
    "billing_event": "OCPM",
    "schedule_type": "SCHEDULE_START_END",
    "schedule_start_time": "{{schedule_start_time}}",
    "schedule_end_time": "{{schedule_end_time}}",
    "targeting_optimization_mode": "AUTOMATIC",
    "targeting_spec": {
        "location_ids": [
            "{{location_id}}"
        ],
        "spc_audience_age": "OVER_EIGHTEEN",
        "excluded_audience_ids": [
            "{{excluded_audience_id}",
            "{{excluded_audience_id}}"
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
        "app_id": "{{app_id}}",
        "attribution_event_count": "ONCE",
        "bid_type": "BID_TYPE_NO_BID",
        "billing_event": "OCPM",
        "budget": 0,
        "budget_mode": "BUDGET_MODE_INFINITE",
        "campaign_id": "{{campaign_id}}",
        "campaign_name": "{{campaign_name}}",
        "click_attribution_window": "SEVEN_DAYS",
        "comment_disabled": false,
        "conversion_bid_price": 0,
        "create_time": "{{create_time}}",
        "dayparting": "111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111",
        "deep_bid_type": "AEO",
        "engaged_view_attribution_window": "SEVEN_DAYS",
        "gaming_ad_compliance_agreement": "OFF",
        "is_hfss": false,
        "is_lhf_compliance": false,
        "min_budget": 0,
        "modify_time": "{{modify_time}}",
        "operation_status": "ENABLE",
        "optimization_event": "ADD_PAYMENT_INFO",
        "optimization_goal": "IN_APP_EVENT",
        "pacing": "PACING_MODE_SMOOTH",
        "phone_info": {},
        "placement_type": "PLACEMENT_TYPE_AUTOMATIC",
        "placements": [
            "PLACEMENT_TIKTOK",
            "PLACEMENT_GLOBAL_APP_BUNDLE",
            "PLACEMENT_PANGLE"
        ],
        "promotion_type": "APP_IOS",
        "schedule_end_time": "{{schedule_end_time}}",
        "schedule_start_time": "{{schedule_start_time}}",
        "schedule_type": "SCHEDULE_START_END",
        "search_result_enabled": false,
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
            "brand_safety_type": "EXPANDED_INVENTORY",
            "excluded_audience_ids": [
                "{{excluded_audience_id}}",
                "{{excluded_audience_id}}"
            ],
            "gender": "GENDER_UNLIMITED",
            "location_ids": [
                "{{location_id}}"
            ],
            "operating_systems": [
                "IOS"
            ],
            "spc_audience_age": "OVER_EIGHTEEN",
            "spending_power": "ALL"
        },
        "video_download_disabled": false,
        "view_attribution_window": "ONE_DAY"
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
      For a single ad, you can include one to **50 ad creatives **that can consist of the following types:
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
      Selling points (Optional) | 
      Disabled | 
      N/A | 
      N/A | 
     |
    
| 
      Call to action | 
      Dynamic | 
      `call_to_action_id` | 
      Specify a valid value | 
     |
    
| 
      `call_to_action_list` | 
      Not specified | 
     |
    
| 
      Interactive add-ons
(Optional)
(When the ad creatives include videos or video posts ) | 
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
- You can only use add-ons when `creative_list` contains video creatives, including videos and TikTok video posts.
To create an interactive add-on (creative portfolio), use [/creative/portfolio/create/](https://business-api.tiktok.com/portal/docs?id=1739091950439426).
- To learn about how to obtain the ID of a Display Card portfolio, see [Cards](https://business-api.tiktok.com/portal/docs?id=1749019652141058#item-link-Display%20Card).
- To learn about how to obtain the ID of a Countdown Sticker or Gift Code Sticker portfolio, see [Stickers](https://business-api.tiktok.com/portal/docs?id=1749019667506177). | 
     |
    
| 
      Destination | 
      
- When the promoted App is an Android App: Google Play or TikTok Instant Page
- When the promoted App is an iOS App: App Store | 
      `landing_page_url_list`
`page_list` | 
      
- When `promotion_type` at the ad group level is `APP_ANDROID`, you can set the Destination to Google Play or TikTok Instant Page.To set the Destination to Google Play, do not specify `landing_page_url_list` and `page_list`.
- To set the Destination to TikTok Instant Page, specify a valid TikTok Instant Page via `landing_page_url_list` and do not specify `landing_page_url_list`.The app details on the TikTok Instant Page should match the promoted `app_id` at the ad group level.
- When `promotion_type` at the ad group level is `APP_IOS`, you can only set the Destination as App Store.Do not specify `landing_page_url_list` and `page_list`. | 
     |
    
| 
      Add specific custom product page as destination (Optional)
(When Destination is App Store) | 
      When the promoted App is an iOS App:
- Disabled or enabled with a valid custom product page. | 
      `custom_product_page_list` | 
      When `promotion_type` at the ad group level is `APP_IOS`: Not specified or specify a custom product page. | 
     |
    
| 
      Direct users to deeplink first
(Optional)
(When Destination is Google Play/App Store) | 
      Disabled or enabled with a valid deeplink.
A deeplink is a URL that takes people to a specific location within your app, such as a product page. | 
      `deeplink_type` | 
      Not specified or specify `NORMAL` | 
     |
    
| 
      `deeplink` | 
      
- When `deeplink_type` is not specified:Not specified
- When `deeplink_type` is `NORMAL`:Specify a custom deeplink. Scheme, Universal, and App Link formats are supported. | 
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
(code http)
curl --location --request POST 'https://business-api.tiktok.com//open_api/v1.3/smart_plus/ad/create/' \
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
                "identity_type": "TT_USER",
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
    "custom_product_page_list": [
        {
            "custom_product_page_url": "{{custom_product_page_url}}"
        }
    ],
    "deeplink_list": [
        {
            "deeplink": "{{deeplink}}",
            "deeplink_type": "NORMAL"
        }
    ],
    "ad_configuration": {
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
            "dark_post_status": "OFF",
            "deeplink_utm_params": [],
            "fallback_type": "UNSET",
            "phone_info": {},
            "tracking_info": {
                "tracking_app_id": "{{tracking_app_id}}"
            },
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
            }
        ],
        "custom_product_page_list": [
            {
                "custom_product_page_url": "{{custom_product_page_url}}"
            }
        ],
        "deeplink_list": [
            {
                "deeplink": "{{deeplink}}",
                "deeplink_type": "NORMAL"
            }
        ],
        "interactive_add_on_list": [],
        "landing_page_url_list": [],
        "modify_time": "{{modify_time}}",
        "operation_status": "ENABLE",
        "page_list": [],
        "secondary_status": "AD_STATUS_AUDIT",
        "smart_plus_ad_id": "{{smart_plus_ad_id}}"
    }
}
(/code)
```
