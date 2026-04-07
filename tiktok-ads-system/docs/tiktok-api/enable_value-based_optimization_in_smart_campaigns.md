# Enable Value-Based Optimization in Smart+ Campaigns

**Doc ID**: 1840137502583809
**Path**: Marketing API/Campaign Management/Guides/Ad group/Bidding/Value-Based Optimization/Enable Value-Based Optimization in Smart+ Campaigns

---

This article walks you through the steps to enable Value-Based Optimization (VBO) in Smart+ Campaigns.

# Prerequisites
- You've gained access to TikTok API for Business. See [Get Started - Step by step workflow](https://ads.tiktok.com/marketing_api/docs?id=1735713609895937&rid=7llhcla7zmh) for details. 
  - To enable VBO, you need relevant permissions. See [API Reference](https://ads.tiktok.com/marketing_api/docs?id=1735713875563521) to find out permissions required for endpoints (including the endpoints listed in the "Steps" section) and see [Update app permissions](https://ads.tiktok.com/marketing_api/docs?id=1738855280338946&rid=7llhcla7zmh) to find out how to configure permissions.  
- VBO IAP (Value-Based Optimization for in-app purchases) and VBO IAA (Value-Based Optimization for in-app advertising) in different scenarios are currently allowlist-only features. If you would like to access them, please contact your TikTok representative.
- Some VBO IAA and VBO IAP features are available after you meet the unlocking criteria. To find out the unlocking criteria, refer to the **"Unlocking criteria for VBO"** section below. To learn more about VBO IAP and VBO IAA, see [Value-Based Optimization - Value types](https://business-api.tiktok.com/portal/docs?id=1739381743067137#item-link-Value%20types).

 
# Unlocking criteria for VBO
VBO will be automatically unlocked for the promoted App (`app_id`) or website (`pixel_id`) when the App or website meets the following unlocking criteria.

```xtable
| Promoted object {15%}| Unlocking criteria {35%}| Parameter {15%}| Requirement {35%}|
|---|---|---|
| App  (VBO IAP)| The criteria depend on the placement setting you want to use: 
-  To use Automatic Placement or non-Pangle-only Select Placement, the App needs to have at least **30 unique Purchase events with value attributed to TikTok or Global App Bundle placements over any consecutive 7 days. **
-  To use Pangle-only Select Placement, you need to first be allowlisted for VBO with Pangle-only placement. Then the App needs to have at least **50 unique Purchase events with value attributed to Pangle placement in its lifetime. ****Note**:
-  Once unlocked, VBO IAP will remain available to use for the app.
-  VBO with Pangle-only placement is currently an allowlist-only feature. If you would like to access it, please contact your TikTok representative.  | `app_id` | 
-  If you don't want to set `placements` to `PLACEMENT_PANGLE`, the App (`app_id`) needs to have at least 30 unique Purchase events (`optimization_event`= `ACTIVE_PAY`) , which are created with `value` specified in the `properties` object and attributed to TikTok or Global App Bundle placements over any consecutive 7 days. 
-  If you want to set `placements` to `PLACEMENT_PANGLE`, the App (`app_id`) needs to have at least 50 unique Purchase events (`optimization_event`= `ACTIVE_PAY`), which are created with `value` specified in the `properties` object and attributed to Pangle placement in its lifetime.  To check whether the App has accumulated enough events and is supported for a certain placement setting, pass `placements` and the App ID to [/tool/vbo_status/](https://ads.tiktok.com/marketing_api/docs?id=1770016073586753). If the App has accumulated enough events and is supported for the specified `placements`, the returned `vo_status` will be `QUALIFIED`. 
To report App Events for your App, use [/app/track/](https://ads.tiktok.com/marketing_api/docs?id=1740859196043266) or [/app/batch/](https://ads.tiktok.com/marketing_api/docs?id=1740859218541569). |
| App (VBO IAA) | To unlock VBO IAA for Automatic Placement, TikTok-only, or Pangle-only Select Placement, the App must meet the following requirements: 
-  The App is an Android App. 
-  The Mobile Measurement Partner for the App is AppsFlyer or Adjust.
-  The Ads impression ROAS for the App is greater than or equal to 1. 
**Note**: Once unlocked, VBO IAA will remain available to use for the app.  | `app_id` | To enable VBO IAA with `PLACEMENT_TYPE_AUTOMATIC`, `PLACEMENT_TIKTOK`, or `PLACEMENT_PANGLE`, the App (`app_id`) must meet the following requirements: 
-  The `platform` returned from [/app/info/](https://business-api.tiktok.com/portal/docs?id=1740859272887297) for the App is `ANDROID`.
-  The `partner_name` returned from [/app/info/](https://business-api.tiktok.com/portal/docs?id=1740859272887297)  for the App is `AppsFlyer` or `Adjust`.
-  The ** Ads impression ROAS** for the App meets or exceeds 1 during any previous time frame.  To confirm if the Ads impression ROAS requirement is met, you can use any of the following methods: **Method 1 (Recommended) **: Pass the `app_id` directly to [/tool/vbo_status/](https://ads.tiktok.com/marketing_api/docs?id=1770016073586753) to check whether the App is eligible for VBO IAA.
- **Method 2**: Run a synchronous basic report by using [/report/integrated/get/](https://business-api.tiktok.com/portal/docs?id=1740302848100353). Set `query_lifetime` to `true`, and include the In-app event metric `total_ad_impression_roas` and the attribute metric `tt_app_id` in the request parameter `metrics`. The Ads impression ROAS (`total_ad_impression_roas`) for the App (`tt_app_id`) should be equal to or greater than 1.   |
| Website | The pixel needs to have at least **20 unique Complete Payment events with value and currency attributed to TikTok, Pangle, or Global App Bundle placements over any consecutive 7 days. **
-  If the pixel, over any consecutive 7 days, obtained **at least 20** unique attributed Complete Payment events with value attributed to TikTok, and **another 20** attributed to Pangle, any placement is valid.  
-  If the pixel, over any consecutive 7 days, obtained **at least 20** unique attributed Complete Payment events with value attributed to TikTok, and **less than 20** attributed to Pangle, only the TikTok placement is valid. 
-  If the pixel, over any consecutive 7 days, obtained **less than 20** unique attributed Complete Payment events with value attributed to TikTok, and **more than 20 ** attributed to Pangle, only the Pangle placement is valid.  **Note**: Once unlocked, VBO will remain available to use for the pixel.| `pixel_id` | The pixel (`pixel_id`) needs to have at least 20 unique Complete Payment events (`optimization_event`= `SHOPPING`) , which are created with `value` and `currency` specified in the `properties` object and attributed to TikTok, Pangle, or Global App Bundle placements over any consecutive 7 days. 
-  If the pixel, over any consecutive 7 days, obtained at least 20 unique attributed Complete Payment events with value attributed to TikTok, and another 20 attributed to Pangle, any configurations through `placement_type` and `placements` are supported.
-  If the pixel, over any consecutive 7 days, obtained at least 20 unique attributed Complete Payment events with value attributed to TikTok, and less than 20 attributed to Pangle, you can only set `placements` to `PLACEMENT_TIKTOK`.
-  If the pixel, over any consecutive 7 days, obtained less than 20 unique attributed Complete Payment events with value attributed to TikTok, and more than 20 attributed to Pangle, you can only set `placements` to `PLACEMENT_PANGLE`.   To check whether the Pixel has accumulated enough events and is supported for a certain placement setting, pass `placements` and the Pixel ID to [/tool/vbo_status/](https://ads.tiktok.com/marketing_api/docs?id=1770016073586753). If the Pixel has accumulated enough events and is supported for the specified `placements`, the returned `vo_status` will be `QUALIFIED`. 
To report Pixel Events for your App, use [/pixel/track/](https://ads.tiktok.com/marketing_api/docs?id=1740858531237890) or [/pixel/batch/](https://ads.tiktok.com/marketing_api/docs?id=1740858565852225). |
```

# Steps
> **Note**

> Before enabling VBO, it is recommended to use [/tool/vbo_status/](https://ads.tiktok.com/marketing_api/docs?id=1770016073586753) to check whether your settings are eligible for VBO.

## Enable VBO for Smart+ App Campaigns
### Enable VBO for Smart+ Android App Campaigns
Create a Smart+ Campaign using [/campaign/spc/create/](https://business-api.tiktok.com/portal/docs?id=1767334204047362). Note that the following requirements must be met.

  
| 
    Setting | 
    Requirement | 
    Parameter | 
    How to configure the parameter | 
   |

  
| 
    Advertising Objective | 
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
	/ | 
   |
  
| 
    iOS 14 Dedicated Campaign | 
    Disabled | 
    `REGULAR_CAMPAIGN` or not specified. | 
   |
  
| 
    Optimization Location 
(Promotion type) | 
    An **Android** App that is eligible for VBO | 
    `promotion_type` | 
    `APP_ANDROID` | 
   |
  
| 
    `app_id` | 
    Specify the ID of an Android app that is eligible for VBO.

You can get IDs of Android Apps from [/app/list/](https://business-api.tiktok.com/portal/docs?id=1740859313270786). For Android Apps, the returned `platform` will be `ANDROID`.

To check whether an App ID is eligible for VBO, pass the App ID to the parameter `app_id` in [/tool/vbo_status/](https://business-api.tiktok.com/portal/docs?id=1770016073586753). | 
   |
  
| 
    Placement | 
    Any of the following types:
- **Automatic Placement**
- **Select Placement** with TikTok placement or Pangle placement or both | 
    `placement_type`
`placements` | 
    Any of the following configurations:
- Set `placement_type` to `PLACEMENT_TYPE_AUTOMATIC`
- Set `placement_type` to `PLACEMENT_TYPE_NORMAL`, and only include `PLACEMENT_TIKTOK` or `PLACEMENT_PANGLE` or both in the value of `placements` | 
   |
  
| 
    Optimization Goal | 
    Value | 
    `optimization_goal` | 
    `VALUE` | 
   |
  
| 
    Select Value | 
    Any of the following types:
- **Purchase value** (also known as VBO IAP)
- **Ad revenue value** (also known as VBO IAA) | 
    `optimization_event` | 
    
- If you want to use Purchase value, set `optimization_event` to `ACTIVE_PAY`.
- If you want to use Ad revenue value, set `optimization_event` to `AD_REVENUE_VALUE`. | 
   |
    
| 
    Bid Strategy | 
    Any of the following types:
- Highest Value: To spend your budget fully and maximize the value of results
- Minimum ROAS: To keep your average ROAS around or higher than the target ROAS value | 
    `deep_bid_type`
`roas_bid` | 
    Set `deep_bid_type` to `VO_MIN_ROAS` or `VO_HIGHEST_VALUE`.
**Note**: If you set `deep_bid_type` to `VO_MIN_ROAS`, pass in `roas_bid` at the same time. | 
   |
  
| 
    `bid_type | 
    BID_TYPE_NO_BID` | 
   |
  
| 
    `conversion_bid_price | 
    Not specified | 
   | 
  
| 
    Time Window of the Bid Strategy | 
    Any of the following types:
- Day 7 ROAS or Highest Value
- Day 0 ROAS or Highest Value | 
    vbo_window` | 
    Any of the following values:
- `SEVEN_DAYS`
- `ZERO_DAY`
For example, if you set `deep_bid_type` to `VO_MIN_ROAS`, pass in `roas_bid`, and set `vbo_window` to `ZERO_DAY`, the system will aim to keep your average ROAS of the current day around or higher than the target ROAS value.

**Note**: Day 0 or Day 7 bidding (`vbo_window` is `ZERO_DAY` or `SEVEN_DAYS`) for VBO IAA in Android campaign scenarios are currently allowlist-only features. If you would like to access them, please contact your TikTok representative. | 
   |
  
| 
    Billing Event | 
    oCPM | 
    `billing_event` | 
    `OCPM` | 
   |
  
| 
    Delivery Type | 
    Standard | 
    N/A | 
    N/A | 
   |

### Enable VBO for Smart+ iOS App Campaigns
Create a Smart+ Campaign using [/campaign/spc/create/](https://business-api.tiktok.com/portal/docs?id=1767334204047362). Note that the following requirements must be met.

  
| 
    Setting | 
    Requirement | 
    Parameter | 
    How to configure the parameter | 
   |

  
| 
    Advertising Objective | 
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
    / | 
   |
  
| 
    iOS 14 Dedicated Campaign | 
    Disabled or Enabled | 
    `campaign_type` | 
    `REGULAR_CAMPAIGN` (or not passed) or `IOS14_CAMPAIGN` | 
   |
  
| 
    Optimization Location 
(Promotion type) | 
    An **iOS** App that is eligible for VBO | 
    `promotion_type` | 
    `APP_IOS` | 
   |
  
| 
    `app_id` | 
    Specify the ID of an iOS app that is eligible for VBO.

You can get IDs of iOS Apps from [/app/list/](https://business-api.tiktok.com/portal/docs?id=1740859313270786). For iOS Apps, the returned `platform` will be `IOS`.

To check whether an App ID is eligible for VBO, pass the App ID to the parameter `app_id` in [/tool/vbo_status/](https://business-api.tiktok.com/portal/docs?id=1770016073586753). | 
   |
  
| 
    Placement | 
    Any of the following types:
- **Automatic Placement**
- **Select Placement** with TikTok placement or Pangle placement or both | 
    `placement_type`
`placements` | 
    Any of the following configurations:
- Set `placement_type` to `PLACEMENT_TYPE_AUTOMATIC`
- Set `placement_type` to `PLACEMENT_TYPE_NORMAL`, and only include `PLACEMENT_TIKTOK` or `PLACEMENT_PANGLE` or both in the value of `placements` | 
   |
  
| 
    Optimization Goal | 
    Value | 
    `optimization_goal` | 
    `VALUE` | 
   |
  
| 
    Select Value | 
    Any of the following types:
- **Purchase value** (also known as VBO IAP, which is short for VBO IAP (Value-Based Optimization for in-app purchases)
- **Ad revenue value** (also known as VBO IAA, which is short for Value-Based Optimization for in-app advertising) | 
    `optimization_event` | 
    
- If you want to use Purchase value, set `optimization_event` to `ACTIVE_PAY`.
- If you want to use Ad revenue value, set `optimization_event` to `AD_REVENUE_VALUE`. | 
   |
  
| 
    Bid Strategy | 
    Any of the following types:
- Highest Value: To spend your budget fully and maximize the value of results
- Minimum ROAS: To keep your average ROAS around or higher than the target ROAS value | 
    `deep_bid_type`
`roas_bid` | 
    Set `deep_bid_type` to `VO_MIN_ROAS` or `VO_HIGHEST_VALUE`.
**Note**: If you set `deep_bid_type` to `VO_MIN_ROAS`, pass in `roas_bid` at the same time. | 
   |
  
| 
    `bid_type | 
    BID_TYPE_NO_BID` | 
   |
  
| 
    `conversion_bid_price | 
    Not specified | 
   | 
  
| 
    Time Window of the Bid Strategy | 
    Any of the following types:
- Day 7 ROAS or Highest Value
- Day 0 ROAS or Highest Value | 
    vbo_window` | 
    Any of the following values:
- `SEVEN_DAYS`
- `ZERO_DAY`
For example, if you set `deep_bid_type` to `VO_MIN_ROAS`, pass in `roas_bid`, and set `vbo_window` to `ZERO_DAY`, the system will aim to keep your average ROAS of the current day around or higher than the target ROAS value.

**Note**:
- Day 0 or day 7 bidding (`vbo_window` is `ZERO_DAY` or `SEVEN_DAYS`) for VBO IAP in Advanced Dedicated Campaign scenarios are currently allowlist-only features. If you would like to access them, please contact your TikTok representative.
- Day 0 or day 7 bidding (`vbo_window` is `ZERO_DAY` or `SEVEN_DAYS`) for VBO IAA in Advanced Dedicated Campaign scenarios are currently allowlist-only features. If you would like to access them, please contact your TikTok representative. | 
   |
  
| 
    Billing Event | 
    oCPM | 
    `billing_event` | 
    `OCPM` | 
   |
  
| 
    Delivery Type | 
    Standard | 
    N/A | 
    N/A | 
   |

## Enable VBO for Smart+ Web Campaigns
To learn about how to enable VBO for Smart+ Web Campaigns, see [Create Smart+ Web Campaigns](https://business-api.tiktok.com/portal/docs?id=1814122471133186) and set `optimization_goal` to `VALUE`.
