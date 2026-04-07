# Supported dimensions for Upgraded Smart+ Creative Breakdown Reports

**Doc ID**: 1843337879988226
**Path**: API Reference/Upgraded Smart+/Reporting/Run an Upgraded Smart+ Creative Breakdown Report/Supported dimensions for Upgraded Smart+ Creative Breakdown Reports

---

Dimension is an attribute to group your data by.

The following table outlines the available dimensions and supported dimension groupings in Upgraded Smart+ Creative Breakdown Reports.

```xtable
| Dimension {20%} | Dimension type {15%} | Description {20%} | Supported dimension groupings {45%} |
| --- | --- | --- | --- |
| `main_material_id` | Material dimension | Group by main creative ID. | 
- `main_material_id` only
- `main_material_id` + one to three Setting dimensions (`ad_text_entity_id`/`call_to_action_entity_id`/ `interactive_add_on_entity_id`)
- `main_material_id` + one Time dimension (`stat_time_hour`/`stat_time_day`/`stat_time_week`/ `stat_time_month`)
- `main_material_id` + one to three Setting dimensions (`ad_text_entity_id`/`call_to_action_entity_id`/ `interactive_add_on_entity_id`) + one Time dimension (`stat_time_hour`/`stat_time_day`/`stat_time_week`/ `stat_time_month`) |
| `ad_text_entity_id` | Setting dimension | Group by ad text entity ID.

The ID is a system-generated unique identifier for an ad text. | 
- `ad_text_entity_id` only
- `ad_text_entity_id` + `main_material_id`
- `ad_text_entity_id` + one to two Setting dimensions (`call_to_action_entity_id`/ `interactive_add_on_entity_id`)
- `ad_text_entity_id` + one to two Setting dimensions (`call_to_action_entity_id`/ `interactive_add_on_entity_id`) + `main_material_id`
- `ad_text_entity_id` + one Time dimension (`stat_time_hour`/`stat_time_day`/`stat_time_week`/ `stat_time_month`)
- `ad_text_entity_id` + one to two Setting dimensions (`call_to_action_entity_id`/ `interactive_add_on_entity_id`) + one Time dimension (`stat_time_hour`/`stat_time_day`/`stat_time_week`/ `stat_time_month`)
- `ad_text_entity_id` + one to two Setting dimensions (`call_to_action_entity_id`/ `interactive_add_on_entity_id`) + one Time dimension (`stat_time_hour`/`stat_time_day`/`stat_time_week`/ `stat_time_month`) + `main_material_id` |
| `call_to_action_entity_id` | Setting dimension | Group by call-to-action entity ID.

The ID is a system-generated unique identifier for a call-to-action. | 
- `call_to_action_entity_id` only
- `call_to_action_entity_id`+ `main_material_id`
- `call_to_action_entity_id` + one to two Setting dimensions (`ad_text_entity_id`/ `interactive_add_on_entity_id`)
- `call_to_action_entity_id` + one to two Setting dimensions (`ad_text_entity_id`/ `interactive_add_on_entity_id`) + `main_material_id`
- `call_to_action_entity_id` + one Time dimension (`stat_time_hour`/`stat_time_day`/`stat_time_week`/ `stat_time_month`)
- `call_to_action_entity_id` + one to two Setting dimensions (`ad_text_entity_id`/ `interactive_add_on_entity_id`) + one Time dimension (`stat_time_hour`/`stat_time_day`/`stat_time_week`/ `stat_time_month`)
- `call_to_action_entity_id` + one to two Setting dimensions (`ad_text_entity_id`/ `interactive_add_on_entity_id`) + one Time dimension (`stat_time_hour`/`stat_time_day`/`stat_time_week`/ `stat_time_month`) + `main_material_id` |
| `interactive_add_on_entity_id` | Setting dimension | Group by interactive add-on entity ID.

The ID is a system-generated unique identifier for an interactive add-on. | 
- `interactive_add_on_entity_id` only
- `interactive_add_on_entity_id`+ `main_material_id`
- `interactive_add_on_entity_id` + one to two Setting dimensions (`ad_text_entity_id`/ `call_to_action_entity_id`)
- `interactive_add_on_entity_id` + one to two Setting dimensions (`ad_text_entity_id`/ `interactive_add_on_entity_id`) + `main_material_id`
- `interactive_add_on_entity_id` + one Time dimension (`stat_time_hour`/`stat_time_day`/`stat_time_week`/ `stat_time_month`)
- `interactive_add_on_entity_id` + one to two Setting dimensions (`ad_text_entity_id`/`call_to_action_entity_id`) + one Time dimension (`stat_time_hour`/`stat_time_day`/`stat_time_week`/ `stat_time_month`)
- `interactive_add_on_entity_id` + one to two Setting dimensions (`ad_text_entity_id`/`call_to_action_entity_id`) + one Time dimension (`stat_time_hour`/`stat_time_day`/`stat_time_week`/ `stat_time_month`) + `main_material_id` |
| `stat_time_hour` | Time dimension | Group by hour. | 
- `stat_time_hour`+ `main_material_id`
- `stat_time_hour` + one to three Setting dimensions (`ad_text_entity_id`/`call_to_action_entity_id`/ `interactive_add_on_entity_id`)
- `stat_time_hour` + one to three Setting dimensions (`ad_text_entity_id`/`call_to_action_entity_id`/ `interactive_add_on_entity_id`) + `main_material_id` |
| `stat_time_day` | Time dimension | Group by day. | 
- `stat_time_day`+ `main_material_id`
- `stat_time_day` + one to three Setting dimensions (`ad_text_entity_id`/`call_to_action_entity_id`/ `interactive_add_on_entity_id`)
- `stat_time_day` + one to three Setting dimensions (`ad_text_entity_id`/`call_to_action_entity_id`/ `interactive_add_on_entity_id`) + `main_material_id` |
| `stat_time_week` | Time dimension | Group by week. | 
- `stat_time_week`+ `main_material_id`
- `stat_time_week` + one to three Setting dimensions (`ad_text_entity_id`/`call_to_action_entity_id`/ `interactive_add_on_entity_id`)
- `stat_time_week` + one to three Setting dimensions (`ad_text_entity_id`/`call_to_action_entity_id`/ `interactive_add_on_entity_id`) + `main_material_id` |
| `stat_time_month` | Time dimension | Group by month. | 
- `stat_time_month`+ `main_material_id`
- `stat_time_month` + one to three Setting dimensions (`ad_text_entity_id`/`call_to_action_entity_id`/ `interactive_add_on_entity_id`)
- `stat_time_month` + one to three Setting dimensions (`ad_text_entity_id`/`call_to_action_entity_id`/ `interactive_add_on_entity_id`) + `main_material_id` |
```
