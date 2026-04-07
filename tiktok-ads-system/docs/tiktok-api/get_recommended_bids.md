# Get recommended bids

**Doc ID**: 1746463347473410
**Path**: Marketing API/Campaign Management/Guides/Ad group/Estimated Delivery Results/Get recommended bids

---

Bid EDR (Estimated Delivery Results) enables you to adopt the suitable bid from estimated results to scale up your ad group and increase budget consumption rate. The estimated results, which are for ad group performance on the same day, include 9 sets of data for recommended bid raise ratios from -10% to 30% with a step of 5% and corresponding estimated cost uplift data.
 
 
## Prerequisites
Please ensure that the below preconditions are met before you call [/tool/diagnosis/get/](https://business-api.tiktok.com/portal/docs?id=1738674986981378) to obtain the bid estimated delivery results:
 
### At the campaign level

``` xtable
| Setting{20%} | Requirement{30%}| Parameter{20%}| How to configure the parameter {30%}      |
|---|---|---|---|
| Advertising objective | One of the following objectives: 
- App promotion
- Web conversions
- Lead generation | `objective_type`	| Any value below: 
- `APP_PROMOTION`
- `WEB_CONVERSIONS`
- `LEAD_GENERATION` |
| Campaign Budget Optimization (CBO) | Disabled | `budget_optimize_on` | `false` |
```
 
### At the ad group level
  
``` xtable
| Setting{20%} | Requirement{25%}| Parameter{20%}| How to configure the parameter {35%}      |
|---|---|---|---|
| Placement |
- **Automatic Placement** or 
- **Select Placement **with TikTok placement included
 | `placement_type` & `placements` | 
-  Set `placement_type` as `PLACEMENT_TYPE_AUTOMATIC`, or 
-  Set `placement_type` as `PLACEMENT_TYPE_NORMAL`, and include `PLACEMENT_TIKTOK` in the value of `placements` |
| Live ads | Disabled | `promotion_type` | **Not** `LIVE_SHOPPING` |
| Budget type | Daily budget | `budget_mode` | `BUDGET_MODE_DAY` |
| Optimization goal | One of the following goals: 
-  Click 
-  Install 
- Leads
- Conversions
- Conversations | `optimization_goal` | Any value below: 
- `CLICK`
- `INSTALL`
- `LEAD_GENERATION`
- `CONVERT`
- `CONVERSATION`   |
| Bidding strategy | Cost Cap | `bid_type` | `BID_TYPE_CUSTOM` |
| Billing Event | `OCPX` type | `billing_event` | `OCPC` or `OCPM` |
| App Event Optimization & Value-based Optimization | Both disabled | `deep_bid_type` | `DEFAULT` |
| Scheduled budget | Disabled | `scheduled_budget` | Not set via [/adgroup/budget/update/](https://ads.tiktok.com/marketing_api/docs?id=1739591133130817) |
| Other | 
- No bid adjustment for the ad group on the day you want to get results from [/delivery/bid/recommend/](https://ads.tiktok.com/marketing_api/docs?id=1746463732779009).
-  At least **five** conversions for the last day.
-  Not a reservation ad group. | / | / |
```

## Steps
Follow the following steps to use the Bid EDR feature： 
1. **Create a campaign** using [/campaign/create/](https://ads.tiktok.com/marketing_api/docs?id=1739318962329602).
2. **Create an ad group** using [/adgroup/create/](https://ads.tiktok.com/marketing_api/docs?id=1739499616346114). 
3. **Create an ad** using [/ad/create/](https://ads.tiktok.com/marketing_api/docs?id=1739953377508354).
4. **Filter out ad groups that meet the conversion requirement** by running a report. The ad group should have at least **five** conversions for the last day. 
We recommend that you run a [Basic Report](https://ads.tiktok.com/marketing_api/docs?id=1738864915188737), [Audience report](https://ads.tiktok.com/marketing_api/docs?id=1738864928947201), [Playable ad reports](https://ads.tiktok.com/marketing_api/docs?id=1738864940608513), or [DSA report](https://ads.tiktok.com/marketing_api/docs?id=1738864960144385), because these report types return conversion data.
5. **Get bid recommendations** using [/tool/diagnosis/get/](https://business-api.tiktok.com/portal/docs?id=1738674986981378). You need to select IDs of qualified ad groups from filtered-out ad groups in step 4, and pass the IDs to `adgroup_ids` in the request. The bid estimated delivery results are available through the returned `bid_edr_info`.
6. **Update bid within the same day** (advertiser account time zone) using [/adgroup/update/](https://ads.tiktok.com/marketing_api/docs?id=1739586761631745) and pass the adopted bid price to `conversion_bid_price` or `bid_price`.
