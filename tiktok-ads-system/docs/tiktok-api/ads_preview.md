# Ads preview

**Doc ID**: 1740317791125506
**Path**: Marketing API/Creatives/Guides/Creative tools/Ads preview

---

You can preview the following ad types. Depending on the type of ads you want to preview, the needed parameters are different. See [/creative/ads_preview/create/](https://ads.tiktok.com/marketing_api/docs?id=1739403070695426) to find out detailed parameters. 

Ads that you can preview include the following types. We strongly recommend that you try out the preview types of ads you plan to create, existing standard ads, existing product card, and existing instant product landing page to have a better developer experience. 
- Ads that you plan to create
- Existing standard ads
- Existing product card
- Existing instant product landing page
- Videos
- Images

> **Note**
ACO (Automated Creative Optimization) ads do not support previews.

A preview link (`preview_link`) will be returned in the response. The link is valid for 24 hours. After it expires, you need to make the request again to get a new preview link.
