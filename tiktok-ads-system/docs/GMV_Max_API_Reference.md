# TikTok GMV Max API - Complete Reference

---

## 1. Get GMV Max Campaigns

**Description:** Use this endpoint to retrieve GMV Max Campaigns within an ad account.

**Method:** `GET`

**Endpoint:** `https://business-api.tiktok.com/open_api/v1.3/gmv_max/campaign/get/`

### Headers

| Field | Data Type | Required | Description |
|-------|-----------|----------|-------------|
| Access-Token | string | Required | Authorized access token. For details, see Authentication. |
| Content-Type | string | Required | `application/json` |

### Parameters

| Field | Data Type | Required | Description |
|-------|-----------|----------|-------------|
| advertiser_id | string | Required | Advertiser ID. |
| filtering | object | Optional | Filter criteria used for search. |
| filtering.campaign_ids | string[] | Optional | A list of up to 100 GMV Max Campaign IDs. If not specified, all campaigns are returned by default. |
| filtering.campaign_name | string | Optional | A campaign name keyword. If provided, only the campaigns with names that contain the keyword will be returned. It is case-insensitive, has a 512 characters limit. |
| filtering.creation_filter_start_time | string | Optional | The start time for filtering on creation time, in format `YYYY-MM-DD HH:MM:SS`. |
| filtering.creation_filter_end_time | string | Optional | The end time for filtering on creation time, in format `YYYY-MM-DD HH:MM:SS`. |
| past_date_provisional_status | string | Optional | Pass this to search for GMV Max Campaigns with a specific provisional status. Enum values: `ACTIVE`, `PAUSED`, `NOT_DELIVERING`. |
| shop_id | string | Optional | A list of TikTok Shop IDs. |
| campaign_id | string | Optional | |
| page | integer | Optional | Page number. |
| page_size | integer | Optional | Page size. Default is 10. Max is 100. |
| primary_status | string | Optional | Primary status. |
| sorting | object | Optional | Sorting criteria. |
| sorting.field | string | Optional | The field name for sorting. |
| sorting.order | string | Optional | Sort order: `ASC` or `DESC`. |
| create_filter_start_time | string | Optional | |
| create_filter_end_time | string | Optional | |

### Response Fields

| Field | Type | Description |
|-------|------|-------------|
| code | integer | Response code. 0 for success. |
| message | string | Response message. |
| request_id | string | Request ID. |
| data | object | Response data. |
| data.list | object[] | List of GMV Max Campaigns. |
| data.page_info | object | Pagination info. |
| data.page_info.page | integer | Current page. |
| data.page_info.page_size | integer | Page size. |
| data.page_info.total_number | integer | Total number of campaigns. |
| data.page_info.total_page | integer | Total number of pages. |

---

## 2. Get the Details of a GMV Max Campaign

**Description:** Use this endpoint to retrieve the details of a GMV Max Campaign.

**Method:** `GET`

**Endpoint:** `https://business-api.tiktok.com/open_api/v1.3/gmv_max/campaign/get_detail/`

### Headers

| Field | Data Type | Required | Description |
|-------|-----------|----------|-------------|
| Access-Token | string | Required | Authorized access token. For details, see Authentication. |
| Content-Type | string | Required | `application/json` |

### Parameters

| Field | Data Type | Required | Description |
|-------|-----------|----------|-------------|
| advertiser_id | string | Required | The ID of the advertiser. |
| campaign_id | string | Required | The ID of the GMV Max Campaign. To create a GMV Max campaign and obtain the campaign ID, see create campaign API. A filter matching GMV Max Campaign where an ad account can be retrieved via get campaigns API. |

### Response Fields

| Field | Type | Description |
|-------|------|-------------|
| code | integer | Response code. |
| message | string | Response message. |
| request_id | string | Request ID. |
| data | object | Response data. |
| data.advertiser_id | string | Advertiser ID. |
| data.campaign_id | string | Campaign ID. |
| data.campaign_name | string | The name of the GMV Max Campaign. |
| data.shop_id | string | The ID of the TikTok Shop. |
| data.status | string | The status of the GMV Max campaign. Enum values: `ENABLE`, `DISABLE`. |
| data.roas | float | The ROAS of the GMV Max campaign. |
| data.operation_status | string | Operation status. Enum values: `ENABLE`, `DISABLE`. |
| data.opt_status | string | Optimization status. |
| data.secondary_status | string | Secondary status. |
| data.budget_mode | string | Budget mode. |
| data.budget | float | The budget of the GMV Max Campaign. |
| data.identity_type | string | Identity type. |
| data.identity_id | string | Identity ID. |
| data.shopping_ads_type | string | Shopping ads type. |
| data.operate_status | string | |
| data.video_id | string | Video ID. |
| data.is_smart_performance_campaign | boolean | Whether this is a smart performance campaign. |
| data.objective_type | string | The type of the GMV Max campaign. |
| data.modify_time | string | The time the campaign was last modified in the format `YYYY-MM-DD HH:MM:SS`. |
| data.create_time | string | The time the campaign was created. |

---

## 3. Create a GMV Max Campaign

**Description:** Use this endpoint to create a GMV Max Campaign.

**Method:** `POST`

**Endpoint:** `https://business-api.tiktok.com/open_api/v1.3/gmv_max/campaign/create/`

### Headers

| Field | Data Type | Required | Description |
|-------|-----------|----------|-------------|
| Access-Token | string | Required | Authorized access token. For details, see Authentication. |
| Content-Type | string | Required | `application/json` |

### Parameters

| Field | Data Type | Required | Description |
|-------|-----------|----------|-------------|
| advertiser_id | string | Required | Advertiser ID. Note: If the request fails with the same request ID multiple times within 5 minutes for the same ad account, the response will be a 500 error. If a duplicate request with the same request ID is submitted successfully, it will return the first result. The ID is different from the `advertiser_id` stored in the corporate parameters, which is used to uniquely identify an API request. |
| shop_id | string | Required | The ID of the TikTok Shop. The ID has been selected in a few request parameters. It is 1 to 64 characters. |
| objectype_id | string | Required | |
| store_authorized_bc_id | string | Required | The ID of the Business Center that is authorized to access the TikTok Shop. |
| identity_id | string | Required | To create the TikTok Shop that is available for GMV Max Campaigns, use `store_authorized_bc_id` and confirm that the resource is a `gmv_max_qualified` one. |
| identity_type | string | Required | The identity type. Enum values: `CUSTOMIZED_USER`, `BC_AUTH_TT`, `TT_USER`. |
| shopping_ads_type | string | Required | The type of the GMV Max Campaign. Enum values: `PRODUCT` (Product GMV Max Campaign), `LIVE` (GMV Max Campaign). |
| campaign_name | string | Optional | Name of the GMV Max campaign. |
| roas | float | Optional | ROAS value. It takes values from a create campaign call. Also refer to `get_recommended_roi` to get recommended ROI. |
| budget | float | Optional | The budget for the campaign. |
| product_specific_type | string | Optional | Product-specific parameter. Enum values: `ALL` (allow TikTok to automatically choose from all available products from the TikTok Shop), `PRODUCT_SET` (apply to a customized number of products within their TikTok Shop). |

### Response Fields

| Field | Type | Description |
|-------|------|-------------|
| code | integer | Response code. |
| message | string | Response message. |
| request_id | string | Request ID. |
| data | object | Response data. |
| data.campaign_id | string | The ID of the created GMV Max campaign. |

---

## 4. Update a GMV Max Campaign

**Description:** Use this endpoint to update a GMV Max Campaign. This endpoint supports incremental updates.

**Method:** `POST`

**Endpoint:** `https://business-api.tiktok.com/open_api/v1.3/gmv_max/campaign/update/`

> **Note:** If you want to update the draft status of a GMV Max campaign, see `status/update` endpoint.

### Headers

| Field | Data Type | Required | Description |
|-------|-----------|----------|-------------|
| Access-Token | string | Required | Authorized access token. For details, see Authentication. |
| Content-Type | string | Required | `application/json` |

### Parameters

| Field | Data Type | Required | Description |
|-------|-----------|----------|-------------|
| advertiser_id | string | Required | Advertiser ID. To create the ad account that corresponds to the TikTok Shop via the Open API, use `advertiser/create` API. |
| campaign_id | string | Required | A valid GMV Max Campaign must meet the criteria on see `campaign/get_detail` API. It is the existing GMV Max Campaign within the ad account, see get campaigns API. |
| roas | float | Optional | ROAS value. |
| budget | float | Optional | The daily budget for the campaign. To obtain the recommended budget, use `get_recommended_roi` API. |
| campaign_name | string | Optional | Campaign name. Max 512 characters. |
| operation_status | string | Optional | To update the operational status. Note: To suspend the campaign and the associated creative but keep the budget and status at the start of the next scheduling period, set to `DISABLE`. Whether or not a campaign that is automatically paused can be automatically activated by TikTok after adjusting balance or experience status will not be affected by this setting. |
| product_specific_type | string | Optional | Product-specific type. Supported values: `ALL`, `PRODUCT_SET`. |
| identity_id | string | Optional | |
| identity_type | string | Optional | |

### Response Fields

| Field | Type | Description |
|-------|------|-------------|
| code | integer | Response code. |
| message | string | Response message. |
| request_id | string | Request ID. |
| data | object | Response data. |
| data.campaign_id | string | The ID of the updated GMV Max campaign. |

---

## 5. Get the Recommended GMV Max ROI Target and Budget

**Description:** Use this endpoint to obtain the recommended ROI target and budget for a Product GMV Max or Live GMV Max Campaign from a specific TikTok Shop.

**Method:** `GET`

**Endpoint:** `https://business-api.tiktok.com/open_api/v1.3/gmv_max/campaign/recommended/`

### Headers

| Field | Data Type | Required | Description |
|-------|-----------|----------|-------------|
| Access-Token | string | Required | Authorized access token. For details, see Authentication. |

### Parameters

| Field | Data Type | Required | Description |
|-------|-----------|----------|-------------|
| advertiser_id | string | Required | The ID of the TikTok Shop. |
| shop_id | string | Required | To obtain a TikTok Shop that is available for GMV Max Campaigns, use `store_authorized_bc_id` and confirm that the resource is a `gmv_max_qualified`. |
| shopping_ads_type | string | Required | Determines which type of the campaign recommendations to retrieve. Enum values: `PRODUCT` (Product GMV Max Campaign), `LIVE` (Live GMV Max Campaign). |
| optimization_goal | string | Required | The optimization goal for the campaign. Enum values: `VALUE` (GMV as optimization goal), `INSTALL` (App install). |
| roas_goal_ids | string[] | Optional | IDs to retrieve specific recommendations. |
| shop_goals | array | Optional | |
| identity_id | string | Optional | The GMV source identifier that you want to use in a Live GMV Max Campaign. |

### Response Fields

| Field | Type | Description |
|-------|------|-------------|
| code | integer | Response code. |
| message | string | Response message. |
| request_id | string | Request ID. |
| data | object | Response data. |
| data.list | array | List of recommended ROI targets and budgets. |

---

## 6. Create a Max Delivery or Creative Boost Session

**Description:** Use this endpoint to create a max delivery session for a specific product or a creative boost session for a specific video in a Product GMV Max Campaign.
- Max delivery for GMV Max sets an additional budget and transitions gross revenue for selected products in your campaign over a specified period of time (see Max Delivery promotions for GMV Max).
- Creative boost is exclusively within Product GMV Max that allows sellers to manually promote specific videos by allocating extra budget.

### Before You Start

**Prerequisites for creating a max delivery session:**
1. Ensure that the current optimization mode of the campaign is Target ROI.
2. In order to use `campaign_update` API to activate campaign details and verify that the campaign status is "active", create/verify GMV Max campaign status.
3. After creating Product GMV Max Campaign within your ad account, using `campaign/create` API.

**Prerequisites for creating a creative boost session:**
1. Ensure there is a Product GMV Max Campaign within your ad account.
2. Ensure that the product associated with the video that you want to create a creative boost for has video details available in the shop.
3. Ensure that a creative boost is funded for more than $50 budget. Within one Product GMV Max campaign, you can create a creative boost for at most 200 videos.
4. Ensure the video has been previously added to the campaign.
5. Ensure that the creative boost session you want to create for it at the date does not overlap with other existing creative boost sessions.
6. Ensure that if you want to include creative boost for dual-run dual authorizations, both are `activated`, `matched`, or `unmatched`.

**Method:** `POST`

**Endpoint:** `https://business-api.tiktok.com/open_api/v1.3/gmv_max/campaign/max_session/create/`

### Headers

| Field | Data Type | Required | Description |
|-------|-----------|----------|-------------|
| Access-Token | string | Required | Authorized access token. For details, see Authentication. |
| Content-Type | string | Required | `application/json` |

### Parameters (for creating a max delivery session)

| Field | Data Type | Required | Description |
|-------|-----------|----------|-------------|
| advertiser_id | string | Required | Advertiser ID. |
| campaign_id | string | Required | To create a Product GMV Max Campaign and obtain the campaign ID, use `campaign/create` API and match the shopping_ads_type to `PRODUCT`. |

Additional parameters are described in the "Before you start" section prerequisites depending on session type (max delivery vs creative boost).

---

## 7. Update a Max Delivery or Creative Boost Session

**Description:** Use this endpoint to update a max delivery session for a specific product or a creative boost session for a specific video within a Product GMV Max Campaign.

> **Note:** You cannot update max delivery or creative boost sessions that have ended.

**Method:** `POST`

**Endpoint:** `https://business-api.tiktok.com/open_api/v1.3/gmv_max/campaign/max_session/update/`

### Headers

| Field | Data Type | Required | Description |
|-------|-----------|----------|-------------|
| Access-Token | string | Required | Authorized access token. For details, see Authentication. |
| Content-Type | string | Required | `application/json` |

### Parameters (for updating a max delivery session)

| Field | Data Type | Required | Description |
|-------|-----------|----------|-------------|
| advertiser_id | string | Required | Advertiser ID. |
| campaign_id | string | Required | To create a Product GMV Max Campaign and obtain the campaign ID, use `campaign/create` and match shopping_ads_type to `PRODUCT`. It filters results in Product GMV Max Campaigns where your ad account can be retrieved via get campaigns API. |
| session_id | string | Required | The ID of the max delivery session. |
| roas_id | string | Optional | To allow the ROI ID of the max delivery session, use `recommended ROI` API. |
| budget | float | Optional | The max daily budget for the session. |
| end_time | string | Optional | To allow the ROI ID of the max delivery session within a Product GMV Max Campaign, use recommended ROI API and match entities with the Live ROI. |
| promote_type | string | Optional | The type of the max delivery session. Supported values: `max_delivery`, `creative_boost`. |
| session_status | string | Optional | Status of the session. To enable the max delivery mode for the product selected, set to `ENABLE`. To disable the max delivery mode for the product selected, set to `DISABLE`. |

### Response Fields

| Field | Type | Description |
|-------|------|-------------|
| code | integer | Response code. |
| message | string | Response message. |
| request_id | string | Request ID. |

---

## 8. Get Max Delivery or Creative Boost Sessions Within a Campaign

**Description:** Use this endpoint to retrieve all active max delivery sessions for products or creative boost sessions for videos within a Product GMV Max Campaign.

> Sessions that have ended cannot be retrieved via `campaign/max_session/get`. To learn details of those sessions, use `campaign/max_session/detail`.

**Method:** `GET`

**Endpoint:** `https://business-api.tiktok.com/open_api/v1.3/gmv_max/campaign/max_session/get/`

### Headers

| Field | Data Type | Required | Description |
|-------|-----------|----------|-------------|
| Access-Token | string | Required | Authorized access token. For details, see Authentication. |

### Parameters

| Field | Data Type | Required | Description |
|-------|-----------|----------|-------------|
| advertiser_id | string | Required | Advertiser ID. |
| campaign_id | string | Required | To create a Product GMV Max Campaign and obtain the campaign ID, use `campaign/create` API and match the shopping_ads_type to `PRODUCT`. To filter existing Product GMV Max Campaigns within your ad account, use get campaigns API. |

### Response Fields

| Field | Type | Description |
|-------|------|-------------|
| code | integer | Response code. |
| message | string | Response message. For details, see Response Status Code. |
| request_id | string | Request ID. |
| data | object | Response data. |
| data.list | array | List of sessions. |
| data.list[].session_id | string | Session ID. |
| data.list[].campaign_id | string/int64 | The ID of the max delivery session for product or creative boost session for video within the Product GMV Max Campaign. |
| data.list[].promote_type | string | Promote type. |
| data.list[].session_status | string | Status of the session. Enum values: `ENABLED`, `DISABLED`. |
| data.list[].budget | float | Budget. |
| data.list[].start_time | string | Start time. The start timestamp for the ID of a max delivery session. |
| data.list[].end_time | string | End time. |
| data.list[].roas_id | string | ROAS ID. |

---

## 9. Get Details of Max Delivery or Creative Boost Sessions

**Description:** Use this endpoint to retrieve the details of max delivery or creative boost sessions for a list of given session IDs.

**Method:** `GET`

**Endpoint:** `https://business-api.tiktok.com/open_api/v1.3/gmv_max/campaign/max_session/detail/`

### Headers

| Field | Data Type | Required | Description |
|-------|-----------|----------|-------------|
| Access-Token | string | Required | Authorized access token. For details, see Authentication. |

### Parameters

| Field | Data Type | Required | Description |
|-------|-----------|----------|-------------|
| advertiser_id | string | Required | Advertiser ID. |
| session_ids | string[] | Required | The IDs of the max delivery or creative boost sessions for products in a Product GMV Max Campaign. To obtain IDs of active max delivery sessions within a Product GMV Max Campaign, use `campaign/max_session/get` and obtain session IDs. To obtain IDs of all (active or ended) creative boost sessions within a campaign, use `campaign/max_session/get` and obtain session IDs. |

### Response Fields

| Field | Type | Description |
|-------|------|-------------|
| code | integer | Response code. |
| message | string | Response message. For details, see Response Status Code. |
| request_id | string | Request ID. |
| data | object | Response data. |
| data.list | array | List of session details. |
| data.list[].session_id | string | Session ID. |
| data.list[].campaign_id | int64 | Campaign ID. |
| data.list[].promote_type | string | The ID of max delivery or creative boost session. |
| data.list[].session_status | string | Status. |
| data.list[].budget | float | Budget. |
| data.list[].start_time | string | Start time. |
| data.list[].end_time | string | End time. The end timestamp for this ID of a max delivery session. |
| data.list[].status | string | Status. Enum values: `RUNNING` (active, max delivery session), `ENDED` (ended), `PAUSED` (paused, creative boost session). |
| data.list[].roas_id | string | ROAS ID. |

---

## 10. Delete a Max Delivery or Creative Boost Session

**Description:** Use this endpoint to delete a max delivery session for a specific product or a creative boost session for a specific video in an active Product GMV Max Campaign.

**Method:** `POST`

**Endpoint:** `https://business-api.tiktok.com/open_api/v1.3/gmv_max/campaign/max_session/delete/`

### Headers

| Field | Data Type | Required | Description |
|-------|-----------|----------|-------------|
| Access-Token | string | Required | Authorized access token. For details, see Authentication. |
| Content-Type | string | Required | `application/json` |

### Parameters

| Field | Data Type | Required | Description |
|-------|-----------|----------|-------------|
| advertiser_id | string | Required | Advertiser ID. |
| session_ids | string[] | Required | The IDs of the max delivery session for a product or creative boost session for a video in the Product GMV Max Campaign. To obtain the IDs of active max delivery sessions within a Product GMV Max Campaign, use `campaign/max_session/get` and obtain session IDs with `SESSION_ID` or `RUNNING`. To obtain the IDs of active creative boost sessions within a Product GMV Max Campaign, use `campaign/max_session/get` and obtain session IDs with `SESSION_ID` or `CREATIVE_BOOST`. |

### Response Fields

| Field | Type | Description |
|-------|------|-------------|
| code | integer | Response code. For the complete list of response codes and descriptions, see Response Status Code. |
| message | string | Response message. For details, see Response Status Code. |
| request_id | string | The ID of a request, which uniquely identifies the request. |

### Response Example

```json
{
  "code": 0,
  "message": "",
  "data": {
    "session_ids": ["session_id1", "session_id2"]
  }
}
```

---

## 11. Get TikTok Shops for GMV Max Campaigns

**Description:** Use this endpoint to obtain a list of TikTok Shops that the ad account has access to and whether the TikTok Shops can be used to create GMV Max Campaigns.

**Method:** `GET`

**Endpoint:** `https://business-api.tiktok.com/open_api/v1.3/gmv_max/shop/get/`

### Headers

| Field | Data Type | Required | Description |
|-------|-----------|----------|-------------|
| Access-Token | string | Required | Authorized access token. For details, see Authentication. |

### Parameters

| Field | Data Type | Required | Description |
|-------|-----------|----------|-------------|
| advertiser_id | string | Required | Advertiser ID. |

### Response Fields

| Field | Type | Description |
|-------|------|-------------|
| code | integer | Response code. For the complete list of response codes and descriptions, see Response Status Code. |
| message | string | Response message. |
| request_id | string | The ID of a request, which uniquely identifies the request. |
| data | object | Response data. |
| data.list | array | List of shops. |
| data.list[].shop_id | string | The ID of the TikTok Shop the ad account has access to. |
| data.list[].shop_name | string | Name of the TikTok Shop. |
| data.list[].region | string | The region of the shop. |
| data.list[].store_authorized_bc_id | string | Store authorized Business Center ID. It is the Business Center that is authorized to access the TikTok Shop. |
| data.list[].gmv_max_qualified | boolean | Whether the TikTok Shop is available for GMV Max. Enum values: `true`, `false`. |
| data.list[].is_owner_sc | string | The ad Business Center owns the TikTok Shop. The ad account that has access to the TikTok Shop does not need to verify the TikTok Shop. |
| data.list[].store_authorized_bc_GM | string | Information about the Business Center that is authorized to grant the TikTok Shop. |
| data.list[].bc_id | string | The ID of the Business Center. |

---

## 12. Check the Availability of a TikTok Shop for Product GMV Max Campaigns

**Description:** Use this endpoint to check whether a TikTok Shop has been assigned by another Video Shopping Ad or Product Shopping Ad, and whether the TikTok Shop can be used to create Product GMV Max Campaigns by promoting all products in the TikTok Shop.

**Method:** `GET`

**Endpoint:** `https://business-api.tiktok.com/open_api/v1.3/gmv_max/shop/availability/get_usage_check/`

### Headers

| Field | Data Type | Required | Description |
|-------|-----------|----------|-------------|
| Access-Token | string | Required | Authorized access token. For details, see Authentication. |

### Parameters

| Field | Data Type | Required | Description |
|-------|-----------|----------|-------------|
| advertiser_id | string | Required | Advertiser ID. |
| shop_id | string | Required | The ID of the TikTok Shop. To obtain a TikTok Shop that is available for GMV Max Campaigns, use `store_authorized_bc_id` and confirm that the resource is a `gmv_max_qualified` or shop. |

### Response Fields

| Field | Type | Description |
|-------|------|-------------|
| code | integer | Response code. For the complete list of response codes and descriptions, see Response Status Code. |
| message_id | string | Response message. For details, see Response Status Code. |
| request_id | string | Request ID. |
| data | object | Response data. |
| data.gmv_max_products_allowed | boolean | Whether the TikTok Shop can be used to create Product GMV Max Campaigns by promoting all products in the TikTok Shop. |
| data.is_running_catalog_cross_sale | boolean | Whether the TikTok Shop is being used to create a Video Shopping Ad or Product Shopping Ad. Supported values: `true`, `false`. |

### Response Example

```json
{
  "code": 0,
  "data": {
    "is_running_catalog_cross_sale": true,
    "gmv_max_products_allowed": false
  }
}
```

---

## 13. Get Identities for GMV Max Campaigns

**Description:** Use this endpoint to obtain a list of identities that are associated with a TikTok Shop, and whether the identities are suitable for GMV Max Campaigns.

**Method:** `GET`

**Endpoint:** `https://business-api.tiktok.com/open_api/v1.3/gmv_max/identity/get/`

### Headers

| Field | Data Type | Required | Description |
|-------|-----------|----------|-------------|
| Access-Token | string | Required | Authorized access token. For details, see Authentication. |

### Parameters

| Field | Data Type | Required | Description |
|-------|-----------|----------|-------------|
| advertiser_id | string | Required | The ID of the TikTok Shop. |
| shop_id | string | Required | To obtain a TikTok Shop that is available for GMV Max Campaigns, use `store_authorized_bc_id` and confirm that the resource is a `gmv_max_qualified`. |
| store_authorized_bc_id | string | Required | ID of the Business Center that is authorized to access the TikTok Shop. |

### Response Fields

| Field | Type | Description |
|-------|------|-------------|
| code | integer | Response code. For the complete list of response codes and descriptions, see Response Status Code. |
| message | string | Response message. |
| request_id | string | Request ID. |
| data | object | Response data. |
| data.list | array | List of identities. |
| data.list[].identity_id | string | Identity ID. An ID of identity/entities used for the ad. |
| data.list[].identity_type | string | Identity type. Enum values: `CUSTOMIZED_USER` (Authorized user, the type of identity to indicate when you set up the combination items in a TikTok ad account or TikTok Business Account), `TT_USER` (TikTok user, the type of identity to indicate when you use your TikTok personal account, which has direct access to your Business Center), `BC_AUTH_TT` (Business authorized TikTok user, the type of identity to create video using your official TikTok account for TikTok Shop). |

---

## 14. Check the Occupancy of Identities or Products in Shopping Ads

**Description:** Use this endpoint to check whether an identity or a product has been occupied by another Shopping Ads (Video Shopping Ad, Product Shopping Ad, or Live Shopping Ad).

**Method:** `GET`

**Endpoint:** `https://business-api.tiktok.com/open_api/v1.3/gmv_max/creative/identity_product_check/`

### Headers

| Field | Data Type | Required | Description |
|-------|-----------|----------|-------------|
| Access-Token | string | Required | Authorized access token. For details, see Authentication. |

### Parameters

| Field | Data Type | Required | Description |
|-------|-----------|----------|-------------|
| advertiser_id | string | Required | Advertiser ID. |
| shop_id | string | Required | To obtain a TikTok Shop that is available for GMV Max Campaigns, use `store_authorized_bc_id` and confirm that the resource is a `gmv_max_qualified` or `shop`. |
| creator_check_type | string | Required | The type of check that you want to run for occupancy or availability within Shopping Ads for Product Shopping Ad or Live Shopping Ad. Enum values: `PRODUCT_CHECK` (TikTok Shop), `IDENTITY_CHECK` (identity), `PRODUCT_IDENTITY_CHECK` (TikTok Shop and identity combined). |
| product_source_page_ids | string[] | Optional | Product source page IDs. |
| creator_related_product_ids | string[] | Optional | IDs of products to check occupancy for. When `creator_check_type` is `IDENTITY_CHECK`, specify the `IDENTITY_ID`, `IDENTITY_TYPE`, etc. When it is `PRODUCT_CHECK`, specify the product IDs. |

### Response Fields

| Field | Type | Description |
|-------|------|-------------|
| code | integer | Response code. For the complete list of response codes and descriptions, see Response Status Code. |
| message | string | Response message. |
| request_id | string | Request ID. |

---

## 15. Get Posts for a Product GMV Max Campaign

**Description:** Use this endpoint to retrieve the list of TikTok posts that are available for a Product GMV Max campaign using a specific TikTok Shop.

**Method:** `GET`

**Endpoint:** `https://business-api.tiktok.com/open_api/v1.3/gmv_max/creative/post/get/`

### Headers

| Field | Data Type | Required | Description |
|-------|-----------|----------|-------------|
| Access-Token | string | Required | Authorized access token. For details, see Authentication. |

### Parameters

| Field | Data Type | Required | Description |
|-------|-----------|----------|-------------|
| advertiser_id | string | Required | Advertiser ID. |
| shop_id | string | Required | To obtain a TikTok Shop that is available for GMV Max Campaigns, use `store_authorized_bc_id` and confirm that the resource is `gmv_max_qualified`. |
| store_authorized_bc_id | string | Required | ID of the Business Center that is authorized to access the TikTok Shop. |
| search_field | string | Optional | A list of fields with detailed description for the TikTok Shop in the Product GMV Max Campaign, and/or parameters posts. |
| search_value | string | Optional | A search value to search for a specific product from the TikTok Shop in the Product GMV Max Campaign using parameters posts, search for the value by the `item_id` and `item_name`. |
| use_creator | boolean | Optional | To use this feature, set to `true`. |
| latest_posts_category | string | Optional | |
| identity_type | string | Optional | |
| identity_id | string | Optional | |
| cursor | string | Optional | |
| page_size | integer | Optional | Page size for results for additional pagination. |
| sort_field | string | Optional | Supported values: `GMV`. |
| sort_type | string | Optional | Sort type values: `ASC`, `DESC`. |

### Response Fields

| Field | Type | Description |
|-------|------|-------------|
| code | integer | Response code. |
| message | string | Response message. |
| data | object | Response data. |
| data.list | array | List of posts. |
| data.list[].item_id | string | Item/product ID. |
| data.list[].post_info | object | Post information. |

---

## 16. Get Details of Videos in Customized Posts

**Description:** Use this endpoint to retrieve the details of videos that have been used in the customized post collection for a Product GMV Max Campaign.

**Method:** `GET`

**Endpoint:** `https://business-api.tiktok.com/open_api/v1.3/gmv_max/creative/video_detail/get/`

### Headers

| Field | Data Type | Required | Description |
|-------|-----------|----------|-------------|
| Access-Token | string | Required | Authorized access token. For details, see Authentication. |

### Parameters

| Field | Data Type | Required | Description |
|-------|-----------|----------|-------------|
| advertiser_id | string | Required | Advertiser ID. |
| campaign_id | string | Required | The ID of a GMV Max Campaign. |
| shopping_ads_type | string | Required | **Important:** `shopping_ads_type` (`LIVE`, `PRODUCT`) must be mapped to campaign settings by API. To filter a default API integration, use `advertiser_id` and a `page_id` configuration, to specify this parameter as TikTok post. |
| customized_creative_posts_video_ids | string[] | Required | The IDs of the customized post collection(s) associated with a Product GMV Max Campaign, use `campaign/creative/video/create` and obtain the created video IDs. |
| creator_content_video_ids | string[] | Optional | To obtain the customized post associated with a Product GMV Max Campaign, use `campaign/creative/post` and obtain the video/creative IDs. |
| creative_ids | string[] | Optional | The ID of the customized post associated (with this post). |
| identity_id | string | Optional | Identity ID. |
| identity_type | string | Optional | Allowed values: `CUSTOMIZED_USER` (this type of Identity to customize/post, set the combination items in a TikTok ad account or TikTok Business Account), `TT_USER` (this type is available when you use your TikTok personal account with Live TikTok accounts resource, to match various apps within the TikTok business account, and also apps on the TikTok accounts), `BC_AUTH_TT` (Business authorized TikTok user. The account will define to create video using an official TikTok account for the TikTok Shop. The `BC_AUTH_TT` would provide access to you). |
| product_customized_id | string | Optional | |
| product_customized_blog_id | string | Optional | The ID of the TikTok Shop that a TikTok post is linked to via product details, customizable in the app. |

### Response Fields

| Field | Type | Description |
|-------|------|-------------|
| code | integer | Response code. |
| message | string | Response message. |
| data | object | Response data. |
| data.list | array | Video details list. |

---

## 17. Remove or Add Back Creatives in a GMV Max Campaign

**Description:** Use this endpoint to either remove creatives (videos) from a Product or Live GMV Max Campaign or to restore creatives (add back previously removed).

**Method:** `POST`

**Endpoint:** `https://business-api.tiktok.com/open_api/v1.3/gmv_max/creative/manage/`

### Headers

| Field | Data Type | Required | Description |
|-------|-----------|----------|-------------|
| Access-Token | string | Required | Authorized access token. For details, see Authentication. |
| Content-Type | string | Required | `application/json` |

### Parameters

| Field | Data Type | Required | Description |
|-------|-----------|----------|-------------|
| advertiser_id | string | Required | Advertiser ID. |
| campaign_id | string | Required | This parameter must refer to an active status. An active status GMV Max campaign is one that all services can see via `campaign/get/detail`. |
| shopping_ads_type | string | Required | If the campaign is a PRODUCT GMV Max campaign, use `Creative.Create` inventory type. If the campaign build ID is the campaign build ID, use `PRODUCT` and `LIVE`. |
| action | enum | Required | The type of action to perform. Enum values: `REMOVE` (to remove creatives from a GMV Max campaign), `RESTORE` (to add back creatives). |
| item_ids | string[] | Optional | One action at a time: remove or add. Items in a remove/restore action must already have creatives that the campaign was previously linked with. The list of TikTok post/video IDs to be removed/re-added. |
| video_ids | string[] | Optional | This endpoint allows for the removal of up to 10,000 posts from a GMV Max Campaign, with a limit of 400 posts per request. For example, if you had to include 800 profiles and a first request with 400 IDs in the body, followed by a second request with the remaining 400. |

### Response Fields

| Field | Type | Description |
|-------|------|-------------|
| code | integer | Response code. |
| message | string | Response message. |
| data | object | Response data. |
| data.video_ids | string[] | List of video IDs. |
| data.op_id | integer | The ID of the query. |

---

## 18. Get the TikTok Shop Exclusive Authorization Status of an Ad Account

**Description:** Use this endpoint to check whether an ad account is exclusively authorized to create GMV Max Campaigns for a specific TikTok Shop.

**Method:** `GET`

**Endpoint:** `https://business-api.tiktok.com/open_api/v1.3/gmv_max/monetization_exclusive/get/`

### Headers

| Field | Data Type | Required | Description |
|-------|-----------|----------|-------------|
| Access-Token | string | Required | Authorized access token. For details, see Authentication. |

### Parameters

| Field | Data Type | Required | Description |
|-------|-----------|----------|-------------|
| shop_id | string | Required | The ID of the TikTok Shop. To obtain a TikTok Shop that is available for GMV Max Campaigns, use `store_authorized_bc_id` and confirm the resource is `gmv_max_qualified` or `shop`. |
| store_authorized_bc_id | string | Required | ID of the Business Center that is authorized to access the TikTok Shop. |
| advertiser_id | string | Required | ID of the ad account that you want to check for GMV Max exclusive authorization status for. |

### Response Fields

| Field | Type | Description |
|-------|------|-------------|
| code | integer | Response code. For the complete list of response codes and descriptions, see Response Status Code. |
| message | string | Response message. |
| request_id | string | The ID of a request, which uniquely identifies the request. |
| data | object | Response data. |
| data.shop_id | string | TikTok Shop ID. |
| data.advertiser_id | string | The ID of the ad account. |
| data.authorization_status | string | The exclusive authorization status for ad account to create GMV Max for the TikTok Shop. Enum values: `AUTHORIZED` (the ad account is currently granted exclusive right to the campaign with the authorization status being activated), `UNAUTHORIZED` (the ad account has been denied and/or this resource/campaign has not been authorized for operation). |
| data.authorization_owner | string | The owner of the ad account. If authorized (`AUTHORIZED`), the field is an ad account. |

---

## 19. Grant an Ad Account Exclusive Authorization for a TikTok Shop

**Description:** Use this endpoint to authorize an ad account to create GMV Max Campaigns for a specific TikTok Shop.

> For each TikTok Shop, only one ad account can be authorized to create GMV Max Campaigns using the TikTok Shop for authorized revenue and sales campaigns.

> **Important:** By using this endpoint, you agree to our partnerships for exclusively linked sellers for this GMV Max automation.

**Method:** `POST`

**Endpoint:** `https://business-api.tiktok.com/open_api/v1.3/gmv_max/monetization_exclusive/grant/exclusive/`

### Headers

| Field | Data Type | Required | Description |
|-------|-----------|----------|-------------|
| Access-Token | string | Required | Authorized access token. For details, see Authentication. |
| Content-Type | string | Required | `application/json` |

### Parameters

| Field | Data Type | Required | Description |
|-------|-----------|----------|-------------|
| shop_id | string | Required | The ID of the TikTok Shop. To obtain a TikTok Shop that is available for GMV Max Campaigns, use `store_authorized_bc_id` and confirm that the resource is a `gmv_max_qualified` or `shop`. |
| store_authorized_bc_id | string | Required | To confirm that a Business Center exists for a TikTok Shop, use `store_authorized_bc_id` and verify whether the resource is a `gmv_max_qualified`. |
| advertiser_id | string | Required | The ID of the ad account that you want to exclusively authorize to create GMV Max Campaigns for the TikTok Shop. The ID of the ad account (which is authorized) needs to be verified via get `exclusive_authorization` API. |

### Response Fields

| Field | Type | Description |
|-------|------|-------------|
| code | integer | Response code. For the complete list of response codes and descriptions, see Response Status Code. |
| message | string | Response message. |
| request_id | string | The ID of a request, which uniquely identifies the request. |

---

## 20. Run a GMV Max Campaign Report

**Description:** Use this endpoint to run a report on GMV Max Campaigns.

> **Note:** All response data includes yesterday's cumulative campaign data.

### Rate Limits

| Rate limit level | Query per Second (QPS) | Query per Minute (QPM) | Query per Day (QPD) |
|---|---|---|---|
| Application | 10 | 600 | 86,400 |
| Advertiser | 5 | 300 | - |

**Method:** `GET`

**Endpoint:** `https://business-api.tiktok.com/open_api/v1.3/gmv_max/report/get/`

### Headers

| Field | Data Type | Required | Description |
|-------|-----------|----------|-------------|
| Access-Token | string | Required | Authorized access token. For details, see Authentication. |

### Parameters

| Field | Data Type | Required | Description |
|-------|-----------|----------|-------------|
| advertiser_id | string | Required | Advertiser ID. |
| shop_id | string | Required | To obtain a TikTok Shop that is available for GMV Max Campaigns, use `store_authorized_bc_id` and confirm that the resource is a `gmv_max_qualified` or `shop`. The data is linked to the session_id for the Products or live. |
| start_date | string | Required | Start date for the report. Format: `YYYY-MM-DD`. This is the date when it references fields to the Product GMV Max Campaign and Live GMV Max Campaign as confirmed. |
| end_date | string | Required | End date for the report. |
| filtering | object | Optional | Filtering criteria. |
| data_level | string | Required | Data level for the report. |
| page | integer | Optional | Page number. |
| page_size | integer | Optional | Page size. |

### Response Fields

| Field | Type | Description |
|-------|------|-------------|
| code | integer | Response code. |
| message | string | Response message. |
| request_id | string | Request ID. |
| data | object | Response data. |
| data.list | array | List of report entries. |
| data.page_info | object | Pagination info. |

---

## Summary Table

| # | API Name | Method | Endpoint Path |
|---|----------|--------|---------------|
| 1 | Get GMV Max Campaigns | GET | `/v1.3/gmv_max/campaign/get/` |
| 2 | Get Campaign Detail | GET | `/v1.3/gmv_max/campaign/get_detail/` |
| 3 | Create Campaign | POST | `/v1.3/gmv_max/campaign/create/` |
| 4 | Update Campaign | POST | `/v1.3/gmv_max/campaign/update/` |
| 5 | Get Recommended ROI | GET | `/v1.3/gmv_max/campaign/recommended/` |
| 6 | Create Boost Session | POST | `/v1.3/gmv_max/campaign/max_session/create/` |
| 7 | Update Boost Session | POST | `/v1.3/gmv_max/campaign/max_session/update/` |
| 8 | Get Boost Sessions | GET | `/v1.3/gmv_max/campaign/max_session/get/` |
| 9 | Get Boost Detail | GET | `/v1.3/gmv_max/campaign/max_session/detail/` |
| 10 | Delete Boost Session | POST | `/v1.3/gmv_max/campaign/max_session/delete/` |
| 11 | Get Shops | GET | `/v1.3/gmv_max/shop/get/` |
| 12 | Check Shop Availability | GET | `/v1.3/gmv_max/shop/availability/get_usage_check/` |
| 13 | Get Identities | GET | `/v1.3/gmv_max/identity/get/` |
| 14 | Check Occupancy | GET | `/v1.3/gmv_max/creative/identity_product_check/` |
| 15 | Get Posts | GET | `/v1.3/gmv_max/creative/post/get/` |
| 16 | Get Video Details | GET | `/v1.3/gmv_max/creative/video_detail/get/` |
| 17 | Manage Creatives | POST | `/v1.3/gmv_max/creative/manage/` |
| 18 | Get Exclusive Auth | GET | `/v1.3/gmv_max/monetization_exclusive/get/` |
| 19 | Grant Exclusive Auth | POST | `/v1.3/gmv_max/monetization_exclusive/grant/exclusive/` |
| 20 | Run Report | GET | `/v1.3/gmv_max/report/get/` |
