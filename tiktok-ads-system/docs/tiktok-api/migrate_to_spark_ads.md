# Migrate to Spark Ads

**Doc ID**: 1848048566169730
**Path**: Use Cases/Campaign creation/Create Spark Ads/Migrate to Spark Ads

---

**If you use Custom Identity for non-Spark Ads targeting placements that include TikTok, read this document to find out the changes and actions you should take.**

# Background
To improve the business and user experience, TikTok is phasing out the use of Custom Identity in ads, that is, ads with custom profile images or display names in ad groups that deliver to Automatic Placement or Select Placement when TikTok is included. New ad accounts created on or after January 15, 2026 cannot create TikTok ad campaigns using Custom Identities (non-Spark Ads) for these placements. Existing ad accounts can no longer create TikTok ad campaigns using Custom Identities (non-Spark Ads) for these placements. Existing ads remain unaffected and editable. This shift promotes a safer and more engaging user experience while enhancing campaign performance. Ad campaigns that deliver only to Pangle or Global App Bundle placements are not be affected by Custom Identity deprecation. Learn more about [changes coming to Custom Identity](https://ads.tiktok.com/help/article/about-changes-coming-to-custom-identity).

# What's changing
- **Scope of impact**: The following campaign types are currently not impacted by this change:
  - Campaigns using "Branded Mission" objective
  - Campaigns using "Sales - TikTok Shop" objective
  - Campaigns with "Use Smart Creative to create ads" toggle on
  - Manual campaigns using a catalog
  - Campaigns with Pangle/Global App Bundle only placements
  
- For Manual Ad creation and update operations, the following fields will be affected by custom identity deprecation:

    
        
| 
            Endpoint | 
            Field | 
            Before | 
            After | 
         |
    
    
        
| 
            [/ad/create/](https://business-api.tiktok.com/portal/docs?id=1739953377508354) | 
            `identity_type` | 
            Identity type.

Enum values: `CUSTOMIZED_USER`, `AUTH_CODE`, `TT_USER`, `BC_AUTH_TT`.

For details about identities, see [Identities]( https://business-api.tiktok.com/portal/docs?id=1738958351620097).
 | 
            Identity type.

Enum values: `CUSTOMIZED_USER`, `AUTH_CODE`, `TT_USER`, `BC_AUTH_TT`.

For details about identities, see [Identities]( https://business-api.tiktok.com/portal/docs?id=1738958351620097).

Support for the `CUSTOMIZED_USER` enum value in ads that deliver to Automatic Placement or Select Placement when TikTok is included has been removed. If `CUSTOMIZED_USER` is specified, an error will occur. | 
         |
        
| 
            `identity_id` | 
            Any identity ID. | 
            If the Identity ID is of a `CUSTOMIZED_USER` identity type, an error will occur. | 
         |
        
| 
            [/ad/update/](https://business-api.tiktok.com/portal/docs?id=1739953405142018) | 
            `identity_type`
 | 
            Identity type.

Enum values: `CUSTOMIZED_USER`, `AUTH_CODE`, `TT_USER`, `BC_AUTH_TT`.

For details about identities, see [Identities]( https://business-api.tiktok.com/portal/docs?id=1738958351620097).
 | 
            Identity type.

Enum values: `CUSTOMIZED_USER`, `AUTH_CODE`, `TT_USER`, `BC_AUTH_TT`.

For details about identities, see [Identities]( https://business-api.tiktok.com/portal/docs?id=1738958351620097).

Support for the `CUSTOMIZED_USER` enum value in ads that deliver to Automatic Placement or Select Placement when TikTok is included has been removed. If `CUSTOMIZED_USER` is specified, an error will occur. | 
         |
        
| 
            `identity_id` | 
            Any identity ID. | 
            If the Identity ID is of a `CUSTOMIZED_USER` identity type, an error will occur. | 
         |
    

 	- To learn more about how to create Manual Spark Ads using TikTok identities, see [Create Spark Ads](https://business-api.tiktok.com/portal/docs?id=1739470744631298).

- For Smart+ Campaign creation and update operations, the following fields will be affected by custom identity deprecation:
  
  

  
    
| 
      Endpoint | 
      Field | 
      Before | 
      After | 
     |
  
  
    
| 
      [/campaign/spc/create/](https://business-api.tiktok.com/portal/docs?id=1767334204047362) | 
      identity_type Conditional | 
      Required when you are not using Spark Ads (`tiktok_item_id`).

Identity type for non-Spark Ads.

Enum value: `CUSTOMIZED_USER`. | 
      The field has been deprecated for ads that deliver to Automatic Placement or Select Placement when TikTok is included.
 | 
     |
    
| 
      identity_id Conditional | 
      Required when you are not using Spark Ads (`tiktok_item_id`).

Identity ID for non-Spark Ads. | 
      The field has been deprecated for ads that deliver to Automatic Placement or Select Placement when TikTok is included. | 
     |
    
| 
      [/campaign/spc/update/](https://business-api.tiktok.com/portal/docs?id=1767334250066945) | 
      identity_id | 
      Identity ID when you are not using Spark Ads. | 
     |
  

- For Upgraded Smart+ Campaign creation and update operations, the following fields will be affected by custom identity deprecation:

  
    
| 
      Endpoint | 
      Field | 
      Before | 
      After | 
     |
  
  
    
| 
      [/smart_plus/ad/create/](https://business-api.tiktok.com/portal/docs?id=1843317390059522) | 
      `ad_configuration.identity_type`  Conditional | 
      Required when you are creating non-Spark Ads.

Non-Spark Ads identity type.

Enum values: `CUSTOMIZED_USER`.

For details about identities, see [Identities](https://business-api.tiktok.com/portal/docs?id=1738958351620097). | 
      Creating non-Spark Ads in ad groups that deliver to Automatic Placement or Select Placement when TikTok is included is no longer available. Existing ads will remain unaffected and editable. Learn more about [changes coming to Custom Identity](https://ads.tiktok.com/help/article/about-changes-coming-to-custom-identity) and [migrate to Spark Ads](https://business-api.tiktok.com/portal/docs?id=1848048566169730). | 
     |
    
| 
      `ad_configuration..identity_id` Conditional | 
      Required when you are creating non-Spark Ads.

Non-Spark Ads identity ID. | 
      Creating non-Spark Ads in ad groups that deliver to Automatic Placement or Select Placement when TikTok is included is no longer available. Existing ads will remain unaffected and editable. Learn more about [changes coming to Custom Identity](https://ads.tiktok.com/help/article/about-changes-coming-to-custom-identity) and [migrate to Spark Ads](https://business-api.tiktok.com/portal/docs?id=1848048566169730). | 
     |
    
| 
      [/smart_plus/ad/update/](https://business-api.tiktok.com/portal/docs?id=1843317411665921) | 
      `ad_configuration.identity_type` | 
      Non-Spark Ads identity type.

Enum values: `CUSTOMIZED_USER`.

For details about identities, see [Identities](https://business-api.tiktok.com/portal/docs?id=1738958351620097). | 
     |
    
| 
      `ad_configuration.identity_id` | 
      Non-Spark Ads identity ID. | 
     |
  

  
- **Changes to ads-only mode have launched**:

Starting January 27, 2026, the default value of `dark_post_status` request parameter in all ads creation API endpoints ([/smart_plus/ad/create/](https://business-api.tiktok.com/portal/docs?id=1843317390059522), [/ad/create/](https://business-api.tiktok.com/portal/docs?id=1739953377508354), and [/campaign/spc/create/](https://business-api.tiktok.com/portal/docs?id=1767334204047362)) has been changed from `OFF` to `ON`. If not specified, ads-only mode, also known as "Show through ads only", will be enabled by default when you create ads via API. This means that a TikTok post will not be displayed in the associated TikTok account's profile when you create Spark Ads with the push method. We recommend setting "Show through ads only" as the default in your integration to match the ad creation process on TikTok Ads Manager.

# What actions you should take
## Prerequisites
A TikTok account for ad creation.

## Steps
### 1. Link TikTok accounts to ad accounts
You need to link a TikTok account to the ad account with ad delivery permissions to select the TikTok account as an identity during ad creation.

#### Option 1: Via TikTok Business Center (Recommended)
This option facilitates linking **multiple TikTok accounts** to **multiple ad accounts** (including those of external partners) with centralized permission management. Once a TikTok account is linked to an ad account, anyone with access to that ad account can use the TikTok account for ad delivery. This removes the need to grant TikTok account access to each user, helping simplify cross-team and agency workflows. This is recommended for most businesses.

To link a TikTok account with ad delivery permissions to an ad account in Business Center:

1. Generate an authorization URL for requesting ad delivery permissions from a TikTok account using [/bc/asset/account/authorization/](https://business-api.tiktok.com/portal/docs?id=1846868897541122).

2. Generate a QR code from the authorization URL using a QR code generator and share the QR code with a TikTok account owner. When the TikTok account owner scans the QR code, they can grant the **"Existing posts"** permissions for Spark Ads Pull and the **"TikTok posts"** permissions for Spark Ads Push to the Business Center.

3. Link the TikTok account to an ad account in Business Center using [/bc/asset/advertiser/assign/](https://business-api.tiktok.com/portal/docs?id=1846868953025538). 

Now your TikTok account is now ready for ad delivery.

#### Option 2: Directly in TikTok Ads Manager UI
TikTok accounts linked this way are **only accessible to the individual user** who linked them, and cannot be centrally managed or shared with other team members or agencies. For team or agency collaboration, **linking via TikTok Business Center is recommended.**

To link a TikTok account to an ad account in [TikTok Ads Manager](https://ads.tiktok.com/i18n/home) UI:

1. In the campaign creation workflow, click **Connect account** under the Ad details section.

2. Follow the linking instructions for your TikTok account.

> **Note**

>  This feature update will be rolled out gradually, so it may not be available to you yet. For impacted clients, you may notice the updated ad creation flow where the Custom Identity option is no longer available. 

### 2. Get identities available for your ad account
The `CUSTOMIZED_USER` enum value remains supported for endpoints such as `/identity/get/` and `/identity/info/`. Learn about the full list of identity endpoints in [Identity](https://business-api.tiktok.com/portal/docs?id=1740133137507393).

Use the following endpoints to get information on the identities available for an ad account and the posts that have been published under a specific identity:

- **Identity list**: Use the [/identity/get/](https://business-api.tiktok.com/portal/docs?id=1740218420781057) endpoint to get a list of identities under an ad account. You can filter results by identity type or display name.

- **Identity information**: Use the[ /identity/info/](https://business-api.tiktok.com/portal/docs?id=1740218453385217) endpoint to gather details about a specific identity.

- **Posts by identity**: Use the [/identity/video/get/](https://business-api.tiktok.com/portal/docs?id=1740218475032577) endpoint to list all posts under an identity of the type `AUTH_CODE`, `TT_USER`, or `BC_AUTH_TT`.

- **TikTok post information**: Use the [/identity/video/info/](https://business-api.tiktok.com/portal/docs?id=1740218522178562) endpoint to get the information about one or more TikTok posts that you published using the `AUTH_CODE`, `TT_USER` or `BC_AUTH_TT` identity.

### 3. (Optional) Authorize TikTok posts
> **Note**

> There are no changes to these endpoints. 

The following endpoints are used to create or update ads that use authorized TikTok posts:

- **Apply TikTok post authorization code**: Use the [/tt_video/authorize/](https://business-api.tiktok.com/portal/docs?id=1738376435339265) endpoint to apply an authorization code. After you get the authorization code from the post owner, the authorization is not automatically in effect. You need to apply the code to connect the ad account with the Spark Ads post.

- **Get Spark Ads authorized posts**: Use the [/tt_video/list/](https://business-api.tiktok.com/portal/docs?id=1738376465972226) endpoint to get a list of Spark Ads posts that have been authorized to an ad account.

- **Get info about a TikTok authorized post**: Use the [/tt_video/info/](https://business-api.tiktok.com/portal/docs?id=1738376324021250) endpoint to get information about the Spark Ads post that you have been authorized to use as an ad. You need to provide the authorization code received from the post owner.

- **Unbind a TikTok authorized post**: Use the [/tt_video/unbind/](https://business-api.tiktok.com/portal/docs?id=1738376509936641) endpoint to unbind a Spark Ad post after the authorization has expired or has been revoked. Unbinding a Spark Ad post removes the post from the list of authorized Spark Ads posts for the ad account.

### 4. Create ads with TikTok identities

Listed below are the different ad or campaign creation and update endpoints for different campaign types:

- **Manual Campaigns**
	- **Create ads**: Use the [/ad/create/](https://business-api.tiktok.com/portal/docs?id=1739953377508354) endpoint to upload your ad creatives (pictures, videos, texts, call-to-action) and create a Manual Ad. See [here](https://business-api.tiktok.com/portal/docs?id=1745292553358338) to learn about how to create Manual Ads.
	- **Update ads**: Use the [/ad/update/](https://business-api.tiktok.com/portal/docs?id=1739953405142018) endpoint to modify the creatives of your Manual Ads, such as call-to-action, ad name, text, image and video material.
	- The following field can be used to set the visibility of the ad post on the TikTok account profile page.

| 
Field | Data Type | Description | 
 |

| 
`dark_post_status` | 
string | 
Valid only when you create Spark Ads through Spark Ads Push.

The status of the "Ads-only mode" for your creatives.

Enum values:
- `ON`: Enable the ads-only mode to limit your posts to paid traffic.`OFF`: Disable the ads-only mode. The post will appear on your TikTok profile and will be eligible to receive organic traffic.Default value for Spark Ads Push: `OFF`. | 
 |

- **Smart+ Campaigns**
	- **Create campaigns**: Use the [/campaign/spc/create/](https://business-api.tiktok.com/portal/docs?id=1767334204047362) endpoint to create a Smart+ Campaign.
	- **Update campaigns**: Use the [/campaign/spc/update/](https://business-api.tiktok.com/portal/docs?id=1767334250066945) endpoint to update a Smart+ Campaign. The endpoint supports incremental updates.

- **Upgraded Smart+ Campaigns**
	- **Create campaigns**: Use the [/smart_plus/campaign/create/](https://business-api.tiktok.com/portal/docs?id=1843312852800706) endpoint to create an Upgraded Smart+ Campaign.
	- **Update campaigns**: Use the [/smart_plus/campaign/update/](https://business-api.tiktok.com/portal/docs?id=1843312876001282) endpoint to update an Upgraded Smart+ Campaign.
