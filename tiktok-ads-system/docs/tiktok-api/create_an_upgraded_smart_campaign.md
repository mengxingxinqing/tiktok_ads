# Create an Upgraded Smart+ Campaign

**Doc ID**: 1843312852800706
**Path**: API Reference/Upgraded Smart+/Campaigns/Create an Upgraded Smart+ Campaign

---

Use this endpoint to create an Upgraded Smart+ Campaign.

## Request

**Endpoint** https://business-api.tiktok.com/open_api/v1.3/smart_plus/campaign/create/

**Method** POST

**Header**

```xtable
|Field{30%}|Data Type{15%}|Description{55%}|
|---|---|---|
|Access-Token {Required}|string|Authorized access token. For details, see [Authentication](https://business-api.tiktok.com/portal/docs?id=1738373164380162).|
|Content-Type {Required}|string|Request message type.
Allowed value: `application/json`.|
```

**Parameters**

```xtable
|Field{30%}|Data Type{15%}|Description{55%}|
|---|---|---|
|advertiser_id {Required}|string|Advertiser ID.|
|request_id {Required}|string|Request ID with which you can create campaigns with duplicate names. It also supports idempotency to prevent you from sending the same request twice. If you retry requests with the same request ID multiple times, then only one will succeed.

It is different from the `request_id` returned in the response parameters, which is used to uniquely identify an HTTP request.

The value should be a string representation of a 64-bit integer number.

Example: `123456789`.|
|operation_status|string|The status of the campaign when created.

Enum values:
- `ENABLE`: The campaign is enabled when created.
- `DISABLE`: The campaign is disabled when created.
Default value: `ENABLE`.|
|objective_type {Required}|string|Advertising objective.

Currently, we support `APP_PROMOTION`, `WEB_CONVERSIONS`, and `LEAD_GENERATION`.

For detailed explanation of enum values, see [Enumeration-Advertising Objective](https://business-api.tiktok.com/portal/docs?id=1737174886619138#item-link-Advertising%20Objective).

- To learn about how to create an Upgraded Smart+ App Campaign, see [Create Upgraded Smart+ App Campaigns](https://business-api.tiktok.com/portal/docs?id=1843309500205058).
- To learn about how to create an Upgraded Smart+ Web Campaign, see [Create Upgraded Smart+ Web Campaigns](https://business-api.tiktok.com/portal/docs?id=1843309514567809).
- To learn about how to create an Upgraded Smart+ Lead Generation Campaign, see [Create Upgraded Smart+ Lead Generation Campaigns](https://business-api.tiktok.com/portal/docs?id=1843324498993154).|
|app_promotion_type {+Conditional}|string|Required when `objective_type` is `APP_PROMOTION`.

App promotion type.

Enum value:
- `APP_INSTALL`: App install. Get new users to install your app.
- `APP_RETARGETING`: App retargeting. Re-engage existing app users to take action in your app.
- `MINIS`: TikTok Minis. Get people to watch your series or play your games with TikTok Minis.To learn more about the campaign type where this setting is supported, see [Create an Upgraded Smart+ Minis Campaign](https://business-api.tiktok.com/portal/docs?id=1853377811982657).|
|sales_destination {+Conditional}|string |Required when `objective_type` is `WEB_CONVERSIONS`.

Sales destination, the destination where you want to drive your sales.

Enum values:
- `WEBSITE`: Website. Drive sales on your website.
- `APP`: App. Drive sales on your app (product catalog required). Learn more about [how to create Upgraded Smart+ Catalog Ads for App](https://business-api.tiktok.com/portal/docs?id=1847303035303106). When `sales_destination` is `APP`:Set `catalog_enabled` to  `true` and `catalog_type` to `ECOMMERCE` or `TRAVEL_ENTERTAINMENT`. 
- The type of catalog that you can specify at the ad group level varies depending on your `rta_id` setting:If `rta_id` is not specified, you can set `catalog_id` at the ad group level to the ID of a catalog with `catalog_type` as `ECOM`, `HOTEL`,`FLIGHT`,`DESTINATION`, or `ENTERTAINMENT`.
- If `rta_id` is specified, you can set `catalog_id` at the ad group level to the ID of a catalog with `catalog_type` as `ECOM` or `ENTERTAINMENT`.
- `WEB_AND_APP`: Website and app. Drive sales on both your website and your app.Learn more about how to [create Upgraded Smart+ Ads with Website and App Optimization](https://business-api.tiktok.com/portal/docs?id=1854746404386113).

**Note**: Once set, this field cannot be updated.
|
|catalog_enabled|boolean|Valid only when `objective_type` is `WEB_CONVERSIONS` or `LEAD_GENERATION`.

Whether to use catalog in the campaign.

Supported values: `true`, `false`.|
|catalog_type {+Conditional}|string|Required when `objective_type` is `WEB_CONVERSIONS` and `catalog_enabled` is `true`.

The type of catalog.

Enum values: 
- `ECOMMERCE`: e-commerce.
- `TRAVEL_ENTERTAINMENT`: travel and entertainment.
- `MINI_SERIES`: mini series.

**Note**: Create Upgraded Smart+ Mini Series Catalog Ads is currently an allowlist-only feature. If you would like to access it, please contact your TikTok representative.
|
|campaign_type|string|Campaign type.

Enum values: `REGULAR_CAMPAIGN`, `IOS14_CAMPAIGN`.
Default value: `REGULAR_CAMPAIGN`.|
|is_promotional_campaign|boolean|Valid when `objective_type` is `WEB_CONVERSIONS`.

Whether to use promotion campaign settings.

Enable this feature to activate specialized campaign setup flows and optimization for theatrical releases and streaming service promotions.

Default value: `false`.

Supported values: `true`, `false`.

**Note**: 
- Using promotion campaign settings for theatrical releases and for streaming service promotions are currently separate allowlist-only features. If you would like to access them, please contact your TikTok  representative.
- Once set, this field cannot be updated.
|
|app_id {+Conditional}|string|Required when the following conditions are both met:
- `objective_type` is `APP_PROMOTION` and `app_promotion_type` is `APP_INSTALL`, or `objective_type` is `WEB_CONVERSIONS` and `sales_destination` is `APP`.
- `camapign_type` is `IOS14_CAMPAIGN`.
The App ID of the app to promote.

To get a list of App IDs, use [/app/list/](https://business-api.tiktok.com/portal/docs?id=1740859313270786).

**Note**: You cannot specify an App that has not activated the SAN module on your MMP through this field to create iOS Dedicated Campaigns. To ensure that TikTok SAN integration is enabled for your App, see [How to migrate your app to SAN integration](https://ads.tiktok.com/help/article/transition-to-san-for-existing-apps).
|
|gaming_ad_compliance_agreement|string|Valid only when the following conditions are all met:
- `objective_type` is `APP_PROMOTION`.
- `app_promotion_type` is `APP_INSTALL`.
- `campaign_type` is `IOS14_CAMPAIGN`.
Whether to agree to the Compliance Assurance Policy for Gaming Advertisers on TikTok.

The policy is as follows: You confirm and attest that any gaming application, product or service (game) you desire to advertise on TikTok, including any associated URL(s), (a) complies with all applicable laws and regulations of the jurisdictions where the game can be accessed or played, and upon request, can provide supporting documentation as evidence of why the game is not considered illegal gambling or lottery; and (b) has not been and is not part of any investigation or lawsuit regarding the game's legality or regulatory compliance.

Enum values: 
- `ON`: To agree to the policy.
- `OFF`: To leave the policy not accepted.
Default value: `OFF`.

**Note**: Agreeing to the Compliance Assurance Policy for Gaming Advertisers on TikTok is currently an allowlist-only feature. If you would like to access it, please contact your TikTok representative.
|
|campaign_app_profile_page_state|string|Whether to use app profile page to optimize delivery.

Enum values: `ON`, `OFF`.
Default value: `OFF`.

**Note**:
- You can use the field only when `objective_type` is `APP_PROMOTION`and your campaign is an iOS 14 Dedicated Campaign. Otherwise, an error will occur.
- When `ON` is selected, pass in the `page_id` of App Profile Page.To create an App Profile Page, use [Instant Page Editor SDK](https://business-api.tiktok.com/portal/docs?id=1740307202170881) and set `businessType` to `4`.
|
|disable_skan_campaign|boolean|Valid only when the following conditions are all met:
- `objective_type` is `APP_PROMOTION` and `app_promotion_type` is `APP_INSTALL`, or `objective_type` is `WEB_CONVERSIONS` and `sales_destination` is `APP`.
- `campaign_type` is `IOS14_CAMPAIGN`.
- `app_id` is set to the ID of an iOS app that is eligible for [Advanced Dedicated Campaigns](https://business-api.tiktok.com/portal/docs?id=1797011827608577). To confirm whether an app is eligible for Advanced Dedicated Campaigns, use [/app/list/](https://business-api.tiktok.com/portal/docs?id=1740859313270786) and check the returned `advanced_dedicated_campaign_allowed`.
Whether to disable SKAN (SKAdNetwork) attribution, Apple's conversion attribution solution for iOS campaigns

Enum values:
- `true`: To disable SKAN attribution. The campaign will not be bound by [Dedicated Campaign quota limits](https://business-api.tiktok.com/portal/docs?id=1752256248260610) and you will be able to retrieve [Self Attribution Network (SAN) metrics](https://business-api.tiktok.com/portal/docs?id=1751443967255553#item-link-SAN%20metrics) for the campaign. However, you cannot retrieve [SKAN reporting metrics](https://business-api.tiktok.com/portal/docs?id=1751443967255553#item-link-SKAN%20metrics) for the campaign. Learn more about [SAN integration](https://ads.tiktok.com/help/article/about-self-attribution-transition).For a Dedicated Campaign using an app that is eligible for Advanced Dedicated Campaigns, you need to enable SKAN attribution or Advanced Dedicated Campaign or both. You cannot disable SKAN attribution and Advanced Dedicated Campaign simultaneously.
- `false`: To enable SKAN attribution. The campaign will be bound by [Dedicated Campaign quota limits](https://business-api.tiktok.com/portal/docs?id=1752256248260610) and you will be able to retrieve [SKAN metrics](https://business-api.tiktok.com/portal/docs?id=1751443967255553#item-link-SKAN%20metrics) for the campaign.If you enable Advanced Dedicated Campaign by setting `is_advanced_dedicated_campaign` to `true` simultaneously, you'll be able to retrieve both [SAN](https://business-api.tiktok.com/portal/docs?id=1751443967255553#item-link-SAN%20metrics) and [SKAN reporting metrics](https://business-api.tiktok.com/portal/docs?id=1751443967255553#item-link-SKAN%20metrics) for the campaign.

**Note**:
- Disabling SKAN attribution for Dedicated Campaigns is currently an allowlist-only feature. If you would like to access it, please contact your TikTok representative.
- If you are allowlisted for disabling SKAN attribution for Dedicated Campaigns, you cannot set `bid_type` to `BID_TYPE_CUSTOM` when the following conditions are all met:`is_advanced_dedicated_campaign` is `false`.
- `disable_skan_campaign` is `false`.
- `optimization_goal` is `INSTALL` or `IN_APP_EVENT`.
- Getting access to Advanced Dedicated Campaign requires the app to meet certain criteria. If your app is ineligible for Advanced Dedicated Campaign, reach out to your TikTok representative. Your TikTok representative will be able to provide troubleshooting support to help your app get access to Advanced Dedicated Campaign.
|
|campaign_name {Required}|string|Campaign name.

Length limit: 512 characters. Emoji is not supported.
Each word in Chinese or Japanese counts as two characters, while each letter in English counts as one character.|
|special_industries|string[]|Ad categories. Enum values:
- `HOUSING`: Ads for real estate listings, homeowners insurance, mortgage loans or other related opportunities.
- `EMPLOYMENT`: Ads for job offers, internships, professional certification programs or other related opportunities.
- `CREDIT`: Ads for credit card offers, auto loans, long-term financing or other related opportunities.

**Note**:
- Once you've specified the industry type, the system will adjust your target options to help you comply with advertising policies. See [Ad targeting](https://business-api.tiktok.com/portal/docs?id=1739381236849665) for details.
- This field is only supported for advertisers who are registered in the US or Canada.
|
|budget_optimize_on|boolean|Whether to enable Campaign Budget Optimization (CBO).

Supported values: `true` (enabled), `false` (disabled).
Default value: `true`.|
|budget_mode|boolean|Budget mode.
- When `budget_optimize_on` is `true` or not specified, this field represents the campaign budget mode. The enum values are:`BUDGET_MODE_DYNAMIC_DAILY_BUDGET`: Dynamic daily budget. It is the average daily budget over a week. Daily costs will not exceed 125% of the average daily budget. Weekly costs will not exceed the average daily budget * 7.
- `BUDGET_MODE_TOTAL`: Lifetime budget.Default value when `budget_optimize_on` is `true` or not specified: `BUDGET_MODE_DYNAMIC_DAILY_BUDGET`.
- When `budget_optimize_on` is `false`, this field allows you to set a fixed limit for the total budget of all ad groups under this campaign. The enum values are:`BUDGET_MODE_INFINITE`: No limit.
- `BUDGET_MODE_DAY`: Daily budget.
- `BUDGET_MODE_TOTAL`: Lifetime budget.Default value when `budget_optimize_on` is `false`: `BUDGET_MODE_INFINITE`.

**Note**:
- Once set, this field cannot be updated.
|
|budget_auto_adjust_strategy|string|Valid only when the following conditions are all met:
- `budget_optimize_on` is `true` or not specified.
- `budget_mode` is `BUDGET_MODE_DYNAMIC_DAILY_BUDGET`.
- `app_promotion_type` is not `MINIS`.
The campaign budget strategy for automatic daily campaign budget.

Enum value: 
- `AUTO_BUDGET_INCREASE`: To enable Goal-based budget increase. Allow your budget to automatically increase when your ads are performing well and target CPA, Day 0 target ROAS, and budget requirements are met. When `budget_auto_adjust_strategy` is `AUTO_BUDGET_INCREASE`, the specified `budget` will be the initial daily budget. Your daily budget will be allowed to automatically increase by 20%, up to 10 times per day, when your budget utilization reaches 90% or more. Your daily budget will reset to your original daily budget each day.

**Note**: Enabling Goal-based budget increase is currently an allowlist-only feature. If you would like to access it, please contact your TikTok representative.
|
|budget {+Conditional}|float|Required when `budget_mode` is set to `BUDGET_MODE_DYNAMIC_DAILY_BUDGET`, `BUDGET_MODE_TOTAL`, or `BUDGET_MODE_DAY`.
- When `budget_optimize_on` is `true` or not specified, this field represents fixed campaign budget or initial campaign budget.When `budget_auto_adjust_strategy` is `UNSET`, this field represents your fixed campaign budget.
- When `budget_auto_adjust_strategy` is `AUTO_BUDGET_INCREASE`, this field represents your initial campaign budget. To retrieve the current campaign budget, check the returned `current_budget`.
- When `budget_optimize_on` is `false`, this field represents the limit for all ad groups under this campaign.When `budget_mode` is `BUDGET_MODE_DAY`, this field represents the daily limit for all ad groups under this campaign.
- When `budget_mode` is `BUDGET_MODE_TOTAL`, this field represents the total limit for all ad groups under this campaign.
To learn about the minimum budget and how to set budget modes, see [Budget](https://business-api.tiktok.com/portal/docs?id=1739381246298114).
To directly see the daily budget value range for a currency, see [Currency-Daily budget value range](https://business-api.tiktok.com/portal/docs?id=1737585839634433#item-link-Daily%20budget%20value%20range).|
|postback_window_mode|string|Valid only when `campaign_type` is `IOS14_CAMPAIGN` and `operation_status` is `DISABLE`.

You can specify this field when you create a disabled campaign or when you disable an existing campaign by using [/smart_plus/campaign/status/update/](https://business-api.tiktok.com/portal/docs?id=1843312888885314). The recommended practice is to specify this field when disabling an existing campaign.

The mode that determines which SKAN (SKAdNetwork) 4.0 postback you want to secure. Options with longer windows require more time to receive, and as a result, more time to release the campaign back to the available number.

Enum values:
- `POSTBACK_WINDOW_MODE1`: This option secures the first postback, which corresponds to the 0-2 day attribution window. The data can take up to 4 days to return, and the campaign will wait for 4 days to release the campaign quota.
- `POSTBACK_WINDOW_MODE2`: This mode secures the first two postbacks, which correspond to the 3-7 day attribution window. The data can take up to 13 days to return, and the campaign will wait for 13 days to release the campaign quota.
- `POSTBACK_WINDOW_MODE3`: This mode secures all three postbacks, which correspond to the 8-35 day attribution window. The data can take up to 41 days to return, and the campaign will wait for 41 days to release the campaign quota.

**Note**: 
- If you have set up Mobile Measurement Partner (MMP) Tracking with **Adjust**, **Airbridge**, **Appsflyer**, **Branch**, **Kochava**, or **Singular** for your App and your MMP SDK version is updated to a SKAN 4.0 supported SDK, you can transition your App to SKAN 4.0 on Events Manager. To learn about how to set up MMP tracking for your App, see [How to Set Up App Attribution in TikTok Ads Manager](https://ads.tiktok.com/help/article/set-up-app-attribution-tiktok-ads-manager). To learn more about how to transition your App to SKAN 4.0, see [About SKAN 4.0 and TikTok](https://ads.tiktok.com/help/article/about-skan-4-0-and-tiktok) and [How to transition to SKAN 4.0](https://ads.tiktok.com/help/article/how-to-transition-to-skan-4-0).
- Once set, this field cannot be updated.
- If `operation_status` is set to `ENABLE` or not specified, this field will be ignored.
- If you pass in this field when you have not enabled SKAN 4.0 for your App (`app_id`), an error will occur.
- If this field is not specified when `campaign_type` is set to `IOS14_CAMPAIGN`, `operation_status` is set to `DISABLE`, and you have enabled SKAN 4.0 for your App, this field will default to `POSTBACK_WINDOW_MODE1`.
- If you have enabled SKAN 4.0 for your App, ensure that you target devices running iOS 16.1 and later so that you can receive SKAN 4.0 postbacks. To only target iOS 16.1+ devices, set `min_ios_version` to `16.1` at the ad group level.
|
|po_number|string|PO (purchase order) number.

PO numbers are useful for invoice tracking and reconciliation. 

[Learn more about PO numbers on monthly invoices](https://ads.tiktok.com/help/article/update-po-number-on-monthly-invoices).|
|rta_id|string|Realtime API (RTA) ID, the RTA strategy identifier.

The RTA enables you to integrate real-time audience data to customize ad auction and targeting, thereby delivering better performance.

To obtain the list of RTA IDs associated with your ad account, contact your TikTok representative. 

**Note**: 
- Enabling RTA for your ads is currently an allowlist-only feature. If you would like to access it, please contact your TikTok representative. You will need to complete the onboarding process to be able to receive and respond to RTA requests sent to your system first.
- Once set, this field cannot be updated.
|
|rta_bid_enabled|boolean|Whether to use RTA bid.

Supported values:
- `true`: enabled.
- `false`: not enabled.
Default value: `false`.

You can only set this field to `true` in any of the following scenarios:
- Scenario 1: `objective_type` is set to `WEB_CONVERSIONS`.
- `sales_destination` is set to `APP`.
- `rta_id` is passed.
- Scenario 2: `objective_type` is set to `APP_PROMOTION`.
- `app_promotion_type` is set to `APP_RETARGETING`.
- `rta_id` is passed.

**Note**: 
- Enabling RTA bid is currently an allowlist-only feature. If you would like to access it, please contact your TikTok representative.
- Once set, this field cannot be updated.
|
|rta_product_selection_enabled|boolean|Whether to use RTA to automatically select products.

Enum values:
- `true`: enabled.
- `false`: not enabled.
Default value: `false`.

You can only set this field to `true` when the following conditions are met:
- `objective_type` is set to `WEB_CONVERSIONS`.
- `sales_destination` is set to `APP`.
- `rta_id` is specified.

**Note**: 
- Once set, this field cannot be updated.
- When `rta_product_selection_enabled` is `true` , you can only set `product_specific_type` to `ALL` at the ad level.
|
```

### Example
```xcodeblock
(code curl http)
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

## Response

```xtable
|Field{30%}|Data Type{15%}|Description{55%}|
|---|---|---|
|code|number|Response code. For the complete list of response codes and descriptions, see [Appendix - Return Codes](https://business-api.tiktok.com/portal/docs?id=1737172488964097).|
|message|string|Response message. For details, see [Appendix - Return Codes](https://business-api.tiktok.com/portal/docs?id=1737172488964097).|
|request_id|string|The log ID of a request, which uniquely identifies the request.|
|data|object|Returned data.|
#|advertiser_id|string|Advertiser ID.|
#|campaign_id|string|Campaign ID.|
#|create_time|string|The time when the campaign was created, in the format of `YYYY-MM-DD HH:MM:SS` (UTC time)|
#|modify_time|string|The time when the campaign was last modified, in the format of `YYYY-MM-DD HH:MM:SS` (UTC time)|
#|objective_type|string|Advertising objective.

Currently, we support `APP_PROMOTION`, `WEB_CONVERSIONS`, and `LEAD_GENERATION`. 
For detailed explanation of enum values, see [Enumeration-Advertising Objective](https://business-api.tiktok.com/portal/docs?id=1737174886619138#item-link-Advertising%20Objective).|
#|app_promotion_type|string|App promotion type.

Enum value:
- `APP_INSTALL`: App install. Get new users to install your app.
- `APP_RETARGETING`: App retargeting. Re-engage existing app users to take action in your app.
- `MINIS`: TikTok Minis. Get people to watch your series or play your games with TikTok Minis.|
#|sales_destination|string |Sales destination, the destination where you want to drive your sales.

Enum values:
- `WEBSITE`: Website. Drive sales on your website.
- `APP`: App. Drive sales on your app (product catalog required).
- `WEB_AND_APP`: Website and app. Drive sales on both your website and your app.|
#|campaign_type|string|Campaign Type.

Currently, we support `REGULAR_CAMPAIGN` and `IOS14_CAMPAIGN`.|
#|app_id|string|The App ID of the app to promote.

To get a list of App IDs, use [/app/list/](https://business-api.tiktok.com/portal/docs?id=1740859313270786).|
#|gaming_ad_compliance_agreement|string|Whether to agree to the Compliance Assurance Policy for Gaming Advertisers on TikTok.

The policy is as follows: Yo confirms and attest that any gaming application, product or service (game) you desire to advertise on TikTok, including any associated URL(s), (a) complies with all applicable laws and regulations of the jurisdictions where the game can be accessed or played, and upon request, can provide supporting documentation as evidence of why the game is not considered illegal gambling or lottery; and (b) has not been and is not part of any investigation or lawsuit regarding the game's legality or regulatory compliance.

Enum values: 
- `ON`: To agree to the policy.
- `OFF`: To leave the policy not accepted.|
#|is_advanced_dedicated_campaign|boolean|Whether the campaign is an Advanced Dedicated Campaign. Advanced Dedicated Campaigns leverage advanced delivery models that benefit from real-time signals.

Supported values: `true`, `false`.|
#|disable_skan_campaign|boolean|Whether to disable SKAN (SKAdNetwork) attribution, Apple's conversion attribution solution for iOS campaigns.

Enum values:
- `true`: To disable SKAN attribution. The campaign will not be bound by [Dedicated Campaign quota limits](https://business-api.tiktok.com/portal/docs?id=1752256248260610) and you will be able to retrieve [Self Attribution Network (SAN) metrics](https://business-api.tiktok.com/portal/docs?id=1751443967255553#item-link-SAN%20metrics) for the campaign. However, you cannot retrieve [SKAN reporting metrics](https://business-api.tiktok.com/portal/docs?id=1751443967255553#item-link-SKAN%20metrics) for the campaign. Learn more about [SAN integration](https://ads.tiktok.com/help/article/about-self-attribution-transition).
- `false`: To enable SKAN attribution. The campaign will be bound by [Dedicated Campaign quota limits](https://business-api.tiktok.com/portal/docs?id=1752256248260610) and you will be able to retrieve [SKAN metrics](https://business-api.tiktok.com/portal/docs?id=1751443967255553#item-link-SKAN%20metrics) for the campaign.|
#|bid_align_type|string|The attribution type for the Dedicated Campaign. The type determines which attribution network the target CPA (conversion_bid_price) or ROAS (roas_bid) at the ad group level is based on.

Enum values:
- `SAN`: SAN.
- `SKAN`: SKAN.|
#|campaign_app_profile_page_state|string|Indicates the status of the App Profile Page.

Enum values: `ON`, `OFF`.|
#|catalog_enabled|boolean|Whether to use your catalog to automatically advertise relevant products or services to people based on their unique interests, intent and actions.

Supported values: `true`, `false`.|
#|catalog_type|string|The type of catalog.
Enum values: 
- `ECOMMERCE`: e-commerce.
- `TRAVEL_ENTERTAINMENT`: travel and entertainment.
- `MINI_SERIES`: mini series.|
#|campaign_name|string|Campaign name.|
#|special_industries|string[]|Ad categories.

Enum values:
- `HOUSING`: Ads for real estate listings, homeowners insurance, mortgage loans or other related opportunities.
- `EMPLOYMENT`: Ads for job offers, internships, professional certification programs or other related opportunities.
- `CREDIT`: Ads for credit card offers, auto loans, long-term financing or other related opportunities.|
#|budget_optimize_on|boolean|Whether CBO is enabled.

Supported values: `true` (enabled), `false` (disabled).|
#|budget_mode|string|Budget mode.

- When `budget_optimize_on` is `true` or not specified, the enum values are:`BUDGET_MODE_DYNAMIC_DAILY_BUDGET`: Dynamic daily campaign budget. It is the average daily budget over a week. Daily costs will not exceed 125% of the average daily budget. Weekly costs will not exceed the average daily budget * 7.
- `BUDGET_MODE_TOTAL`: Lifetime campaign budget.
- When `budget_optimize_on` is `false`, the enum values are:`BUDGET_MODE_INFINITE`: No limit for all ad groups under this campaign.
- `BUDGET_MODE_DAY`: Daily budget limit for all ad groups under this campaign.
- `BUDGET_MODE_TOTAL`: Total budget limit for all ad groups under this campaign.|
#|budget_auto_adjust_strategy|string|Returned only when the following conditions are all met:
- `budget_optimize_on` is `true` or not specified.
- `budget_mode` is `BUDGET_MODE_DYNAMIC_DAILY_BUDGET`.
- `app_promotion_type` is not `MINIS`.
The campaign budget strategy for automatic daily campaign budget.

Enum values: 
- `AUTO_BUDGET_INCREASE`: To enable Goal-based budget increase. Allow your budget to automatically increase when your ads are performing well and target CPA, Day 0 target ROAS, and budget requirements are met. When `budget_auto_adjust_strategy` is `AUTO_BUDGET_INCREASE`, the specified `budget` will be the initial daily budget. Your daily budget will be allowed to automatically increase by 20%, up to 10 times per day, when your budget utilization reaches 90% or more. Your daily budget will reset to your original daily budget each day.
- `UNSET`: To disable Goal-based budget increase.|
#|budget|float|
- When `budget_optimize_on` is `true` or not specified, this field represents fixed campaign budget or initial campaign budget.When `budget_auto_adjust_strategy` is `UNSET`, this field represents your fixed campaign budget.
- When `budget_auto_adjust_strategy` is `AUTO_BUDGET_INCREASE`, this field represents your initial campaign budget. To retrieve the current campaign budget, check the returned `current_budget`.
- When `budget_optimize_on` is `false`, this field represents the limit for all ad groups under this campaign.When `budget_mode` is `BUDGET_MODE_DAY`, this field represents the daily limit for all ad groups under this campaign.
- When `budget_mode` is `BUDGET_MODE_TOTAL`, this field represents the total limit for all ad groups under this campaign.|
#|current_budget|float|Returned only when `budget_auto_adjust_strategy`  is `AUTO_BUDGET_INCREASE`.

Current campaign budget for a campaign with Goal-based budget increase enabled.|
#|operation_status|string|Operation status.

Enum values:
- `ENABLE` : The campaign is enabled (in 'ON' status).
- `DISABLE`: The campaign is disabled (in 'OFF' status).|
#|secondary_status|string|Campaign secondary status.

For enum values, see [Enumeration- Campaign Status - Secondary Status](https://business-api.tiktok.com/portal/docs?id=1737174886619138#item-link-Campaign%20Status%20-%20Secondary%20Status).|
#|smart_plus_adgroup_mode|string|The ad group mode for the campaign.

Enum values:
- `SINGLE`: You can only create one single ad group within the campaign.
- `MULTIPLE`: You can only create multiple ad groups within the campaign.|
#|postback_window_mode|string|The mode that determines which SKAN 4.0 postback you want to secure.

Enum values:
- `POSTBACK_WINDOW_MODE1`: This option secures the first postback, which corresponds to the 0-2 day attribution window. The data can take up to 4 days to return, and the campaign will wait for 4 days to release the campaign quota.
- `POSTBACK_WINDOW_MODE2`: This mode secures the first two postbacks, which correspond to the 3-7 day attribution window. The data can take up to 13 days to return, and the campaign will wait for 13 days to release the campaign quota.
- `POSTBACK_WINDOW_MODE3`: This mode secures all three postbacks, which correspond to the 8-35 day attribution window. The data can take up to 41 days to return, and the campaign will wait for 41 days to release the campaign quota.
**Note**: If you have set up Mobile Measurement Partner (MMP) Tracking with **Adjust**, **Airbridge**, **Appsflyer**, **Branch**, **Kochava**, or **Singular** for your App and your MMP SDK version is updated to a SKAN 4.0 supported SDK, you can transition your App to SKAN 4.0 on Events Manager. To learn about how to set up MMP tracking for your App, see [How to Set Up App Attribution in TikTok Ads Manager](https://ads.tiktok.com/help/article/set-up-app-attribution-tiktok-ads-manager). To learn more about how to transition your App to SKAN 4.0, see [About SKAN 4.0 and TikTok](https://ads.tiktok.com/help/article/about-skan-4-0-and-tiktok) and [How to transition to SKAN 4.0](https://ads.tiktok.com/help/article/how-to-transition-to-skan-4-0).|
#|po_number|string|PO (purchase order) number.

PO numbers are useful for invoice tracking and reconciliation. 

[Learn more about PO numbers on monthly invoices](https://ads.tiktok.com/help/article/update-po-number-on-monthly-invoices).|
#|is_promotional_campaign|boolean|Whether to use promotion campaign settings.

Enable this feature to activate specialized campaign setup flows and optimization for theatrical releases and streaming service promotions.

Supported values: `true`, `false`.|
#|rta_id|string|Realtime API (RTA) ID, the RTA strategy identifier.|
#|rta_bid_enabled|boolean|Whether to use RTA bid.

Supported values:
- `true`: enabled.
- `false`: not enabled.|
#|rta_product_selection_enabled|boolean|Whether to use RTA to automatically select products.

Enum values:
- `true`: enabled.
- `false`: not enabled.|
```

### Example
```xcodeblock
(code Success-Response http)
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
        "campaign_name": "{{campaign_name}}",
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
