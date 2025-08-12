# OTC Resource Monitor

FunctionGraph function for automated resource reports via email.

## Features
- Lists all resources: ECS, RDS, OBS, EVS, VPC, Subnets, DMS, DCS, APIG, CCE
- HTML email report
- Timer trigger for automated reports

## Quick Setup

### 1. Create SMN Topic
- SMN → Create Topic → `resource-monitor`
- Add Subscription → Email → Your email address
- Confirm subscription email

### 2. Create Agency
- IAM → Agencies → Create Agency
- Type: `Cloud service` → `FunctionGraph`
- Add permissions:
  - `ECS FullAccess`
  - `RDS ReadOnlyAccess` 
  - `EVS ReadOnlyAccess`
  - `VPC ReadOnlyAccess`
  - `DMS ReadOnlyAccess`
  - `DCS ReadOnlyAccess`
  - `APIG ReadOnlyAccess`
  - `CCE ReadOnlyAccess`
  - `SMN FullAccess`

### 3. Deploy Function
```bash
zip -r function.zip index.py requirements.txt src/
```

- FunctionGraph → Create Function
- Runtime: `Python 3.9`
- Handler: `index.handler`
- Agency: Select created agency
- Memory: `128 MB`
- Timeout: `30s`
- Upload ZIP

### 4. Environment Variable
- `SMN_TOPIC_URN`: urn:smn:eu-de:PROJECT_ID:resource-monitor

### 5. Timer (optional)
- Triggers → Timer → `0 8 * * *` (daily at 8 AM)

