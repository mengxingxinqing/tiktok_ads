# Create a GMV Max Campaign

**Doc ID**: 1822000988713089
**Path**: API Reference/GMV Max/Create a GMV Max Campaign

---

Use this endpoint to create a GMV Max Campaign.

## Request

**Endpoint** https://business-api.tiktok.com/open_api/v1.3/campaign/gmv_max/create/

**Method** POST

**Header**

```xtable
|Field{35%}|Data Type{15%}|Description{50%}|
|---|---|---|
|Access-Token {Required}|string|Authorized access token.
 For details, see [Authentication](https://business-api.tiktok.com/portal/docs?id=1738373164380162).|
|Content-Type {Required}|string|Request message type.
Allowed format: `application/json`.  |
```

**Parameters**

``` xtable
|Field{35%}|Data Type{15%}|Description{50%}|
|--- |--- |--- |
| request_id {Required} | string | Request ID that supports idempotency to prevent you from sending the same request twice. 
If you retry requests with the same request ID multiple times within the 10-second cache time, then only one request will succeed. If a duplicate request with the expired request ID is received after the cache time, the server will treat it as a new request and process it accordingly. 

The ID is different from the `request_id` returned in the response parameters, which is used to uniquely identify an HTTP request.

 The value should be a string representation of a 64-bit integer. 

Example: `"123456789"`. |
| store_id {Required} | string | The ID of the TikTok Shop.

 To obtain a TikTok Shop that is available for GMV Max Campaigns, use [/gmv_max/store/list/](https://business-api.tiktok.com/portal/docs?id=1822001044479041) and confirm that the returned `is_gmv_max_available` is `true`. |
| store_authorized_bc_id {Required} | string | ID of the Business Center that is authorized to access the TikTok Shop (`store_id`). |
| advertiser_id {Required} | string | Advertiser ID. 

To ensure that the ad account has exclusive GMV Max authorization for the TikTok Shop that you want to promote, call [/gmv_max/store/list/](https://business-api.tiktok.com/portal/docs?id=1822001044479041) and confirm that the returned `advertiser_id` within `exclusive_authorized_advertiser_info` is the same as the ad account that you want to use to create GMV Max Campaigns.
- If the returned `advertiser_id` is not the same as the ad account that you want to use to create GMV Max Campaigns, use [/gmv_max/exclusive_authorization/create/](https://business-api.tiktok.com/portal/docs?id=1822001200356354) to grant the ad account exclusive GMV Max authorization for the TikTok Shop.|
| shopping_ads_type {Required} | string | The type of the GMV Max Campaign.

Enum values:
- `PRODUCT`: Product GMV Max Campaign.
- `LIVE`: Live GMV Max Campaign.  
 To learn about how to create such campaigns, see [Create Product GMV Max Campaigns](https://business-api.tiktok.com/portal/docs?id=1822009220448257) and [Create LIVE GMV Max Campaigns](https://business-api.tiktok.com/portal/docs?id=1822009242546258). |
| product_specific_type | string | Valid only when `shopping_ads_type` is `PRODUCT`.

Different dimensions to choose products. 

Enum values:
- `ALL`: Allow TikTok to dynamically choose from all products within the TikTok Shop.
- `CUSTOMIZED_PRODUCTS`: Specify a customized number of products within the TikTok Shop. 
To confirm whether you can promote all products in the TikTok Shop, call [/gmv_max/store/shop_ad_usage_check/](https://business-api.tiktok.com/portal/docs?id=1822001084174338) and check the returned `promote_all_products_allowed`. |
| item_group_ids {+Conditional} | string[] | Required when `shopping_ads_type` is `PRODUCT` and `product_specific_type` is `CUSTOMIZED_PRODUCTS`. 

Product SPU (standard product unit) IDs. 

 Max size: 400.

To obtain the list of SPU IDs for products within a TikTok Shop, use [/store/product/get/](https://business-api.tiktok.com/portal/docs?id=1793482248880130). Set `ad_creation_eligible` to `GMV_MAX` and select `item_group_id` values where `status` is `AVAILABLE` and `gmv_max_ads_status` is `UNOCCUPIED`. |
| optimization_goal {Required} | string | Optimization goal. 

Enum value:
- `VALUE`: Gross revenue.|
| deep_bid_type {Required} | string | Bid strategy. 

Enum value:
- `VO_MIN_ROAS`: Minimum ROAS. Bid with an ROI target.|
| roas_bid {+Conditional} | number | Required only when `deep_bid_type` is `VO_MIN_ROAS`.

 ROI target, kept to up to one decimal place. 

Examples: 3.2, 3.

To obtain the recommended ROI target, use [/gmv_max/bid/recommend/](https://business-api.tiktok.com/portal/docs?id=1822001024720897) and check the returned `roas_bid`. |
| budget {Required} | number | Daily budget. 

 To obtain the recommended budget, use [/gmv_max/bid/recommend/](https://business-api.tiktok.com/portal/docs?id=1822001024720897) and check the returned `budget`. |
| promotion_days | object | The promotion days setting details.

**Note**: To customize the percentage and the maximum times the budget can increase per day within your promotion days settings, use `budget_increase_percentage` and `increase_limit`within this object.|
#| is_enabled | boolean | Whether to enable promotion days to automatically optimize your campaign for higher GMV during high-intent shopping dates in regions where your ads are delivering. 

Supported values: `true`, `false`.
Default value: `false`.

When `promotion_days` is specified, this field will be automatically set to `true`. |
#| auto_schedule_enabled | boolean | Valid only when `is_enabled` is `true`.

Whether to use TikTok Shop promotion days schedule.

Supported values: `true`, `false`.

When`is_enabled` is `true`, this field will be automatically set to `true`. |
#| custom_schedule_list {+Conditional} | object[] | Details of the custom promotion day schedules.

- If `auto_schedule_enabled` is `false`, specify at least one set of `start_date` and `end_date` in `custom_schedule_list`.
- If `auto_schedule_enabled` is `true`, `custom_schedule_list` is optional.Max size: 50. |
##| start_date | string | The start date of the custom promotion day schedule, in the format of `YYYY-MM-DD`(ad account time zone).

**Note**: 
- The start date cannot be after the `end_date`.
- The start date cannot be earlier than the current date.
- The start date must be on the same day as or after the `schedule_start_time` of the campaign.
- The custom promotion days schedule will automatically start at 00:00:00 of the start date in the ad account time zone. |
##| end_date | string | The end date of the custom promotion day schedule, in the format of `YYYY-MM-DD` (ad account time zone) .

**Note**: 
- The end date cannot be earlier than the current time.
- The custom promotion days schedule will automatically end at 00:00:00 of the end date in the ad account time zone. |
#| roas_bid_multiplier | number | The target ROI index.
Changes to your target ROI will be in effect during promotion days and may drive higher GMV for this campaign.

Enum values:
- `90`: -10%. To decrease your target ROI by 10% during promotion days.
- `80`: -20%. To decrease your target ROI by 20% during promotion days.
- `70`: -30%. To decrease your target ROI by 30% during promotion days.Default value: `90`. 

**Note**: We will be updating the way ROI goals are calculated during promotions to improve performance accuracy and ensure fairness across campaigns. Instead of using just the value you manually specify, the system will calculate your promotional ROI goal based on **the lower of your recent campaign performance (last 7 non-promotion days) or your entered ROI**, and then apply the selected reduction (10%, 20%, or 30%). This will be an allowlist-only feature. You might not need to make code changes, but the returned value of ROI goal will be different. |
#|budget_increase_percentage|integer|The increase percentage for the budget during promotion days.

Value range: 50-300.
A value of 50 means a 50% budget increase when the automatic budget increase is triggered.
Default value: 50.|
#|increase_limit|integer|The increase limit for the daily budget during promotion days.

Value range: 1-10.
A value of 10 means allows up to 10 budget increases per day when the automatic budget increases are triggered.
Default value: 10.|
|auto_budget|object|The details of the automatic budget settings during non-promotion days.|
#|auto_budget_enabled|boolean|Whether to enable automatic budget increase during non-promotion days.
Enabling automatic budget increase will allow your daily budget to be automatically increased to optimize your campaign for more sales on days when your campaign has reached at least 90% of your ROI target and at least 80% of your budget has been used. Your daily budget will reset to its original amount each day.

Supported values: `true`, `false`.
Default value: `false`.|
#|budget_increase_percentage|integer|The increase percentage for the budget during non-promotion days.

Value range: 50-300.
A value of 50 means a 50% budget increase when the automatic budget increase is triggered.
Default value: 50.|
#|increase_limit|integer|The increase limit for the budget during non-promotion days.

Value range: 1-10.
A value of 10 means allows up to 10 budget increases per day when the automatic budget increases are triggered.
Default value: 10.|
| auto_budget_enabled {-To be deprecated} | boolean | Whether to enable automatic budget increase.
When your achieved ROI reaches at least 90% of the target and 80% or more of your budget has been used, your daily campaign budget may automatically increase by up to 10 times to capture more sales. Your budget will reset to its original amount each day.

- When `is_enabled` within the object `promotion_days` is `true` and`auto_budget_enabled` is `false`, your ROI target will decrease and your daily budget will automatically increase during TikTok Shop promotion days (when `auto_schedule_enabled` is `true`) and custom promotion days as defined by `custom_schedule_list`. Your daily budget will reset to its original amount every day. During standard days, your ROI target and budget won't change.
- When `is_enabled` within the object `promotion_days` is `true` and`auto_budget_enabled` is `true`, auto budget increase will be turned on during TikTok Shop promotion days (when `auto_schedule_enabled` is `true`), custom promotion days as defined by `custom_schedule_list`, **and standard days**. Your daily budget will reset to its original amount every day. During TikTok Shop promotion days and custom promotion days as defined by `custom_schedule_list`, your ROI target will decrease. During standard days, your ROI target won't change.
- When `is_enabled` within the object `promotion_days` is `false` and`auto_budget_enabled` is `true`, your ROI won't change, your daily campaign budget may automatically increase up to 10 times to optimize gross revenue. Your daily budget will reset to its original amount every day. However, if you specify `auto_budget_enabled` and `auto_budget` at the same time, `auto_budget_enabled` will be ignored.
Supported values: `true`, `false`.
Default value: `false`.

**Note**: When you use this parameter, the automatic budget increase settings for GMV Max Campaigns are fixed in terms of percentage and maximum frequency. If you want to customize the percentage and the maximum times the budget can increase per day during non-promotion days, use `auto_budget` instead. |
| schedule_type {Required} | string | Schedule type.

Enum values:
- `SCHEDULE_FROM_NOW`: To run the campaign continuously after the scheduled start time.
- `SCHEDULE_START_END`: To run the campaign between the scheduled start time and end time. |
| schedule_start_time {Required} | string | Campaign delivery start time, in the format of `YYYY-MM-DD HH:MM:SS` (UTC+0). 

 The start time can be up to 12 hours earlier than the current time, but cannot be later than `2028-01-01 00:00:00`.|
| schedule_end_time {+Conditional} | string | 
- Required when `schedule_type` is `SCHEDULE_START_END`. 
- Not supported when `schedule_type` is `SCHEDULE_FROM_NOW`. 
Campaign delivery end time, in the format of `YYYY-MM-DD HH:MM:SS` (UTC+0).

 The end time cannot be later than `2038-01-01 00:00:00`. |
| product_video_specific_type {+Conditional} | string | Required when `shopping_ads_type` is `PRODUCT`. 

The video selection mode. 

Enum values:
- `AUTO_SELECTION`: To autoselect videos. You can specify `identity_list` simultaneously or leave `identity_list` unspecified.
- `CUSTOM_SELECTION`: To manually select videos. You need to specify `item_list` simultaneously.|
|accelerate_testing_for_new_videos|string|Valid only when `product_video_specific_type` is `AUTO_SELECTION`.

Whether to accelerate testing for new videos, that is, prioritize performance testing for your new, recently authorized, and updated videos as part of your campaign.
Videos that have been uploaded or authorized in the past 7 days, including recently authorized TikTok account videos, customized posts, and videos with new or updated product links, will be prioritized for testing. This may temporarily reduce gross revenue, but your campaign's overall ROI will stay within your target ROI range. Your campaign will still be eligible for ROI protection when you turn on accelerated learning.

Enum values:
- `ON`: To accelerate testing for new videos.
- `OFF`: To not accelerate testing for new videos.
Default value: `OFF`.|
| identity_list {+Conditional} | object[] | 
- Required when `shopping_ads_type` is `LIVE`.
- Optional when `shopping_ads_type` is `PRODUCT` and `product_video_specific_type` is `AUTO_SELECTION`.
The list of identities (TikTok accounts) to associate with the GMV Max Campaign.

- When `shopping_ads_type` is `PRODUCT` and `product_video_specific_type` is `AUTO_SELECTION`, specify 0-20 identities as the source of video creatives via this field.To obtain a list of identities available for a Product GMV Max Campaign using the same TikTok Shop, use [/gmv_max/identity/get/](https://business-api.tiktok.com/portal/docs?id=1822001101474882) and select identities with `product_gmv_max_available` as `true`.
- When no identities are specified through `identity_list`, the product images will be used as ad creatives.
- When `shopping_ads_type` is `LIVE`, specify one identity as the LIVE source via this field. To obtain an identity that is available for LIVE GMV Max Campaigns, call [/gmv_max/identity/get/](https://business-api.tiktok.com/portal/docs?id=1822001101474882) and select identities with `live_gmv_max_available` as `true`.|
#| identity_id {+Conditional} | string | Required when `identity_list` is passed.

Identity ID. |
#| identity_type {+Conditional} | string | Required when `identity_list` is passed.

 Identity type. 

Enum values: 
- `AUTH_CODE`: Authorized User. This type of identity is created when you use the authorization code to access a TikTok account or a TikTok post.
- `TT_USER`: TikTok User. This type of identity is created when you bind your TikTok For Business account with your TikTok Business Account, or when you bind your TikTok For Business account with your regular TikTok account and then upgrade the account to Business Account.
- `BC_AUTH_TT`: TikTok Account User in Business Center. This type of identity is created when you add a TikTok account to your Business Center, and the TikTok account owner approves your request. 
- `TTS_TT`: TikTok Account User for TikTok Shop. This type of identity is created when you set an official TikTok account for the TikTok Shop. |
#| identity_authorized_bc_id {+Conditional} | string | Required when `identity_type` is `BC_AUTH_TT`. 

 The ID of the Business Center that a TikTok Account User in Business Center identity is associated with. |
#| identity_authorized_shop_id {+Conditional} | string | Required only when `dentity_type` is `BC_AUTH_TT` and `identity_authorized_shop_id` is returned for the identity from [/gmv_max/identity/get/](https://business-api.tiktok.com/portal/docs?id=1822001101474882). 

 The ID of the TikTok Shop that a TikTok Account User in Business Center identity is associated with. |
#| store_id {+Conditional} | string | Required when `identity_type` is `TTS_TT`. 

The ID of the TikTok Shop that a TikTok Account User for TikTok Shop identity is associated with. |
|affiliate_posts_enabled |boolean|This field is valid and defaults to `true` when the following conditions are both met:
- `shopping_ads_type` is `PRODUCT`
- `product_video_specific_type` is `AUTO_SELECTION`Whether to enable affiliate posts for your Product GMV Max Campaign.
Affiliate posts are TikTok posts created by affiliates (creators participating in the TikTok Shop Affiliate Program) and authorized for use in TikTok Shop Ads. Learn more [about affiliate creatives for TikTok Shop Ads](https://ads.tiktok.com/help/article/about-affiliate-creatives-for-tiktok-shop-ads).

Supported values: `true`, `false`.|
| item_list {+Conditional} | object[] | Required when `shopping_ads_type` is `PRODUCT` and `product_video_specific_type` is `CUSTOM_SELECTION`. 

The list of authorized TikTok posts or customized TikTok posts to associate with the Product GMV Max campaign.
- Authorized TikTok posts are existing posts featuring your selected products from your TikTok accounts or authorized using video codes.If you want to manually select authorized TikTok posts only for the Product GMV Max campaign, include their details using `item_list` and do not specify `custom_anchor_video_list`.
- Customized TikTok posts are newly created posts for the campaign, built by adding customized product links to your selected videos. These posts will be exclusive to this Product GMV Max campaign.If you want to manually select customized TikTok posts for the Product GMV Max campaign, include details of the videos to be used in customized posts using `item_list` and specify `custom_anchor_video_list` simultaneously.
Max size: 50.

To obtain a list of TikTok posts available for a Product GMV Max Campaign using the same TikTok Shop, use [/gmv_max/video/get/](https://business-api.tiktok.com/portal/docs?id=1822001168512129). |
#| item_id {+Conditional} | string | Required when `item_list` is passed.

 The ID of the TikTok post. |
#| spu_id_list {+Conditional} | string[] | Required when `item_list` is passed. 

 Product SPU IDs associated or to associate with the TikTok post. |
#| identity_info {+Conditional} | object | Required when `item_list` is passed. 

Information about the identity associated or to associate with the TikTok post. |
##| identity_id {+Conditional} | string | Required when `item_list` is passed.

 Identity ID. |
##| identity_type {+Conditional} | string | Required when `item_list` is passed.

Identity type. 

Enum values: 
- `AUTH_CODE`: Authorized User. This type of identity is created when you use the authorization code to access a TikTok account or a TikTok post.
- `TT_USER`: TikTok User. This type of identity is created when you bind your TikTok For Business account with your TikTok Business Account, or when you bind your TikTok For Business account with your regular TikTok account and then upgrade the account to Business Account.
- `BC_AUTH_TT`: TikTok Account User in Business Center. This type of identity is created when you add a TikTok account to your Business Center, and the TikTok account owner approves your request. 
- `TTS_TT`: TikTok Account User for TikTok Shop. This type of identity is created when you set an official TikTok account for the TikTok Shop. |
##| identity_authorized_bc_id {+Conditional} | string | Required when `identity_type` is `BC_AUTH_TT`. 

 The ID of the Business Center that a TikTok Account User in Business Center identity is associated with. |
##| identity_authorized_shop_id {+Conditional} | string | Required only when `dentity_type` is `BC_AUTH_TT` and `identity_authorized_shop_id` is returned for the identity from [/gmv_max/identity/get/](https://business-api.tiktok.com/portal/docs?id=1822001101474882). 

 The ID of the TikTok Shop that a TikTok Account User in Business Center identity is associated with. |
##| store_id {+Conditional} | string | Required when `identity_type` is `TTS_TT`. 

The ID of the TikTok Shop that a TikTok Account User for TikTok Shop identity is associated with. |
#| video_info {+Conditional} | object | Required when `item_list` is passed. 

Details of the video in the post. |
##| video_id {+Conditional} | string | Required when `item_list` is passed. 

 The ID of the video. |
| custom_anchor_video_list | object[] | The list of customized TikTok posts to associate with the Product GMV Max campaign.
Customized TikTok posts are posts created during campaign setup by adding customized product links for your products (`spu_id_list` within `custom_anchor_video_list`) to specified videos (`item_id` within `custom_anchor_video_list`). These posts will be exclusive to this Product GMV Max campaign.
- For manual selection: When `shopping_ads_type` is `PRODUCT` and `product_video_specific_type` is `CUSTOM_SELECTION`, specify the videos to be used in customized posts using this field.
- For auto selection: When `shopping_ads_type` is `PRODUCT` and `product_video_specific_type` is `AUTO_SELECTION`, specify the videos to be auto-selected for customized posts using this field.
Max size: 200.

**Note**: Although you can add a maximum number of 200 customized posts during campaign creation, one Product GMV Max campaign can eventually include up to 2,000 customized posts. If you want to specify more than 200 customized posts for a Product GMV Max Campaign, you can update the `custom_anchor_video_list` of the campaign incrementally using [/campaign/gmv_max/update/](https://business-api.tiktok.com/portal/docs?id=1822001009002497), with updates limited to 200 additional posts per request. |
#| item_id {+Conditional}| string | Required when `custom_anchor_video_list` is passed.

The ID of a TikTok video to be used in a customized post.

To retrieve eligible videos, use [/gmv_max/video/get/](https://business-api.tiktok.com/portal/docs?id=1822001168512129) with `custom_posts_eligible` set to true. |
#| spu_id_list {+Conditional}| string[] | Required when `custom_anchor_video_list` is passed.

The SPU IDs of the products to associate with the customized product anchor link in the TikTok post.

Max size: 1. |
#| identity_info {+Conditional}| object | Required when `custom_anchor_video_list` is passed.

Information about the identity to associate with the post. |
##| identity_id {+Conditional}| string | Required when `custom_anchor_video_list` is passed.

Identity ID.

To obtain a list of identities available for GMV Max Campaigns, use [/gmv_max/identity/get/](https://business-api.tiktok.com/portal/docs?id=1822001101474882). |
##| identity_type{+Conditional} | string | Required when `custom_anchor_video_list` is passed.

Identity type.

Enum values:
- `AUTH_CODE`: Authorized User. This type of identity is created when you use the authorization code to access a TikTok account or a TikTok post.
- `TT_USER`: TikTok User. This type of identity is created when you bind your TikTok For Business account with your TikTok Business Account, or when you bind your TikTok For Business account with your regular TikTok account and then upgrade the account to Business Account.
- `BC_AUTH_TT`: TikTok Account User in Business Center. This type of identity is created when you add a TikTok account to your Business Center, and the TikTok account owner approves your request.
- `TTS_TT`: TikTok Account User for TikTok Shop. This type of identity is created when you set an official TikTok account for the TikTok Shop. |
##| identity_authorized_bc_id {+Conditional}| string | Required when `identity_type` is `BC_AUTH_TT`.

The ID of the Business Center that a TikTok Account User in Business Center identity is associated with. |
##| identity_authorized_shop_id {+Conditional}| string | Required only when `identity_type` is `BC_AUTH_TT` and `identity_authorized_shop_id` is returned for the identity from [/gmv_max/identity/get/](https://business-api.tiktok.com/portal/docs?id=1822001101474882).

The ID of the TikTok Shop that a TikTok Account User in Business Center identity is associated with. |
##| store_id {+Conditional}| string | Required when `identity_type` is `TTS_TT`.

The ID of the TikTok Shop that a TikTok Account User for TikTok Shop identity is associated with. |
| campaign_name {Required} | string | The name of the GMV Max Campaign. |
```

### Example

#### Create a Product GMV Max Campaign
```xcodeblock
(code curl http)
curl --location --request POST 'https://business-api.tiktok.com/open_api/v1.3/campaign/gmv_max/create/' \
--header 'Access-Token: {{Access-Token}}' \
--header 'Content-Type: application/json' \
--data '{
    "request_id": "{{request_id}}",
    "advertiser_id": "{{advertiser_id}}",
    "store_id": "{{store_id}}",
    "store_authorized_bc_id": "{{store_authorized_bc_id}}",
    "shopping_ads_type": "PRODUCT",
    "product_specific_type": "ALL",
    "optimization_goal": "VALUE",
    "deep_bid_type": "VO_MIN_ROAS",
    "roas_bid": {{roas_bid}},
    "budget": {{budget}},
    "schedule_type": "SCHEDULE_START_END",
    "schedule_start_time": "{{schedule_start_time}}",
    "schedule_end_time": "{{schedule_end_time}}",
    "product_video_specific_type": "AUTO_SELECTION",
        "identity_list": [
            {
                "identity_id": "{{identity_id}}",
                "identity_type": "TTS_TT",
                "store_id": "{{store_id}}"
            },
            {
                "identity_id": "{{identity_id}}",
                "identity_type": "TT_USER"
            },
            {
                "identity_authorized_bc_id": "{{identity_authorized_bc_id}}",
                "identity_id": "{{identity_id}}",
                "identity_type": "BC_AUTH_TT"
            }
        ],
    "campaign_name": "{{campaign_name}}"
}'
(/code)
```

#### Create a LIVE GMV Max Campaign
```xcodeblock
(code curl http)
curl --location --request POST 'https://business-api.tiktok.com/open_api/v1.3/campaign/gmv_max/create/' \
--header 'Access-Token: {{Access-Token}}' \
--header 'Content-Type: application/json' \
--data '{
    "request_id": "{{request_id}}",
    "advertiser_id": "{{advertiser_id}}",
    "store_id": "{{store_id}}",
    "store_authorized_bc_id": "{{store_authorized_bc_id}}",
    "shopping_ads_type": "LIVE",
    "identity_list": [
        {
            "identity_id": "{{identity_id}}",
            "identity_type": "BC_AUTH_TT",
            "identity_authorized_bc_id": "{{identity_authorized_bc_id}}"
        }
    ],
    "optimization_goal": "VALUE",
    "deep_bid_type": "VO_MIN_ROAS",
    "roas_bid": {{roas_bid}},
    "budget": {{budget}},
    "schedule_type": "{{schedule_type}}",
    "schedule_start_time": "{{schedule_start_time}}",
    "schedule_end_time": "{{schedule_end_time}}",
    "campaign_name": "{{campaign_name}}"
}'
(/code)
```

## Response

``` xtable
|Field{30%}|Type{15%}|Description{55%}|
|---|---|---|
|code |number|Response code. For the complete list of response codes and descriptions, see [Appendix-Return Code](https://ads.tiktok.com/marketing_api/docs?id=1737172488964097). |
|message|string|Response message. For details, see [Appendix - Return Codes](https://ads.tiktok.com/marketing_api/docs?id=1737172488964097).|
|request_id |string|The log ID of a request, which uniquely identifies the request.  |
|data |object|Returned data.|
#| advertiser_id | string | Advertiser ID. |
#| operation_status| string | The status of the GMV Max Campaign.

Enum values:
- `DISABLE`: Disabled.
- `ENABLE`: Enabled.  |
#| campaign_id | string | The ID of the GMV Max Campaign. |
#| campaign_name | string | The name of the GMV Max Campaign. |
#| store_id | string | The ID of the TikTok Shop. |
#| store_authorized_bc_id | string | ID of the Business Center that is authorized to access the TikTok Shop (`store_id`). |
#| shopping_ads_type | string | The type of the GMV Max Campaign.

Enum values:
- `PRODUCT`: Product GMV Max Campaign.
- `LIVE`: Live GMV Max Campaign.  |
#| product_specific_type | string | Different dimensions to choose products. 

Enum values:
- `ALL`: Allow TikTok to dynamically choose from all products within the TikTok Shop.
- `CUSTOMIZED_PRODUCTS`: Specify a customized number of products within the TikTok Shop.
- `UNSET`: Unset. |
#| item_group_ids | string[] | Returned only when `shopping_ads_type` is `PRODUCT` and `product_specific_type` is `CUSTOMIZED_PRODUCTS`. 

Product SPU (standard product unit) IDs. |
#| optimization_goal | string | Optimization goal. 

Enum value:
- `VALUE`: Gross revenue.|
#| roi_protection_enabled | boolean | Whether the campaign is eligible for ROI protection. 
ROI protection is a feature that automatically issues ad credits when the return on investment (ROI) for your campaign falls below a certain threshold despite following GMV Max guidelines and best practices. To learn about the eligibility criteria for ROI protection and scenarios where the campaign is ineligible for ROI protection, see [About ROI protection for GMV Max campaigns](https://ads.tiktok.com/help/article/about-roi-protection-for-gmv-max-campaigns).

Supported values: `true`, `false`.|
#| deep_bid_type | string | Bid strategy. 

Enum value:
- `VO_MIN_ROAS`: Minimum ROAS. Bid with an ROI target.|
#| roas_bid | number | Returned only when `deep_bid_type` is `VO_MIN_ROAS`.

ROI target. |
#| budget | number | Daily budget. |
#| promotion_days | object | The promotion days setting details. |
##| is_enabled | boolean | Whether to enable promotion days to automatically optimize your campaign for higher GMV during high-intent shopping dates in regions where your ads are delivering. 
When promotion days are active for this campaign, your ad credits will be calculated for your promotion days target ROI setting.

Supported values: `true`, `false`. |
##| auto_schedule_enabled | boolean | Whether to use TikTok Shop promotion days schedule.

Supported values: `true`, `false`. |
##| custom_schedule_list | object[] | Details of the custom promotion day schedules. |
###| start_date | string | The start date of the custom promotion day schedule, in the format of `YYYY-MM-DD` (ad account time zone). |
###| end_date | string | The end date of the custom promotion day schedule, in the format of `YYYY-MM-DD`  (ad account time zone). |
##| roas_bid_multiplier | number| The target ROI index.
Changes to your target ROI will be in effect during promotion days and may drive higher GMV for this campaign.

Enum values:
- `90`: -10%. To decrease your target ROI by 10% during promotion days.
- `80`: -20%. To decrease your target ROI by 20% during promotion days.
- `70`: -30%. To decrease your target ROI by 30% during promotion days. |
##| adjusted_roas_bid | number | Promotion days target ROI. |
##|budget_increase_percentage|integer|The increase percentage for the budget during promotion days.

A value of 50 means a 50% budget increase when the automatic budget increase is triggered.|
##|increase_limit|integer|The increase limit for the daily budget during promotion days.

A value of 10 means allows up to 10 budget increases per day when the automatic budget increases are triggered.|
##| current_budget | number | The specified campaign daily budget (`budget`). |
##| next_increase | number | The increase in budget compared with your specified campaign daily budget (`budget`).

Formula: `next_increase` = `current_budget` x `budget_increase_percentage`.

For example, if `budget` is 300 USD and `budget_increase_percentage` is 50, `next_increase` will be 150 USD, indicating a daily budget increase of 150 USD.|
##|remained_times|number|The remaining times of automatic budget increases.|
##|maximum_budget|number|The maximum possible budget.

Formula: `maximum_budget` = `current_budget` + `current_budget` x `budget_increase_percentage` x `remained_times`.

For example, if `current_budget` is 200 USD, `budget_increase_percentage` is 50, and `remained_times` is 10,  your `maximum_budget` will be 1200 USD, as the increase can occur up to 10 times daily.|
##| estimated_gross_revenue_increase | string | The estimated percentage increase in gross revenue due to the ROI change during promotion days. 

Example: `24%`. |
#|auto_budget|object|The details of the automatic budget settings during non-promotion days.|
##|auto_budget_enabled|boolean|Whether to enable automatic budget increase during non-promotion days.

Enabling automatic budget increase will allow your daily budget to be automatically increased to optimize your campaign for more sales on days when your campaign has reached at least 90% of your ROI target and at least 80% of your budget has been used. Your daily budget will reset to its original amount each day.

Supported values: `true`, `false`.|
##|budget_increase_percentage|integer|The increase percentage for the budget during non-promotion days.

A value of 50 means a 50% budget increase when the automatic budget increase is triggered.|
##|increase_limit|integer|The increase limit for the daily budget during non-promotion days.

A value of 10 means allows up to 10 budget increases per day when the automatic budget increases are triggered.|
##|current_budget|number|The specified campaign daily budget (`budget`).|
##|next_increase|number|The increase in budget compared with your specified campaign daily budget (`budget`).

Formula: `next_increase` = `current_budget` x `budget_increase_percentage`.

For example, if `budget` is 300 USD and `budget_increase_percentage` is 50, `next_increase` will be 150 USD, indicating a daily budget increase of 150 USD.|
##|remained_times|number|The remaining times of automatic budget increases.|
##|maximum_budget|number|The maximum possible budget.

Formula: `maximum_budget` = `current_budget` + `current_budget` x `budget_increase_percentage` x `remained_times`.

For example, if `current_budget` is 200 USD, `budget_increase_percentage` is 50, and `remained_times` is 10,  your `maximum_budget` will be 1200 USD, as the increase can occur up to 10 times daily.|
#| auto_budget_enabled {-to be deprecated} | boolean | Whether to enable automatic budget increase.
When your achieved ROI reaches at least 90% of the target and 80% or more of your budget has been used, your daily campaign budget may automatically increase by up to 10 times to capture more sales. Your budget will reset to its original amount each day.

- When `is_enabled` within the object `promotion_days` is `true` and`auto_budget_enabled` is `false`, your ROI target will decrease and your daily budget will automatically increase during TikTok Shop promotion days (when `auto_schedule_enabled` is `true`) and custom promotion days as defined by `custom_schedule_list`. Your daily budget will reset to its original amount every day. During standard days, your ROI target and budget won't change.
- When `is_enabled` within the object `promotion_days` is `true` and`auto_budget_enabled` is `true`, auto budget increase will be turned on during TikTok Shop promotion days (when `auto_schedule_enabled` is `true`), custom promotion days as defined by `custom_schedule_list`, **and standard days**. Your daily budget will reset to its original amount every day. During TikTok Shop promotion days and custom promotion days as defined by `custom_schedule_list`, your ROI target will decrease. During standard days, your ROI target won't change.
- When `is_enabled` within the object `promotion_days` is `false` and`auto_budget_enabled` is `true`, your ROI won't change, your daily campaign budget may automatically increase up to 10 times to optimize gross revenue. Your daily budget will reset to its original amount every day.
Supported values: `true`, `false`.|
#| schedule_type | string | Schedule type.

Enum values:
- `SCHEDULE_FROM_NOW`: To run the campaign continuously after the scheduled start time.
- `SCHEDULE_START_END`: To run the campaign between the scheduled start time and end time. |
#| schedule_start_time | string | Campaign delivery start time, in the format of `YYYY-MM-DD HH:MM:SS` (UTC+0). |
#| schedule_end_time | string | Campaign delivery end time, in the format of `YYYY-MM-DD HH:MM:SS` (UTC+0). |
#| placements | string[] | Placements.
The apps where you want to deliver your campaign. 

 Enum values: 
- `PLACEMENT_TIKTOK`: TikTok.
- `PLACEMENT_PANGLE`: Pangle.
**Note**:  
- Product GMV Max Campaigns automatically explore and choose from the most extensive audience scope across TikTok and Pangle. Learn more [about Pangle](https://ads.tiktok.com/help/article/pangle-placement).
- If you want to opt out of the Pangle placement for your Product GMV Max Campaigns, contact your TikTok representative.|
#| location_ids | string[] | The IDs of the targeted locations. 

 To learn about the corresponding location for a location ID, see [Location IDs](https://business-api.tiktok.com/portal/docs?id=1739311040498689). |
#| age_groups | string[] | The targeted age groups.

 For enum values, see [Enumeration - Age Group](https://ads.tiktok.com/marketing_api/docs?id=1737174886619138#item-link-Age%20Group). |
#| product_video_specific_type | string | The video selection mode. 

Enum values:
- `AUTO_SELECTION`: To autoselect videos.
- `CUSTOM_SELECTION`: To manually select videos. 
- `UNSET`: Unset. |
#|accelerate_testing_for_new_videos|string|Whether to accelerate testing for new videos, that is, prioritize performance testing for your new, recently authorized, and updated videos as part of your campaign.
Videos that have been uploaded or authorized in the past 7 days, including recently authorized TikTok account videos, customized posts, and videos with new or updated product links, will be prioritized for testing. This may temporarily reduce gross revenue, but your campaign's overall ROI will stay within your target ROI range. Your campaign will still be eligible for ROI protection when you turn on accelerated learning.

Enum values:
- `ON`: To accelerate testing for new videos.
- `OFF`: To not accelerate testing for new videos.|
#| identity_list | object[] | The list of identities (TikTok accounts) associated with the GMV Max Campaign. |
##| identity_id | string | Identity ID. |
##| identity_type | string | Identity type. 

Enum values: 
- `AUTH_CODE`: Authorized User. This type of identity is created when you use the authorization code to access a TikTok account or a TikTok post.
- `TT_USER`: TikTok User. This type of identity is created when you bind your TikTok For Business account with your TikTok Business Account, or when you bind your TikTok For Business account with your regular TikTok account and then upgrade the account to Business Account.
- `BC_AUTH_TT`: TikTok Account User in Business Center. This type of identity is created when you add a TikTok account to your Business Center, and the TikTok account owner approves your request. 
- `TTS_TT`: TikTok Account User for TikTok Shop. This type of identity is created when you set an official TikTok account for the TikTok Shop. |
##| identity_authorized_bc_id | string | Returned only when `identity_type` is `BC_AUTH_TT`. 

The ID of the Business Center that a TikTok Account User in Business Center identity is associated with. |
##| identity_authorized_shop_id | string | Returned for some `BC_AUTH_TT` identities. 

The ID of the TikTok Shop that the TikTok Account User in Business Center identity is associated with. |
##| store_id | string | Returned only when `identity_type` is `TTS_TT`. 

The ID of the TikTok Shop that a TikTok Account User for TikTok Shop identity is associated with. |
#|affiliate_posts_enabled |boolean|Whether to enable affiliate posts for your Product GMV Max Campaign.
Affiliate posts are TikTok posts created by affiliates (creators participating in the TikTok Shop Affiliate Program) and authorized for use in TikTok Shop Ads. Learn more [about affiliate creatives for TikTok Shop Ads](https://ads.tiktok.com/help/article/about-affiliate-creatives-for-tiktok-shop-ads).

Supported values: `true`, `false`.|
#| item_list| object[] | The list of authorized TikTok posts associated with the GMV Max campaign. 
Authorized TikTok posts are existing posts featuring your selected products from your TikTok accounts or authorized using video codes. |
##| item_id | string | The ID of the TikTok post. |
##| text | string | The caption of the TikTok post. |
##| spu_id_list| string[] | The list of Product SPU IDs that the TikTok post is associated with. |
##| identity_info | object | Information about the identity associated with the TikTok post. |
###| identity_id | string | Identity ID. |
###| identity_type | string | Identity type. 

Enum values: 
- `AUTH_CODE`: Authorized User. This type of identity is created when you use the authorization code to access a TikTok account or a TikTok post.
- `TT_USER`: TikTok User. This type of identity is created when you bind your TikTok For Business account with your TikTok Business Account, or when you bind your TikTok For Business account with your regular TikTok account and then upgrade the account to Business Account.
- `BC_AUTH_TT`: TikTok Account User in Business Center. This type of identity is created when you add a TikTok account to your Business Center, and the TikTok account owner approves your request. 
- `TTS_TT`: TikTok Account User for TikTok Shop. This type of identity is created when you set an official TikTok account for the TikTok Shop. |
###| identity_authorized_bc_id | string | Returned only when `identity_type` is `BC_AUTH_TT`. 

The ID of the Business Center that a TikTok Account User in Business Center identity is associated with. |
###| identity_authorized_shop_id | string | Returned for some `BC_AUTH_TT` identities. 

The ID of the TikTok Shop that the TikTok Account User in Business Center identity is associated with. |
###| store_id | string | Returned only when `identity_type` is `TTS_TT`. 

The ID of the TikTok Shop that a TikTok Account User for TikTok Shop identity is associated with. |
###| profile_image | string | Temporary profile image URL for the TikTok account that is associated with the identity. 

Validity period: around 48 hours. The expiration time is included in the URL after the `x-expires` parameter, in the format of an Epoch/Unix timestamp in seconds.

Once the URL expires, you need to call [/campaign/gmv_max/info/](https://business-api.tiktok.com/portal/docs?id=1822000968821762) to obtain a new URL. |
###| user_name| string | The username of the TikTok account that is associated with the identity. |
##| video_info | object | Details of the video in the post. |
###| video_id | string | The ID of the video. |
###| video_cover_url | string | Temporary URL for the video cover.

Validity period: around 24 hours. The expiration time is included in the URL after the `x-expires` parameter, in the format of an Epoch/Unix timestamp in seconds. 

Once the URL expires, you need to call [/campaign/gmv_max/info/](https://business-api.tiktok.com/portal/docs?id=1822000968821762) to obtain a new URL. |
###| preview_url | string | Temporary preview URL for the video. 

Validity period: six hours.

Once the URL expires, you need to call [/campaign/gmv_max/info/](https://business-api.tiktok.com/portal/docs?id=1822000968821762) to obtain a new URL. |
###| height | number | The height of the video in pixels. 

 Example: 1920. |
###| width | number | The width of the video in pixels.

Example: 1080. |
###| bit_rate | number | The bit rate of the video in bps. 

Example: 8500323. |
###| duration | number | The duration of the video in seconds. 

Example: 3.669. |
###| size | number | The size of the video in bytes. 

Example: 3898461. |
###| signature | string | The MD5 of the video. 

Example: `ab1cd2345e678fghi91jkl23b456m7no`. |
###| format | string | The format of the video.

Example: `mp4`. |
###| definition | string | The definition of the video.

 Example: `1080p`. |
###| fps | number | The frames per second (FPS) of the video. 

Example: 27. |
#|campaign_custom_anchor_video_id|string|The ID of the collection of customized posts created in the Product GMV Max Campaign.

You can pass this field to [/gmv_max/custom_anchor_video_list/get/](https://business-api.tiktok.com/portal/docs?id=1830215925061633) to obtain the details of the customized posts within the collection.|
#| custom_anchor_video_list | object[] | The list of customized TikTok posts associated with the GMV Max campaign. 
Customized TikTok posts are posts with custom product links. |
##| item_id | string | The ID of the TikTok post. |
##| spu_id_list| string[] | The list of Product SPU IDs that the TikTok post is associated with. |
##| identity_info | object | Information about the identity associated with the TikTok post. |
###| identity_id | string | Identity ID. |
###| identity_type | string | Identity type. 

Enum values: 
- `AUTH_CODE`: Authorized User. This type of identity is created when you use the authorization code to access a TikTok account or a TikTok post.
- `TT_USER`: TikTok User. This type of identity is created when you bind your TikTok For Business account with your TikTok Business Account, or when you bind your TikTok For Business account with your regular TikTok account and then upgrade the account to Business Account.
- `BC_AUTH_TT`: TikTok Account User in Business Center. This type of identity is created when you add a TikTok account to your Business Center, and the TikTok account owner approves your request. 
- `TTS_TT`: TikTok Account User for TikTok Shop. This type of identity is created when you set an official TikTok account for the TikTok Shop. |
###| identity_authorized_bc_id | string | Returned only when `identity_type` is `BC_AUTH_TT`. 

The ID of the Business Center that a TikTok Account User in Business Center identity is associated with. |
###| identity_authorized_shop_id | string | Returned for some `BC_AUTH_TT` identities. 

The ID of the TikTok Shop that the TikTok Account User in Business Center identity is associated with. |
###| store_id | string | Returned only when `identity_type` is `TTS_TT`. 

The ID of the TikTok Shop that a TikTok Account User for TikTok Shop identity is associated with. |
```

### Example
#### Create a Product GMV Max Campaign
```xcodeblock
(code Success-Response http)
HTTPS/1.1 200 OK
{
    "code": 0,
    "message": "OK",
    "request_id": "{{request_id}}",
    "data": {
        "advertiser_id": "{{advertiser_id}}",
        "age_groups": [
            "AGE_18_24",
            "AGE_25_34",
            "AGE_35_44",
            "AGE_45_54",
            "AGE_55_100"
        ],
        "budget": {{budget}},
        "campaign_id": "{{campaign_id}}",
        "campaign_name": "{{campaign_name}}",
        "custom_anchor_video_list": [],
        "deep_bid_type": "VO_MIN_ROAS",
        "identity_list": [
            {
                "identity_id": "{{identity_id}}",
                "identity_type": "TTS_TT",
                "store_id": "{{store_id}}"
            },
            {
                "identity_id": "{{identity_id}}",
                "identity_type": "TT_USER"
            },
            {
                "identity_authorized_bc_id": "{{identity_authorized_bc_id}}",
                "identity_id": "{{identity_id}}",
                "identity_type": "BC_AUTH_TT"
            }
        ],
        "item_list": [],
        "location_ids": [
            "1562822"
        ],
        "operation_status": "ENABLE",
        "optimization_goal": "VALUE",
        "placements": [
            "PLACEMENT_TIKTOK"
        ],
        "product_specific_type": "ALL",
        "product_video_specific_type": "AUTO_SELECTION",
		"affiliate_posts_enabled": true,
        "roas_bid": {{roas_bid}},
        "schedule_end_time": "{{schedule_end_time}}",
        "schedule_start_time": "{{schedule_start_time}}",
        "schedule_type": "SCHEDULE_START_END",
        "shopping_ads_type": "PRODUCT",
        "store_authorized_bc_id": "{{store_authorized_bc_id}}",
        "store_id": "{{store_id}}"
    }
}
(/code)
```

#### Create a LIVE GMV Max Campaign
```xcodeblock
(code Success-Response http)
HTTPS/1.1 200 OK
{
    "code": 0,
    "message": "OK",
    "request_id": "{{request_id}}",
    "data": {
        "advertiser_id": "{{advertiser_id}}",
        "age_groups": [
            "AGE_18_24",
            "AGE_25_34",
            "AGE_35_44",
            "AGE_45_54",
            "AGE_55_100"
        ],
        "budget": {{budget}},
        "campaign_id": "{{campaign_id}}",
        "campaign_name": "{{campaign_name}}",
        "custom_anchor_video_list": [],
        "deep_bid_type": "VO_MIN_ROAS",
        "identity_list": [
            {
                "identity_authorized_bc_id": "{{identity_authorized_bc_id}}",
                "identity_id": "{{identity_id}}",
                "identity_type": "BC_AUTH_TT"
            }
        ],
        "item_list": [],
		"affiliate_posts_enabled": false,
        "location_ids": [
            "1562822"
        ],
        "operation_status": "ENABLE",
        "optimization_goal": "VALUE",
        "placements": [
            "PLACEMENT_TIKTOK"
        ],
        "roas_bid": {{roas_bid}},
        "schedule_end_time": "{{schedule_end_time}}",
        "schedule_start_time": "{{schedule_start_time}}",
        "schedule_type": "SCHEDULE_START_END",
        "shopping_ads_type": "LIVE",
        "store_authorized_bc_id": "{{store_authorized_bc_id}}",
        "store_id": "{{store_id}}"
    }
}
(/code)
```
