# Create an Upgraded Smart+ Ad Group

**Doc ID**: 1843314887930946
**Path**: API Reference/Upgraded Smart+/Ad groups/Create an Upgraded Smart+ Ad Group

---

Use this endpoint to create an Upgraded Smart+ Ad Group.

You can create up to 30 ad groups within an Upgraded Smart+ Campaign.
- If Campaign Budget Optimization (CBO) is enabled (`budget_optimize_on` is `true`) at the campaign level, you need to ensure that the following settings, if specified, are the same for ad groups within the same campaign:
	- `promotion_type`
	- `promotion_target_type`
	- `optimization_goal`
	- `optimization_event`
	- `billing_event`
	- `bid_type`
	- `bid_price`
	- `conversion_bid_price`
	- `deep_bid_type`
	- `vbo_window`
	- `roas_bid`
- If CBO is disabled (`budget_optimize_on` is `false`) at the campaign level, you need to ensure that the following settings, if specified, are the same for ad groups within the same campaign:
	- `bid_type`
	- `deep_bid_type`
	- `vbo_window`
	- `budget_mode`

## Request
**Endpoint** https://business-api.tiktok.com/open_api/v1.3/smart_plus/adgroup/create/

**Method** POST

**Header**

```xtable
|Field{35%}|Type{15%}|Description{50%}|
|---|---|---|
|Access-Token {Required}|string|Authorized access token. For details, see [Authentication](https://business-api.tiktok.com/portal/docs?id=1738373164380162).|
|Content-Type {Required}|string|Request message type.
Allowed value: `application/json`.|
```

**Parameters**

```xtable
|Field{35%}|Type{15%}|Description{50%}|
|---|---|---|
|advertiser_id {Required}|string|Advertiser ID.|
|request_id {Required}|string|Request ID with which you can create ad groups with duplicate names. It also supports idempotency to prevent you from sending the same request twice. If you retry requests with the same request ID multiple times, then only one will succeed.

It is different from the `request_id` returned in the response parameters, which is used to uniquely identify an HTTP request.

The value should be a string representation of a 64-bit integer number.

Example: `123456789`.|
|campaign_id {Required}|string|The ID of the campaign that the ad group belongs to.|
|operation_status|string|The status of the ad group when created.

Enum values:
- `ENABLE` : The ad group is enabled when created.
- `DISABLE` : The ad group is disabled when created.
Default value: `ENABLE`.|
|adgroup_name {Required}|string|Ad group name.

Length limit: 512 characters. Emoji is not supported.|
|catalog_id {+Conditional}|string|Required when `catalog_enabled` is `true` at the campaign level.

The ID of the catalog to use in the ad group.

To retrieve the catalogs within your Business Center, use [/catalog/get/](https://business-api.tiktok.com/portal/docs?id=1740315452868610).|
|catalog_authorized_bc_id {+Conditional}|string|Required when `catalog_enabled` is `true`.

The ID of the Business Center that the catalog (`catalog_id`) belongs to.|
|promotion_type {Required}|string|Promotion type (Optimization location). 
You can decide where you'd like to promote your products using this field.

Currently, we support `APP_ANDROID`, `APP_IOS`, `WEBSITE`, `MINI_APP`, `MINI_GAME`, and `LEAD_GENERATION`.
- When `objective_type` is `APP_PROMOTION` and `app_promotion_type` is `APP_INSTAL` or `APP_RETARGETING`, set this field to `APP_ANDROID` or `APP_IOS`.
- When `objective_type` is `APP_PROMOTION` and `app_promotion_type` is `MINIS`, set this field to `MINI_APP` or `MINI_GAME`.
- When `objective_type` is `WEB_CONVERSIONS`:If `sales_destination` is `WEBSITE`, set this field to `WEBSITE`.
- If `sales_destination` is `APP`, set this field to `APP_ANDROID` or `APP_IOS`.
- When `objective_type` is `LEAD_GENERATION`, set this field to any of the following values:`LEAD_GENERATION`
- `LEAD_GEN_CLICK_TO_TT_DIRECT_MESSAGE`
- `LEAD_GEN_CLICK_TO_SOCIAL_MEDIA_APP_MESSAGE`
- `LEAD_GEN_CLICK_TO_CALL`

**Note**: When CBO is enabled (`budget_optimize_on` is `true` ) at the campaign level, this setting must be the same across all ad groups within the same campaign.
|
|promotion_target_type {+Conditional}|string|Required when `objective_type` is `LEAD_GENERATION`.

The optimization location for Lead Generation objective.

Enum values:
- `INSTANT_PAGE`: Instant Form. To create a fast-loading in-app TikTok Instant Form to collect more leads.
- `EXTERNAL_WEBSITE`: Website Form. To use a landing page that has the Website Form or the TikTok Instant Page that redirects to the website with the Website Form to collect more leads.

**Note**: When CBO is enabled (`budget_optimize_on` is `true`) at the campaign level, this setting, if specified, must be the same across all ad groups within the same campaign.
|
|optimization_goal {Required}|string|The measurable results you'd like to drive with your campaigns.

Currently, we support `CLICK`, `INSTALL`, `IN_APP_EVENT`, `VALUE`, `CONVERT`, `TRAFFIC_LANDING_PAGE_VIEW`, `CONVERSATION`, and `LEAD_GENERATION`.

To find the detailed description for each optimization goal, see [Enumeration - Optimization Goal](https://business-api.tiktok.com/portal/docs?id=1737174886619138#item-link-Optimization%20Goal).

**Note**: 
- When CBO is enabled (`budget_optimize_on` is `true`) at the campaign level, this setting, if specified, must be the same across all ad groups within the same campaign.
- When `promotion_type` is `LEAD_GEN_CLICK_TO_SOCIAL_MEDIA_APP_MESSAGE` and `optimization_goal` is `CONVERSATION`, you can only set `messaging_app_type` to any of the following values:`MESSENGER`
- `WHATSAPP`
- `ZALO`
|
|app_id {+Conditional}|string|Required when the following conditions are both met:
At the campaign level:
- `objective_type` is`APP_PROMOTION` and `app_promotion_type` is `APP_INSTALL` or `APP_RETARGETING`, or `objective_type` is`WEB_CONVERSIONS` and `sales_destination` is `APP`.
- `camapign_type` is `REGULAR_CAMPAIGN`.
The App ID of the app to promote.

To get a list of App IDs, use [/app/list/](https://business-api.tiktok.com/portal/docs?id=1740859313270786).

**Note**: You cannot specify an App that has not activated the SAN module on your MMP through this field to create ad groups. To ensure that TikTok SAN integration is enabled for your App, see [How to migrate your app to SAN integration](https://ads.tiktok.com/help/article/transition-to-san-for-existing-apps).
|
|gaming_ad_compliance_agreement|string|Valid in any of the following scenarios:
- Scenario 1: When the following conditions are both met at the campaign level:`objective_type` is `APP_PROMOTION`.
- `app_promotion_type` is `APP_RETARGETING`.
- Scenario 2: When the following conditions are both met at the campaign level:`objective_type` is `APP_PROMOTION`.
- `app_promotion_type` is `APP_INSTALL`.
- `campaign_type` is `REGULAR_CAMPAIGN`.
Whether to agree to the Compliance Assurance Policy for Gaming Advertisers on TikTok.

The policy is as follows: You confirm and attest that any gaming application, product or service (game) you desire to advertise on TikTok, including any associated URL(s), (a) complies with all applicable laws and regulations of the jurisdictions where the game can be accessed or played, and upon request, can provide supporting documentation as evidence of why the game is not considered illegal gambling or lottery; and (b) has not been and is not part of any investigation or lawsuit regarding the game's legality or regulatory compliance.

Enum values: 
- `ON`: To agree to the policy.
- `OFF`: To leave the policy not accepted.
Default value: `OFF`.

**Note**: Agreeing to the Compliance Assurance Policy for Gaming Advertisers on TikTok is currently an allowlist-only feature. If you would like to access it, please contact your TikTok representative.
|
|pixel_id {+Conditional}|string|
- Required when the following conditions are met:At the campaign level: `objective_type` is `WEB_CONVERSIONS` or `LEAD_GENERATION`.
- At the ad group level: `optimization_goal` is set to `CONVERT` or `VALUE`.
- Not supported when `optimization_goal` is set to `CLICK`, `INSTALL`, `IN_APP_EVENT`, or `TRAFFIC_LANDING_PAGE_VIEW`.
Pixel ID. 

To get all Pixel IDs, use [/pixel/list/](https://business-api.tiktok.com/portal/docs?id=1740858697598978).|
| app_config {+Conditional} | object[] | Required when `sales_destination` is `WEB_AND_APP` at the campaign level.

Details of the app or apps to promote.

Max size: 2.

You can specify any of the following in this field:
- an Android app
- an iOS app
- an Android app and an iOS app |
#| app_id {+Conditional} | string | Required when `app_config` is specified.

The App ID of the app to promote.

To obtain the list of App IDs within your ad account, use [/app/list/](https://business-api.tiktok.com/portal/docs?id=1740859313270786) and check the returned `app_id`.|
|minis_id {+Conditional}|string|Required when `promotion_type` is `MINI_APP` or `MINI_GAME`.

The ID of a TikTok Minis.
- When `promotion_type` is `MINI_APP`, specify a TikTok Minis ID of the mini series type.
- When `promotion_type` is `MINI_GAME`, specify a TikTok Minis ID of the mini game type.
To obtain the list of TikTok Minis within an ad account, use [/minis/get/](https://business-api.tiktok.com/portal/docs?id=1853450329535490) and select a TikTok Minis with `minis_status` as `ACTIVE`.

To learn more about the campaign type where this setting is supported, see [Create an Upgraded Smart+ Minis Campaign](https://business-api.tiktok.com/portal/docs?id=1853377811982657).|
|optimization_event {+Conditional}|string|Required in any of the following scenarios:
- `pixel_id` is specified.
- `pixel_id` is not specified and `optimization_goal` is `IN_APP_EVENT` or `VALUE`.
- `pixel_id` is not specified and `minis_id` is specified.
Conversion event.

For the supported app and pixel events, see [Conversion events](https://business-api.tiktok.com/portal/docs?id=1739361474981889).
To find out the supported events for your app, use [/app/optimization_event/](https://business-api.tiktok.com/portal/docs?id=1740859338750977).

**Note**: When CBO is enabled (`budget_optimize_on` is `true`) at the campaign level, this setting, if specified, must be the same across all ad groups within the same campaign.
|
|custom_conversion_id|string|The ID of the Custom Conversion to use in the ad group.

Valid only when the following conditions are all met:
- Either `pixel_id` or `app_id` is specified.
- A Custom Conversion has been configured for the `pixel_id` or `app_id`.
- The `optimization_goal` is set to `CONVERT` or `IN_APP_EVENT`.
- The parameter `optimization_event` is specified and matches the Standard Event associated with the Custom Conversion.
- The status of the Custom Conversion is Active or No recent activity.

- To obtain the list of Custom Conversions associated with a Pixel or an App, use [/custom_conversion/list/](https://business-api.tiktok.com/portal/docs?id=1842225174460673). 
- To confirm the eligibility of the Custom Conversion for ad group creation:Ensure the returned `optimization_event` matches the `optimization_event` specified during ad group creation. 
- Ensure the `activity_status` is `NO_RECENT_ACTIVITY` or `ACTIVE`.|
|deep_funnel_optimization_status|string|Valid only when `promotion_type` is `LEAD_GENERATION`.

The status of deep funnel optimization.
Deep funnel optimization optimizes both your upper funnel events and deeper funnel events. You can select a secondary event alongside the primary optimization event, which can help improve campaign effectiveness.

Enum values:
- `ON`: To enable deep funnel optimization.
- `OFF`: To disable deep funnel optimization.
Default value: `OFF`.

**Note**: 
- Deep funnel optimization with CRM events is currently an allowlist-only feature. If you would like to access it, please contact your TikTok representative.
- Deep funnel optimization with Pixel or Offline events is generally available.
|
|deep_funnel_event_source {+Conditional}|string|Required when `deep_funnel_optimization_status` is `ON`.

The event source type.

Enum values:
- `PIXEL`: Pixel.
- `OFFLINE`: Offline Event Set.
- `CRM`: CRM Event Set.|
|deep_funnel_event_source_id {+Conditional}|string|Required when `deep_funnel_optimization_status` is `ON`.

Event Source ID.
- When `deep_funnel_event_source` is `PIXEL`, specify a Pixel ID via this field.To obtain a list of Pixels, use [/pixel/list/](https://business-api.tiktok.com/portal/docs?id=1740858697598978).
- When `deep_funnel_event_source` is `OFFLINE`, specify an Offline Event Set ID via this field.To obtain a list of Offline Event Set IDs, use [/offline/get/](https://business-api.tiktok.com/portal/docs?id=1765596808589313).
- When `deep_funnel_event_source` is `CRM`, specify a CRM Event Set ID via this field.To obtain a list of CRM Event Set IDs, use [/crm/list/](https://business-api.tiktok.com/portal/docs?id=1780896521680898).|
|deep_funnel_optimization_event {+Conditional}|string|Required when `deep_funnel_optimization_status` is `ON`.

Deep funnel optimization event.

- To find out the supported values for Standard Events available for Pixels, Offline Event Sets, and CRM Event Sets, see the **"Event name for ad creation"** column in [Supported Pixel events](https://business-api.tiktok.com/portal/docs?id=1739585696931842).
-  To find the list of optimization events for a Pixel, use [/pixel/list/](https://business-api.tiktok.com/portal/docs?id=1740858697598978) and check the returned `optimization_event`. 
Example: `SHOPPING`.|
|identity_id |string|
- Valid only when the following conditions are both met:`promotion_type` is `LEAD_GEN_CLICK_TO_TT_DIRECT_MESSAGE`
- Your ad account is allowlisted for selecting a TikTok account at the ad group level in TikTok Direct Messaging Ads.
- Not supported when `promotion_type` is `LEAD_GEN_CLICK_TO_TT_DIRECT_MESSAGE` and your ad account is not allowlisted for selecting a TikTok account at the ad group level in TikTok Direct Messaging Ads.
Identity ID of the TikTok account to use in TikTok Direct Messaging Ads.

To learn more about how to create TikTok Direct Messaging Ads, see [Create an Upgraded Smart+ Lead Generation Campaign with optimization location as TikTok direct messages](https://business-api.tiktok.com/portal/docs?id=1847302969710913).

**Note**:
- Selecting a TikTok account at the ad group level in TikTok Direct Messaging Ads is currently an allowlist-only feature. If you would like to access it, please contact your TikTok representative.
- Once set, this field cannot be updated.|
|identity_type|string|
- Valid only when the following conditions are both met:`promotion_type` is `LEAD_GEN_CLICK_TO_TT_DIRECT_MESSAGE`
- Your ad account is allowlisted for selecting a TikTok account at the ad group level in TikTok Direct Messaging Ads.
- Not supported when `promotion_type` is `LEAD_GEN_CLICK_TO_TT_DIRECT_MESSAGE` and your ad account is not allowlisted for selecting a TikTok account at the ad group level in TikTok Direct Messaging Ads.
Identity type of the TikTok account to use in TikTok Direct Messaging Ads.

Enum values: 

- `TT_USER`: TikTok Business Account User.
- `BC_AUTH_TT`: The TikTok account that a Business Center is authorized to access.
See [Identities](https://business-api.tiktok.com/portal/docs?id=1738958351620097) for details.

**Note**:
- Selecting a TikTok account at the ad group level in TikTok Direct Messaging Ads is currently an allowlist-only feature. If you would like to access it, please contact your TikTok representative.
- Once set, this field cannot be updated.|
|identity_authorized_bc_id {+Conditional}|string|Required when `identity_type` is `BC_AUTH_TT`.

ID of the Business Center that a TikTok Account User in Business Center identity is associated with.

**Note**: Once set, this field cannot be updated.|
|messaging_app_type {+Conditional}|string|Valid only when `promotion_type` is `LEAD_GEN_CLICK_TO_SOCIAL_MEDIA_APP_MESSAGE`.
- When `optimization_goal` is `CONVERSATION`, this field is required.
- When `optimization_goal` is `CLICK`, the default value for this field is `IM_URL`.
The type of instant messaging app or customized URL to use in the Instant Messaging App Ad Group.

Enum values:
- `MESSENGER`: Messenger. You need to simultaneously specify a Facebook Page ID via `messaging_app_account_id`.
- `WHATSAPP`: WhatsApp. You need to simultaneously specify `phone_info`, which will be used to automatically populate the corresponding WhatsApp phone number.
- `ZALO`: Zalo. You need to simultaneously specify Zalo contact format via `zalo_id_type`. 
- `LINE`: Line. You need to simultaneously specify a LINE Business ID via `messaging_app_account_id`.
- `IM_URL`: Instant Messaging URL.
To learn more about how to create Upgraded Smart+ TikTok Instant Messaging Ads, see [Create an Upgraded Smart+ Lead Generation Campaign with optimization location as instant messaging apps](https://business-api.tiktok.com/portal/docs?id=1847302988449921).

**Note**: 
- When `optimization_goal` is `CONVERSATION`, you cannot set this field to `LINE` or `IM_URL`.
- Once set, this field cannot be updated.|
|zalo_id_type {+Conditional}|string|Required when `messaging_app_type` is `ZALO`.

The type of Zalo contact format.

Enum values:
- `ZALO_OFFICIAL_ACCOUNT`: Zalo Official Account ID. You need to simultaneously specify a Zalo Official Account ID via `messaging_app_account_id`.
- `ZALO_PHONE_ACCOUNT`: Zalo phone number. You need to simultaneously specify `phone_info` to automatically populate the corresponding Zalo phone number.
- You can only set `zalo_id_type` to `ZALO_PHONE_ACCOUNT` when `optimization_goal` is `CLICK`.
**Note**: Once set, this field cannot be updated.|
|messaging_app_account_id {+Conditional}|string|Required and valid in any of the following scenarios:
- When `messaging_app_type` is `MESSENGER` or `LINE`.
- When `messaging_app_type` is `ZALO` and `zalo_id_type` is `ZALO_OFFICIAL_ACCOUNT`.
The ID of the instant messaging app account.
- When `messaging_app_type` is `MESSENGER`, specify the Facebook Page ID via this field.To find your Facebook Page ID, go to your Facebook Page and click About below your cover photo, then click Page transparency.
- When  `zalo_id_type` is `ZALO_OFFICIAL_ACCOUNT`, specify the Zalo Official Account ID via this field.
- When `messaging_app_type` is `LINE`, specify the LINE Business ID via this field.To find your LINE Business ID, go to your LINE official account page.
- When `messaging_app_type` is `WHATSAPP` or when `zalo_id_type` is `ZALO_PHONE_ACCOUNT`, this field will be ignored and be set as the corresponding WhatsApp or Zalo phone number automatically populated based on the specified `phone_info`.
**Note**: Once set, this field cannot be updated.|
|message_event_set_id {+Conditional}|string|Required when the following conditions are met:
- `promotion_type` is `LEAD_GEN_CLICK_TO_SOCIAL_MEDIA_APP_MESSAGE`.
- `optimization_goal` is `CONVERSATION`.
- The instant messaging app account in your ad group settings doesn't match any existing message event set.
The ID of the message event set to be used in the Instant Messaging Ad Group.
- If the instant messaging app account, either the Messenger account or Zalo Official Account specified via `messaging_app_account_id` or the WhatsApp or Zalo phone account populated from the specified `phone_info`, in your ad group settings matches an existing event set, this field will be **ignored and automatically populated** with the unique message event set associated with the instant messaging app account you choose.To confirm whether a unique message event set is associated with the instant messaging app account you choose, use [/ctm/message_event_set/get/](https://business-api.tiktok.com/portal/docs?id=1816979158055937) and check the returned `matched_event_set`.
- If the instant messaging app account in your ad group settings doesn't match any existing message event set (`matched_event_set` returned from `/ctm/message_event_set/get/` is empty), use [/ctm/message_event_set/get/](https://business-api.tiktok.com/portal/docs?id=1816979158055937) to obtain the message event sets available for ad creation via the response parameter `message_event_set_list`.
**Note**: Once set, this field cannot be updated.|
|phone_info {+Conditional}|object|Required in any of the following scenarios:
- When `messaging_app_type` is `WHATSAPP`
- When `messaging_app_type` is `ZALO` and `zalo_id_type` is `ZALO_PHONE_ACCOUNT`.
Details of WhatsApp or Zalo phone number.

**Note**: Once set, this field cannot be updated.|
#|phone_region_code {+Conditional}|string|Required when `phone_info` is specified.

The region code for WhatsApp or Zalo phone number.

Example: `US`.

To obtain the region code (`phone_region_code`) and region calling code (`phone_region_calling_code`) for the region that is associated with a specific phone number, use [/tool/phone_region_code/](https://business-api.tiktok.com/portal/docs?id=1774488637039618).|
#|phone_region_calling_code {+Conditional}|string|Required when `phone_info` is specified.

The region calling code for the WhatsApp or Zalo phone number.

Example: `+1`.

To obtain the region code (`phone_region_code`) and region calling code (`phone_region_calling_code`) for the region that is associated with a specific phone number, use [/tool/phone_region_code/](https://business-api.tiktok.com/portal/docs?id=1774488637039618).|
#|phone_number {+Conditional}|string|Required when `phone_info` is specified.

The WhatsApp or Zalo phone number.

For WhatsApp, use the same WhatsApp phone number connected to the Messagement Management Tool (MMT).|
|bid_type {Required}|string|Bidding strategy that determines how the system manages your cost per result, spends your budget, and how it delivers campaigns.

Enum values:
- `BID_TYPE_NO_BID`: Maximum Delivery.
- `BID_TYPE_CUSTOM`: Cost Cap (or Target CPA).You can only set `bid_type` to `BID_TYPE_CUSTOM` in any of the following scenarios:At the campaign level, `budget_mode` is `BUDGET_MODE_DYNAMIC_DAILY_BUDGET` 
- At the ad group level, `budget_mode` is `BUDGET_MODE_DYNAMIC_DAILY_BUDGET`
**Note**: This setting, if specified, must be the same across all ad groups within the same campaign.
|
|bid_price {+Conditional}|float|Required when the following conditions are met:
- `optimization_goal` is `CLICK`.
- `bid_type` is `BID_TYPE_CUSTOM`.
The target cost per click. The system will aim to get the most results while keeping the average cost per result around or lower than the specified amount.

`bid_price` needs to be lower than budget. See [Bidding-Bidding limits](https://business-api.tiktok.com/portal/docs?id=1745292444424193) to learn more about the bid verification mechanism.

**Note**: When CBO is enabled (`budget_optimize_on` is `true`) at the campaign level, this setting, if specified, must be the same across all ad groups within the same campaign.
|
|conversion_bid_price {+Conditional}|float|Required when the following conditions are met:
- `optimization_goal` is `CONVERT`,`TRAFFIC_LANDING_PAGE_VIEW` , `INSTALL`, or `IN_APP_EVENT`.
- `bid_type` is `BID_TYPE_CUSTOM`.
The target cost per conversion or cost per landing page view. The system will aim to get the most results while keeping the average cost per result around or lower than the specified amount.

`conversion_bid_price` needs to be lower than budget. See [Bidding-Bidding limits](https://business-api.tiktok.com/portal/docs?id=1745292444424193) to learn more about the bid verification mechanism.

**Note**: When CBO is enabled (`budget_optimize_on` is `true`) at the campaign level, this setting, if specified, must be the same across all ad groups within the same campaign.
|
|deep_bid_type {+Conditional}|string|Required when `optimization_goal` is `VALUE`.

Bidding strategy for in-app events.

Enum values: `DEFAULT`, `AEO`, `VO_MIN_ROAS`, and `VO_HIGHEST_VALUE`.

For the descriptions of supported values, see [Enumeration - Deep Event Bidding Strategy](https://business-api.tiktok.com/portal/docs?id=1737174886619138#item-link-Deep%20Event%20Bidding%20Strategy).

You can only set `deep_bid_type` to `VO_MIN_ROAS` in any of the following scenarios:
- At the campaign level, `budget_mode` is `BUDGET_MODE_DYNAMIC_DAILY_BUDGET` 
- At the ad group level, `budget_mode` is `BUDGET_MODE_DYNAMIC_DAILY_BUDGET`

**Note**: This setting, if specified, must be the same across all ad groups within the same campaign.
|
|roas_bid {+Conditional}|float|Required when `deep_bid_type` is `VO_MIN_ROAS`.

Target ROAS for Value-Based Optimization.

Value range: 0.01-1,000.

**Note**: When CBO is enabled (`budget_optimize_on` is `true`) at the campaign level, this setting, if specified, must be the same across all ad groups within the same campaign.
|
|vbo_window|string|The time window of the specified bidding strategy for [VBO IAA](https://business-api.tiktok.com/portal/docs?id=1739381743067137) (Value-Based Optimization for in-app advertising) or [VBO IAP](https://business-api.tiktok.com/portal/docs?id=1739381743067137) (Value-Based Optimization for in-app purchase).

Enum values:
- `SEVEN_DAYS`: The first seven days (day 7).
- `ZERO_DAY`: The current day (day 0).
Default value: `SEVEN_DAYS`.

- When the Minimum ROAS (Target ROAS) bidding strategy is used, this field represents the window type of the target ROAS value (Day 7 ROAS or Day 0 ROAS). The system will aim to keep your average ROAS of the seventh day or of the current day around or higher than the target ROAS value, regardless of your budget.
- When the Highest Value bidding strategy is used, this field represents the Highest Value window type (Day 7 Highest Value or Day 0 Highest Value). The system will aim to spend your budget fully and maximize the value of results within the first seven days or within the current day.

**Note**: 
- This setting, if specified, must be the same across all ad groups within the same campaign.
- VBO IAP and VBO IAA in different scenarios are currently allowlist-only features. If you would like to access them, please contact your TikTok representative.
- Day 0 or day 7 bidding (`vbo_window` is `ZERO_DAY` or `SEVEN_DAYS`) for **VBO IAP** in Advanced Dedicated Campaign or Android campaign scenarios are currently allowlist-only features. If you would like to access them, please contact your TikTok representative.
- Day 0 or day 7 bidding (`vbo_window` is `ZERO_DAY` or `SEVEN_DAYS`) for **VBO IAA** in Advanced Dedicated Campaign or Android campaign scenarios are currently allowlist-only features. If you would like to access them, please contact your TikTok representative.
- Once set, this field cannot be updated.
|
|click_attribution_window|string|Click-through window. This attribution window is the time between when a person clicks your ad and then takes an action.

Use this field to define the timeframe during which conversions can be attributed to the ad group.

Enum values:
- `OFF`: Off.
- `ONE_DAY`: 1-day click.
- `SEVEN_DAYS`: 7-day click.
- `FOURTEEN_DAYS`: 14-day click.
- `TWENTY_EIGHT_DAYS`: 28-day click.
- `THIRTY_DAYS`: 30-day click.This value is only valid when `promotion_type` is `MINI_GAME`.
- `THIRTY_TWO_DAYS`: 32-day click. This value is only valid when `promotion_type` is `MINI_APP` and `optimization_event` is `ACTIVE_PAY`.
- `ONE_HUNDRED_EIGHTY_DAYS`: 180-day click.This value is only valid when `promotion_type` is `MINI_APP` and `optimization_event` is `ACTIVE_PAY`.
To learn about the allowed values of this field for different advertising objective scenarios, refer to [Attribution window and event count](https://business-api.tiktok.com/portal/docs?id=1777694366654465).

**Note**:
- If you want to manually configure the attribution windows, you need to pass at least `click_attribution_window` and `view_attribution_window` simultaneously, and optionally `engaged_view_attribution_window`. Note that the `engaged_view_attribution_window`, once passed, must be accompanied by `click_attribution_window` and `view_attribution_window`.
- If you don't manually pass `click_attribution_window`, `engaged_view_attribution_window`, `view_attribution_window` and `attribution_event_count`, then default settings, if any, will be used. To confirm whether a default setting is used when you don't manually pass this field, use [/smart_plus/adgroup/get/](https://business-api.tiktok.com/portal/docs?id=1843314879617026).
- Once set, this field cannot be updated.
|
|engaged_view_attribution_window|string|Engaged view-through window. This attribution window is the time after someone watches at least 6 seconds of your video ad that a conversion is counted.
Use this field to define the timeframe during which conversions can be attributed to the ad group.

Enum values:
- `OFF`: Off.
- `ONE_DAY`: 1-day engaged view.
- `SEVEN_DAYS`: 7-day engaged view.
- `FOURTEEN_DAYS`: 14-day engaged view.This value is only valid in [Upgraded Smart+ Ads with Website and App Optimization](https://business-api.tiktok.com/portal/docs?id=1854746404386113).
- `TWENTY_EIGHT_DAYS`: 28-day engaged view.This value is only valid in [Upgraded Smart+ Ads with Website and App Optimization](https://business-api.tiktok.com/portal/docs?id=1854746404386113).
Default value: `OFF`.

To learn about the allowed values of this field for different advertising objective scenarios, refer to [Attribution window and event count](https://business-api.tiktok.com/portal/docs?id=1777694366654465).

**Note**: 
- If you want to manually configure the attribution windows, you need to pass at least `click_attribution_window` and `view_attribution_window` simultaneously, and optionally `engaged_view_attribution_window`. Note that the `engaged_view_attribution_window`, once passed, must be accompanied by `click_attribution_window` and `view_attribution_window`.
- If you don't manually pass `click_attribution_window`, `engaged_view_attribution_window`, `view_attribution_window` and `attribution_event_count`, then default settings, if any, will be used. To confirm whether a default setting is used when you don't manually pass this field, use the [/smart_plus/adgroup/get/](https://business-api.tiktok.com/portal/docs?id=1843314879617026) interface.
- Once set, this field cannot be updated.
|
|view_attribution_window|string|View-through window. This attribution window is the time between when a person views your ad and then takes an action.

Use this field to define the timeframe during which conversions can be attributed to the ad group.

Enum values:
- `OFF`: Off.
- `ONE_DAY`: 1-day view.
- `SEVEN_DAYS`: 7-day view.
To learn about the allowed values of this field for different advertising objective scenarios, refer to [Attribution window and event count](https://business-api.tiktok.com/portal/docs?id=1777694366654465).

**Note**: 
- If you want to manually configure the attribution windows, you need to pass at least `click_attribution_window` and `view_attribution_window` simultaneously, and optionally `engaged_view_attribution_window`. Note that the `engaged_view_attribution_window`, once passed, must be accompanied by `click_attribution_window` and `view_attribution_window`.
- If you don't manually pass `click_attribution_window`, `engaged_view_attribution_window`, `view_attribution_window` and `attribution_event_count`, then default settings, if any, will be used. To confirm whether a default setting is used when you don't manually pass this field, use[/smart_plus/adgroup/get/](https://business-api.tiktok.com/portal/docs?id=1843314879617026).
- Once set, this field cannot be updated.
|
|attribution_event_count|string|Event count (Statistic type).

The way that people\'s actions are counted after only viewing or clicking an ad.

Enum values:
- `UNSET`: Unset.
- `EVERY`: Every. To count multiple events from someone as separate conversions.
- `ONCE`: Once. To count multiple events from someone as 1 conversion.
To learn about the allowed values of this field for different advertising objective scenarios, refer to [Attribution window and event count](https://business-api.tiktok.com/portal/docs?id=1777694366654465).

**Note**: 
- If you don't manually pass `click_attribution_window`, `engaged_view_attribution_window`, `view_attribution_window` and `attribution_event_count`, then default settings, if any, will be used. To confirm whether a default setting is used when you don't manually pass this field, use [/smart_plus/adgroup/get/](https://business-api.tiktok.com/portal/docs?id=1843314879617026).
- Once set, this field cannot be updated.
|
|billing_event {Required}|string|Events that you want to pay for.

For enum values, see [Enumeration - Billing Event](https://business-api.tiktok.com/portal/docs?id=1737174886619138#item-link-Billing%20Event).

Currently, we only support `OCPM` and `CPC`:
- When `optimization_goal` is `CLICK`, set this field to `CPC`.
- When `optimization_goal` is not `CLICK`, set this field to `OCPM`. 

**Note**: When CBO is enabled (`budget_optimize_on` is `true`) at the campaign level, this setting must be the same across all ad groups within the same campaign.
|
|targeting_optimization_mode|string|Audience targeting optimization mode.

- `AUTOMATIC`: Automatic targeting. You can use automatic targeting to leverage real-time data and machine learning to target audiences most likely to engage with your ads. For an ad group that is not an Upgraded Smart+ Catalog Ad Group for App, when `targeting_optimization_mode` is `AUTOMATIC`, you can set `suggestion_audience_enabled` to `false` or `true`. When `targeting_optimization_mode` is `AUTOMATIC` and `suggestion_audience_enabled` is `false`, you can specify the following optional audience control settings: `location_ids`
- `zipcode_ids`
- `spc_audience_age`
- `languages`
- `operating_systems`
- `excluded_audience_ids` 
- When `targeting_optimization_mode` is `AUTOMATIC` and `suggestion_audience_enabled` is `true`, you can specify additional audience targeting settings as suggestions that guide automatic targeting. To learn more about the available settings, see the description of the parameter `suggestion_audience_enabled`.  
- For an Upgraded Smart+ Catalog Ad Group for App (at the campaign level `sales_destination` is `APP`), when `targeting_optimization_mode` is `AUTOMATIC`, you can only set `suggestion_audience_enabled` to `false`. When `targeting_optimization_mode` is `AUTOMATIC` and `suggestion_audience_enabled` is `false` , you can specify the following optional audience control settings: `location_ids`
- `zipcode_ids`
- `spc_audience_age`
- `languages`
- `audience_ids`
- `excluded_audience_ids`
- `gender`  
- `MANUAL`: Custom targeting. You can use custom targeting settings to precisely control who sees your ads. This may limit delivery and impact campaign performance. When `targeting_optimization_mode` is `MANUAL`, you can specify the following audience settings: `location_ids`
- `zipcode_ids`
- `age_groups`
- `gender`
- `languages`
- `audience_ids`
- `excluded_audience_ids`
- `included_pangle_audience_package_ids`
- `excluded_pangle_audience_package_ids`
- `interest_category_ids`
- `interest_keyword_ids`
- `purchase_intention_keyword_ids`
- `actions`
- `smart_interest_behavior_enabled`
- `smart_audience_enabled`
- `spending_power`
- `household_income`
- `operating_systems`
- `min_android_version`
- `min_ios_version`
- `device_model_ids`
- `network_types`
- `carrier_ids`
- `isp_ids`
- `device_price_ranges`
- `saved_audience_id`    
Default value: `AUTOMATIC`.

**Note**: If you specify targeting settings that don’t align with your targeting optimization mode settings (`targeting_optimization_mode` and `suggestion_audience_enabled`), those settings will be ignored, and no errors will occur.|
|suggestion_audience_enabled|boolean|Valid only when `targeting_optimization_mode` is `AUTOMATIC`.

Whether to enable audience suggestions.

Audience suggestions guide automatic targeting by specifying additional audience settings. These serve as suggestions only, and delivery to those audiences is not guaranteed.

Supported values: `true` (recommended), `false`.

Default value: `false`.

When `suggestion_audience_enabled` is `true`, you can specify the following additional audience targeting settings:
- `age_groups`
- `gender`
- `audience_ids`
- `interest_category_ids`
- `interest_keyword_ids`
- `purchase_intention_keyword_ids`
- `actions`

**Note**: 
- If you specify targeting settings that don’t align with your targeting optimization mode settings (`targeting_optimization_mode` and `suggestion_audience_enabled`), those settings will be ignored, and no errors will occur.
- You cannot set this field to `true` if Realtime API (RTA) is enabled at the campaign level.
|
|targeting_spec {Required}|object|Targeting settings.

The targeting settings that you can specify vary based on the values for `targeting_optimization_mode` and `suggestion_audience_enabled`. To learn more about the available settings, see the descriptions of the two parameters.|
#|app_targeting_type {+Conditional}|string|Required and valid only when the following conditions are all met:

- At the campaign level:
- `objective_type` is `WEB_CONVERSIONS`
- `sales_destination` is `APP`.
- `optimization_goal` is `CLICK`, `IN_APP_EVENT`, or `VALUE`.
App targeting type.

Enum values:
- `PROSPECT`: Prospect. Find prospective customers, including those who have not interacted with your products.
- `RETARGETING`: Retarget. Show ads to people who have already interacted with your business on and off TikTok.

**Note**: 

- When `campaign_type` is `IOS14_CAMPAIGN` at the campaign level, you can only set this field to `PROSPECT`.
- Once set, this field cannot be updated.|
#|location_ids {+Conditional}|string[]|
- When `catalog_type` is `TRAVEL_ENTERTAINMENT` at the campaign level, you need to set `location_ids` or `zipcode_ids` or both.
- When you create other types of Upgraded Smart+ Campaigns, `location_ids` is required.
IDs of the locations that you want to target.

To get the available locations and corresponding IDs based on your placement and objective, use the [/tool/targeting/search/](https://business-api.tiktok.com/portal/docs?id=1761236883355649) or [/tool/region/](https://business-api.tiktok.com/portal/docs?id=1737189539571713) endpoint.
To get the list of location IDs, see [Location IDs](https://business-api.tiktok.com/portal/docs?id=1739311040498689).

**Note**: If you add the US as your target location, then you can not remove the US after campaign creation.
|
#|zipcode_ids {+Conditional}|string[]|
-  When `catalog_type` is `TRAVEL_ENTERTAINMENT` at the campaign level, you need to set `location_ids` or `zipcode_ids` or both.
- When you create other types of Upgraded Smart+ Campaigns, `zipcode_ids` is not supported.
Zip code IDs or postal code IDs that you want to use to target locations.

Max size: 3,000. If you provide both `location_ids` and `zipcode_ids`, the combined total of location IDs, zip code IDs, and postal code IDs cannot exceed 3,000 per ad group.

You can get the available zip code IDs or postal code IDs based on your placement, objective and keyword via `geo_id` (when `geo_type` = `ZIP_CODE`) returned from the [/tool/targeting/search/](https://business-api.tiktok.com/portal/docs?id=1761236883355649) endpoint.

**Note**: 
- Zip code targeting is currently only supported for the US and postal code targeting is currently only supported for Canada, Brazil, Indonesia, Thailand, and Vietnam.
- Targeting postal code areas in Brazil, Indonesia, Thailand, and Vietnam is currently an allowlist-only feature. If you would like to access it, please contact your TikTok representative.
- You cannot use zip code targeting or postal code targeting in campaigns that have enabled special ad categories (`special_industries`).
- You cannot use zip code targeting or postal code targeting in campaigns with the `objective_type` as `RF_REACH`.
- Overlapping targeted locations are not supported. For instance, you cannot target the US and the state of California at the same time.
- If you target locations in the US via `location_ids` or `zipcode_ids` during ad group creation, you can subsequently update those IDs to other US locations but you cannot remove all US locations to target only non-US countries.
- To get information about the zip code IDs or postal code IDs, you can only use [/tool/targeting/info/](https://business-api.tiktok.com/portal/docs?id=1761237001980929).
|
#|languages|string[]|Codes of the languages that you want to target.

For the list of language codes supported, see [Enumeration - Language Code](https://business-api.tiktok.com/portal/docs?id=1737174886619138#item-link-Language%20Code).|
#|operating_systems|string[]|Device operating systems that you want to target. 

Enum values: `ANDROID`, `IOS`.

Only one value is allowed.

- When `promotion_type` is `APP_ANDROID`, this field will be ignored and default to `["ANDROID"]`.
- When `promotion_type` is `APP_IOS`, this field will be ignored and default to `["IOS"]`. |
#|spc_audience_age|string|The age group that the campaign targets.

Enum value:
- `ALL`: all age groups.
- `18+`: 18+.
- `25+`: 25+.
Default value: `18+`.

**Note**: You can only use the value `ALL` when at the campaign level `smart_plus_adgroup_mode` is `MULTIPLE`. To check the `smart_plus_adgroup_mode` of a campaign, use [/smart_plus/campaign/get/](https://business-api.tiktok.com/portal/docs?id=1843312818332930).
|
#|excluded_audience_ids|string[]|A list of audience IDs to be excluded.

To get a list of audience IDs, use [/dmp/custom_audience/list/](https://business-api.tiktok.com/portal/docs?id=1739940506015746).

**Note**: When at the campaign level `rta_id` is specified, this field is not supported.|
#|age_groups|string[]|Age groups you want to target.

Enum values:
- `AGE_13_17`: 13-17.
- `AGE_18_24`: 18-24.
- `AGE_25_34`: 25-34.
- `AGE_35_44`:`35-44.`
- `AGE_45_54`: 45-54.
- `AGE_55_100`: 55+
**Note**: You can only use the value `AGE_13_17` in the following scenario:
- At the campaign level `objective_type` is `APP_PROMOTION` and `app_promotion_type` is `APP_INSTALL` or `APP_RETARGETING`.
|
#|gender|string|Gender that you want to target.

Enum values: `GENDER_FEMALE`,`GENDER_MALE`,`GENDER_UNLIMITED`.|
#|audience_ids|string[]|A list of audience IDs.

To get audience IDs, use [/dmp/custom_audience/list/](https://business-api.tiktok.com/portal/docs?id=1739940506015746).

**Note**: When at the campaign level `rta_id` is specified, this field is not supported.|
#|shopping_ads_retargeting_type|string|Valid only when the following conditions are all met:
- At the campaign level:`objective_type` is `WEB_CONVERSION`
- `sales_destination` is `WEB_AND_APP`
- `catalog_type` is `ECOMMERCE`
- At the ad group level: `targeting_optimization_mode` is `MANUAL`.
The retargeting type.

Enum values:
- `LAB1`: Retargeting audiences who viewed products or added products to cart but didn't purchase products.
- `LAB2`: Retargeting audiences who added products to cart but didn't purchase products.
- `LAB3`: Retargeting audiences using custom combination.
- `OFF`: No retargeting.
Default value: `OFF`.|
#|shopping_ads_retargeting_actions_days {+Conditional}|number|Required when `shopping_ads_retargeting_type` is `LAB1` or `LAB2`.

The valid time range for the specified audience action. Audiences who have completed the specified action within the time range will be retargeted.

Value range: 1, 2, 3, 7, 14, 30, 60, 90, 180.|
#|included_custom_actions{+Conditional}|object[]|When `shopping_ads_retargeting_type` is `LAB3`, you need to specify either `included_custom_actions` or `excluded_custom_actions`.

Details of the catalog audience to include.
Catalog audience is based on people's interactions with specific products and often drives better performance than custom audience.|
##|code|string|The custom action used to filter the audiences to be retargeted.

Enum values:
- `VIEW_PRODUCT`: The audience viewed the product.
- `ADD_TO_CART`: The audience added the product to the cart.
- `PURCHASE`: The audience purchased the product.|
##|days|integer|The time range used to filter the audiences that completed the specified action.

Value range: 1-180.|
#|excluded_custom_actions{+Conditional}|object[]|When `shopping_ads_retargeting_type` is `LAB3`, you need to specify either `included_custom_actions` or `excluded_custom_actions`.

Details of the catalog audience to exclude.
Improve ad performance by excluding products that people have already interacted with, ensuring they only see relevant ads from your brand.|
##|code|string|The custom action used to filter out the audiences.

Enum values:
- `VIEW_PRODUCT`: The audience viewed the product.
- `ADD_TO_CART`: The audience added the product to the cart.
- `PURCHASE`: The audience purchased the product.|
##|days|integer|The time range used to filter out the audiences that completed the specified action.

Value range: 1-180.|
#|shopping_ads_retargeting_custom_audience_relation|string|Valid only when the following conditions are both met:
- `shopping_ads_retargeting_type` is set to `LAB1`, `LAB2`, or `LAB3`.
- `audience_ids` is specified.
The logical relation between the retargeting audience specified by `shopping_ads_retargeting_type` and the custom audience specified by `audience_ids`.

Enum values:
- `OR`: To combine the retargeting audience and the custom audience to create the targeted audience. The ad group will target anyone in catalog or custom audiences.
- `AND`: To intersect between the retargeting audience and the custom audience to create the targeted audience. The ad group will target individuals who belong to both the retargeting audience and the custom audience.
If this field is not set, the targeted audience will consist of individuals who belong to both the retargeting audience and the custom audience.

**Note**: Once set, this field cannot be updated to a null value.|
#|included_pangle_audience_package_ids|string[]|Valid only for Pangle placement. Do not specify this field and `excluded_pangle_audience_package_ids` at the same time.

IDs of the Pangle audiences that you want to include.

You can get audience IDs (`package_id`) by using the [/pangle_audience_package/get/](https://business-api.tiktok.com/portal/docs?id=1740040177229826) endpoint. The `bind_type` for the package should be `INCLUDE`.

IDs of the Pangle audiences that you want to include.|
#|excluded_pangle_audience_package_ids|string[]|Valid only for Pangle placement. Do not specify this field and `included_pangle_audience_package_ids` at the same time.

IDs of the Pangle audiences that you want to exclude.

You can get audience IDs (`package_id`) by using the [/pangle_audience_package/get/](https://business-api.tiktok.com/portal/docs?id=1740040177229826) endpoint. The `bind_type` for the package should be `EXCLUDE`.|
#|interest_category_ids|string[]|IDs of general interest keywords that you want to use to target audiences.

- To search for or list general interest category IDs, use [/targeting/search/](https://business-api.tiktok.com/portal/docs?id=1796638342793218) (recommended) or [/tool/interest_category/](https://business-api.tiktok.com/portal/docs?id=1737174348712961).
- To get recommended interest category IDs based on your industry, use [/tool/targeting_category/recommend/](https://business-api.tiktok.com/portal/docs?id=1736275204260866). |
#|interest_keyword_ids|string[]|IDs of additional interest categories that you want to use to target audience.

To search for additional interest categories, use [/targeting/search/](https://business-api.tiktok.com/portal/docs?id=1796638342793218) (recommended) or [/tool/interest_keyword/recommend/](https://business-api.tiktok.com/portal/docs?id=1763590884474882).|
#|purchase_intention_keyword_ids|string[]|IDs of purchase intention categories that you want to use to target audiences with an interest in purchases related to a content category.

To search for or list purchase intention category IDs, use [/targeting/search/](https://business-api.tiktok.com/portal/docs?id=1796638342793218).

**Note**: The placement setting should include TikTok (`PLACEMENT_TIKTOK`) or Pangle (`PLACEMENT_PANGLE`).
|
#|actions|object[]|A list of targeting behavioral category objects.|
##|action_scene|string|The type of user behavior that you want to target.

Enum values:
- `VIDEO_RELATED`: Video interactions.
- `CREATOR_RELATED`: Creator interactions.
- `HASHTAG_RELATED`: Hashtag interactions.|
##|action_period|number|The time period to include behaviors from.

Enum values: `0`, `7`, `15`.

If `action_scene` is `CREATOR_RELATED` or `HASHTAG_RELATED`, `0` will be used regardless of the value you specify. `0` means that there is no definite timeframe to select actions from.

**Note**: Currently, when creating an ad group with video interactions targeting (`action_scene`= `VIDEO_RELATED`) via **TikTok Ads Manager**, you cannot select the time period (`action_period`), and 15 days (`15`) will be used by default. However, when creating ad groups via **API**, `0`, `7`, or `15` can still be passed.
|
##|video_user_actions|string[]|The specific user interactions that you want to target for the user behavior type.

- If `action_scene` is `VIDEO_RELATED`, the allowed values are: `WATCHED_TO_END`,`LIKED`,`COMMENTED`,`SHARED`.
- If `action_scene` is `CREATOR_RELATED`, the allowed values are: `FOLLOWING`, `VIEW_HOMEPAGE`.
- If `action_scene` is `HASHTAG_RELATED`, the allowed value is `VIEW_HASHTAG`. 

**Note**: Currently, when creating an ad group via **TikTok Ads Manager (TTAM)**, you cannot define the kind of user actions (`video_user_actions`). By default, the ad group created via **TTAM** will use the options as follows:
- For an ad group with video interaction targeting (`action_scene`= `VIDEO_RELATED`), all the four options (`["WATCHED_TO_END","LIKED","COMMENTED","SHARED"]`) will be used.
- For an ad group with creator interaction targeting (`action_scene`=`CREATOR_RELATED`), both options(`["FOLLOWING","VIEW_HOMEPAGE"]`) will be used.However, when creating ad groups via **API**, you can still pass in the desired enum value combinations, for example: `["LIKED","COMMENTED"]` if `action_scene`=`VIDEO_RELATED`.
|
##|action_category_ids|string[]|Valid only when TikTok placement is the only placement selected.

IDs of the video interactions categories, creator interactions categories, hashtags, or hashtag bundles that you want to use to target audiences.

- To search for or list video interactions category IDs or creator interactions category IDs, use [/targeting/search/](https://business-api.tiktok.com/portal/docs?id=1796638342793218) (recommended) or [/tool/action_category/](https://business-api.tiktok.com/portal/docs?id=1737166752522241).
- To get hashtag IDs or hashtag bundle IDs, use [/targeting/search/](https://business-api.tiktok.com/portal/docs?id=1796638342793218) (recommended) or [/tool/hashtag/recommend/](https://business-api.tiktok.com/portal/docs?id=1736271339521025).
- To get recommended video interactions category IDs, creator interactions category IDs, hashtag IDs, or hashtag bundle IDs based on your industry, use [/tool/targeting_category/recommend/](https://business-api.tiktok.com/portal/docs?id=1736275204260866). |
#|smart_interest_behavior_enabled|boolean|Whether to turn on Smart interests & behaviors.

Supported values: `true`, `false`.

To learn more about Smart interests & behaviors and how to turn on Smart interests & behaviors, see [Smart Targeting](https://business-api.tiktok.com/portal/docs?id=1783164662979586) and [Enable Smart Targeting for your ad groups](https://business-api.tiktok.com/portal/docs?id=1783164826830849).|
#|smart_audience_enabled|boolean|Whether to turn on Smart audience.

Supported values: `true`, `false`.

To learn more about Smart audience and how to turn on Smart audience, see [Smart Targeting](https://business-api.tiktok.com/portal/docs?id=1783164662979586) and [Enable Smart Targeting for your ad groups](https://business-api.tiktok.com/portal/docs?id=1783164826830849).|
#|spending_power|string|Spending power that you want to target. 

Enum values: `ALL`, `HIGH`. 

If it is set to `HIGH`, you can target high spending users who typically spend more on purchases on TikTok ads than average users.|
#|household_income|string[]|Household income that you want to target. 

Enum values: `TOP5`(Top 5% of ZIP codes), `TOP10`(Top 10% of ZIP codes), `TOP10_25`(Top 10% -25% of ZIP codes), `TOP25_50`(Top 25% - 50% of ZIP codes).|
#|min_android_version|string|Minimum Android version. 

For enum values, see [Enumeration - Minimum Android Version](https://business-api.tiktok.com/portal/docs?id=1737174886619138#item-link-Minimum%20Android%20Version).|
#|min_ios_version|string|Audience minimum ios version. 

For enum values, see [Enumeration - Minimum iOS Version](https://business-api.tiktok.com/portal/docs?id=1737174886619138#item-link-Minimum%20iOS%20Version).|
#|device_model_ids|string[]|List of device model IDs. 

To get the complete list of device model IDs and their statuses, use [/tool/device_model/](https://business-api.tiktok.com/portal/docs?id=1737172880570369). Only active devices (`is_active` = `true` in the response of [/tool/device_model/](https://business-api.tiktok.com/portal/docs?id=1737172880570369)) can be used to create ad groups.

**Note**: Device model (`device_model_ids`) and device price (`device_price_ranges`) cannot be set at the same time.
|
#|network_types|string[]|Network types that you want to target. 

For enum values, see [Enumeration - Connection Type](https://business-api.tiktok.com/portal/docs?id=1737174886619138#item-link-Connection%20Type).|
#|carrier_ids|string[]|Carriers that you want to target. 

The carriers must be consistent with the location(s) that you want to target.

To get the enum values, use [/tool/carrier/](https://business-api.tiktok.com/portal/docs?id=1737168013095938). A carrier is valid only when the `in_use` field for the carrier is `true`.|
#|isp_ids|string[]|Valid only when you specify a valid location ID at the country or region level via `location_ids` at the same time.

IDs of the Internet service providers (ISP) that you want to target.

You can use [/tool/targeting/list/](https://business-api.tiktok.com/portal/docs?id=1762962378261506) to get the ISP IDs that you can target for a location ID.

**Note**: When you pass in `isp_ids`, you cannot set the placement as Global App Bundle only (`placements` =`PLACEMENT_GLOBAL_APP_BUNDLE`).
|
#|device_price_ranges|number[]|Targeting device price range. 

10000 means 1000+. The numbers must be in multiples of 50.

**Note**: The upper limit you set will be added by 50 and the resulting new number will be used as the actual upper limit for device targeting. The actual upper limit is shown in the ad group settings in TikTok Ads Manager. If you set and get the price range of [0, 250], it actually means [0, 300].
|
#|saved_audience_id|string|Valid when the following conditions are both met:
- The category of Housing, Employment, or Credit (`specical_industries`) is NOT specified in your campaign.
- TikTok placement is selected in your ad group (i.e., `placement_type` is set as `PLACEMENT_TYPE_AUTOMATIC` **or** `placement_type` is set as `PLACEMENT_TYPE_NORMAL` and `PLACEMENT_TIKTOK` is included in `placements`).
Saved Audience ID.

To obtain the list of Saved Audiences within your ad account, use [/dmp/saved_audience/list/](https://business-api.tiktok.com/portal/docs?id=1780154619404290).

Before using this field, call [/dmp/saved_audience/create/](https://business-api.tiktok.com/portal/docs?id=1780154541898754) to create a Saved Audience and get the Saved Audience ID in response. The advertiser ID associated with your Saved Audience should be the same as the advertiser ID in your ad group. Otherwise, an error will occur.

If you use `saved_audience_id` to create an ad group, we will return both the Saved Audience ID and the targeting options that are included within your Saved Audience in response.

See [Create a Saved Audience](https://business-api.tiktok.com/portal/docs?id=1780156510696449) to find out the detailed workflow and code examples.

**Note**: 
- When creating a Saved Audience via [/dmp/saved_audience/create/](https://business-api.tiktok.com/portal/docs?id=1780154541898754), you can specify various targeting options, including `gender`. However, be aware that if you are creating an ad group based on a Saved Audience, it’s essential to avoid setting both the `saved_audience_id` and targeting options (such as `gender`) defined within your Saved Audience at the same time.
- In cases where the targeting settings in your Saved Audience conflict with those in your ad group, the settings from your Saved Audience will take precedence. As a result, the conflicting targeting options in your ad group will be ignored.For example, if you create a Saved Audience where `gender` is set to `GENDER_FEMALE` and then use that Saved Audience to create an ad group while specifying `gender` as `GENDER_MALE`, the resulting ad group will adopt `GENDER_FEMALE` as the gender targeting configuration, reflecting what is set in the Saved Audience.
- If the `saved_audience_id` was created with `age_groups` specified, the age restriction rules outlined in [New age restrictions for ads on TikTok](https://business-api.tiktok.com/portal/docs?id=1788755983247362) for different advertising objectives also apply. Make sure that the age targeting setting is allowed before you use the Saved Audience (`saved_audience_id` ) in the ad group.
|
#|blocked_pangle_app_ids|string[]|Pangle app block ID list.

You can get an ID via the `app_package_id` field returned by [Get Pangle block list](https://business-api.tiktok.com/portal/docs?id=1740039957181441). It only takes effect when Pangle placement is selected.|
|budget_mode|string|
-  Required when Campaign Budget Optimization (CBO) is disabled  (`budget_optimize_on` is `false`) at the campaign level.
- Ignored when CBO is enabled  (`budget_optimize_on` is `true`) at the campaign level.
Ad group budget mode. 

Enum values:
- `BUDGET_MODE_TOTAL`: Lifetime budget.
- `BUDGET_MODE_DYNAMIC_DAILY_BUDGET`: Dynamic daily budget. It is the average daily budget over a week. Daily costs will not exceed 125% of the average daily budget. Weekly costs will not exceed the average daily budget * 7.

**Note**: 
- This setting, if specified, must be the same across all ad groups within the same campaign.
- If this field is set to `BUDGET_MODE_TOTAL`, then `schedule_type` must be `SCHEDULE_START_END`, which requires an end date (`schedule_end_time`).
- When at the campaign level `budget_optimize_on` is `false` and `budget_mode` is `BUDGET_MODE_DAY`, you can only set this field to `BUDGET_MODE_DYNAMIC_DAILY_BUDGET`. |
|budget_auto_adjust_strategy |string|Valid only when the following conditions are all met: 
- At the campaign level: `budget_optimize_on` is `false`. 
- At the ad group level: When `objective_type` is `APP_PROMOTION`: `budget_mode` is `BUDGET_MODE_DYNAMIC_DAILY_BUDGET`.
- `optimization_goal` is `VALUE`.
- `deep_bid_type` is `VO_MIN_ROAS`.
- `vbo_window` is `ZERO_DAY`. 
- When `objective_type` is `LEAD_GENERATION`:`budget_mode` is `BUDGET_MODE_DYNAMIC_DAILY_BUDGET`.
- `bid_type` is`BID_TYPE_CUSTOM`. 
The ad group budget strategy for custom ad group budget.

Enum values: 
- `AUTO_BUDGET_INCREASE`: To enable Goal-based budget increase. Allow your budget to automatically increase when your ads are performing well and target CPA, Day 0 target ROAS, and budget requirements are met.  When `budget_auto_adjust_strategy` is `AUTO_BUDGET_INCREASE`, the specified `budget` will be the initial daily budget. Your daily budget will be allowed to automatically increase by 20%, up to 10 times per day, when your budget utilization reaches 90% or more. Your daily budget will reset to your original daily budget each day.
- `UNSET`: To disable Goal-based  budget increase.
**Note**: Enabling Goal-based budget increase is currently an allowlist-only feature. If you would like to access it, please contact your TikTok representative.|
|budget|float|
- Required when Campaign Budget Optimization (CBO) is disabled  (`budget_optimize_on` is `false`) at the campaign level.
- Ignored when CBO is enabled  (`budget_optimize_on` is `true`) at the campaign level.
Fixed ad group budget or initial ad group budget.
- When `budget_auto_adjust_strategy`  is `UNSET`, this field represents your fixed ad group budget.
- When `budget_auto_adjust_strategy`  is `AUTO_BUDGET_INCREASE`, this field represents your initial ad group budget. To retrieve the current campaign budget, check the returned `current_budget`.
For how to configure budget settings, see [Budget](https://business-api.tiktok.com/portal/docs?id=1739381246298114). To directly see the daily budget value range for a currency, see [Currency-Daily budget value range](https://business-api.tiktok.com/portal/docs?id=1737585839634433#item-link-Daily%20budget%20value%20range).|
|min_budget|float|Valid only when the following conditions are all met:
- At the campaign level:`budget_optimize_on` is `true`
- `budget_mode` is `BUDGET_MODE_DYNAMIC_DAILY_BUDGET`
- At the ad group level:`bid_type` is `BID_TYPE_NO_BID`
Ad group minimum budget.

The system will aim to spend at least this amount, but it is not guaranteed.|
|schedule_type {Required}|string|Schedule type.

Enum values:
- `SCHEDULE_FROM_NOW`: To run the ad group continuously after the scheduled start time.You can only set `schedule_type` to `SCHEDULE_FROM_NOW` in any of the following scenarios:At the campaign level, `budget_mode` is `BUDGET_MODE_DYNAMIC_DAILY_BUDGET` 
- At the ad group level, `budget_mode` is `BUDGET_MODE_DYNAMIC_DAILY_BUDGET`
- `SCHEDULE_START_END`: To run the ad group between the scheduled start time and end time.|
|schedule_start_time {Required}|string|Schedule start time, in the format of`YYYY-MM-DD HH:MM:SS` (UTC+0).

The start time can be up to 12 hours earlier than the current time, but cannot be later than `2028-01-01 00:00:00`.|
|schedule_end_time {+Conditional}|string|Required when `schedule_type` is `SCHEDULE_START_END`.

Schedule end time, in the format of `YYYY-MM-DD HH:MM:SS` (UTC+0).

The end time cannot be later than `2038-01-01 00:00:00`.|
|movie_premiere_date|string|Valid when the following conditions are both met:
- `is_promotional_campaign` is `true` at the campaign level.
- You are allowlisted to use promotion campaign settings for theatrical releases.
The theatrical release date, in the format of `YYYY-MM-DD` (UTC+0).

Providing the movie release date allows the system to incorporate this timing into performance enhancements.|
|dayparting|string|Ad delivery arrangement, in the format of a string that consists of 48 x 7 characters. 
Each character is mapped to a 30-minute timeframe from Monday to Sunday. Each character can be set to either 0 or 1. 1 represents delivery in the 30-minute timeframe, and 0 stands for non-delivery in the 30-minute timeframe. The first character is mapped to 0:01-0:30 of Monday; The second character is mapped to 0:31-1:00 of Monday, and the last character represents 23:31-0:00 Sunday.

**Note**: An all-1 value and when this field is not specified, are considered full-time delivery.
|
|is_hfss|boolean|Valid only when `targeting_optimization_mode` is `MANUAL`.

Whether the promoted content is HFSS (High Fat, Salt, Sugar) Product/Brand.

If your ad is promoting or prominently featuring a product/brand classed as high in fat, salt or sugar, set this field to `true`.

In regulated regions, HFSS ads must only be targeted to users aged 18 or over.

You can set this field to `true`when your targeting locations include locations in the UK, Australia, New Zealand, and the European Union. 

Supported values: `true`, `false`.

Default value: `false`.|
|is_lhf_compliance {+Conditional}|boolean|When the targeting locations include locations in the UK and `is_hfss` is `true`, this field is required and must be set to `true`.

Whether the promoted content complies with LHF (Less Healthy Foods) regulations.

By setting `is_lhf_compliance` to `true`, you confirm that any food or drink products you advertise on TikTok in the UK comply with the [2024 Less Healthy Foods Regulations](https://www.legislation.gov.uk/uksi/2024/1266/made) and all other applicable laws.

Supported values: `true`, `false`.

Default value: `false`.|
|placement_type|string|The placement strategy that decides where your ads will be shown.

Enum values:
- `PLACEMENT_TYPE_AUTOMATIC`: Automatic Placement. TikTok's ad system will use smart calculations to give you the best combination of ad placements across all apps.
- `PLACEMENT_TYPE_NORMAL`: Select Placement. By selecting your placement manually, you\'ll be able to choose the apps to deliver your ads on.
By default, the system will automatically configure placements for your Upgraded Smart+ Campaigns based on your other settings and select high-quality traffic from various placements to deliver better results.

However, in cases where only Select Placement is supported, omitting the placement parameters (`placement_type` and `placements`) might trigger a placement error. In such cases, you need to manually set `placement_type` to `PLACEMENT_TYPE_NORMAL` and specify `placements`.

**Note**:
- `placement_type` cannot be updated after the ad group has been created.
- If you set this field to `PLACEMENT_TYPE_AUTOMATIC`, the actual supported placements will be shown in the returned `placements`. For instance, if the actual supported placement is TikTok only, the returned `placements` value will be `PLACEMENT_TIKTOK`.|
|placements {+Conditional}|string[]|
-  When `placement_type` is `PLACEMENT_TYPE_NORMAL`, this field is required.
- When `placement_type` is `PLACEMENT_TYPE_AUTOMATIC`, this field is ignored and overwritten to the combination of ad placements that the TikTok ad system selects for your ad.
The apps where you want to deliver your ads.

Enum values:
- `PLACEMENT_TIKTOK`: TikTok.
- `PLACEMENT_PANGLE`: Pangle.
- `PLACEMENT_GLOBAL_APP_BUNDLE`: Global App Bundle.

**Note**:
- `placements` cannot be updated after the ad group has been created.
- The available locations you can target with the Global App Bundle placement (`PLACEMENT_GLOBAL_APP_BUNDLE`) are: Brazil, Indonesia, Vietnam, the Philippines, Thailand, Malaysia, Mexico, Saudi Arabia, and Japan.
- The Global App Bundle placement (`PLACEMENT_GLOBAL_APP_BUNDLE`) does not support the optimization goal Landing Page View (`optimization_goal`=`TRAFFIC_LANDING_PAGE_VIEW`). To learn about the optimization goal, refer to the section [Enumerations-Optimization Goal](https://business-api.tiktok.com/portal/docs?id=1737174886619138#item-link-Optimization%20Goal).  |
|comment_disabled|boolean|Whether to allow comments on your campaigns on TikTok.

Supported values: `true`, `false`.

Default value: `false`.|
|share_disabled|boolean|Whether to disable sharing of the campaign to third-party platforms.

Supported values: `true`, `false`.

Default value: `false`.|
|video_download_disabled|boolean|Whether users can download your video ads on TikTok.

Supported values: `true`, `false`.

Default value: `false`.|
```
### Example
#### Automatic targeting without audience suggestions
```xcodeblock
(code curl http)
curl --location --request POST 'https://business-api.tiktok.com/open_api/v1.3/smart_plus/adgroup/create/' \
--header 'Access-Token: "{{Access-Token}}" ' \
--header 'Content-Type: application/json' \
--data '{
    "advertiser_id": "{{advertiser_id}}",
    "campaign_id": "{{campaign_id}}",
    "request_id": "{{request_id}}",
    "adgroup_name": "{{adgroup_name}}",
    "app_id": "{{app_id}}",
    "promotion_type": "APP_ANDROID",
    "optimization_goal": "INSTALL",
    "bid_type": "BID_TYPE_NO_BID",
    "billing_event": "OCPM",
    "schedule_type": "SCHEDULE_START_END",
    "schedule_start_time": "{{schedule_start_time}}",
    "schedule_end_time": "{{schedule_end_time}}",
    "targeting_optimization_mode": "AUTOMATIC",
    "targeting_spec": {
        "location_ids": [
            "1562822"
        ],
        "spc_audience_age": "OVER_EIGHTEEN",
        "operating_systems": [
            "ANDROID"
        ]
    }
}'

(/code)
```

#### Automatic targeting with audience suggestions
```xcodeblock
(code curl http)
curl --location --request POST 'https://business-api.tiktok.com/open_api/v1.3/smart_plus/adgroup/create/' \
--header 'Access-Token: "{{Access-Token}}"' \
--header 'Content-Type: application/json' \
--data '{
    "advertiser_id": "{{advertiser_id}}",
    "campaign_id": "{{campaign_id}}",
    "request_id": "{{request_id}}",
    "adgroup_name": "{{adgroup_name}}",
    "app_id": "{{app_id}}",
    "promotion_type": "APP_ANDROID",
    "optimization_goal": "INSTALL",
    "bid_type": "BID_TYPE_NO_BID",
    "billing_event": "OCPM",
    "schedule_type": "SCHEDULE_START_END",
    "schedule_start_time": "{{schedule_start_time}}",
    "schedule_end_time": "{{schedule_end_time}}",
    "targeting_optimization_mode": "AUTOMATIC",
    "suggestion_audience_enabled": true,
    "targeting_spec": {
        "location_ids": [
            "1562822"
        ],
        "spc_audience_age": "OVER_EIGHTEEN",
        "operating_systems": [
            "ANDROID"
        ],
        "age_groups": [
            "AGE_18_24",
            "AGE_25_34",
            "AGE_35_44",
            "AGE_45_54",
            "AGE_55_100"
        ],
        "gender": "GENDER_UNLIMITED",
        "audience_ids": [
            "{{audience_id}}",
            "{{audience_id}}",
            "{{audience_id}}",
            "{{audience_id}}"
        ],
        "interest_category_ids": [
            "17",
            "10"
        ],
        "purchase_intention_keyword_ids": [
            "14",
            "17"
        ],
        "actions": [
            {
                "action_scene": "VIDEO_RELATED",
                "action_period": 15,
                "video_user_actions": [
                    "WATCHED_TO_END",
                    "LIKED",
                    "COMMENTED",
                    "SHARED"
                ],
                "action_category_ids": [
                    "13",
                    "15"
                ]
            },
            {
                "action_scene": "CREATOR_RELATED",
                "action_period": 0,
                "video_user_actions": [
                    "FOLLOWING",
                    "VIEW_HOMEPAGE"
                ],
                "action_category_ids": [
                    "8",
                    "10"
                ]
            },
            {
                "action_scene": "HASHTAG_RELATED",
                "action_period": 0,
                "video_user_actions": [
                    "VIEW_HASHTAG"
                ],
                "action_category_ids": [
                    "8",
                    "5"
                ]
            }
        ]
    }
}'

(/code)
```

#### Custom targeting
```xcodeblock
(code curl http)
curl --location --request POST 'https://business-api.tiktok.com/open_api/v1.3/smart_plus/adgroup/create/' \
--header 'Access-Token: "{{Access-Token}}"' \
--header 'Content-Type: application/json' \
--data '{
    "advertiser_id": "{{advertiser_id}}",
    "campaign_id": "{{campaign_id}}",
    "request_id": "{{request_id}}",
    "adgroup_name": "{{adgroup_name}}",
    "app_id": "{{app_id}}",
    "promotion_type": "APP_ANDROID",
    "optimization_goal": "INSTALL",
    "bid_type": "BID_TYPE_NO_BID",
    "billing_event": "OCPM",
    "schedule_type": "SCHEDULE_START_END",
    "schedule_start_time": "{{schedule_start_time}}",
    "schedule_end_time": "{{schedule_end_time}}",
    "targeting_optimization_mode": "MANUAL",
    "targeting_spec": {
        "location_ids": [
            "1562822"
        ],
        "age_groups": [
            "AGE_18_24",
            "AGE_25_34",
            "AGE_35_44",
            "AGE_45_54",
            "AGE_55_100"
        ],
        "gender": "GENDER_UNLIMITED",
        "audience_ids": [
            "{{audience_id}}",
            "{{audience_id}}",
            "{{audience_id}}",
            "{{audience_id}}"
        ],
        "interest_category_ids": [
            "17",
            "10"
        ],
        "purchase_intention_keyword_ids": [
            "14",
            "17"
        ],
        "actions": [
            {
                "action_scene": "VIDEO_RELATED",
                "action_period": 15,
                "video_user_actions": [
                    "WATCHED_TO_END",
                    "LIKED",
                    "COMMENTED",
                    "SHARED"
                ],
                "action_category_ids": [
                    "13",
                    "15"
                ]
            },
            {
                "action_scene": "CREATOR_RELATED",
                "action_period": 0,
                "video_user_actions": [
                    "FOLLOWING",
                    "VIEW_HOMEPAGE"
                ],
                "action_category_ids": [
                    "8",
                    "10"
                ]
            },
            {
                "action_scene": "HASHTAG_RELATED",
                "action_period": 0,
                "video_user_actions": [
                    "VIEW_HASHTAG"
                ],
                "action_category_ids": [
                    "8",
                    "5"
                ]
            }
        ],
        "smart_interest_behavior_enabled": false,
        "smart_audience_enabled": true,
        "spending_power": "HIGH",
        "operating_systems": [
            "ANDROID"
        ]
    }
}'

(/code)
```

## Response

```xtable
|Field{30%}|Data Type{15%}|Description{55%}|
|-|-|-|
|code |number|Response code. For the complete list of response codes and descriptions, see [Appendix-Return Code](https://ads.tiktok.com/marketing_api/docs?id=1737172488964097). |
|message|string|Response message. For details, see [Appendix - Return Codes](https://ads.tiktok.com/marketing_api/docs?id=1737172488964097).|
|request_id |string|The log ID of a request, which uniquely identifies the request.  |
|data |object|Returned data.|
#|advertiser_id|string|Advertiser ID.|
#|campaign_id|string|Campaign ID.|
#|campaign_name|string|The name of the campaign that the ad group belongs to.|
#|adgroup_id|string|Ad group ID.|
#|adgroup_name|string|Ad group name.|
#|catalog_id|string|Returned when `catalog_enabled` is  `true` at the campaign level.

The ID of the catalog used in the ad group.|
#|catalog_authorized_bc_id|string|Returned when `catalog_enabled` is  `true` at the campaign level.

The ID of the Business Center that the catalog (`catalog_id`) belongs to.|
#|promotion_type|string|Promotion type (Optimization location). You can decide where you'd like to promote your products using this field.

Currently, we support `APP_ANDROID`, `APP_IOS`, `WEBSITE`, `MINI_GAME`, and `LEAD_GENERATION`.
- When `objective_type` is `APP_PROMOTION`  and `app_promotion_type` is `APP_INSTAL`, this field will be `APP_ANDROID` or `APP_IOS`.
- When `objective_type` is `APP_PROMOTION` and `app_promotion_type` is `MINIS`, this field will be `MINI_APP` or `MINI_GAME`.
- When `objective_type` is `WEB_CONVERSIONS`:If `sales_destination` is `WEBSITE`, this field will be `WEBSITE`.
- If `sales_destination` is `APP`, this field will be `APP_ANDROID` or `APP_IOS`.
- When `objective_type` is `LEAD_GENERATION`, this field will be any of the following values:`LEAD_GENERATION`
- `LEAD_GEN_CLICK_TO_TT_DIRECT_MESSAGE`
- `LEAD_GEN_CLICK_TO_SOCIAL_MEDIA_APP_MESSAGE`
- `LEAD_GEN_CLICK_TO_CALL`|
#|app_id |string|The App ID of the app to promote.

To get a list of App IDs, use [/app/list/](https://business-api.tiktok.com/portal/docs?id=1740859313270786).|
#| gaming_ad_compliance_agreement|string|Returned only in any of the following scenarios:
- Scenario 1: When the following conditions are both met at the campaign level:`objective_type` is `APP_PROMOTION`.
- `app_promotion_type` is `APP_RETARGETING`.
- Scenario 2: When the following conditions are all met at the campaign level:`objective_type` is `APP_PROMOTION`.
- `app_promotion_type` is `APP_INSTALL`.
- `campaign_type` is `REGULAR_CAMPAIGN`.
Whether to agree to the Compliance Assurance Policy for Gaming Advertisers on TikTok.

The policy is as follows: Yo confirms and attest that any gaming application, product or service (game) you desire to advertise on TikTok, including any associated URL(s), (a) complies with all applicable laws and regulations of the jurisdictions where the game can be accessed or played, and upon request, can provide supporting documentation as evidence of why the game is not considered illegal gambling or lottery; and (b) has not been and is not part of any investigation or lawsuit regarding the game's legality or regulatory compliance.

Enum values:
- `ON`: To agree to the policy.
- `OFF`: To leave the policy not accepted.|
#|promotion_website_type|string|TikTok Instant Page type.

Currently, we only support `TIKTOK_NATIVE_PAGE`(To use TikTok Instant Page).|
#|promotion_target_type|string|The optimization location for Lead Generation objective.

Enum values:
- `INSTANT_PAGE`: Instant Form. To create a fast-loading in-app TikTok Instant Form to collect more leads.
- `EXTERNAL_WEBSITE`: Website Form. To use a landing page that has the Website Form or the TikTok Instant Page that redirects to the website with the Website Form to collect more leads.|
#|optimization_goal|string|The measurable results that you'd like to drive your ads with.

For enum values, see [Enumeration - Optimization Goal](https://business-api.tiktok.com/portal/docs?id=1737174886619138#item-link-Optimization%20Goal).|
#|pixel_id|string|Pixel ID.|
#| app_config | object[] | Returned when `sales_destination` is `WEB_AND_APP`.

Details of the app or apps to promote. |
##| app_id | string | The App ID of the app to promote. |
#| minis_id|string|Returned when `promotion_type` is `MINI_APP` or `MINI_GAME`.

The ID of the TikTok Minis.|
#|optimization_event|string|Conversion event for the ad group.

See [Conversion events](https://business-api.tiktok.com/portal/docs?id=1739361474981889) for more.|
#|custom_conversion_id|string|The ID of the Custom Conversion used in the ad group.|
#|deep_funnel_optimization_status|string|With deep funnel optimization, you can select a secondary event alongside the primary optimization event, which can help improve campaign effectiveness.  

Enum values:  
- `ON`: enabled.
- `OFF`: disabled.|
#|deep_funnel_event_source|string|Returned when `deep_funnel_optimization_status` is `ON`.

The event source type.

Enum values:
- `PIXEL`: Pixel.
- `OFFLINE`: Offline Event Set.
- `CRM`: CRM Event Set.|
#|deep_funnel_event_source_id|string|Returned when `deep_funnel_optimization_status` is `ON`.

Event Source ID.
- When `deep_funnel_event_source` is `PIXEL` , this field represents a Pixel ID.
- When `deep_funnel_event_source` is `OFFLINE`, this field represents an Offline Event Set ID.
- When `deep_funnel_event_source` is `CRM`, this field represents a CRM Event Set ID.|
#|deep_funnel_optimization_event|string|Returned when `deep_funnel_optimization_status` is `ON`.

Deep funnel optimization event.

Example: `SHOPPING`.|
#| identity_id|string|Returned only when `promotion_type` is `LEAD_GEN_CLICK_TO_TT_DIRECT_MESSAGE` and your ad account is allowlisted for selecting a TikTok account at the ad group level in TikTok Direct Messaging Ads.

Identity ID.|
#| identity_type |string|Returned only when `promotion_type` is `LEAD_GEN_CLICK_TO_TT_DIRECT_MESSAGE` and your ad account is allowlisted for selecting a TikTok account at the ad group level in TikTok Direct Messaging Ads.

Identity type.

Enum values: 
- `TT_USER` : TikTok Business Account User.
- `BC_AUTH_TT`: The TikTok account that a Business Center is authorized to access.
See [Identities](https://business-api.tiktok.com/portal/docs?id=1738958351620097) for details.|
#| identity_authorized_bc_id|string|Returned when `identity_type` is `BC_AUTH_TT`.

ID of the Business Center that a TikTok Account User in Business Center identity is associated with.|
#| messaging_app_type|string|The type of instant messaging app or customized URL to use in the Instant Messaging Ad Group.

Enum values:
- `MESSENGER`: Messenger. 
- `WHATSAPP`: WhatsApp. 
- `ZALO`: Zalo. 
- `LINE`: Line. 
- `IM_URL`: Instant Messaging URL.
To learn more about how to create Upgraded Smart+ TikTok Instant Messaging Ads, see [Create an Upgraded Smart+ Lead Generation Campaign with optimization location as instant messaging apps](https://business-api.tiktok.com/portal/docs?id=1847302988449921).|
#| zalo_id_type |string|The type of Zalo contact format.

Enum values:
- `ZALO_OFFICIAL_ACCOUNT`: Zalo Official Account ID. 
- `ZALO_PHONE_ACCOUNT`: Zalo phone number. |
#| messaging_app_account_id |string|The ID of the instant messaging app account.
- When `messaging_app_type` is `MESSENGER`, this field represents the Facebook Page ID.
- When `messaging_app_type` is `LINE`, this field represents the LINE Business ID.
- When `zalo_id_type` is `ZALO_OFFICIAL_ACCOUNT`, this field represents the Zalo Official Account ID.
- When `messaging_app_type` is `WHATSAPP` or when `zalo_id_type` is `ZALO_PHONE_ACCOUNT`, this field represents the WhatsApp or Zalo phone number automatically populated based on the specified `phone_info`.|
#| message_event_set_id|string|The ID of the message event set to be used in the Instant Messaging Ad Group.

If the instant messaging app account, either the Messenger account or Zalo Official Account specified via `messaging_app_account_id` or the WhatsApp or Zalo phone account matched from the specified `phone_info`, in your ad group settings matches an existing event set, this field will be **automatically populated** with the unique message event set associated with the instant messaging app account you choose.|
#| phone_info|object|Details of WhatsApp or Zalo phone number.|
##| phone_region_code |string|The region code for WhatsApp or Zalo phone number.

Example: `US`.|
##| phone_region_calling_code|string|The region calling code for the WhatsApp or Zalo phone number.

Example: `+1`.|
##| phone_number|string|The WhatsApp or Zalo phone number.|
#|bid_type|string|Bidding strategy.

For enum values and their descriptions, see [Enumeration - Bidding Strategy](https://business-api.tiktok.com/portal/docs?id=1737174886619138#item-link-Bidding%20Strategy).|
#|bid_price|float|The target cost per click. The system will aim to get the most results while keeping the average cost per result around or lower than the specified amount.|
#|conversion_bid_price|float|The target cost per conversion or cost per landing page view. The system will aim to get the most results while keeping the average cost per result around or lower than the specified amount.|
#|deep_bid_type|string|Bidding strategy for in-app events.

For enum values and their descriptions, see [Enumeration - Deep Event Bidding Strategy](https://business-api.tiktok.com/portal/docs?id=1737174886619138#item-link-Deep%20Event%20Bidding%20Strategy).|
#|roas_bid|float|Target ROAS for Value-Based Optimization.|
#| incentive_offer_type|string|The type of incentive offer applicable to the Upgraded Smart+ Ad Group.
If your ad group meets the eligibility criteria and exceeds certain CPA or Minimum ROAS/Target ROAS thresholds, you will be incentivized with ad credits to use within the same ad account.
To learn more about the incentive offer eligibility criteria and the calculation of incentive amount, see [Smart+ Platform Incentive Offer (Cost Cap/Minimum ROAS/Target ROAS)](https://ads.tiktok.com/help/article/incentive-offer). 

Enum values:
- `INELIGIBLE`: The ad group is ineligible for any incentive offer.
- `COST_CAP_AND_MIN_ROAS`: The ad group uses the Cost Cap or Minimum ROAS/Target ROAS bidding strategy and is eligible for the incentive offer. |
#|vbo_window|string|The time window of the specified bidding strategy for [VBO IAA](https://business-api.tiktok.com/portal/docs?id=1739381743067137) (Value-Based Optimization for in-app advertising) or [VBO IAP](https://business-api.tiktok.com/portal/docs?id=1739381743067137) (Value-Based Optimization for in-app purchase).

Enum values:
- `SEVEN_DAYS`: The first seven days (day 7).
- `ZERO_DAY`: The current day (day 0).|
#|click_attribution_window|string|Click-through window. This attribution window is the time between when a person clicks your ad and then takes an action.

Enum values:
- `OFF`: Off.
- `ONE_DAY`: 1-day click.
- `SEVEN_DAYS`: 7-day click.
- `FOURTEEN_DAYS`: 14-day click.
- `TWENTY_EIGHT_DAYS`: 28-day click.
- `THIRTY_DAYS`: 30-day click.
- `THIRTY_TWO_DAYS`: 32-day click.
- `ONE_HUNDRED_EIGHTY_DAYS`: 180-day click.|
#| engaged_view_attribution_window | string | Engaged view-through window. This attribution window is the time after someone watches at least 6 seconds of your video ad that a conversion is counted.

Enum values:
- `OFF`: off.
- `ONE_DAY`: 1-day engaged view.
- `SEVEN_DAYS`: 7-day engaged view.
- `FOURTEEN_DAYS`: 14-day engaged view.
- `TWENTY_EIGHT_DAYS`: 28-day engaged view.|
#|view_attribution_window|string|View-through window. This attribution window is the time between when a person views your ad and then takes an action.

Enum values:
- `OFF`: Off.
- `ONE_DAY`: 1-day view.
- `SEVEN_DAYS`: 7-day view.|
#|attribution_event_count|string|Event count (Statistic type).

The way that people's actions are counted after only viewing or clicking an ad.

Enum values:
- `UNSET`: Unset.
- `EVERY`: Every. To count multiple events from someone as separate conversions.
- `ONCE`: Once. To count multiple events from someone as 1 conversion.|
#|billing_event|string|Billing event.

For enum values, see [Enumerations - Billing event](https://business-api.tiktok.com/portal/docs?id=1737174886619138#item-link-Billing%20Event).|
#|pacing|string|Delivery type. Your choice of ad delivery type determines the speed at which your daily budget is used.

Enum values:
- `PACING_MODE_SMOOTH`: Standard. Your budget will be used as evenly as possible depending on market demand and peaktime rates. This delivery type is suitable for advertisers who prefer steady spending.|
#|budget_mode|string|Ad group budget mode. 

Enum values:
- `BUDGET_MODE_TOTAL`: Lifetime budget.
- `BUDGET_MODE_DYNAMIC_DAILY_BUDGET`: Dynamic daily budget. It is the average daily budget over a week. Daily costs will not exceed 125% of the average daily budget. Weekly costs will not exceed the average daily budget * 7.|
#| budget_auto_adjust_strategy |string|Returned only when the following conditions are both met:
- At the campaign level: `budget_optimize_on` is `false`.
- At the ad group level: `budget_mode` is `BUDGET_MODE_DYNAMIC_DAILY_BUDGET`.
The ad group budget strategy for custom ad group budget.

Enum values: 
- `AUTO_BUDGET_INCREASE`: To enable Goal-based budget increase. Allow your budget to automatically increase when your ads are performing well and target CPA, Day 0 target ROAS, and budget requirements are met. 
- When `budget_auto_adjust_strategy` is `AUTO_BUDGET_INCREASE`, the specified `budget` will be the initial daily budget. Your daily budget will be allowed to automatically increase by 20%, up to 10 times per day, when your budget utilization reaches 90% or more. Your daily budget will reset to your original daily budget each day.
- `UNSET`: To disable Goal-based budget increase.|
#|budget|float|Fixed ad group budget or initial ad group budget.
- When `budget_auto_adjust_strategy`  is `UNSET`, this field represents your fixed ad group budget.
- When `budget_auto_adjust_strategy`  is `AUTO_BUDGET_INCREASE`, this field represents your initial ad group budget. To retrieve the current campaign budget, check the returned `current_budget`.|
#| current_budget|float|Returned only when `budget_auto_adjust_strategy`  is `AUTO_BUDGET_INCREASE`.

Current ad group budget for an ad group with Goal-based budget increase enabled.|
#|min_budget|float|Ad group minimum budget. 

The system will aim to spend at least this amount, but it is not guaranteed.|
#|schedule_type|string|Schedule type.

Enum values:
- `SCHEDULE_FROM_NOW`: To run the ad group continuously after the scheduled start time.
- `SCHEDULE_START_END`: To run the ad group between the scheduled start time and end time.|
#|schedule_start_time|string|Ad group delivery start time, in the format of `YYYY-MM-DD HH:MM:SS` (UTC+0).|
#|schedule_end_time|string|Ad group delivery end time, in the format of`YYYY-MM-DD HH:MM:SS` (UTC+0).|
#| movie_premiere_date|string|The theatrical release date, in the format of `YYYY-MM-DD` (UTC+0).

Providing the movie release date allows the system to incorporate this timing into performance enhancements.|
#|dayparting|string|Ad delivery arrangement, in the format of a string that consists of 48 x 7 characters. Each character is mapped to a 30-minute timeframe from Monday to Sunday. Each character can be set to either 0 or 1. 1 represents delivery in the 30-minute timeframe, and 0 stands for non-delivery in the 30-minute timeframe. The first character is mapped to 0:01-0:30 of Monday; The second character is mapped to 0:31-1:00 of Monday, and the last character represents 23:31-0:00 Sunday.

**Note**: All-0 and all-1 values are considered full-time delivery.
|
#|targeting_optimization_mode|string|Audience targeting optimization mode.
- `MANUAL`: Custom targeting. You can use custom targeting settings to precisely control who sees your ads. This may limit delivery and impact campaign performance.
- `AUTOMATIC`: Automatic targeting. You can use automatic targeting to leverage real-time data and machine learning to target audiences most likely to engage with your ads|
#|suggestion_audience_enabled|boolean|Whether to enable audience suggestions.

Audience suggestions guide automatic targeting by choosing additional audience settings. These serve as suggestions only, and delivery to those audiences is not guaranteed.

Supported values: `true`, `false`.|
#|targeting_spec|object|Targeting settings.|
##| app_targeting_type |string|Returned only when the following conditions are all met:
- At the campaign level:
- `objective_type` is `WEB_CONVERSIONS`
- `sales_destination` is `APP`.
- `optimization_goal` is `CLICK`, `IN_APP_EVENT`, or `VALUE`.
App targeting type.

Enum values:
- `PROSPECT`: Prospecting. Find prospective customers, including those who have not interacted with your products.
- `RETARGETING`: Retargeting. Show ads to people who have already interacted with your business on and off TikTok.|
##|location_ids|string[]|IDs of the locations that you want to target.|
##|zipcode_ids|string[]|Zip code IDs or postal code IDs of the targeted locations.|
##|spc_audience_age|string|The age group that the ad group targets.

Enum values:
- `ALL`: all age groups.
- `OVER_EIGHTEEN`: 18+.
- `OVER_TWENTY_FIVE`: 25+.|
##|languages|string[]|Codes of the languages that you want to target. 

For the list of language codes supported, see [Enumerations - Language Code](https://business-api.tiktok.com/portal/docs?id=1737174886619138#item-link-Language%20Code).|
##|operating_systems|string[]|Device operating systems that you want to target. 

Enum values: `ANDROID`, `IOS`|
##|excluded_audience_ids|string[]|List of audience IDs to be excluded.|
##|age_groups|string[]|Age groups you want to target. 

For enum values, see [Enumeration - Age Group](https://business-api.tiktok.com/portal/docs?id=1737174886619138#item-link-Age%20Group).|
##|gender|string|Gender that you want to target.

Enum values: `GENDER_FEMALE`, `GENDER_MALE`, `GENDER_UNLIMITED`.|
##|audience_ids|string[]|A list of audience IDs.|
##|shopping_ads_retargeting_type|string|The retargeting type.

Enum values:
- `LAB1`: Retargeting audiences who viewed products or added products to cart but didn't purchase products.
- `LAB2`: Retargeting audiences who added products to cart but didn't purchase products.
- `LAB3`: Retargeting audiences using custom combination.
- `OFF`: No retargeting.|
##|shopping_ads_retargeting_actions_days|number|Returned when `shopping_ads_retargeting_type` is `LAB1` or `LAB2`.

The valid time range for the specified audience action. Audiences who have completed the specified action within the time range will be retargeted.|
##|included_custom_actions|object[]|Details of the catalog audience to include.
Catalog audience is based on people's interactions with specific products and often drives better performance than custom audience.|
###|code|string|The custom action used to filter the audiences to be retargeted.

Enum values:
- `VIEW_PRODUCT`: The audience viewed the product.
- `ADD_TO_CART`: The audience added the product to the cart.
- `PURCHASE`: The audience purchased the product.|
###|days|integer|The time range used to filter the audiences that completed the specified action.|
##|excluded_custom_actions|object[]|Details of the catalog audience to exclude.
Improve ad performance by excluding products that people have already interacted with, ensuring they only see relevant ads from your brand.|
###|code|string|The custom action used to filter out the audiences.

Enum values:
- `VIEW_PRODUCT`: The audience viewed the product.
- `ADD_TO_CART`: The audience added the product to the cart.
- `PURCHASE`: The audience purchased the product.|
###|days|integer|The time range used to filter out the audiences that completed the specified action.|
##|shopping_ads_retargeting_custom_audience_relation|string|The logical relation between the retargeting audience specified by `shopping_ads_retargeting_type` and the custom audience specified by `audience_ids`.

Enum values:
- `OR`: To combine the retargeting audience and the custom audience to create the targeted audience. The ad group will target anyone in catalog or custom audiences.
- `AND`: To intersect between the retargeting audience and the custom audience to create the targeted audience. The ad group will target individuals who belong to both the retargeting audience and the custom audience.|
##|included_pangle_audience_package_ids|string[]|IDs of the Pangle audiences that you want to include. |
##|excluded_pangle_audience_package_ids|string[]|IDs of the Pangle audiences that you want to exclude. |
##|interest_category_ids|string[]|IDs of general interest keywords that you want to use to target audiences.|
##|interest_keyword_ids|string[]|IDs of additional interest categories that you want to use to target audience.

To search for additional interest categories, use [/targeting/search/](https://business-api.tiktok.com/portal/docs?id=1796638342793218) (recommended) or [/tool/interest_keyword/recommend/](https://business-api.tiktok.com/portal/docs?id=1763590884474882).|
##|purchase_intention_keyword_ids|string[]|IDs of purchase intention categories that you want to use to target audiences with an interest in purchases related to a content category.|
##|actions|object[]|A list of targeting behavioral category objects.|
###|action_scene|string|The type of user behavior that you want to target.

Enum values:
- `VIDEO_RELATED`: Video interactions.
- `CREATOR_RELATED`: Creator interactions.
- `HASHTAG_RELATED`: Hashtag interactions.|
###|action_period|number|The time period to include behaviors from.|
###|video_user_actions|string[]|The specific user interactions that you want to target for the user behavior type.
- If `action_scene` is `VIDEO_RELATED`, the allowed values are: `WATCHED_TO_END`,`LIKED`,`COMMENTED`,`SHARED`.
- If `action_scene` is `CREATOR_RELATED`, the allowed values are: `FOLLOWING`, `VIEW_HOMEPAGE`.
- If `action_scene` is `HASHTAG_RELATED`, the allowed value is `VIEW_HASHTAG`.|
###|action_category_ids|string[]|IDs of the video interactions categories, creator interactions categories, hashtags, or hashtag bundles that you want to use to target audiences.|
##|smart_interest_behavior_enabled|boolean|Whether Smart interests & behaviors is turned on.

Supported values: `true`, `false`.

To learn more about Smart interests & behaviors and how to turn on Smart interests & behaviors, see [Smart Targeting](https://business-api.tiktok.com/portal/docs?id=1783164662979586).|
##|smart_audience_enabled|boolean|Whether to turn on Smart audience.

Supported values: `true`, `false`.

To learn more about Smart audience and how to turn on Smart audience, see [Smart Targeting](https://business-api.tiktok.com/portal/docs?id=1783164662979586).|
##|spending_power|string|Spending power that you want to target. 

Enum values: `ALL`, `HIGH`. 

If it is set to `HIGH`, you can target high spending users who typically spend more on purchases on TikTok ads than average users.|
##|household_income|string[]|Household income that you want to target. 

Enum values: `TOP5`(Top 5% of ZIP codes), `TOP10`(Top 10% of ZIP codes), `TOP10_25`(Top 10% -25% of ZIP codes), `TOP25_50`(Top 25% - 50% of ZIP codes).|
##|min_android_version|string|Minimum Android version. 

For enum values, see [Enumeration - Minimum Android Version](https://business-api.tiktok.com/portal/docs?id=1737174886619138#item-link-Minimum%20Android%20Version).|
##|min_ios_version|string|Audience minimum ios version. 

For enum values, see [Enumeration - Minimum iOS Version](https://business-api.tiktok.com/portal/docs?id=1737174886619138#item-link-Minimum%20iOS%20Version).|
##|device_model_ids|string[]|List of device model IDs. |
##|network_types|string[]|Network types that you want to target. 

For enum values, see [Enumeration - Connection Type](https://business-api.tiktok.com/portal/docs?id=1737174886619138#item-link-Connection%20Type).|
##|carrier_ids|string[]|Carriers that you want to target. |
##|isp_ids|string[]|IDs of the targeted Internet service providers.|
##|device_price_ranges|number[]|Targeting device price range. 10000 means 1000+. The numbers must be in multiples of 50.

**Note**: The upper limit you set will be added by 50 and the resulting new number will be used as the actual upper limit for device targeting. The actual upper limit is shown in the ad group settings in TikTok Ads Manager. If you set and get the price range of [0, 250], it actually means [0, 300].
|
##|saved_audience_id|string|Returned when you have specified `saved_audience_id` when creating an ad group.

Saved Audience ID.|
##|blocked_pangle_app_ids|string[]|Pangle app block ID list.|
##|brand_safety_type|string|Inventory filter tier for the Smart+ Campaign.

Enum values:
- `EXPANDED_INVENTORY`: Expanded inventory. Your ads will not appear next to explicitly inappropriate content, but they may appear next to content that features mature themes.
- `STANDARD_INVENTORY`: Standard inventory. Your ads will appear next to content that is appropriate for most brands.
- `LIMITED_INVENTORY`: Limited inventory. Your ads will not appear next to content that contains mature themes.
- `NO_BRAND_SAFETY`: Full inventory without using any brand safety solution, which means your ads may appear next to some content featuring mature themes.

**Note**: The setting is automatically applied based on your [Brand Safety Hub](https://business-api.tiktok.com/portal/docs?id=1739381752981505#item-link-Brand%20Safety%20Hub) configurations. To retrieve the details of such settings for your ad account, use [/tiktok_inventory_filters/get/](https://business-api.tiktok.com/portal/docs?id=1830112550443073).
|
##|category_exclusion_ids|string[]|Content exclusion category IDs.|
#| is_hfss|boolean|Whether the promoted content is HFSS (High Fat, Salt, Sugar) Product/Brand.

Supported values: `true`, `false`.|
#| is_lhf_compliance |boolean|Whether the promoted content complies with LHF (Less Healthy Foods) regulations.

When `is_lhf_compliance` is `true`, you confirm that any food or drink products you advertise on TikTok in the UK comply with the [2024 Less Healthy Foods Regulations](https://www.legislation.gov.uk/uksi/2024/1266/made) and all other applicable laws.

Supported values: `true`, `false`.|
#|placement_type|string[]|The placement strategy that decides where your ads will be shown.

Enum values: 
- `PLACEMENT_TYPE_AUTOMATIC`: Automatic placement.
- `PLACEMENT_TYPE_NORMAL` : Select placement.|
#|placements|string[]|The apps where you want to deliver your ads.

Enum values: 
- `PLACEMENT_TIKTOK`: TikTok.
- `PLACEMENT_PANGLE`: Pangle.
- `PLACEMENT_GLOBAL_APP_BUNDLE`: Global App Bundle.|
#|search_result_enabled|boolean|Whether to include your ads in Search Ads, namely to show your ads to users when they search for your business on TikTok.

Supported values: `true`, `false`.|
#|comment_disabled|boolean|Whether to allow comments on your ads on TikTok.

Supported values: `true`, `false`.|
#|share_disabled|boolean|Whether to disable sharing of the campaign to third-party platforms.

Supported values: `true`, `false`.|
#|video_download_disabled|boolean|Whether users can download your video ads on TikTok.

Supported values: `true`, `false`.|
#|skip_learning_phase|boolean|Whether to skip the learning stage.

Supported value: `true`.|
#|create_time|string|The time when the ad group was created, in the format of `YYYY-MM-DD HH:MM:SS`(UTC+0).

Example: `2025-01-01 00:00:01`.|
#|modify_time|string|The time when the ad group was last modified, in the format of `YYYY-MM-DD HH:MM:SS`(UTC+0).

Example: `2025-01-01 00:00:01`.|
```
### Example
#### Automatic targeting without audience suggestions
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
        "create_time": "{{create_time}}",
        "dayparting": "111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111",
        "deep_bid_type": "DEFAULT",
        "engaged_view_attribution_window": "SEVEN_DAYS",
        "min_budget": 0,
        "modify_time": "{{modify_time}}",
        "operation_status": "ENABLE",
        "optimization_event": "ACTIVE",
        "optimization_goal": "INSTALL",
        "pacing": "PACING_MODE_SMOOTH",
        "placement_type": "PLACEMENT_TYPE_AUTOMATIC",
        "placements": [
            "PLACEMENT_TIKTOK",
            "PLACEMENT_GLOBAL_APP_BUNDLE",
            "PLACEMENT_PANGLE"
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
            "actions": [],
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
            "operating_systems": [
                "ANDROID"
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

#### Automatic targeting with audience suggestions
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
        "create_time": "{{create_time}}",
        "dayparting": "111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111",
        "deep_bid_type": "DEFAULT",
        "engaged_view_attribution_window": "SEVEN_DAYS",
        "min_budget": 0,
        "modify_time": "{{modify_time}}",
        "operation_status": "ENABLE",
        "optimization_event": "ACTIVE",
        "optimization_goal": "INSTALL",
        "pacing": "PACING_MODE_SMOOTH",
        "placement_type": "PLACEMENT_TYPE_AUTOMATIC",
        "placements": [
            "PLACEMENT_TIKTOK",
            "PLACEMENT_GLOBAL_APP_BUNDLE",
            "PLACEMENT_PANGLE"
        ],
        "promotion_type": "APP_ANDROID",
        "schedule_end_time": "{{schedule_end_time}}",
        "schedule_start_time": "{{schedule_start_time}}",
        "schedule_type": "SCHEDULE_START_END",
        "search_result_enabled": true,
        "secondary_status": "ADGROUP_STATUS_CREATE",
        "share_disabled": false,
        "skip_learning_phase": true,
        "suggestion_audience_enabled": true,
        "targeting_optimization_mode": "AUTOMATIC",
        "targeting_spec": {
            "actions": [
                {
                    "action_category_ids": [
                        "13",
                        "15"
                    ],
                    "action_period": 15,
                    "action_scene": "VIDEO_RELATED",
                    "video_user_actions": [
                        "WATCHED_TO_END",
                        "LIKED",
                        "COMMENTED",
                        "SHARED"
                    ]
                },
                {
                    "action_category_ids": [
                        "8",
                        "10"
                    ],
                    "action_period": 0,
                    "action_scene": "CREATOR_RELATED",
                    "video_user_actions": [
                        "FOLLOWING",
                        "VIEW_HOMEPAGE"
                    ]
                },
                {
                    "action_category_ids": [
                        "8",
                        "5"
                    ],
                    "action_period": 0,
                    "action_scene": "HASHTAG_RELATED",
                    "video_user_actions": [
                        "VIEW_HASHTAG"
                    ]
                }
            ],
            "age_groups": [
                "AGE_18_24",
                "AGE_25_34",
                "AGE_35_44",
                "AGE_45_54",
                "AGE_55_100"
            ],
            "audience_ids": [
                "{{audience_id}}",
                "{{audience_id}}",
                "{{audience_id}}",
                "{{audience_id}}"
            ],
            "brand_safety_type": "STANDARD_INVENTORY",
            "category_exclusion_ids": [
                "200",
                "201",
                "202",
                "203"
            ],
            "gender": "GENDER_UNLIMITED",
            "interest_category_ids": [
                "17",
                "10"
            ],
            "location_ids": [
                "1562822"
            ],
            "operating_systems": [
                "ANDROID"
            ],
            "purchase_intention_keyword_ids": [
                "14",
                "17"
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

#### Custom targeting
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
        "create_time": "{{create_time}}",
        "dayparting": "111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111",
        "deep_bid_type": "DEFAULT",
        "engaged_view_attribution_window": "SEVEN_DAYS",
        "min_budget": 0,
        "modify_time": "{{modify_time}}",
        "operation_status": "ENABLE",
        "optimization_event": "ACTIVE",
        "optimization_goal": "INSTALL",
        "pacing": "PACING_MODE_SMOOTH",
        "placement_type": "PLACEMENT_TYPE_AUTOMATIC",
        "placements": [
            "PLACEMENT_TIKTOK",
            "PLACEMENT_GLOBAL_APP_BUNDLE",
            "PLACEMENT_PANGLE"
        ],
        "promotion_type": "APP_ANDROID",
        "schedule_end_time": "{{schedule_end_time}}",
        "schedule_start_time": "{{schedule_start_time}}",
        "schedule_type": "SCHEDULE_START_END",
        "search_result_enabled": true,
        "secondary_status": "ADGROUP_STATUS_CREATE",
        "share_disabled": false,
        "skip_learning_phase": true,
        "suggestion_audience_enabled": false,
        "targeting_optimization_mode": "MANUAL",
        "targeting_spec": {
            "actions": [
                {
                    "action_category_ids": [
                        "13",
                        "15"
                    ],
                    "action_period": 15,
                    "action_scene": "VIDEO_RELATED",
                    "video_user_actions": [
                        "WATCHED_TO_END",
                        "LIKED",
                        "COMMENTED",
                        "SHARED"
                    ]
                },
                {
                    "action_category_ids": [
                        "8",
                        "10"
                    ],
                    "action_period": 0,
                    "action_scene": "CREATOR_RELATED",
                    "video_user_actions": [
                        "FOLLOWING",
                        "VIEW_HOMEPAGE"
                    ]
                },
                {
                    "action_category_ids": [
                        "8",
                        "5"
                    ],
                    "action_period": 0,
                    "action_scene": "HASHTAG_RELATED",
                    "video_user_actions": [
                        "VIEW_HASHTAG"
                    ]
                }
            ],
            "age_groups": [
                "AGE_18_24",
                "AGE_25_34",
                "AGE_35_44",
                "AGE_45_54",
                "AGE_55_100"
            ],
            "audience_ids": [
                "{{audience_id}}",
                "{{audience_id}}",
                "{{audience_id}}",
                "{{audience_id}}"
            ],
            "brand_safety_type": "STANDARD_INVENTORY",
            "category_exclusion_ids": [
                "200",
                "201",
                "202",
                "203"
            ],
            "gender": "GENDER_UNLIMITED",
            "interest_category_ids": [
                "17",
                "10"
            ],
            "location_ids": [
                "1562822"
            ],
            "operating_systems": [
                "ANDROID"
            ],
            "purchase_intention_keyword_ids": [
                "14",
                "17"
            ],
            "smart_audience_enabled": true,
            "smart_interest_behavior_enabled": false,
            "spending_power": "HIGH"
        },
        "video_download_disabled": false,
        "view_attribution_window": "ONE_DAY"
    }
}

(/code)
```
