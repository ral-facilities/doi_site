# DOI System Tests

These tests are designed to run on a local service that is configured to point
to the DataCite test service.

N.B. Ensure the service is pointing at the test service.

## Prerequisites

- A locally running service pointing to the DataCite test service
- A group `TEST` added via the admin interface
- A test user as defined [here](__init__.py) added via the admin interface
- The test user should be in the `TEST` group

## Running The Tests

```
python test_all.py
```
