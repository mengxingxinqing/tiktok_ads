# Get TikTok Shops for GMV Max Campaigns

**Doc ID**: 1822001044479041
**Path**: API Reference/GMV Max/Get TikTok Shops for GMV Max Campaigns

---

Use this endpoint to obtain a list of TikTok Shops that an ad account has access to and whether the TikTok Shops can be used to create GMV Max Campaigns.

## Request

**Endpoint** https://business-api.tiktok.com/open_api/v1.3/gmv_max/store/list/

**Method** GET

**Header**

```xtable
|Field{35%}|Data Type{12%}|Description{53%}|
|---|---|---|
|Access-Token {Required}|string|Authorized access token.
 For details, see [Authentication](https://business-api.tiktok.com/portal/docs?id=1738373164380162).|
```

**Parameters**

``` xtable
|Field{35%}|Data Type{12%}|Description{53%}|
|--- |--- |--- |
| advertiser_id {Required} | string | Advertiser ID. |
```

### Example
```xcodeblock
(code curl http)
curl --location  --request GET 'https://business-api.tiktok.com/open_api/v1.3/gmv_max/store/list/?advertiser_id={{advertiser_id}}' \
--header 'Access-Token: {{Access-Token}}' 
(/code)
```
## Response

``` xtable
|Field{35%}|Type{12%}|Description{53%}|
|---|---|---|
|code |number|Response code. For the complete list of response codes and descriptions, see [Appendix-Return Code](https://ads.tiktok.com/marketing_api/docs?id=1737172488964097). |
|message|string|Response message. For details, see [Appendix - Return Codes](https://ads.tiktok.com/marketing_api/docs?id=1737172488964097).|
|request_id |string|The log ID of a request, which uniquely identifies the request.  |
|data |object|Returned data.|
#| store_list | object[] | The list of TikTok Shops that the ad account has access to. |
##| store_id | string | ID of the TikTok Shop. |
##| is_gmv_max_available | boolean | Whether the TikTok Shop is available for GMV Max Campaigns. 

 Supported values: 
- `true`: available.
- `false`: unavailable. |
##| store_authorized_bc_id | string | ID of the Business Center that is authorized to access the TikTok Shop (`store_id`). |
##| is_owner_bc | boolean | Whether the Business Center (`store_authorized_bc_id`) owns the TikTok Shop (`store_id`). 

Supported values:
- `true`: The Business Center owns the TikTok Shop.
-  `false`: The Business Center is a Partner Business Center that has access to the TikTok Shop and does not own the TikTok Shop.|
##| store_authorized_bc_info | object | Information about the Business Center that is authorized to access the TikTok Shop. |
###| bc_id | string | The ID of the Business Center. |
###| bc_profile_image | string | The profile image URL of the Business Center. |
###| bc_name | string | The name of the Business Center. |
###| user_role| string | The role of the user (member) within the Business Center.

 Enum values: 
- `ADMIN`: Admin. Admins have full access to all features in Business Center. 
- `STANDARD`: Standard. Standard members can only work on accounts they've been assigned to.|
##| thumbnail_url | string | The thumbnail URL of the TikTok Shop. |
##| store_name | string | The name of the TikTok Shop. |
##| store_code| string | The shop code of the TikTok Shop. |
##| targeting_region_codes | string[] | The codes of the regions that the TikTok Shop can target. 

  To find out the region that a region code corresponds to, see [Appendix-Location code](https://business-api.tiktok.com/portal/docs?id=1737585867307010). 

 For example, `VN` corresponds to Vietnam. |
##| store_status | string | The status of the TikTok Shop. 

 Enum values:
- `ACTIVE`: active. 
- `INACTIVE`: inactive.
- `NEW_CREATE`: newly created.|
##| store_role | string | Business Center user's permission to the TikTok Shop.

Enum values: 
- `AD_PROMOTION`: Ad promotion. Create ads promoting products from this TikTok Shop.
- `MANAGER`: Manager. Manage stores and related catalogs and view data insights in Store Manager.
- `UNSET`: Unset.|
##| exclusive_authorized_advertiser_info | object | Information about the GMV Max exclusive authorization of the TikTok Shop. |
###| advertiser_id | string | The ID of the only ad account that is authorized to create GMV Max Campaigns for the TikTok Shop. |
###| advertiser_name | string | The name of the only ad account that is authorized to create GMV Max Campaigns for the TikTok Shop. |
###| advertiser_status | string | The status of the only ad account that is authorized to create GMV Max Campaign for the TikTok Shop. 

 Enum values:
- `STATUS_ENABLE`: Approved.
- `STATUS_CONFIRM_FAIL`: Not approved.
- `STATUS_PENDING_CONFIRM`: In review.
- `STATUS_LIMIT`: Suspended.
- `STATUS_CONTRACT_PENDING`: Contract has not taken effect.
- `STATUS_DISABLE`: Disabled.
- `STATUS_PENDING_CONFIRM_MODIFY`: Modifications pending review.
- `STATUS_PENDING_VERIFIED`: Pending verification.
- `STATUS_SELF_SERVICE_UNAUDITED`: Pending verification of qualifications for the self-service account.
-  `STATUS_WAIT_FOR_BPM_AUDIT`: Pending CRM system review.
- `STATUS_CONFIRM_FAIL_END`: CRM system review failed.
- `STATUS_CONFIRM_MODIFY_FAIL`: Review of modifications failed. |
```

### Example
```xcodeblock
(code Success-Response http)
HTTPS/1.1 200 OK
{
    "code": 0,
    "message": "OK",
    "request_id": "{{request_id}}",
    "data": {
        "store_list": [
            {
                "exclusive_authorized_advertiser_info": {
                    "advertiser_id": "{{advertiser_id}}",
                    "advertiser_name": "{{advertiser_name}}",
                    "advertiser_status": "STATUS_ENABLE"
                },
                "is_gmv_max_available": false,
                "is_owner_bc": true,
                "store_authorized_bc_id": "{{store_authorized_bc_id}}",
                "store_authorized_bc_info": {
                    "bc_id": "{{bc_id}}",
                    "bc_name": "{{bc_name}}",
                    "bc_profile_image": "{{bc_profile_image}}",
                    "user_role": "ADMIN"
                },
                "store_code": "{{store_code}}",
                "store_id": "{{store_id}}",
                "store_name": "{{store_name}}",
                "store_role": "AD_PROMOTION",
                "store_status": "ACTIVE",
                "targeting_region_codes": [
                    "ID"
                ],
                "thumbnail_url": "{{thumbnail_url}}"
            },
            {
                "exclusive_authorized_advertiser_info": {
                    "advertiser_id": "{{advertiser_id}}",
                    "advertiser_name": "{{advertiser_name}}",
                    "advertiser_status": "STATUS_ENABLE"
                },
                "is_gmv_max_available": true,
                "is_owner_bc": true,
                "store_authorized_bc_id": "{{store_authorized_bc_id}}",
                "store_authorized_bc_info": {
                    "bc_id": "{{bc_id}}",
                    "bc_name": "{{bc_name}}",
                    "bc_profile_image": "{{bc_profile_image}}",
                    "user_role": "ADMIN"
                },
                "store_code": "{{store_code}}",
                "store_id": "{{store_id}}",
                "store_name": "{{store_name}}",
                "store_role": "AD_PROMOTION",
                "store_status": "ACTIVE",
                "targeting_region_codes": [
                    "ID"
                ],
                "thumbnail_url": "{{thumbnail_url}}"
            },
            {
                "exclusive_authorized_advertiser_info": {
                    "advertiser_id": "{{advertiser_id}}",
                    "advertiser_name": "{{advertiser_name}}",
                    "advertiser_status": "STATUS_ENABLE"
                },
                "is_gmv_max_available": true,
                "is_owner_bc": false,
                "store_authorized_bc_id": "{{store_authorized_bc_id}}",
                "store_authorized_bc_info": {
                    "bc_id": "{{bc_id}}",
                    "bc_name": "{{bc_name}}",
                    "bc_profile_image": "{{bc_profile_image}}",
                    "user_role": "ADMIN"
                },
                "store_code": "{{store_code}}",
                "store_id": "{{store_id}}",
                "store_name": "{{store_name}}",
                "store_role": "AD_PROMOTION",
                "store_status": "ACTIVE",
                "targeting_region_codes": [
                    "MY"
                ],
                "thumbnail_url": "{{thumbnail_url}}"
            },
            {
                "exclusive_authorized_advertiser_info": {
                    "advertiser_id": "{{advertiser_id}}",
                    "advertiser_name": "{{advertiser_name}}",
                    "advertiser_status": "STATUS_ENABLE"
                },
                "is_gmv_max_available": false,
                "is_owner_bc": false,
                "store_authorized_bc_id": "{{store_authorized_bc_id}}",
                "store_authorized_bc_info": {
                    "bc_id": "{{bc_id}}",
                    "bc_name": "{{bc_name}}",
                    "bc_profile_image": "{{bc_profile_image}}",
                    "user_role": "ADMIN"
                },
                "store_code": "{{store_code}}",
                "store_id": "{{store_id}}",
                "store_name": "{{store_name}}",
                "store_role": "AD_PROMOTION",
                "store_status": "ACTIVE",
                "targeting_region_codes": [
                    "ID"
                ],
                "thumbnail_url": "{{thumbnail_url}}"
            }
        ]
    }
}
(/code)
```
