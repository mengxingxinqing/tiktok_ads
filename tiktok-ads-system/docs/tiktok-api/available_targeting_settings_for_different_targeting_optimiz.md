# Available targeting settings for different targeting optimization modes in Upgraded Smart+ Ad Groups

**Doc ID**: 1847839827327106
**Path**: Appendix/Available targeting settings for different targeting optimization modes in Upgraded Smart+ Ad Groups

---

The following table outlines the available targeting settings for different targeting optimization modes in [Upgraded Smart+ Ad Groups](https://business-api.tiktok.com/portal/docs?id=1843310524500993).

    
        
| 
            Targeting optimization mode | 
            Available targeting setting | 
            Requirement | 
            Parameter | 
            How to configure the parameter | 
         |
    
    
        
| 
            Automatic targeting
(`targeting_optimization_mode`
 as `AUTOMATIC` or not specified) | 
            Audience controls
· Location | 
            Specify valid locations.
If a catalog is specified, the location should match or be the subset of the targeting location of your catalog. | 
            `location_ids` or `zipcode_ids` or both | 
            Specify valid values.

If a catalog is specified, specify IDs of locations that match or are a subset of the targeting location of `catalog_id`.
To obtain the targeting location of a catalog, use [/catalog/get/](https://business-api.tiktok.com/portal/docs?id=1740315452868610) and check the returned `country`. | 
         |
        
| 
            Audience controls
· Minimum age | 
            Any of the following options:
                
                    
- 18
                    
- 25
                 | 
            `spc_audience_age` | 
            Any of the following values:
                
                    
- `OVER_EIGHTEEN` or unspecified
                    
- `OVER_TWENTY_FIVE`
                 | 
         |
        
| 
            Audience controls
· Languages
 (Optional) | 
            Enabled or disabled | 
            `languages` | 
            Specify valid values or not specified | 
         |
        
| 
            Audience controls
· Exclude audience
(Optional) | 
            Enabled or disabled | 
            `excluded_audience_ids` | 
            Specify valid values or not specified | 
         |
        
| 
            Audience suggestions
· Age
 (Optional)

**Note**: Audience suggestions guide automatic targeting by choosing additional audience settings. These serve as suggestions only, and delivery to those audiences is not guaranteed. | 
            Enabled or disabled | 
            `age_groups` | 
            Specify valid values or not specified | 
         |
        
| 
            Audience suggestions
· Gender
 (Optional) | 
            Enabled or disabled | 
            `gender` | 
            Specify valid values or not specified | 
         |
        
| 
            Audience suggestions
· Custom audience
 (Optional) | 
            Enabled or disabled | 
            `audience_ids` | 
            Specify valid values or not specified | 
         |
        
| 
            Audience suggestions
· Interests & behaviors
  · Interests
 (Optional) | 
            Enabled or disabled | 
            `interest_category_ids`
`interest_keyword_ids` | 
            Specify valid values or not specified | 
         |
        
| 
            Audience suggestions
· Interests & behaviors
  · Purchase intention
 (Optional) | 
            Enabled or disabled | 
            `purchase_intention_keyword_ids` | 
            Specify valid values or not specified | 
         |
        
| 
            Audience suggestions
· Interests & behaviors
  · Video interactions
  · Creator interactions
  · Hashtag interactions
 (Optional) | 
            Enabled or disabled | 
            `actions` | 
            Specify valid values or not specified | 
         |
        
| 
            Custom targeting
(`targeting_optimization_mode` 
as `MANUAL`) | 
            Demographics
· Location | 
            Specify a valid value.
If a catalog is specified, the location should match or be the subset of the targeting location of your catalog. | 
            `location_ids` or `zipcode_ids` or both | 
            Specify a valid value.
If a catalog is specified, specify IDs of locations that match or are a subset of the targeting location of `catalog_id`.
To obtain the targeting location of a catalog, use [/catalog/get/](https://business-api.tiktok.com/portal/docs?id=1740315452868610) and check the returned `country`. | 
         |
        
| 
            Demographics
· HFSS Product/Brand | 
            Enabled or disabled

                
                    
- You can enable this setting when your targeting locations include locations in the UK, Australia, New Zealand, and the European Union.
                 | 
            `is_hfss` | 
            `true` or `false`.
                
                    
- You can set it to `true` when your targeting locations include locations in the UK, Australia, New Zealand, and the European Union.
                 | 
         |
        
| 
            Demographics
· LHF (Less Healthy Foods) compliance | 
            Enabled or disabled

                
                    
- This setting must be enabled when your targeting locations include locations in the UK and HFSS Product/Brand is enabled.
                 | 
            `is_lhf_compliance` | 
            `true` or `false`.
                
                    
- You need to set it to `true` when your targeting locations include locations in the UK and `is_hfss` is `true`.
                 | 
         |
        
| 
            Demographics
· Age
 (Optional) | 
            Enabled or disabled | 
            `age_groups` | 
            Specify valid values or not specified | 
         |
        
| 
            Demographics
· Gender
 (Optional) | 
            Enabled or disabled | 
            `gender` | 
            Specify valid values or not specified | 
         |
        
| 
            Demographics
· Languages
 (Optional) | 
            Enabled or disabled | 
            `languages` | 
            Specify valid values or not specified | 
         |
        
| 
            Custom audience
· Include audience
 (Optional) | 
            Enabled or disabled | 
            `audience_ids` | 
            Specify valid values or not specified | 
         |
        
| 
            Custom audience
· Smart audience
 (Optional) | 
            Enabled or disabled | 
            `smart_audience_enabled` | 
            `true` or `false` | 
         |
        
| 
            Custom audience
· Exclude audience
 (Optional) | 
            Enabled or disabled | 
            `excluded_audience_ids` | 
            Specify valid values or not specified | 
         |
        
| 
            Detailed targeting
· Interests & behaviors
  · Interests
 (Optional) | 
            Enabled or disabled | 
            `interest_category_ids`
`interest_keyword_ids` | 
            Specify valid values or not specified | 
         |
        
| 
            Detailed targeting
· Interests & behaviors
  · Purchase intention
 (Optional) | 
            Enabled or disabled | 
            `purchase_intention_keyword_ids` | 
            Specify valid values or not specified | 
         |
        
| 
            Detailed targeting
· Interests & behaviors
  · Video interactions
  · Creator interactions
  · Hashtag interactions
 (Optional) | 
            Enabled or disabled | 
            `actions` | 
            `true` or `false` | 
         |
        
| 
            Detailed targeting
· Interests & behaviors
  · Smart interests & behaviors
 (Optional) | 
            Enabled or disabled | 
            `smart_interest_behavior_enabled` | 
            Specify valid values or not specified | 
         |
        
| 
            Detailed targeting
· Spending power
 (Optional) | 
            Enabled or disabled | 
            `spending_power` | 
            Specify valid values or not specified | 
         |
        
| 
            Detailed targeting
· Household income
 (Optional) | 
            Enabled or disabled | 
            `household_income` | 
            Specify valid values or not specified | 
         |
        
| 
            Device
· Operating system
(Optional) | 
            Enabled or disabled | 
            `operating_systems` | 
            Specify valid values or not specified | 
         |
        
| 
            Device
· OS versions
(Optional) | 
            Enabled or disabled | 
            `min_android_version`
`min_ios_version` | 
            Specify valid values or not specified | 
         |
        
| 
            Device
· Device model
(Optional) | 
            Enabled or disabled | 
            `device_model_ids` | 
            Specify valid values or not specified | 
         |
        
| 
            Device
· Connection type
(Optional) | 
            Enabled or disabled | 
            `network_types` | 
            Specify valid values or not specified | 
         |
        
| 
            Device
· Carriers
(Optional) | 
            Enabled or disabled | 
            `carrier_ids` | 
            Specify valid values or not specified | 
         |
        
| 
            Device
· Internet service provider
(Optional) | 
            Enabled or disabled | 
            `isp_ids` | 
            Specify valid values or not specified | 
         |
        
| 
            Device
· Device price
(Optional) | 
            Enabled or disabled | 
            `device_price_ranges` | 
            Specify valid values or not specified | 
         |
        
| 
            Use saved audience
(Optional) | 
            Enabled or disabled | 
            `saved_audience_id` | 
            Specify valid values or not specified | 
         |
