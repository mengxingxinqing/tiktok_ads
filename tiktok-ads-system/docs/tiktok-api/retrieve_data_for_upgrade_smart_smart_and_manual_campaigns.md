# Retrieve data for Upgrade Smart+, Smart+, and Manual Campaigns

**Doc ID**: 1854103649826817
**Path**: Marketing API/Campaign Management/Guides/Campaign/Upgraded Smart+ Campaign/Retrieve data for Upgrade Smart+, Smart+, and Manual Campaigns

---

This guide provides an overview of data levels for three distinct campaign types: Manual Campaigns, Smart+ Campaigns, and Upgrade Smart+ Campaigns (also known as Upgraded Smart+ experience). It outlines detailed procedures to retrieve data for each of these campaign types, ensuring a comprehensive understanding of their structures.

# Overall data levels

Upgrade Smart+ Campaigns unify Manual and Smart+ experiences into a single streamlined process, offering a flexible ad buying experience. This enhancement allows for fine-tuning campaigns with various levels of control, including full automation, partial automation, or complete manual operation.

  
    
| 
      Data level | 
      Manual Campaign | 
      Smart+ Campaign | 
      Upgrade Smart+ Campaign | 
     |
  
  
    
| 
      Campaign | 
      ✅ | 
      ✅ | 
      ✅ | 
     |
    
| 
      Ad group | 
      ✅ | 
      ✅ | 
      ✅ | 
     |
    
| 
      Ad | 
      ✅ | 
      ⚠️ (returns limited data) | 
      ✅ | 
     |
    
| 
      Creative | 
      ❌ | 
      ✅ | 
      ✅ | 
     |
  

## Retrieve data for different campaign types
This section guides you through the process of retrieving data for Manual Campaigns, Smart+ Campaigns, and Upgrade Smart+ Campaigns separately.

## Data retrieval landscape

 

  
    
| 
      Automation Type | 
      **Get Endpoints** | 
      **Reporting API** | 
     |
    
| 
       | 
      Get Campaign | 
      Get Ad group | 
      Get Ad 
 (Asset Group in Upgraded Smart+) | 
      Get Creative | 
      Campaign | 
      Ad Group | 
      Ad
 (Asset Group in Upgraded Smart+) | 
      Creative | 
     |
  
  
    
| 
      **Manual Flow** | 
      ✅ [/campaign/get/](https://business-api.tiktok.com/portal/docs?id=1739315828649986) | 
      ✅ [/adgroup/get/](https://business-api.tiktok.com/portal/docs?id=1739314558673922) | 
      ✅ [/ad/get/](https://business-api.tiktok.com/portal/docs?id=1735735588640770) | 
      N/A | 
      ✅ [/report/integrated/get/](https://business-api.tiktok.com/portal/docs?id=1740302848100353)
Reporting API | 
      N/A | 
     |
    
| 
      **Smart+ API** | 
      ✅ [/campaign/get/](https://business-api.tiktok.com/portal/docs?id=1739315828649986)
✅ [/campaign/spc/get/](https://business-api.tiktok.com/portal/docs?id=1767334299811842) | 
      N/A
(there's no ad group in legacy Smart+ campaigns) | 
      ⚠️ [/ad/get/](https://business-api.tiktok.com/portal/docs?id=1735735588640770)
 (returns limited data) | 
      ✅ [/campaign/spc/get/](https://business-api.tiktok.com/portal/docs?id=1767334299811842) | 
      ✅ [/campaign/spc/report/get/](https://business-api.tiktok.com/portal/docs?id=1776454619412481) | 
     |
    
| 
      **Upgraded Smart+ API** | 
      ✅ [/campaign/get/](https://business-api.tiktok.com/portal/docs?id=1739315828649986)
✅ [/smart_plus/campaign/get/](https://business-api.tiktok.com/portal/docs?id=1843312818332930) | 
      ✅ [/adgroup/get/](https://business-api.tiktok.com/portal/docs?id=1739314558673922)
✅ [/smart_plus/adgroup/get/](https://business-api.tiktok.com/portal/docs?id=1843314879617026) | 
      ✅ [/smart_plus/ad/get/](https://business-api.tiktok.com/portal/docs?id=1843317378982914)
⚠️ [/ad/get/](https://business-api.tiktok.com/portal/docs?id=1735735588640770) 
(returns limited data at ad & creative levels)

**ID in Upgraded Smart+:**
Asset group (L3):
- `smart_plus_ad_id` is returned when you pull the creative level and is used to identify the ad for the creative.
- `ad_id_v2` is returned when you pull the ad (asset group) level and is used to filter and display the asset group level data.Creative (L4): `ad_id` | 
      ✅ [/smart_plus/material_report/overview/](https://business-api.tiktok.com/portal/docs?id=1843317489576961)
✅ [/smart_plus/material_report/breakdown/](https://business-api.tiktok.com/portal/docs?id=1843317510389761) | 
     |
  

### Retrieve the data for Manual Campaigns

  
    
| 
      Data level | 
      Through Campaign Management API endpoints | 
      Through Reporting API endpoints | 
     |
  
  
    
| 
      Campaign | 
      Use [/campaign/get/](https://business-api.tiktok.com/portal/docs?id=1739315828649986) to retrieve all Manual Campaigns within an ad account.
- Optionally, specify up to 100 IDs of Manual Campaigns in `campaign_ids` to retrieve these campaigns.
- The returned `campaign_automation_type` will be `MANUAL`. | 
      Use [/report/integrated/get/](https://business-api.tiktok.com/portal/docs?id=1740302848100353) for synchronous reports or [/report/task/create/](https://business-api.tiktok.com/portal/docs?id=1740302766489602) for asynchronous reports.
- Set `data_level` to `AUCTION_CAMPAIGN` and include `campaign_id` in `dimensions`. | 
     |
    
| 
      Ad group | 
      Use [/adgroup/get/](https://business-api.tiktok.com/portal/docs?id=1739314558673922) to retrieve all Manual Ad Groups within an ad account.
- Optionally, you can specify up to 100 IDs of Manual Ad Groups in `adgroup_ids` to retrieve these ad groups.
- The returned `campaign_automation_type` will be `MANUAL`. | 
      Use [/report/integrated/get/](https://business-api.tiktok.com/portal/docs?id=1740302848100353) for synchronous reports or [/report/task/create/](https://business-api.tiktok.com/portal/docs?id=1740302766489602) for asynchronous reports.
- Set `data_level` to `AUCTION_ADGROUP` and include `adgroup_id` in `dimensions`. | 
     |
    
| 
      Ad | 
      Use [/ad/get/](https://business-api.tiktok.com/portal/docs?id=1735735588640770) to retrieve all Manual Ads.
- Optionally, specify up to 100 IDs of Manual Ads in `ad_ids_v2` (recommended) or `ad_ids` to retrieve these ads.
- The returned `campaign_automation_type` will be `MANUAL`. The returned `ad_ids_v2` or `ad_id` represents the ID of a Manual Ad. | 
      Use [/report/integrated/get/](https://business-api.tiktok.com/portal/docs?id=1740302848100353) for synchronous reports or [/report/task/create/](https://business-api.tiktok.com/portal/docs?id=1740302766489602) for asynchronous reports.
- Set `data_level` to `AUCTION_AD` and include `ad_id_v2` (recommended) or `ad_id` in `dimensions`.
- Optionally, specify up to 100 IDs of Manual Ads in the `ad_ids_v2` (recommended) or `ad_ids` filter to retrieve the details of these ads. | 
     |
    
| 
      Creative | 
      ❌ | 
      ❌ | 
     |
  

  
### Retrieve the data for Smart+ Campaigns

  
    
| 
      Data level | 
      Through Campaign Management API endpoints | 
      Through Smart+ API endpoints | 
      Through Reporting API endpoints | 
     |
  
  
    
| 
      Campaign | 
      Use [/campaign/get/](https://business-api.tiktok.com/portal/docs?id=1739315828649986) and set `is_smart_performance_campaign` to `true` to retrieve all Smart+ Campaigns within an ad account.
- Optionally, specify up to 100 IDs of Smart+ Campaigns in `campaign_ids` to retrieve these campaigns.
- The returned `campaign_automation_type` will be `SMART_PLUS`. | 
      Use [/campaign/spc/get/](https://business-api.tiktok.com/portal/docs?id=1767334299811842) and specify up to 100 IDs of Smart+ Campaigns in `campaign_ids` to retrieve the details of these campaigns.
- **Note**: You cannot retrieve all Smart+ Campaigns within your ad account through this endpoint. | 
      Use [/report/integrated/get/](https://business-api.tiktok.com/portal/docs?id=1740302848100353) for synchronous reports or [/report/task/create/](https://business-api.tiktok.com/portal/docs?id=1740302766489602) for asynchronous reports.
- Set `data_level` to `AUCTION_CAMPAIGN` and include `campaign_id` in `dimensions`. | 
     |
    
| 
      Ad group | 
      Use [/adgroup/get/](https://business-api.tiktok.com/portal/docs?id=1739314558673922) to retrieve all ad groups within Smart+ Campaigns.
- Optionally, specify up to 100 IDs of ad groups within Smart+ Campaigns in `adgroup_ids` to retrieve these ad groups.
- The returned `campaign_automation_type` will be `SMART_PLUS`. | 
      ❌ | 
      Use [/report/integrated/get/](https://business-api.tiktok.com/portal/docs?id=1740302848100353) for synchronous reports or [/report/task/create/](https://business-api.tiktok.com/portal/docs?id=1740302766489602) for asynchronous reports.
- Set `data_level` to `AUCTION_ADGROUP` and include `adgroup_id` in `dimensions`. | 
     |
    
| 
      Ad | 
      Use [/ad/get/](https://business-api.tiktok.com/portal/docs?id=1735735588640770) to retrieve all ads within Smart+ Campaigns.
- Optionally, specify up to 100 IDs of ads within Smart+ Campaigns in `ad_ids` to retrieve these ads.
- The returned `campaign_automation_type` will be `SMART_PLUS`. | 
      ❌ | 
      Use [/report/integrated/get/](https://business-api.tiktok.com/portal/docs?id=1740302848100353) for synchronous reports or [/report/task/create/](https://business-api.tiktok.com/portal/docs?id=1740302766489602) for asynchronous reports.
- Set `data_level` to `AUCTION_AD` and include `ad_id` in `dimensions`. | 
     |
    
| 
      Creative | 
      ❌ | 
      Use [/campaign/spc/report/get/](https://business-api.tiktok.com/portal/docs?id=1776454619412481) to retrieve the creative-level data of one Smart+ Campaign. | 
      ❌ | 
     |
  

### Retrieve the data for Upgraded Smart+ Campaigns

  
    
| 
      Data level | 
      Through Campaign Management API endpoints | 
      Through Upgraded Smart+ API endpoints | 
      Through Reporting API endpoints | 
     |
  
  
    
| 
      Campaign | 
      Use [/campaign/get/](https://business-api.tiktok.com/portal/docs?id=1739315828649986).
- Optionally, specify up to 100 IDs of Upgraded Smart+ Campaigns in `campaign_ids` to retrieve these campaigns.
- The returned `campaign_automation_type` will be `UPGRADED_SMART_PLUS`. | 
      Use [/smart_plus/campaign/get/](https://business-api.tiktok.com/portal/docs?id=1843312818332930) to retrieve all Upgraded Smart+ Campaigns within an ad account.
- Optionally, specify up to 100 IDs of Upgraded Smart+ Campaigns in `campaign_ids` to retrieve these campaigns. | 
      Use [/report/integrated/get/](https://business-api.tiktok.com/portal/docs?id=1740302848100353) for synchronous reports or [/report/task/create/](https://business-api.tiktok.com/portal/docs?id=1740302766489602) for asynchronous reports.
- Set `data_level` to `AUCTION_CAMPAIGN` and include `campaign_id` in `dimensions`. | 
     |
    
| 
      Ad group | 
      Use [/adgroup/get/](https://business-api.tiktok.com/portal/docs?id=1739314558673922).
- Optionally, specify up to 100 IDs of Upgraded Smart+ Ad Groups in `adgroup_ids` to retrieve these ad groups.
- The returned `campaign_automation_type` will be `UPGRADED_SMART_PLUS`. | 
      Use [/smart_plus/adgroup/get/](https://business-api.tiktok.com/portal/docs?id=1843314879617026) to retrieve all Upgraded Smart+ Ad Groups within an ad account.
- Optionally, specify up to 100 IDs of Upgraded Smart+ Ad Groups in `adgroup_ids` to retrieve these ad groups. | 
      Use [/report/integrated/get/](https://business-api.tiktok.com/portal/docs?id=1740302848100353) for synchronous reports or [/report/task/create/](https://business-api.tiktok.com/portal/docs?id=1740302766489602) for asynchronous reports.
- Set `data_level` to `AUCTION_ADGROUP` and include `adgroup_id` in `dimensions`. | 
     |
    
| 
      Ad | 
      Use [/ad/get/](https://business-api.tiktok.com/portal/docs?id=1735735588640770) and specify up to 100 IDs of Upgraded Smart+ Ads in the `ad_ids_v2` filter to retrieve the details of these ads.
- For Upgraded Smart+ Ads, the returned `campaign_automation_type` will be `UPGRADED_SMART_PLUS`.
- The returned `ad_id_v2` represents the ID of the Upgraded Smart+ Ad. | 
      Use [/smart_plus/ad/get/](https://business-api.tiktok.com/portal/docs?id=1843317378982914) to retrieve all Upgraded Smart+ Ads within an ad account.
- Optionally, specify up to 100 IDs of Upgraded Smart+ Ads in `smart_plus_ad_ids` to retrieve these ads. | 
      Use [/report/integrated/get/](https://business-api.tiktok.com/portal/docs?id=1740302848100353) for synchronous reports or [/report/task/create/](https://business-api.tiktok.com/portal/docs?id=1740302766489602) for asynchronous reports.
- Set `data_level` to `AUCTION_AD` and include `ad_id_v2` in `dimensions`.
- Optionally, specify up to 100 IDs of Upgraded Smart+ Ads in the `ad_ids_v2` filter to retrieve the details of these ads. | 
     |
    
| 
      Creative | 
      Use [/ad/get/](https://business-api.tiktok.com/portal/docs?id=1735735588640770) with the `ad_ids_v2` filter not specified.
- For creatives within Upgraded Smart+ Ads, the returned `campaign_automation_type` will be `UPGRADED_SMART_PLUS_CREATIVE`.
- The returned `ad_id` represents the ID of a creative in the Upgraded Smart+ Ad and the returned `smart_plus_ad_id` represents the ID of the Upgraded Smart+ Ad. | 
      Use [/smart_plus/material_report/overview/](https://business-api.tiktok.com/portal/docs?id=1843317489576961) to retrieve an Upgraded Smart+ Creative Overview Report or [/smart_plus/material_report/breakdown/](https://business-api.tiktok.com/portal/docs?id=1843317510389761) to retrieve an Upgraded Smart+ Creative Breakdown Report. | 
      Use [/report/integrated/get/](https://business-api.tiktok.com/portal/docs?id=1740302848100353) for synchronous reports or [/report/task/create/](https://business-api.tiktok.com/portal/docs?id=1740302766489602) for asynchronous reports.
- Set `data_level` to `AUCTION_AD` and include `ad_id` in `dimensions`.
- Optionally, specify up to 100 IDs of creatives within Upgraded Smart+ Ads in the `ad_ids` filter to retrieve the details of these creatives. | 
     |
