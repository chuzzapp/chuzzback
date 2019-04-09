Database schema overview
============

### user
| column | type | notes |
| ------ | ---- | ----- |
| email | string | with unique constraint |
| username | string| with unique constraint |
| display_name | string|  |
| first_name | string|  |
| last_name | string|  |
| phone_number | string |  |
| phone_country_code | string |  |
| birthday | date | |
| gender | string | "male", "female" or "other" |
| country_id | string | reference to table `country` |
| image_id | reference | reference to table `asset` |
| is_enabled_interested_new_poll_notif | boolean | default `true` |
| is_enabled_new_answer_notif | boolean | default `true` |
| is_enabled_celebrity_new_poll_notif | boolean | default `true` |
| is_admin | boolean | default `false` |
| is_celebrity | boolean | default `false` |
| is_writer | boolean | default `false` |
| answers_count | integer |  |
| groups_count | integer |  |
| likes_count | integer |  |
| polls_count | integer |  |
| followers_count | integer |  |
| following_count | integer |  |
| metadata | jsonb |  |
| is_linked_to_instagram | boolean | default `false` |
| deleted | boolean | default `false` |
| is_declared_adult | boolean | default `false` |


### poll
| column | type | notes | 
| ------ | ---- | ----- |
| name | string |
| description | string |  |
| user_id | reference | reference to table `user` |
| start_time | datetime | |
| end_time | datetime | |
| topic_id | reference | reference to table `topic` |
| image_id | reference | reference to table `asset` |
| is_active | boolean |  |
| is_live | boolean | default `false` |
| likes | integer |
| answers | integer |
| views | integer |  |
| promoted | boolean | default `false` |
| is_adult_only | boolean | default `false` |
| is_published | boolean | default `true` |


### question
| column | type | notes |
| ------ | ---- | ----- |
| title | string |  |
| type | string |  |
| poll_id | reference | reference to table `poll` |
| ordering | integer |  |
| deleted | boolean | default `false` |


### choice
| column | type | notes |
| ------ | ---- | ----- |
| content | string |  |
| image_id | reference | reference to table `asset` |
| question_id | reference | reference to table `question` |
| select_count | integer |  |
| ordering | integer |  |
| deleted | boolean | default `false` |


### answer
| column | type | notes |
| ------ | ---- | ----- |
| user_id | reference | reference to table `user` |
| poll_id | reference | reference to table `poll` |
| question_id | reference | reference to table `question` |
| selected_choice_id | reference | reference to table `choice` |


### poll_like
| column | type | notes |
| ------ | ---- | ----- |
| poll_id | reference | reference to table `poll` |
| user_id | reference | reference to table `user` |


### poll_view
| column | type | notes |
| ------ | ---- | ----- |
| poll_id | reference | reference to table `poll` |
| user_id | reference | reference to table `user` |


### poll_topic
| column | type | notes |
| ------ | ---- | ----- |
| poll_id | reference | reference to table `poll` |
| topic_id | reference | reference to table `topic` |


### poll_country
| column | type | notes |
| ------ | ---- | ----- |
| poll_id | reference | reference to table `poll` |
| country_id | reference | reference to table `country` |


### celebrity
| column | type | notes |
| ------ | ---- | ----- |
| username | string | with unique constraint |
| display_name | string | |
| user_id | reference | reference to table `user` |
| image_id | reference | reference to table `asset` |
| country_id | string | reference to table `country` |
| deleted | boolean | default `false` |


### celebrity_follow
| column | type | notes |
| ------ | ---- | ----- |
| user_id | reference | reference to table `user` |
| celebrity_id | reference | reference to table `celebrity` |


### topic
| column | type | notes |
| ------ | ---- | ----- |
| name | string | |
| image_id | reference | reference to table `asset` |
| is_disabled | boolean | default `false` |
| is_featured | boolean | default `false` |
| is_adult_only | boolean | default `false` |
| is_international | boolean | default `false` |


### user_topic
| column | type | notes |
| ------ | ---- | ----- |
| topic_id | reference | reference to table `topic` |
| user_id | reference | reference to table `user` |


### country
| column | type | notes |
| ------ | ---- | ----- |
| name | string | |


## email_verification
| column | type | notes |
| ------ | ---- | ----- |
| number | string | |
| country_code | string | |
| revoked | boolean | |
| code | string | |
| expired_at | datetime | |
