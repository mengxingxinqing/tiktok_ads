# Budget

**Doc ID**: 1739381246298114
**Path**: Marketing API/Campaign Management/Guides/Campaign/Budget

---

To give more control over your advertising cost, TikTok For Business supports budget settings at both campaign and ad group level.

For effectiveness, TikTok for Business limits the minimum amount for lifetime and daily budgets. 
* **Campaign level minimum budget**
	- For campaigns, with the exception of those with `objective_type` as `PRODUCT_SALES` and` campaign_product_source` as `STORE`, both daily budgets and lifetime budgets must exceed 50 USD.
	- For campaigns with `objective_type` as `PRODUCT_SALES` and` campaign_product_source` as `STORE`, both daily budgets and lifetime budgets must exceed 10 USD.
* **Ad group level minimum budget**
	- For ad groups, with the exception of those with `product_source` as `STORE` or `SHOWCASE`, daily budgets must exceed 20 USD. Lifetime budgets will be calculated as the minimum daily budget (20 USD) × scheduled days.
	- For ad groups with `product_source` as `STORE` or `SHOWCASE`, daily budgets must exceed 10 USD. Lifetime budgets will be calculated as the minimum daily budget (10 USD) × scheduled days.

For detailed information, please refer to [About Budget](https://ads.tiktok.com/help/article/budget?redirected=1).

## Budget modes at different levels

  
| 
    Ad Level | 
    Campaign Budget Optimization (CBO) | 
    Buget Mode
 | 
   |

  
| 
    Campaign
 | 
    Enabled
 | 
    When CBO is enabled, `budget_mode` at the campaign level supports the following enum values:
- `BUDGET_MODE_TOTAL`: Lifetime budget.
- `BUDGET_MODE_DYNAMIC_DAILY_BUDGET`: Dynamic daily budget. It is the average daily budget over a week. Daily costs will not exceed 125% of the average daily budget. Weekly costs will not exceed the average daily budget * 7.When `objective_type` is `TRAFFIC`, `APP_PROMOTION`, `WEB_CONVERSIONS`, `LEAD_GENERATION`, `PRODUCT_SALES` (Video Shopping Ads only), `REACH`, `VIDEO_VIEWS`, or `ENGAGEMENT`, and you want to set a non-lifetime budget, set this field to `BUDGET_MODE_DYNAMIC_DAILY_BUDGET`.

**Note**: `BUDGET_MODE_DYNAMIC_DAILY_BUDGET` for campaign objectives `REACH`, `VIDEO_VIEWS`, and `ENGAGEMENT` is currently an allowlist-only feature. If you would like to access it, please contact your TikTok representative.
- `BUDGET_MODE_DAY`: Daily budget. | 
   |
  
| 
    Disabled
 | 
    When CBO is disabled, `budget_mode` at the campaign level supports the following enum values:
- `BUDGET_MODE_INFINITE`: Unlimited budget.`BUDGET_MODE_TOTAL`: Lifetime budget.`BUDGET_MODE_DAY`: Daily budget. | 
   |
  
| 
    Ad Group
 | 
    Enabled
 | 
    When CBO is enabled, `budget_mode` at the ad group level will be ignored.
 | 
   |
  
| 
    Disabled
 | 
    When CBO is disabled, `budget_mode` at the ad group level supports the following enum values:`BUDGET_MODE_TOTAL`: Lifetime budget.
- `BUDGET_MODE_DYNAMIC_DAILY_BUDGET`: Dynamic daily budget. It is the average daily budget over a week. Daily costs will not exceed 125% of the average daily budget. Weekly costs will not exceed the average daily budget * 7.When `objective_type` is `TRAFFIC`, `APP_PROMOTION`, `WEB_CONVERSIONS`, `LEAD_GENERATION`, `PRODUCT_SALES` (Video Shopping Ads only), `REACH`, `VIDEO_VIEWS`, or `ENGAGEMENT`, and you want to set a non-lifetime budget, set this field to `BUDGET_MODE_DYNAMIC_DAILY_BUDGET`.
**Note**: `BUDGET_MODE_DYNAMIC_DAILY_BUDGET` for campaign objectives `REACH`, `VIDEO_VIEWS`, and `ENGAGEMENT` is currently an allowlist-only feature. If you would like to access it, please contact your TikTok representative.
- `BUDGET_MODE_DAY`: Daily budget. | 
   |

## Budget setting guidelines
Allowed advertising budget is related to the currency of your advertiser account. Note that the verification of the budget you specify is threefold:
- Currency precision. Different currencies may vary in the maximum decimal places you can specify. For instance, for US Dollar (USD) you can keep two decimal places at most, but for Japanese Yen (JPY) you can only specify integers. 
- Budget value range. The value range of the daily advertising budget for each currency is calculated as **base daily budget value range** * **Budget Verification Ratio for the currency**. 
	- For campaigns, with the exception of those with `objective_type` as `PRODUCT_SALES` and `campaign_product_source` as `STORE` , the base daily budget value range is \[50, 10 000 000). For campaigns with `objective_type` as `PRODUCT_SALES` and `campaign_product_source` as `STORE`, the base daily budget value range is \[10, 10 000 000).    
	- For ad groups, with the exception of those with `product_source` as `STORE` or `SHOWCASE`, the base daily budget value range is \[20,10 000 000). For ad groups with `product_source` as `STORE` or `SHOWCASE`, the base daily budget value range is \[10, 10 000 000). 
	- For example, if the currency of your advertiser account is JPY (the corresponding Budget Verification Ratio is 100) and the ad group is not with the `product_source` as `STORE` or `SHOWCASE`, the allowed daily budget value range at the ad group level is \[2 000,1 000 000 000).
- If you are updating the budget at the ad group level or campaign level, the new budget should be at least 105% of the current spend. You can run [a synchronous report](https://ads.tiktok.com/marketing_api/docs?id=1740302848100353) or [an asynchronous report]( https://ads.tiktok.com/marketing_api/docs?id=1740302766489602) to get the spend data via the Basic data metric `spend`. 
 
>**Note**

>You can see the precision and Budget Verification Ratio of each currency in [Currency-Budget verification ratio and precision of each currency](https://ads.tiktok.com/marketing_api/docs?id=1737585839634433). **OR** you can see the maximum and minimum daily budget for each currency directly in [Currency-Daily budget value range](https://ads.tiktok.com/marketing_api/docs?id=1737585839634433).

If the ad group is created from the TikTok Ads Manager in **Simplified Mode**, the base minimum daily budget value at the ad group level may not be 20:
-  For advertising goal Traffic, the base minimum daily budget is 5.
-  For advertising goal Community interaction, Lead generation, or Conversions, the base minimum daily budget is 10.
-  For other advertising goals, the base minimum daily budget is 20.

##  Budget mode combinations

`budget_mode` at the ad group level can only be set as daily budget in either of these scenarios:

1. For ad groups with delivery mode (`schedule_type`) specified as continuous delivery (`SCHEDULE_FROM_NOW`), `budget_mode` should be either `BUDGET_MODE_DAY` or `BUDGET_MODE_DYNAMIC_DAILY_BUDGET`.
2. When the `budget_mode` for the corresponding campaign is daily budget (`BUDGET_MODE_DAY`), then ad group `budget_mode` must be `BUDGET_MODE_DAY` as well.

See the table below for the allowed combinations of budget modes at campaign and ad group levels.

|  |Ad Group Lifetime Budget
`BUDGET_MODE_TOTAL` |Ad Group Daily Budget 

`BUDGET_MODE_DAY`|Ad Group Dynamic Daily Budget

`BUDGET_MODE_DYNAMIC_DAILY_BUDGET`
| --- | --- | --- | --- |
|Campaign Unlimited Budget 

`BUDGET_MODE_INFINITE`  | ☑️ |  ☑️ | ☑️|
|Campaign Lifetime Budget  

`BUDGET_MODE_TOTAL` |  ☑️ | ☑️  | ☑️|
|Campaign Daily Budget 

`BUDGET_MODE_DAY` |  ❎ |  ☑️ | ☑️|
|Campaign Dynamic Daily Budget 

`BUDGET_MODE_DYNAMIC_DAILY_BUDGET` |  The setting will be ignored as CBO is enabled. |  The setting will be ignored as CBO is enabled.   |  The setting will be ignored as CBO is enabled.  |

## Related links

* [Budget Best Practices](https://ads.tiktok.com/help/article?aid=744163857974606118)
