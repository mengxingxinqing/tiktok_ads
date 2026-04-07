# Report App, Web, Offline, or CRM Events

**Doc ID**: 1771101303285761
**Path**: API Reference/Events 2.0/Report App, Web, Offline, or CRM Events

---

Use this endpoint to report a single App, Web, Offline, or CRM (Customer relationship management) event, or multiple App, Web, Offline, or CRM events in batch.

## Request

**Endpoint** https://business-api.tiktok.com/open_api/v1.3/event/track/

**Method** POST

**Header**

```xtable
|Field{20%}|Data Type{15%}|Description{65%}|
|---|---|---|
|Access-Token {Required}|string|Authorized access token. 
To obtain an access token, refer to [Events API 2.0 - Authentication](https://ads.tiktok.com/marketing_api/docs?id=1771101130925058).|
|Content-Type {Required}|string|Request message type.
Allowed format: `application/json`.  |
```

**Parameters**

```xtable
|Field{20%}|Data Type{15%}|Description{65%}|
|---|---|---|
| event_source {Required} | string | This field is used to specify the type of events you are uploading through Events API.  
Enum values:  
-  `web`: The events took place on your website and are measured by a Pixel Code. To generate sample code in cURL, Python, or Node.js format for reporting Web Events via the Events API 2.0, use [the Payload Helper for Web](https://business-api.tiktok.com/portal/docs?id=1807346079965186).   
- `app`: The events took place on your app and are measured by a TikTok App ID.
- `offline` : The conversions took place in a physical store and are measured by an Offline Event Set ID.
- `crm`: The lead events took place in a CRM system and are measured by a CRM Event Set ID. 
**Note**: Reporting App Events using Events API 2.0 is currently an allowlist-only feature. If you would like to access it, please contact your TikTok representative.   |
| event_source_id {Required} | string | An Event Source ID that is used to measure events.  
- When `event_source` is set to `web`, specify a Pixel Code through this field. 
To obtain a Pixel Code, refer to [FAQs - Where can I find the Pixel Code](https://ads.tiktok.com/marketing_api/docs?id=1771101001228290). 
- When `event_source` is set to `offline`, specify an Offline Event Set ID through this field. 
To obtain an Offline Event Set ID, refer to [Setup Guide for Offline](https://ads.tiktok.com/marketing_api/docs?id=1771101027431425).
- When `event_source` is set to `app`, specify a TikTok App ID through this field. 
To obtain a TikTok App ID, refer to [Setup Guide for App](https://ads.tiktok.com/marketing_api/docs?id=1771101111730178).
- When `event_source` is set to `crm`, specify a CRM Event Set ID through this field.
To obtain a CRM Event Set ID, use [/crm/list/](https://business-api.tiktok.com/portal/docs?id=1780896521680898).  |
| data {Required} | object[] | An object array of the events you want to report.  
-  If you are sending a single event, pass one object in the array. 
-  If you are batching multiple events in a single payload, **you can report up to 1,000 events in one request**. If a request contains more than 1,000 events, the entire request will be rejected.  
-  To optimize campaign performance, it's **highly recommended to send the event in real-time (without batching)** as soon as it is seen on the advertiser's server.     |
#| event {Required} | string | **For web, app, offline, and CRM events.**
Conversion event name. 

- For web and app events, it can be either a Standard Event or Custom Event.
- For offline events, it can only be a Standard Event.
- For CRM events, it can only be a Custom Event.To find out the supported values for Standard Events, refer to [Events API 2.0-Supported events](https://ads.tiktok.com/marketing_api/docs?id=1771101186666498).  
To report a Custom Web Event or Custom App Event, pass a customized name in this field.
 Do not use sensitive words in the name of Custom Events. Otherwise, the responsibility for any consequences that may arise will be borne by you.|
#| event_time {Required} | integer | **For web, app, offline, and CRM events.**
The time when the event occurred, indicated as a Unix timestamp measured in seconds, and in UTC+0 time zone.|
#| event_id {+Conditional} | string | **For web, offline, and CRM events.**
Required in any of the following scenarios:
- You are sending web events (`event_source` = `web`) from both TikTok browser pixel and Events API.
- You are sending CRM events (`event_source` = `crm`) from both Events API and by uploading CSV files on Events Manager.The ID that is used to identify a unique event. It can be hashed or unhashed.   
 TikTok uses the `event_source_id`, `event_id` and `event` to deduplicate the same event sent multiple times from a single channel or across multiple channels (for instance browser pixel and Events API).  
For more information on event deduplication and how to complete the setup, refer to [Events API 2.0 - Event Deduplication](https://ads.tiktok.com/marketing_api/docs?id=1771100965992450).   |
#| user | object |**For web, app, offline, and CRM events.**
 Information about the customer.   
  To view the list of fields included in the `user` object, refer to the "[`user` parameters](#item-link-user parameters)" section below.   |
#| properties | object |**For web, app, offline, and CRM events.**
 Information about the product, order and additional information to help improve ad performance.  
To view the list of fields included in the `properties` object, refer to the "[`properties` parameters](#item-link-properties parameters)" section below.   |
#| page{+Conditional} | object | **Required for web events.**
Information about the web page.  
 To view the list of fields included in the `page` object, refer to the "[`page` parameters](#item-link-page parameters)" section below.   |
#| app{+Conditional} | object |**Required for app events.**
Information about the app.  
 To view the list of fields included in the `app` object, refer to the "[`app` parameters](#item-link-app parameters)" section below.
**Note**: Reporting App Events using Events API 2.0 is currently an allowlist-only feature. If you would like to access it, please contact your TikTok representative. |
#| ad |  object |**Only for app and web events.**
Information about the ad. 
To view the list of fields included in the `ad` object, refer to the "[`ad` parameters](#item-link-ad parameters)" section below.|
#| limited_data_use | boolean | **For web and app events.**
To learn more about the Limited Data Use feature, refer to [Events API 2.0 - Limited Data Use](https://ads.tiktok.com/marketing_api/docs?id=1771101204435970).   |
#| lead {+Conditional} | object | **Required for CRM events. **
Information about the lead. 
To view the list of fields included in the `lead` object, refer to the "[`lead` parameters](#item-link-lead parameters)" section below. |
```

### `user` parameters
Events API 2.0 uses customer information, such as TikTok Click IDs, Advanced Matching, and additional signals like IP address and User Agent, to match web visitor events with TikTok users. Once matched, information shared via the Events API can be used to build targeting audiences, inform the optimization algorithm, and better measure campaign results.

To increase the accuracy of targeting and optimization models, it is highly recommended to include multiple types of matching data. You can use Advanced Matching, TikTok Click IDs (`ttclid`), and Cookies to attribute conversions.

```xtable
| Field {15%}| Data Type {15%}|Description{40%} |Examples{30%}|
|---|---|---|
| ttclid | string | **For web events only.**

TikTok Click ID, a data connection parameter appended to a landing page URL whenever a user clicks on an ad on TikTok. 
The `ttclid` valid period is the same as your CTA window setting in [Attribution Manager](https://ads.tiktok.com/help/article/attribution-manager?redirected=1). 
For more information on sending TikTok Click IDs, refer to [Events API 2.0 - Send TikTok Click ID (`ttclid`)](https://ads.tiktok.com/marketing_api/docs?id=1771100879787009). ||
| email | string 
 or string[]| **For web, app, offline, and CRM events.**

**SHA-256 hashing is required.** 
The email address, or email addresses of the customer. 
 Follow the instructions below to obtain a valid value: 
- **Trim** any leading and trailing spaces of each email before hashing. 
- **Lowercase** all characters before hashing.
- **Hash** the normalized email values using SHA-256.**Example**: 
-  Original: " ALICE_abc@gmail.com " 
-  Normalized: "alice_abc@gmail.com" (leading and trailing spaces trimmed and lowercased) 
-  SHA-256 hashed: "848a771458438fc2ec420560d769fb9b9b86851ee338ec56517baabd79d3bb4f"| `"848a771458438fc2ec420560d769fb9b9b86851ee338ec56517baabd79d3bb4f"`|
| phone | string
 or string[] |  **For web, app, offline, and CRM events.**

**SHA-256 hashing is required. ** 
The phone number or phone numbers of the customer. 
Follow the instructions below to obtain a valid value: 
- **Normalize** the phone number to [E.164 format](https://www.twilio.com/docs/glossary/what-e164) (for example, "+12133734253"). We recommend using [https://github.com/catamphetamine/libphonenumber-js](https://github.com/catamphetamine/libphonenumber-js) for E.164 parsing. **Country code** must be included and prefixed with the `+` sign, without any parentheses or leading `0`s. For example, a US phone number should be prefixed with the `+1` country code.
-  **No spaces, letters or symbols** except the `+` for the country code are included. 
- **SHA-256 hash** the phone number after normalizing. **Example**: 
-  Original: "(+1)2133734253"
-  Normalized to E.164 format: "+12133734253"
-  SHA256 hashed: "9f7ec22d72092cd3c0b58726ed9c2d91b92e51a3f29837508fb2948bb22dd2fd"|`"9f7ec22d72092cd3c0b58726ed9c2d91b92e51a3f29837508fb2948bb22dd2fd"`|
| external_id | string 
 or string[]|  **For web and CRM events only.**

**SHA-256 hashing is required. ** 
External ID, a unique identifier on the advertiser's side, such as loyalty membership IDs, user IDs, and external cookie IDs. To learn more about the `external_id` parameter, refer to [Events API 2.0 - Set up External ID](https://ads.tiktok.com/marketing_api/docs?id=1771100952291330). 
**Example**: 
-  Original: "user_123"
-  SHA-256 hashed: "80fba0ae1c48e3978e43e4efc365e14e12ea0c830ba8ba5b9a2dafc7e3f2ab8b"| `"80fba0ae1c48e3978e43e4efc365e14e12ea0c830ba8ba5b9a2dafc7e3f2ab8b"` |
| ttp | string |**For web events only.**

 Cookie ID. 
If you also use Pixel SDK and have enabled cookies, Pixel SDK automatically saves a unique identifier in the `_ttp` cookie. The value of `_ttp` is used to match website visitor events with TikTok ads. You can extract the value of `_ttp` and attach the value here. 
  To learn more about the `ttp` parameter, refer to [Events API 2.0 - Send TikTok Cookie (`_ttp`)](https://ads.tiktok.com/marketing_api/docs?id=1771100936446977). ||
| ip | string | **For web and app events only.**

Non-hashed ** public IP** address of the user's device. 
To increase the probability of matching website visitor events with TikTok ads, we recommend sending both `ip` and `user_agent`. 

Both IPv4 and IPv6 addresses are supported. For IPv6 addresses, both full and compressed formats are acceptable. 
For example:
- Full format: **2001:0db8:1111:000a:00b0:0000:0000:0200**
- Compressed format: **2001:db8:1111:a:b0::200**|`"203.0.113.1"`

`"2001:0db8:85a3:0000:0000:8a2e:0370:7334"`|
| user_agent | string | **For web and app events only.**

 Non-hashed user agent from the user’s device. 
To increase the probability of matching website visitor events with TikTok ads, we recommend sending both `ip` and `user_agent`. | `"Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604"`|
| idfa | string | The iOS IDFA **for app events only. **
 For iOS 14 and above, ensure that IDFA data collection follows [Apple’s policies](https://developer.apple.com/app-store/user-privacy-and-data-use/). Both raw and SHA-256 IDFAs are accepted:
- For raw IDFAs, all characters must be **UPPERCASE**. 
- For SHA-256 IDFAs, all characters must be **lowercase**, and any **leading/trailing spaces** must be **trimmed** before hashing.| 
- Raw IDFA: `"EA7583CD-A667-48BC-B806-42ECB2B48606"`
- SHA-256 IDFA: `"70574fa9c8f498a7b2e5c8712b1126de7b1406fd02fdc591821c5bd33092fd1c"`  |
| idfv | string | The iOS IDFV ** for app events only**. | |
| gaid | string | The GAID (Google Advertising ID)** for app events only**.
 Both raw and SHA-256 GAIDs are accepted.
For both raw and SHA-256 GAIDs:
- All characters must be **lowercase**.
- **Leading/trailing spaces** must be **trimmed** before hashing | 
- Raw GAID: `"aaaaaa-2222-1111-8787-809e92233ba0"`
-  SHA-256 GAID: `"0ebad966881e1eebffe69b3abf624631cf83ec9bf8cb3ce134c7c75c6d8ee7fc"`     |
| locale | string  | **For web and app events only.**

 The BCP 47 language identifier. 
 For reference, refer to [the IETF BCP 47 standardized code](https://www.rfc-editor.org/rfc/bcp/bcp47.txt). |`"en-US"`

`"zh-CN"`|
| att_status | string | **For app events only.**

 Whether the user has authorized your mobile app to access app-related data for measuring the user or the device. This is an iOS only field. 
Enum values: 
- `AUTHORIZED`: The user has authorized access to app-related data that can be used for measuring the user or the device. 
-  `DENIED`: The user has not agreed to authorize your mobile app to access app-related data for measuring the user or the device via [Apple's AppTrackingTransparency framework](https://developer.apple.com/documentation/apptrackingtransparency). 
If this field is set to `DENIED`, TikTok will not use the PII data (for instance, user email address or phone number) in this App Event for user-level matching.
- `NOT_DETERMINED`: The user has not yet received an authorization request to authorize access to app-related data that can be used for measuring the user or the device.
- `RESTRICTED`: The authorization to access app-related data is restricted.
-  `NOT_APPLICABLE`: The iOS version is below 14 or the device is running Android. | `"AUTHORIZED"`   |
```

### `properties` parameters
Information about the order and product associated with the event. Providing this information allows TikTok to help optimize your ads performance.
```xtable
| Field {20%}| Data Type {10%}| Description{40%} |Required for reporting Return on Ad Spend (ROAS) or for Value-based Optimization (VBO){15%} |Required for Video Shopping Ads (VSA){15%} |
|---|---|---|---|---|
|content_ids|string[] |Unique ID or array of multiple IDs of the products or content. 
Example: `["987", "654"]`. 
We recommend using `sku_id` or `item_group_id` that matches the `sku_id` or `item_group_id` you set up in the catalog, if available.
This field is required for Video Shopping Ads (VSA). | |✅|
| contents {+Conditional} | object[]| Relevant products in an event with product information.   
 To view the list of fields included in the contents object, refer to the "[`contents` parameters](#item-link-contents parameters)" section below.   |    | ✅ |
| content_type{+Conditional} | string | The type of content in the event.   
Enum values: `product`, `product_group`.   
-  When the `content_id` in the `contents` parameter is specified as `sku_id`, set this field to `product`.  
-  When the `content_id` in the `contents` parameter is specified as `item_group_id`, set this field to `product_group`.   |  |  ✅|
| currency{+Conditional}  | string | **Recommended for revenue related events. ** 

     The ISO 4217 currency code.   
Examples: `EUR`, `USD`, `JPY`.  
**List of currencies currently supported**: `AED`, `ARS`, `AUD`, `BDT`, `BHD`, `BIF`, `BOB`, `BRL`, `CAD`, `CHF`, `CLP`, `CNY`, `COP`, `CRC`, `CZK`, `DKK`, `DZD`, `EGP`, `EUR`, `GBP`, `GTQ`, `HKD`, `HNL`, `HUF`, `IDR`, `ILS`, `INR`, `ISK`, `JPY`, `KES`, `KHR`, `KRW`, `KWD`, `KZT`, `MAD`, `MOP`, `MXN`, `MYR`, `NGN`, `NIO`, `NOK`, `NZD`, `OMR`, `PEN`, `PHP`, `PHP`, `PKR`, `PLN`, `PYG`, `QAR`, `RON`, `RUB`, `SAR`, `SEK`, `SGD`, `THB`, `TRY`, `TWD`, `UAH`, `USD`, `VES`, `VND`, `ZAR` .  | ✅ |  |
| value {+Conditional} | float | **Recommended for revenue related events. ** 
 
 Value of the order or items sold. 
 The value should always be formatted as an integer or decimal (for instance, 10.00) regardless of the location, currency, or other factors. It should not contain any currency symbols, special characters, letters, or commas.   
**Note**: `price` specifies the price for a single item, and `value` specifies the total price of the order. For example, if you have two items each sold for ten dollars, the `price` parameter would be `10.00` and the `value` parameter would be `20.00`.   |  ✅|  |
|num_items|integer| The quantity of items.| | |
|search_string|string|The user-entered string for search.| | |
| description | string | Description of the item or page. |  |  |
| order_id | string | Order ID.   |  |  |
| shop_id | string | Shop ID.   |  |  |
|customer_type|string|**Only for app and web events.**

A categorical label indicating the customer segment associated with the conversion event.

Enum values: 
- `new`: A new customer.
- `returning`: A returning customer.| | |
```
#### `contents` parameters
```xtable
| Field {20%}| Data Type {10%}| Description{40%} |Required for reporting Return on Ad Spend (ROAS) or for Value-based Optimization (VBO){15%} |Required for Video Shopping Ads (VSA){15%} |
|---|---|---|---|---|
| price | float | The price of the item.  
**Note**: `price` specifies the price for a single item, and `value` specifies the total price of the order. For example, if you have two items each sold for ten dollars, the `price` parameter would be `10.00` and the `value` parameter would be `20.00`.   
 Example: `10`, `10.5`.   |  |  |
| content_id {+Conditional} | string | Unique ID of the product or content.  
We recommend using `sku_id` or `item_group_id` if you have one.  
 If you have set up `sku_id` or `item_group_id` in the catalog, the ID should match the `sku_id` or `item_group_id`.   |  | ✅ |
| content_category| string | Category of the page or product.   |  |  |
| content_name | string | Name of the page or product.   |  |  |
| brand | string | Brand name of the product item.   |  |  |
```

### `page` parameters
```xtable
| Field {20%}| Data Type {10%}| Description{50%} |Example{20%} |
|---|---|---|---|
| url {Required} | string | The browser URL where the event happened, for example, the value of `location.href` in the client side Javascript. 
It is recommended to use the full URL, including all URL parameters.   | `"http://demo.mywebsite.com/purchase?v=helloworld"` |
| referrer | string | The referrer URL.   
For example, [document.referrer ](https://developer.mozilla.org/en-US/docs/Web/API/Document/referrer) in the client side Javascript, or the server side [Referer http header](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Referer). 
 It is recommended to use the full URL, including all URL parameters. |`"http://demo.mywebsite.com/purchase"` |
```

### `app` parameters
Use the `app` parameters to share information about the advertiser's app with Events API 2.0. The `app` parameters should only be used when reporting App Events ( `event_source` = `app`).
> **Note**

> Reporting App Events using Events API 2.0 is currently an allowlist-only feature. If you would like to access it, please contact your TikTok representative.

```xtable
| Field {20%}| Data Type {10%}| Description{70%} |
|---|---|---|
| app_id {+Conditional} | string | **Required for app events. **
Mobile App ID. 
-  For iOS Apps, use the app ID found in the App Store URL  Example: Apple Store URL: `https://apps.apple.com/us/app/angry-birds/id343200656``id` = `"343200656"`
-  For Android Apps in the Google Play store, use the app ID found in the Google Play store URL.  Example: Google Play store URL: `https://play.google.com/store/apps/details?id=com.rovio.angrybird` `id` = `"com.rovio.angrybirds"` 
-  For Android Apps  not in the Google Play store, use the package name.|
| app_name | string | Application name. |
| app_version | string | App version number. 
Example: `"3.0.2"`. |
```

### `ad` parameters
Use the `ad` parameters to share information about the advertiser's app with Events API 2.0. The `ad` parameters should only be used when reporting App or website Events ( `event_source` = `app` or `web`).

> **Note**

> Reporting App Events using Events API 2.0 is currently an allowlist-only feature. If you would like to access it, please contact your TikTok representative.

```xtable
| Field {20%}| Data Type {10%}| Description{70%} |
|---|---|---|
| callback | string | **For app events only.**

Callback information to help attribute events |
| campaign_id | string | **For app events only.**

Campaign ID. |
| ad_id | string | **For app events only.**

Ad group ID. |
| creative_id | string | **For app events only.**

Ad ID. |
| is_retargeting | boolean | **For app events only.**

Whether the user is a retargeting user. |
| attributed | boolean | **For app events only.**

Whether the event is attributed. |
| attribution_type | string | **For app events only.**

Attribution type. |
| attribution_provider | string | **For app events only.**
Attribution provider. |
|attribution_share|float| **For app and web events only.**

Attribution share score.
A score provided by you per conversion, representing the portion of credit TikTok should receive for the conversion. A greater value indicates a larger credit share for TikTok. 

Examples:
- 0.0: No credit.
- 0.5: Partial credit.
- 1.0: Full credit.|
```

### `lead` parameters
Use the `lead` parameters to share information about the leads in a CRM system with Events API 2.0. The `lead` parameters should only be used when reporting CRM Events (`event_source` = `crm`).

```xtable
| Field {20%}| Data Type {10%}| Description{70%} |
|---|---|
| lead_id {+Conditional} | string |** Required for CRM events. **
ID of TikTok leads. 
 Every lead will have its `lead_id` when exported from TikTok. 
To obtain the ID of a lead, download the lead by using the endpoints [/page/lead/task/](https://business-api.tiktok.com/portal/docs?id=1739052936772610) and [/page/lead/task/download/](https://business-api.tiktok.com/portal/docs?id=1739053563877378), or export the lead from TikTok Leads Center, the first-party CRM platform located within TikTok Ads Manager. |
| lead_event_source | string | Lead event source. 
You can set this field to the name of your CRM system, such as HubSpot or Salesforce. |
```
### Example
#### Reporting Web Events
```xcodeblock
 (code curl http)

curl --location --request POST 'https://business-api.tiktok.com/open_api/v1.3/event/track/' \
--header 'Access-Token: {{Access-Token}}' \
--header 'Content-Type: application/json' \
--data-raw '{
  "event_source": "web",
  "event_source_id": "{{PIXEL-CODE}}",
  "data": [
    {
      "event": "Purchase",
      "event_time": 1687758765,
      "event_id": "12345",
      "user": {
        "external_id": "user_12345678",
        "phone": "0c7e6a405862e402eb76a70f8a26fc732d07c32931e9fae9ab1582911d2e8a3b",
        "email": "123456405862e402eb76a70f8a26fc732d07c32931e9fae9ab1582911d2e8a3b",
        "ip": "123.456.789.1",
        "user_agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.6.1 Safari/605.1.15",
        "locale": "en_US"
      },
      "properties": {
        "currency": "USD",
        "value": 200.0,
        "content_type": "product",
        "description": "some product decription",
        "contents": [
          {
            "price": 100.0,
            "quantity": 2,
            "content_id": "12345",
            "content_name": "Fancy-AirMax2.0 Black",
            "content_category": "Shoes - Running Shoes",
            "brand": "Fancy Sneakers"
          }
        ]
      }
    }
  ]
}'

 (/code)
```
#### Reporting Offline Events
```xcodeblock
 (code curl http)

curl --location --request POST 'https://business-api.tiktok.com/open_api/v1.3/event/track/' \
--header 'Access-Token: {{Access-Token}}' \
--header 'Content-Type: application/json' \
--data-raw '{
  "event_source": "offline",
  "event_source_id": "{{Offline-Event-Set-ID}}",
  "data": [
    {
      "event": "Purchase",
      "event_time": 1684574395,
      "user": {
        "email": ["848a771458438fc2ec420560d769fb9b9b86851ee338ec56517baabd79d3bb4f",
        "dd6ff77f54e2106661089bae4d40cdb600979bf7edc9eb65c0942ba55c7c2d7f"],
        "phone": ["2f9d2b4df907e5c9a7b3434351b55700167b998a83dc479b825096486ffcf4ea"]
      },
      "properties": {
        "order_id": "abc_xyz",
        "shop_id": "123abc",
        "contents": [
          {
            "price": 8,
            "quantity": 2,
            "content_id": "1077218",
            "content_name": "running shoes",
            "content_category": "Shoes > Sneakers > running shoes",
            "brand": "your_brand_name"
          },
          {
            "price": 30,
            "quantity": 1,
            "content_id": "1197218",
            "content_name": "running shoes",
            "content_category": "Shoes > Sneakers > running shoes",
            "brand": "your_brand_name"
          }
        ],
        "content_type": "product",
        "currency": "USD",
        "value": 46.00
      }
    }
  ]
}'

 (/code)
```
#### Reporting App Events
```xcodeblock
 (code curl http)

curl --location --request POST 'https://business-api.tiktok.com/open_api/v1.3/event/track/' \
--header 'Access-Token: {{ACCESS_TOKEN}}' \
--header 'Content-Type: application/json' \
--data-raw '{
  "event_source": "app",
  "event_source_id": "{{TIKTOK_APP_ID}}",
  "data": [
    {
      "event": "InstallApp",
      "event_time": 1687758765,
      "user": {
        "phone": "{{HASHED_PHONE}}",
        "email": "{{HASHED_EMAIL}}",
        "idfa": "{{IDFA}}",
        "idfv": "{{IDFV}}",
        "gaid": "{{GAID}}",
        "att_status": "AUTHORIZED",
        "locale": "en-US"
      },
      "app": {
        "app_id": "com.test.flyingsneakers",
        "app_name": "Flying Sneakers",
        "app_version": "3.0.2"
      },
      "ad": {
        "attributed": true,
        "callback": "{{CALLBACK}}",
        "campaign_id": "1700817380525057",
        "ad_id": "1700817380806706",
        "creative_id": "1700817378256945",
        "is_retargeting": false,        
        "attribution_type": "click_through"
      },
      "properties": {
        "currency": "USD",
        "value": 200.0,
        "content_type": "product",
        "contents": [
          {
            "price": 100.0,
            "quantity": 2,
            "content_id": "12345",
            "content_name": "Fancy-AirMax2.0 Black",
            "content_category": "Shoes - Running Shoes",
            "brand": "Fancy Sneakers"
          }
        ]
      }
    }
  ]
}'

 (/code)
```
#### Reporting CRM Events
##### With required fields only
```xcodeblock
 (code curl http)

curl --location --request POST 'https://business-api.tiktok.com/open_api/v1.3/event/track/' \
--header 'Access-Token: {{ACCESS_TOKEN}}' \
--header 'Content-Type: application/json' \
--data-raw '{
  "event_source": "crm",
  "event_source_id": "{{CRM-Event-Set-ID}}",
  "data": [
    {
      "event": "AddToCart",
      "event_time": 1687673101,
      "lead": {
        "lead_id": "{{lead_id}}"
      }
    }
  ]
}'

 (/code)
```
##### With required and optional fields
```xcodeblock
 (code curl http)

curl --location --request POST 'https://business-api.tiktok.com/open_api/v1.3/event/track/' \
--header 'Access-Token: {{ACCESS_TOKEN}}' \
--header 'Content-Type: application/json' \
--data-raw '{
  "event_source": "crm",
  "event_source_id": "{{CRM-Event-Set-ID}}",
  "data": [
    {
      "event": "AddToCart",
      "event_time": 1687673101,
      "lead": {
        "lead_id": "{{lead_id}}",
        "lead_event_source": "Salesforce"
      }
      "user": {
        "external_id": "{{external_id}}",
        "phone": "0c7e6a405862e402eb76a70f8a26fc732d07c32931e9fae9ab1582911d2e8a3b",
        "email": "0c7e6a405862e402eb76a70f8a26fc732d07c32931e9fae9ab1582911d2e8a3b"
      },
      "event_id": "{{event_id}}",
    }
  ]
}'

 (/code)
```
## Response
> **Note**

> When conducting tests, pay attention to the `code` and `message` fields. If the `code` is not `0`, it indicates an error, and the `message` field will provide a description of the error.

```xtable
|Field{30%}|Data Type{15%}|Description{55%}|
|-|-|-|
|code |number|Response code. For the complete list of response codes and descriptions, see [Appendix-Return Code](https://ads.tiktok.com/marketing_api/docs?id=1737172488964097). |
|message|string|Response message. For details, see [Appendix - Return Codes](https://ads.tiktok.com/marketing_api/docs?id=1737172488964097).|
|request_id |string|The log ID of a request, which uniquely identifies the request.  |
|data |object|Returned data.|

```
### Example
```xcodeblock
 (code curl http)

HTTPS/1.1 200 OK
{
  "code": 0, 
  "message": "OK", 
  "request_id": "{{request_id}}", 
  "data": {}
}

 (/code)
```
