# Get Upgraded Smart+ Campaigns

**Doc ID**: 1843312818332930
**Path**: API Reference/Upgraded Smart+/Campaigns/Get Upgraded Smart+ Campaigns

---

Use this endpoint to retrieve Upgraded Smart+ Campaigns within an ad account.

## Request

**Endpoint** https://business-api.tiktok.com/open_api/v1.3/smart_plus/campaign/get/

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
|fields|string[]|Fields that you want to get.

When not specified, all fields are returned by default.

For allowed fields, see the fields under `list` in the [Response](#item-link-Response) section.|
|page|integer|Current page number.

Default value: 1.
Value range: ≥ 1.|
|page_size|integer|Page size.

Default value: 10.
Value range: 1-1,000.|
|filtering|object|Filtering conditions.

Example: `filtering={"objective_type":"APP_PROMOTION"}`|
#|campaign_ids|string[]|Filter by campaign IDs.

Max size: 100.|
#|campaign_name|string|Filter by campaign name. 

Fuzzy match is supported.|
#|primary_status|string|Primary status.

For enum values, see [Enumeration-Primary Status](https://business-api.tiktok.com/portal/docs?id=1737174886619138#item-link-Primary%20Status).|
#|secondary_status|string|Filter by campaign secondary status.

For enum values, see [Enumeration- Campaign Status - Secondary Status](https://business-api.tiktok.com/portal/docs?id=1737174886619138#item-link-Campaign%20Status%20-%20Secondary%20Status).|
#|objective_type|string|Filter by advertising objective.

For enum values, see [Enumeration-Advertising Objective](https://business-api.tiktok.com/portal/docs?id=1737174886619138#item-link-Advertising%20Objective).|
#| sales_destination | string | Sales destination, the destination where you want to drive your sales.

Enum values:
- `WEBSITE`: Website. Drive sales on your website.
- `APP`: App. Drive sales on your app (product catalog required).
- `WEB_AND_APP`: Website and app. Drive sales on both your website and your app.|
#|creation_filter_start_time|string|The earliest campaign creation time, in the format of `YYYY-MM-DD HH:MM:SS` (UTC time). This filter will retrieve campaigns created after this time.

Example: `2025-01-01 00:00:01`.

If `creation_filter_start_time` and `creation_filter_end_time` are not specified, the results will include campaigns created at any time.

**Note**: To ensure task efficiency and speed, consider setting a time range within 6 months for the creation time filters.|
#|creation_filter_end_time|string|The latest campaign creation time, in the format of `YYYY-MM-DD HH:MM:SS` (UTC time). This filter will retrieve campaigns created before this time.

Example: `2025-02-01 00:00:01`.

If `creation_filter_start_time` and `creation_filter_end_time` are not specified, the results will include campaigns created at any time.

**Note**: To ensure task efficiency and speed, consider setting a time range within 6 months for the creation time filters.|
```

### Example
```xcodeblock
(code curl http)
curl --location --request GET 'https://business-api.tiktok.com/open_api/v1.3/smart_plus/campaign/get/?advertiser_id={{advertiser_id}}&page=1&page_size=1000' \
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
#|list|object[]|A list of Upgraded Smart+ Campaigns.|
##|advertiser_id|string|Advertiser ID.|
##|campaign_id|string|Campaign ID.|
##|create_time|string|The time when the campaign was created, in the format of `YYYY-MM-DD HH:MM:SS` (UTC time)|
##|modify_time|string|The time when the campaign was last modified, in the format of `YYYY-MM-DD HH:MM:SS` (UTC time)|
##|objective_type|string|Advertising objective.

For enum values, see [Enumeration-Advertising Objective](https://business-api.tiktok.com/portal/docs?id=1737174886619138#item-link-Advertising%20Objective).|
##|app_promotion_type|string|App promotion type.

Enum value:
- `APP_INSTALL`: App install. Get new users to install your app.
- `APP_RETARGETING`: App retargeting. Re-engage existing app users to take action in your app.
- `MINIS`: TikTok Minis. Get people to watch your series or play your games with TikTok Minis.|
##|sales_destination|string|Sales destination, the destination where you want to drive your sales.

Enum values:
- `WEBSITE`: Website. Drive sales on your website.
- `APP`: App. Drive sales on your app (product catalog required).
- `WEB_AND_APP`: Website and app. Drive sales on both your website and your app.|
##|campaign_type|string|Campaign type.

Currently, we support `REGULAR_CAMPAIGN` and `IOS14_CAMPAIGN`.|
##|app_id|string|The App ID of the app to promote.

To get a list of App IDs, use [/app/list/](https://business-api.tiktok.com/portal/docs?id=1740859313270786).|
##|gaming_ad_compliance_agreement|string|Whether to agree to the Compliance Assurance Policy for Gaming Advertisers on TikTok.

The policy is as follows: Yo confirms and attest that any gaming application, product or service (game) you desire to advertise on TikTok, including any associated URL(s), (a) complies with all applicable laws and regulations of the jurisdictions where the game can be accessed or played, and upon request, can provide supporting documentation as evidence of why the game is not considered illegal gambling or lottery; and (b) has not been and is not part of any investigation or lawsuit regarding the game's legality or regulatory compliance.

Enum values: 
- `ON`: To agree to the policy.
- `OFF`: To leave the policy not accepted.|
##|is_advanced_dedicated_campaign|boolean|Whether the campaign is an Advanced Dedicated Campaign. Advanced Dedicated Campaigns leverage advanced delivery models that benefit from real-time signals.

Supported values: `true`, `false`.

By default, Upgraded Smart+ App Campaigns with iOS 14 dedicated campaign setting enabled are all Advanced Dedicated Campaigns.|
##|disable_skan_campaign|boolean|Whether to disable SKAN (SKAdNetwork) attribution, Apple's conversion attribution solution for iOS campaigns.

Enum values:
- `true`: To disable SKAN attribution. The campaign will not be bound by [Dedicated Campaign quota limits](https://business-api.tiktok.com/portal/docs?id=1752256248260610) and you will be able to retrieve [Self Attribution Network (SAN) metrics](https://business-api.tiktok.com/portal/docs?id=1751443967255553#item-link-SAN%20metrics) for the campaign. However, you cannot retrieve [SKAN reporting metrics](https://business-api.tiktok.com/portal/docs?id=1751443967255553#item-link-SKAN%20metrics) for the campaign. Learn more about [SAN integration](https://ads.tiktok.com/help/article/about-self-attribution-transition).
- `false`: To enable SKAN attribution. The campaign will be bound by [Dedicated Campaign quota limits](https://business-api.tiktok.com/portal/docs?id=1752256248260610) and you will be able to retrieve [SKAN metrics](https://business-api.tiktok.com/portal/docs?id=1751443967255553#item-link-SKAN%20metrics) for the campaign.|
##|bid_align_type|string|The attribution type for the Dedicated Campaign. The type determines which attribution network the target CPA (`conversion_bid_price`) or ROAS (`roas_bid`) at the ad group level is based on.

Enum values:
- `SAN`: SAN.
- `SKAN`: SKAN.|
##|campaign_app_profile_page_state|string|Indicates the status of the App Profile Page.

Enum values: `ON`, `OFF`.|
##|catalog_enabled|boolean|Whether to use your catalog to automatically advertise relevant products or services to people based on their unique interests, intent and actions.

Supported values: `true`, `false`.|
##|catalog_type|string|The type of catalog.

Enum values: 
- `ECOMMERCE`: e-commerce
- `TRAVEL_ENTERTAINMENT`: travel and entertainment.
- `MINI_SERIES`: mini series.|
##|campaign_name|string|Campaign name.|
##|special_industries|string[]|Ad categories.

Enum values:
- `HOUSING`: Ads for real estate listings, homeowners insurance, mortgage loans or other related opportunities.
- `EMPLOYMENT`: Ads for job offers, internships, professional certification programs or other related opportunities.
- `CREDIT`: Ads for credit card offers, auto loans, long-term financing or other related opportunities.|
##|budget_optimize_on|boolean|Whether CBO is enabled.

Supported value: `true` (enabled), `false` (disabled).|
##|budget_mode|string|Budget mode.

- When `budget_optimize_on` is `true` or not specified, the enum values are:`BUDGET_MODE_DYNAMIC_DAILY_BUDGET`: Dynamic daily campaign budget. It is the average daily budget over a week. Daily costs will not exceed 125% of the average daily budget. Weekly costs will not exceed the average daily budget * 7.
- `BUDGET_MODE_TOTAL`: Lifetime campaign budget.
- When `budget_optimize_on` is `false`, the enum values are:`BUDGET_MODE_INFINITE`: No limit for all ad groups under this campaign.
- `BUDGET_MODE_DAY`: Daily budget limit for all ad groups under this campaign.
- `BUDGET_MODE_TOTAL`: Total budget limit for all ad groups under this campaign.|
##|budget_auto_adjust_strategy |string|Returned only when the following conditions are all met:
- `budget_optimize_on` is `true` or not specified.
- `budget_mode` is `BUDGET_MODE_DYNAMIC_DAILY_BUDGET`.
- `app_promotion_type` is not `MINIS`.
The campaign budget strategy for automatic daily campaign budget.

Enum values: 
- `AUTO_BUDGET_INCREASE`: To enable Goal-based budget increase. Allow your budget to automatically increase when your ads are performing well and target CPA, Day 0 target ROAS, and budget requirements are met. 	When `budget_auto_adjust_strategy` is `AUTO_BUDGET_INCREASE`, the specified `budget` will be the initial daily budget. Your daily budget will be allowed to automatically increase by 20%, up to 10 times per day, when your budget utilization reaches 90% or more. Your daily budget will reset to your original daily budget each day.
- `UNSET`: To disable Goal-based budget increase.|
##|budget|float|
- When `budget_optimize_on` is `true` or not specified, this field represents fixed campaign budget or initial campaign budget.When `budget_auto_adjust_strategy` is `UNSET`, this field represents your fixed campaign budget.
- When `budget_auto_adjust_strategy` is `AUTO_BUDGET_INCREASE`, this field represents your initial campaign budget. To retrieve the current campaign budget, check the returned `current_budget`.
- When `budget_optimize_on` is `false`, this field represents the limit for all ad groups under this campaign.When `budget_mode` is `BUDGET_MODE_DAY`, this field represents the daily limit for all ad groups under this campaign.
- When `budget_mode` is `BUDGET_MODE_TOTAL`, this field represents the total limit for all ad groups under this campaign.|
##|current_budget|float|Returned only when `budget_auto_adjust_strategy`  is `AUTO_BUDGET_INCREASE`.

Current campaign budget for a campaign with Goal-based budget increase enabled.|
##|operation_status|string|Operation status.

Enum values:
- `ENABLE` : The campaign is enabled (in 'ON' status).
- `DISABLE`: The campaign is disabled (in 'OFF' status).|
##|secondary_status|string|Campaign secondary status.

For enum values, see [Enumeration- Campaign Status - Secondary Status](https://business-api.tiktok.com/portal/docs?id=1737174886619138#item-link-Campaign%20Status%20-%20Secondary%20Status).|
##|smart_plus_adgroup_mode|string|The ad group mode for the campaign.

Enum values:
- `SINGLE`: You can only create one single ad group within the campaign.
- `MULTIPLE`: You can only create multiple ad groups within the campaign.|
##|postback_window_mode|string|The mode that determines which SKAN 4.0 postback you want to secure.

Enum values:
- `POSTBACK_WINDOW_MODE1`: This option secures the first postback, which corresponds to the 0-2 day attribution window. The data can take up to 4 days to return, and the campaign will wait for 4 days to release the campaign quota.
- `POSTBACK_WINDOW_MODE2`: This mode secures the first two postbacks, which correspond to the 3-7 day attribution window. The data can take up to 13 days to return, and the campaign will wait for 13 days to release the campaign quota.
- `POSTBACK_WINDOW_MODE3`: This mode secures all three postbacks, which correspond to the 8-35 day attribution window. The data can take up to 41 days to return, and the campaign will wait for 41 days to release the campaign quota.
**Note**: If you have set up Mobile Measurement Partner (MMP) Tracking with **Adjust**, **Airbridge**, **Appsflyer**, **Branch**, **Kochava**, or **Singular** for your App and your MMP SDK version is updated to a SKAN 4.0 supported SDK, you can transition your App to SKAN 4.0 on Events Manager. To learn about how to set up MMP tracking for your App, see [How to Set Up App Attribution in TikTok Ads Manager](https://ads.tiktok.com/help/article/set-up-app-attribution-tiktok-ads-manager). To learn more about how to transition your App to SKAN 4.0, see [About SKAN 4.0 and TikTok](https://ads.tiktok.com/help/article/about-skan-4-0-and-tiktok) and [How to transition to SKAN 4.0](https://ads.tiktok.com/help/article/how-to-transition-to-skan-4-0).|
##|po_number|string|PO (purchase order) number.

PO numbers are useful for invoice tracking and reconciliation. 

[Learn more about PO numbers on monthly invoices](https://ads.tiktok.com/help/article/update-po-number-on-monthly-invoices).|
##|is_promotional_campaign|boolean|Whether to use promotion campaign settings.

Enable this feature to activate specialized campaign setup flows and optimization for theatrical releases and streaming service promotions.

Supported values: `true`, `false`.|
##|rta_id|string|Realtime API (RTA) ID, the RTA strategy identifier.|
##|rta_bid_enabled|boolean|Whether to use RTA bid.

Supported values:
- `true`: enabled.
- `false`: not enabled.|
##|rta_product_selection_enabled|boolean|Whether to use RTA to automatically select products.

Enum values:
- `true`: enabled.
- `false`: not enabled.|
#|page_info|object|Pagination information.|
##|page|number|Current page number.|
##|page_size|number|Page size.|
##|total_number|number|Total number of results.|
##|total_page|number|Total pages of results.|
```

### Example
```xcodeblock
(code Success-Response http)
{
    "code": 0,
    "message": "OK",
    "request_id": "{{request_id}}",
    "data": {
        "list": [
            {
                "advertiser_id": "{{advertiser_id}}",
                "budget": {{budget}},
                "budget_mode": "BUDGET_MODE_DYNAMIC_DAILY_BUDGET",
                "budget_optimize_on": true,
                "campaign_id": "{{campaign_id}}",
                "campaign_name": "{{campaign_name}}",
                "catalog_enabled": false,
                "create_time": "{{create_time}}",
                "modify_time": "{{modify_time}}",
                "objective_type": "LEAD_GENERATION",
                "operation_status": "ENABLE",
                "secondary_status": "CAMPAIGN_STATUS_ENABLE",
                "smart_plus_adgroup_mode": "MULTIPLE"
            },
            {
                "advertiser_id": "{{advertiser_id}}",
                "budget": {{budget}},
                "budget_mode": "BUDGET_MODE_DYNAMIC_DAILY_BUDGET",
                "budget_optimize_on": true,
                "campaign_id": "{{campaign_id}}",
                "campaign_name": "{{campaign_name}}",
                "campaign_type": "REGULAR_CAMPAIGN",
                "create_time": "{{create_time}}",
                "modify_time": "{{modify_time}}",
                "objective_type": "WEB_CONVERSIONS",
                "operation_status": "ENABLE",
                "sales_destination": "WEBSITE",
                "secondary_status": "CAMPAIGN_STATUS_ENABLE",
                "smart_plus_adgroup_mode": "MULTIPLE"
            },
            {
                "advertiser_id": "{{advertiser_id}}",
                "budget": {{budget}},
                "budget_mode": "BUDGET_MODE_DYNAMIC_DAILY_BUDGET",
                "budget_optimize_on": true,
                "campaign_id": "{{campaign_id}}",
                "campaign_name": "{{campaign_name}}",
                "campaign_type": "REGULAR_CAMPAIGN",
                "catalog_enabled": true,
                "catalog_type": "TRAVEL_ENTERTAINMENT",
                "create_time": "{{create_time}}",
                "modify_time": "{{modify_time}}",
                "objective_type": "WEB_CONVERSIONS",
                "operation_status": "ENABLE",
                "sales_destination": "WEBSITE",
                "secondary_status": "CAMPAIGN_STATUS_ENABLE",
                "smart_plus_adgroup_mode": "MULTIPLE"
            },
            {
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
                "smart_plus_adgroup_mode": "SINGLE"
            }
        ],
        "page_info": {
            "page": 1,
            "page_size": 1000,
            "total_number": 4,
            "total_page": 1
        }
    }
}
(/code)
```
