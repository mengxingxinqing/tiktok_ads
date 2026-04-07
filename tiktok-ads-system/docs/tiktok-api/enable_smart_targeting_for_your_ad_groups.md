# Enable Smart Targeting for your ad groups

**Doc ID**: 1783164826830849
**Path**: Marketing API/Campaign Management/Guides/Ad group/Targeting/Audience targeting/Smart Targeting/Enable Smart Targeting for your ad groups

---

This article walks you through the steps to enable Smart Targeting for your ad groups.

# Prerequisites
- You've gained access to TikTok API for Business. See [Get Started - Step by step workflow](https://ads.tiktok.com/marketing_api/docs?id=1735713609895937) for details. 
  - To create ad groups, you need relevant permissions. See [API Reference](https://ads.tiktok.com/marketing_api/docs?id=1735713875563521) to find out permissions required for endpoints (including the endpoints listed in the "Steps" section) and see [Update app permissions](https://ads.tiktok.com/marketing_api/docs?id=1738855280338946) to find out how to configure permissions.  

# Steps
## 1. Create a campaign
Create a campaign using [/campaign/create/](https://ads.tiktok.com/marketing_api/docs?id=1739318962329602). Note that the following requirements must be met.

``` xtable
| Setting{20%} | Requirement{25%} | Parameter{25%} | How to configure the parameter{30%} |
|---|---|---|
| Advertising objective | Any of the following objectives: 
-  Traffic 
-  App promotion 
-  Lead generation 
-  Website conversions  | `objective_type` | Any of the following values: 
- `TRAFFIC`
- `APP_PROMOTION` 
- `LEAD_GENERATION`
- `WEB_CONVERSIONS`|
| App promotion type for App promotion objective | Any of the following types: 
-  App install 
-  App pre-registration  | `app_promotion_type` 
(when `objective_type` is `APP_PROMOTION`) | Any of the following values: 
- `APP_INSTALL` 
- `APP_PREREGISTRATION`  |
|Smart+ Campaign| Disabled

 If you are not sure about whether the campaign is Smart+ Campaign, you can use the `is_smart_performance_campaign` field returned from [/campaign/get/](https://business-api.tiktok.com/portal/docs?id=1739315828649986) to check. | / | / |
| Special ad categories | Disabled | `special_industries` | Not passed |
``` 

## 2. Create an ad group
Create an ad group using [/adgroup/create/](https://ads.tiktok.com/marketing_api/docs?id=1739499616346114). Note that the following requirements must be met.
``` xtable
| Setting{20%} | Requirement{25%} | Parameter{25%} | How to configure the parameter{30%} |
|---|---|---|
| Placements | **Select Placement** with only TikTok placement | 
- `placement_type`
-  `placements` | Set `placement_type` to `PLACEMENT_TYPE_NORMAL`, and set `placements` to `["PLACEMENT_TIKTOK"]` |
| Audience targeting
• Saved audience  | Disabled | `saved_audience_id` | Not passed |
| Audience targeting
• Automatic targeting | Disabled | `auto_targeting_enabled` | Not passed |
| Audience targeting
• Targeting expansion| Disabled | `targeting_expansion` | Not passed |
``` 

### Requirements for Smart audience
If you want to enable Smart audience, the following requirements must be met at the same time.
``` xtable
| Setting{25%} | Requirement{25%} | Parameter{25%} | How to configure the parameter{25%} |
|---|---|---|
| Audience targeting 
• Audience 
    ○ Include | At least one included audience is specified | `audience_ids` | Pass a valid value |
| Audience targeting 
• Audience
    ○ Smart audience  | Enabled | `smart_audience_enabled`  | `true`  |
```
### Requirements for Smart interests & behaviors
If you want to enable Smart interests & behaviors, the following requirements must be met at the same time.
``` xtable
| Setting{25%} | Requirement{25%} | Parameter{25%} | How to configure the parameter{25%} |
|---|---|---|
| Audience targeting  
• Interests & Behaviors
    ○ Interests 
    ○ Purchase intention
    ○ Video interactions & Creator interactions & Hashtag interactions   | At least one interest, purchase intention or action category is specified  | Any of the following parameters:
- `interest_category_ids`
- `interest_keyword_ids`
- `purchase_intention_keyword_ids`
- `actions`  | Pass a valid value |
| Audience targeting 
• Interests & Behaviors
    ○ Smart interests & behaviors| Enabled  | `smart_interest_behavior_enabled` | `true`  |
```
# Next steps
Create an ad using [/ad/create/](https://ads.tiktok.com/marketing_api/docs?id=1739953377508354). 

# Related docs

- [Audience targeting](https://business-api.tiktok.com/portal/docs?id=1739381236849665)
- [Smart Targeting](https://business-api.tiktok.com/portal/docs?id=1783164662979586)
- [Create an ad group](https://business-api.tiktok.com/portal/docs?id=1739499616346114)
