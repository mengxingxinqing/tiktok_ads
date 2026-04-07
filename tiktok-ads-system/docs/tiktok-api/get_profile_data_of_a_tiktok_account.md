# Get profile data of a TikTok account

**Doc ID**: 1762228399168514
**Path**: API Reference/Accounts/Insights/Get profile data of a TikTok account

---

Use this endpoint to access detailed analytics and insights about a TikTok account's follower base and profile engagement. 

> **Note**

> To ensure proper use of the Accounts API, starting March 20, 2026 at 00:00 (GMT+0), developers must complete the [Accounts API Access Application Form](https://bytedance.sg.larkoffice.com/share/base/form/shrlgu4WEvtSXpEDLcCw56u4Rfc) before submitting a new developer app or requesting a scope increase that includes the "TikTok Accounts" permission scope. Please follow the instructions carefully and provide clear, accurate information to help facilitate the application review process. For more details on Accounts API use cases, please refer to the [Accounts API](https://business-api.tiktok.com/portal/docs?id=1737944384433218) documentation.

>**Note**

> - There is a 24-48 hour delay for some profile level metrics. To find the data latencies, you can check out the description in the Response table or see [Accounts Insights data latency- Reference table for data latency](https://ads.tiktok.com/marketing_api/docs?id=1746624508278786#item-link-Reference%20table%20for%20data%20latency).
> - The data you can get from `/business/get/` depends on whether you can see the corresponding TikTok Analytics data available in the app and at [https://www.tiktok.com/analytics](https://www.tiktok.com/analytics). If the corresponding metric data are missing from TikTok Analytics, you will not be able to get the data. 
> 	- To learn about the TikTok Analytics platform (TikTok Studio or Business Analytics) that each metric corresponds to, see the field description for each metric in the response.
> 	- To view insights and analytics data, TikTok account owners need to first publish at least one video, then tap the "Turn On" button on the Analytics page of their mobile TikTok app. For more information, refer to [here](https://www.tiktok.com/feedback?id=7133058093574806018&lang=en&type=).
> - The video view data you obtain from `/business/get/` via the field `video_views` represents a total metric, encompassing both organic and paid activities.

## Comparing v1.2 and v1.3
The following table outlines the differences between v1.2 and v1.3 endpoints.
```xtable
|Changes {33%}|v1.2 {33%}|v1.3 {33%}|
|---|---|---|
|Endpoint path|/v1.2/business/get/|/v1.3/business/get/|
|Method|POST|GET|
|New response parameters|/|`is_business_account`
`bio_description`
`profile_deep_link`
`is_verified`
`following_count`
`total_likes`
`videos_count`
`unique_video_views`
`phone_number_clicks`
`lead_submissions`
`app_download_clicks`
`bio_link_clicks`
`email_clicks`
`address_clicks`
`daily_total_followers`
`daily_new_followers`
`daily_lost_followers`
`audience_ages`
`audience_cities`
`engaged_audience`|
```

## Request
**Endpoint** https://business-api.tiktok.com/open_api/v1.3/business/get/

**Method** GET

**Header**

```xtable
|Field{30%}|Data Type{15%}|Description{55%}|
|---|---|---|
|Access-Token {Required}|string|Authorized access token. For details, see [Authentication](https://business-api.tiktok.com/portal/docs?id=1738373164380162). |
```

**Parameters**

Pass params as url parameters.
``` xtable
|Field{30%}|Data Type{15%}|Description{55%}|
|--- |--- |--- |
| business_id {Required} | string | Application specific unique identifier for the TikTok account. 
Pass the value of the `open_id` field returned in the response of [/tt_user/oauth2/token/](https://business-api.tiktok.com/portal/docs?id=1833997638479041) to this field.|
| start_date | string | Query start date, closed interval, format such as: 2021-06-01. The date is based on the UTC time zone.
 If not set, then the `start_date` will be [current date - 7 days]. 
 The maximum supported look-back period is 60 days. |
| end_date | string | Query end date, closed interval, format such as: 2021-06-01. The date is based on the UTC time zone. 
 If not set, then `end_date` will be [current date - 1 day]. |
| fields | string[] | Requested fields. If not set, returns the **default** fields only.  
Default fields: `["display_name", "profile_image"]` 
 
To retrieve certain fields in the response, you must have specific permissions. You can check the **"Required permission"** column for each field in the response schema to determine the permissions needed. 
To confirm that you have the necessary permission scope, you can check the scope returned by the [/tt_user/token_info/get/](https://ads.tiktok.com/marketing_api/docs?id=1765927978092545) endpoint. If the required permission has not been granted to you, follow the steps outlined in [Authorization](https://ads.tiktok.com/marketing_api/docs?id=1738083939371009) to enable the TikTok account user to reauthorize your app with the permission.
 
**Example**: `["display_name", "profile_image"]`. 
 
** Supported fields**: 
- `is_business_account`：Whether the TikTok account is a TikTok Business Account. This metric is only available when the TikTok account user has granted you the new permission scope "user.account.type". 
**Note**: To determine whether you have obtained the permission scope "user.account.type", you can check the `scope` returned from [/tt_user/token_info/get/](https://ads.tiktok.com/marketing_api/docs?id=1765927978092545). If the permission scope has not been granted to you, follow the steps outlined in [Authorization](https://ads.tiktok.com/marketing_api/docs?id=1738083939371009) to enable the TikTok account user to reauthorize your app with the permission scope.
- `profile_image`: The URL to the profile photo of the TikTok account.
- `username`: The username (handle) of the TikTok account.
- `profile_deep_link`: The link to the profile page of the TikTok account.
- `display_name`: The display name (nickname) of the TikTok account.
- `bio_description`: The bio description of the TikTok account. 
- `is_verified`: Whether TikTok has provided a verified badge to the TikTok account after confirming that it belongs to the user it represents.
- `following_count`: The number of accounts that the TikTok account is following. 
- `followers_count`: The number of followers for the TikTok account. 
**Note**: If you specify `followers_count` in the value of `fields`, you will obtain `followers_count` as both a lifetime metric and a daily metric in the response.
- `total_likes`: Total likes. The total number of times people have liked your published videos.
- `videos_count`: The lifetime number of public videos posted by the TikTok account. 
- `video_views`: Daily video views. The daily number of times your videos have been viewed. 
**Note**:  Counts when playback duration >0 and the playback is the first playback in an impression session. 
-  If the user swipes away from the ad then swipes back, it would be counted as 2 impressions. Therefore, a new video view will be counted again with the new impression session.   
- `unique_video_views`: Daily reached audience. The daily number of people who watched your published content at least once.  
- `profile_views`: Daily profile views. The daily number of clicks on your profile from users.
- `likes`: Daily likes. The daily number of times people have liked your published videos.
- `comments`: Daily comments. The daily number of times people have commented on your published videos. 
- `shares`: Daily shares. The daily number of times people have shared your published videos. 
- `phone_number_clicks`: Daily phone number clicks. The daily number of clicks collected on your phone number link in the selected date range.  
- `lead_submissions`: Daily lead submissions. The daily number of leads (e.g. price quotes, newsletter subscriptions, etc.) collected from your consumers in the selected date range.   
- `app_download_clicks`: Daily app download link clicks. The daily number of clicks collected on your app download link in the selected date range. 
- `bio_link_clicks`: Daily bio link clicks. The daily number of clicks collected on your link-in-bio during the selected time range.  
- `email_clicks`: Daily email clicks. The daily number of clicks collected on the Email button on your profile during the selected time range.  
- `address_clicks`: Daily address clicks. The daily number of clicks collected on the Address button on your profile during the selected time range. 
- `daily_total_followers`: Daily net growth. The daily change in the number of followers.   
- `daily_new_followers`: Daily new followers. The daily number of new followers you have gained.   
- `daily_lost_followers`: Daily lost followers. The daily number of followers you have lost. 
- `audience_activity`: Hourly follower activity. The hourly breakdown of followers active on TikTok during the day.The data for this metric is only available for TikTok accounts with at least 100 followers.
- `engaged_audience`: Daily engaged audience. The daily number of people who engaged (liked, commented or shared) with at least one of your published content.  
- `audience_ages`: Follower age. The distribution of your followers by age. This demographic data is based on a number of factors, including information users provide in their profiles. The data for this metric is only available for TikTok accounts with at least 100 followers. 
- `audience_genders`: Follower gender. The distribution of your followers by gender. This demographic data is based on a number of factors, including information users provide in their profiles.The data for this metric is only available for TikTok accounts with at least 100 followers.
- `audience_countries`: Follower top countries or regions. The distribution of your followers by their location (countries or regions). This demographic data is based on a number of factors, including information users provide in their profiles.The data for this metric is only available for TikTok accounts with at least 100 followers. 
- `audience_cities`: Follower top cities. The distribution of your followers by their cities. This demographic data is based on a number of factors, including information users provide in their profiles.The data for this metric is only available for TikTok accounts with at least 100 followers. |
```

### Example
```xcodeblock
(code curl http)
curl --location -g --request GET 'https://business-api.tiktok.com/open_api/v1.3/business/get/?business_id=b3d2f73d-4b8c-47fb-85c3-cd571287754b&fields=["username","display_name","shares","comments", "video_views", "audience_countries"]&start_date=2021-07-28&end_date=2021-08-01' \
--header 'Access-Token: 1234a16d2e08c3f17d1984a1be07d00406p3LIAF7vEpxliox8GRpCINv70x'
(/code)
```
## Response

**Header**

These are important headers to record for issue reports and troubleshooting. This is not an exhaustive list of response headers.
```xtable
|Field {20%}|Data Type {20%}|Description {60%}|
|---|---|---|
|Date|string|Date and time (GMT) when the response was received.

**Example**: Fri, 13 Aug 2021 08:04:42 GMT|
|X-Tt-Logid|string|Unique identifier for the API request.|
```

**Body**
``` xtable
|Field{25%}|Type{15%}|Description{40%}|Required permission {20%}|
|---|---|---|---|
| request_id | string | Unique identifier for the API request. 
**Note**: Please record this field for all API requests. Important for issue reports and troubleshooting. ||
| code | integer | Response code. For the complete list of response codes and descriptions, see [Appendix - Return Codes](https://ads.tiktok.com/marketing_api/docs?id=1737172488964097). ||
| message | string | Response message. For details, see [Appendix - Return Codes](https://ads.tiktok.com/marketing_api/docs?id=1737172488964097). ||
| data | object | Return data ||
#| is_business_account| boolean | Whether the TikTok account (`business_id`) is a TikTok Business Account. 
Enum values: 
-  `true`: The TikTok account is a TikTok Business Account.
-  `false`: The TikTok account is a TikTok Personal Account. | `user.account.type` |
#|profile_image | string | Temporary URL for profile photo of the TikTok account. Expiration date-time included in x-expires query param as Epoch/Unix time in seconds.  
 
**Example**: https://p16-sign-va.tiktokcdn.com/tos-maliva-avt-0068/75dec21d63500917fb6ec8bc59415156~c5_300x300.jpeg?x-expires=1614099600&x-signature=PmK%2BWs3LzSzRL2tYs%2FZx7EjG3Gk%3D  
 
**Updated in**: Real-time  |`user.info.basic` |
#|username | string | The username (handle) of the TikTok account. 
 
**Example**: la_flama_blanca  
 
**Updated in**: Real-time   |`user.info.username` |
#| profile_deep_link | string | The link to the profile page of the TikTok account. 
 
**Example**: https://vm.tiktok.com/ABcdEfghi/  
 
**Updated in**: Real-time | `user.info.profile` |
#|display_name | string | The display name  (nickname) for the TikTok account.
 
**Example**: La Flama Blanca  
 
**Updated in**: Real-time | `user.info.basic` |
#| bio_description | string | The bio description of the TikTok account. 
 
**Updated in**: Real-time 

**Note**: If you have not set a bio for the TikTok account, the value of this field will be an empty string (`""`).| `user.info.profile` |
#| is_verified | boolean | Whether TikTok has provided a verified badge to the TikTok account after confirming that it belongs to the user it represents.
 
Supported values: `true`, `false`. 
 
**Example**: `true` 
 
**Updated in**: Real-time | `user.info.profile` |
#| following_count | integer | The lifetime number of accounts that the TikTok account is following. 
 
**Example**: 2  
 
**Updated in**: Real-time| `user.info.stats` |
#|followers_count | integer | The total number of followers for the TikTok account.  
 
**Example**: 123  
 
**Updated in**: Real-time  |`user.info.stats` |
#| total_likes | integer |Total likes. 
 The total number of times people have liked your published videos. 
 
**Example**: 6 
 
**Updated in**: Real-time| `user.info.stats` |
#| videos_count | integer | The lifetime number of public videos posted by the TikTok account. 
 
**Example**: 6 
 
**Updated in**: Real-time| `user.info.stats` |
#|metrics | object[] | All requested daily metrics. 
 
**Note**: Metrics data will only be returned for dates after the TikTok Account was created. There can be up to a **24-48 hour delay** in metrics availability. | |
##| date | string | The date for this set of daily metrics - in YYYY-MM-DD format - in UTC time zone.  
 
**Example**: 2021-08-12  
 
**Updated in**: T + 24-48 hrs (UTC time) |N/A |
##| video_views | integer | Daily video views. 
The daily number of times your videos have been viewed.

**Note**: 
-  Counts when playback duration >0 and the playback is the first playback in an impression session. 
-  If the user swipes away from the ad then swipes back, it would be counted as 2 impressions. Therefore, a new video view will be counted again with the new impression session.  
 **Data source**: TikTok Studio.
 
**Example**: 123  
 
**Updated in**: T + 24-48 hrs (UTC time)  |`user.insights` |
##| unique_video_views | integer | Daily reached audience.
 The daily number of people who watched your published content at least once. 

 **Data source**: Business Analytics.
 
**Example**: 123 

**Updated in**: T + 24-48 hrs (UTC time) 

**Note**: The data for this metric is only available for Business Accounts.| `user.insights` |
##| profile_views | integer | Daily profile views. 
The daily number of clicks on your profile from users. 

**Data source**: TikTok Studio.
 
**Example**: 123  
 
**Updated in**: T + 24-48 hrs (UTC time)  |`user.insights` |
##| likes | integer | Daily likes.  
 The daily number of times people have liked your published videos. 

**Data source**: TikTok Studio.
 
**Example**: 123  
 
**Updated in**: T + 24-48 hrs (UTC time)  

**Note**:  The likes count displayed in this field does not subtract unlikes (likes that are removed or withdrawn later). There may be a discrepancy between this value and the likes displayed on the **Business Suite** > **Analytics** page for Business Accounts.
For example, if a post receives 30 likes and 10 unlikes:
- This field will show 30 likes.
- The Analytics page for Business Accounts will show 20 likes (30 likes - 10 unlikes).  |`user.insights` |
##| comments | integer | Daily comments. 
The daily number of times people have commented on your published videos. 

**Data source**: TikTok Studio.
 
**Example**: 123  
 
**Updated in**: T + 24-48 hrs (UTC time)  |`user.insights` |
##| shares | integer | Daily shares. 
The daily number of times people have shared your published videos.

**Data source**: TikTok Studio.
 
**Example**: 123  
 
**Updated in**: T + 24-48 hrs (UTC time)   |`user.insights` |
##| phone_number_clicks | integer | Daily phone number clicks.
 The daily number of clicks collected on your phone number link in the selected date range.

**Data source**: Business Analytics. 

**Example**: 123 

**Updated in**: T + 24-48 hrs (UTC time)  

**Note**: The data for this metric is only available for [Registered Business Accounts](https://ads.tiktok.com/help/article/about-business-registration).| `user.insights` |
##| lead_submissions | integer | Daily lead submissions.
 The daily number of leads (e.g. price quotes, newsletter subscriptions, etc.) collected from your consumers in the selected date range. 

**Data source**: Business Analytics. 

**Example**: 123 

**Updated in**: T + 24-48 hrs (UTC time)  

**Note**: The data for this metric is only available for [Registered Business Accounts](https://ads.tiktok.com/help/article/about-business-registration).   | `user.insights` |
##| app_download_clicks | integer | Daily app download link clicks.
The daily number of clicks collected on your app download link in the selected date range. 

**Data source**: Business Analytics. 

**Example**: 123 

**Updated in**: T + 24-48 hrs (UTC time) 

**Note**: The data for this metric is only available for [Registered Business Accounts](https://ads.tiktok.com/help/article/about-business-registration).  | `user.insights` |
##| bio_link_clicks | integer | Daily bio link clicks.
 The daily number of clicks collected on your link-in-bio during the selected time range.

**Data source**: Business Analytics. 

**Example**: 123 

**Updated in**: T + 24-48 hrs (UTC time) 

**Note**: The data for this metric is only available for [Registered Business Accounts](https://ads.tiktok.com/help/article/about-business-registration).   | `user.insights` |
##| email_clicks | integer | Daily email clicks..
 The daily number of clicks collected on the Email button on your profile during the selected time range. 

**Data source**: Business Analytics. 

**Example**: 123 

**Updated in**: T + 24-48 hrs (UTC time)  

**Note**: The data for this metric is only available for [Registered Business Accounts](https://ads.tiktok.com/help/article/about-business-registration). | `user.insights` |
##| address_clicks | integer | Daily address clicks.
 The daily number of clicks collected on the Address button on your profile during the selected time range.

**Data source**: Business Analytics. 

**Example**: 123 

**Updated in**: T + 24-48 hrs (UTC time)

**Note**: The data for this metric is only available for [Registered Business Accounts](https://ads.tiktok.com/help/article/about-business-registration).  | `user.insights` |
##| daily_total_followers | integer | Daily net growth.
The daily change in the number of followers.

**Data source**: Business Analytics. 

**Example**: 123 

**Updated in**: T + 24-48 hrs (UTC time)  
 
**Note**: The data for this metric is only available for Business Accounts| `user.insights` |
##|  daily_new_followers | integer |Daily new followers. 
The daily number of new followers you have gained.

**Data source**: Business Analytics.

**Example**: 123 

**Updated in**: T + 24-48 hrs (UTC time) 
 
**Note**: The data for this metric is only available for Business Accounts | `user.insights` |
##| daily_lost_followers | integer | Daily lost followers.
The daily number of followers you have lost.

**Data source**: Business Analytics. 

**Example**: 123 

**Updated in**: T + 24-48 hrs (UTC time) 
 
**Note**: The data for this metric is only available for Business Accounts | `user.insights` |
##| followers_count | integer | The total number of people who are following your account on the date. 

**Data source**: TikTok Studio.
 
**Example**: 123  
 
**Updated in**: T + 24-48 hrs (UTC time)  |`user.insights` |
##| audience_activity | object[] | Hourly follower activity. The hourly breakdown of followers active on TikTok during the day in UTC+0 time zone.  

**Note**: The data for this metric is only available for Business Accounts with at least 100 followers. 

**Data source**: TikTok Studio.
 
**Example**: `[{"hour": "0", "count": 12}, {"hour": "1", "count": 18}, {"hour": "2", "count": 23}, {"hour": "3", "count": 28}, ...]`  
 
**Updated in**: T + 24-48 hrs (UTC time)   |`user.insights` |
###| hour | string | The specific hour in the day. | |
###| count | integer | The number of followers active on TikTok during the hour. | |
##| engaged_audience | integer | Daily engaged audience. 
The daily number of people who engaged (liked, commented or shared) with at least one of your published content.

**Data source**: Business Analytics.
 
**Note**: The data for this metric is only available for Business Accounts.| `user.insights` |
#| audience_ages | object[] |Follower age. 
The distribution of your followers by age. This demographic data is based on a number of factors, including information users provide in their profiles..
 
**Updated in**: T + 24-48 hrs (UTC time)

**Data source**: TikTok Studio

**Note**: The data for this metric is only available for TikTok accounts with at least 100 followers.| `user.insights` |
##| age | string | Age group.   

 Enum values: `18-24`, `25-34`, `35-44`, `45-54`, `55+`.   ||
##| percentage | float | Percentage of followers associated with the age group.   ||
#|audience_genders | object[] | Follower gender. 
The distribution of your followers by gender. This demographic data is based on a number of factors, including information users provide in their profiles.

**Note**: The data for this metric is only available for TikTok accounts with at least 100 followers.
 
**Data source**: TikTok Studio

**Example**: `[{gender: "Female", percentage: 0.7554470336505679}, {gender: "Male", percentage: 0.24455296634943213}, ...]`  
 
**Updated in**: T + 24-48 hrs (UTC time)  |`user.insights` |
##| gender | string | Gender. 

Enum values: `Female`, `Male`, `Other`. | |
##| percentage | float | Percentage of followers associated with the gender. | |
#|audience_countries | object[] | Follower top countries or regions. 
The distribution of your followers by their location (countries or regions). This demographic data is based on a number of factors, including information users provide in their profiles.
 
**Data source**: TikTok Studio

**Note**: The data for this metric is only available for TikTok accounts with at least 100 followers. 
 
**Example**: `[{country: "US", percentage: 0.7554470336505679}, {country: "UK", percentage: 0.24455296634943213}, ...]`  
 
**Updated in**: T + 24-48 hrs (UTC time)|`user.insights` |
##| country | string | [ISO 3166-1 alpha-2](https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2#Officially_assigned_code_elements) country or region code. | |
##| percentage | float | Percentage of followers registered from a specified country or region. | |
#| audience_cities | object[] | Follower top cities. 
The distribution of your followers by their cities. This demographic data is based on a number of factors, including information users provide in their profiles. 
 
**Data source**: TikTok Studio
 
**Updated in**: T + 24-48 hrs (UTC time)

**Note**: The data for this metric is only available for TikTok accounts with at least 100 followers. | `user.insights` |
##| city_name | string | City name.   | |
##| percentage | float | Percentage of followers associated with the city.   | |
```

### Example
```xcodeblock
(code curl http)
HTTPS/1.1 200 OK
{
    "code": 0,
    "message": "OK",
    "request_id": "202108030711080102450310564DA3B2EB",
    "data": {
        "profile_image": "https://p16-sign-va.tiktokcdn.com/tos-maliva-avt-0068/188d468fc1de3f328250ea0c96e98f8b~c5_100x100.webp?x-expires=1628060400&x-signature=BnPoX8rWsYZZ%2BtyzCoWanxYdRyg%3D",
        "username": "la_flama_blanca",
        "display_name": "Display Name",
        "followers_count": 1124,
        "audience_countries": [
            {
                "percentage": 0.1797,
                "country": "MY"
            },
            {
                "percentage": 0.5996,
                "country": "TW"
            },
            {
                "percentage": 0.0629,
                "country": "VN"
            }
        ],
        "audience_genders": [
            {
                "percentage": 0.6031,
                "gender": "Female"
            },
            {
                "percentage": 0.1685,
                "gender": "Male"
            },
            {
                "percentage": 0.2283,
                "gender": "Other"
            }
        ],
        "metrics": [
            {
                "date": "2021-07-30",
                "followers_count": 4,
                "video_views": 1126,
                "comments": 4,
                "shares": 0,
                "likes": 26
            },
            {
                "date": "2021-07-31",
                "followers_count": 6,
                "video_views": 312,
                "comments": 0,
                "shares": 0,
                "likes": 15
            },
            {
                "date": "2021-08-01",
                "followers_count": 8,
                "video_views": 283,
                "comments": 0,
                "shares": 0,
                "likes": 19
            }
        ]
    }
}
(/code)
```
## Field permission changelog
The permissions required to access certain fields have been updated. Refer to the table below for the changelog. 

To ensure a smooth API integration, we recommend you follow the steps outlined in [Authorization](https://ads.tiktok.com/marketing_api/docs?id=1738083939371009) to enable the TikTok account user to reauthorize your app with the updated permission as soon as possible.

To confirm that you have the necessary permission scope, you can check the scope returned by the [/tt_user/token_info/get/](https://ads.tiktok.com/marketing_api/docs?id=1765927978092545) endpoint.

  
| 
    Field | 
    Previous permission | 
    Existing permission | 
    Updated Time | 
   |

  
| 
    is_business_account | 
    `user.account.type` | 
    `user.account.type` | 
    - | 
   |
  
| 
    username | 
    `user.info.basic`
 | 
	`user.info.username` | 
    June, 2023 | 
   |
  
| 
    display_name | 
    `user.info.basic`
 | 
    - | 
   |
  
| 
    profile_image | 
    - | 
   |
  
| 
    followers_count | 
    `user.info.stats` | 
    June, 2023 | 
   |
  
| 
    audience_countries | 
    `user.insights` | 
    `user.insights`
 | 
    - | 
   |
  
| 
    audience_genders | 
    - | 
   |
  
| 
    metrics.followers_count | 
    - | 
   |
  
| 
    metrics.profile_views | 
    - | 
   |
  
| 
    metrics.video_views | 
    - | 
   |
  
| 
    metrics.likes | 
    - | 
   |
  
| 
    metrics.comments | 
    - | 
   |
  
| 
    metrics.shares | 
    - | 
   |
  
| 
    metrics.audience_activity | 
    - | 
   |
  
| 
    metrics.date | 
    N/A | 
    N/A | 
    - | 
   |
