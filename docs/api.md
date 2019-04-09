API overview
============

### Poll

#### Creating new poll (User token required):

    POST /poll

Form json data:

```
{
  poll: {
    name: {POLL_NAME_STRING},
    description: {POLL_DESCRIPTION_STRING},
    topic_id: {POLL_TOPIC_ID_STRING},
    start_time: {POLL_START_TIME_DATETIME},
    end_time: {POLL_END_TIME_DATETIME},
    image_id: {POLL_IMAGE_ID_STRING},
    is_active: {POLL_IS_ACTIVE_STRING},
    country_id: {POLL_COUNTRY_ID_STRING}
  }
  questions: [
    {
      title: {QUESTION_TITLE_STRING},
      type: {QUESTION_TYPE_STRING},
      ordering: {QUESTION_TYPE_INTEGER},
      choices: [
        {
          content: {CHOICE_CONTENT_STRING},
          image_id: {CHOICE_IMAGE_ID_STRING},
          ordering: {CHOICE_ORDERING_INTEGER}
        }
      ]
    }
  ]
}
```


### Verification Code

#### Generate phone verification (Public):

    POST /send_verification_code

Form json data:

```
{
  phone_number: {PHONE_NUMBER_STRING},
  country_code: {COUNTRY_CODE_STRING}
}
```


### Signup/Login

#### Signup/Login by phone number:

    POST /

Form json data:

```
{
  provider: "sms",
  action: "auth:login",
  api_key: {SKYGEAR_API_KEY_STRING},
  provider_auth_data: {
    phone_number: {PHONE_NUMBER_STRING},
    country_code: {COUNTRY_CODE_STRING},
    code: {VERIFICATION_CODE_STRING}
  }
}
```
