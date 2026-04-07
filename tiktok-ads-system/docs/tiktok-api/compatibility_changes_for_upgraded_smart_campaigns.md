# Compatibility changes for Upgraded Smart+ Campaigns

**Doc ID**: 1854112742370306
**Path**: Marketing API/Campaign Management/Guides/Campaign/Upgraded Smart+ Campaign/Compatibility changes for Upgraded Smart+ Campaigns

---

The following table outlines the compatibility changes for Upgraded Smart+ Campaigns in various endpoints.

  
    
| 
      Module | 
      Endpoints | 
      Main Compatibility Changes | 
     |
  
  
    
| 
      Campaign | 
      [/campaign/get/](https://business-api.tiktok.com/portal/docs?id=1739315828649986) | 
      
- Upgraded Smart+ Campaigns are returned by default.
- The `campaign_automation_type` parameter is available in the request and response for retrieving campaign types, including Manual, Smart+, and Upgraded Smart+ campaigns. | 
     |
    
| 
      [/campaign/create/](https://business-api.tiktok.com/portal/docs?id=1739318962329602) | 
      You cannot use these endpoints to create, update or copy an Upgraded Smart+ Campaign.
Use [Upgraded Smart+ Campaigns endpoints](https://business-api.tiktok.com/portal/docs?id=1843310518576130) instead. | 
     |
    
| 
      [/campaign/update/](https://business-api.tiktok.com/portal/docs?id=1739320422086657) | 
     |
    
| 
      [/campaign/copy/task/create/](https://business-api.tiktok.com/portal/docs?id=1788434394151938) | 
     |
    
| 
      Ad group | 
      [/adgroup/get/](https://business-api.tiktok.com/portal/docs?id=1739314558673922) | 
      
- Upgraded Smart+ Ad Groups are returned by default.
- The `campaign_automation_type` parameter is available in the request and response so you can tell whether an ad group belongs to a Manual, a Smart+, or an Upgraded Smart+ Campaign. | 
     |
    
| 
      [/adgroup/create/](https://business-api.tiktok.com/portal/docs?id=1739499616346114) | 
      You cannot use these endpoints to create or update an Upgraded Smart+ Ad Group.
Use [Upgraded Smart+ Ad Groups endpoints](https://business-api.tiktok.com/portal/docs?id=1843310524500993) instead. | 
     |
    
| 
      [/adgroup/update/](https://business-api.tiktok.com/portal/docs?id=1739586761631745) | 
     |
    
| 
     |
    
| 
      [/adgroup/budget/update/](https://business-api.tiktok.com/portal/docs?id=1739591133130817) | 
     |
    
| 
      Ad | 
      [/ad/get/](https://business-api.tiktok.com/portal/docs?id=1735735588640770) | 
      
- You can retrieve Upgraded Smart+ Ads. 
- The `campaign_automation_type` parameter is available in the request and response for retrieving campaign types that the ads belong to, including Manual, Smart+, and Upgraded Smart+ Campaigns.
- You can retrieve the ad ID of Upgraded Smart+ Ads through the new response parameter `smart_plus_ad_id`.
- You can use the `ad_ids_v2` filter to efficiently filter ads across Manual, Smart+, and Upgraded Smart+ Campaigns, ensuring focused analysis.
- Use the `ad_id_v2` response parameter to identify specific ads within Manual, Smart+, and Upgraded Smart+ Campaigns with ease.
- The new enum value `UPGRADED_SMART_PLUS` for the `campaign_automation_type` response parameter helps you distinguish ads within Upgraded Smart+ Campaigns, aiding in targeted analysis. | 
     |
    
| 
      [/ad/create/](https://business-api.tiktok.com/portal/docs?id=1739953377508354) | 
      You cannot use these endpoints to create or update an Upgraded Smart+ Ad.
Use [Upgraded Smart+ Ads endpoints](https://business-api.tiktok.com/portal/docs?id=1843310530260097) instead. | 
     |
    
| 
      [/ad/update/](https://business-api.tiktok.com/portal/docs?id=1739953405142018) | 
     |
	
| 
      Ads Preview | 
      [/creative/ads_preview/create/](https://business-api.tiktok.com/portal/docs?id=1739403070695426) | 
      You cannot use this endpoint to preview Upgraded Smart+ Ads.
Use [/smart_plus/ad/preview/](https://business-api.tiktok.com/portal/docs?id=1843317445798914) instead. | 
     |
    
| 
      Smart Creative | 
      [/ad/aco/create/](https://business-api.tiktok.com/portal/docs?id=1739473063234626) | 
      You cannot use these endpoints to create or update Smart Creative ads using Upgraded Smart+ Ad Groups. | 
     |
    
| 
      [/ad/aco/update/](https://business-api.tiktok.com/portal/docs?id=1739473077112833) | 
     |
    
| 
      [/ad/aco/material_status/update/](https://business-api.tiktok.com/portal/docs?id=1739506701165570) | 
     |
    
| 
      Smart+ | 
      [/campaign/spc/create/](https://business-api.tiktok.com/portal/docs?id=1767334204047362) | 
      You cannot use these endpoints to create, update, or retrieve Upgraded Smart+ Campaigns.
Use [Upgraded Smart+ Campaigns endpoints](https://business-api.tiktok.com/portal/docs?id=1843310518576130) instead. | 
     |
	
| 
      [/campaign/spc/update/](https://business-api.tiktok.com/portal/docs?id=1767334250066945) | 
     |
    
| 
      [/campaign/spc/get/](https://business-api.tiktok.com/portal/docs?id=1767334299811842) | 
     |
    
| 
      [/campaign/spc/material_status/update/](https://business-api.tiktok.com/portal/docs?id=1837969177953361) | 
     |
	    
| 
      Reporting | 
      [/report/integrated/get/](https://business-api.tiktok.com/portal/docs?id=1740302848100353) | 
      
- By default, the data for creatives in Upgraded Smart+ Ads is included.
- You **can** get Upgraded Smart+ Ads data (with `ad_id` representing the creative ID) when you use the `ad_ids` filter, specify `ad_id` in `dimensions`, or set `data_level` to `AUCTION_AD`.
- The `ad_id_v2` dimension is now available to group ads across Manual, Smart+, and Upgraded Smart+ Campaigns. This allows for a more refined analysis of your advertising efforts.
- Gain deeper insights with these attribute metrics associated with the `ad_id_v2` dimension:`ad_id_v2`
- `ad_text_list`
- `call_to_action_list`
- `ad_profile_image_list`
- `ad_url_list`
- `image_mode_list`
- `image_info_list`
- `ad_display_name_list`
- `identity_type_list`
- `profile_image_list`
- Use the filters `ad_id_v2` and `campaign_automation_type` to efficiently filter data across Manual, Smart+, and Upgraded Smart+ Campaigns, ensuring focused analysis. | 
     |
    
| 
      [/report/task/create/](https://business-api.tiktok.com/portal/docs?id=1740302766489602) | 
     |
    
| 
      [/campaign/spc/report/get/](https://business-api.tiktok.com/portal/docs?id=1776454619412481) | 
      You cannot use this endpoint to get the reporting data on creatives within Upgraded Smart+ Ads.
Use [/smart_plus/material_report/overview/](https://business-api.tiktok.com/portal/docs?id=1843317489576961) or [/smart_plus/material_report/breakdown/](https://business-api.tiktok.com/portal/docs?id=1843317510389761) instead. | 
     |
	
| 
      Creative Report | 
      [/report/ad_benchmark/get/](https://business-api.tiktok.com/portal/docs?id=1738824501176321) | 
      You cannot use these endpoints to get Creative Report data for Upgraded Smart+ Ads. | 
     |
    
| 
      [/report/video_performance/get/](https://business-api.tiktok.com/portal/docs?id=1738825259075586) | 
     |
	
| 
      Reach & Frequency | 
      [/adgroup/rf/create/](https://business-api.tiktok.com/portal/docs?id=1738235338194945) | 
      You cannot use these endpoints to create, update, cancel, or get the estimated daily cost and frequency distribution for an Upgraded Smart+ ad group. | 
     |
    
| 
      [/adgroup/rf/update/](https://business-api.tiktok.com/portal/docs?id=1738235402874882) | 
     |
    
| 
      [/adgroup/rf/order/cancel/](https://business-api.tiktok.com/portal/docs?id=1740489099367425) | 
     |
    
| 
      [/adgroup/rf/estimated/info/](https://business-api.tiktok.com/portal/docs?id=1740489551354881) | 
     |
    
| 
      Tools | 
      [/delivery/budget/recommend/](https://business-api.tiktok.com/portal/docs?id=1746463695763458) | 
      You cannot use these endpoints to get budget and bid estimated delivery results for Upgraded Smart+ Ad Groups. | 
     |
    
| 
      [/delivery/bid/recommend/](https://business-api.tiktok.com/portal/docs?id=1746463732779009) | 
     |
	
| 
	  [/tool/vbo_status/](https://business-api.tiktok.com/portal/docs?id=1770016073586753) | 
      You can check the Value-Based Optimization eligibility of settings for creating [Upgraded Smart+ Minis Campaigns](https://business-api.tiktok.com/portal/docs?id=1853377811982657) via the `campaign_automation_type` parameter and the `MINIS` value for the request parameter `app_promotion_type`. | 
	 |
    
| 
      Subscription | 
      [/subscription/subscibe/](https://business-api.tiktok.com/portal/docs?id=1739092028876801) | 
      You cannot use this endpoint to subscribe to review or fatigue status events for Upgraded Smart+ Ad Groups or Ads. | 
     |
    
| 
      Ad Diagnosis | 
      [/tool/diagnosis/get/](https://business-api.tiktok.com/portal/docs?id=1738674986981378) | 
      You cannot use this endpoint to get diagnoses for Upgraded Smart+ Ad Groups. | 
     |
    
| 
      Ad Comment | 
      [/comment/list/](https://business-api.tiktok.com/portal/docs?id=1738086301876225) | 
      You cannot get the ad ID, ad name, ad group ID, and ad group name for a comment on an Upgraded Smart+ Ad. | 
     |
    
| 
      [/comment/post/](https://business-api.tiktok.com/portal/docs?id=1738957702411265) | 
      You cannot use these endpoints to:
- Reply to a comment on an Upgraded Smart+ Ad,
- Delete a comment from an Upgraded Smart+ Ad, or
- Create a comment export task for an Upgraded Smart+ Ad Group | 
     |
    
| 
      [/comment/delete/](https://business-api.tiktok.com/portal/docs?id=1738957772267522) | 
     |
    
| 
      [/comment/task/create/](https://business-api.tiktok.com/portal/docs?id=1738088144215041) | 
     |
    
| 
      Automated Rules | 
      [/optimizer/rule/create/](https://business-api.tiktok.com/portal/docs?id=1738767670852610) | 
      You cannot use these endpoints to:
- Create automated rules for Upgraded Smart+ Campaigns, Ad Groups, and Ads,
- Update automated rules for Upgraded Smart+ Campaigns, Ad Groups, and Ads, or
- Bind automated rules to or unbind automated rules from Upgraded Smart+ Campaigns, Ad Groups, and Ads | 
     |
    
| 
      [/optimizer/rule/batch_bind/](https://business-api.tiktok.com/portal/docs?id=1738769164954626) | 
     |
    
| 
      [/optimizer/rule/update/](https://business-api.tiktok.com/portal/docs?id=1738769123170306) | 
     |
    
| 
      Creative Tools | 
      [/creative_fatigue/get/](https://business-api.tiktok.com/portal/docs?id=1767568466842626) | 
      You cannot use this endpoint to get Creative Fatigue Detection results for Upgraded Smart+ Ads. | 
     |
	 
| 
      Business Messaging | 
      [/business/message/conversation/list/](https://business-api.tiktok.com/portal/docs?id=1832184415059970) | 
      
- You can retrieve the IDs of creatives in Upgraded Smart+ Ads through the existing `ad_id` field.
- You can retrieve encoded creative IDs for Upgraded Smart+ Ads through the new `message_material_id` field. | 
     |
    
| 
      [Webhook schema for `im_referral_msg`](https://business-api.tiktok.com/portal/docs?id=1832190670631937#item-link-im_referral_msg) | 
      
- You can retrieve the IDs of creatives in Upgraded Smart+ Ads through the existing `ad_id` field.
- You can retrieve encoded creative IDs for Upgraded Smart+ Ads through the new `message_material_id` field. | 
     |
