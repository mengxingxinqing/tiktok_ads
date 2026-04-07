# Product set  operators and fields

**Doc ID**: 1740673108747265
**Path**: Marketing API/Catalog Management/Guides/Create catalogs and add products/Product set  operators and fields

---

This article lists the operators and the filter fields you can pass to `operation` and `field` respectively when calling [/catalog/set/create/](https://ads.tiktok.com/marketing_api/docs?id=1740572891104257) or [/catalog/set/update/](https://ads.tiktok.com/marketing_api/docs?id=1740572974725122).

### Operators
```xtable
| Operator {23%} | Definition{25%} | Details {52%} |
| -------- | ---------- | ------- |
| EQUAL | Equal to | Can only be used with a single value (string, int/long, float) |
| NOT_EQUAL | Not equal to | Can only be used with a single value (string, int/long, float) |
| GT | Greater than | Can only be used with a single value (string, int/long, float) |
| LT | Less than | Can only be used with a single value(string, int/long, float) |
| GTE | Greater than or equal | Can only be used with a single value (string, int/long, float) |
| LTE | Less than or equal | Can only be used with a single value (string, int/long, float) |
| CONTAIN | Contains a value in the list
 (case-sensitive) | Can be used with multiple values in a list (list<string>, list<int>, list<long>, list<float>) |
| I_CONTAIN | Contains a value in the list
 (case-insensitive) | Can be used with multiple values in a list (list<string>, list<int>, list<long>, list<float>) |
| EXCLUDE | Not equal to any value in the list 
(case-sensitive) | Can be used with multiple values in a list (list<string>, list<int>, list<long>, list<float>) |
| I_EXCLUDE | Not equal to any value in the list
 (case -insensitive) | Can be used with multiple values in a list (list<string>, list<int>, list<long>, list<float>) |
| NOT_EMPTY | Not empty | No values needed |
| WILDCARD | Contains a substring 
(case-sensitive) | You can specify a single value or multiple values. When multiple values are specified, the filter looks for strings that contain any value in the list. (string, list<string>)|
| I_WILDCARD | Contains a substring
 (case-insensitive) | You can specify a single value or multiple values. When multiple values are specified, the filter looks for strings that contain any value in the list. (string, list<string>) |
| NOT_WILDCARD | Not contains any substring
 (case-sensitive) | You can specify a single value or multiple values. When multiple values are specified, the filter looks for strings that do not contain any value in the list. (string, list<string>) |
| I_NOT_WILDCARD | Not contains any substring
 (case-insensitive) | You can specify a single value or multiple values. When multiple values are specified, the filter looks for strings that do not contain any value in the list. (string, list<string>) |
| PREFIX | Prefixed with a value
 (case-sensitive)  | You can specify a value or multiple values. When multiple values are specified, the filter looks for strings that are prefixed with any value. (string, list<string>) |
| I_PREFIX | Prefixed with a value
 (case-insensitive) | You can specify a value or multiple values. When multiple values are specified, the filter looks for strings that are prefixed with any value. (string, list<string>) |
```

### Filter fields

#### For E-commerce catalog product sets
```xtable
| Field{23%} | Description {25%}| Supported operators {22%}| Additional information{30%} |
| --- | --- | --- | --- |
| title | The title of the product. It can include words like "in sale". | EQUAL
NOT_EQUAL
WILDCARD
I_WILDCARD
NOT_WILDCARD
I_NOT_WILDCARD
PREFIX
I_PREFIX |  |
| description | The product description | EQUAL
NOT_EQUAL
WILDCARD
I_WILDCARD
NOT_WILDCARD
I_NOT_WILDCARD
PREFIX
I_PREFIX |  |
| availability | Product inventory status. | EQUAL
NOT_EQUAL | Supported values:
- `IN_STOCK`
- `AVAILABLE_FOR_ORDER`
- `PREORDER`
- `OUT_OF_STOCK`
- `DISCONTINUED` |
| brand | The product brand | CONTAIN
 I_CONTAIN
 EXCLUDE
 I_EXCLUDE
 WILDCARD
 I_WILDCARD
 NOT_WILDCARD
 I_NOT_WILDCARD
PREFIX
I_PREFIX |  |
| item_group_id | The SPU ID of the product | CONTAIN
I_CONTAIN
 EXCLUDE
I_EXCLUDE
 WILDCARD
I_WILDCARD 
NOT_WILDCARD
I_NOT_WILDCARD
PREFIX
I_PREFIX | Example: tiktok_1234_shirts |
| google_product_category | The product category. | CONTAIN
I_CONTAIN
EXCLUDE 
I_EXCLUDE
WILDCARD
 I_WILDCARD
NOT_WILDCARD
I_NOT_WILDCARD
PREFIX
I_PREFIX | Example: Apparel & Accessories > Clothing > Shirts |
| condition | The condition of the product in the shop | EQUAL
NOT_EQUAL | Supported values:
- `NEW`
- `REFURBISHED`
- `USED` |
| age_group | The audience age group | EQUAL
NOT_EQUAL | Supported values:
- `NEW_BORN`
- `INFANT`
- `TODDLER`
- `KIDS`
- `ADULT` |
| color | The product color | EQUAL
NOT_EQUAL
WILDCARD
I_WILDCARD
NOT_WILDCARD
I_NOT_WILDCARD
PREFIX
I_PREFIX |  |
| gender | The target gender of the product | EQUAL
NOT_EQUAL | Supported values:
- `MALE`
- `FEMALE`
- `UNISEX` |
| material | The material that the product is made of or made from. | EQUAL
NOT_EQUAL 
WILDCARD
 I_WILDCARD
NOT_WILDCARD
I_NOT_WILDCARD
PREFIX
I_PREFIX |  |
| pattern | The pattern or image that is on the product | EQUAL
NOT_EQUAL
WILDCARD
I_WILDCARD
NOT_WILDCARD
I_NOT_WILDCARD
PREFIX
I_PREFIX |  |
| product_type | The product type. Only the first three levels are needed. | CONTAIN
I_CONTAIN 
EXCLUDE
I_EXCLUDE
 WILDCARD
I_WILDCARD
NOT_WILDCARD
I_NOT_WILDCARD
PREFIX
I_PREFIX | Example: Apparel & Accessories > Clothing > Shirts |
| size | The product size | EQUAL
NOT_EQUAL
WILDCARD
I_WILDCARD
NOT_WILDCARD
I_NOT_WILDCARD
PREFIX
I_PREFIX | Example: small, L, XL |
| price | The cost price of the product. | GT
GTE
LT
LTE
EQUAL |  |
| sale_price | The sale price of the product. | GT
GTE
LT
LTE
EQUAL |  |
| sale_price_effective_start_date | The time when sales for this product start. | GT
GTE
LT
LTE
EQUAL | Format: 2017-12-31T0:00 |
| sale_price_effective_end_date | The time when the sales for this product end. | GT
GTE
LT
LTE
EQUAL | Format: 2017-12-31T0:00 |
| custom_label_(0\~4) | Additional information that you want to filter by. | CONTAIN
I_CONTAIN
 EXCLUDE
I_EXCLUDE
WILDCARD 
I_WILDCARD
NOT_WILDCARD 
I_NOT_WILDCARD
PREFIX
I_PREFIX |  |
```

#### For hotel catalog product sets
```xtable
| Field{24%} | Description {25%}| Supported operators {22%}| Additional information{29%} |
|---|---|---|---|
| hotel_id | A unique ID for the hotel |CONTAIN
I_CONTAIN
NOT_EQUAL
WILDCARD
I_WILDCARD
NOT_WILDCARD
I_NOT_WILDCARD
PREFIX
I_PREFIX | |
| availability | The current availability of the hotel room. | EQUAL
NOT_EQUAL | Supported values: 
- `IN_STOCK`: Available for booking.
- `OUT_OF_STOCK`: Unavailable for booking.|
| hotel_category | The category of the hotel. | EQUAL
NOT_EQUAL | Supported values: 
- `HOTEL`: Hotel. 
- `APARTMENT`: Apartment.
- `BOAT`: Boat.
- `CAMPSITE`: Campsite.
- `CAPSULE_HOTEL`: Capsule hotel.
- `GUESTHOUSE`: Guesthouse. 
- `HOMESTAY`: Homestay.
- `HOSTEL`: Hostel. 
- `LUXURY_TENT`: Luxury tent.
- `RESORT`: Resorts.
- `VILLA`: Villa. |
| brand | The brand name of the hotel. | NOT_EQUAL
CONTAIN |  |
| city | The city where the hotel is located. | CONTAIN
 I_CONTAIN
 NOT_EQUAL
 WILDCARD
 I_WILDCARD
 NOT_WILDCARD
 I_NOT_WILDCARD 
PREFIX
I_PREFIX  ||
| region | The region (state/province) where the hotel is located. | NOT_EQUAL 
CONTAIN  |   |
| margin_level | The percentage of the base price (`price`) for a hotel room that the hotel charges as deposit. | NOT_EQUAL 
CONTAIN  | Value range: 1-10. |
| guest_rating_score | The actual score of the hotel.

 This filter field filters products based on the product attribute field `score` within the object array `guest_ratings`. | GT
GTE
LT
LTE
EQUAL | Value range: ≥0. |
|guest_rating_number_of_reviewers | The number of guests who have reviewed the hotel.

This filter field filters products based on the product attribute field `number_of_reviewers` within the object array `guest_ratings`. | GT
GTE
LT
LTE
EQUAL | Value range: ≥0. |
|star_rating | The star rating of the hotel. | NOT_EQUAL
CONTAIN   |  |
| price | The base price for one night in the hotel room. | GT
GTE
LT
LTE
EQUAL  | |
| custom_label_0
custom_label_1
custom_label_2
custom_label_3
custom_label_4 | Additional information. |CONTAIN 
I_CONTAIN 
NOT_EQUAL 
EXCLUDE 
I_EXCLUDE 
WILDCARD
I_WILDCARD
NOT_WILDCARD
I_NOT_WILDCARD
PREFIX
I_PREFIX   | |
```

#### For flight catalog product sets
```xtable
| Field{24%} | Description {25%}| Supported operators {22%}| Additional information{29%} |
|---|---|---|---|
| availability | The current availability of the flight.|EQUAL
NOT_EQUAL | Supported values: 
- `IN_STOCK`: Available for booking.
- `OUT_OF_STOCK`: Unavailable for booking.|
| origin_airport | The origin airport of the flight, in the format of a three-letter IATA (International Air Transport Association) code. | CONTAIN
 I_CONTAIN
 NOT_EQUAL
 WILDCARD
 I_WILDCARD
NOT_WILDCARD
I_NOT_WILDCARD
PREFIX
I_PREFIX | Example: `AAR`. |
| destination_airport | The destination airport of the flight, in the format of a three-letter IATA code. | CONTAIN 
I_CONTAIN 
NOT_EQUAL 
WILDCARD 
I_WILDCARD 
NOT_WILDCARD 
I_NOT_WILDCARD
PREFIX
I_PREFIX | Example: `ABD`. |
| origin_city | The origin city of the flight. | CONTAIN 
I_CONTAIN 
NOT_EQUAL 
WILDCARD 
I_WILDCARD 
NOT_WILDCARD 
I_NOT_WILDCARD 
PREFIX
I_PREFIX| |
|destination_city | The destination city of the flight. | CONTAIN
I_CONTAIN
NOT_EQUAL
WILDCARD
I_WILDCARD
NOT_WILDCARD
I_NOT_WILDCARD
PREFIX
I_PREFIX| |
|airline_company | The name of the airline company operating the flight. | CONTAIN
I_CONTAIN
NOT_EQUAL
WILDCARD
I_WILDCARD
NOT_WILDCARD
I_NOT_WILDCARD
PREFIX
I_PREFIX|  |
| price | The base price for the flight. | GT
GTE
LT
LTE
EQUAL   | |
| custom_label_0
custom_label_1
custom_label_2
custom_label_3
custom_label_4 | Additional information. |CONTAIN 
I_CONTAIN 
NOT_EQUAL 
EXCLUDE 
I_EXCLUDE 
WILDCARD
I_WILDCARD
NOT_WILDCARD
I_NOT_WILDCARD
PREFIX
I_PREFIX   | |
```

#### For destination catalog product sets
```xtable
| Field{24%} | Description {25%}| Supported operators {22%}| Additional information{29%} |
|---|---|---|---|
| destination_id | A unique ID for the destination. | CONTAIN
 I_CONTAIN
 EQUAL
 NOT_EQUAL
 PREFIX
I_PREFIX  | |
| city | The city where the destination is located. | CONTAIN
 I_CONTAIN
 NOT_EQUAL
 WILDCARD
 I_WILDCARD 
NOT_WILDCARD 
I_NOT_WILDCARD 
PREFIX 
I_PREFIX  | |
| region | The region (state/province) where the destination is located. |NOT_EQUAL
CONTAIN   | |
| price | The average or lowest price for the destination. | GT
GTE
LT
LTE
EQUAL|  |
| custom_label_0
custom_label_1
custom_label_2
custom_label_3
custom_label_4 | Additional information. |CONTAIN 
I_CONTAIN 
NOT_EQUAL 
EXCLUDE 
I_EXCLUDE 
WILDCARD
I_WILDCARD
NOT_WILDCARD
I_NOT_WILDCARD
PREFIX
I_PREFIX   | |
```

#### For entertainment catalog product sets
```xtable
| Field{23%} | Description {25%}| Supported operators {22%}| Additional information{30%} |
|---|---|---|---|
| title | The name of the media title item. | EQUAL
NOT_EQUAL
WILDCARD
I_WILDCARD
NOT_WILDCARD
I_NOT_WILDCARD
PREFIX
I_PREFIX   |  |
| availability | The current availability of the media title item. | EQUAL
NOT_EQUAL | Supported values:
- `AVAILABLE`
- `SUBSCRIBERS_ONLY`
- `ON_DEMAND`
- `NOT_AVAILABLE`  |
| condition | The current condition of the media title item. | EQUAL
 NOT_EQUAL | Supported values:
- `NEW`: new. 
- `USED`: used.  |
| timeline | The timeline for the media title item. | EQUAL
NOT_EQUAL | Supported values: 
- `COMING_SOON` : The media title item is not available now, but will be released soon. 
- `ONLINE`: The media title item is currently available for purchase. 
- `EXPIRE_SOON`: The media title item will no longer be available for purchase soon.|
| category | The category of the media title item. | EQUAL
NOT_EQUAL | Supported values:
- `MOVIE` : movie. 
- `MUSIC` : music. 
- `TV_SHOW` : TV show. 
- `TV_SERIES`: TV series. 
- `SPORTS_GAME` : sports game. 
- `LIVE_EVENT`: live event. |
| genres | The genres of the media title item. |CONTAIN
I_CONTAIN
EXCLUDE
I_EXCLUDE
WILDCARD
I_WILDCARD
NOT_WILDCARD
I_NOT_WILDCARD
PREFIX
 I_PREFIX| Supported values: 
To find out the allowed values for this field, refer to the "[ List of values for `genres` ](#item-link-List of values for genres ) " section below.  |
| price | The price for the media title item. |GT
GTE
LT
LTE
 EQUAL   |      |
| custom_label_0
  custom_label_1
  custom_label_2 
 custom_label_3 
 custom_label_4 | Additional information that you want to filter by. | CONTAIN
 I_CONTAIN
 EXCLUDE
I_EXCLUDE
WILDCARD
I_WILDCARD
NOT_WILDCARD
I_NOT_WILDCARD
PREFIX
I_PREFIX  | |
```

##### List of values for `genres`

```xtable
| Value {30%}| Description {60%}|
|---|---|
| `ACTION` | action |
| `ADULT_ANIMATION` | adult animation |
| `ADVENTURE` | adventure |
| `ANIMATION` | animation |
| `BIOGRAPHICAL` | biographical |
| `BLACK_COMEDY` | black comedy |
| `BUDDY` | buddy |
| `COMEDY` | comedy |
| `COMIC` | comic |
| `COOKING_SHOW` | cooking show |
| `CRIME` | crime |
| `DISASTER` | disaster |
| `DOCUMENTARY` | documentary |
| `DRAMA` | drama |
| `FAMILY` | family |
| `FANTASY` | fantasy |
| `GAME_SHOW` | game show |
| `HISTORY` | history |
| `HORROR` | horror |
| `LGBT` | lgbt |
| `MARTIAL_ARTS` | martial arts |
| `MILITARY` | military |
| `MUSIC` | music |
| `POLICE` | police |
| `POLICE_PROCEDURAL` | police procedural |
| `POLITIC` | politic |
| `REALITY_TV` | reality TV |
| `ROAD` | road |
| `ROMANCE` | romance |
| `SATIRE` | satire |
| `SCIENCE_FICTION` | science fiction |
| `SITCOM` | sitcom |
| `SOAP_OPERA` | soap opera |
| `SPORT` | sport |
| `SPY` | spy |
| `STEAMPUNK` | steampunk |
| `SUPERHERO` | superhero |
| `TALK_SHOW` | talk show |
| `TEEN` | teen |
| `THRILLER` | thriller |
| `TIME_TRAVEL` | time travel |
| `VAMPIRE` | vampire |
| `WAR` | war |
| `WESTERN` | western |
| `ZOMBIE` | zombie |
```

#### For Auto-Inventory catalog product sets
```xtable
| Field{23%} | Description {25%}| Supported operators {22%}| Additional information{30%} |
|---|---|---|---|
| vehicle_id | A unique ID for the vehicle. | CONTAIN
I_CONTAIN
EXCLUDE
I_EXCLUDE
WILDCARD
I_WILDCARD
NOT_WILDCARD
I_NOT_WILDCARD
PREFIX
I_PREFIX |  |
| title | The name of the vehicle. | EQUAL
NOT_EQUAL
WILDCARD
I_WILDCARD
NOT_WILDCARD
I_NOT_WILDCARD
PREFIX
I_PREFIX |  |
| availability | The current availability of the vehicle. | EQUAL
NOT_EQUAL
CONTAIN
I_CONTAIN
EXCLUDE
I_EXCLUDE | Supported values:
- `AVAILABLE`: available for order.
- `NOT_AVAILABLE`: Not available for order. |
| condition | The current condition of the vehicle. | EQUAL
NOT_EQUAL
CONTAIN
I_CONTAIN
EXCLUDE
I_EXCLUDE | Supported values:
- `EXCELLENT`: excellent.
- `GOOD`: good.
- `FAIR`: fair.
- `POOR`: poor.
- `OTHER`: other. |
| state_of_vehicle | The state of the vehicle. | CONTAIN
I_CONTAIN
EXCLUDE
I_EXCLUDE | Supported values:
- `NEW`: new.
- `USED`: used.
- `CPO`: CPO (certified pre-owned). CPO vehicles are used vehicles that have undergone thorough inspection and are typically newer, have lower mileage, and come with additional warranty coverage compared to regular used cars. |
| vehicle_type | The type of the vehicle. | CONTAIN
I_CONTAIN
EXCLUDE
I_EXCLUDE | Supported values:
- `BOAT`: boat.
- `CAR_TRUCK`: car or truck.
- `COMMERCIAL`: A vehicle used for commercial purposes, such as a delivery truck.
- `MOTORCYCLE`: motorcycle.
- `POWERSPORT`: powersport. Recreational vehicles that are designed for outdoor activities and adventure, such as a snowmobile.
- `RV_CAMPER`: recreational vehicle or camper designed for travel and camping purposes.
- `TRAILER`: trailer.
- `OTHER`: Any other vehicle type not covered above. |
| make | The make (brand) of the vehicle. | CONTAIN
I_CONTAIN
EXCLUDE
I_EXCLUDE
WILDCARD
I_WILDCARD
NOT_WILDCARD
I_NOT_WILDCARD
PREFIX
I_PREFIX |  |
| model | The model of the vehicle. | CONTAIN
I_CONTAIN
EXCLUDE
I_EXCLUDE
WILDCARD
I_WILDCARD
NOT_WILDCARD
I_NOT_WILDCARD
PREFIX
I_PREFIX |  |
| trim | The trim of the vehicle. The trim represents the distinctive specification package of the vehicle, tailored specifically to that model. | CONTAIN
I_CONTAIN
EXCLUDE
I_EXCLUDE
WILDCARD
I_WILDCARD
NOT_WILDCARD
I_NOT_WILDCARD
PREFIX
I_PREFIX |  |
| year | The year when the vehicle was launched, in the format of `YYYY`. | GT
GTE
LT
LTE
EQUAL | |
| vin | The VIN (Vehicle Identification Number) of the vehicle. | CONTAIN
I_CONTAIN
EXCLUDE
I_EXCLUDE
WILDCARD
I_WILDCARD
NOT_WILDCARD
I_NOT_WILDCARD
PREFIX
I_PREFIX |  |
| value 
(within the mileage object) | Mileage value. | GT
GTE
LT
LTE
EQUAL |  |
| body_style | The body style of the vehicle. | CONTAIN
I_CONTAIN
EXCLUDE
I_EXCLUDE | Supported values:
- `CONVERTIBLE`: convertible.
- `COUPE`: coupe.
- `CROSSOVER`: crossover.
- `HATCHBACK`: hatchback.
- `MINIVAN`: minivan.
- `SMALL_CAR`: small car.
- `SEDAN`: sedan.
- `SUV`: SUV.
- `TRUCK`: truck.
- `VAN`: van.
- `WAGON`: wagon.
- `OTHER`: other. |
| exterior_color | The exterior color of the vehicle. | CONTAIN
I_CONTAIN
EXCLUDE
I_EXCLUDE
WILDCARD
I_WILDCARD
NOT_WILDCARD
I_NOT_WILDCARD
PREFIX
I_PREFIX |  |
| interior_color | The interior color of the vehicle. | CONTAIN
I_CONTAIN
EXCLUDE
I_EXCLUDE
WILDCARD
I_WILDCARD
NOT_WILDCARD
I_NOT_WILDCARD
PREFIX
I_PREFIX |  |
| transmission | The transmission type of the vehicle. | CONTAIN
I_CONTAIN
EXCLUDE
I_EXCLUDE | Supported values:
- `AUTOMATIC`: automatic.
- `MANUAL`: manual. |
| drivetrain | The drivetrain type of the vehicle. | CONTAIN
I_CONTAIN
EXCLUDE
I_EXCLUDE | Supported values:
- `4X2`: four-wheel drive vehicle with two wheel drive (2WD). The drivetrain delivers power to either the front wheels or the rear wheels.
- `4X4`: four-wheel drive vehicle with four wheel drive. The drivetrain delivers power to all four wheels.
- `AWD`: all-wheel drive. The drivetrain delivers power to all wheels continuously.
- `FWD`: front-wheel drive. The drivetrain delivers power to the front wheels only.
- `RWD`: rear-wheel drive. The drivetrain delivers power to the rear wheels only.
- `OTHER`: any other drivetrain type not covered above, such as electric vehicles with unique drivetrain styles. |
| fuel_type | The fuel type of the vehicle. | CONTAIN
I_CONTAIN
EXCLUDE
I_EXCLUDE | Supported values:
- `DIESEL`: diesel.
- `ELECTRIC`: electric.
- `FLEX`: flex fuel, a blend of gasoline and ethanol.
- `GASOLINE`: gasoline.
- `HYBRID`: hybrid.
- `OTHER`: other. |
| city | The city where the dealership is located. | CONTAIN
I_CONTAIN
EXCLUDE
I_EXCLUDE
WILDCARD
I_WILDCARD
NOT_WILDCARD
I_NOT_WILDCARD
PREFIX
I_PREFIX |  |
| region | The region (state or province) where the dealership is located. | CONTAIN
I_CONTAIN
EXCLUDE
I_EXCLUDE
WILDCARD
I_WILDCARD
NOT_WILDCARD
I_NOT_WILDCARD
PREFIX
I_PREFIX |  |
| dealer_id | A unique ID for the dealership. | CONTAIN
I_CONTAIN
EXCLUDE
I_EXCLUDE
WILDCARD
I_WILDCARD
NOT_WILDCARD
I_NOT_WILDCARD
PREFIX
I_PREFIX |  |
| dealer_name | The name of the dealership. | CONTAIN
I_CONTAIN
EXCLUDE
I_EXCLUDE
WILDCARD
I_WILDCARD
NOT_WILDCARD
I_NOT_WILDCARD
PREFIX
I_PREFIX |  |
| stock_number | The stock number assigned to the vehicle by the dealership. | CONTAIN
I_CONTAIN
EXCLUDE
I_EXCLUDE
WILDCARD
I_WILDCARD
NOT_WILDCARD
I_NOT_WILDCARD
PREFIX
I_PREFIX |  |
| date_first_on_lot | The date when the vehicle physically arrives at the dealership's lot, in the format of `YYYY-MM-DD`. | GT
GTE
LT
LTE
EQUAL |  |
| days_on_lot | The number of days the vehicle has been on the dealership's lot. | GT
GTE
LT
LTE
EQUAL |  |
| price | The price of the vehicle. | GT
GTE
LT
LTE
EQUAL |  |
| sale_price | The discounted price of the vehicle. | GT
GTE
LT
LTE
EQUAL |  |
| custom_label_0
custom_label_1
custom_label_2
custom_label_3
custom_label_4 | Additional information that you want to filter by. | CONTAIN
I_CONTAIN
EXCLUDE
I_EXCLUDE
WILDCARD
I_WILDCARD
NOT_WILDCARD
I_NOT_WILDCARD
PREFIX
I_PREFIX |  |
```

#### For Auto-Model catalog product sets
```xtable
| Field{24%} | Description {25%}| Supported operators {22%}| Additional information{29%} |
|---|---|---|---|
| vehicle_id | A unique ID for the vehicle. | CONTAIN
 I_CONTAIN
 EXCLUDE
 I_EXCLUDE
 WILDCARD
 I_WILDCARD
 NOT_WILDCARD
 I_NOT_WILDCARD
 PREFIX
 I_PREFIX | |
| title | The name of the vehicle. | EQUAL
 NOT_EQUAL
 WILDCARD
 I_WILDCARD
 NOT_WILDCARD
 I_NOT_WILDCARD
 PREFIX
 I_PREFIX | |
| make | The make (brand) of the vehicle. | CONTAIN
 I_CONTAIN
 EXCLUDE
 I_EXCLUDE
 WILDCARD
 I_WILDCARD
 NOT_WILDCARD
 I_NOT_WILDCARD
 PREFIX
 I_PREFIX | |
| model | The model of the vehicle. | CONTAIN
 I_CONTAIN
 EXCLUDE
 I_EXCLUDE
 WILDCARD
 I_WILDCARD
 NOT_WILDCARD
 I_NOT_WILDCARD
 PREFIX
 I_PREFIX | |
| trim | The trim of the vehicle. The trim represents the distinctive specification package of the vehicle, tailored specifically to that model. | CONTAIN
 I_CONTAIN
 EXCLUDE
 I_EXCLUDE
 WILDCARD
 I_WILDCARD
 NOT_WILDCARD
 I_NOT_WILDCARD
 PREFIX
 I_PREFIX | |
| year | The year when the vehicle was launched, in the format of `YYYY`. | GT
GTE
LT
LTE
EQUAL | |
| exterior_color | The color of the vehicle. | CONTAIN
 I_CONTAIN
 EXCLUDE
 I_EXCLUDE
 WILDCARD
 I_WILDCARD
 NOT_WILDCARD
 I_NOT_WILDCARD
 PREFIX
 I_PREFIX | |
```
