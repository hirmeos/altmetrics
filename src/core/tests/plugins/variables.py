"""I've put as much effort as possible into removing/obscuring any genuine
data that is not public (granted this all came from a public API, but still...).
"""
from dateutil.tz import tzutc
import datetime

from core.variables import Origins
from processor.models import Event, RawEvent


# DOIs - The idea is (id, raw) in the database

dois_unexpected = [  # Returned by the API but not for supported origins
    (1, '10.987654321/abcd.123'),
    (3, '10.987654321/batman'),
    (5, '10.987654321/jophd.lati'),
    (7, '10.987654321/oq.thinkmachine'),
    (9, '10.987654321/ouioui.01'),
    (11, '10.987654321/wors.142'),
    (13, '10.987654321/wors.911/'),
    (15, '10.987654321/wors.lado'),
    (17, '10.987654321/wors.sub'),
]

dois_expected = [  # Returned by the API for supported origin events
    (2, '10.987654321/bjj-2020-007'),
    (4, '10.987654321/dem-538'),
    (6, '10.987654321/publictv'),
    (8, '10.987654321/s.aureus'),
    (10, '10.987654321/thinkmachine.1984'),
]


# returned by event data, and should be saved

event_data_expected_events = [   # This was just painful to prepare
  {
    "license": "https://creativecommons.org/publicdomain/zero/1.0/",
    "terms": "https://doi.org/10.13011/CED-terms-of-use",
    "updated_reason": "https://evidence.eventdata.crossref.org/announcements/2179-04-26T00-00-00Z-ED-16.json",
    "updated": "edited",
    "obj_id": "https://doi.org/10.987654321/dem-538",
    "source_token": "9b1b89a4-b364-412a-b0ef-9e70c6d1e68a",
    "occurred_at": "2017-02-18T01:35:24Z",
    "subj_id": "http://twitter.com/asTwitteruser1gz/statuses/000000000000000001",
    "id": "f1e98c3a-97b7-48be-849d-74a8929d5b79",
    "evidence_record": "https://evidence.eventdata.crossref.org/evidence/21991218aabe95ae-2322-4060-a9a4-0232cde919ef",
    "action": "add",
    "subj": {
      "pid": "http://twitter.com/asTwitteruser1gz/statuses/000000000000000001",
      "title": "Tweet 000000000000000001",
      "issued": "2017-02-18T01:35:24.000Z",
      "author": {
        "url": "http://www.twitter.com/asTwitteruser1gz"
      },
      "original-tweet-url": "http://twitter.com/dGTwitteruser4aw/statuses/000000000000000004",
      "original-tweet-author": "http://www.twitter.com/dGTwitteruser4aw",
      "alternative-id": "000000000000000001"
    },
    "source_id": "twitter",
    "obj": {
      "pid": "https://doi.org/10.987654321/dem-538",
      "url": "http://www.api-journal.co.za/articles/10.987654321/dem-538/"
    },
    "timestamp": "2017-02-18T02:41:44Z",
    "updated_date": "2018-05-03T09:46:16Z",
    "relation_type_id": "discusses"
  },
  {
    "license": "https://creativecommons.org/publicdomain/zero/1.0/",
    "terms": "https://doi.org/10.13011/CED-terms-of-use",
    "updated_reason": "https://evidence.eventdata.crossref.org/announcements/2179-04-26T00-00-00Z-ED-16.json",
    "updated": "edited",
    "obj_id": "https://doi.org/10.987654321/dem-538",
    "source_token": "9b1b89a4-b364-412a-b0ef-9e70c6d1e68a",
    "occurred_at": "2017-02-20T08:44:25Z",
    "subj_id": "http://twitter.com/cRTwitteruser32x/statuses/000000000000000003",
    "id": "19aebdf1-5a0e-4ca0-8602-875283a05f32",
    "evidence_record": "https://evidence.eventdata.crossref.org/evidence/21991220aa4c5e36-b337-416e-bff9-935b41e49275",
    "action": "add",
    "subj": {
      "pid": "http://twitter.com/cRTwitteruser32x/statuses/000000000000000003",
      "title": "Tweet 000000000000000003",
      "issued": "2017-02-20T08:44:25.000Z",
      "author": {
        "url": "http://www.twitter.com/cRTwitteruser32x"
      },
      "original-tweet-url": "http://twitter.com/bpTwitteruser2ly/statuses/000000000000000002",
      "original-tweet-author": "http://www.twitter.com/apijournal",
      "alternative-id": "000000000000000003"
    },
    "source_id": "twitter",
    "obj": {
      "pid": "https://doi.org/10.987654321/dem-538",
      "url": "http://www.api-journal.co.za/articles/10.987654321/dem-538/"
    },
    "timestamp": "2017-02-20T08:48:36Z",
    "updated_date": "2018-05-03T09:50:55Z",
    "relation_type_id": "discusses"
  },
  {
    "license": "https://creativecommons.org/publicdomain/zero/1.0/",
    "terms": "https://doi.org/10.13011/CED-terms-of-use",
    "updated_reason": "https://evidence.eventdata.crossref.org/announcements/2179-04-26T00-00-00Z-ED-16.json",
    "updated": "edited",
    "obj_id": "https://doi.org/10.987654321/bjj-2020-007",
    "source_token": "9b1b89a4-b364-412a-b0ef-9e70c6d1e68a",
    "occurred_at": "2017-02-20T10:35:26Z",
    "subj_id": "http://twitter.com/emTwitteruser5av/statuses/000000000000000005",
    "id": "409f6320-0782-4dad-ac18-cc1f8caf2b59",
    "evidence_record": "https://evidence.eventdata.crossref.org/evidence/21991220aa58e77b-5008-458b-9f3f-93950298c094",
    "action": "add",
    "subj": {
      "pid": "http://twitter.com/emTwitteruser5av/statuses/000000000000000005",
      "title": "Tweet 000000000000000005",
      "issued": "2017-02-20T10:35:26.000Z",
      "author": {
        "url": "http://www.twitter.com/emTwitteruser5av"
      },
      "original-tweet-url": "http://twitter.com/emTwitteruser5av/statuses/000000000000000005",
      "original-tweet-author": None,
      "alternative-id": "000000000000000005"
    },
    "source_id": "twitter",
    "obj": {
      "pid": "https://doi.org/10.987654321/bjj-2020-007",
      "url": "http://infodiscipline.coinfo.org/articles/10.987654321/bjj-2020-007/"
    },
    "timestamp": "2017-02-20T10:54:13Z",
    "updated_date": "2018-05-03T09:51:00Z",
    "relation_type_id": "discusses"
  },
  {
    "license": "https://creativecommons.org/publicdomain/zero/1.0/",
    "obj_id": "https://doi.org/10.987654321/publictv",
    "source_token": "4926824c-ed99-53ca-a632-177ba7e46d6d",
    "occurred_at": "2017-04-06T15:51:53Z",
    "subj_id": "https://jwpuser1s.wordpress.com/2199/11/01/open/",
    "id": "bf2bdc5d-c4a6-4f6d-aca7-7cdcde9cf928",
    "evidence_record": "https://evidence.eventdata.crossref.org/evidence/21991007-wordpressdotcom-9dec7db1-3f27-4622-b6af-ee6dbc9365fa",
    "terms": "https://doi.org/10.13011/CED-terms-of-use",
    "action": "add",
    "subj": {
      "pid": "https://jwpuser1s.wordpress.com/2199/11/01/open/",
      "type": "post-weblog",
      "title": "Open"
    },
    "source_id": "wordpressdotcom",
    "obj": {
      "pid": "https://doi.org/10.987654321/publictv",
      "url": "https://doi.org/10.987654321/publictv"
    },
    "timestamp": "2017-04-07T07:46:53Z",
    "relation_type_id": "discusses"
  },
  {
    "license": "https://creativecommons.org/publicdomain/zero/1.0/",
    "obj_id": "https://doi.org/10.987654321/publictv",
    "source_token": "4926824c-ed99-53ca-a632-177ba7e46d6d",
    "occurred_at": "2017-04-06T15:51:53Z",
    "subj_id": "https://jwpuser1s.wordpress.com/2199/11/01/open/",
    "id": "2ce25673-09b4-4dfb-8836-72e2dfe63a72",
    "evidence_record": "https://evidence.eventdata.crossref.org/evidence/21991007-wordpressdotcom-9dec7db1-3f27-4622-b6af-ee6dbc9365fa",
    "terms": "https://doi.org/10.13011/CED-terms-of-use",
    "action": "add",
    "subj": {
      "pid": "https://jwpuser1s.wordpress.com/2199/11/01/open/",
      "type": "post-weblog",
      "title": "Open"
    },
    "source_id": "wordpressdotcom",
    "obj": {
      "pid": "https://doi.org/10.987654321/publictv",
      "url": "https://doi.org/10.987654321/publictv"
    },
    "timestamp": "2017-04-07T07:46:53Z",
    "relation_type_id": "discusses"
  },
  {
    "license": "https://creativecommons.org/publicdomain/zero/1.0/",
    "obj_id": "https://doi.org/10.987654321/publictv",
    "source_token": "4926824c-ed99-53ca-a632-177ba7e46d6d",
    "occurred_at": "2017-04-06T15:51:53Z",
    "subj_id": "https://jwpuser1s.wordpress.com/2199/11/01/open/",
    "id": "2bf67e8f-140c-4427-aac6-0b0d04d09d75",
    "evidence_record": "https://evidence.eventdata.crossref.org/evidence/21991007-wordpressdotcom-9dec7db1-3f27-4622-b6af-ee6dbc9365fa",
    "terms": "https://doi.org/10.13011/CED-terms-of-use",
    "action": "add",
    "subj": {
      "pid": "https://jwpuser1s.wordpress.com/2199/11/01/open/",
      "type": "post-weblog",
      "title": "Open"
    },
    "source_id": "wordpressdotcom",
    "obj": {
      "pid": "https://doi.org/10.987654321/publictv",
      "url": "https://doi.org/10.987654321/publictv"
    },
    "timestamp": "2017-04-07T07:46:53Z",
    "relation_type_id": "discusses"
  },
  {
    "license": "https://creativecommons.org/publicdomain/zero/1.0/",
    "terms": "https://doi.org/10.13011/CED-terms-of-use",
    "updated_reason": "https://evidence.eventdata.crossref.org/announcements/2179-01-19T00-00-00Z-ED-15.json",
    "obj_id": "https://doi.org/10.987654321/thinkmachine.1984",
    "source_token": "8fdc3ffd-7999-43bb-af57-b3792ce11851",
    "occurred_at": "2017-04-11T14:15:56Z",
    "subj_id": "https://en.wikipedia.org/wiki/Clay_Soldiers_Group",
    "id": "4d4d1f8d-36c1-4294-b02a-54393188a0c0",
    "evidence_record": "https://evidence.eventdata.crossref.org/evidence/21991011-wikipedia-cefd1e58-4109-4c7e-b05f-c956b5cf2c03",
    "action": "add",
    "subj": {
      "pid": "https://en.wikipedia.org/wiki/Clay_Soldiers_Group",
      "url": "https://en.wikipedia.org/w/index.php?title=Clay_Soldiers_Group&oldid=774919153",
      "title": "Clay Soldiers Group",
      "api-url": "https://en.wikipedia.org/api/rest_v1/page/html/Clay_Soldiers_Group/774919287"
    },
    "source_id": "wikipedia",
    "obj": {
      "pid": "https://doi.org/10.987654321/thinkmachine.1984",
      "url": "https://doi.org/10.987654321/thinkmachine.1984"
    },
    "timestamp": "2017-04-11T14:16:42Z",
    "updated_date": "2018-01-31T17:30:00Z",
    "relation_type_id": "references"
  },
  {
    "license": "https://creativecommons.org/publicdomain/zero/1.0/",
    "terms": "https://doi.org/10.13011/CED-terms-of-use",
    "updated_reason": "https://evidence.eventdata.crossref.org/announcements/2179-01-19T00-00-00Z-ED-15.json",
    "obj_id": "https://doi.org/10.987654321/thinkmachine.1984",
    "source_token": "8fdc3ffd-7999-43bb-af57-b3792ce11851",
    "occurred_at": "2017-04-11T14:15:56Z",
    "subj_id": "https://en.wikipedia.org/wiki/Clay_Soldiers_Group",
    "id": "dedcc16c-885c-492d-8ddf-522c4a85b580",
    "evidence_record": "https://evidence.eventdata.crossref.org/evidence/21991011-wikipedia-cefd1e58-4109-4c7e-b05f-c956b5cf2c03",
    "action": "add",
    "subj": {
      "pid": "https://en.wikipedia.org/wiki/Clay_Soldiers_Group",
      "url": "https://en.wikipedia.org/w/index.php?title=Clay_Soldiers_Group&oldid=774919153",
      "title": "Clay Soldiers Group",
      "api-url": "https://en.wikipedia.org/api/rest_v1/page/html/Clay_Soldiers_Group/774919287"
    },
    "source_id": "wikipedia",
    "obj": {
      "pid": "https://doi.org/10.987654321/thinkmachine.1984",
      "url": "http://www.ai-journal.com/articles/10.987654321/thinkmachine.1984/"
    },
    "timestamp": "2017-04-11T14:16:43Z",
    "updated_date": "2018-01-31T17:30:00Z",
    "relation_type_id": "references"
  },
  {
    "license": "https://creativecommons.org/publicdomain/zero/1.0/",
    "terms": "https://doi.org/10.13011/CED-terms-of-use",
    "updated_reason": "https://evidence.eventdata.crossref.org/announcements/2179-01-19T00-00-00Z-ED-15.json",
    "obj_id": "https://doi.org/10.987654321/s.aureus",
    "source_token": "8fdc3ffd-7999-43bb-af57-b3792ce11851",
    "occurred_at": "2017-04-11T14:50:18Z",
    "subj_id": "https://en.wikipedia.org/wiki/Conflict_Caused_Unknown_Truths(2991/932028)",
    "id": "dfbe4c00-de84-453c-8939-a7ed45b7a891",
    "evidence_record": "https://evidence.eventdata.crossref.org/evidence/21991011-wikipedia-a8581d1e-07f2-43d3-b8f3-6ac0f320fb2b",
    "action": "add",
    "subj": {
      "pid": "https://en.wikipedia.org/wiki/Conflict_Caused_Unknown_Truths(2991/932028)",
      "url": "https://en.wikipedia.org/w/index.php?title=Conflict_Caused_Unknown_Truths(2991/932028)&oldid=774923731",
      "title": "Conflict Caused Unknown Truths (2991/932028)",
      "api-url": "https://en.wikipedia.org/api/rest_v1/page/html/Conflict_Caused_Unknown_Truths(2991/932028)/774923731"
    },
    "source_id": "wikipedia",
    "obj": {
      "pid": "https://doi.org/10.987654321/s.aureus",
      "url": "https://doi.org/10.987654321/s.aureus"
    },
    "timestamp": "2017-04-11T14:52:00Z",
    "updated_date": "2018-01-31T17:30:00Z",
    "relation_type_id": "references"
  },
  {
    "license": "https://creativecommons.org/publicdomain/zero/1.0/",
    "obj_id": "https://doi.org/10.987654321/bjj-2020-007",
    "source_token": "668ecf93-7885-45bb-ba41-98ea8074dbb0",
    "occurred_at": "2016-05-17T07:11:37Z",
    "subj_id": "https://hypothes.is/a/sehIFMsJEzzl3tU6NUdj",
    "id": "43531cb9-d3c2-45fb-a8de-48815bdc173c",
    "evidence_record": "https://evidence.eventdata.crossref.org/evidence/21991011-hypothesis-718266b5-9327-419a-82d2-0cfa97704c7f",
    "terms": "https://doi.org/10.13011/CED-terms-of-use",
    "action": "add",
    "subj": {
      "pid": "https://hypothes.is/a/sehIFMsJEzzl3tU6NUdj",
      "json-url": "https://hypothes.is/api/annotations/sehIFMsJEzzl3tU6NUdj",
      "url": "https://hyp.is/dNljzKpNjtgj3bK4EeA6/infodiscipline.coinfo.org/articles/10.987654321/bjj-2020-007/",
      "type": "annotation",
      "title": "No ideas what to do with this one",
      "issued": "2016-05-17T07:11:37Z"
    },
    "source_id": "hypothesis",
    "obj": {
      "pid": "https://doi.org/10.987654321/bjj-2020-007",
      "url": "http://infodiscipline.coinfo.org/articles/10.987654321/bjj-2020-007/"
    },
    "timestamp": "2017-04-11T19:36:20Z",
    "relation_type_id": "annotates"
  },
  {
    "license": "https://creativecommons.org/publicdomain/zero/1.0/",
    "obj_id": "https://doi.org/10.987654321/bjj-2020-007",
    "source_token": "668ecf93-7885-45bb-ba41-98ea8074dbb0",
    "occurred_at": "2016-07-05T20:25:49Z",
    "subj_id": "https://hypothes.is/a/LGtG52kTmSz5lgo8MzAu89",
    "id": "52e3e202-a5b7-410d-a91f-9dd4ee593d7f",
    "evidence_record": "https://evidence.eventdata.crossref.org/evidence/21991011-hypothesis-025a5ebd-1300-4950-b687-90c7153c9dc0",
    "terms": "https://doi.org/10.13011/CED-terms-of-use",
    "action": "add",
    "subj": {
      "pid": "https://hypothes.is/a/LGtG52kTmSz5lgo8MzAu89",
      "json-url": "https://hypothes.is/api/annotations/LGtG52kTmSz5lgo8MzAu89",
      "url": "https://hyp.is/Uvx5KkzKBBpkgFSeRTWf/infodiscipline.coinfo.org/articles/10.987654321/bjj-2020-007/",
      "type": "annotation",
      "title": "Even though the paper as a whole was rubbish, it doesn't mean all the data were (because people like to be technically correct when using data as a plural)",
      "issued": "2016-07-05T20:25:49Z"
    },
    "source_id": "hypothesis",
    "obj": {
      "pid": "https://doi.org/10.987654321/bjj-2020-007",
      "url": "http://infodiscipline.coinfo.org/articles/10.987654321/bjj-2020-007/"
    },
    "timestamp": "2017-04-11T19:38:09Z",
    "relation_type_id": "annotates"
  },
  {
    "license": "https://creativecommons.org/publicdomain/zero/1.0/",
    "obj_id": "https://doi.org/10.987654321/bjj-2020-007",
    "source_token": "668ecf93-7885-45bb-ba41-98ea8074dbb0",
    "occurred_at": "2016-07-05T19:33:37Z",
    "subj_id": "https://hypothes.is/a/S6j5OG7fJ1i0Gc6ITJthoT",
    "id": "33d8dacd-a6e1-4934-8daf-25351759592f",
    "evidence_record": "https://evidence.eventdata.crossref.org/evidence/21991011-hypothesis-025a5ebd-1300-4950-b687-90c7153c9dc0",
    "terms": "https://doi.org/10.13011/CED-terms-of-use",
    "action": "add",
    "subj": {
      "pid": "https://hypothes.is/a/S6j5OG7fJ1i0Gc6ITJthoT",
      "json-url": "https://hypothes.is/api/annotations/S6j5OG7fJ1i0Gc6ITJthoT",
      "url": "https://hyp.is/QCPTEcdLvr3TjOrYaMJH/infodiscipline.coinfo.org/articles/10.987654321/bjj-2020-007/",
      "type": "annotation",
      "title": "Nobody cares, Dave... nobody cares.",
      "issued": "2016-07-05T19:33:37Z"
    },
    "source_id": "hypothesis",
    "obj": {
      "pid": "https://doi.org/10.987654321/bjj-2020-007",
      "url": "http://infodiscipline.coinfo.org/articles/10.987654321/bjj-2020-007/"
    },
    "timestamp": "2017-04-11T19:38:09Z",
    "relation_type_id": "annotates"
  },
]


# returned by event data, but currently not supported by hirmeos altmetrics
event_data_unexpected_events = [
  {
    "license": "https://creativecommons.org/publicdomain/zero/1.0/",
    "obj_id": "https://doi.org/10.987654321/oq.thinkmachine",
    "source_token": "0064360b-74b8-46e2-a775-54880de535f9",
    "occurred_at": "2015-11-26T01:42:57Z",
    "subj_id": "https://reddit.com/r/Anthropology/comments/9lajla/the_location_of_confidence_and_backstabbing/",
    "id": "9dcaea06-9b53-41f0-bb4c-341d144a1dbf",
    "evidence_record": "https://evidence.eventdata.crossref.org/evidence/21991223aa9152e1-dea9-4ba4-8e04-6e000bf97dea",
    "terms": "https://doi.org/10.13011/CED-terms-of-use",
    "action": "add",
    "subj": {
      "pid": "https://reddit.com/r/Anthropology/comments/9lajla/the_location_of_confidence_and_backstabbing/",
      "type": "post",
      "title": "The Location of Confidence and Backstabbing: Discussion and Scattering",
      "issued": "2015-11-26T01:42:57.000Z"
    },
    "source_id": "reddit",
    "obj": {
      "pid": "https://doi.org/10.987654321/oq.thinkmachine",
      "url": "http://www.openquaternary.com/articles/10.987654321/oq.thinkmachine/"
    },
    "timestamp": "2017-02-23T02:51:16Z",
    "relation_type_id": "discusses"
  },
  {
    "license": "https://creativecommons.org/publicdomain/zero/1.0/",
    "obj_id": "https://doi.org/10.987654321/oq.thinkmachine",
    "source_token": "0064360b-74b8-46e2-a775-54880de535f9",
    "occurred_at": "2015-11-26T01:48:23Z",
    "subj_id": "https://reddit.com/r/evopsych/comments/9lak82/the_location_of_confidence_and_backstabbing/",
    "id": "bb46bea4-d38e-4e20-be9a-f129d16eec03",
    "evidence_record": "https://evidence.eventdata.crossref.org/evidence/21991223aa9152e1-dea9-4ba4-8e04-6e000bf97dea",
    "terms": "https://doi.org/10.13011/CED-terms-of-use",
    "action": "add",
    "subj": {
      "pid": "https://reddit.com/r/evopsych/comments/9lak82/the_location_of_confidence_and_backstabbing/",
      "type": "post",
      "title": "The Location of Confidence and Backstabbing: Discussion and Scattering",
      "issued": "2015-11-26T01:48:23.000Z"
    },
    "source_id": "reddit",
    "obj": {
      "pid": "https://doi.org/10.987654321/oq.thinkmachine",
      "url": "http://www.openquaternary.com/articles/10.987654321/oq.thinkmachine/"
    },
    "timestamp": "2017-02-23T02:51:16Z",
    "relation_type_id": "discusses"
  },
  {
    "license": "https://creativecommons.org/publicdomain/zero/1.0/",
    "obj_id": "https://doi.org/10.987654321/oq.thinkmachine",
    "source_token": "0064360b-74b8-46e2-a775-54880de535f9",
    "occurred_at": "2015-11-25T21:00:36Z",
    "subj_id": "https://reddit.com/r/Archaeology/comments/9l9ibs/animal_cities_light_adjacent_fought_unity/",
    "id": "cf128f24-9fc4-4e4f-a232-4fb37980af69",
    "evidence_record": "https://evidence.eventdata.crossref.org/evidence/21991223aa9152e1-dea9-4ba4-8e04-6e000bf97dea",
    "terms": "https://doi.org/10.13011/CED-terms-of-use",
    "action": "add",
    "subj": {
      "pid": "https://reddit.com/r/Archaeology/comments/9l9ibs/animal_cities_light_adjacent_fought_unity/",
      "type": "post",
      "title": "Animal cities light adjacent fought unity across the world",
      "issued": "2015-11-25T21:00:36.000Z"
    },
    "source_id": "reddit",
    "obj": {
      "pid": "https://doi.org/10.987654321/oq.thinkmachine",
      "url": "http://www.openquaternary.com/articles/10.987654321/oq.thinkmachine/"
    },
    "timestamp": "2017-02-23T02:51:17Z",
    "relation_type_id": "discusses"
  },
  {
    "terms": "https://doi.org/10.13011/CED-terms-of-use",
    "updated_reason": "https://evidence.eventdata.crossref.org/announcements/2199-10-06T00-00-00Z-ED-12.json",
    "updated": "edited",
    "obj_id": "https://doi.org/10.987654321/batman",
    "source_token": "e9f90a26-d032-4e35-8b00-488520a99aba",
    "occurred_at": "2017-03-12T05:08:45Z",
    "subj_id": "http://www.citeulike.org/user/aAculuser1u/article/28124311",
    "id": "a0733e88-dee3-4ff5-b25d-55e00112c600",
    "evidence_record": "https://evidence.eventdata.crossref.org/evidence/21991112aad9a6a7-50ef-45c0-803b-f4fa36af82eb",
    "action": "add",
    "subj": {
      "pid": "http://www.citeulike.org/user/aAculuser1u/article/28124311",
      "work-type": "webpage",
      "url": "http://www.citeulike.org/user/aAculuser1u/article/28124311"
    },
    "source_id": "web",
    "obj": {
      "pid": "https://doi.org/10.987654321/batman",
      "url": "https://doi.org/10.987654321/batman"
    },
    "timestamp": "2017-03-12T05:09:46Z",
    "updated_date": "2017-10-18T14:31:11.869Z",
    "relation_type_id": "mentions"
  },
  {
    "terms": "https://doi.org/10.13011/CED-terms-of-use",
    "updated_reason": "https://evidence.eventdata.crossref.org/announcements/2199-10-06T00-00-00Z-ED-12.json",
    "updated": "edited",
    "obj_id": "https://doi.org/10.987654321/batman",
    "source_token": "e9f90a26-d032-4e35-8b00-488520a99aba",
    "occurred_at": "2017-03-12T05:08:45Z",
    "subj_id": "http://www.citeulike.org/user/aAculuser1u/article/28124311",
    "id": "358d73b3-7edb-44fa-9b07-cf133a5a519d",
    "evidence_record": "https://evidence.eventdata.crossref.org/evidence/21991112aad9a6a7-50ef-45c0-803b-f4fa36af82eb",
    "action": "add",
    "subj": {
      "pid": "http://www.citeulike.org/user/aAculuser1u/article/28124311",
      "work-type": "webpage",
      "url": "http://www.citeulike.org/user/aAculuser1u/article/28124311"
    },
    "source_id": "web",
    "obj": {
      "pid": "https://doi.org/10.987654321/batman",
      "url": "http://dx.doi.org/10.987654321/batman"
    },
    "timestamp": "2017-03-12T05:09:53Z",
    "updated_date": "2017-10-18T14:31:20.783Z",
    "relation_type_id": "mentions"
  },
  {
    "terms": "https://doi.org/10.13011/CED-terms-of-use",
    "updated_reason": "https://evidence.eventdata.crossref.org/announcements/2199-10-06T00-00-00Z-ED-12.json",
    "updated": "edited",
    "obj_id": "https://doi.org/10.987654321/batman",
    "source_token": "e9f90a26-d032-4e35-8b00-488520a99aba",
    "occurred_at": "2017-03-12T05:08:45Z",
    "subj_id": "http://www.citeulike.org/user/aAculuser1u/article/28124311",
    "id": "5746c169-be9a-4c59-9f0a-f4d53d580210",
    "evidence_record": "https://evidence.eventdata.crossref.org/evidence/21991112aad9a6a7-50ef-45c0-803b-f4fa36af82eb",
    "action": "add",
    "subj": {
      "pid": "http://www.citeulike.org/user/aAculuser1u/article/28124311",
      "work-type": "webpage",
      "url": "http://www.citeulike.org/user/aAculuser1u/article/28124311"
    },
    "source_id": "web",
    "obj": {
      "pid": "https://doi.org/10.987654321/batman",
      "url": "http://dx.doi.org/10.987654321/batman"
    },
    "timestamp": "2017-03-12T05:09:53Z",
    "updated_date": "2017-10-18T14:31:19.059Z",
    "relation_type_id": "mentions"
  },
  {
    "license": "https://creativecommons.org/publicdomain/zero/1.0/",
    "obj_id": "https://doi.org/10.987654321/wors.911/",
    "source_token": "bbd00154-6ad5-43e0-bd63-086cc5e15be0",
    "occurred_at": "2017-01-11T03:04:23Z",
    "subj_id": "https://doi.org/10.123456789/10101010",
    "id": "c8791a48-42ff-43a8-b89b-a27d565dd6e0",
    "terms": "https://doi.org/10.13011/CED-terms-of-use",
    "message_action": "create",
    "source_id": "datacite",
    "timestamp": "2017-03-30T06:12:35Z",
    "relation_type_id": "references"
  },
  {
    "license": "https://creativecommons.org/publicdomain/zero/1.0/",
    "obj_id": "https://doi.org/10.987654321/wors.142",
    "source_token": "bbd00154-6ad5-43e0-bd63-086cc5e15be0",
    "occurred_at": "2016-12-09T14:45:00Z",
    "subj_id": "https://doi.org/10.123456789/mendel.589100",
    "id": "ac2ba88b-5eed-463a-9d75-f04aa033e788",
    "terms": "https://doi.org/10.13011/CED-terms-of-use",
    "message_action": "create",
    "source_id": "datacite",
    "timestamp": "2017-03-30T07:51:26Z",
    "relation_type_id": "is_supplement_to"
  },
  {
    "license": "https://creativecommons.org/publicdomain/zero/1.0/",
    "obj_id": "https://doi.org/10.987654321/jophd.lati",
    "source_token": "bbd00154-6ad5-43e0-bd63-086cc5e15be0",
    "occurred_at": "2013-06-24T16:55:05Z",
    "subj_id": "https://doi.org/10.123456789/atree.88888",
    "id": "f7d9d7c9-23c6-43a9-ba77-2a84a3226d87",
    "terms": "https://doi.org/10.13011/CED-terms-of-use",
    "message_action": "create",
    "source_id": "datacite",
    "timestamp": "2017-03-30T15:28:38Z",
    "relation_type_id": "is_referenced_by"
  },
  {
    "license": "https://creativecommons.org/publicdomain/zero/1.0/",
    "terms": "https://doi.org/10.13011/CED-terms-of-use",
    "updated_reason": "https://evidence.eventdata.crossref.org/announcements/2199-10-06T00-00-00Z-ED-12.json",
    "updated": "edited",
    "obj_id": "https://doi.org/10.987654321/abcd.123",
    "source_token": "f3b80e7e-619d-4da3-8804-8367f7c2571a",
    "occurred_at": "2016-09-21T13:53:12Z",
    "subj_id": "http://blog.efpsa.org/2189/09/09/trying-to-do-your-job-a-pleb/",
    "id": "73b50cca-1812-4ebb-98e1-98e3de25e1bf",
    "evidence_record": "https://evidence.eventdata.crossref.org/evidence/21991010-reddit-links-b7b6531b-c4cc-48c7-a535-2cdae6627c97",
    "action": "add",
    "subj": {
      "pid": "http://blog.efpsa.org/2189/09/09/trying-to-do-your-job-a-pleb/",
      "url": "http://blog.efpsa.org/2189/09/09/trying-to-do-your-job-a-pleb/"
    },
    "source_id": "reddit-links",
    "obj": {
      "pid": "https://doi.org/10.987654321/abcd.123",
      "url": "http://jeps.efpsa.org/articles/10.987654321/abcd.123/"
    },
    "timestamp": "2017-04-10T15:52:04Z",
    "updated_date": "2017-10-13T16:44:22.118Z",
    "relation_type_id": "discusses"
  },
  {
    "license": "https://creativecommons.org/publicdomain/zero/1.0/",
    "terms": "https://doi.org/10.13011/CED-terms-of-use",
    "updated_reason": "https://evidence.eventdata.crossref.org/announcements/2199-10-06T00-00-00Z-ED-12.json",
    "updated": "edited",
    "obj_id": "https://doi.org/10.987654321/wors.lado",
    "source_token": "39aad6d1-0f1a-4e0f-846d-2ff98acbb635",
    "occurred_at": "2017-04-11T13:07:02Z",
    "subj_id": "https://metarabbit.wordpress.com/2199/11/01/just-because-you-say-you-support-thought-it-doesnt-mean-you-can-think/",
    "id": "61f752b9-9712-4534-b9df-f923e3863bd6",
    "evidence_record": "https://evidence.eventdata.crossref.org/evidence/21991011-newsfeed-45c53433-de34-414c-841d-d043ae358cf1",
    "action": "add",
    "subj": {
      "pid": "https://metarabbit.wordpress.com/2199/11/01/just-because-you-say-you-support-thought-it-doesnt-mean-you-can-think/",
      "type": "post-weblog",
      "title": "Just because you say you support thought it doesnt mean you canthink?",
      "url": "https://metarabbit.wordpress.com/2199/11/01/just-because-you-say-you-support-thought-it-doesnt-mean-you-can-think/"
    },
    "source_id": "newsfeed",
    "obj": {
      "pid": "https://doi.org/10.987654321/wors.lado",
      "url": "http://dx.doi.org/10.987654321/wors.lado"
    },
    "timestamp": "2017-04-11T13:31:23Z",
    "updated_date": "2017-10-12T15:51:12.778Z",
    "relation_type_id": "discusses"
  },
  {
    "license": "https://creativecommons.org/publicdomain/zero/1.0/",
    "terms": "https://doi.org/10.13011/CED-terms-of-use",
    "updated_reason": "https://evidence.eventdata.crossref.org/announcements/2199-10-06T00-00-00Z-ED-12.json",
    "updated": "edited",
    "obj_id": "https://doi.org/10.987654321/wors.lado",
    "source_token": "39aad6d1-0f1a-4e0f-846d-2ff98acbb635",
    "occurred_at": "2017-04-11T13:07:02Z",
    "subj_id": "https://metarabbit.wordpress.com/2199/11/01/just-because-you-say-you-support-thought-it-doesnt-mean-you-can-think/",
    "id": "fb8852a0-c9eb-4f79-9d07-88bd32b27ca4",
    "evidence_record": "https://evidence.eventdata.crossref.org/evidence/21991011-newsfeed-45c53433-de34-414c-841d-d043ae358cf1",
    "action": "add",
    "subj": {
      "pid": "https://metarabbit.wordpress.com/2199/11/01/just-because-you-say-you-support-thought-it-doesnt-mean-you-can-think/",
      "type": "post-weblog",
      "title": "Just because you say you support thought it doesnt mean you canthink?",
      "url": "https://metarabbit.wordpress.com/2199/11/01/just-because-you-say-you-support-thought-it-doesnt-mean-you-can-think/"
    },
    "source_id": "newsfeed",
    "obj": {
      "pid": "https://doi.org/10.987654321/wors.lado",
      "url": "http://dx.doi.org/10.987654321/wors.lado"
    },
    "timestamp": "2017-04-11T13:31:24Z",
    "updated_date": "2017-10-12T15:51:12.979Z",
    "relation_type_id": "discusses"
  },  {
    "license": "https://creativecommons.org/licenses/by-sa/4.0/",
    "obj_id": "https://doi.org/10.987654321/wors.sub",
    "source_token": "4a4ae95e-857d-45cc-8c0e-0b604349430e",
    "occurred_at": "2013-11-12T15:52:30Z",
    "subj_id": "https://academia.stackexchange.com/a/28101",
    "id": "5e6e3a57-3dea-4d77-9750-5d9852923179",
    "evidence_record": "https://evidence.eventdata.crossref.org/evidence/21991013-stackexchange-04e13616-c49e-53f5-9662-787b5df41c61",
    "terms": "https://doi.org/10.13011/CED-terms-of-use",
    "action": "add",
    "subj": {
      "pid": "https://academia.stackexchange.com/a/28101",
      "title": "This was actually a really interesting question",
      "issued": "2013-11-12T15:52:30Z",
      "type": "comment",
      "author": {
        "url": "https://academia.stackexchange.com/users/7991/dseuser1n",
        "name": "dgraziotin",
        "id": 7112
      }
    },
    "source_id": "stackexchange",
    "obj": {
      "pid": "https://doi.org/10.987654321/wors.sub",
      "url": "https://doi.org/10.987654321/wors.sub"
    },
    "timestamp": "2017-04-13T20:01:56Z",
    "relation_type_id": "discusses"
  },
  {
    "license": "https://creativecommons.org/licenses/by-sa/4.0/",
    "obj_id": "https://doi.org/10.987654321/wors.sub",
    "source_token": "4a4ae95e-857d-45cc-8c0e-0b604349430e",
    "occurred_at": "2013-11-12T15:52:30Z",
    "subj_id": "https://academia.stackexchange.com/a/28101",
    "id": "db05b725-027e-53ce-b7af-828dcbab0680",
    "evidence_record": "https://evidence.eventdata.crossref.org/evidence/21991013-stackexchange-04e13616-c49e-53f5-9662-787b5df41c61",
    "terms": "https://doi.org/10.13011/CED-terms-of-use",
    "action": "add",
    "subj": {
      "pid": "https://academia.stackexchange.com/a/28101",
      "title": "This was actually a really interesting question",
      "issued": "2013-11-12T15:52:30Z",
      "type": "comment",
      "author": {
        "url": "https://academia.stackexchange.com/users/7991/dseuser1n",
        "name": "dgraziotin",
        "id": 7112
      }
    },
    "source_id": "stackexchange",
    "obj": {
      "pid": "https://doi.org/10.987654321/wors.sub",
      "url": "http://dx.doi.org/10.987654321/wors.sub"
    },
    "timestamp": "2017-04-13T20:01:56Z",
    "relation_type_id": "discusses"
  },
  {
    "license": "https://creativecommons.org/licenses/by-sa/4.0/",
    "obj_id": "https://doi.org/10.987654321/wors.sub",
    "source_token": "4a4ae95e-857d-45cc-8c0e-0b604349430e",
    "occurred_at": "2013-11-12T15:52:30Z",
    "subj_id": "https://academia.stackexchange.com/a/28101",
    "id": "006f3a57-2b31-4917-8de1-7d17b8137e86",
    "evidence_record": "https://evidence.eventdata.crossref.org/evidence/21991013-stackexchange-04e13616-c49e-53f5-9662-787b5df41c61",
    "terms": "https://doi.org/10.13011/CED-terms-of-use",
    "action": "add",
    "subj": {
      "pid": "https://academia.stackexchange.com/a/28101",
      "title": "This was actually a really interesting question",
      "issued": "2013-11-12T15:52:30Z",
      "type": "comment",
      "author": {
        "url": "https://academia.stackexchange.com/users/7991/dseuser1n",
        "name": "dgraziotin",
        "id": 7112
      }
    },
    "source_id": "stackexchange",
    "obj": {
      "pid": "https://doi.org/10.987654321/wors.sub",
      "url": "http://dx.doi.org/10.987654321/wors.sub"
    },
    "timestamp": "2017-04-13T20:01:56Z",
    "relation_type_id": "discusses"
  },
  {
    "license": "https://creativecommons.org/publicdomain/zero/1.0/",
    "terms": "https://doi.org/10.13011/CED-terms-of-use",
    "updated_reason": "https://evidence.eventdata.crossref.org/announcements/2199-10-06T00-00-00Z-ED-12.json",
    "updated": "edited",
    "obj_id": "https://doi.org/10.987654321/ouioui.01",
    "source_token": "f3b80e7e-619d-4da3-8804-8367f7c2571a",
    "occurred_at": "2017-04-18T15:50:11Z",
    "subj_id": "https://en.wikipedia.org/wiki/Some_guy",
    "id": "34d33d6d-b68f-49b7-9f2a-e597ec6271c9",
    "evidence_record": "https://evidence.eventdata.crossref.org/evidence/21991019-reddit-links-784f84be-6ae6-4f23-893b-9da25b15f100",
    "action": "add",
    "subj": {
      "pid": "https://en.wikipedia.org/wiki/Some_guy",
      "url": "https://en.wikipedia.org/wiki/Some_guy"
    },
    "source_id": "reddit-links",
    "obj": {
      "pid": "https://doi.org/10.987654321/ouioui.01",
      "url": "https://doi.org/10.987654321/ouioui.01"
    },
    "timestamp": "2017-04-19T12:24:25Z",
    "updated_date": "2017-10-13T17:48:23.728Z",
    "relation_type_id": "discusses"
  },
  {
    "license": "https://creativecommons.org/publicdomain/zero/1.0/",
    "terms": "https://doi.org/10.13011/CED-terms-of-use",
    "updated_reason": "https://evidence.eventdata.crossref.org/announcements/2199-10-06T00-00-00Z-ED-12.json",
    "updated": "edited",
    "obj_id": "https://doi.org/10.987654321/wors.lado",
    "source_token": "39aad6d1-0f1a-4e0f-846d-2ff98acbb635",
    "occurred_at": "2017-05-02T12:36:44Z",
    "subj_id": "https://metarabbit.wordpress.com/2199/09/09/i-tried-to-learn-you-a-reference/",
    "id": "5f95e9f4-765d-42fc-8469-53a708c37cbf",
    "evidence_record": "https://evidence.eventdata.crossref.org/evidence/21990912-newsfeed-2b9ac3d5-2794-425f-a365-1a21cd23a0d8",
    "action": "add",
    "subj": {
      "pid": "https://metarabbit.wordpress.com/2199/09/09/i-tried-to-learn-you-a-reference/",
      "type": "post-weblog",
      "title": "I tried to learn you a reference",
      "url": "https://metarabbit.wordpress.com/2199/09/09/i-tried-to-learn-you-a-reference/"
    },
    "source_id": "newsfeed",
    "obj": {
      "pid": "https://doi.org/10.987654321/wors.lado",
      "url": "http://dx.doi.org/10.987654321/wors.lado"
    },
    "timestamp": "2017-05-02T16:34:43Z",
    "updated_date": "2017-10-12T16:17:14.740Z",
    "relation_type_id": "discusses"
  }
]


expected_valid = [
    {
        'origin': Origins.twitter,
        'uri_id': 4,
        'external_id': 'f1e98c3a-97b7-48be-849d-74a8929d5b79',
        'provider': 2,
        'created_at': datetime.datetime(2017, 2, 18, 1, 35, 24, tzinfo=tzutc()),
        'scrape_id': 0,
        'subject_id': 'http://twitter.com/asTwitteruser1gz/statuses/000000000000000001'
    }, {
        'origin': Origins.twitter,
        'uri_id': 4,
        'external_id': '19aebdf1-5a0e-4ca0-8602-875283a05f32',
        'provider': 2,
        'created_at': datetime.datetime(2017, 2, 20, 8, 44, 25, tzinfo=tzutc()),
        'scrape_id': 0,
        'subject_id': 'http://twitter.com/cRTwitteruser32x/statuses/000000000000000003'
    }, {
        'origin': Origins.twitter,
        'uri_id': 2,
        'external_id': '409f6320-0782-4dad-ac18-cc1f8caf2b59',
        'provider': 2,
        'created_at': datetime.datetime(2017, 2, 20, 10, 35, 26, tzinfo=tzutc()),
        'scrape_id': 0,
        'subject_id': 'http://twitter.com/emTwitteruser5av/statuses/000000000000000005'
    }, {
        'origin': Origins.wordpressdotcom,
        'uri_id': 6,
        'external_id': 'bf2bdc5d-c4a6-4f6d-aca7-7cdcde9cf928',
        'provider': 2,
        'created_at': datetime.datetime(2017, 4, 6, 15, 51, 53, tzinfo=tzutc()),
        'scrape_id': 0,
        'subject_id': 'https://jwpuser1s.wordpress.com/2199/11/01/open/'
    }, {
        'origin': Origins.wordpressdotcom,
        'uri_id': 6,
        'external_id': '2ce25673-09b4-4dfb-8836-72e2dfe63a72',
        'provider': 2,
        'created_at': datetime.datetime(2017, 4, 6, 15, 51, 53, tzinfo=tzutc()),
        'scrape_id': 0,
        'subject_id': 'https://jwpuser1s.wordpress.com/2199/11/01/open/'
    }, {
        'origin': Origins.wordpressdotcom,
        'uri_id': 6,
        'external_id': '2bf67e8f-140c-4427-aac6-0b0d04d09d75',
        'provider': 2,
        'created_at': datetime.datetime(2017, 4, 6, 15, 51, 53, tzinfo=tzutc()),
        'scrape_id': 0,
        'subject_id': 'https://jwpuser1s.wordpress.com/2199/11/01/open/'
    }, {
        'origin': Origins.wikipedia,
        'uri_id': 10,
        'external_id': '4d4d1f8d-36c1-4294-b02a-54393188a0c0',
        'provider': 2,
        'created_at': datetime.datetime(2017, 4, 11, 14, 15, 56, tzinfo=tzutc()),
        'scrape_id': 0,
        'subject_id': 'https://en.wikipedia.org/wiki/Clay_Soldiers_Group'
    }, {
        'origin': Origins.wikipedia,
        'uri_id': 10,
        'external_id': 'dedcc16c-885c-492d-8ddf-522c4a85b580',
        'provider': 2,
        'created_at': datetime.datetime(2017, 4, 11, 14, 15, 56, tzinfo=tzutc()),
        'scrape_id': 0,
        'subject_id': 'https://en.wikipedia.org/wiki/Clay_Soldiers_Group'
    }, {
        'origin': Origins.wikipedia,
        'uri_id': 8,
        'external_id': 'dfbe4c00-de84-453c-8939-a7ed45b7a891',
        'provider': 2,
        'created_at': datetime.datetime(2017, 4, 11, 14, 50, 18, tzinfo=tzutc()),
        'scrape_id': 0,
        'subject_id': 'https://en.wikipedia.org/wiki/Conflict_Caused_Unknown_Truths(2991/932028)'
    }, {
        'origin': Origins.hypothesis,
        'uri_id': 2,
        'external_id': '43531cb9-d3c2-45fb-a8de-48815bdc173c',
        'provider': 2,
        'created_at': datetime.datetime(2016, 5, 17, 7, 11, 37, tzinfo=tzutc()),
        'scrape_id': 0,
        'subject_id': 'https://hypothes.is/a/sehIFMsJEzzl3tU6NUdj'
    }, {
        'origin': Origins.hypothesis,
        'uri_id': 2,
        'external_id': '52e3e202-a5b7-410d-a91f-9dd4ee593d7f',
        'provider': 2,
        'created_at': datetime.datetime(2016, 7, 5, 20, 25, 49, tzinfo=tzutc()),
        'scrape_id': 0,
        'subject_id': 'https://hypothes.is/a/LGtG52kTmSz5lgo8MzAu89'
    }, {
        'origin': Origins.hypothesis,
        'uri_id': 2,
        'external_id': '33d8dacd-a6e1-4934-8daf-25351759592f',
        'provider': 2,
        'created_at': datetime.datetime(2016, 7, 5, 19, 33, 37, tzinfo=tzutc()),
        'scrape_id': 0,
        'subject_id': 'https://hypothes.is/a/S6j5OG7fJ1i0Gc6ITJthoT'
    }
]

prebuild_expected_division = [  # How predbuild should split events in demo data
    (4, ['twitter']),
    (2, ['hypothesis', 'twitter']),
    (6, ['wordpressdotcom']),
    (10, ['wikipedia']),
    (8, ['wikipedia'])
]


build_events_input = (
    4,
    Origins.twitter,
    [
        {
            'origin': Origins.twitter,
            'uri_id': 4,
            'external_id': 'f1e98c3a-97b7-48be-849d-74a8929d5b79',
            'provider': 2,
            'created_at': datetime.datetime(2017, 2, 18, 1, 35, 24, tzinfo=tzutc()),
            'scrape_id': 0,
            'subject_id': 'http://twitter.com/asTwitteruser1gz/statuses/000000000000000001'
        }, {
            'origin': Origins.twitter,
            'uri_id': 4,
            'external_id': '19aebdf1-5a0e-4ca0-8602-875283a05f32',
            'provider': 2,
            'created_at': datetime.datetime(2017, 2, 20, 8, 44, 25, tzinfo=tzutc()),
            'scrape_id': 0,
            'subject_id': 'http://twitter.com/cRTwitteruser32x/statuses/000000000000000003'
        }
    ],
)

expected_build_type_profile = [
    type(Event()),
    type(Event()),
    type(RawEvent()),
    type(RawEvent()),
]
