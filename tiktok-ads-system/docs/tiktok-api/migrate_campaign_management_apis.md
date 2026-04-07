# Migrate Campaign Management APIs

**Doc ID**: 1749537346290689
**Path**: Overview/V1.3 updates/Migrate to v1.3/Migrate Campaign Management APIs

---

Please read the following guidance before you migrate your campaign management calls to v1.3.  

1. Use `/campaign/create/` to create a campaign.  See [Create a campaign - Comparing v1.2 and v1.3](https://ads.tiktok.com/marketing_api/docs?id=1739318962329602) for detailed changes, for example,  parameter name changes, data type changes and the full ad entity returned.  

2. Use `/adgroup/create/` to create an ad group. See [Create an ad group - Comparing v1.2 and v1.3](https://ads.tiktok.com/marketing_api/docs?id=1739499616346114) for detailed changes, for example, parameter name changes, data type changes,  and the full ad entity returned.  

>**Notes**

- **The enum value of `VIDEO_VIEW` is deprecated in the `optimization_goal` field.** We recommend that you use `ENGAGED_VIEW` or `ENGAGED_VIEW_FIFTEEN` (on allowlist) when `objective_type` is `VIDEO_VIEW` at the campaign level. 
- When `objective_type` is `VIDEO_VIEW` and `bid_type` is `BID_TYPE_CUSTOM`,  `bid_display_mode` is required and must be set to `CPV`(Cost per One View). **You can no longer use `CPMV` in the `bid_display_mode` field. ** 
-  **The `cpv_video_duration` field is deprecated. ** You can use the optimization goal of `ENGAGED_VIEW`(6-second views (Focused view)) or `ENGAGED_VIEW_FIFTEEN` (15-second views(Focused view), on allowlist) to specify your video play length. 
- **`pixel_id` can only be used for the advertising objectives of `CONVERSIONS`, `PRODUCT_SALES`.**  If you want to track events for other objectives, use `tracking_pixel_id` at the ad level. 

3. Use `/ad/create/` to create an ad.  See [Create ads - Comparing v1.2 and v1.3](https://ads.tiktok.com/marketing_api/docs?id=1739953377508354) for detailed changes, for example, parameter name changes, data type changes,  and the full ad entity returned.

>**Note**
 `identity_id` and `identity_type` are required. 

**OR** use `/ad/aco/create/` to create an automatic ad.  

>**Note**
[/ad/aco/create/](https://ads.tiktok.com/marketing_api/docs?id=1739473063234626) is a totally new endpoint in v1.3, and both `identity_id` and `identity_type` are required.
