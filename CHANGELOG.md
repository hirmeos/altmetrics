# Changelog

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]


## [0.4.7] - 2019-05-07
### Changed
 - Create separate supervisord file for each each plugin task.
 

## [0.4.4 - 0.4.6] - 2019-05-04
### Changed
 - Apply fixes to celery task and queue settings. 


## [0.4.3] - 2019-05-04
### Changed
 - Assign queue and worker to each plugin task
 

## [0.4.2] - 2019-04-28
### Added
 - Jira step added to CI


## [0.4.1] - 2019-04-27
### Changed
 - Upgraded to Python 3.8
 - Updated requirements 


## [0.3.27] - 2019-12-01
### Changed
 - Updated docs to point to operas.eu URLs
 - Updated docs to point to new storage bucket for the CDN
  

## [0.3.26] - 2019-12-01
### Added
 - Added changelog
 

## [0.3.24] - 2019-12-01

### Added
 - Re-enabled crossref event data plugin
 - Added timeout for requests to Crossref Event Data


## [0.3.23] - 2019-11-10
### Changed
 - Improved Sentry version in Gitlab CI


## [0.3.21] - 2019-09-03
### Changed
 - Updated Dockerfile with workers-specific Supervisor conf


## [0.3.20] - 2019-09-03
### Changed
 - Updated requirements
### Removed 
 - Removed Crossref cited-by plugin


## [0.3.17] - 2019-09-03
### Changed
 - Staggered queries when pulling metrics


## [0.3.16] - 2019-09-02
### Changed
 - Split Celery config into to dedicated Supervisord file


## [0.3.15] - 2019-09-02
### Changed
 - Mixed pep8 fixes


## [0.3.14] - 2019-08-30
### Added
 - Expanded unit tests


## [0.3.13] - 2019-08-28
### Added
 - Extracted up/hirmeos-specific values into environmental variables
### Changed
 - Moved license to root


## [0.3.12] - 2019-08-19
### Added
 - Added MIT license
 - Improved CI build with Kaniko
### Changed
 - Updated requirements
### Removed
 - Replaced nameko with an API call


## [0.3.11] - 2019-07-17
### Changed
 - Disabled token lifespan


## [0.3.10] - 2019-06-28
### Changed
 - Updated widget docs


## [0.3.9] - 2019-06-28
### Changed
 - Updated wordpressdotcom measure


## [0.3.8] - 2019-06-28
### Changed
 - Updated demo widget support 


## [0.3.7] - 2019-06-27
### Changed
 - Increased token lifespan


## [0.3.6] - 2019-06-27
### Changed
 - Updated tokens logic
 - Updated admin logic
 - match tokens-api response for post requests
### Fixed
 - Fix typo in acct schema


## [0.3.4] - 2019-06-25
### Changed
 - Rework logic to send events to new metrics API


## [0.3.3] - 2019-06-25
### Changed
 - Updated measure names to match new Metrics-API schema


## [0.3.2] - 2019-06-18
### Changed
 - Set strict_slashes to false for URL routing


## [0.3.1] - 2019-06-14
### Fixed
 - Changed page_size to per_page (typo)


## [0.3.0] - 2019-06-14
### Added
 - Added demo pages for widget
 - Added last_updated field to Event table
 - Added logging to capture error info during doi registration
 - Added widget documentation
 - API endpoint for a single DOI
 - Added auto-update for helm chart building
 - Added documentation to set up and run the altmetrics service 
 - Added Flake8 configuration
 - Added gitlab config
 - Added nameko dispatcher to send metrics to the Metrics-API
 - Added task: send-data-to-metrics-api
 - Added tests in CI
 - Added tests to Tox command
 - Added Twitter client
 - Query urls for hypothesis annotations 
 - Schedule send metrics to metrics api
 - Set celery beat schedule to send metrics to the metrics-api
### Changed
 - Apply pagination to uriset 
 - Allow urls with underscores
 - Disable crossref_event_data plugin
 - Fix celery tasks not registering
 - lock database for Uri being updated by different plugins
 - Updated celery config in supervisord
 - Take rate-limitations into account when querying twitter
 - Twitter plugin: Revert to TwitterSearch client
 - Updated nameko config
 - Updated nameko to fix PyYAML security concerns
 - Updated requirements
 - Updated twitter plugin logic
 - Updated wikipedia requirements
### Fixed
 - Attempt to resolve sentry retry error spamming
 - Depreciate PyYAML version to fix nameko
 - Handle additional wikimedia links
 - Handle invalid/deleted wikipedia events
 - Handle RawEvent integrity issues
 - Improved Sentry release handling
 - Tidy up import
### Removed
 - Remove celery result backend


## [0.2.0] - 2019-02-14
### Changed
 - Refactor code 
 - Restructure database


## [0.1.0] - 2019-02-14
 ### (Pending)
