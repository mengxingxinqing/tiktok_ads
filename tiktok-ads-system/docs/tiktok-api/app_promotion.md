# App promotion

**Doc ID**: 1747553433902082
**Path**: Marketing API/Campaign Management/Guides/Campaign/Advertising objective/App promotion

---

With the App promotion objective, you can find users to install your mobile app and re-engage your app's users. See [About the New App Promotion Advertising Objective](https://ads.tiktok.com/help/article?aid=10012707) for more details.  
>**Note**
The App promotion objective is only available in TikTok API for Business v1.3. 

Currently, App promotion supports the following three app promotion types: 
- App install (`APP_INSTALL`): Get new users to install and take action in your app. 
**It is identical to the existing App installs objective**.
- App retargeting (`APP_RETARGETING`): Re-engage existing users to take action on your app. 
**The App retargeting campaign type replaces the functionality of an App conversion campaign**. 
>**Note**
App retargeting is not supported in iOS14 Dedicated Campaigns. 
- App Pre-Registration (`APP_PREREGISTRATION`): Get new users to pre-register before your app launches. To learn about how to create App Pre-Registration ads, refer to [Create App Pre-Registration ads](https://ads.tiktok.com/marketing_api/docs?id=1772549012687873).
> **Note**

> 
- App Pre-Registration is currently an allowlist-only feature. If you would like to access it, please contact your TikTok representative.
- App Pre-Registration is not supported in iOS14 Dedicated Campaigns.

## Create App promotion ads
1. Use [/campaign/create/](https://ads.tiktok.com/marketing_api/docs?id=1739318962329602) to create a campaign. 

Note that the following requirements must be met.

  
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
    One of the following types: 
-  App install 
-  App retargeting 
-  App pre-registration  | 
    `app_promotion_type` | 
    Any value below: 
- `APP_INSTALL`
- `APP_RETARGETING` 
- `APP_PREREGISTRATION` | 
   |
  
| 
    iOS 14 Dedicated Campaign | 
    
-  Supported only when App promotion type is App install.
-  Not supported when App promotion type is App retargeting or App pre-registration. | 
    `campaign_type` | 
    
-  Can be set to `IOS14_CAMPAIGN` only when `app_promotion_type` is `APP_INSTALL`.
-  Cannot be set to `IOS14_CAMPAIGN` when `app_promotion_type` = `APP_RETARGETING` or `APP_PREREGISTRATION`.  | 
   |
  
| 
    `app_id` | 
    
-  Supported only when `app_promotion_type` is `APP_INSTALL`. 
-  Not supported when `app_promotion_type` = `APP_RETARGETING` or `APP_PREREGISTRATION`. | 
   |
  
| 
    `campaign_app_profile_page_state` | 
    
-  Supported only when `app_promotion_type` is `APP_INSTALL`. This field can be used to determine whether to use App Profile Page to optimize delivery. Default value is `OFF`.
-  Not supported when `app_promotion_type` = `APP_RETARGETING` or `APP_PREREGISTRATION`.  | 
   |
  
| 
    Smart+ Campaign | 
    
-  Supported only for App Install campaigns (`app_promotion_type` =`APP_INSTALL`) 
-  Not supported for App retargeting campaigns or App Pre-Registration campaign (`app_promotion_type` = `APP_RETARGETING` or `APP_PREREGISTRATION`). If you are not sure about whether the campaign is Smart+ Campaign, you can use the `is_smart_performance_campaign` field returned from [/campaign/get/](https://ads.tiktok.com/marketing_api/docs?id=1739315828649986) to check. | 
    / | 
    / | 
   |

2. Use [/adgroup/create/](https://ads.tiktok.com/marketing_api/docs?id=1739499616346114) to create an ad group. 
   
If your campaign is an iOS14 Dedicated Campaign, note that: 
  -    In the `ios14_targeting` field, you need to either specify a consistent iOS14 value (i.e. what you enter in the `campaign_type` field at the campaign level) , or choose not to pass in any value and we will automatically set them. 
For example, if `campaign_type` is `IOS14_CAMPAIGN`, you should either specify `ios14_targeting` as `IOS14_PLUS` or pass in no value. 
  - In the `app_id` field, you need to specify the same ID as you entered in `app_id` at the campaign level , or choose not to pass in any value and we will automatically set it.  
  - In the `adgroup_app_profile_page_state` field, you need to specify the same value as you entered in the `campaign_app_profile_page_state` at the campaign level, or choose not to pass in any value and we will automatically set it. 

If you want to create an App Pre-Registration ad group, refer to [Create App Pre-Registration ads](https://ads.tiktok.com/marketing_api/docs?id=1772549012687873).

3. Use [/ad/create/](https://ads.tiktok.com/marketing_api/docs?id=1739953377508354) to create an ad. 

If you want to create an App Pre-registration ad, refer to [Create App Pre-Registration ads](https://ads.tiktok.com/marketing_api/docs?id=1772549012687873).

## Related use cases
[Create App Pre-Registration ads](https://business-api.tiktok.com/portal/docs?id=1772549012687873)
