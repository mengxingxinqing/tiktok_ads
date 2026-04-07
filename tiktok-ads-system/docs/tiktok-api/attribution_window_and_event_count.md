# Attribution window and event count

**Doc ID**: 1777694366654465
**Path**: Marketing API/Campaign Management/Guides/Ad group/Attribution window and event count

---

At the ad group level, you have the flexibility to set different attribution windows for your campaigns or ad groups. This allows you to customize how conversions are measured based on specific timeframes.

 The supported attribution setting options at the ad group levels are as follows:    
 - Click-through attribution window (`click_attribution_window`) : This defines the timeframe within which a conversion will be measured after a person clicks your ad. You can set your window to a maximum of 28 days, capturing conversions that occur within 28 
days after the ad click.
- Engaged view-through attribution window (`engaged_view_attribution_window`): This defines the timeframe within which a conversion will be measured after a person watches at least six seconds of your video ad. You can set your window to a maximum of seven days, capturing conversions that occur within seven days after the 6-second video view.
 - View-through attribution window (`view_attribution_window`) : This defines the timeframe that a conversion will be measured after a person views your ad. You can set your 
window to a maximum of seven days, capturing conversions that occur within seven days 
after the ad view.
 - Event count (`attribution_event_count`): This refers to the way that people's actions are counted after only clicking or viewing an ad.

## Supported attribution setting options for different advertising objectives

To learn about the supported values of the fields `click_attribution_window`, `engaged_view_attribution_window`, `view_attribution_window`, and `attribution_event_count` for specific settings at the campaign level and the ad group level, refer to the following tables.

Note that for advertising objectives not listed in the tables below, you cannot manually select from a range of attribution settings. In such cases, a default setting may be applied. To confirm whether a default setting is used for your ad group when you don't manually set the attribution settings, use [/adgroup/get/](https://business-api.tiktok.com/portal/docs?id=1739314558673922) or [/campaign/spc/get/](https://business-api.tiktok.com/portal/docs?id=1767334299811842).

### App promotion

  
| 
    Advertising objective
(`objective_type`) | 
    App promotion type
(`app_promotion_type`) | 
    Optimization location | 
    Optimization goal | 
    Billing Event
(`billing_event`) | 
    Attribution window | 
    Event count
(`attribution_event_count`) | 
   |
  
| 
    Click-through attribution window
(`click_attribution_window`) | 
    View-through attribution window
(`view_attribution_window`) | 
	Engaged view-through window 
(`engaged_view_attribution_window`) | 
   |

  
| 
    App promotion
(`APP_PROMOTION`) | 
    App install
(`APP_INSTALL`) | 
    Android App
(`promotion_type` is set to `APP_ANDROID`) | 
    Self Attribution Network (SAN) App
(The value of the `self_attribution_enabled` field returned in [/app/info/](https://business-api.tiktok.com/portal/docs?id=1740859272887297) for the App (`app_id`) is `true`) | 
    Install
(`optimization_goal` is set to `INSTALL`) | 
    oCPM 
(`OCPM`) | 
    Supported values: 
- `ONE_DAY`
- `SEVEN_DAYS` | 
    Supported values: 
- `OFF`
- `ONE_DAY` | 
	Supported values: 
- `ONE_DAY`
- `SEVEN_DAYS` | 
    Supported value:
- `ONCE` | 
   |
  
| 
    Install with in-app event
 (`optimization_goal` is set to `INSTALL`, and `secondary_optimization_event` is specified) | 
   |
  
| 
    In-app event, with the optimization event as purchase
 (`optimization_goal` is set to `IN_APP_EVENT`, and `optimization_event` is set to `ACTIVE_PAY`) | 
    Supported value:
- `ONCE`
- `EVERY` | 
   |
  
| 
    In-app event, with the optimization event not as purchase
 (`optimization_goal` is set to `IN_APP_EVENT`, and `optimization_event` is set to a value other than `ACTIVE_PAY`) | 
    Supported value:
- `ONCE` | 
   |
  
| 
    Value
(`optimization_goal` is set to `VALUE`) | 
    Supported value:
- `EVERY` | 
   |
  
| 
    Non-SAN App
(The value of the `self_attribution_enabled` field returned in [/app/info/](https://business-api.tiktok.com/portal/docs?id=1740859272887297) for the App (`app_id`) is `false`) | 
    In-app event, with the optimization event as purchase
 (`optimization_goal` is set to `IN_APP_EVENT`, and `optimization_event` is set to `ACTIVE_PAY`) | 
    oCPM
 (`OCPM`) | 
    Supported value: 
- `SEVEN_DAYS` | 
    Supported value: 
- `ONE_DAY` | 
	Supported value: 
- `SEVEN_DAYS` | 
    Supported value:
- `ONCE`
- `EVERY` | 
   |
  
| 
    iOS App in a Non-Dedicated Campaign
(`promotion_type` is set to `APP_IOS` and the `campaign_type` of the campaign is `REGULAR_CAMPAIGN`) | 
    SAN App
(The value of the `self_attribution_enabled` field returned in [/app/info/](https://business-api.tiktok.com/portal/docs?id=1740859272887297) for the App (`app_id`) is `true`) | 
    Install
(`optimization_goal` is set to `INSTALL`) | 
    oCPM
 (`OCPM`) | 
    Supported values: 
- `ONE_DAY`
- `SEVEN_DAYS` | 
    Supported values: 
- `OFF`
- `ONE_DAY` | 
	Supported values: 
- `ONE_DAY`
- `SEVEN_DAYS` | 
    Supported value:
- `ONCE` | 
   |
  
| 
    Install with in-app event 
 (`optimization_goal` is set to `INSTALL`, and `secondary_optimization_event` is specified) | 
    Supported value:
- `ONCE` | 
   |
  
| 
    In-app event 
 (`optimization_goal` is set to `IN_APP_EVENT`) | 
    Supported value:
- `ONCE` | 
   |
  
| 
    Value
(`optimization_goal` is set to `VALUE`) | 
    Supported value:
- `EVERY` | 
   |
  
| 
    App retargeting
(`APP_RETARGETING`) | 
    Android App
(`promotion_type` is set to `APP_ANDROID`) | 
    SAN App
(The value of the `self_attribution_enabled` field returned in [/app/info/](https://business-api.tiktok.com/portal/docs?id=1740859272887297) for the App (`app_id`) is `true`) | 
    In-app event, with the optimization event as purchase
 (`optimization_goal` is set to `IN_APP_EVENT`, and `optimization_event` is set to `ACTIVE_PAY`) | 
    oCPM
 (`OCPM`) | 
    Supported values:
- `ONE_DAY`
- `SEVEN_DAYS` | 
    Supported values: 
- `OFF`
- `ONE_DAY` | 
	Supported values:
- `ONE_DAY`
- `SEVEN_DAYS` | 
    Supported value:
- `ONCE`
- `EVERY` | 
   |
  
| 
    In-app event, with the optimization event not as purchase 
 (`optimization_goal` is set to `IN_APP_EVENT`, and `optimization_event` is set to a value other than `ACTIVE_PAY`) | 
    Supported value:
- `ONCE` | 
   |
  
| 
    Value
(`optimization_goal` is set to `VALUE`) | 
    Supported value:
- `EVERY` | 
   |
  
| 
    Non-SAN App
(The value of the `self_attribution_enabled` field returned in [/app/info/](https://business-api.tiktok.com/portal/docs?id=1740859272887297) for the App (`app_id`) is `false`) | 
    In-app event, with the optimization event as purchase
 (`optimization_goal` is set to `IN_APP_EVENT`, and `optimization_event` is set to `ACTIVE_PAY`) | 
    oCPM
 (`OCPM`) | 
    Supported value: 
- `SEVEN_DAYS` | 
    Supported value: 
- `ONE_DAY` | 
    Supported value: 
- `SEVEN_DAYS` | 
    Supported value:
- `ONCE`
- `EVERY` | 
   |
  
| 
    iOS App
(`promotion_type` is set to `APP_IOS`) | 
    SAN App
(The value of the `self_attribution_enabled` field returned in [/app/info/](https://business-api.tiktok.com/portal/docs?id=1740859272887297) for the App (`app_id`) is `true`) | 
    In-app event 
 (`optimization_goal` is set to `IN_APP_EVENT`) | 
    oCPM 
(`OCPM`) | 
    Supported values: 
- `ONE_DAY`
- `SEVEN_DAYS` | 
    Supported values: 
- `OFF`
- `ONE_DAY` | 
	Supported values: 
- `ONE_DAY`
- `SEVEN_DAYS` | 
    Supported values:
- `ONCE` | 
   |
  
| 
    Value
(`optimization_goal` is set to `VALUE`) | 
    Supported value:
- `EVERY` | 
   |
  
| 
    App pre-registration
 (`APP_PREREGISTRATION`) | 
    Website 
(`promotion_type` is set to `WEBSITE`)
 | 
    Conversion
 (`optimization_goal` is set to `CONVERT`)
 | 
    oCPM
 (`OCPM`) | 
    Supported values: 
- `ONE_DAY`
- `SEVEN_DAYS`
- `FOURTEEN_DAYS`
- `TWENTY_EIGHT_DAYS` | 
    Supported values: 
- `OFF`
- `ONE_DAY`
- `SEVEN_DAYS` | 
    / | 
    Supported values:
- `ONCE`
- `EVERY` | 
   |

  
  
  
### Lead generation

  
| 
    Advertising objective
(`objective_type`) | 
    Optimization location | 
    Optimization goal 
(`optimization_goal`) | 
    Billing Event
(`billing_event`) | 
    Attribution window | 
    Event count
(`attribution_event_count`) | 
   |
  
| 
    Click-through attribution window
(`click_attribution_window`) | 
    View-through attribution window
(`view_attribution_window`) | 
   |

  
| 
    Lead generation (`LEAD_GENERATION`) | 
    Website 
(`promotion_type` is set to `LEAD_GENERATION` , and `promotion_target_type` is set to `EXTERNAL_WEBSITE`) | 
    Conversion
(`CONVERT`) | 
    oCPM
 (`OCPM`) | 
    Supported values: 
- `ONE_DAY`
- `SEVEN_DAYS`
- `FOURTEEN_DAYS`
- `TWENTY_EIGHT_DAYS` | 
    Supported Values: 
- `OFF`
- `ONE_DAY`
- `SEVEN_DAYS` | 
    Supported values:
- `ONCE`
- `EVERY` | 
   |

### Product Sales
  
  

  
| 
    Advertising objective 
(`objective_type`) | 
    Campaign product source 
(`campaign_product_source`) | 
    Optimization location | 
    Optimization goal | 
    Billing Event 
(`billing_event`) | 
    Attribution window | 
    Event count 
(`attribution_event_count`) | 
   |
  
| 
    Click-through attribution window 
(`click_attribution_window`) | 
    View-through attribution window 
(`view_attribution_window`) | 
	Engaged view-through window 
(`engaged_view_attribution_window`) | 
   |

  
| 
    Product sales 
(`PRODUCT_SALES`) | 
    Catalog 
(`CATALOG`) | 
    Website 
(`promotion_type` is set to `WEBSITE`) | 
    Conversion 
(`optimization_goal` is set to `CONVERT`) | 
    oCPM 
(`OCPM`) | 
    Supported values:
- `ONE_DAY`
- `SEVEN_DAYS`
- `FOURTEEN_DAYS`
- `TWENTY_EIGHT_DAYS` | 
    Supported Values:
- `OFF`
- `ONE_DAY`
- `SEVEN_DAYS` | 
    / | 
    Supported values:
- `ONCE`
- `EVERY` | 
   |
  
| 
    Value 
(`optimization_goal` is set to `VALUE`) | 
    Supported value:
- `EVERY` | 
   |
  
| 
    Android App, with retargeting disabled 
(`promotion_type` is set to `APP_ANDROID`, and `shopping_ads_retargeting_type` is set to `OFF` or not passed) | 
    SAN App 
(The value of the `self_attribution_enabled` field returned in [/app/info/](https://business-api.tiktok.com/portal/docs?id=1740859272887297) for the App (`app_id`) is `true`) | 
    Install 
(`optimization_goal` is set to `INSTALL`) | 
    oCPM 
(`OCPM`) | 
    Supported values:
- `ONE_DAY`
- `SEVEN_DAYS` | 
    Supported Values:
- `OFF`
- `ONE_DAY` | 
    Supported values:
- `ONE_DAY`
- `SEVEN_DAYS` | 
    Supported value:
- `ONCE` | 
   |
  
| 
    In-app event, with the optimization event as purchase 
(`optimization_goal` is set to `IN_APP_EVENT`, and `optimization_event` is set to `ACTIVE_PAY`) | 
    Supported value:
- `ONCE`
- `EVERY` | 
   |
  
| 
    In-app event, with the optimization event not as purchase 
(`optimization_goal` is set to `IN_APP_EVENT`, and `optimization_event` is set to a value other than `ACTIVE_PAY`) | 
    Supported value:
- `ONCE` | 
   |
  
| 
    Value 
(`optimization_goal` is set to `VALUE`) | 
    Supported value:
- `EVERY` | 
   |
  
| 
    Non-SAN App 
(The value of the `self_attribution_enabled` field returned in [/app/info/](https://business-api.tiktok.com/portal/docs?id=1740859272887297) for the App (`app_id`) is `false`) | 
    In-app event, with the optimization event as purchase 
(`optimization_goal` is set to `IN_APP_EVENT`, and `optimization_event` is set to `ACTIVE_PAY`) | 
    oCPM 
(`OCPM`)
 | 
    Supported value:
- `SEVEN_DAYS` | 
    Supported value:
- `ONE_DAY` | 
    Supported value:
- `SEVEN_DAYS` | 
    Supported values:
- `ONCE`
- `EVERY` | 
   |
  
| 
    Android App, with retargeting enabled 
(`promotion_type` is set to `APP_ANDROID`, and `shopping_ads_retargeting_type` is set to `LAB1`, `LAB2`, or `LAB3`) | 
    SAN App 
(The value of the `self_attribution_enabled` field returned in [/app/info/](https://business-api.tiktok.com/portal/docs?id=1740859272887297) for the App (`app_id`) is `true`)
 | 
    In-app event, with the optimization event as purchase 
(`optimization_goal` is set to `IN_APP_EVENT`, and `optimization_event` is set to `ACTIVE_PAY`) | 
    oCPM 
(`OCPM`)
 | 
    Supported values:
- `ONE_DAY`
- `SEVEN_DAYS` | 
    Supported values:
- `OFF`
- `ONE_DAY` | 
    Supported values:
- `ONE_DAY`
- `SEVEN_DAYS` | 
    Supported values:
- `ONCE`
- `EVERY` | 
   |
  
| 
    In-app event, with the optimization event not as purchase 
(`optimization_goal` is set to `IN_APP_EVENT`, and `optimization_event` is set to a value other than `ACTIVE_PAY`) | 
    Supported value:
- `ONCE` | 
   |
  
| 
    Value 
(`optimization_goal` is set to `VALUE`) | 
    Supported value:
- `EVERY` | 
   |
  
| 
    Non-SAN App 
(The value of the `self_attribution_enabled` field returned in [/app/info/](https://business-api.tiktok.com/portal/docs?id=1740859272887297) for the App (`app_id`) is `false`) | 
    In-app event, with the optimization event as purchase 
(`optimization_goal` is set to `IN_APP_EVENT`, and `optimization_event` is set to `ACTIVE_PAY`) | 
    oCPM 
(`OCPM`) | 
    Supported value:
- `SEVEN_DAYS` | 
    Supported value:
- `ONE_DAY` | 
    Supported value:
- `SEVEN_DAYS` | 
    Supported values:
- `ONCE`
- `EVERY` | 
   |
  
| 
    iOS App in a Non-Dedicated Campaign, with retargeting disabled 
(`promotion_type` is set to `APP_IOS`, the `campaign_type` of the campaign is `REGULAR_CAMPAIGN`, and `shopping_ads_retargeting_type` is set to `OFF` or not passed) | 
    SAN App 
(The value of the `self_attribution_enabled` field returned in [/app/info/](https://business-api.tiktok.com/portal/docs?id=1740859272887297) for the App (`app_id`) is `true`) | 
    Install 
(`optimization_goal` is set to `INSTALL`) | 
    oCPM 
(`OCPM`) | 
    Supported values:
- `ONE_DAY`
- `SEVEN_DAYS` | 
    Supported values:
- `OFF`
- `ONE_DAY` | 
    Supported values:
- `ONE_DAY`
- `SEVEN_DAYS` | 
    Supported value:
- `ONCE` | 
   |
  
| 
    Install with in-app event 
(`optimization_goal` is set to `INSTALL`, and `secondary_optimization_event` is specified) | 
    Supported value:
- `ONCE` | 
   |
  
| 
    In-app event 
(`optimization_goal` is set to `IN_APP_EVENT`) | 
    Supported value:
- `ONCE` | 
   |
  
| 
    Value 
(`optimization_goal` is set to `VALUE`) | 
    Supported value:
- `EVERY` | 
   |
  
| 
    iOS App, with retargeting enabled 
(`promotion_type` is set to `APP_IOS`, and `shopping_ads_retargeting_type` is set to `LAB1`, `LAB2`, or `LAB3`) | 
    SAN App 
(The value of the `self_attribution_enabled` field returned in [/app/info/](https://business-api.tiktok.com/portal/docs?id=1740859272887297) for the App (`app_id`) is `true`) | 
    In-app event 
(`optimization_goal` is set to `IN_APP_EVENT`) | 
    oCPM 
(`OCPM`) | 
    Supported values:
- `ONE_DAY`
- `SEVEN_DAYS` | 
    Supported values:
- `OFF`
- `ONE_DAY` | 
    Supported values:
- `ONE_DAY`
- `SEVEN_DAYS` | 
    Supported value:
- `ONCE` | 
   |
  
| 
    Value 
(`optimization_goal` is set to `VALUE`) | 
    Supported value:
- `EVERY` | 
   |
  
| 
    TikTok Shop 
(`STORE`) | 
    Video Shopping Ad 
(`promotion_type` is set to `VIDEO_SHOPPING`, and `shopping_ads_type` is set to `VIDEO`) | 
    TikTok Shop 
(`store_id` is set to a TikTok Shop ID) | 
    Conversion 
(`optimization_goal` is set to `CONVERT`) | 
    oCPM 
(`OCPM`) | 
    Supported values:
- `ONE_DAY`
- `SEVEN_DAYS`
- `FOURTEEN_DAYS`
- `TWENTY_EIGHT_DAYS` | 
    Supported Values:
- `OFF`
- `ONE_DAY`
- `SEVEN_DAYS` | 
    / | 
    Supported value:
- `ONCE` | 
   |
  
| 
    Value 
(`optimization_goal` is set to `VALUE`) | 
   |
  
| 
    Live Shopping Ad 
(`promotion_type` is set to `LIVE_SHOPPING`, and `shopping_ads_type` is set to `LIVE`) | 
    TikTok Shop 
(`store_id` is set to a TikTok Shop ID) | 
    Conversion 
(`optimization_goal` is set to `CONVERT`) | 
    oCPM 
(`OCPM`) | 
    Supported values:
- `ONE_DAY`
- `SEVEN_DAYS`
- `FOURTEEN_DAYS`
- `TWENTY_EIGHT_DAYS` | 
    Supported Values:
- `OFF`
- `ONE_DAY`
- `SEVEN_DAYS` | 
    /
 | 
    Supported value:
- `ONCE` | 
   |
  
| 
    Value 
(`optimization_goal` is set to `VALUE`) | 
   |

### Website conversions

    
| 
    Advertising objective
(`objective_type`) | 
    Optimization location | 
    Optimization goal 
(`optimization_goal`) | 
    Billing Event
(`billing_event`) | 
    Attribution window | 
    Event count
(`attribution_event_count`) | 
   |
  
| 
    Click-through attribution window
(`click_attribution_window`) | 
    View-through attribution window
(`view_attribution_window`) | 
   |

  
| 
    Website conversions
(`WEB_CONVERSIONS`) | 
    Website
(`promotion_type` is set to `WEBSITE`, and`promotion_website_type` is set to `UNSET` or not passed) | 
    Conversion
(`CONVERT`) | 
    oCPM 
(`OCPM`) | 
    Supported values:
- `ONE_DAY`
- `SEVEN_DAYS`
- `FOURTEEN_DAYS`
- `TWENTY_EIGHT_DAYS` | 
    Supported Values: 
- `OFF`
- `ONE_DAY`
- `SEVEN_DAYS` | 
    Supported values:
- `ONCE`
- `EVERY` | 
   |
  
| 
    Value 
 (`VALUE`) | 
    Supported value:
- `EVERY` | 
   |
