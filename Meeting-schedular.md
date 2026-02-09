# Meeting Scheduler - User Journey

## Main Booking Flow

### Step 1: Select Advisor
- **API:** `GET /advisors`
- **Auth:** `Authorization: Bearer <token>`
- **Action:** Display list of advisors for selection

**Response (200):**
```json
{
  "advisors": [
    {
      "id": "adv-001",
      "name": "Advisor Name",
      "timezone": "Asia/Kolkata"
    }
  ]
}
```

### Step 2: View Availability
- **API:** `GET /advisors/{advisorId}/availability?startDate=YYYY-MM-DD&endDate=YYYY-MM-DD`
- **Auth:** `Authorization: Bearer <token>`
- **Action:** Display calendar with available time slots (30 min / 60 min)

**Response (200):**
```json
{
  "advisorId": "adv-001",
  "availableSlots": [
    {
      "startDateTime": "2026-02-10T09:00:00Z",
      "durationMinutes": 30
    },
    {
      "startDateTime": "2026-02-10T09:30:00Z",
      "durationMinutes": 60
    }
  ]
}
```

### Step 3: Book Meeting
- **API:** `POST /meetings`
- **Auth:** `Authorization: Bearer <token>`
- **Action:** Create booking with selected slot, duration, and attendee details
- **Returns:** Meeting confirmation

**Request:**
```json
{
  "advisorId": "adv-001",
  "startDateTime": "2026-02-10T09:00:00Z",
  "durationMinutes": 30,
  "attendee": {
    "name": "John Doe",
    "email": "john.doe@example.com"
  },
  "title": "Consultation"
}
```

**Response (201):**
```json
{
  "meetingId": "mtg-001",
  "advisorId": "adv-001",
  "startDateTime": "2026-02-10T09:00:00Z",
  "endDateTime": "2026-02-10T09:30:00Z",
  "durationMinutes": 30,
  "attendee": {
    "name": "John Doe",
    "email": "john.doe@example.com"
  },
  "title": "Consultation",
  "status": "confirmed"
}
```

---

## Additional Flows

### View My Meetings
- **API:** `GET /meetings?attendeeEmail=email@example.com`
- **Auth:** `Authorization: Bearer <token>`
- **Action:** List user's booked meetings

**Response (200):**
```json
{
  "meetings": [
    {
      "meetingId": "mtg-001",
      "advisorId": "adv-001",
      "startDateTime": "2026-02-10T09:00:00Z",
      "endDateTime": "2026-02-10T09:30:00Z",
      "status": "confirmed"
    }
  ]
}
```

### View Meeting Details
- **API:** `GET /meetings/{meetingId}`
- **Auth:** `Authorization: Bearer <token>`
- **Action:** Show meeting information

**Response (200):**
```json
{
  "meetingId": "mtg-001",
  "advisorId": "adv-001",
  "startDateTime": "2026-02-10T09:00:00Z",
  "endDateTime": "2026-02-10T09:30:00Z",
  "durationMinutes": 30,
  "attendee": {
    "name": "John Doe",
    "email": "john.doe@example.com"
  },
  "title": "Consultation",
  "status": "confirmed"
}
```

### Reschedule Meeting
- **API:** `PATCH /meetings/{meetingId}`
- **Auth:** `Authorization: Bearer <token>`
- **Action:** Update meeting time/duration

**Request (example):**
```json
{
  "startDateTime": "2026-02-10T10:00:00Z",
  "durationMinutes": 60
}
```

**Response (200):**
```json
{
  "meetingId": "mtg-001",
  "advisorId": "adv-001",
  "startDateTime": "2026-02-10T10:00:00Z",
  "endDateTime": "2026-02-10T11:00:00Z",
  "durationMinutes": 60,
  "status": "confirmed"
}
```

### Cancel Meeting
- **API:** `DELETE /meetings/{meetingId}`
- **Auth:** `Authorization: Bearer <token>`
- **Action:** Cancel booking and free up slot

**Response (204):**
```json
{}
```

---

## API Summary

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/advisors` | GET | List all advisors |
| `/advisors/{advisorId}` | GET | Get advisor details |
| `/advisors/{advisorId}/availability` | GET | Get available time slots |
| `/meetings` | POST | Book a meeting |
| `/meetings` | GET | List meetings (with filters) |
| `/meetings/{meetingId}` | GET | Get meeting details |
| `/meetings/{meetingId}` | PATCH | Update meeting |
| `/meetings/{meetingId}` | DELETE | Cancel meeting |
